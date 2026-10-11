# CLASSIFY: L1
"""cache-anchor 域限条款 v0.3 可执行核查器（EXT09② M3 试点 · PIVOT-01 WS-27）。

唯一规范源：board/CACHE-ANCHOR-CLAUSE-DRAFT-01.md（候选案 v0.3 @be48a770dc0e）。
本核查器实现 v0.3 文本的机器可强制部分：

  * §0.1 默认拒绝律：缺省 PENDING；BLOCKED 优先于 DONE；禁止缺席推理。
  * §2.1 热验证轨 FAIL 语义（rc≠0 ⇒ FAIL，不得转 fallthrough）——第五态。
  * §2.3 DONE ⟺ (C1 ∧ C2 ∧ C3) ∧ C4 显式合取，无任何析取豁免。
  * §2.4 B1–B7 BLOCKED 触发器优先级表（高优先级遮蔽低优先级，登记最高命中项），
    各带 recoverable / retry_after 缺省值；B7 = ③§4a 追溯降级/推翻（信任源失信）。
  * §2.4 退出路径状态迁移：BLOCKED → 重验 → PENDING → DONE/拒绝；
    禁止 BLOCKED 直达 DONE，禁止 DONE 静默改写（仅判定席复议撤销且留痕）。
  * §2.5 fallthrough 存在性证明条目（C3 组成部分）。
  * §3.1 anchor_only 强制标注：缺标注 → REJECTED（拒绝受理）；
    anchor_only 出现在内容认证依据字段 → 违规 → 自动 BLOCKED（B2 同级）。
  * §3.2 否定例封闭清单：越权引用显式拒绝（映射 §3.1 违规处置）。
  * §3.3 抖动/不可信二分：无法归类按不可信（B2）处理。
  * §3.4 锚污染失效路径与锚反自指条款（自指锚定 → B2）。
  * §4 判别顺序：先查 §5 结构不可验证族登记（B1），再进 §2 状态机。
  * §8 状态合法集 {PENDING, DONE, FAIL, BLOCKED} × 争议层；REJECTED 为本条款
    拒绝/归档出口（§2.4 退出路径"拒绝须留痕"）。

五态机：PENDING（缺省）/ BLOCKED（优先）/ DONE / FAIL（§2.1）/ REJECTED。

CLI：
    python3 cache_anchor_check.py adjudicate <evidence.json> \
        [--anchor-ref COMMIT] [--case-id ID] [--now EPOCH_S] [--ttl S]

输出判定 JSON：{state, trigger, reason, recoverable, retry_after, violations}。

证据 JSON 模式（本核查器口径，均为机器可读字段）：
    case_id               str   必填  裁决格 id（跨案污染检查基准）
    rev_hash              str   必填  目标 rev
    anchor_ref            str   必填  证据锚定的 commit；须与 --anchor-ref 一致，否则不采
    evidence_class        str   必填  必须为 "anchor_only"（§3.1）
    run_mode              str   必填  "hot" | "cold"
    structural_unverifiable bool      §5 在册标志（B1）
    anchor_overturned     bool        ③§4a 追溯降级/推翻信号（B7）
    invalidated_by        str|null    污染失效标记（§3.4 → B2 级不可信）
    self_referential_anchor bool      锚反自指检测（§3.4 → B2）
    content_cert_use      bool        anchor_only 被引用于内容认证依据字段（§3.1 违规）
    unclassifiable_error  bool        核验异常且无法归类抖动/不可信（§3.3 → 按不可信）
    build_exit_code       int|null    fallthrough 必须为 null；非 0 ⇒ FAIL（§2.1）
    skip_requested        bool        run_mode=cold 而以 cache 缺请求跳过（B5）
    cache_coverage        {m, N}      双源核验合计命中计数（C1：须 0/N）
    dual_source           {official:{reachable,hash_match,epoch_drift_suspect},
                           relay:{...}, ts_collect, anchor_epoch}
    equivalence_ref       null|{cell_id, rev, rc, crosscheck, log_digest_match}  （C2/B3）
    verdict               str         C3 要求 "cold-fallthrough"
    result_commit         str|null    C3 证据链指针
    toolchain_version     str         §2.3(b) 必填证据字段
    env_hash              str         §2.3(b) 必填证据字段
    paired_run_id         str         §2.3(b) 必填证据字段
    fallthrough_log       {seq:int, contiguous:bool}  §2.5 事件日志条目（C3）
    b4_retry_count        int         B4 已退避次数（≥4 ⇒ 转不可恢复并上报，§2.4-2）
    ttl_s                 int         C4 TTL，缺省 86400

保守解释原则：文本歧义处一律取更严格解释（见 ws27 报告歧义清单）。
"""
import argparse
import json
import sys
import time

