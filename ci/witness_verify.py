# CLASSIFY: L1
# witness_verify.py · CIRC 重做 route B「见证认证」M0 独立核验器（schema v1.0 · fail-closed）
#
# 规格：board/CIRC-REWORK-M0-SPEC-01.md §0/§2/§3。
# 独立性：本文件与 ci/witness_gen.py 零共享代码路径（IF-M2 达标形态）；区间复算由本文件
#         自含实现（circulant: mpmath.iv 外向舍入 Krawczyk；auction: np.nextafter 定向端点
#         区间算术 + HiGHS 仅作不可信候选生成器），不 import 锚定复算脚本。
# 判定语义（OBL §0.1 默认拒绝律）：
#   · 任一检查 false / 证据缺失 / 异常 → 整体 fail，退出码 1；
#   · 缺 schema_version → 拒绝受理；major ≠ 1 → unsupported_schema 拒验（禁止静默降级）；
#   · minor > 0 向后兼容受理并显式登记；
#   · 度量比对容差 = 逐字符串一致（数值比对仅对字符串解析后的有理/区间量）；
#   · 负控必须拒证：circulant neg_inside 复算必须 false；auction neg_cost 必须在括弧外；
#   · 证书不咨询闭形式解（披露锚 §5.1 纪律）：本核验器不使用 g* 闭式，仅以见证登记的
#     有理中心为证书输入复算 Krawczyk 内包。
#
# witness_sha256 规范化序列化规则（M0 interim，U4 待冻结；与 witness_gen.py 文首一致）：
#   json.dumps(除去 witness_sha256 的对象, sort_keys=True, separators=(",", ":"),
#              ensure_ascii=False).encode("utf-8") 的 sha256 十六进制小写。
#
# 用法：python3 ci/witness_verify.py WITNESS.json [WITNESS2.json ...] [--json]
#   退出码 0=全部通过；1=任一失败或异常；2=用法错误。
import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction

SUPPORTED_MAJOR = 1

TOP_REQUIRED = ["schema_version", "witness_id", "family", "claim", "inputs",
                "interval_engine", "rationalization", "bounds", "verdict",
                "negative_control", "replay", "provenance", "witness_sha256"]


def _canon_sha256(witness_obj):
    obj = {k: v for k, v in witness_obj.items() if k != "witness_sha256"}
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_rational(s):
    """解析有理/十进制字符串 → Fraction（接受 "num/den"、整数、小数、科学计数法）。"""
    if not isinstance(s, str):
        raise ValueError(f"非字符串数值登记: {s!r}")
    s = s.strip()
    if "/" in s and not s.startswith("/"):
        num, den = s.split("/")
        return Fraction(int(num.strip()), int(den.strip()))
    return Fraction(s)


def _find_repo_root(witness_path, script_rel):
    """自见证文件向上找到含 replay.script_path 的仓根；回退核验器自身仓根；找不到返回 None。"""
    d = os.path.abspath(os.path.dirname(witness_path))
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


def _check_schema(w, cl):
    sv = w.get("schema_version")
    if sv is None:
        cl.add("schema_version_present", False, "缺 schema_version，拒绝受理（默认拒绝律延伸至格式层）")
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
               f"unsupported_schema: major={major} 高于/异于核验器支持 {SUPPORTED_MAJOR}（fail-closed，禁止静默降级）")
        return False
    detail = f"major={major} 受理"
    if minor > 0:
        detail += f"；minor={minor} 向后兼容受理（纯增字段以显式缺省补全并登记）"
    cl.add("schema_major_dispatch", True, detail)
    return True


