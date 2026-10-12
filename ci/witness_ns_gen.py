# CLASSIFY: L1
# witness_ns_gen.py · EXT-WAVE-09「NS」波 WS-43 数值见证生成器（schema v1.0）
#
# 对象：2D Navier–Stokes Galerkin 截断（WS-41 Lean 核：GalerkinNS 结构 ν>0、A 强制性、
#   hB: ∀u, ⟪B u u, u⟫=0；具体实例 skewB a u v = ⟪a,u⟫•v − ⟪a,v⟫•u；ModeSpace N = R^{2N+1}；
#   能量界 ‖x(t)‖² ≤ max(‖x₀‖², ‖f‖²/ν²)）的三件数值见证：
#   · W-NS1 ns-energy-cancellation：⟪B(u,u),u⟫ ∋ 0 的 mpmath.iv（dps=50）区间实证，
#     skewB（ModeSpace 1 / N=2 推广）+ orthProjB（B(u,v)=(u·v)g−(v·g)u，非平凡相消），
#     ≥200 组随机/退化/大范数/小范数角例；负控=符号翻转 plus-形式必须拒证。
#   · W-NS2 ns-galerkin-energy-bound：≥50 组 (ν,x₀,f) 参数，scipy solve_ivp（DOP853,
#     rtol=1e-12, atol=1e-14，**不可信候选**）高密度采样；证书=「采样点上界成立」区间实证
#     （mpmath.iv dps=50 + nextafter 双括号余量 η），明示「非轨道包络」。
#   · W-NS3 ns-trajectory-envelope-blocked：完整轨道包络（RadiiPolynomial 级 CAP）
#     BLOCKED(B1 结构性/工具链缺) 登记。
#
# 纪律（沿用 WS-37 M0 范式）：
#   · 所有见证数值来自本文件**真实运行**产出（固定种子决定论；禁止合成数据）；
#   · sandbox 一致性门禁：主流程与独立子进程（--emit-raw）各算一遍，规范化 JSON 逐字节
#     一致方签发（无仓内前置锚定脚本，门禁改为双跑决定论一致性，如实登记）；
#   · 先写临时目录、全部成功再整体替换（fail-closed，不留半成品）；
#   · lean_binding 恒 null；notes 固定登记「非机器验证证书」口径。
#
# witness_sha256 规范化序列化规则（沿用 WS-37 M0 interim）：
#   json.dumps(除去 witness_sha256 的对象, sort_keys=True, separators=(",", ":"),
#              ensure_ascii=False).encode("utf-8") 的 sha256 十六进制小写。
#
# 区间计算规范（与独立核验器 witness_ns_verify.py 各自实现同一规范，零共享代码）：
#   十进制字符串 → Fraction → iv.mpf(分子)/iv.mpf(分母)（dps=50 外向舍入）；
#   求和按下标升序从左到右，初值 iv.mpf(0)；skewB/orthProjB 公式见下文函数 docstring。
#
# 用法：python3 ci/witness_ns_gen.py [--out artifacts/witnesses-ns]
#   --emit-raw PATH：仅供一致性门禁内部调用（重算决定论负载并写规范化 JSON）。
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
from fractions import Fraction

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_REL = "ci/witness_ns_gen.py"
VER_REL = "ci/witness_ns_verify.py"
RUNLOG_REL = "artifacts/witnesses-ns/run-log.json"

SCHEMA_VERSION = "1.0"
GENERATOR_LINE = "PIVOT-01 计算线"
SEED = 20261012
IV_DPS = 50

NS1_N_RANDOM = {"skewB@N1": 100, "skewB@N2": 60, "orthProjB@N1": 40}
NS2_N_CASES = 56
NS2_N_SAMPLES = 65
NS2_RTOL, NS2_ATOL = 1e-12, 1e-14
NS2_ETA_REL, NS2_NEXTAFTER_STEPS = 1e-9, 8

