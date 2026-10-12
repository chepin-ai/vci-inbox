# CLASSIFY: L1
# krawczyk_ns_gen.py · EXT-WAVE-10「融」波 WS-55「Krawczyk×Galerkin」融构件
# 证书生成器（不可信侧，schema v1.0）
#
# 对象：WS-42 Lean 核的显式三模态截断 B₃（ModeSpace 1 = EuclideanSpace ℝ (Fin 3)，
#   B3fun u v = ![u₁v₂+u₂v₁, -(u₀v₂+u₂v₀), 0]）稳态问题
#     F(u) = B₃(u)u − ν·A·u + f = 0，A = diag(a₀,a₁,a₂)（aᵢ>0），f 常外力。
#   符号约定与 ws42-report / NsGalerkin.Basic.vf（vf x = -(ν•A x) + B x x + f）
#   逐字一致；稳态即 vf = 0。逐分量：
#     F₀ = 2u₁u₂ − νa₀u₀ + f₀
#     F₁ = −2u₀u₂ − νa₁u₁ + f₁
#     F₂ = −νa₂u₂ + f₂
#   Fréchet 导数（B₃ 双线性，DF(u)h = B₃(u)h + B₃(h)u − νAh）：
#     DF(u) = [[−νa₀, 2u₂, 2u₁], [−2u₂, −νa₁, −2u₀], [0, 0, −νa₂]]
#
# 证书定理（Newton–Krawczyk；ws51-report §4.1）：
#   盒 U = z + [−r,r]³，Y ≈ DF(z)⁻¹（常矩阵，证书数据），
#   K(U) = z − Y·F(z) + (I₃ − Y·□DF(U))·(U − z)（全程区间运算）：
#     · K(U) ⊂ int(U)（逐分量严格）⟹ ∃ u* ∈ int(U)，F(u*) = 0   （存在）
#     · ρ = ‖I₃ − Y·□DF(U)‖∞ < 1（行和 sup 范数区间上界）⟹ u* 在 U 内唯一
#       （压缩映射路线，绕 Brouwer）。
#
# 生成器职责（全部不可信，仅产候选与证书数据）：
#   · float64 Newton 迭代产候选 z（策略见 CANDIDATE_NOTE：只用 float64，不升格高精度）；
#   · 数值逆 Y = DF(z)⁻¹（float64），以 repr 十进制字符串登记（= 精确有理数）；
#   · 半径扫描：r 自 r₀ = max(8·‖Y·F(z)‖∞_hi, R_FLOOR) 起按 ×√2 几何递增，
#     取满足「min_margin ≥ 0.3·r 且 ρ_hi ≤ 0.25」的最大 r（≤ R_CAP）；
#     扫描耗尽则本组登记 FAIL（诚实失败登记，不强行升格高精度候选——熔断判据 ws52 §3）；
#   · 全部判定量由本文件自含的 mpmath.iv（dps=50，外向舍入）区间核复算后登记，
#     与 ci/krawczyk_ns_verify.py 零共享代码（同一规范、独立实现，见 VERIFY_SPEC）。
#
# 区间计算规范 VERIFY_SPEC（验证器独立实现同一规范，端点逐比特一致方接受）：
#   · 十进制字符串 s → Fraction(s) → iv.mpf(分子)/iv.mpf(分母)（dps=50 外向舍入）；
#   · 区间求和按下标升序从左到右，初值 iv.mpf(0)；
#   · 盒 U_i = z_i + iv.mpf([-1,1])·r；U − z 直接取 iv.mpf([-1,1])·r（不经 U_i − z_i）；
#   · □DF(U) 按上式逐元素区间求值（对 u 仿射，直接区间代换即精确包围）；
#   · R = I₃ − Y·□DF(U)（3×3 区间矩阵乘，内积按下标升序）；
#   · K_i = z_i − (Y·F(z))_i + (R·(U−z))_i；
#   · ρ 行和：rowsum_i = Σ_j max(|R_ij.a|, |R_ij.b|)（区间加和），ρ_hi = max_i rowsum_i.b；
#   · margin_i = min((K_i.a − U_i.a), (U_i.b − K_i.b))（点区间差取下端 .a）；
#   · 存在性判定：∀i, K_i.a > U_i.a 且 K_i.b < U_i.b；唯一性判定：ρ_hi < 1。
#
# 证书 schema（v1.0，成文于此与验证器文首）：
#   schema_version / family="ns-krawczyk-stationary" / claim="exists_unique_zero_in_box"
#   / case_id / run_id / ts_utc / params{nu,a[3],f[3]}（十进制字符串=精确有理）
#   / candidate{z[3]} / preconditioner{Y[3][3]} / box{center,radius}
#   / krawczyk{F_z:[[lo,hi]×3], y0_hi, K:[[lo,hi]×3], margins[3], min_margin, rho_hi,
#              radius_schedule{r0,r_cap,factor,n_steps,chosen_index}}
#   / verdict{existence,uniqueness,status∈{PASS,FAIL}}
#   / fail_registration（仅 FAIL 组：reason + diagnostics{eps_hi, last_rho_hi, last_min_margin}）
#   / generator{script,sha256} / verifier{script,sha256} / cert_sha256（规范化序列化，
#     规则：json.dumps(除 cert_sha256, sort_keys=True, separators=(",", ":"),
#     ensure_ascii=False) 的 sha256）。
#
# 用法：python3 ci/krawczyk_ns_gen.py [--out artifacts/witnesses-cap]
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
GEN_REL = "ci/krawczyk_ns_gen.py"
VER_REL = "ci/krawczyk_ns_verify.py"
RUNLOG_REL = "artifacts/witnesses-cap/run-log.json"

