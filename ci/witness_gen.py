# CLASSIFY: L1
# witness_gen.py · CIRC 重做 route B「见证认证」M0 见证生成器（schema v1.0）
#
# 规格：board/CIRC-REWORK-M0-SPEC-01.md §2（witness 五要素/schema v1.0）。
# 纪律：见证数值一律来自仓内锚定复算脚本的**实跑输出**，且实跑结果与锚定结果 JSON
#       逐字段一致（不一致即中止，不签发任何见证）；本生成器不自创任何数值。
#
# 锚定材料（实跑对象，subprocess 于临时沙箱中执行，不覆写仓内锚定结果文件）：
#   circulant：artifacts/CERT-CIRC-LEAN-01/family/EXT05-BATCH-01_verify.py
#              （mpmath.iv 外向舍入, mp.dps=80, Krawczyk 严格内包, 盒半径 1e-9,
#               有理中心 limit_denominator(1e13), 预条件子 limit_denominator(1e10),
#               负控 g 中心 +1e-6 重算预条件子必须拒证）
#   auction  ：artifacts/CERT-AUCTION-01/auction_verify.py
#              （前向拍卖+ε-scaling+暖启动；HiGHS 仅作不可信候选生成器；
#               np.nextafter 外向舍入区间算术；δ-deflation=1e-10；括弧 k×[LB_lo,UB_hi]）
#
# witness_sha256 规范化序列化规则（M0 interim，对应规格未决项 U4；M1 前须冻结）：
#   对「除去 witness_sha256 字段」的见证对象做
#   json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
#   的 UTF-8 编码，取 sha256 十六进制小写。
#
# 用法：python3 ci/witness_gen.py [--out artifacts/witnesses]
#   退出码 0=全部生成并自检通过；非 0=失败（fail-closed，不写半成品目录：先写临时目录再整体替换）。
import argparse
import datetime
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CIRC_SCRIPT = "artifacts/CERT-CIRC-LEAN-01/family/EXT05-BATCH-01_verify.py"
CIRC_RESULTS = "artifacts/CERT-CIRC-LEAN-01/family/EXT05-BATCH-01-results.json"
AUCT_SCRIPT = "artifacts/CERT-AUCTION-01/auction_verify.py"
AUCT_RESULTS = "artifacts/CERT-AUCTION-01/family/EXT05-BATCH-01-auction-results.json"

# circulant 族显式有理 c 向量（锚定于 EXT05-BATCH-01_verify.py FAMILIES 与
# artifacts/CERT-CIRC-LEAN-01/family/README.md「显式有理 c」登记；属决定论输入，非结果数值）。
C_VECTORS = {
    6: ["1/2", "1/3", "2/3", "1/4", "3/4", "1/5"],
    10: ["1/2", "1/3", "2/3", "1/4", "3/4", "1/5", "2/5", "3/5", "4/5", "1/6"],
}
# M0-AC2 六实例族：k∈{6,10} × ε∈{1,1/2,1/5}（扩例 ε∈{1/10,1/20} 不在 M0 范围）。
CIRC_SIX = [(6, "1"), (6, "1/2"), (6, "1/5"), (10, "1"), (10, "1/2"), (10, "1/5")]

AUCTION_HONESTY_BOUNDARY = (
    "UB=c·x 以 HiGHS 原始解为候选，primal 可行性信赖至 ~1e-12，未经区间认证"
    "（hexagon-submission v2 §5.3 Remark 5.2 口径；该族无 Lean 移植）"
)

SCHEMA_VERSION = "1.0"
GENERATOR_LINE = "PIVOT-01 计算线"