# ---------------------------------------------------------------- 五态机
PENDING = "PENDING"      # 缺省挂起态（§0.1-1，§1）
BLOCKED = "BLOCKED"      # 优先态（§0.1-3）
DONE = "DONE"            # §2.3 显式合取
FAIL = "FAIL"            # §2.1 rc≠0 编译裁决（第五态）
REJECTED = "REJECTED"    # §2.4 退出路径之"拒绝"；§3.1 拒绝受理
STATES = frozenset({PENDING, BLOCKED, DONE, FAIL, REJECTED})

DEFAULT_TTL_S = 86400    # §2.3 C4：TTL 缺省 24h

# ------------------------------------------------- §2.4 B1–B7 触发器优先级表
# 优先级从高到低；判定程序按序逐项核查，任一命中即落 BLOCKED 并停止后续核查
# （高优先级遮蔽低优先级，登记最高优先级命中项）。
TRIGGERS = {
    "B1": {"recoverable": False, "retry_after": None,
           "desc": "核验对象属 §5 结构不可验证族；fallthrough 不适用，转 §5 接口"},
    "B2": {"recoverable": False, "retry_after": "reanchor_wave",
           "desc": "锚完整性失败：制品哈希不符 / 源端 epoch 漂移疑似重指向 / 自指锚定 / "
                   "污染失效 / anchor_only 越权引用（§3.1 违规同级）；不可信事件（§3.3）"},
    "B3": {"recoverable": True, "retry_after": "dependency_wave",
           "desc": "C2 等价依据缺失：同 rev 无任何已完成编译裁决格或 crosscheck 共识"},
    "B4": {"recoverable": True, "retry_after": 3600,
           "desc": "双源不可达：官方 cache 与中继仓均不可达；3600s 指数退避（上限 4 次）"},
    "B5": {"recoverable": False, "retry_after": None,
           "desc": "格声明 run_mode=cold 而执行方以 cache 缺为由请求跳过"},
    "B6": {"recoverable": True, "retry_after": 0,
           "desc": "C4 时效失效（TTL 超时 / anchor_epoch 不一致 / 时效字段缺失）；立即重验"},
    "B7": {"recoverable": False, "retry_after": "reanchor_wave",
           "desc": "anchor 经 ③§4a DISPUTED 追溯降级/推翻（信任源失信/失效）；"
                   "关联缓存条目即时作废、回 PENDING 重走 §2 主链，并上报判定席"},
}
B4_MAX_RETRIES = 4       # §2.4-2：B4 退避 4 次用尽 → 转 recoverable=false 并上报


class IllegalTransition(Exception):
    """禁止的状态迁移（§0.1-4、§2.4-4）。"""