NS3_STATEMENT = (
    "完整轨道包络（RadiiPolynomial 级 CAP）登记为 BLOCKED（B1 结构性/工具链缺）："
    "WS-41 Lean 核已证 2D NS Galerkin 截断的能量相消、Grönwall 先验界与整体存在（定性层，零 sorry）；"
    "但对有限 Galerkin ODE 的严格轨道包络需 radii-polynomial 不动点认证（区间 Banach 代数上的"
    "范数界 + p(r)<0 多项式不等式 + 严格积分器）。当前联邦工具链无现货：本仓区间层仅支持"
    "逐点 mpmath.iv 算术，无 Taylor 模型/Hermite–Obreshkov 级严格积分层，无 RadiiPolynomial "
    "认证层；WS-40 §4 评估指出 Lean 侧 RadiiPolynomial 框架（arXiv:2610.02335）仅覆盖多项式 "
    "IVP/Lorenz 级实例，NS 所需的 Fourier 系数 Banach 代数与卷积界缺席。本批次不产出任何"
    "轨道包络数值，此登记仅为阻塞显式化，非部分成果宣称。"
)
NS3_REQUIREMENTS = [
    "RadiiPolynomial 不动点认证框架（有限维约化 + 尾部分解 + p(r)<0 区间验证）",
    "严格 ODE 积分器（Taylor 模型或区间 Hermite–Obreshkov 级，mpmath.iv 可承载）",
    "（PDE/Fourier 层）系数 Banach 代数与卷积界——超出本波范围，仅登记不承诺",
]

NS2_HONESTY_BOUNDARY = (
    "采样点证书：scipy solve_ivp（DOP853, rtol=1e-12, atol=1e-14）产出为不可信候选轨道；"
    "区间认证仅覆盖「登记采样点上 ‖x(t_i)‖² ≤ max(‖x₀‖², ‖f‖²/ν²) + η」，"
    "η = max(1e-9·(1+|bound|), 8×nextafter ulp) 覆盖非严格积分器误差；"
    "非轨道包络——采样点之间与真解的逐点包络未认证（CAP 级包络见 W-NS3 阻塞登记 B1）"
)


class GenError(RuntimeError):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(obj):
    if "witness_sha256" in obj:
        raise GenError("canonical_sha256 输入不得含 witness_sha256")
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def env_fp():
    import mpmath
    import numpy
    import scipy
    pkgs = {"python": platform.python_version(), "numpy": numpy.__version__,
            "mpmath": mpmath.__version__, "scipy": scipy.__version__}
    manifest = "\n".join(f"{k}=={v}" for k, v in sorted(pkgs.items())) + "\n"
    return {
        "runner": "PIVOT-01 WS-43 witness_ns_gen.py",
        "platform": platform.platform(),
        "packages": pkgs,
        "deps_manifest_sha256": hashlib.sha256(manifest.encode("utf-8")).hexdigest(),
        "lean_free": True,
        "note": "interim（沿用 WS-37 U3 代偿）：runner 声明 + 依赖清单哈希；无 lean/mathlib 维度",
    }


# ---------------------------------------------------------------- 决定论负载

def _iv_of(s):
    """十进制字符串 → mpmath.iv 区间（规范：Fraction → iv.mpf(num)/iv.mpf(den)）。"""
    from mpmath import iv
    fr = Fraction(str(s).strip())
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def _lsum(terms):
    from mpmath import iv
    acc = iv.mpf(0)
    for t in terms:
        acc = acc + t
    return acc


def _skewb_cancellation(a, u):
    """⟪skewB(a)(u,u),u⟫：s=⟪a,u⟫，t=⟪a,u⟫（独立第二遍求和），B_i=s·u_i−t·u_i，inner=Σ B_i·u_i。"""
    n = len(u)
    s = _lsum([a[j] * u[j] for j in range(n)])
    t = _lsum([a[j] * u[j] for j in range(n)])
    B = [s * u[i] - t * u[i] for i in range(n)]
    return _lsum([B[i] * u[i] for i in range(n)])


def _orthproj_cancellation(g, u):
    """⟪B(u,u),u⟫，B(u,v)=(u·v)g−(v·g)u：p=Σu²，q=Σg·u，B_i=p·g_i−q·u_i，inner=Σ B_i·u_i。"""
    n = len(u)
    p = _lsum([u[j] * u[j] for j in range(n)])
    q = _lsum([g[j] * u[j] for j in range(n)])
    B = [p * g[i] - q * u[i] for i in range(n)]
    return _lsum([B[i] * u[i] for i in range(n)])


