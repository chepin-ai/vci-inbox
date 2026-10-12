#!/usr/bin/env python3
# CLASSIFY: L1
"""A1 栈 P0-1/P0-3 登记模板最小校验器（PIVOT-01 WS-36 · A 级 · 仅标准库）。

唯一规范源：
  * board/A1-STACK-P0-PLAN-01.md @c95e392e（P0-1 §1 / P0-3 §3 字段集与验收判据）
  * board/A1-STACK-UPGRADE-DRAFT-01.md v0.3（§4a 八字段 + §4a(6)/§4b schema_version 律）

校验面（fail-closed：不识别即拒，任何失败非零退出）：
  * schema_version 存在、为 "<major>.<minor>" 且受支持（当前仅 "1.0"）；
    高于受支持 major → unsupported_schema 拒收（退出码 3）；缺失/畸形/不识版本 → 拒（§4b）。
  * schema_version 必须为对象首字段（§4b 首字段必填律延伸适用）。
  * L0 确权登记（P0-1）：11 字段全必填；sorryAx_present 为布尔且 false 硬门（计划 §1 判据 2）。
  * DISPUTED 登记册/条目（P0-3 / §4a）：八字段 {dispute_id, artifact_sha256,
    l1_record_ptr, l2_record_ptr, ts_open, dispute_resolver, dispute_timeout_ms,
    default_action_on_timeout} + schema_version 全必填，缺任一键即不合规；
    dispute_timeout_ms 为正整数（缺省恰 604800000 = 7 天）；
    default_action_on_timeout ∈ {hold, demote, escalate}（缺省 escalate）；
    dispute_resolver 以「判定席」前缀锚定（resolver 独占性机检钩，§4a(3)）；
    status∈{open,resolved}（若存在）且 resolved ⇒ resolution_ptr 非空（计划 §3 判据 6）。
  * 未识别结构（既非 L0 登记亦非 DISPUTED 册/条目）→ fail-closed 拒收。

用法：python3 validate_registry.py [--kind l0|disputed|auto] <file.json> [...]
退出码：0 全部通过；2 校验失败/不可解析；3 unsupported_schema；1 用法/IO 错误。
"""
import json
import re
import sys
from pathlib import Path

SUPPORTED_SCHEMA_VERSIONS = {"1.0"}
SCHEMA_VERSION_RE = re.compile(r"^(\d+)\.(\d+)$")

L0_REQUIRED_FIELDS = [
    "schema_version", "base_id", "artifact_path", "artifact_sha256",
    "theorems", "axiom_audit", "sorryAx_present", "verify_request_ids",
    "env_fp", "lock_status", "ts_register",
]

# §4a 进入条款八字段 + schema_version（计划 §3 判据 1：全必填，缺任一键即不合规）
DISPUTED_REQUIRED_FIELDS = [
    "schema_version", "dispute_id", "artifact_sha256", "l1_record_ptr",
    "l2_record_ptr", "ts_open", "dispute_resolver", "dispute_timeout_ms",
    "default_action_on_timeout",
]

DEFAULT_DISPUTE_TIMEOUT_MS = 604800000  # 7 天（§4a(3) 缺省）
DEFAULT_ACTION_ENUM = {"hold", "demote", "escalate"}
DEFAULT_ACTION_ON_TIMEOUT = "escalate"
RESOLVER_PREFIX = "判定席"
STATUS_ENUM = {"open", "resolved"}

EXIT_USAGE = 1
EXIT_INVALID = 2
EXIT_UNSUPPORTED_SCHEMA = 3


class UnsupportedSchema(Exception):
    """消费方遇高于自身支持的 major / 不识版本：拒绝消费（§4b unsupported_schema）。"""