# ------------------------------------------------- 退出路径状态迁移函数
# §0.1-4：PENDING→DONE 仅经显式合取；PENDING→BLOCKED 任一触发；
#         BLOCKED→（重验通过）→PENDING 重判；禁止 DONE 静默改写。
# §2.4-4：禁止 BLOCKED 直达 DONE；禁止以重试覆盖原 BLOCKED 登记。
_LEGAL_TRANSITIONS = {
    (PENDING, PENDING): "持存（缺省）",
    (PENDING, BLOCKED): "任一 BLOCKED 触发器命中",
    (PENDING, DONE): "§2.3 显式合取 (C1∧C2∧C3)∧C4 满足且 §2.4 逐项排除完成",
    (PENDING, FAIL): "§2.1 rc≠0 编译裁决",
    (PENDING, REJECTED): "证据不予受理（§3.1 格式不合规/未锚定/跨案污染）",
    (BLOCKED, PENDING): "§2.4 退出路径：recoverable=true 重验通过，回 PENDING 重判",
    (BLOCKED, REJECTED): "§2.4-3：recoverable=false 经判定席裁决拒绝并归档（留痕）",
    (BLOCKED, BLOCKED): "重验仍触发同一或更高优先级触发器，维持 BLOCKED（退避递增）",
    (DONE, PENDING): "判定席复议撤销 / §3.4 污染追溯降级（须留痕，非静默）",
    (FAIL, PENDING): "判定席复议撤销（须留痕，非静默）",
}


def transition(current, target, *, by=None, trace=None, reverify_evidence=None):
    """状态迁移守卫。非法迁移抛 IllegalTransition（fallthrough 不可能性之外
    的第二层禁止：禁止隐式跃迁与静默改写）。

    - BLOCKED→DONE 永远禁止（§2.4-4 禁止路径）。
    - DONE/FAIL→任何状态：仅允许 →PENDING，且必须 by="adjudication_board"
      且 trace 非空（§0.1-4：仅判定席复议撤销，撤销留痕）。
    - BLOCKED→PENDING：必须附重验新证据指针（§2.4-2：重验输出新证据；
      旧登记保留，禁止覆盖）。
    """
    if current not in STATES or target not in STATES:
        raise IllegalTransition("未知状态：%r -> %r" % (current, target))
    if (current, target) == (BLOCKED, DONE):
        raise IllegalTransition("禁止路径：BLOCKED 禁止直达 DONE（§2.4-4）")
    if current in (DONE, FAIL) and current != target:
        if target != PENDING or by != "adjudication_board" or not trace:
            raise IllegalTransition(
                "禁止 DONE/FAIL 静默改写：仅判定席复议撤销且留痕可降回 PENDING（§0.1-4）")
    if (current, target) == (BLOCKED, PENDING) and not reverify_evidence:
        raise IllegalTransition("BLOCKED→PENDING 须附重验新证据指针（§2.4-2）")
    if (current, target) not in _LEGAL_TRANSITIONS:
        raise IllegalTransition("非法迁移：%s -> %s" % (current, target))
    return target


# ---------------------------------------------------------------- 判定内核
def _verdict(state, trigger=None, reason="", recoverable=None, retry_after=None,
             violations=None, extra=None):
    if state not in STATES:
        raise AssertionError("fallthrough 不可能性被破坏：非法状态 %r" % state)
    out = {
        "state": state,
        "trigger": trigger,
        "reason": reason,
        "recoverable": recoverable,
        "retry_after": retry_after,
        "violations": violations or [],
    }
    if extra:
        out.update(extra)
    return out


def _blocked(trigger, reason, violations=None, b4_retry_count=0, extra=None):
    spec = TRIGGERS[trigger]
    recoverable = spec["recoverable"]
    retry_after = spec["retry_after"]
    if trigger == "B4" and b4_retry_count >= B4_MAX_RETRIES:
        # §2.4-2：B4 退避 4 次用尽 → 转 recoverable=false 处理并上报
        recoverable = False
        reason += "；B4 退避 %d 次用尽，转 recoverable=false 并上报判定席" % b4_retry_count
    return _verdict(BLOCKED, trigger=trigger, reason=reason,
                    recoverable=recoverable, retry_after=retry_after,
                    violations=violations, extra=extra)