def _mag(form, coeffs, u):
    from mpmath import iv
    n = len(u)
    if form == "skewB":
        s1 = _lsum([abs(coeffs[j] * u[j]) for j in range(n)])
        s2 = _lsum([u[j] * u[j] for j in range(n)])
        return float((s1 * s2).b)
    p = _lsum([u[j] * u[j] for j in range(n)])
    q = _lsum([coeffs[j] * u[j] for j in range(n)])
    m = _lsum([p * abs(coeffs[i] * u[i]) + abs(q) * (u[i] * u[i]) for i in range(n)])
    return float(m.b)


def _tol(mag):
    return max(1e-45, 1e-38 * mag)


def _gen_ns1_cases():
    """≥200 组 interval 点：随机 / 大范数(1e6) / 小范数(1e-8) / 退化（零向量、平行）角例。"""
    import numpy as np
    rng = np.random.default_rng(SEED)
    cases = []

    def add(form, dim, regime, a=None, g=None, u=None):
        if form == "skewB":
            a_s = [repr(float(v)) for v in (a if a is not None else rng.standard_normal(dim))]
            g_s = None
        else:
            a_s = None
            g_s = [repr(float(v)) for v in (g if g is not None else rng.standard_normal(dim))]
        u_s = [repr(float(v)) for v in (u if u is not None else rng.standard_normal(dim))]
        cases.append({"tag": f"ns1-{form.replace('@', '-')}-{regime}-{len(cases):03d}",
                      "form": form, "dim": dim, "regime": regime,
                      "a": a_s, "g": g_s, "u": u_s})

    for spec, n_rand in NS1_N_RANDOM.items():
        form, nn = spec.split("@")
        dim = 3 if nn == "N1" else 5
        for _ in range(n_rand):
            add(form, dim, "random")
        n_big = 12 if nn == "N1" and form == "skewB" else 10
        for _ in range(n_big):
            add(form, dim, "large_norm",
                a=(rng.standard_normal(dim) * 1e6) if form == "skewB" else None,
                g=(rng.standard_normal(dim) * 1e6) if form != "skewB" else None,
                u=rng.standard_normal(dim) * 1e6)
        for _ in range(10 if nn == "N1" else 10):
            add(form, dim, "small_norm",
                a=(rng.standard_normal(dim) * 1e-8) if form == "skewB" else None,
                g=(rng.standard_normal(dim) * 1e-8) if form != "skewB" else None,
                u=rng.standard_normal(dim) * 1e-8)
    # 退化角例（ModeSpace 1）：a=0 / u=0 / a∥u；orthProjB：g=0 / g∥u / u=0
    z3 = np.zeros(3)
    for _ in range(4):
        add("skewB", 3, "degenerate-a0", a=z3.copy())
    for _ in range(4):
        add("skewB", 3, "degenerate-u0", u=z3.copy())
    for _ in range(8):
        u = rng.standard_normal(3)
        lam = float(rng.standard_normal() * 3.0)
        add("skewB", 3, "degenerate-parallel", a=lam * u, u=u)
    for _ in range(3):
        add("orthProjB", 3, "degenerate-g0", g=z3.copy())
    for _ in range(3):
        add("orthProjB", 3, "degenerate-u0", u=z3.copy())
    for _ in range(4):
        u = rng.standard_normal(3)
        lam = float(rng.standard_normal() * 2.0)
        add("orthProjB", 3, "degenerate-parallel", g=lam * u, u=u)
    return cases