def check_schema_version(obj, ctx, errors):
    """schema_version 存在、首字段、受支持；失败计入 errors 或抛 UnsupportedSchema。"""
    if not isinstance(obj, dict):
        errors.append(f"{ctx}: 非 JSON 对象，拒绝受理")
        return
    keys = list(obj.keys())
    if "schema_version" not in obj:
        errors.append(f"{ctx}: schema_version 缺失即格式不合规，拒绝受理（§4b）")
        return
    if keys and keys[0] != "schema_version":
        errors.append(f"{ctx}: schema_version 非首字段（§4b 首字段必填律）")
    sv = obj["schema_version"]
    if not isinstance(sv, str):
        errors.append(f"{ctx}: schema_version 非字符串，拒绝受理")
        return
    m = SCHEMA_VERSION_RE.match(sv)
    if not m:
        raise UnsupportedSchema(f"{ctx}: schema_version={sv!r} 畸形，fail-closed 拒收")
    if sv not in SUPPORTED_SCHEMA_VERSIONS:
        raise UnsupportedSchema(
            f"{ctx}: schema_version={sv!r} 不受支持（支持集 {sorted(SUPPORTED_SCHEMA_VERSIONS)}），"
            f"登记 unsupported_schema 拒绝消费（§4b）"
        )


def check_l0_entry(obj, ctx, errors):
    """P0-1 L0 确权登记条目：11 字段全必填 + sorryAx 硬门。"""
    for f in L0_REQUIRED_FIELDS:
        if f not in obj:
            errors.append(f"{ctx}: 缺必填字段 {f!r}（P0-1 字段集）")
    if "theorems" in obj and not (
        isinstance(obj["theorems"], list) and all(isinstance(t, str) for t in obj["theorems"])
    ):
        errors.append(f"{ctx}: theorems 须为字符串数组")
    if "axiom_audit" in obj and not (
        isinstance(obj["axiom_audit"], list) and all(isinstance(a, str) for a in obj["axiom_audit"])
    ):
        errors.append(f"{ctx}: axiom_audit 须为字符串数组")
    if "sorryAx_present" in obj:
        if not isinstance(obj["sorryAx_present"], bool):
            errors.append(f"{ctx}: sorryAx_present 须为布尔")
        elif obj["sorryAx_present"] is not False:
            errors.append(f"{ctx}: sorryAx_present=true 触发无 sorryAx 硬门（计划 §1 判据 2）")
    if "verify_request_ids" in obj and not (
        isinstance(obj["verify_request_ids"], list)
        and all(isinstance(r, str) for r in obj["verify_request_ids"])
    ):
        errors.append(f"{ctx}: verify_request_ids 须为字符串数组")


def check_disputed_entry(entry, ctx, errors):
    """P0-3 / §4a DISPUTED 条目：八字段+schema_version 齐、timeout/default 合法值域。"""
    check_schema_version(entry, ctx, errors)
    for f in DISPUTED_REQUIRED_FIELDS:
        if f not in entry:
            errors.append(f"{ctx}: 缺必填字段 {f!r}（§4a 八字段+schema_version 全必填）")
    if "dispute_timeout_ms" in entry:
        t = entry["dispute_timeout_ms"]
        if isinstance(t, bool) or not isinstance(t, int) or t <= 0:
            errors.append(f"{ctx}: dispute_timeout_ms 须为正整数毫秒，得 {t!r}")
    if "default_action_on_timeout" in entry:
        a = entry["default_action_on_timeout"]
        if a not in DEFAULT_ACTION_ENUM:
            errors.append(
                f"{ctx}: default_action_on_timeout={a!r} 越域，"
                f"合法值域 {sorted(DEFAULT_ACTION_ENUM)}（§4a(3)）"
            )
    if "dispute_resolver" in entry:
        r = entry["dispute_resolver"]
        if not isinstance(r, str) or not r.startswith(RESOLVER_PREFIX):
            errors.append(f"{ctx}: dispute_resolver 须以「{RESOLVER_PREFIX}」前缀锚定（§4a(3) 独占性）")
    if "dispute_id" in entry:
        d = entry["dispute_id"]
        if not isinstance(d, str) or not d.startswith("DSP-"):
            errors.append(f"{ctx}: dispute_id 须为 'DSP-' 前缀字符串（计划 §3 格式 DSP-YYYYMMDD-NN）")
    if "status" in entry:
        s = entry["status"]
        if s not in STATUS_ENUM:
            errors.append(f"{ctx}: status={s!r} 越域，合法值域 {sorted(STATUS_ENUM)}")
        elif s == "resolved" and not entry.get("resolution_ptr"):
            errors.append(f"{ctx}: status=resolved 但 resolution_ptr 为空（计划 §3 判据 6）")
    if "timeout_frozen" in entry and not isinstance(entry["timeout_frozen"], bool):
        errors.append(f"{ctx}: timeout_frozen 须为布尔")
    if "freeze_log" in entry and not isinstance(entry["freeze_log"], list):
        errors.append(f"{ctx}: freeze_log 须为数组")


