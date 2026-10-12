# CLASSIFY: L1
# krawczyk_ns_verify.py · EXT-WAVE-10「融」波 WS-55「Krawczyk×Galerkin」证书独立验证器
# （schema v1.0 · fail-closed · 默认拒绝律）
#
# 对象：WS-42 Lean 核显式三模态 B₃ 截断的稳态问题
#   F(u) = B₃(u)u − ν·diag(a)·u + f = 0（逐分量与 Jacobian 见证书 system 字段），
# 对证书登记的 (params, z, Y, r) 做**独立区间复算**（mpmath.iv dps=50 外向舍入）：
#   · 存在性：K(U) ⊂ int(U)（逐分量严格包含，6 个严格不等式）⟹ ∃ u* ∈ int(U), F(u*) = 0；
#   · 唯一性：ρ_hi = ‖I₃ − Y·□DF(U)‖∞ 的区间上界 < 1 ⟹ u* 在 U 内唯一
#     （压缩映射路线，Newton–Krawczyk/Rump；ws51-report §4.1）。
#
# 独立性（WS-37/WS-43 零共享代码纪律）：
#   · 本文件与 ci/krawczyk_ns_gen.py 零共享代码路径：区间核、规范实现、判定逻辑
#     全部自含重写；不 import 生成器，不读生成器中间产物（只读证书 JSON 与仓内脚本哈希）；
#   · 不使用 numpy/scipy（验证器无候选生成职责，纯 mpmath.iv 复算）；
#   · 度量比对 = 逐字符串一致（数值仅经规范路线解析为有理/区间量后比较）。
#
# 区间计算规范（与生成器各自独立实现同一规范，端点须逐比特一致）：
#   · 十进制字符串 s → Fraction(s) → iv.mpf(分子)/iv.mpf(分母)（dps=50 外向舍入）；
#   · 区间求和按下标升序从左到右，初值 iv.mpf(0)；
#   · 盒 U_i = z_i + iv.mpf([-1,1])·r；U − z 直接取 iv.mpf([-1,1])·r；
#   · F(u) 逐分量：F0 = (u1·u2 + u2·u1) + (−(ν·a0)·u0) + f0；
#     F1 = (−(u0·u2) + −(u2·u0)) + (−(ν·a1)·u1) + f1；F2 = −(ν·a2)·u2 + f2；
#     （线性化主部写作 ν·a_i 后再取负乘 u_i，与生成器 spec 逐序一致）；
#   · □DF(U) = [[−νa0, 2U2, 2U1], [−2U2, −νa1, −2U0], [0, 0, −νa2]]（逐元素区间代换）；
#   · R = I₃ − Y·□DF(U)；K_i = z_i − (Y·F(z))_i + (R·(U−z))_i；
#   · ρ 行和：rowsum_i = Σ_j iv.mpf([|R_ij.a|, |R_ij.b|])（升序），ρ_hi = max_i rowsum_i.b；
#   · margin_i = min((K_i.a − U_i.a), (U_i.b − K_i.b)) 取下端点 .a。
#
# 判定语义（fail-closed）：
#   · 任一检查 false / 字段缺失 / 异常 → 整体 FAIL，退出码 1；
#   · 缺 schema_version 拒收；major ≠ 1 → unsupported_schema 拒验（禁止静默降级）；
#   · PASS 证书：复算值与登记值逐字符串一致 + 两条件严格成立 + verdict 登记一致；
#   · FAIL 证书：box/krawczyk 必须为 null、verdict 必须为 FAIL，且对登记的
#     fail_registration.diagnostics.last_attempt 半径独立复算确认「证书两条件确实不成立」
#     （诚实失败复算确认，防止 FAIL 伪装/PASS 误废）。
#
# cert_sha256 规范化序列化规则（同 WS-37 M0 interim）：
#   json.dumps(除去 cert_sha256 的对象, sort_keys=True, separators=(",", ":"),
#              ensure_ascii=False).encode("utf-8") 的 sha256 十六进制小写。
#
# 用法：python3 ci/krawczyk_ns_verify.py CERT.json [CERT2.json ...] [--json]
#   退出码 0=全部通过；1=任一失败或异常；2=用法错误。
import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction

