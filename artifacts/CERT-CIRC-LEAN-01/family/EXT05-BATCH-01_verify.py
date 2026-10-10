# CLASSIFY: L1
# EXT05-BATCH-01 · circulant Sinkhorn 族 Krawczyk 区间复验批（复现 CERT-CIRC-LEAN-01 方法学）
#
# 方法学（复原自 artifacts/CERT-CIRC-LEAN-01/README.md、family/README.md 与 6 件 Lean 证书）：
#   系统（n=2k-1 维，gauged：f0 pinned=0；变量序 f1..f_{k-1}, g0..g_{k-1}）：
#     Ff_i = f_i + eps*log(k) + eps*log( sum_j exp((g_j - c[(j-i)%k])/eps) ),  i=1..k-1
#     Fg_j = g_j + eps*log(k) + eps*log( sum_i exp((f_i - c[(j-i)%k])/eps) ),  j=0..k-1  (f0≡0)
#   闭形式：f*=0, g* = -eps*(log k + lse(-c/eps))（全 j 相同）。
#   证书：有理中心（|ĝ-g*|≤1e-13, limit_denominator(1e13)），盒半径 1e-9，
#         预条件子 C ≈ J(center)^{-1} 的有理化（limit_denominator(1e10)）。
#   判据（Krawczyk，mpmath.iv 外向舍入区间算术，mp.dps=80）：
#     K(X) = center - C·F(center) + (I - C·J(X))·(X - center)  严格内包于 X（inside=True）
#     ⇒ 盒内存在唯一实根。
#   负面控制：g 中心偏移 +1e-6（重算预条件子）→ 内包必须失败（拒证）。
#
# 用法：python3 EXT05-BATCH-01_verify.py  →  stdout 打印汇总，并写 EXT05-BATCH-01-results.json
import json
from fractions import Fraction
import numpy as np
import mpmath
from mpmath import mp, mpf, iv, mpi, log, exp

mp.dps = 80
iv.dps = 80

FAMILIES = {
    "k6": [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5)],
    "k10": [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4),
            Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(1, 6)],
}

BOX_R = Fraction(1, 10**9)          # 盒半径 1e-9
CENTER_TOL_DEN = 10**13             # 有理中心精度 ~1e-13
PRECOND_DEN = 10**10                # 预条件子有理化分母界
NEG_SHIFT = Fraction(1, 10**6)      # 负面控制偏移 1e-6


def closed_form_gstar(k, c, eps):
    """g* = -eps*(log k + lse(-c/eps))，mpf 高精度。"""
    e = mpf(eps.numerator) / eps.denominator
    lse = log(sum(exp(-mpf(ci.numerator) / ci.denominator / e) for ci in c))
    return -e * (log(k) + lse)


def rational_center(gstar):
    return Fraction(mp.nstr(gstar, 40)).limit_denominator(CENTER_TOL_DEN)