def _eval_ns1(cases):
    """区间实证 ⟪B(u,u),u⟫ ∋ 0 且宽度 ≤ 容差；返回 (cases_with_metrics, metrics, neg)。"""
    from mpmath import iv
    iv.dps = IV_DPS
    max_w, max_rel, per_form = 0.0, 0.0, {}
    for c in cases:
        form, dim = c["form"], c["dim"]
        u = [_iv_of(s) for s in c["u"]]
        coeffs = [_iv_of(s) for s in (c["a"] if form == "skewB" else c["g"])]
        inner = _skewb_cancellation(coeffs, u) if form == "skewB" else _orthproj_cancellation(coeffs, u)
        lo, hi = float(inner.a), float(inner.b)
        width = hi - lo
        mag = _mag(form, coeffs, u)
        if not (lo <= 0.0 <= hi):
            raise GenError(f"能量相消区间不含 0（算法错误）: {c['tag']} inner=[{lo!r},{hi!r}]")
        if width > _tol(mag):
            raise GenError(f"包络宽度超容差: {c['tag']} width={width!r} tol={_tol(mag)!r}")
        c["inner_lo"], c["inner_hi"] = repr(lo), repr(hi)
        c["width"] = repr(width)
        max_w = max(max_w, width)
        max_rel = max(max_rel, width / max(1.0, mag))
        per_form[form] = per_form.get(form, 0) + 1
    metrics = {"n_cases": len(cases), "max_width": repr(max_w),
               "max_rel_width": repr(max_rel), "per_form": per_form}
    # 负控：plus-形式 B_plus(u,v)=(u·v)g+(v·g)u → inner=2·p·q，必须拒证
    ref = next(c for c in cases if c["form"] == "orthProjB" and c["regime"] == "random")
    g = [_iv_of(s) for s in ref["g"]]
    u = [_iv_of(s) for s in ref["u"]]
    pp = _lsum([u[j] * u[j] for j in range(3)])
    qq = _lsum([g[j] * u[j] for j in range(3)])
    neg_inner = pp * qq + qq * pp
    nlo, nhi = float(neg_inner.a), float(neg_inner.b)
    if nlo <= 0.0 <= nhi:
        raise GenError(f"负控案例选取不当（plus-形式仍含 0）: {ref['tag']}")
    neg = {"kind": "sign_flip", "form": "orthProjB-plus", "case_tag": ref["tag"],
           "neg_inner_lo": repr(nlo), "neg_inner_hi": repr(nhi)}
    return cases, metrics, neg


def _ns2_vf(kind, nu, aux, f):
    import numpy as np
    aux = np.asarray(aux, dtype=float)
    f = np.asarray(f, dtype=float)

    def vf(t, x):
        if kind == "orthProjB":
            Bxx = float(np.dot(x, x)) * aux - float(np.dot(x, aux)) * x
        else:  # skewB：B(a)(x,x) ≡ 0（WS-41 concreteData），线性动力学
            Bxx = 0.0
        return -nu * x + Bxx + f
    return vf


def _gen_ns2_cases():
    import numpy as np
    rng = np.random.default_rng(SEED + 1)
    cases = []
    for i in range(NS2_N_CASES):
        kind = "orthProjB" if i % 2 == 0 else "skewB"
        nu = float(10.0 ** rng.uniform(-1.0, 1.0))
        scale0 = [0.5, 2.0, 8.0][i % 3]
        scalef = [0.0, 0.3, 1.0, 3.0][i % 4]
        x0 = rng.standard_normal(3) * scale0
        f = np.zeros(3) if scalef == 0.0 else rng.standard_normal(3) * scalef
        aux = rng.standard_normal(3)
        T = float([1.0, 2.0, 4.0][i % 3])
        cases.append({"tag": f"ns2-{kind}-{i:03d}", "kind": kind,
                      "nu": repr(nu), "x0": [repr(float(v)) for v in x0],
                      "f": [repr(float(v)) for v in f],
                      ("g" if kind == "orthProjB" else "a"): [repr(float(v)) for v in aux],
                      "T": repr(T)})
    return cases


def _ns2_eta(bound_hi):
    import numpy as np
    m = bound_hi
    for _ in range(NS2_NEXTAFTER_STEPS):
        m = float(np.nextafter(m, np.inf))
    return max(NS2_ETA_REL * (1.0 + abs(bound_hi)), m - bound_hi)