SUPPORTED_MAJOR = 1
IV_DPS = 50

TOP_REQUIRED = ["schema_version", "family", "claim", "case_id", "run_id", "ts_utc",
                "system", "params", "candidate", "preconditioner", "box",
                "radius_schedule", "krawczyk", "interval_engine", "verdict",
                "generator", "verifier", "cert_sha256"]


def _canon_sha256(cert_obj):
    obj = {k: v for k, v in cert_obj.items() if k != "cert_sha256"}
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _find_repo_root(cert_path, script_rel):
    d = os.path.abspath(os.path.dirname(cert_path))
    while True:
        if os.path.isfile(os.path.join(d, script_rel)):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    self_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isfile(os.path.join(self_root, script_rel)):
        return self_root
    return None


class _Checklist:
    def __init__(self):
        self.checks = []

    def add(self, name, ok, detail=""):
        self.checks.append({"check": name, "ok": bool(ok), "detail": detail})

    @property
    def ok(self):
        return all(c["ok"] for c in self.checks)


# ---------------------------------------------------------------- 独立区间核
# （与生成器同规范、独立书写；除规范常量外不复制生成器代码）

def _to_interval(s):
    """十进制字符串 → 区间（规范路线：Fraction → 分子/分母外向舍入除法）。"""
    from mpmath import iv
    q = Fraction(str(s).strip())
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def _seq_sum(terms):
    from mpmath import iv
    out = iv.mpf(0)
    for t in terms:
        out = out + t
    return out


def _residual_iv(u, nu, a, f):
    """F(u) = B₃(u)u − ν·diag(a)·u + f（区间；项序按规范）。"""
    u0, u1, u2 = u
    return [_seq_sum([u1 * u2, u2 * u1, -(nu * a[0]) * u0, f[0]]),
            _seq_sum([-(u0 * u2), -(u2 * u0), -(nu * a[1]) * u1, f[1]]),
            _seq_sum([-(nu * a[2]) * u2, f[2]])]


def _jacobian_iv(U, nu, a):
    """□DF(U)（区间；对 u 仿射，逐元素代换即精确包围）。"""
    from mpmath import iv
    U0, U1, U2 = U
    zero = iv.mpf(0)
    return [[-nu * a[0], 2 * U2, 2 * U1],
            [-2 * U2, -nu * a[1], -2 * U0],
            [zero, zero, -nu * a[2]]]


def _mmul(A, B):
    return [[_seq_sum([A[i][t] * B[t][k] for t in range(3)]) for k in range(3)]
            for i in range(3)]


def _mvec(A, v):
    return [_seq_sum([A[i][t] * v[t] for t in range(3)]) for i in range(3)]