def feval(k, c, eps, x):
    """F 在点 x（Fraction 列表，长度 2k-1）处取值，返回 iv 列表。"""
    e = iv.mpf(eps.numerator) / eps.denominator
    f = [iv.mpf(0)] + [iv.mpf(t.numerator) / t.denominator for t in x[:k - 1]]
    g = [iv.mpf(t.numerator) / t.denominator for t in x[k - 1:]]
    logk = iv.log(k)
    out = []
    for i in range(1, k):
        s = sum(iv.exp((g[j] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
                for j in range(k))
        out.append(f[i] + e * logk + e * iv.log(s))
    for j in range(k):
        s = sum(iv.exp((f[i] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
                for i in range(k))
        out.append(g[j] + e * logk + e * iv.log(s))
    return out


def jac_interval(k, c, eps, box):
    """区间 Jacobian：J = [[I, P],[Q, I]]，P/Q 为行随机比。box 为 iv 列表。"""
    n = 2 * k - 1
    e = iv.mpf(eps.numerator) / eps.denominator
    f = [iv.mpf(0)] + box[:k - 1]
    g = box[k - 1:]
    S = [sum(iv.exp((g[j] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
             for j in range(k)) for i in range(1, k)]
    T = [sum(iv.exp((f[i] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
             for i in range(k)) for j in range(k)]
    J = [[iv.mpf(0)] * n for _ in range(n)]
    for r in range(k - 1):            # Ff 行，i=r+1
        i = r + 1
        J[r][r] = iv.mpf(1)
        for j in range(k):
            J[r][k - 1 + j] = iv.exp((g[j] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e) / S[r]
    for j in range(k):                # Fg 行
        row = k - 1 + j
        J[row][row] = iv.mpf(1)
        for i in range(1, k):
            J[row][i - 1] = iv.exp((f[i] - iv.mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e) / T[j]
    return J


def jac_point_mp(k, c, eps, x):
    """中心处高精度（mp）Jacobian，用于求逆得预条件子。"""
    n = 2 * k - 1
    e = mpf(eps.numerator) / eps.denominator
    f = [mpf(0)] + [mpf(t.numerator) / t.denominator for t in x[:k - 1]]
    g = [mpf(t.numerator) / t.denominator for t in x[k - 1:]]
    S = [sum(exp((g[j] - mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
             for j in range(k)) for i in range(1, k)]
    T = [sum(exp((f[i] - mpf(c[(j - i) % k].numerator) / c[(j - i) % k].denominator) / e)
             for i in range(k)) for j in range(k)]
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


def preconditioner(k, c, eps, center):
    """C = J(center)^{-1} 的有理化（iv 紧包有理值）。"""
    Cinv = mp.inverse(jac_point_mp(k, c, eps, center))
    n = 2 * k - 1
    C = []
    for r in range(n):
        row = []
        for s in range(n):
            q = Fraction(mp.nstr(mpf(Cinv[r, s]), 40)).limit_denominator(PRECOND_DEN)
            row.append(iv.mpf(q.numerator) / q.denominator)
        C.append(row)
    return C


def matmul_iv(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(m)) for j in range(p)] for i in range(n)]


def krawczyk(k, c, eps, center, box, C):
    """K(X) = center - C·F(center) + (I - C·J(X))·(X-center)。返回 (K, inside, maxwidth, minmargin)。"""
    n = 2 * k - 1
    Fc = feval(k, c, eps, center)
    JI = jac_interval(k, c, eps, box)
    CFc = [sum(C[r][s] * Fc[s] for s in range(n)) for r in range(n)]
    CJ = matmul_iv(C, JI)
    M = [[(iv.mpf(1) if r == s else iv.mpf(0)) - CJ[r][s] for s in range(n)] for r in range(n)]
    Delta = [box[i] - (iv.mpf(center[i].numerator) / center[i].denominator) for i in range(n)]
    MD = [sum(M[r][s] * Delta[s] for s in range(n)) for r in range(n)]
    ctr = [iv.mpf(t.numerator) / t.denominator for t in center]
    K = [ctr[r] - CFc[r] + MD[r] for r in range(n)]
    inside = all(K[r].a > box[r].a and K[r].b < box[r].b for r in range(n))
    # 端点 .a/.b 为零宽区间可直接 float；差区间取下端点 .a 作保守裕度
    maxw = max(float(K[r].b) - float(K[r].a) for r in range(n))
    margin = min(min(float((K[r].a - box[r].a).a), float((box[r].b - K[r].b).a)) for r in range(n))
    return K, inside, maxw, margin


def run_instance(k, c, eps, negshift=False):
    """单实例全流程：闭形式→有理中心→盒→预条件子→Krawczyk。返回结果 dict。"""
    n = 2 * k - 1
    gstar = closed_form_gstar(k, c, eps)
    gh = rational_center(gstar)
    center = [Fraction(0)] * (k - 1) + [gh] * k
    if negshift:
        center = center[:k - 1] + [gh + NEG_SHIFT] * k
    rad = mpi(-BOX_R.numerator, BOX_R.numerator) / BOX_R.denominator
    box = [iv.mpf(t.numerator) / t.denominator + rad for t in center]
    C = preconditioner(k, c, eps, center)
    K, inside, maxw, margin = krawczyk(k, c, eps, center, box, C)
    Jc = jac_point_mp(k, c, eps, center)
    Jn = np.array([[float(Jc[r, s]) for s in range(n)] for r in range(n)])
    cond = float(np.linalg.cond(Jn))  # 2-范数条件数（与族 README 公布口径一致）
    return {
        "k": k, "eps": str(eps), "n": n, "negative_control": negshift,
        "gstar": mp.nstr(gstar, 25), "ghat": f"{gh.numerator}/{gh.denominator}",
        "center_err": mp.nstr(abs(mpf(gh.numerator) / gh.denominator - gstar), 5),
        "condJ": cond, "K_max_width": maxw, "K_min_margin": margin, "inside": bool(inside),
    }


def main():
    instances = []
    # 既有六例复验
    for fam in ("k6", "k10"):
        k = int(fam[1:])
        for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 5)):
            instances.append((f"{fam}-e{eps}", k, FAMILIES[fam], eps))
    # 扩实例：ε-scaling 延伸（沿用各族 c 向量）
    for fam in ("k6", "k10"):
        k = int(fam[1:])
        for eps in (Fraction(1, 10), Fraction(1, 20)):
            instances.append((f"{fam}-e{eps}-EXT", k, FAMILIES[fam], eps))

    results = []
    for tag, k, c, eps in instances:
        pos = run_instance(k, c, eps, negshift=False)
        neg = run_instance(k, c, eps, negshift=True)
        pos["tag"] = tag
        pos["neg_inside"] = neg["inside"]
        pos["neg_K_min_margin"] = neg["K_min_margin"]
        pos["pass"] = pos["inside"] and (not neg["inside"])
        results.append(pos)
        print(f"{tag:16s} n={pos['n']:2d} cond={pos['condJ']:7.2f} Kw={pos['K_max_width']:.3e} "
              f"margin={pos['K_min_margin']:.3e} inside={pos['inside']} neg_inside={neg['inside']} pass={pos['pass']}")

    n_ok = sum(1 for r in results if r["pass"])
    print(f"\nTOTAL: {n_ok}/{len(results)} inside=True 且负面拒证")
    with open("EXT05-BATCH-01-results.json", "w") as fh:
        json.dump({"methodology": "Krawczyk interval verification, mpmath.iv outward rounding, mp.dps=80; "
                                 "rational center limit_denominator(1e13); box radius 1e-9; "
                                 "preconditioner=inv(J(center)) rationalized limit_denominator(1e10); "
                                 "negative control: g-center shift +1e-6 must fail containment",
                   "results": results}, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