SCHEMA_VERSION = "1.0"
GENERATOR_LINE = "PIVOT-01 计算线"
IV_DPS = 50

# 半径扫描策略（生成器内部阈值；证书判定仍以「严格包含 + ρ<1」为准）
R_FLOOR = 1e-9          # 半径下限（避免 ε≈0 时退化盒）
R_CAP = 0.25            # 半径上限
R_FACTOR = 2.0 ** 0.5   # 几何步长 √2
R_STEPS = 80            # 最大步数
PASS_MARGIN_FRAC = 0.3  # 内部通过阈值：min_margin ≥ 0.3·r
PASS_RHO_HI = 0.25      # 内部通过阈值：ρ_hi ≤ 0.25

CANDIDATE_NOTE = (
    "候选 z 与 Y 均由 float64（Newton 迭代 ≤64 步 + numpy 数值逆）产出，不升格高精度："
    "若 float64 候选质量不足以在给定半径调度内闭合 Krawczyk 两条件，本组如实登记 FAIL"
    "（ws52 §3 熔断判据：区间见证无法闭合→降级登记，不强行升格）。证书可靠性不依赖"
    "候选质量——两条件由验证器对登记数据的独立区间复算承载。"
)

# ---------------------------------------------------------------- 参数组
# ≥3 组（含小 ν 刚性较强组）；P4 为预期的诚实失败组（f₂=0 使 det DF = −ν³a₀a₁a₂，
# ν=1e-6 时 ‖Y‖~1e18，float64 候选残差经 Y 放大后无法在调度内闭合）。
CASES = [
    {"case_id": "cap-b3-p1-mild",
     "params": {"nu": "1", "a": ["1", "1", "1"], "f": ["1", "0.5", "-0.25"]},
     "note": "温和组：ν=1、A=I；解析稳态 u*=(3/5, 4/5, -1/4)（精确有理）"},
    {"case_id": "cap-b3-p2-medium",
     "params": {"nu": "0.05", "a": ["1", "2", "3"], "f": ["1", "-1", "0.5"]},
     "note": "中等组：ν=5e-2、非对称 A"},
    {"case_id": "cap-b3-p3-stiff",
     "params": {"nu": "0.0001", "a": ["1", "1.5", "2"], "f": ["0.5", "0.25", "-0.1"]},
     "note": "刚性组：ν=1e-4，u₂=f₂/(νa₂)=-500 大模态"},
    {"case_id": "cap-b3-p4-hardfail",
     "params": {"nu": "0.000000001", "a": ["1", "1", "1"], "f": ["0.5", "0.25", "0"]},
     "note": "诚实失败组：f₂=0 ⇒ u₂=0、DF 上三角化（ρ 斜率 ~6/ν=6e9），"
             "存在性需 r>ε 而唯一性需 r<ν/6≈1.7e-10，窗口不交 ⇒ 全半径调度失败，"
             "如实登记 FAIL（不升格高精度候选）"},
]