def _krawczyk_recompute(params, z_s, Y_s, r_s):
    """独立复算 Krawczyk 全部判定量。返回 dict（区间对象与端点字符串）。"""
    from mpmath import iv
    iv.dps = IV_DPS
    nu = _to_interval(params["nu"])
    a = [_to_interval(s) for s in params["a"]]
    f = [_to_interval(s) for s in params["f"]]
    z = [_to_interval(s) for s in z_s]
    Y = [[_to_interval(s) for s in row] for row in Y_s]
    r = _to_interval(r_s)

    span = iv.mpf([-1, 1]) * r
    U = [z[i] + span for i in range(3)]
    Umz = [span, span, span]
    DFU = _jacobian_iv(U, nu, a)
    YD = _mmul(Y, DFU)
    R = [[(iv.mpf(1) if i == j else iv.mpf(0)) - YD[i][j] for j in range(3)]
         for i in range(3)]
    F_z = _residual_iv(z, nu, a, f)
    YF = _mvec(Y, F_z)
    RU = _mvec(R, Umz)
    K = [_seq_sum([z[i], -YF[i], RU[i]]) for i in range(3)]

    margins = []
    for i in range(3):
        m1 = iv.mpf(K[i].a) - iv.mpf(U[i].a)
        m2 = iv.mpf(U[i].b) - iv.mpf(K[i].b)
        margins.append(m1 if float(m1.a) <= float(m2.a) else m2)
    rowsums = [_seq_sum([iv.mpf(sorted([float(abs(R[i][j].a)), float(abs(R[i][j].b))]))
                         for j in range(3)]) for i in range(3)]
    rho_hi = max(float(rs.b) for rs in rowsums)
    y0_hi = max(float(abs(YF[i].a)) if float(abs(YF[i].a)) >= float(abs(YF[i].b))
                else float(abs(YF[i].b)) for i in range(3))
    exists = all(float(K[i].a) > float(U[i].a) and float(K[i].b) < float(U[i].b)
                 for i in range(3))
    return {
        "U": U, "K": K, "F_z": F_z, "margins": margins,
        "min_margin": min(float(m.a) for m in margins),
        "rho_hi": rho_hi, "y0_hi": y0_hi,
        "exists": exists, "uniq": rho_hi < 1.0,
        "str": {
            "U": [[repr(float(v.a)), repr(float(v.b))] for v in U],
            "K": [[repr(float(v.a)), repr(float(v.b))] for v in K],
            "F_z": [[repr(float(v.a)), repr(float(v.b))] for v in F_z],
            "margins": [repr(float(m.a)) for m in margins],
            "min_margin": repr(min(float(m.a) for m in margins)),
            "rho_hi": repr(rho_hi),
            "y0_hi": repr(y0_hi),
        },
    }


# ---------------------------------------------------------------- 检查件

def _check_schema(w, cl):
    sv = w.get("schema_version")
    if sv is None:
        cl.add("schema_version_present", False, "缺 schema_version，拒绝受理")
        return False
    cl.add("schema_version_present", True, sv)
    try:
        major_s, minor_s = str(sv).split(".")
        major, minor = int(major_s), int(minor_s)
    except Exception:
        cl.add("schema_parse", False, f"schema_version 不可解析: {sv!r}")
        return False
    cl.add("schema_parse", True, sv)
    if major != SUPPORTED_MAJOR:
        cl.add("schema_major_dispatch", False,
               f"unsupported_schema: major={major}（fail-closed，禁止静默降级）")
        return False
    cl.add("schema_major_dispatch", True,
           f"major={major} 受理" + (f"；minor={minor} 兼容受理" if minor > 0 else ""))
    return True