def _eval_ns2(cases):
    """solve_ivp 产候选轨道（不可信）；对采样点做区间能量界实证；返回 (cases, metrics, neg)。"""
    from mpmath import iv
    from scipy.integrate import solve_ivp
    import numpy as np
    iv.dps = IV_DPS
    t_end_free = []
    max_defect, total, per_kind = -np.inf, 0, {}
    tight = None  # (margin, case, idx, bound_hi)
    for c in cases:
        kind = c["kind"]
        nu = float(Fraction(c["nu"]))
        x0 = [float(Fraction(s)) for s in c["x0"]]
        f = [float(Fraction(s)) for s in c["f"]]
        aux = [float(Fraction(s)) for s in (c["g"] if kind == "orthProjB" else c["a"])]
        T = float(Fraction(c["T"]))
        t_grid = [T * i / (NS2_N_SAMPLES - 1) for i in range(NS2_N_SAMPLES)]
        sol = solve_ivp(_ns2_vf(kind, nu, aux, f), (0.0, T), np.asarray(x0),
                        method="DOP853", rtol=NS2_RTOL, atol=NS2_ATOL,
                        t_eval=np.asarray(t_grid))
        if not sol.success:
            raise GenError(f"solve_ivp 失败: {c['tag']}: {sol.message}")
        nu_iv = _iv_of(c["nu"])
        x02 = _lsum([_iv_of(s) ** 2 for s in c["x0"]])
        f2 = _lsum([_iv_of(s) ** 2 for s in c["f"]])
        fnu2 = f2 / (nu_iv * nu_iv)
        b_hi = max(float(x02.b), float(fnu2.b))
        eta = _ns2_eta(b_hi)
        samples, case_max = [], -np.inf
        for i in range(NS2_N_SAMPLES):
            row = [repr(float(sol.y[j, i])) for j in range(3)]
            n_iv = _lsum([_iv_of(s) ** 2 for s in row])
            n_hi = float(n_iv.b)
            d = n_hi - b_hi
            case_max = max(case_max, d)
            if n_hi > b_hi + eta:
                raise GenError(f"采样点越界（候选轨道不可用）: {c['tag']} t_i={i} "
                               f"norm²_hi={n_hi!r} bound_hi={b_hi!r} eta={eta!r}")
            samples.append(row)
            if tight is None or (-d) < tight[0]:
                tight = (-d, c, i, b_hi)
        c["t"] = [repr(v) for v in t_grid]
        c["x"] = samples
        c["bound_hi"] = repr(b_hi)
        c["max_defect"] = repr(case_max)
        max_defect = max(max_defect, case_max)
        total += NS2_N_SAMPLES
        per_kind[kind] = per_kind.get(kind, 0) + 1
    metrics = {"n_cases": len(cases), "n_samples_total": total,
               "max_defect": repr(max_defect), "per_kind": per_kind}
    # 负控：最紧案例的最大范数采样点 ×1.0001 → 必须越界
    _, neg_case, neg_idx, neg_bhi = tight
    fac_s, eta = "1.0001", _ns2_eta(neg_bhi)
    fac = _iv_of(fac_s)
    row = neg_case["x"][neg_idx]
    neg_n = _lsum([(fac * _iv_of(s)) ** 2 for s in row])
    neg_hi = float(neg_n.b)
    if not neg_hi > neg_bhi + eta:
        raise GenError(f"负控扰动未越界（选取不当）: {neg_case['tag']}[{neg_idx}]")
    neg = {"kind": "scale_sample", "case_tag": neg_case["tag"],
           "sample_index": neg_idx, "factor": fac_s, "neg_norm_sq_hi": repr(neg_hi)}
    return cases, metrics, neg


def compute_payload():
    """决定论负载：三件见证的全部计算数据（不含时间戳/run_id）。一致性门禁比较对象。"""
    ns1_cases, ns1_metrics, ns1_neg = _eval_ns1(_gen_ns1_cases())
    ns2_cases, ns2_metrics, ns2_neg = _eval_ns2(_gen_ns2_cases())
    return {"ns1": {"cases": ns1_cases, "metrics": ns1_metrics, "neg": ns1_neg},
            "ns2": {"cases": ns2_cases, "metrics": ns2_metrics, "neg": ns2_neg},
            "ns3": {"statement": NS3_STATEMENT, "requirements": NS3_REQUIREMENTS}}