class GenError(RuntimeError):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(obj):
    """规范化序列化 sha256（规则见文件头注释；输入 obj 不得含 witness_sha256 字段）。"""
    if "witness_sha256" in obj:
        raise GenError("canonical_sha256 输入不得含 witness_sha256")
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def env_fp():
    """环境指纹（U3 interim：runner 声明 + 依赖清单哈希代偿；不含任何 lean/mathlib 维度）。"""
    import mpmath
    import numpy
    pkgs = {"python": platform.python_version(), "numpy": numpy.__version__, "mpmath": mpmath.__version__}
    try:
        import scipy
        pkgs["scipy"] = scipy.__version__
    except ImportError:
        pass
    manifest = "\n".join(f"{k}=={v}" for k, v in sorted(pkgs.items())) + "\n"
    return {
        "runner": "PIVOT-01 WS-37 witness_gen.py",
        "platform": platform.platform(),
        "packages": pkgs,
        "deps_manifest_sha256": hashlib.sha256(manifest.encode("utf-8")).hexdigest(),
        "lean_free": True,
        "note": "M0-AC5 interim（规格 U3）：env_fp 规范未定，以 runner 声明 + 依赖清单哈希代偿；无 lean/mathlib 维度",
    }


def run_anchored_script(script_rel, out_name):
    """在临时沙箱实跑锚定脚本，返回 (results dict, stdout)。失败即 GenError。"""
    script_abs = os.path.join(REPO_ROOT, script_rel)
    if not os.path.isfile(script_abs):
        raise GenError(f"锚定脚本缺失: {script_rel}")
    tmp = tempfile.mkdtemp(prefix="ws37-gen-")
    try:
        proc = subprocess.run([sys.executable, script_abs], cwd=tmp,
                              capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            raise GenError(f"锚定脚本实跑失败 {script_rel}: rc={proc.returncode}\n{proc.stderr[-2000:]}")
        out_path = os.path.join(tmp, out_name)
        if not os.path.isfile(out_path):
            raise GenError(f"锚定脚本未产出 {out_name}")
        with open(out_path, encoding="utf-8") as fh:
            return json.load(fh), proc.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def check_anchor_consistency(fresh, anchor_rel):
    """实跑结果必须与仓内锚定结果 JSON 逐字段一致（1:1 复原纪律）。"""
    with open(os.path.join(REPO_ROOT, anchor_rel), encoding="utf-8") as fh:
        anchor = json.load(fh)
    if json.dumps(fresh, sort_keys=True) != json.dumps(anchor, sort_keys=True):
        raise GenError(f"实跑结果与锚定结果不一致: {anchor_rel}；拒绝签发见证")


def _eps_tag(eps_str):
    return "e" + eps_str.replace("/", "-")


def build_circulant_witness(r, run_meta):
    k, eps = r["k"], r["eps"]
    if r["n"] != 2 * k - 1:
        raise GenError(f"n≠2k-1: {r}")
    ghat = r["ghat"]  # 有理字符串 "num/den"
    w = {
        "schema_version": SCHEMA_VERSION,
        "witness_id": f"circulant-sinkhorn-k{k}-{_eps_tag(eps)}-{run_meta['date']}",
        "family": "circulant-sinkhorn",
        "claim": "unique_root_in_box",
        "inputs": {
            "k": k,
            "eps": eps,
            "c": list(C_VECTORS[k]),
            "gauge": "f0=0",
            "n": r["n"],
        },
        "interval_engine": {"name": "mpmath.iv", "precision": "dps=80", "rounding": "outward"},
        "rationalization": {
            "center_limit_denominator": "1e13",
            "preconditioner_limit_denominator": "1e10",
            "center_err": r["center_err"],
        },
        "bounds": {
            "box_radius": "1e-9",
            "center": {"f": ["0"] * (k - 1), "g": ghat},
            "preconditioner": {"kind": "rationalized_inverse_jacobian", "limit_denominator": "1e10"},
            "krawczyk_image": {
                "max_width": repr(r["K_max_width"]),
                "min_margin": repr(r["K_min_margin"]),
            },
        },
        "verdict": {
            "inside": bool(r["inside"]),
            "metrics": {
                "condJ": repr(r["condJ"]),
                "K_max_width": repr(r["K_max_width"]),
                "K_min_margin": repr(r["K_min_margin"]),
            },
        },
        "negative_control": {
            "perturbation": {"kind": "center_shift", "target": "g", "delta": "1e-6",
                             "preconditioner": "recomputed"},
            "neg_verdict": {"neg_inside": bool(r["neg_inside"]),
                            "neg_K_min_margin": repr(r["neg_K_min_margin"])},
            "same_lineage": {
                "same_script": True,
                "script_path": CIRC_SCRIPT,
                "env_fp_sha256": run_meta["env_fp"]["deps_manifest_sha256"],
                "statement": "负控与正例同脚本、同环境指纹（OBL §4 AC4 纪律延伸至见证层）",
            },
        },
        "replay": {
            "script_path": CIRC_SCRIPT,
            "script_sha256": run_meta["script_sha"][CIRC_SCRIPT],
            "results_path": CIRC_RESULTS,
            "results_sha256": run_meta["results_sha"][CIRC_RESULTS],
            "env_fp": run_meta["env_fp"],
            "run_id": run_meta["run_id"],
            "ts": run_meta["ts"],
        },
        "provenance": {
            "generator_line": GENERATOR_LINE,
            "source_anchors": [
                CIRC_SCRIPT,
                CIRC_RESULTS,
                "artifacts/CERT-CIRC-LEAN-01/family/EXT05-BATCH-01-RESULTS.md",
                "artifacts/CERT-CIRC-LEAN-01/family/README.md",
            ],
        },
        "lean_binding": None,
        "notes": "M0 口径=内生 fail-closed 见证复算核验；非机器验证证书（OBL §10 升级门未过）",
    }
    w["witness_sha256"] = canonical_sha256(w)
    return w


def _fmt_eps0(v):
    s = repr(float(v))
    return s[:-2] if s.endswith(".0") else s


def build_auction_witness(r, run_meta):
    k = r["k"]
    w = {
        "schema_version": SCHEMA_VERSION,
        "witness_id": f"auction-dual-{r['tag'].lower()}-{run_meta['date']}",
        "family": "auction-dual",
        "claim": "cost_in_dual_bracket",
        "inputs": {
            "k": k,
            "R": r["R"],
            "seed": r["seed"],
            "eps_schedule": {
                "eps0": _fmt_eps0(r["eps0"]),
                "factor": f"/{int(r['factor'])}",
                "eps_final": repr(float(r["eps_final"])),
            },
            "generator": "rng=np.random.default_rng(seed); rng.random(k)×2 预抽; C=10^(R·(2·rng.random((k,k))−1))",
            "solver": "forward-auction + HiGHS(仅作不可信候选生成器)",
        },
        "interval_engine": {"name": "numpy.nextafter", "precision": "float64",
                            "rounding": "directed_endpoints"},
        "rationalization": {"limit_denominator": None,
                            "note": "auction 族无有理化收敛子；区间算术为 np.nextafter 定向舍入"},
        "bounds": {
            "bracket": {"lb_lo": r["bracket"][0], "ub_hi": r["bracket"][1]},
            "bracket_scale": "k×[LB_lo,UB_hi] (Birkhoff)",
            "bracket_width": r["bracket_width"],
            "rc_min_lo": r["rc_min_lo"],
            "delta_deflation": "1e-10",
            "deflated": bool(r["deflated"]),
            "gap": r["gap"],
            "gap_bound": "k·eps_final",
            "gap_bound_value": r["gap_bound_k_eps"],
            "auction_cost": r["auction_cost"],
            "epsCS_residual": r["epsCS_residual"],
            "rounds": r["rounds"],
            "bids": r["bids"],
        },
        "verdict": {
            "inside": bool(r["inside"]),
            "gap_within_bound": bool(r["gap_within_bound"]),
            "dual_feasible_certified": bool(r["dual_feasible_certified"]),
            "metrics": {
                "auction_cost": r["auction_cost"],
                "gap": r["gap"],
                "gap_bound_k_eps": r["gap_bound_k_eps"],
                "bracket_width": r["bracket_width"],
                "rc_min_lo": r["rc_min_lo"],
            },
        },
        "honesty_boundary": AUCTION_HONESTY_BOUNDARY,
        "negative_control": {
            "perturbation": {"kind": "swap_perturbation",
                             "spec": "交换扰动：交换增量最大的一对分配",
                             "swap": [int(v) for v in r["neg_swap"]]},
            "neg_verdict": {"neg_rejected": bool(r["neg_rejected"]), "neg_cost": r["neg_cost"]},
            "same_lineage": {
                "same_script": True,
                "script_path": AUCT_SCRIPT,
                "env_fp_sha256": run_meta["env_fp"]["deps_manifest_sha256"],
                "statement": "负控与正例同脚本、同环境指纹（OBL §4 AC4 纪律延伸至见证层）",
            },
        },
        "replay": {
            "script_path": AUCT_SCRIPT,
            "script_sha256": run_meta["script_sha"][AUCT_SCRIPT],
            "results_path": AUCT_RESULTS,
            "results_sha256": run_meta["results_sha"][AUCT_RESULTS],
            "env_fp": run_meta["env_fp"],
            "run_id": run_meta["run_id"],
            "ts": run_meta["ts"],
        },
        "provenance": {
            "generator_line": GENERATOR_LINE,
            "source_anchors": [
                AUCT_SCRIPT,
                AUCT_RESULTS,
                "artifacts/CERT-AUCTION-01/README.md",
            ],
        },
        "lean_binding": None,
        "notes": "M0 口径=内生 fail-closed 见证复算核验；非机器验证证书（OBL §10 升级门未过）",
    }
    w["witness_sha256"] = canonical_sha256(w)
    return w


def main():
    ap = argparse.ArgumentParser(description="M0 见证生成器（schema v1.0）")
    ap.add_argument("--out", default=os.path.join(REPO_ROOT, "artifacts", "witnesses"))
    ap.add_argument("--keep-ext", action="store_true",
                    help="同时为 circulant 扩例(ε=1/10,1/20)出证（M0 默认仅六例）")
    args = ap.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)
    run_meta = {
        "date": now.strftime("%Y%m%d"),
        "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_id": f"ws37-m0-{now.strftime('%Y%m%dT%H%M%SZ')}",
        "env_fp": env_fp(),
        "script_sha": {p: sha256_file(os.path.join(REPO_ROOT, p)) for p in (CIRC_SCRIPT, AUCT_SCRIPT)},
        "results_sha": {p: sha256_file(os.path.join(REPO_ROOT, p)) for p in (CIRC_RESULTS, AUCT_RESULTS)},
    }

    # 实跑锚定脚本并与锚定结果比对（fail-closed）
    circ_fresh, circ_log = run_anchored_script(CIRC_SCRIPT, "EXT05-BATCH-01-results.json")
    check_anchor_consistency(circ_fresh, CIRC_RESULTS)
    auct_fresh, auct_log = run_anchored_script(AUCT_SCRIPT, "EXT05-BATCH-01-auction-results.json")
    check_anchor_consistency(auct_fresh, AUCT_RESULTS)

    witnesses = []
    want = {(k, e) for k, e in CIRC_SIX}
    for r in circ_fresh["results"]:
        if not args.keep_ext and (r["k"], r["eps"]) not in want:
            continue
        if not (r["inside"] and not r["neg_inside"] and r["pass"]):
            raise GenError(f"锚定实例未过判据，拒绝签发: {r['tag']}")
        witnesses.append(build_circulant_witness(r, run_meta))
    for r in auct_fresh["results"]:
        if not (r["inside"] and r["gap_within_bound"] and r["dual_feasible_certified"]
                and r["neg_rejected"] and r["pass"]):
            raise GenError(f"锚定实例未过判据，拒绝签发: {r['tag']}")
        witnesses.append(build_auction_witness(r, run_meta))

    # 先写临时目录，全部成功再整体替换（不留下半成品目录）
    out_dir = args.out
    tmp_out = tempfile.mkdtemp(prefix="ws37-wit-", dir=os.path.dirname(out_dir) or ".")
    try:
        for w in witnesses:
            path = os.path.join(tmp_out, w["witness_id"] + ".witness.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(w, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        shutil.move(tmp_out, out_dir)
    except Exception:
        shutil.rmtree(tmp_out, ignore_errors=True)
        raise

    print(f"run_id={run_meta['run_id']} 生成见证 {len(witnesses)} 件 → {out_dir}")
    for w in witnesses:
        print(f"  {w['witness_id']}  sha256={w['witness_sha256'][:16]}…")
    print(circ_log.strip().splitlines()[-1])
    print(auct_log.strip().splitlines()[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