def check_disputed_register(obj, errors):
    """DISPUTED 登记册本体：册级 schema_version + 缺省值 + 逐条目校验。"""
    check_schema_version(obj, "register", errors)
    if "defaults" in obj:
        d = obj["defaults"]
        if not isinstance(d, dict):
            errors.append("register: defaults 须为对象")
        else:
            if "dispute_timeout_ms" in d and d["dispute_timeout_ms"] != DEFAULT_DISPUTE_TIMEOUT_MS:
                errors.append(
                    f"register: defaults.dispute_timeout_ms={d['dispute_timeout_ms']!r} "
                    f"≠ 缺省 {DEFAULT_DISPUTE_TIMEOUT_MS}（计划 §3 判据 2）"
                )
            if "default_action_on_timeout" in d and d["default_action_on_timeout"] != DEFAULT_ACTION_ON_TIMEOUT:
                errors.append(
                    f"register: defaults.default_action_on_timeout={d['default_action_on_timeout']!r} "
                    f"≠ 缺省 {DEFAULT_ACTION_ON_TIMEOUT!r}（§4a(3)）"
                )
    entries = obj.get("entries")
    if not isinstance(entries, list):
        errors.append("register: entries 缺失或非数组，拒绝受理")
        return
    for i, e in enumerate(entries):
        ctx = f"entries[{i}]"
        if not isinstance(e, dict):
            errors.append(f"{ctx}: 非 JSON 对象，拒绝受理")
            continue
        check_disputed_entry(e, ctx, errors)


def detect_kind(obj):
    """fail-closed 类型识别：不识结构返回 None（拒收）。"""
    if not isinstance(obj, dict):
        return None
    if isinstance(obj.get("entries"), list) or obj.get("kind") == "disputed_register":
        return "disputed"
    if "dispute_id" in obj:
        return "disputed"
    if "base_id" in obj:
        return "l0"
    return None


def validate_file(path, kind="auto"):
    """返回 (ok, errors, unsupported)。unsupported=True 时退出码取 3。"""
    errors = []
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return False, [f"{path}: 不可解析为 JSON（fail-closed 拒收）: {e}"], False
    resolved = detect_kind(obj) if kind == "auto" else kind
    if resolved not in ("l0", "disputed"):
        return False, [f"{path}: 结构不识别（既非 L0 登记亦非 DISPUTED 册/条目），fail-closed 拒收"], False
    try:
        if resolved == "l0":
            check_schema_version(obj, "l0_entry", errors)
            if isinstance(obj, dict):
                check_l0_entry(obj, "l0_entry", errors)
        else:
            if isinstance(obj, dict) and "entries" in obj:
                check_disputed_register(obj, errors)
            elif isinstance(obj, dict):
                check_disputed_entry(obj, "disputed_entry", errors)
            else:
                errors.append(f"{path}: 非 JSON 对象，拒绝受理")
    except UnsupportedSchema as e:
        return False, [str(e)], True
    return not errors, errors, False


def main(argv):
    args = list(argv)
    kind = "auto"
    if "--kind" in args:
        i = args.index("--kind")
        try:
            kind = args[i + 1]
        except IndexError:
            print("用法错误：--kind 缺参数", file=sys.stderr)
            return EXIT_USAGE
        del args[i : i + 2]
        if kind not in ("auto", "l0", "disputed"):
            print(f"用法错误：--kind={kind!r} 不识别", file=sys.stderr)
            return EXIT_USAGE
    if not args:
        print("用法：validate_registry.py [--kind l0|disputed|auto] <file.json> [...]", file=sys.stderr)
        return EXIT_USAGE
    rc = 0
    for f in args:
        ok, errors, unsupported = validate_file(f, kind)
        if ok:
            print(f"OK   {f}")
        else:
            for e in errors:
                print(f"FAIL {e}", file=sys.stderr)
            if unsupported:
                rc = max(rc, EXIT_UNSUPPORTED_SCHEMA)
            else:
                rc = max(rc, EXIT_INVALID)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