def _check_common(w, cl, cert_path):
    missing = [f for f in TOP_REQUIRED if f not in w]
    cl.add("required_top_fields", not missing, f"missing={missing}" if missing else "齐")
    if missing:
        return False
    cl.add("cert_sha256", _canon_sha256(w) == w["cert_sha256"], "规范化序列化复算")
    cl.add("family_shape", w.get("family") == "ns-krawczyk-stationary", str(w.get("family")))
    cl.add("claim_shape", w.get("claim") == "exists_unique_zero_in_box", str(w.get("claim")))
    eng = w["interval_engine"]
    cl.add("engine_supported",
           eng.get("name") == "mpmath.iv" and eng.get("rounding") == "outward"
           and eng.get("precision") == f"dps={IV_DPS}",
           json.dumps(eng, ensure_ascii=False))
    cl.add("params_shape",
           isinstance(w["params"].get("nu"), str)
           and len(w["params"].get("a") or []) == 3
           and len(w["params"].get("f") or []) == 3
           and len(w["candidate"].get("z") or []) == 3
           and len(w["preconditioner"].get("Y") or []) == 3
           and all(len(row) == 3 for row in w["preconditioner"].get("Y") or []),
           "nu 字符串 + a/f/z 三维 + Y 3×3")
    if not cl.ok:
        return False
    # 参数合法性：ν>0、aᵢ>0（有理比较）
    nu_q = Fraction(w["params"]["nu"])
    a_q = [Fraction(s) for s in w["params"]["a"]]
    cl.add("params_admissible", nu_q > 0 and all(q > 0 for q in a_q),
           f"nu={nu_q}, a={a_q}")
    repo = _find_repo_root(cert_path, w["generator"].get("script", ""))
    if repo is None:
        cl.add("generator_script_sha256", False,
               f"无法在仓内定位 {w['generator'].get('script')}")
        return False
    cl.add("generator_script_sha256",
           _sha256_file(os.path.join(repo, w["generator"]["script"]))
           == w["generator"].get("sha256"),
           w["generator"]["script"])
    vscript = w["verifier"].get("script")
    if os.path.isfile(os.path.join(repo, vscript or "")):
        cl.add("verifier_script_sha256",
               _sha256_file(os.path.join(repo, vscript)) == w["verifier"].get("sha256"),
               vscript)
    else:
        cl.add("verifier_script_sha256", False, f"验证器脚本缺失: {vscript}")
    return cl.ok


def _check_pass(w, cl):
    box = w["box"]
    kw = w["krawczyk"]
    cl.add("box_present", box is not None and kw is not None, "PASS 证书须携带 box+krawczyk")
    if box is None or kw is None:
        return
    cl.add("box_consistent", box.get("center") == w["candidate"]["z"]
           and isinstance(box.get("radius"), str),
           "box.center == candidate.z 且 radius 为十进制字符串")
    rec = _krawczyk_recompute(w["params"], w["candidate"]["z"],
                              w["preconditioner"]["Y"], box["radius"])
    s = rec["str"]
    cl.add("recompute_F_z", s["F_z"] == kw.get("F_z"),
           "F(z) 端点逐字符串一致" if s["F_z"] == kw.get("F_z")
           else f"复算={s['F_z']} 登记={kw.get('F_z')}")
    cl.add("recompute_U", s["U"] == kw.get("U"), "盒端点逐字符串一致")
    cl.add("recompute_K", s["K"] == kw.get("K"),
           "Krawczyk 像端点逐字符串一致" if s["K"] == kw.get("K")
           else f"复算={s['K']} 登记={kw.get('K')}")
    cl.add("recompute_margins", s["margins"] == kw.get("margins")
           and s["min_margin"] == kw.get("min_margin"),
           f"复算 min_margin={s['min_margin']} 登记={kw.get('min_margin')}")
    cl.add("recompute_rho", s["rho_hi"] == kw.get("rho_hi"),
           f"复算={s['rho_hi']} 登记={kw.get('rho_hi')}")
    cl.add("recompute_y0", s["y0_hi"] == kw.get("y0_hi"),
           f"复算={s['y0_hi']} 登记={kw.get('y0_hi')}")
    # 证书数学条件（独立判定，不依赖登记 verdict）
    cl.add("existence_condition", rec["exists"],
           "K(U) ⊂ int(U) 逐分量严格包含（6 严格不等式）⟹ 存在")
    cl.add("uniqueness_condition", rec["uniq"],
           f"ρ_hi={s['rho_hi']} < 1 ⟹ 唯一（压缩映射）")
    v = w["verdict"]
    cl.add("verdict_consistent",
           v.get("existence") is True and v.get("uniqueness") is True
           and v.get("status") == "PASS",
           json.dumps(v, ensure_ascii=False))