def _check_common(w, cl, witness_path):
    missing = [f for f in TOP_REQUIRED if f not in w]
    cl.add("required_top_fields", not missing, f"missing={missing}" if missing else "齐")
    if missing:
        return False
    cl.add("witness_sha256", _canon_sha256(w) == w["witness_sha256"], "规范化序列化复算")
    lb = w.get("lean_binding", None)
    cl.add("lean_binding_null", lb is None, "M0 恒 null（C3：禁止任何 Lean 通过性声明）")
    # env_fp 无 lean/mathlib 维度（M0-AC5，U3 interim）
    pkgs = (w["replay"].get("env_fp") or {}).get("packages") or {}
    blob = json.dumps(pkgs).lower()
    cl.add("env_lean_free", ("lean" not in blob and "mathlib" not in blob),
           f"packages={sorted(pkgs)}（interim：runner 声明+依赖清单哈希代偿）")
    # replay 指针完整性：脚本/结果文件 sha256 与登记一致
    rp = w["replay"]
    repo = _find_repo_root(witness_path, rp.get("script_path", ""))
    if repo is None:
        cl.add("replay_script_sha256", False, f"无法在仓内定位 {rp.get('script_path')}")
        cl.add("replay_results_sha256", False, "仓根未定")
        return False
    sp = os.path.join(repo, rp["script_path"])
    cl.add("replay_script_sha256", _sha256_file(sp) == rp.get("script_sha256"), rp["script_path"])
    rp_results = rp.get("results_path")
    if rp_results and os.path.isfile(os.path.join(repo, rp_results)):
        cl.add("replay_results_sha256",
               _sha256_file(os.path.join(repo, rp_results)) == rp.get("results_sha256"), rp_results)
    else:
        cl.add("replay_results_sha256", False, f"结果文件缺失: {rp_results}")
    return cl.ok


# ---------------------------------------------------------------- circulant

