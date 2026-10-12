# CLASSIFY: L1
# witness_ns_verify.py · EXT-WAVE-09「NS」波 WS-43 数值见证独立核验器（schema v1.0 · fail-closed）
#
# 对象：2D Navier–Stokes Galerkin 截断（WS-41 Lean 核 GalerkinNS / skewB 实例）的三件数值见证：
#   · family "ns-energy-cancellation"（W-NS1）：能量相消代数见证。对 skewB 显式实例
#     （ModeSpace 1 = Fin 3 / N=2 = Fin 5）与 orthProjB 非平凡实例，对随机/退化/大范数 interval
#     点区间验证 ⟪B(u,u),u⟫ ∋ 0 且包络宽度 ≤ 容差（mpmath.iv dps=50 外向舍入）。
#   · family "ns-galerkin-energy-bound"（W-NS2）：Grönwall 能量界采样证书。 scipy solve_ivp
#     高密度采样产**不可信候选轨道**；本核验器对登记采样点做区间求值 ‖x(t_i)‖² ≤ bound+η，
#     bound = max(‖x₀‖², ‖f‖²/ν²) 由有理输入区间算出，η 为 nextafter/积分器余量（登记规则）。
#     诚实边界：证书仅断言「采样点上界成立」，**非轨道包络**（CAP 级包络见 W-NS3 阻塞登记）。
#   · family "ns-trajectory-envelope-blocked"（W-NS3）：完整轨道包络（RadiiPolynomial 级 CAP）
#     阻塞登记。本核验器仅做结构核验：blocked.code="B1"、certified=false、无包络数值宣称。
#
# 独立性：本文件与 ci/witness_ns_gen.py **零共享代码路径**（IF-M2 形态延伸）：区间复算、
#         ODE 候选积分、容差规则均由本文件自含实现；不 import 生成器或其任何产物模块。
#         scipy/solve_ivp 在本核验器中仅作**不可信候选**生成器（WS-37 auction 范式同款纪律）；
#         认证性判定只依赖登记数据的 mpmath.iv 区间复算。
#
# 判定语义（默认拒绝律，沿用 WS-37 M0 口径）：
#   · 任一检查 false / 证据缺失 / 异常 → 整体 fail，退出码 1；
#   · 缺 schema_version → 拒绝受理；major ≠ 1 → unsupported_schema 拒验（禁止静默降级）；
#   · 度量比对容差 = 逐字符串一致（数值比对仅对字符串解析后的有理/区间量）；
#   · 负控必须拒证并复算确认；
#   · lean_binding 恒 null（C3：禁止任何 Lean 通过性声明）；env_fp 无 lean/mathlib 维度。
#
# witness_sha256 规范化序列化规则（沿用 WS-37 M0 interim 规则）：
#   json.dumps(除去 witness_sha256 的对象, sort_keys=True, separators=(",", ":"),
#              ensure_ascii=False).encode("utf-8") 的 sha256 十六进制小写。
#
# 区间计算规范（生成器/核验器各自独立实现同一规范，以保证端点逐比特一致）：
#   · 十进制字符串 s → Fraction(s) → iv.mpf(分子)/iv.mpf(分母)（dps=50，外向舍入）；
#   · 求和一律按下标升序从左到右累加，初值 iv.mpf(0)；
#   · skewB 形式：s = Σ_j a_j·u_j，t = Σ_j a_j·v_j（v=u，独立第二遍求和），
#     B_i = s·u_i − t·u_i，inner = Σ_i B_i·u_i；
#   · orthProjB 形式：p = Σ_j u_j²，q = Σ_j g_j·u_j，B_i = p·g_i − q·u_i，inner = Σ_i B_i·u_i；
#   · 容差：width ≤ max(1e-45, 1e-38·mag)，mag 为各形式登记的上尺度（见 _ns1_mag）。
#
# 用法：python3 ci/witness_ns_verify.py WITNESS.json [WITNESS2.json ...] [--json]
#   退出码 0=全部通过；1=任一失败或异常；2=用法错误。
import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction

SUPPORTED_MAJOR = 1
IV_DPS = 50

TOP_REQUIRED = ["schema_version", "witness_id", "family", "claim", "inputs",
                "interval_engine", "rationalization", "bounds", "verdict",
                "negative_control", "replay", "provenance", "witness_sha256"]