class GenError(RuntimeError):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(obj):
    if "cert_sha256" in obj:
        raise GenError("canonical_sha256 输入不得含 cert_sha256")
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def env_fp():
    import mpmath
    import numpy
    pkgs = {"python": platform.python_version(), "numpy": numpy.__version__,
            "mpmath": mpmath.__version__}
    manifest = "\n".join(f"{k}=={v}" for k, v in sorted(pkgs.items())) + "\n"
    return {
        "runner": "PIVOT-01 WS-55 krawczyk_ns_gen.py",
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


def _f_iv(u, nu, a, f):
    """F(u) = B₃(u)u − νAu + f 的区间求值（规范件）。"""
    u0, u1, u2 = u
    return [_lsum([u1 * u2, u2 * u1, -(nu * a[0]) * u0, f[0]]),
            _lsum([-(u0 * u2), -(u2 * u0), -(nu * a[1]) * u1, f[1]]),
            _lsum([-(nu * a[2]) * u2, f[2]])]


def _df_iv(U, nu, a):
    """□DF(U) 的区间求值（规范件；对 u 仿射，直接区间代换）。"""
    from mpmath import iv
    U0, U1, U2 = U
    z0 = iv.mpf(0)
    return [[-nu * a[0], 2 * U2, 2 * U1],
            [-2 * U2, -nu * a[1], -2 * U0],
            [z0, z0, -nu * a[2]]]


def _matmul(A, B):
    return [[_lsum([A[i][t] * B[t][j] for t in range(3)]) for j in range(3)]
            for i in range(3)]


def _matvec(A, v):
    return [_lsum([A[i][t] * v[t] for t in range(3)]) for i in range(3)]


def _krawczyk(z, Y, r, nu, a, f):
    """规范区间核：返回 (U, K, margins, rho_hi, F_z, y0_hi)，全部按 VERIFY_SPEC。"""
    from mpmath import iv
    span = iv.mpf([-1, 1]) * r
    U = [z[i] + span for i in range(3)]
    Umz = [span, span, span]
    DFU = _df_iv(U, nu, a)
    YD = _matmul(Y, DFU)
    R = [[(iv.mpf(1) if i == j else iv.mpf(0)) - YD[i][j] for j in range(3)]
         for i in range(3)]
    F_z = _f_iv(z, nu, a, f)
    YF = _matvec(Y, F_z)
    RU = _matvec(R, Umz)
    K = [_lsum([z[i], -YF[i], RU[i]]) for i in range(3)]
    margins = []
    for i in range(3):
        m1 = iv.mpf(K[i].a) - iv.mpf(U[i].a)
        m2 = iv.mpf(U[i].b) - iv.mpf(K[i].b)
        margins.append(m1 if float(m1.a) <= float(m2.a) else m2)
    rowsums = [_lsum([iv.mpf(sorted([float(abs(R[i][j].a)), float(abs(R[i][j].b))]))
                      for j in range(3)]) for i in range(3)]
    rho_hi = max(float(rs.b) for rs in rowsums)
    y0_hi = max(float(abs(YF[i].a)) if float(abs(YF[i].a)) >= float(abs(YF[i].b))
                else float(abs(YF[i].b)) for i in range(3))
    return U, K, margins, rho_hi, F_z, y0_hi


def _exists_ok(U, K):
    return all(float(K[i].a) > float(U[i].a) and float(K[i].b) < float(U[i].b)
               for i in range(3))


def _newton_candidate(nu_s, a_s, f_s):
    """float64 Newton（不可信候选）。返回 (z floats, residual_sup)。"""
    import numpy as np
    nu = float(Fraction(nu_s))
    a = [float(Fraction(s)) for s in a_s]
    f = [float(Fraction(s)) for s in f_s]

    def Fv(u):
        return np.array([2 * u[1] * u[2] - nu * a[0] * u[0] + f[0],
                         -2 * u[0] * u[2] - nu * a[1] * u[1] + f[1],
                         -nu * a[2] * u[2] + f[2]])

    def DFv(u):
        return np.array([[-nu * a[0], 2 * u[2], 2 * u[1]],
                         [-2 * u[2], -nu * a[1], -2 * u[0]],
                         [0.0, 0.0, -nu * a[2]]])

    u = np.zeros(3)
    for _ in range(64):
        try:
            du = np.linalg.solve(DFv(u), -Fv(u))
        except np.linalg.LinAlgError as e:
            raise GenError(f"Newton 奇异: {e}")
        u = u + du
        if float(np.max(np.abs(du))) < 1e-15:
            break
    if not np.all(np.isfinite(u)):
        raise GenError("Newton 发散（候选非有限）")
    return u, float(np.max(np.abs(Fv(u))))


def _numeric_inverse(nu_s, a_s, z):
    import numpy as np
    nu = float(Fraction(nu_s))
    a = [float(Fraction(s)) for s in a_s]
    DFz = np.array([[-nu * a[0], 2 * z[2], 2 * z[1]],
                    [-2 * z[2], -nu * a[1], -2 * z[0]],
                    [0.0, 0.0, -nu * a[2]]])
    return np.linalg.inv(DFz)


def _eval_case(case):
    """单组参数：候选 → Y → 半径扫描 → 区间复算登记。返回证书负载（决定论）。"""
    from mpmath import iv
    iv.dps = IV_DPS
    p = case["params"]
    nu_s, a_s, f_s = p["nu"], p["a"], p["f"]
    z_np, res_sup = _newton_candidate(nu_s, a_s, f_s)
    z_s = [repr(float(v)) for v in z_np]
    Y_np = _numeric_inverse(nu_s, a_s, z_np)
    Y_s = [[repr(float(v)) for v in row] for row in Y_np]

    nu = _iv_of(nu_s)
    a = [_iv_of(s) for s in a_s]
    f = [_iv_of(s) for s in f_s]
    z = [_iv_of(s) for s in z_s]
    Y = [[_iv_of(s) for s in row] for row in Y_s]

    # ε = ‖Y·F(z)‖∞ 上界（区间）
    _, _, _, _, _, eps_hi = _krawczyk(z, Y, _iv_of("0"), nu, a, f)
    r0 = max(8.0 * eps_hi, R_FLOOR)

    chosen = None  # (idx, r, U, K, margins, rho_hi, F_z, y0_hi)
    last = None
    idx = 0
    r = r0
    while idx < R_STEPS and r <= R_CAP:
        U, K, margins, rho_hi, F_z, y0_hi = _krawczyk(z, Y, _iv_of(repr(r)), nu, a, f)
        min_margin = min(float(m.a) for m in margins)
        exists = _exists_ok(U, K)
        uniq = rho_hi < 1.0
        last = {"r": repr(r), "rho_hi": repr(rho_hi), "min_margin": repr(min_margin),
                "exists": exists, "uniq": uniq}
        if exists and uniq and min_margin >= PASS_MARGIN_FRAC * r and rho_hi <= PASS_RHO_HI:
            chosen = (idx, r, U, K, margins, rho_hi, F_z, y0_hi)
        idx += 1
        r *= R_FACTOR
    n_steps = idx

    base = {
        "case_id": case["case_id"],
        "params": {"nu": nu_s, "a": list(a_s), "f": list(f_s)},
        "candidate": {"z": z_s, "float64_residual_sup": repr(res_sup),
                      "policy": CANDIDATE_NOTE},
        "preconditioner": {"Y": Y_s},
        "radius_schedule": {"r0": repr(r0), "r_cap": repr(R_CAP),
                            "factor": repr(R_FACTOR), "n_steps": n_steps},
        "note": case["note"],
    }
    if chosen is not None:
        cidx, r, U, K, margins, rho_hi, F_z, y0_hi = chosen
        base["radius_schedule"]["chosen_index"] = cidx
        base["box"] = {"center": z_s, "radius": repr(r)}
        base["krawczyk"] = {
            "F_z": [[repr(float(v.a)), repr(float(v.b))] for v in F_z],
            "y0_hi": repr(y0_hi),
            "K": [[repr(float(v.a)), repr(float(v.b))] for v in K],
            "U": [[repr(float(v.a)), repr(float(v.b))] for v in U],
            "margins": [repr(float(m.a)) for m in margins],
            "min_margin": repr(min(float(m.a) for m in margins)),
            "rho_hi": repr(rho_hi),
        }
        base["verdict"] = {"existence": True, "uniqueness": True, "status": "PASS"}
    else:
        base["box"] = None
        base["krawczyk"] = None
        base["verdict"] = {"existence": False, "uniqueness": False, "status": "FAIL"}
        base["fail_registration"] = {
            "reason": "半径调度耗尽：float64 候选下无半径同时满足内部阈值"
                      f"（min_margin ≥ {PASS_MARGIN_FRAC}·r 且 ρ_hi ≤ {PASS_RHO_HI}）",
            "diagnostics": {"eps_hi": repr(eps_hi), "last_attempt": last},
            "fuse_policy": "ws52 §3 熔断判据：区间见证无法闭合 → 如实降级登记 FAIL，"
                           "不升格高精度候选、不粉饰",
        }
    return base


def compute_payload():
    """决定论负载：全部参数组的证书数据（不含时间戳/run_id/哈希）。门禁比较对象。"""
    return {"cases": [_eval_case(c) for c in CASES]}


def _canonical_blob(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def consistency_gate(payload):
    """sandbox 一致性门禁：独立子进程重算决定论负载，规范化 JSON 逐字节一致方放行。"""
    tmp = tempfile.mkdtemp(prefix="ws55-gate-")
    try:
        out = os.path.join(tmp, "raw.json")
        proc = subprocess.run([sys.executable, os.path.abspath(__file__), "--emit-raw", out],
                              capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            raise GenError(f"门禁子进程失败 rc={proc.returncode}\n{proc.stderr[-2000:]}")
        with open(out, "rb") as fh:
            if fh.read() != _canonical_blob(payload):
                raise GenError("双跑决定论负载不一致，拒绝签发证书")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- 证书组装

def build_cert(case_payload, run_meta):
    cert = {
        "schema_version": SCHEMA_VERSION,
        "family": "ns-krawczyk-stationary",
        "claim": "exists_unique_zero_in_box",
        "case_id": case_payload["case_id"],
        "run_id": run_meta["run_id"],
        "ts_utc": run_meta["ts"],
        "system": {
            "equation": "F(u) = B3(u)u − ν·diag(a)·u + f = 0（稳态；vf 符号约定同 WS-42 Lean 核）",
            "components": ["F0 = 2*u1*u2 − nu*a0*u0 + f0",
                           "F1 = −2*u0*u2 − nu*a1*u1 + f1",
                           "F2 = −nu*a2*u2 + f2"],
            "jacobian": "DF(u) = [[−νa0, 2u2, 2u1], [−2u2, −νa1, −2u0], [0, 0, −νa2]]",
            "b3_source": "library/ns/NsGalerkin/ExplicitB.lean (B3fun/B3, WS-42, commit 5887bbb4)",
        },
        "params": case_payload["params"],
        "candidate": case_payload["candidate"],
        "preconditioner": case_payload["preconditioner"],
        "box": case_payload["box"],
        "radius_schedule": case_payload["radius_schedule"],
        "krawczyk": case_payload["krawczyk"],
        "interval_engine": {"name": "mpmath.iv", "precision": f"dps={IV_DPS}",
                            "rounding": "outward"},
        "verdict": case_payload["verdict"],
        "note": case_payload["note"],
        "generator": {"script": GEN_REL, "sha256": run_meta["script_sha"]},
        "verifier": {"script": VER_REL, "sha256": run_meta["verifier_sha"]},
        "provenance": {"generator_line": GENERATOR_LINE,
                       "source_anchors": ["/mnt/agents/output/ws42-report.md",
                                          "/mnt/agents/output/ws51-report.md §4",
                                          GEN_REL, RUNLOG_REL]},
    }
    if case_payload["verdict"]["status"] == "FAIL":
        cert["fail_registration"] = case_payload["fail_registration"]
    cert["cert_sha256"] = canonical_sha256(cert)
    return cert


def build_manifest(certs, run_meta):
    n_pass = sum(1 for c in certs if c["verdict"]["status"] == "PASS")
    return {
        "schema": "witnesses-cap-manifest/1.0",
        "run_id": run_meta["run_id"],
        "ts": run_meta["ts"],
        "generator": {"script": GEN_REL, "sha256": run_meta["script_sha"]},
        "verifier": {"script": VER_REL, "sha256": run_meta["verifier_sha"]},
        "certificates": [{"case_id": c["case_id"],
                          "file": c["case_id"] + ".cap.json",
                          "sha256": c["cert_sha256"],
                          "status": c["verdict"]["status"]} for c in certs],
        "counts": {"cases": len(certs), "pass": n_pass, "fail": len(certs) - n_pass},
        "consistency_gate": "双跑决定论一致性（主流程 vs --emit-raw 独立子进程，规范化 JSON 逐字节一致方签发）",
        "env_fp": run_meta["env_fp"],
        "notes": "PASS 组=区间 Krawczyk 存在+唯一证书（外证层真实数学证，待验证器独立复算确认）；"
                 "FAIL 组=诚实失败登记（熔断判据 ws52 §3，未升格高精度候选）",
    }


def main():
    ap = argparse.ArgumentParser(description="WS-55 Krawczyk×Galerkin 证书生成器（schema v1.0）")
    ap.add_argument("--out", default=os.path.join(REPO_ROOT, "artifacts", "witnesses-cap"))
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
        "run_id": f"ws55-cap-{now.strftime('%Y%m%dT%H%M%SZ')}",
        "env_fp": env_fp(),
        "script_sha": sha256_file(os.path.join(REPO_ROOT, GEN_REL)),
        "verifier_sha": sha256_file(os.path.join(REPO_ROOT, VER_REL)),
    }

    out_dir = args.out
    tmp_out = tempfile.mkdtemp(prefix="ws55-cap-", dir=os.path.dirname(out_dir) or ".")
    try:
        runlog = {
            "run_id": run_meta["run_id"], "ts": run_meta["ts"],
            "payload_sha256": hashlib.sha256(_canonical_blob(payload)).hexdigest(),
            "counts": {"cases": len(payload["cases"]),
                       "pass": sum(1 for c in payload["cases"]
                                   if c["verdict"]["status"] == "PASS")},
            "consistency_gate": "passed（双跑逐字节一致）",
            "env_fp": run_meta["env_fp"],
        }
        runlog_path = os.path.join(tmp_out, "run-log.json")
        with open(runlog_path, "w", encoding="utf-8") as fh:
            json.dump(runlog, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        certs = [build_cert(c, run_meta) for c in payload["cases"]]
        for c in certs:
            with open(os.path.join(tmp_out, c["case_id"] + ".cap.json"), "w",
                      encoding="utf-8") as fh:
                json.dump(c, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
        manifest = build_manifest(certs, run_meta)
        with open(os.path.join(tmp_out, "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        shutil.move(tmp_out, out_dir)
    except Exception:
        shutil.rmtree(tmp_out, ignore_errors=True)
        raise

    print(f"run_id={run_meta['run_id']} 生成证书 {len(certs)} 件 + manifest → {out_dir}")
    for c in certs:
        extra = ""
        if c["verdict"]["status"] == "PASS":
            extra = (f" r={c['box']['radius']} rho_hi={c['krawczyk']['rho_hi']}"
                     f" min_margin={c['krawczyk']['min_margin']}")
        print(f"  {c['case_id']}  {c['verdict']['status']}  sha256={c['cert_sha256'][:16]}…{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