def _c1(ev):
    """C1（双源核验实报）：run_mode=hot 且双源核验实报 0/N（含 ts_collect）。"""
    if ev.get("run_mode") != "hot":
        return False, "run_mode 非 hot（fallthrough 以 hot 声明为前提）"
    cov = ev.get("cache_coverage") or {}
    m, n = cov.get("m"), cov.get("N")
    if not isinstance(m, int) or not isinstance(n, int) or n <= 0:
        return False, "cache 覆盖计数缺失或非法"
    if m != 0:
        return False, "双源核验实报 %d/%d（非 0/N，fallthrough 不成立）" % (m, n)
    ds = ev.get("dual_source") or {}
    if not isinstance(ds.get("ts_collect"), (int, float)):
        return False, "双源核验缺 ts_collect"
    return True, ""


def _c2(ev):
    """C2（等价依据存在性）：同 manifest 同 rev 已完成 cold/crosscheck 编译裁决
    且 rc 共识成立。空指针即不成立。"""
    ref = ev.get("equivalence_ref")
    if not ref:
        return False, "等价依据格指针为空"
    if ref.get("rev") != ev.get("rev_hash"):
        return False, "等价依据格 rev 不一致"
    if ref.get("rc") != 0:
        return False, "等价依据格 rc 共识不成立（rc=%r）" % (ref.get("rc"),)
    if not (ref.get("crosscheck") == "CROSSCHECK_OK" or ref.get("log_digest_match")):
        return False, "缺 crosscheck 共识或 log_digest 一致性证据"
    return True, ""


def _c3(ev):
    """C3（记法完整）：保留 hot 标 + verdict=cold-fallthrough + build_exit_code=null
    + result_commit 指针 + §2.5 事件日志条目就位 + §2.3(b) 必填字段。"""
    if ev.get("verdict") != "cold-fallthrough":
        return False, "verdict 未显式标 cold-fallthrough"
    if ev.get("build_exit_code") is not None:
        return False, "build_exit_code 非 null（fallthrough 不产生编译证据）"
    if not ev.get("result_commit"):
        return False, "缺 result_commit 指针"
    log = ev.get("fallthrough_log") or {}
    if not isinstance(log.get("seq"), int) or log.get("contiguous") is not True:
        return False, "§2.5 事件日志条目未就位或序号不连续（未记录视同可能已发生）"
    for f in ("toolchain_version", "env_hash", "paired_run_id"):
        if not ev.get(f):
            return False, "§2.3(b) 必填证据字段缺失：%s" % f
    return True, ""


def _c4(ev, now, ttl):
    """C4（时效成立）：ts_collect 距裁决时刻 ≤ TTL 且源端 epoch 与登记
    anchor_epoch 一致。时效字段必填，缺字段视同 C4 不成立。"""
    ds = ev.get("dual_source") or {}
    ts = ds.get("ts_collect")
    epoch = ds.get("anchor_epoch")
    if not isinstance(ts, (int, float)) or not epoch:
        return False, "时效字段缺失（ts_collect/anchor_epoch），视同 C4 不成立"
    if abs(now - ts) > ttl:
        return False, "TTL 超时：|now-ts_collect|=%ds > TTL=%ds" % (abs(now - ts), ttl)
    registered = ev.get("anchor_epoch_registered")
    if registered is not None and epoch != registered:
        return False, "anchor_epoch 漂移：核验 epoch=%r ≠ 登记 %r" % (epoch, registered)
    return True, ""