NS2_DEV_TOL = 1e-6          # 候选轨道与登记采样点的最大容许偏差（不可信层一致性闸）
NS2_ETA_REL = 1e-9          # 采样证书的相对余量（覆盖非严格积分器误差，见诚实边界）
NS2_NEXTAFTER_STEPS = 8     # 双括号余量的 nextafter 步数


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


def _find_repo_root(witness_path, script_rel):
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
    cl.add("schema_major_dispatch", True, f"major={major} 受理" + (f"；minor={minor} 兼容受理" if minor > 0 else ""))
    return True


def _check_common(w, cl, witness_path):
    missing = [f for f in TOP_REQUIRED if f not in w]
    cl.add("required_top_fields", not missing, f"missing={missing}" if missing else "齐")
    if missing:
        return False
    cl.add("witness_sha256", _canon_sha256(w) == w["witness_sha256"], "规范化序列化复算")
    cl.add("lean_binding_null", w.get("lean_binding") is None, "恒 null（C3）")
    pkgs = (w["replay"].get("env_fp") or {}).get("packages") or {}
    blob = json.dumps(pkgs).lower()
    cl.add("env_lean_free", ("lean" not in blob and "mathlib" not in blob),
           f"packages={sorted(pkgs)}")
    rp = w["replay"]
    repo = _find_repo_root(witness_path, rp.get("script_path", ""))
    if repo is None:
        cl.add("replay_script_sha256", False, f"无法在仓内定位 {rp.get('script_path')}")
        cl.add("replay_results_sha256", False, "仓根未定")
        return False
    cl.add("replay_script_sha256",
           _sha256_file(os.path.join(repo, rp["script_path"])) == rp.get("script_sha256"),
           rp["script_path"])
    rp_results = rp.get("results_path")
    if rp_results and os.path.isfile(os.path.join(repo, rp_results)):
        cl.add("replay_results_sha256",
               _sha256_file(os.path.join(repo, rp_results)) == rp.get("results_sha256"), rp_results)
    else:
        cl.add("replay_results_sha256", False, f"结果文件缺失: {rp_results}")
    return cl.ok


# ---------------------------------------------------------------- 公共区间件

def _iv_from_str(s):
    """十进制字符串 → mpmath.iv 区间（规范见文件头）。"""
    from mpmath import iv
    fr = Fraction(str(s).strip())
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def _skewb_inner(a, u):
    """⟪skewB(a)(u,u),u⟫：s=⟪a,u⟫, t=⟪a,u⟫（独立第二遍）, B_i=s·u_i−t·u_i, inner=Σ B_i·u_i。"""
    s = _iv_sum_raw([a[j] * u[j] for j in range(len(u))])
    t = _iv_sum_raw([a[j] * u[j] for j in range(len(u))])
    B = [s * u[i] - t * u[i] for i in range(len(u))]
    return _iv_sum_raw([B[i] * u[i] for i in range(len(u))])


def _orthproj_inner(g, u):
    """⟪B(u,u),u⟫，B(u,v)=(u·v)g−(v·g)u：p=Σu², q=Σg·u, B_i=p·g_i−q·u_i。"""
    p = _iv_sum_raw([u[j] * u[j] for j in range(len(u))])
    q = _iv_sum_raw([g[j] * u[j] for j in range(len(u))])
    B = [p * g[i] - q * u[i] for i in range(len(u))]
    return _iv_sum_raw([B[i] * u[i] for i in range(len(u))])


def _iv_sum_raw(terms):
    from mpmath import iv
    acc = iv.mpf(0)
    for t in terms:
        acc = acc + t
    return acc


def _ns1_mag(form, coeffs, u):
    """包络宽度容差的上尺度（规范件，双端各自独立实现同一公式）。
    skewB: mag = (Σ_j |a_j·u_j|)·(Σ_j u_j²)；orthProjB: mag = Σ_i (p·|g_i·u_i| + |q|·u_i²)。"""
    from mpmath import iv
    n = len(u)
    if form == "skewB":
        a = coeffs
        s1 = _iv_sum_raw([abs(a[j] * u[j]) for j in range(n)])
        s2 = _iv_sum_raw([u[j] * u[j] for j in range(n)])
        return float((s1 * s2).b)
    p = _iv_sum_raw([u[j] * u[j] for j in range(n)])
    q = _iv_sum_raw([coeffs[j] * u[j] for j in range(n)])
    m = _iv_sum_raw([p * abs(coeffs[i] * u[i]) + abs(q) * (u[i] * u[i]) for i in range(n)])
    return float(m.b)