def _circ_F(k, c, eps, center_iv):
    """Ff_i = f_i+eps·(log k + log Σ_j exp((g_j−c_{j−i})/eps))；Fg_j 对称（f0≡0）。"""
    from mpmath import iv
    e = iv.mpf(eps.numerator) / eps.denominator
    f = [iv.mpf(0)] + list(center_iv[:k - 1])
    g = list(center_iv[k - 1:])
    logk = iv.log(k)
    out = []
    for i in range(1, k):
        s = iv.mpf(0)
        for j in range(k):
            s += iv.exp((g[j] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
        out.append(f[i] + e * logk + e * iv.log(s))
    for j in range(k):
        s = iv.mpf(0)
        for i in range(k):
            s += iv.exp((f[i] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
        out.append(g[j] + e * logk + e * iv.log(s))
    return out


def _circ_jac_iv(k, c, eps, box):
    from mpmath import iv
    n = 2 * k - 1
    e = iv.mpf(eps.numerator) / eps.denominator
    f = [iv.mpf(0)] + list(box[:k - 1])
    g = list(box[k - 1:])
    S = []
    for i in range(1, k):
        s = iv.mpf(0)
        for j in range(k):
            s += iv.exp((g[j] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
        S.append(s)
    T = []
    for j in range(k):
        s = iv.mpf(0)
        for i in range(k):
            s += iv.exp((f[i] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
        T.append(s)
    J = [[iv.mpf(0)] * n for _ in range(n)]
    for r in range(k - 1):
        i = r + 1
        J[r][r] = iv.mpf(1)
        for j in range(k):
            J[r][k - 1 + j] = iv.exp((g[j] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e) / S[r]
    for j in range(k):
        row = k - 1 + j
        J[row][row] = iv.mpf(1)
        for i in range(1, k):
            J[row][i - 1] = iv.exp((f[i] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e) / T[j]
    return J


def _circ_jac_mp(k, c, eps, center):
    from mpmath import mp, mpf, exp
    n = 2 * k - 1
    e = mpf(eps.numerator) / eps.denominator
    f = [mpf(0)] + [mpf(t.numerator) / t.denominator for t in center[:k - 1]]
    g = [mpf(t.numerator) / t.denominator for t in center[k - 1:]]
    S = []
    for i in range(1, k):
        s = mpf(0)
        for j in range(k):
            s += exp((g[j] - mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
        S.append(s)
    T = []
    for j in range(k):
        s = mpf(0)
        for i in range(k):
            s += exp((f[i] - mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
        T.append(s)
    J = mp.zeros(n, n)
    for r in range(k - 1):
        i = r + 1
        J[r, r] = 1
        for j in range(k):
            J[r, k - 1 + j] = exp((g[j] - mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e) / S[r]
    for j in range(k):
        row = k - 1 + j
        J[row, row] = 1
        for i in range(1, k):
            J[row, i - 1] = exp((f[i] - mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e) / T[j]
    return J


def _circ_preconditioner(k, c, eps, center, precond_den):
    from mpmath import mp, mpf, iv
    Cinv = mp.inverse(_circ_jac_mp(k, c, eps, center))
    n = 2 * k - 1
    C = []
    for r in range(n):
        row = []
        for s in range(n):
            q = Fraction(mp.nstr(mpf(Cinv[r, s]), 40)).limit_denominator(precond_den)
            row.append(iv.mpf(q.numerator) / q.denominator)
        C.append(row)
    return C


def _circ_krawczyk(k, c, eps, center, box, C):
    """K(X)=center−C·F(center)+(I−C·J(X))·(X−center) → (inside, max_width, min_margin)。"""
    from mpmath import iv
    n = 2 * k - 1
    Fc = _circ_F(k, c, eps, [iv.mpf(t.numerator) / t.denominator for t in center])
    JI = _circ_jac_iv(k, c, eps, box)
    CFc = []
    for r in range(n):
        acc = iv.mpf(0)
        for s in range(n):
            acc += C[r][s] * Fc[s]
        CFc.append(acc)
    CJ = [[sum(C[r][t] * JI[t][s] for t in range(n)) for s in range(n)] for r in range(n)]
    M = [[(iv.mpf(1) if r == s else iv.mpf(0)) - CJ[r][s] for s in range(n)] for r in range(n)]
    Delta = [box[i] - (iv.mpf(center[i].numerator) / center[i].denominator) for i in range(n)]
    MD = [sum(M[r][s] * Delta[s] for s in range(n)) for r in range(n)]
    K = [iv.mpf(center[r].numerator) / center[r].denominator - CFc[r] + MD[r] for r in range(n)]
    inside = all(K[r].a > box[r].a and K[r].b < box[r].b for r in range(n))
    maxw = max(float(K[r].b) - float(K[r].a) for r in range(n))
    margin = min(min(float((K[r].a - box[r].a).a), float((box[r].b - K[r].b).a)) for r in range(n))
    return bool(inside), maxw, margin


def _circ_run(k, c, eps, ghat, box_radius, precond_den, neg_shift=None):
    from mpmath import iv, mpi
    n = 2 * k - 1
    g = ghat if neg_shift is None else ghat + neg_shift
    center = [Fraction(0)] * (k - 1) + [g] * k
    rad = mpi(-box_radius.numerator, box_radius.numerator) / box_radius.denominator
    box = [iv.mpf(t.numerator) / t.denominator + rad for t in center]
    C = _circ_preconditioner(k, c, eps, center, precond_den)
    inside, maxw, margin = _circ_krawczyk(k, c, eps, center, box, C)
    return inside, maxw, margin


def _verify_circulant(w, cl):
    from mpmath import mp, iv
    import numpy as np
    eng = w["interval_engine"]
    cl.add("engine_supported",
           eng.get("name") == "mpmath.iv" and eng.get("rounding") == "outward"
           and eng.get("precision") == "dps=80",
           json.dumps(eng, ensure_ascii=False))
    if eng.get("name") != "mpmath.iv":
        return
    mp.dps = 80
    iv.dps = 80
    inp, bnd, neg = w["inputs"], w["bounds"], w["negative_control"]
    k = int(inp["k"])
    eps = _parse_rational(inp["eps"])
    c = [_parse_rational(v) for v in inp["c"]]
    cl.add("inputs_shape", len(c) == k and int(inp["n"]) == 2 * k - 1
           and inp.get("gauge") == "f0=0" and w.get("claim") == "unique_root_in_box",
           f"k={k} n={inp.get('n')}")
    ghat = _parse_rational(bnd["center"]["g"])
    freg = bnd["center"].get("f")
    cl.add("center_f_zero", freg == ["0"] * (k - 1), f"f 登记={freg}")
    box_radius = _parse_rational(bnd["box_radius"])
    precond_den = int(_parse_rational(bnd["preconditioner"]["limit_denominator"]))
    cl.add("preconditioner_kind",
           bnd["preconditioner"].get("kind") == "rationalized_inverse_jacobian",
           bnd["preconditioner"].get("kind", ""))

    inside, maxw, margin = _circ_run(k, c, eps, ghat, box_radius, precond_den)
    cl.add("recompute_inside", inside, "Krawczyk 严格内包复算")
    cl.add("verdict_inside_true", w["verdict"].get("inside") is True, str(w["verdict"].get("inside")))
    cl.add("metric_K_max_width", repr(maxw) == bnd["krawczyk_image"]["max_width"]
           == w["verdict"]["metrics"]["K_max_width"],
           f"复算={repr(maxw)} 登记={bnd['krawczyk_image']['max_width']}")
    cl.add("metric_K_min_margin", repr(margin) == bnd["krawczyk_image"]["min_margin"]
           == w["verdict"]["metrics"]["K_min_margin"],
           f"复算={repr(margin)} 登记={bnd['krawczyk_image']['min_margin']}")
    Jn = np.array([[float(_circ_jac_mp(k, c, eps, [Fraction(0)] * (k - 1) + [ghat] * k)[r, s])
                    for s in range(2 * k - 1)] for r in range(2 * k - 1)])
    cond = float(np.linalg.cond(Jn))
    cl.add("metric_condJ", repr(cond) == w["verdict"]["metrics"]["condJ"],
           f"复算={repr(cond)} 登记={w['verdict']['metrics']['condJ']}")

    # 负控：g 中心 +delta（重算预条件子）→ 内包必须失败
    p = neg.get("perturbation", {})
    cl.add("neg_perturbation_spec",
           p.get("kind") == "center_shift" and p.get("target") == "g"
           and p.get("preconditioner") == "recomputed",
           json.dumps(p, ensure_ascii=False))
    delta = _parse_rational(p.get("delta", "0"))
    n_inside, _, n_margin = _circ_run(k, c, eps, ghat, box_radius, precond_den, neg_shift=delta)
    cl.add("neg_recompute_rejected", n_inside is False,
           f"扰动后内包={n_inside}（必须 False，fail-closed）")
    cl.add("neg_registered_false", neg["neg_verdict"].get("neg_inside") is False,
           str(neg["neg_verdict"].get("neg_inside")))
    cl.add("neg_metric_margin", repr(n_margin) == neg["neg_verdict"]["neg_K_min_margin"],
           f"复算={repr(n_margin)} 登记={neg['neg_verdict']['neg_K_min_margin']}")
    cl.add("neg_same_lineage", bool(neg.get("same_lineage", {}).get("same_script")),
           "负控与正例同脚本同环境声明")


# ---------------------------------------------------------------- auction

def _auct_gen_C(k, R, seed):
    import numpy as np
    rng = np.random.default_rng(seed)
    rng.random(k)
    rng.random(k)
    return 10.0 ** (R * (2 * rng.random((k, k)) - 1))


def _auct_forward(C, eps, p=None, assign=None):
    import numpy as np
    k = C.shape[0]
    if p is None:
        p = np.zeros(k)
    if assign is None:
        assign = {}
    owner = {j: i for i, j in assign.items()}
    bids = 0
    unassigned = [i for i in range(k) if i not in assign]
    while unassigned:
        i = unassigned.pop(0)
        v = -C[i] - p
        order = np.argsort(v)[::-1]
        j1 = order[0]
        best = v[j1]
        second = v[order[1]] if k > 1 else -np.inf
        p[j1] = p[j1] + (best - second) + eps
        bids += 1
        if j1 in owner:
            prev = owner[j1]
            del owner[j1]
            del assign[prev]
            unassigned.append(prev)
        assign[i] = j1
        owner[j1] = i
    return assign, p, bids


def _auct_scaling(C, eps0, factor, eps_final):
    import numpy as np
    p = np.zeros(C.shape[0])
    assign = {}
    eps = eps0
    rounds = 0
    bids = 0
    while True:
        for i, j in list(assign.items()):
            if (-C[i] - p).max() - (-C[i, j] - p[j]) > eps + 1e-15:
                del assign[i]
        assign, p, b = _auct_forward(C, eps, p, assign)
        rounds += 1
        bids += b
        if eps <= eps_final:
            break
        eps = eps / factor
        if eps < eps_final:
            eps = eps_final
    return assign, p, rounds, bids


def _nextafter(v, d):
    import numpy as np
    return float(np.nextafter(v, d))


def _iv_pt(v):
    return (float(v), float(v))


def _iv_add(a, b):
    import numpy as np
    return (_nextafter(a[0] + b[0], -np.inf), _nextafter(a[1] + b[1], np.inf))


def _iv_sub(a, b):
    import numpy as np
    return (_nextafter(a[0] - b[1], -np.inf), _nextafter(a[1] - b[0], np.inf))


def _iv_mul(a, b):
    import numpy as np
    ps = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (_nextafter(min(ps), -np.inf), _nextafter(max(ps), np.inf))


def _auct_certify(C, k, delta):
    """F-X3 对偶括弧认证复算：HiGHS 仅作不可信候选生成器，np.nextafter 定向端点区间算术。"""
    import numpy as np
    from scipy.optimize import linprog
    kk = k * k
    c = C.flatten()
    Aeq = np.zeros((2 * k, kk))
    for i in range(k):
        Aeq[i, i * k:(i + 1) * k] = 1.0
    for j in range(k):
        Aeq[k + j, j::k] = 1.0
    beq = np.full(2 * k, 1.0 / k)
    res = linprog(c, A_eq=Aeq, b_eq=beq, method="highs")
    if res.status != 0:
        raise RuntimeError(f"HiGHS failed: {res.message}")
    y0 = res.eqlin.marginals
    x = res.x

    def rc_min_lo(yv):
        lo = np.inf
        for j in range(kk):
            s = _iv_add(_iv_pt(yv[j // k]), _iv_pt(yv[k + j % k]))
            rc = _iv_sub(_iv_pt(c[j]), s)
            lo = min(lo, rc[0])
        return lo

    deflated = rc_min_lo(y0) < 0
    yv = (1 - delta) * np.asarray(y0) if deflated else np.asarray(y0)
    rc_lo = rc_min_lo(yv)

    beq_iv = (_nextafter(1.0 / k, -np.inf), _nextafter(1.0 / k, np.inf))
    LB = (0.0, 0.0)
    for i in range(2 * k):
        LB = _iv_add(LB, _iv_mul(beq_iv, _iv_pt(yv[i])))
    UB = (0.0, 0.0)
    for j in range(kk):
        UB = _iv_add(UB, _iv_mul(_iv_pt(c[j]), _iv_pt(float(x[j]))))
    br = (_nextafter(k * LB[0], -np.inf), _nextafter(k * UB[1], np.inf))
    return {
        "dual_feasible_certified": bool(rc_lo >= 0),
        "deflated": bool(deflated),
        "rc_min_lo": rc_lo,
        "bracket": br,
        "bracket_width": br[1] - br[0],
    }


def _verify_auction(w, cl):
    eng = w["interval_engine"]
    cl.add("engine_supported",
           eng.get("name") == "numpy.nextafter" and eng.get("rounding") == "directed_endpoints",
           json.dumps(eng, ensure_ascii=False))
    if eng.get("name") != "numpy.nextafter":
        return
    cl.add("honesty_boundary_present", isinstance(w.get("honesty_boundary"), str)
           and "HiGHS" in w["honesty_boundary"],
           "C7：UB=c·x 未经区间认证的诚实边界必须携带")
    inp, bnd, neg = w["inputs"], w["bounds"], w["negative_control"]
    k = int(inp["k"])
    R = float(inp["R"])
    seed = int(inp["seed"])
    sch = inp["eps_schedule"]
    eps0 = float(_parse_rational(sch["eps0"]))
    fac_s = sch["factor"]
    factor = float(_parse_rational(fac_s[1:])) if fac_s.startswith("/") else float(_parse_rational(fac_s))
    eps_final = float(_parse_rational(sch["eps_final"]))
    cl.add("inputs_shape", w.get("claim") == "cost_in_dual_bracket" and k >= 2,
           f"k={k} R={inp['R']} seed={seed} schedule={json.dumps(sch)}")

    C = _auct_gen_C(k, R, seed)
    assign, p, rounds, bids = _auct_scaling(C, eps0, factor, eps_final)
    cost = float(sum(C[i, j] for i, j in assign.items()))
    cl.add("metric_auction_cost", repr(cost) == bnd["auction_cost"],
           f"复算={repr(cost)} 登记={bnd['auction_cost']}")
    cl.add("metric_rounds_bids", rounds == bnd.get("rounds") and bids == bnd.get("bids"),
           f"复算=({rounds},{bids}) 登记=({bnd.get('rounds')},{bnd.get('bids')})")
    resid = float(max((-C[i] - p).max() - (-C[i, j] - p[j]) for i, j in assign.items()))
    cl.add("metric_epsCS_residual", repr(resid) == bnd["epsCS_residual"],
           f"复算={repr(resid)} 登记={bnd['epsCS_residual']}")

    delta = float(_parse_rational(bnd["delta_deflation"]))
    cert = _auct_certify(C, k, delta)
    lo, hi = cert["bracket"]
    cl.add("metric_bracket", repr(lo) == bnd["bracket"]["lb_lo"] and repr(hi) == bnd["bracket"]["ub_hi"],
           f"复算=({repr(lo)},{repr(hi)}) 登记=({bnd['bracket']['lb_lo']},{bnd['bracket']['ub_hi']})")
    cl.add("metric_bracket_width", repr(cert["bracket_width"]) == bnd["bracket_width"],
           f"复算={repr(cert['bracket_width'])} 登记={bnd['bracket_width']}")
    cl.add("metric_rc_min_lo", repr(cert["rc_min_lo"]) == bnd["rc_min_lo"],
           f"复算={repr(cert['rc_min_lo'])} 登记={bnd['rc_min_lo']}")
    cl.add("metric_deflated", cert["deflated"] == bnd.get("deflated"),
           f"复算={cert['deflated']} 登记={bnd.get('deflated')}")
    gap = cost - lo
    gap_bound = k * eps_final
    cl.add("metric_gap", repr(gap) == bnd["gap"], f"复算={repr(gap)} 登记={bnd['gap']}")
    cl.add("metric_gap_bound", repr(gap_bound) == bnd["gap_bound_value"],
           f"复算={repr(gap_bound)} 登记={bnd['gap_bound_value']}")

    inside = bool(lo < cost < hi) and cert["dual_feasible_certified"]
    cl.add("recompute_inside", inside, "cost∈括弧 ∧ 对偶可行认证")
    v = w["verdict"]
    cl.add("verdict_trio", v.get("inside") is True and v.get("gap_within_bound") is True
           and v.get("dual_feasible_certified") is True
           and (gap <= gap_bound) and cert["dual_feasible_certified"],
           json.dumps({kk: v.get(kk) for kk in ("inside", "gap_within_bound", "dual_feasible_certified")}))

    # 负控：交换增量最大的一对分配 → cost 必须越出括弧
    items = sorted(assign.items())
    worst = None
    for a in range(k):
        for b in range(a + 1, k):
            i1, j1 = items[a]
            i2, j2 = items[b]
            c2 = cost - C[i1, j1] - C[i2, j2] + C[i1, j2] + C[i2, j1]
            if worst is None or c2 > worst[0]:
                worst = (float(c2), [int(i1), int(j1), int(i2), int(j2)])
    neg_cost, neg_swap = worst
    cl.add("neg_recompute_rejected", not (lo < neg_cost < hi),
           f"扰动 cost={repr(neg_cost)} 在括弧外（必须越界，fail-closed）")
    cl.add("neg_registered_true", neg["neg_verdict"].get("neg_rejected") is True,
           str(neg["neg_verdict"].get("neg_rejected")))
    cl.add("neg_metric_cost", repr(neg_cost) == neg["neg_verdict"]["neg_cost"],
           f"复算={repr(neg_cost)} 登记={neg['neg_verdict']['neg_cost']}")
    cl.add("neg_swap_match", neg.get("perturbation", {}).get("swap") == neg_swap,
           f"复算={neg_swap} 登记={neg.get('perturbation', {}).get('swap')}")
    cl.add("neg_same_lineage", bool(neg.get("same_lineage", {}).get("same_script")),
           "负控与正例同脚本同环境声明")


# ---------------------------------------------------------------- driver

def verify_witness(path):
    """核验单件见证 → verdict dict（fail-closed：任何异常即 fail）。"""
    cl = _Checklist()
    try:
        with open(path, encoding="utf-8") as fh:
            w = json.load(fh)
    except Exception as e:
        return {"witness": path, "ok": False,
                "checks": [{"check": "parse_json", "ok": False, "detail": repr(e)}]}
    try:
        if not _check_schema(w, cl):
            return {"witness": path, "witness_id": w.get("witness_id"), "ok": False, "checks": cl.checks}
        if not _check_common(w, cl, path):
            return {"witness": path, "witness_id": w.get("witness_id"), "ok": False, "checks": cl.checks}
        fam = w["family"]
        if fam == "circulant-sinkhorn":
            _verify_circulant(w, cl)
        elif fam == "auction-dual":
            _verify_auction(w, cl)
        else:
            cl.add("family_known", False, f"未知族: {fam!r}")
    except Exception as e:
        cl.add("exception", False, f"{type(e).__name__}: {e}")
    return {"witness": path, "witness_id": w.get("witness_id"), "ok": cl.ok, "checks": cl.checks}


def main(argv=None):
    ap = argparse.ArgumentParser(description="M0 见证独立核验器（fail-closed）")
    ap.add_argument("witnesses", nargs="+")
    ap.add_argument("--json", action="store_true", help="打印完整逐检查项 JSON")
    args = ap.parse_args(argv)
    verdicts = [verify_witness(p) for p in args.witnesses]
    all_ok = all(v["ok"] for v in verdicts)
    if args.json:
        print(json.dumps(verdicts, ensure_ascii=False, indent=2))
    else:
        for v in verdicts:
            n_ok = sum(1 for c in v["checks"] if c["ok"])
            print(f"{'PASS' if v['ok'] else 'FAIL'} {v.get('witness_id') or v['witness']} "
                  f"({n_ok}/{len(v['checks'])} checks)")
            for c in v["checks"]:
                if not c["ok"]:
                    print(f"    ✗ {c['check']}: {c['detail']}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