def adjudicate(ev, *, anchor_ref=None, case_id=None, now=None, ttl=None):
    """§4 判别顺序 + §0.1 判定语义总则。

    返回判定 dict；任何输入必落五态之一（fallthrough 不可能性由末尾断言
    与异常兜底共同保证，无隐式允许）。
    """
    if now is None:
        now = time.time()
    violations = []

    try:
        if not isinstance(ev, dict):
            return _verdict(REJECTED, reason="证据非 JSON 对象，拒绝受理（默认拒绝律）")
        if ttl is None:
            ttl = ev.get("ttl_s", DEFAULT_TTL_S)
        if not isinstance(ttl, (int, float)):
            ttl = DEFAULT_TTL_S

        # ---------- 受理门槛（§3.1 + anchor_only 强制 + 否定例三类）----------
        # §3.1：缺 evidence_class: "anchor_only" 标注视为格式不合规，拒绝受理。
        if ev.get("evidence_class") != "anchor_only":
            return _verdict(REJECTED,
                            reason="缺 evidence_class=anchor_only 强制标注，"
                                   "格式不合规，拒绝受理（§3.1，默认拒绝律适用）")
        # anchor_only 强制：证据须锚定到指定 commit；未锚定一律不采。
        if anchor_ref is not None and ev.get("anchor_ref") != anchor_ref:
            return _verdict(REJECTED,
                            reason="证据未锚定到指定 commit（%r ≠ %r），一律不采"
                                   % (ev.get("anchor_ref"), anchor_ref))
        if not ev.get("anchor_ref"):
            return _verdict(REJECTED, reason="证据缺 anchor_ref，未锚定，一律不采")
        # 否定例·跨案污染：证据主体非本案裁决格，显式拒绝。
        if case_id is not None and ev.get("case_id") != case_id:
            return _verdict(REJECTED,
                            reason="跨案污染：证据 case_id=%r 非本案 %r，显式拒绝"
                                   % (ev.get("case_id"), case_id))
        # 否定例·越权引用（§3.1 违规）：anchor_only 记录出现在内容认证依据字段。
        # §3.1 明文处置 = 自动 BLOCKED（B2 同级）并登记违规事件——较 REJECTED
        # 更严格且须上报，从文本。
        if ev.get("content_cert_use"):
            violations.append("anchor_only 越权引用：缓存锚证据出现在内容认证依据字段（§3.1/§3.2）")
            return _blocked("B2", "§3.1 违规：anchor_only 充任内容认证依据，"
                                  "该裁决自动落 BLOCKED（B2 同级）并登记违规事件",
                            violations=violations)

        # ---------- §2.4 BLOCKED 逐项排除核查（B1→B7，高优先级遮蔽低优先级）----------
        # §4 判别顺序：先查 §5 结构不可验证族登记册。
        if ev.get("structural_unverifiable"):
            return _blocked("B1", TRIGGERS["B1"]["desc"], violations)
        # B2 不可信族（§3.3：完整性矛盾 / 无法归类按不可信；§3.4 自指与污染失效）。
        if ev.get("self_referential_anchor"):
            violations.append("锚反自指：证据链闭环于被锚对象自身（§3.4）")
            return _blocked("B2", "检测到自指锚定，按 B2 阻断并登记违规（§3.4 锚反自指条款）",
                            violations)
        if ev.get("invalidated_by"):
            return _blocked("B2", "锚污染坐实，证据已被失效标记 invalidated_by=%r（§3.4 失效路径）"
                                  % ev.get("invalidated_by"), violations)
        ds = ev.get("dual_source") or {}
        for src in ("official", "relay"):
            s = ds.get(src) or {}
            if s.get("hash_match") is False:
                return _blocked("B2", "制品哈希与登记不符（源=%s），不可信事件（§3.3）" % src,
                                violations)
            if s.get("epoch_drift_suspect"):
                return _blocked("B2", "源端 epoch 非预期漂移疑似重指向（源=%s），不可信事件（§3.3）"
                                      % src, violations)
        if ev.get("unclassifiable_error"):
            return _blocked("B2", "核验异常无法归类抖动/不可信，按不可信处理（§3.3 判别义务）",
                            violations)
        # B3：C2 等价依据缺失。
        c2_ok, c2_why = _c2(ev)
        if not c2_ok:
            return _blocked("B3", "C2 等价依据缺失：%s；禁止以「cache 缺」单方记 DONE" % c2_why,
                            violations)
        # B4：双源不可达（核验本身无法完成）。
        off, rel = ds.get("official") or {}, ds.get("relay") or {}
        if off.get("reachable") is False and rel.get("reachable") is False:
            return _blocked("B4", TRIGGERS["B4"]["desc"], violations,
                            b4_retry_count=int(ev.get("b4_retry_count") or 0))
        # B5：cold 格以 cache 缺请求跳过。
        if ev.get("run_mode") == "cold" and ev.get("skip_requested"):
            return _blocked("B5", TRIGGERS["B5"]["desc"], violations)
        # B6：C4 时效失效（TTL 超时 / epoch 不一致 / 时效字段缺失）。
        c4_ok, c4_why = _c4(ev, now, ttl)
        if not c4_ok:
            return _blocked("B6", "C4 时效失效：%s；须重验后方可再判" % c4_why, violations)
        # B7：③§4a 追溯降级/推翻（信任源失信/失效）。
        if ev.get("anchor_overturned"):
            return _blocked("B7", TRIGGERS["B7"]["desc"], violations,
                            extra={"invalidate_entries": True,
                                   "next_state": PENDING})

        # ---------- §2.1 FAIL：编译裁决 rc≠0（不得转 fallthrough）----------
        bec = ev.get("build_exit_code")
        if isinstance(bec, int) and bec != 0:
            return _verdict(FAIL, reason="rc≠0（build_exit_code=%d）编译裁决 FAIL，"
                                         "不得转 fallthrough（§2.1）" % bec,
                            recoverable=None, retry_after=None, violations=violations)

        # ---------- §2.3 DONE ⟺ (C1∧C2∧C3)∧C4 ----------
        c1_ok, c1_why = _c1(ev)
        c3_ok, c3_why = _c3(ev)
        if c1_ok and c2_ok and c3_ok and c4_ok:
            return _verdict(DONE, reason="DONE（cold-fallthrough）：显式合取 "
                                         "(C1∧C2∧C3)∧C4 全部正证据成立，"
                                         "§2.4 触发器逐项排除完成",
                            violations=violations)
        # 合取不成立且无触发器命中 → 维持缺省 PENDING（默认拒绝律，禁止缺席推理）。
        missing = [n for n, (ok, why) in
                   (("C1", (c1_ok, c1_why)), ("C2", (c2_ok, c2_why)),
                    ("C3", (c3_ok, c3_why)), ("C4", (c4_ok, c4_why))) if not ok]
        whys = "; ".join(w for ok, w in
                         ((c1_ok, c1_why), (c2_ok, c2_why), (c3_ok, c3_why), (c4_ok, c4_why))
                         if not ok and w)
        return _verdict(PENDING, reason="显式合取不成立（%s）：%s；维持 PENDING（默认拒绝律）"
                                        % ("∧".join("¬" + m for m in missing), whys),
                        violations=violations)
    except Exception as exc:  # §0.1-3：核查无法完成 → 直接落 BLOCKED
        v = _verdict(BLOCKED, trigger=None,
                     reason="核查无法完成（内部异常 %s: %s），按 §0.1-3 落 BLOCKED"
                            % (type(exc).__name__, exc),
                     recoverable=True, retry_after=0, violations=violations)
        assert v["state"] in STATES
        return v


# ---------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="cache-anchor 域限条款 v0.3 核查器")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("adjudicate", help="对证据 JSON 作出五态判定")
    p.add_argument("evidence_json")
    p.add_argument("--anchor-ref", default=None, help="指定锚定 commit（未锚定一律不采）")
    p.add_argument("--case-id", default=None, help="本案裁决格 id（跨案污染检查）")
    p.add_argument("--now", type=float, default=None, help="裁决时刻（epoch s，缺省当前）")
    p.add_argument("--ttl", type=float, default=None, help="C4 TTL 秒（缺省 86400）")
    args = ap.parse_args(argv)

    if args.cmd == "adjudicate":
        with open(args.evidence_json, encoding="utf-8") as f:
            ev = json.load(f)
        out = adjudicate(ev, anchor_ref=args.anchor_ref, case_id=args.case_id,
                         now=args.now, ttl=args.ttl)
        assert out["state"] in STATES  # fallthrough 不可能性（无隐式允许）
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