def _ns1_tol(mag):
    return max(1e-45, 1e-38 * mag)


# ---------------------------------------------------------------- W-NS1

def _verify_ns1(w, cl):
    from mpmath import iv
    eng = w["interval_engine"]
    cl.add("engine_supported",
           eng.get("name") == "mpmath.iv" and eng.get("rounding") == "outward"
           and eng.get("precision") == f"dps={IV_DPS}",
           json.dumps(eng, ensure_ascii=False))
    if eng.get("name") != "mpmath.iv":
        return
    iv.dps = IV_DPS
    cl.add("claim_shape", w.get("claim") == "inner_B_u_u_contains_zero",
           str(w.get("claim")))
    cases = w["inputs"].get("cases") or []
    n_reg = int(w["inputs"].get("n_cases", -1))
    cl.add("inputs_n_cases", n_reg == len(cases) and n_reg >= 200,
           f"登记={n_reg} 实际={len(cases)}（须 ≥200）")
    all_zero, max_w, max_rel, mismatch = True, 0.0, 0.0, []
    per_form = {}
    for idx, c in enumerate(cases):
        form = c["form"]
        u = [_iv_from_str(s) for s in c["u"]]
        coeffs = [_iv_from_str(s) for s in (c["a"] if form == "skewB" else c["g"])]
        inner = _skewb_inner(coeffs, u) if form == "skewB" else _orthproj_inner(coeffs, u)
        lo, hi = float(inner.a), float(inner.b)
        width = hi - lo
        mag = _ns1_mag(form, coeffs, u)
        tol = _ns1_tol(mag)
        if not (lo <= 0.0 <= hi):
            all_zero = False
            mismatch.append(c.get("tag", idx))
        if width > tol:
            all_zero = False
            mismatch.append(f"width:{c.get('tag', idx)}")
        max_w = max(max_w, width)
        max_rel = max(max_rel, width / max(1.0, mag))
        if repr(lo) != c["inner_lo"] or repr(hi) != c["inner_hi"]:
            mismatch.append(f"endpoints:{c.get('tag', idx)}")
        per_form[form] = per_form.get(form, 0) + 1
    cl.add("recompute_all_contain_zero", all_zero and not mismatch,
           f"失配={mismatch[:5]}" if mismatch else f"{len(cases)} 例全部 ∋0 且宽度≤容差且端点逐字符串一致")
    v = w["verdict"]
    cl.add("verdict_all_zero_true", v.get("all_contain_zero") is True, str(v.get("all_contain_zero")))
    cl.add("metric_n_cases", v["metrics"].get("n_cases") == len(cases), str(v["metrics"].get("n_cases")))
    cl.add("metric_max_width", repr(max_w) == v["metrics"].get("max_width"),
           f"复算={repr(max_w)} 登记={v['metrics'].get('max_width')}")
    cl.add("metric_max_rel_width", repr(max_rel) == v["metrics"].get("max_rel_width"),
           f"复算={repr(max_rel)} 登记={v['metrics'].get('max_rel_width')}")
    cl.add("metric_per_form", v["metrics"].get("per_form") == per_form,
           f"复算={per_form} 登记={v['metrics'].get('per_form')}")
    cl.add("width_machine_scale", max_rel <= 1e-40,
           f"max_rel_width={repr(max_rel)} ≤ 1e-40（dps={IV_DPS} 机器精度级）")
    # 负控：plus-形式 B_plus(u,v)=(u·v)g+(v·g)u → inner=2·p·q 必须不含 0
    neg = w["negative_control"]
    p = neg.get("perturbation", {})
    cl.add("neg_perturbation_spec", p.get("kind") == "sign_flip" and p.get("form") == "orthProjB-plus",
           json.dumps(p, ensure_ascii=False))
    ref = next((c for c in cases if c.get("tag") == p.get("case_tag")), None)
    if ref is None:
        cl.add("neg_case_found", False, f"负控引用案例缺失: {p.get('case_tag')}")
        return
    g = [_iv_from_str(s) for s in ref["g"]]
    u = [_iv_from_str(s) for s in ref["u"]]
    pp = _iv_sum_raw([u[j] * u[j] for j in range(len(u))])
    qq = _iv_sum_raw([g[j] * u[j] for j in range(len(u))])
    neg_inner = pp * qq + qq * pp  # 2·p·q
    nlo, nhi = float(neg_inner.a), float(neg_inner.b)
    rejected = not (nlo <= 0.0 <= nhi)
    cl.add("neg_recompute_rejected", rejected,
           f"plus-形式 inner=[{nlo!r},{nhi!r}] 不含 0（必须拒证，fail-closed）")
    cl.add("neg_registered_true", neg["neg_verdict"].get("neg_rejected") is True,
           str(neg["neg_verdict"].get("neg_rejected")))
    cl.add("neg_metric_endpoints",
           repr(nlo) == neg["neg_verdict"].get("neg_inner_lo")
           and repr(nhi) == neg["neg_verdict"].get("neg_inner_hi"),
           f"复算=({nlo!r},{nhi!r}) 登记=({neg['neg_verdict'].get('neg_inner_lo')},"
           f"{neg['neg_verdict'].get('neg_inner_hi')})")
    cl.add("neg_same_lineage", bool(neg.get("same_lineage", {}).get("same_script")),
           "负控与正例同脚本同环境声明")