def _check_fail(w, cl):
    cl.add("fail_box_null", w.get("box") is None, "FAIL 证书 box 必须为 null")
    cl.add("fail_krawczyk_null", w.get("krawczyk") is None, "FAIL 证书 krawczyk 必须为 null")
    v = w["verdict"]
    cl.add("fail_verdict_shape",
           v.get("status") == "FAIL" and v.get("existence") is False
           and v.get("uniqueness") is False,
           json.dumps(v, ensure_ascii=False))
    fr = w.get("fail_registration") or {}
    cl.add("fail_registration_present",
           isinstance(fr.get("reason"), str) and len(fr["reason"]) >= 20,
           str(fr.get("reason", ""))[:60])
    diag = fr.get("diagnostics") or {}
    last = diag.get("last_attempt") or {}
    if not last.get("r"):
        cl.add("fail_diagnostics_present", False, "缺 last_attempt.r")
        return
    cl.add("fail_diagnostics_present", True, f"last r={last['r']}")
    # 独立复算最后一次尝试：证书两条件确实不成立（诚实失败确认）
    rec = _krawczyk_recompute(w["params"], w["candidate"]["z"],
                              w["preconditioner"]["Y"], last["r"])
    cl.add("fail_recompute_consistent",
           rec["str"]["rho_hi"] == last.get("rho_hi")
           and rec["str"]["min_margin"] == last.get("min_margin"),
           f"复算 rho_hi={rec['str']['rho_hi']} min_margin={rec['str']['min_margin']}"
           f" 登记 rho_hi={last.get('rho_hi')} min_margin={last.get('min_margin')}")
    cl.add("fail_confirmed", not (rec["exists"] and rec["uniq"]),
           f"末次尝试复算：exists={rec['exists']} uniq={rec['uniq']}（须不同时成立）")
    eps = diag.get("eps_hi")
    if eps is not None:
        rec0 = _krawczyk_recompute(w["params"], w["candidate"]["z"],
                                   w["preconditioner"]["Y"], "0")
        cl.add("fail_eps_consistent", rec0["str"]["y0_hi"] == eps,
               f"复算 eps_hi={rec0['str']['y0_hi']} 登记={eps}")


def verify_cert(path):
    cl = _Checklist()
    try:
        with open(path, encoding="utf-8") as fh:
            w = json.load(fh)
    except Exception as e:
        return {"cert": path, "ok": False,
                "checks": [{"check": "parse_json", "ok": False, "detail": repr(e)}]}
    try:
        if not _check_schema(w, cl):
            return {"cert": path, "case_id": w.get("case_id"), "ok": False, "checks": cl.checks}
        if not _check_common(w, cl, path):
            return {"cert": path, "case_id": w.get("case_id"), "ok": False, "checks": cl.checks}
        status = (w.get("verdict") or {}).get("status")
        if status == "PASS":
            _check_pass(w, cl)
        elif status == "FAIL":
            _check_fail(w, cl)
        else:
            cl.add("verdict_status_known", False, f"未知 status: {status!r}")
    except Exception as e:
        cl.add("exception", False, f"{type(e).__name__}: {e}")
    return {"cert": path, "case_id": w.get("case_id"), "ok": cl.ok, "checks": cl.checks}


def main(argv=None):
    ap = argparse.ArgumentParser(description="WS-55 Krawczyk×Galerkin 证书独立验证器（fail-closed）")
    ap.add_argument("certs", nargs="+")
    ap.add_argument("--json", action="store_true", help="打印完整逐检查项 JSON")
    args = ap.parse_args(argv)
    verdicts = [verify_cert(p) for p in args.certs]
    all_ok = all(v["ok"] for v in verdicts)
    if args.json:
        print(json.dumps(verdicts, ensure_ascii=False, indent=2))
    else:
        for v in verdicts:
            n_ok = sum(1 for c in v["checks"] if c["ok"])
            print(f"{'PASS' if v['ok'] else 'FAIL'} {v.get('case_id') or v['cert']} "
                  f"({n_ok}/{len(v['checks'])} checks)")
            for c in v["checks"]:
                if not c["ok"]:
                    print(f"    ✗ {c['check']}: {c['detail']}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