def _canonical_blob(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def consistency_gate(payload):
    """sandbox 一致性门禁：独立子进程重算决定论负载，规范化 JSON 逐字节一致方放行。"""
    tmp = tempfile.mkdtemp(prefix="ws43-gate-")
    try:
        out = os.path.join(tmp, "raw.json")
        proc = subprocess.run([sys.executable, os.path.abspath(__file__), "--emit-raw", out],
                              capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            raise GenError(f"门禁子进程失败 rc={proc.returncode}\n{proc.stderr[-2000:]}")
        with open(out, "rb") as fh:
            if fh.read() != _canonical_blob(payload):
                raise GenError("双跑决定论负载不一致，拒绝签发见证")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- 见证组装

def _replay(run_meta):
    return {"script_path": GEN_REL,
            "script_sha256": run_meta["script_sha"],
            "results_path": RUNLOG_REL,
            "results_sha256": run_meta["runlog_sha"],
            "env_fp": run_meta["env_fp"],
            "run_id": run_meta["run_id"],
            "ts": run_meta["ts"]}


def _provenance(anchors):
    return {"generator_line": GENERATOR_LINE, "source_anchors": anchors}


def _lineage():
    return {"same_script": True, "script_path": GEN_REL,
            "statement": "负控与正例同脚本、同环境指纹（沿用 WS-37 AC4 纪律）"}


def build_ns1(payload, run_meta):
    d = payload["ns1"]
    w = {
        "schema_version": SCHEMA_VERSION,
        "witness_id": f"ns-energy-cancellation-{run_meta['date']}",
        "family": "ns-energy-cancellation",
        "claim": "inner_B_u_u_contains_zero",
        "inputs": {
            "n_cases": d["metrics"]["n_cases"],
            "spaces": {"ModeSpace1": "EuclideanSpace ℝ (Fin 3)", "ModeSpace2": "EuclideanSpace ℝ (Fin 5)"},
            "forms": {
                "skewB": "B(a)(u,v) = ⟪a,u⟫•v − ⟪a,v⟫•u（WS-41 skewB 实例，N=1 与 N=2 推广）",
                "orthProjB": "B(u,v) = (u·v)g − (v·g)u（满足同一 hB 假设的非平凡相消实例）",
            },
            "seed": SEED,
            "cases": d["cases"],
        },
        "interval_engine": {"name": "mpmath.iv", "precision": f"dps={IV_DPS}", "rounding": "outward"},
        "rationalization": {"input_encoding": "repr(float64) 十进制字符串 → Fraction 精确有理",
                            "tol_rule": "width ≤ max(1e-45, 1e-38·mag)，mag=形式上尺度（规范见核验器文首）"},
        "bounds": {"width_tol_rule": "max(1e-45, 1e-38·mag)",
                   "max_width": d["metrics"]["max_width"],
                   "max_rel_width": d["metrics"]["max_rel_width"]},
        "verdict": {"all_contain_zero": True,
                    "metrics": d["metrics"]},
        "negative_control": {
            "perturbation": {"kind": d["neg"]["kind"], "form": d["neg"]["form"],
                             "case_tag": d["neg"]["case_tag"],
                             "spec": "符号翻转：B_plus(u,v)=(u·v)g+(v·g)u → ⟪B_plus(u,u),u⟫=2‖u‖²(g·u)，一般非零"},
            "neg_verdict": {"neg_rejected": True,
                            "neg_inner_lo": d["neg"]["neg_inner_lo"],
                            "neg_inner_hi": d["neg"]["neg_inner_hi"]},
            "same_lineage": _lineage(),
        },
        "replay": _replay(run_meta),
        "provenance": _provenance(["/mnt/agents/output/ws41-report.md",
                                   "ws41-src/NsGalerkin/Basic.lean (skewB/concreteData)",
                                   GEN_REL, RUNLOG_REL]),
        "lean_binding": None,
        "notes": "能量相消代数恒等式的区间实证（内生 fail-closed 见证复算核验）；非机器验证证书（OBL §10 升级门未过）",
    }
    w["witness_sha256"] = canonical_sha256(w)
    return w


def build_ns2(payload, run_meta):
    d = payload["ns2"]
    w = {
        "schema_version": SCHEMA_VERSION,
        "witness_id": f"ns-galerkin-energy-bound-{run_meta['date']}",
        "family": "ns-galerkin-energy-bound",
        "claim": "sampled_energy_bound",
        "inputs": {
            "n_cases": d["metrics"]["n_cases"],
            "ode": "x' = −ν·x + B(x,x) + f（skewB: B(a)(x,x)≡0；orthProjB: B(x,x)=‖x‖²g−(x·g)x），ModeSpace 1",
            "integrator": {"method": "DOP853", "rtol": repr(NS2_RTOL), "atol": repr(NS2_ATOL),
                           "role": "untrusted_candidate",
                           "note": "solve_ivp 仅产不可信候选轨道；认证由区间复算承载"},
            "n_samples_per_case": NS2_N_SAMPLES,
            "seed": SEED + 1,
            "cases": d["cases"],
        },
        "interval_engine": {"name": "mpmath.iv", "precision": f"dps={IV_DPS}", "rounding": "outward"},
        "rationalization": {"input_encoding": "repr(float64) 十进制字符串 → Fraction 精确有理",
                            "bound": "max(‖x₀‖², ‖f‖²/ν²) 由有理输入经 iv 区间算出"},
        "bounds": {"bound_rule": "max(‖x₀‖², ‖f‖²/ν²)",
                   "eta_rule": f"eta = max({NS2_ETA_REL}*(1+|bound_hi|), {NS2_NEXTAFTER_STEPS}×nextafter ulp)",
                   "max_defect": d["metrics"]["max_defect"]},
        "verdict": {"all_within_bound": True,
                    "certificate": "登记采样点上 ‖x(t_i)‖² ≤ bound + η（区间实证）",
                    "metrics": d["metrics"]},
        "honesty_boundary": NS2_HONESTY_BOUNDARY,
        "negative_control": {
            "perturbation": {"kind": d["neg"]["kind"], "case_tag": d["neg"]["case_tag"],
                             "sample_index": d["neg"]["sample_index"], "factor": d["neg"]["factor"],
                             "spec": "最紧案例最大范数采样点放大 ×1.0001 → 必须越出 bound+η"},
            "neg_verdict": {"neg_rejected": True, "neg_norm_sq_hi": d["neg"]["neg_norm_sq_hi"]},
            "same_lineage": _lineage(),
        },
        "replay": _replay(run_meta),
        "provenance": _provenance(["/mnt/agents/output/ws41-report.md (norm_sq_le_of_solution)",
                                   "ws41-src/NsGalerkin/Basic.lean (energy bound)",
                                   GEN_REL, RUNLOG_REL]),
        "lean_binding": None,
        "notes": "Grönwall 能量界的采样点区间实证（内生 fail-closed 见证复算核验）；非轨道包络、非机器验证证书（OBL §10 升级门未过）",
    }
    w["witness_sha256"] = canonical_sha256(w)
    return w


def build_ns3(payload, run_meta):
    w = {
        "schema_version": SCHEMA_VERSION,
        "witness_id": f"ns-trajectory-envelope-blocked-{run_meta['date']}",
        "family": "ns-trajectory-envelope-blocked",
        "claim": "blocked_registration",
        "inputs": {"scope": "2D NS Galerkin 截断 ODE 的完整严格轨道包络（RadiiPolynomial 级 CAP）",
                   "mode_spaces": "ModeSpace N 任意 N"},
        "interval_engine": {"name": "none", "note": "阻塞登记：未产出任何区间认证计算"},
        "rationalization": {"note": "不适用（无认证数值）"},
        "bounds": {"envelope": None, "note": "未产出任何轨道包络数值"},
        "verdict": {"blocked": True, "certified": False, "code": "B1"},
        "blocked": {"code": "B1", "kind": "structural/toolchain-missing",
                    "statement": payload["ns3"]["statement"],
                    "requirements": payload["ns3"]["requirements"],
                    "references": ["/mnt/agents/output/ws40-report.md §4（CAP 路线评估）",
                                   "/mnt/agents/output/ws41-report.md §3（堵报清单）"]},
        "negative_control": {"kind": "not_applicable",
                             "statement": "阻塞登记无正例宣称，负控语义不适用"},
        "replay": _replay(run_meta),
        "provenance": _provenance(["/mnt/agents/output/ws40-report.md",
                                   "/mnt/agents/output/ws41-report.md",
                                   GEN_REL, RUNLOG_REL]),
        "lean_binding": None,
        "notes": "阻塞登记非成果宣称：未产出、未尝试任何轨道包络数值；阻塞为结构性（B1 工具链缺），待 RadiiPolynomial 级工具链就位后由后续波次承接",
    }
    w["witness_sha256"] = canonical_sha256(w)
    return w


def build_manifest(witnesses, run_meta):
    return {
        "schema": "witnesses-ns-manifest/1.0",
        "run_id": run_meta["run_id"],
        "ts": run_meta["ts"],
        "generator": {"script": GEN_REL, "sha256": run_meta["script_sha"]},
        "verifier": {"script": VER_REL, "sha256": run_meta["verifier_sha"]},
        "witnesses": [{"witness_id": w["witness_id"],
                       "file": w["witness_id"] + ".witness.json",
                       "sha256": w["witness_sha256"],
                       "family": w["family"],
                       "verdict": ("blocked(B1)" if w["family"].endswith("blocked")
                                   else "all_pass")} for w in witnesses],
        "counts": {
            "ns1_cases": witnesses[0]["verdict"]["metrics"]["n_cases"],
            "ns1_per_form": witnesses[0]["verdict"]["metrics"]["per_form"],
            "ns2_cases": witnesses[1]["verdict"]["metrics"]["n_cases"],
            "ns2_samples_total": witnesses[1]["verdict"]["metrics"]["n_samples_total"],
            "ns2_per_kind": witnesses[1]["verdict"]["metrics"]["per_kind"],
        },
        "blocked": [{"witness_id": witnesses[2]["witness_id"], "code": "B1",
                     "kind": "structural/toolchain-missing",
                     "statement": witnesses[2]["blocked"]["statement"],
                     "requirements": witnesses[2]["blocked"]["requirements"]}],
        "consistency_gate": "双跑决定论一致性（主流程 vs --emit-raw 独立子进程，规范化 JSON 逐字节一致方签发）",
        "env_fp": run_meta["env_fp"],
        "notes": "W-NS1/W-NS2=区间实证见证（内生 fail-closed 复算核验，非机器验证证书）；W-NS3=阻塞登记（BLOCKED B1）",
    }


def main():
    ap = argparse.ArgumentParser(description="WS-43 NS 见证生成器（schema v1.0）")
    ap.add_argument("--out", default=os.path.join(REPO_ROOT, "artifacts", "witnesses-ns"))
    ap.add_argument("--emit-raw", metavar="PATH", help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args.emit_raw:
        with open(args.emit_raw, "wb") as fh:
            fh.write(_canonical_blob(compute_payload()))
        return 0

    payload = compute_payload()
    consistency_gate(payload)

    now = datetime.datetime.now(datetime.timezone.utc)
    run_meta = {
        "date": now.strftime("%Y%m%d"),
        "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_id": f"ws43-ns-{now.strftime('%Y%m%dT%H%M%SZ')}",
        "env_fp": env_fp(),
        "script_sha": sha256_file(os.path.join(REPO_ROOT, GEN_REL)),
        "verifier_sha": sha256_file(os.path.join(REPO_ROOT, VER_REL)),
    }

    out_dir = args.out
    tmp_out = tempfile.mkdtemp(prefix="ws43-wit-", dir=os.path.dirname(out_dir) or ".")
    try:
        runlog = {
            "run_id": run_meta["run_id"], "ts": run_meta["ts"], "seed": SEED,
            "payload_sha256": hashlib.sha256(_canonical_blob(payload)).hexdigest(),
            "counts": {"ns1_cases": payload["ns1"]["metrics"]["n_cases"],
                       "ns2_cases": payload["ns2"]["metrics"]["n_cases"],
                       "ns2_samples_total": payload["ns2"]["metrics"]["n_samples_total"]},
            "consistency_gate": "passed（双跑逐字节一致）",
            "env_fp": run_meta["env_fp"],
        }
        runlog_path = os.path.join(tmp_out, "run-log.json")
        with open(runlog_path, "w", encoding="utf-8") as fh:
            json.dump(runlog, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        run_meta["runlog_sha"] = sha256_file(runlog_path)
        # run-log sha 进入见证 → 见证须在 run-log 之后定稿（此处重建三件）
        witnesses = [build_ns1(payload, run_meta), build_ns2(payload, run_meta),
                     build_ns3(payload, run_meta)]
        for w in witnesses:
            with open(os.path.join(tmp_out, w["witness_id"] + ".witness.json"), "w",
                      encoding="utf-8") as fh:
                json.dump(w, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
        manifest = build_manifest(witnesses, run_meta)
        with open(os.path.join(tmp_out, "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        shutil.move(tmp_out, out_dir)
    except Exception:
        shutil.rmtree(tmp_out, ignore_errors=True)
        raise

    print(f"run_id={run_meta['run_id']} 生成见证 {len(witnesses)} 件 + manifest → {out_dir}")
    for w in witnesses:
        print(f"  {w['witness_id']}  sha256={w['witness_sha256'][:16]}…")
    print(f"  ns1_cases={payload['ns1']['metrics']['n_cases']} "
          f"ns2_cases={payload['ns2']['metrics']['n_cases']} "
          f"ns2_samples={payload['ns2']['metrics']['n_samples_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