# ---------------------------------------------------------------- W-NS2

def _ns2_rhs(kind, nu, aux):
    """候选向量场（不可信层）：x' = -ν·x + B(x,x) + f。
    skewB：B(a)(x,x)≡0（WS-41 concreteData，线性动力学）；orthProjB：B(x,x)=‖x‖²g−(x·g)x。"""
    import numpy as np

    def rhs(t, x):
        x = np.asarray(x, dtype=float)
        if kind == "orthProjB":
            g = aux
            Bxx = float(np.dot(x, x)) * g - float(np.dot(x, g)) * x
        else:
            Bxx = 0.0
        return -nu * x + Bxx + F_FORCING[0]
    return rhs


F_FORCING = [None]  # 每次积分前由调用方置入（避免闭包共享可变默认参）


def _ns2_integrate(kind, nu, aux, f, x0, t_grid, rtol, atol):
    from scipy.integrate import solve_ivp
    import numpy as np
    F_FORCING[0] = np.asarray(f, dtype=float)
    try:
        sol = solve_ivp(_ns2_rhs(kind, nu, np.asarray(aux, dtype=float)),
                        (float(t_grid[0]), float(t_grid[-1])), np.asarray(x0, dtype=float),
                        method="DOP853", rtol=rtol, atol=atol, t_eval=np.asarray(t_grid, dtype=float))
    finally:
        F_FORCING[0] = None
    if not sol.success:
        raise RuntimeError(f"solve_ivp 失败: {sol.message}")
    return sol


def _ns2_eta(bound_hi):
    import numpy as np
    m = bound_hi
    for _ in range(NS2_NEXTAFTER_STEPS):
        m = float(np.nextafter(m, np.inf))
    return max(NS2_ETA_REL * (1.0 + abs(bound_hi)), m - bound_hi)


def _verify_ns2(w, cl):
    from mpmath import iv
    eng = w["interval_engine"]
    cl.add("engine_supported",
           eng.get("name") == "mpmath.iv" and eng.get("rounding") == "outward"
           and eng.get("precision") == f"dps={IV_DPS}",
           json.dumps(eng, ensure_ascii=False))
    if eng.get("name") != "mpmath.iv":
        return
    iv.dps = IV_DPS
    cl.add("honesty_boundary_present", isinstance(w.get("honesty_boundary"), str)
           and "非轨道包络" in w["honesty_boundary"] and "solve_ivp" in w["honesty_boundary"],
           "W-NS2 必须携带「采样点证书·非轨道包络」诚实边界")
    cl.add("claim_shape", w.get("claim") == "sampled_energy_bound",
           str(w.get("claim")))
    cases = w["inputs"].get("cases") or []
    n_reg = int(w["inputs"].get("n_cases", -1))
    cl.add("inputs_n_cases", n_reg == len(cases) and n_reg >= 50,
           f"登记={n_reg} 实际={len(cases)}（须 ≥50）")
    rtol = float(w["inputs"]["integrator"]["rtol"])
    atol = float(w["inputs"]["integrator"]["atol"])
    cl.add("integrator_spec", w["inputs"]["integrator"].get("method") == "DOP853"
           and w["inputs"]["integrator"].get("role") == "untrusted_candidate",
           json.dumps(w["inputs"]["integrator"], ensure_ascii=False))

    import numpy as np
    all_within, max_defect, dev_worst, mismatch = True, -np.inf, 0.0, []
    total_samples = 0
    per_kind = {}
    for c in cases:
        kind = c["kind"]
        nu = float(Fraction(c["nu"]))
        f = [float(Fraction(s)) for s in c["f"]]
        x0 = [float(Fraction(s)) for s in c["x0"]]
        aux = [float(Fraction(s)) for s in (c["g"] if kind == "orthProjB" else c["a"])]
        t_grid = [float(Fraction(s)) for s in c["t"]]
        samples = [[float(Fraction(s)) for s in row] for row in c["x"]]
        # 不可信候选一致性闸：独立重积分与登记采样点偏差 ≤ NS2_DEV_TOL
        sol = _ns2_integrate(kind, nu, aux, f, x0, t_grid, rtol, atol)
        dev = float(max(abs(float(sol.y[j, i]) - samples[i][j])
                        for i in range(len(t_grid)) for j in range(len(x0))))
        dev_worst = max(dev_worst, dev)
        if dev > NS2_DEV_TOL:
            mismatch.append(f"candidate_dev:{c.get('tag')}")
        # 区间界：bound = max(‖x0‖², ‖f‖²/ν²)，全部有理输入
        nu_iv = _iv_from_str(c["nu"])
        x02 = _iv_sum_raw([_iv_from_str(s) ** 2 for s in c["x0"]])
        f2 = _iv_sum_raw([_iv_from_str(s) ** 2 for s in c["f"]])
        fnu2 = f2 / (nu_iv * nu_iv)
        b_hi = max(float(x02.b), float(fnu2.b))  # bound = max(‖x0‖², ‖f‖²/ν²) 的区间上端
        eta = _ns2_eta(b_hi)
        case_max_defect = -np.inf
        for row in samples:
            n_iv = _iv_sum_raw([_iv_from_str(s) ** 2 for s in row])
            d = float(n_iv.b) - b_hi
            case_max_defect = max(case_max_defect, d)
            if float(n_iv.b) > b_hi + eta:
                all_within = False
                mismatch.append(f"bound:{c.get('tag')}")
        max_defect = max(max_defect, case_max_defect)
        if repr(b_hi) != c["bound_hi"] or repr(case_max_defect) != c["max_defect"]:
            mismatch.append(f"metrics:{c.get('tag')}")
        total_samples += len(samples)
        per_kind[kind] = per_kind.get(kind, 0) + 1
    cl.add("candidate_consistency", not any(m.startswith("candidate_dev") for m in mismatch),
           f"最大候选偏差={dev_worst!r} ≤ {NS2_DEV_TOL}")
    cl.add("recompute_all_within_bound", all_within
           and not any(m.startswith(("bound", "metrics")) for m in mismatch),
           f"失配={mismatch[:5]}" if mismatch else "全部采样点区间满足 ‖x‖² ≤ bound+η 且度量逐字符串一致")
    v = w["verdict"]
    cl.add("verdict_within_true", v.get("all_within_bound") is True, str(v.get("all_within_bound")))
    cl.add("metric_n_samples", v["metrics"].get("n_samples_total") == total_samples,
           f"复算={total_samples} 登记={v['metrics'].get('n_samples_total')}")
    cl.add("metric_max_defect", repr(max_defect) == v["metrics"].get("max_defect"),
           f"复算={repr(max_defect)} 登记={v['metrics'].get('max_defect')}")
    cl.add("metric_per_kind", v["metrics"].get("per_kind") == per_kind,
           f"复算={per_kind} 登记={v['metrics'].get('per_kind')}")
    cl.add("eta_rule", w["bounds"].get("eta_rule") ==
           f"eta = max({NS2_ETA_REL}*(1+|bound_hi|), {NS2_NEXTAFTER_STEPS}×nextafter ulp)",
           str(w["bounds"].get("eta_rule")))
    # 负控：最大范数采样点放大 factor → 必须越界（拒证复算确认）
    neg = w["negative_control"]
    p = neg.get("perturbation", {})
    cl.add("neg_perturbation_spec", p.get("kind") == "scale_sample" and "case_tag" in p,
           json.dumps(p, ensure_ascii=False))
    ref = next((c for c in cases if c.get("tag") == p.get("case_tag")), None)
    if ref is None:
        cl.add("neg_case_found", False, f"负控引用案例缺失: {p.get('case_tag')}")
        return
    nu_iv = _iv_from_str(ref["nu"])
    x02 = _iv_sum_raw([_iv_from_str(s) ** 2 for s in ref["x0"]])
    f2 = _iv_sum_raw([_iv_from_str(s) ** 2 for s in ref["f"]])
    fnu2 = f2 / (nu_iv * nu_iv)
    b_hi = max(float(x02.b), float(fnu2.b))
    eta = _ns2_eta(b_hi)
    fac = _iv_from_str(p["factor"])
    row = ref["x"][int(p["sample_index"])]
    neg_n = _iv_sum_raw([(fac * _iv_from_str(s)) ** 2 for s in row])
    neg_hi = float(neg_n.b)
    cl.add("neg_recompute_rejected", neg_hi > b_hi + eta,
           f"扰动后 norm²_hi={neg_hi!r} > bound_hi+eta={b_hi + eta!r}（必须越界，fail-closed）")
    cl.add("neg_registered_true", neg["neg_verdict"].get("neg_rejected") is True,
           str(neg["neg_verdict"].get("neg_rejected")))
    cl.add("neg_metric_norm", repr(neg_hi) == neg["neg_verdict"].get("neg_norm_sq_hi"),
           f"复算={neg_hi!r} 登记={neg['neg_verdict'].get('neg_norm_sq_hi')}")
    cl.add("neg_same_lineage", bool(neg.get("same_lineage", {}).get("same_script")),
           "负控与正例同脚本同环境声明")


# ---------------------------------------------------------------- W-NS3

def _verify_ns3(w, cl):
    eng = w["interval_engine"]
    cl.add("engine_none", eng.get("name") == "none",
           "阻塞登记不携带任何区间认证引擎产出")
    cl.add("claim_shape", w.get("claim") == "blocked_registration", str(w.get("claim")))
    v = w["verdict"]
    cl.add("verdict_blocked_true", v.get("blocked") is True, str(v.get("blocked")))
    cl.add("verdict_not_certified", v.get("certified") is False,
           "阻塞登记严禁宣称任何认证通过")
    blk = w.get("blocked") or {}
    cl.add("blocked_code_B1", blk.get("code") == "B1" and v.get("code") == "B1",
           f"code={blk.get('code')}")
    stmt = blk.get("statement", "")
    cl.add("blocked_statement", isinstance(stmt, str) and len(stmt) >= 80
           and "RadiiPolynomial" in stmt and "阻塞" in stmt,
           f"statement 长度={len(stmt)}")
    cl.add("blocked_requirements", isinstance(blk.get("requirements"), list)
           and len(blk["requirements"]) >= 2,
           f"requirements={len(blk.get('requirements') or [])} 项")
    cl.add("no_envelope_claimed", (w["bounds"].get("envelope") is None),
           "bounds.envelope 必须为 null（未产出任何包络数值）")
    cl.add("neg_not_applicable", w["negative_control"].get("kind") == "not_applicable",
           "阻塞登记无负控语义")
    cl.add("disclosure_present", isinstance(w.get("notes"), str)
           and "非" in w["notes"] and "阻塞" in w["notes"], "披露口径")


# ---------------------------------------------------------------- driver

def verify_witness(path):
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
        if fam == "ns-energy-cancellation":
            _verify_ns1(w, cl)
        elif fam == "ns-galerkin-energy-bound":
            _verify_ns2(w, cl)
        elif fam == "ns-trajectory-envelope-blocked":
            _verify_ns3(w, cl)
        else:
            cl.add("family_known", False, f"未知族: {fam!r}")
    except Exception as e:
        cl.add("exception", False, f"{type(e).__name__}: {e}")
    return {"witness": path, "witness_id": w.get("witness_id"), "ok": cl.ok, "checks": cl.checks}


def main(argv=None):
    ap = argparse.ArgumentParser(description="WS-43 NS 见证独立核验器（fail-closed）")
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
