# CLASSIFY: L1
# CERT-AUCTION-01 · 拍卖族（前向拍卖+ε-scaling+价格暖启动）对偶括弧交叉认证复验批
#
# 方法学（按 vci-inbox board/LAB-FRONTIER-04-20261008T1530Z.md §1「F-X4」与
# board/LAB-FRONTIER-03-20261008T1420Z.md「F-X3」忠实复原；判据不自创）：
#   实例生成器（由既成基准 cost=0.2550220110027003 逐位反演确认）：
#     rng = np.random.default_rng(seed); μ,ν = rng.random(k)×2（预抽，均匀边际不用）；
#     C = 10^(R·(2·rng.random((k,k))−1))   （动态范围参数 R）
#   拍卖：前向拍卖（min-cost，利润 a=-C）；bid = p_j + (best−second) + ε；
#     ε-scaling：ε0=0.5，每轮 /5，终轮 ε=1e-6；价格跨轮存续（暖启动）；
#     轮间解除违反当前 ε-CS 的分配对。
#   认证（F-X3 式对偶括弧，HiGHS 仅作不可信候选生成器）：
#     OT LP min c·x, Aeq x = beq(=1/k), x≥0；对偶 max beq·y, Aeq^T y ≤ c；
#     区间算术（np.nextafter 外向舍入）逐分量认证 rc_j = c_j−(Aeq^T y)_j ≥ 0；
#     退化修复 δ-deflation：y′=(1−δ)y, δ=1e-10（c>0 ⇒ y=0 严格可行 ⇒ 内点存在）；
#     LB=beq·y（区间），UB=c·x（x=HiGHS 原始解）；assignment 尺度括弧 = k×[LB_lo, UB_hi]；
#     判定：拍卖 cost ∈ 括弧 且 gap = cost − k·LB_lo ≤ k·ε_final。
#   阴性对照：交换两分配项（取增量最大者）→ cost 必须越出括弧（拒证）。
#
# 用法：python3 auction_verify.py → stdout 汇总 + EXT05-BATCH-01-auction-results.json
import json
import numpy as np
from scipy.optimize import linprog

INSTANCES = [
    # (tag, k, R, seed, eps0, factor, eps_final, 备注)
    ("k8-R2-seed7-BENCH", 8, 2, 7, 0.5, 5.0, 1e-6, "F-X4 既成基准复验"),
    ("k6-R2-seed11-EXT", 6, 2, 11, 0.5, 5.0, 1e-6, "扩实例"),
    ("k10-R2-seed13-EXT", 10, 2, 13, 0.5, 5.0, 1e-6, "扩实例"),
    ("k12-R2-seed17-EXT", 12, 2, 17, 0.5, 5.0, 1e-6, "扩实例"),
    ("k8-R2-seed7-SCHED-VAR", 8, 2, 7, 1.0, 4.0, 1e-6, "ε-schedule 变体 ε0=1,/4"),
]

INF = np.inf


def gen_C(k, R, seed):
    rng = np.random.default_rng(seed)
    rng.random(k); rng.random(k)          # μ,ν 预抽（均匀边际不使用，但占用随机流）
    return 10.0 ** (R * (2 * rng.random((k, k)) - 1))


def forward_auction(C, eps, p=None, assign=None):
    k = C.shape[0]
    if p is None: p = np.zeros(k)
    if assign is None: assign = {}
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
            del owner[j1]; del assign[prev]
            unassigned.append(prev)
        assign[i] = j1; owner[j1] = i
    return assign, p, bids


def eps_scaling_auction(C, eps0, factor, eps_final):
    k = C.shape[0]
    p = np.zeros(k); assign = {}
    eps = eps0; rounds = 0; total_bids = 0
    while True:
        for i, j in list(assign.items()):   # 解除违反当前 ε-CS 的对（价格保留=暖启动）
            if (-C[i] - p).max() - (-C[i, j] - p[j]) > eps + 1e-15:
                del assign[i]
        assign, p, b = forward_auction(C, eps, p, assign)
        rounds += 1; total_bids += b
        if eps <= eps_final:
            break
        eps = eps / factor
        if eps < eps_final:
            eps = eps_final
    return assign, p, rounds, total_bids


def epsCS_residual(C, assign, p):
    return float(max((-C[i] - p).max() - (-C[i, j] - p[j]) for i, j in assign.items()))


def iv_pt(v): return (float(v), float(v))
def iv_encl(v): return (float(np.nextafter(v, -INF)), float(np.nextafter(v, INF)))
def iv_add(a, b): return (float(np.nextafter(a[0] + b[0], -INF)), float(np.nextafter(a[1] + b[1], INF)))
def iv_sub(a, b): return (float(np.nextafter(a[0] - b[1], -INF)), float(np.nextafter(a[1] - b[0], INF)))
def iv_mul(a, b):
    ps = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (float(np.nextafter(min(ps), -INF)), float(np.nextafter(max(ps), INF)))


def certify_bracket(C, k, delta=1e-10):
    """F-X3 对偶括弧：HiGHS 生成候选 (x,y)，区间算术独立认证。"""
    kk = k * k
    c = C.flatten()
    Aeq = np.zeros((2 * k, kk))
    for i in range(k): Aeq[i, i * k:(i + 1) * k] = 1.0
    for j in range(k): Aeq[k + j, j::k] = 1.0
    beq = np.full(2 * k, 1.0 / k)
    res = linprog(c, A_eq=Aeq, b_eq=beq, method='highs')
    if res.status != 0:
        raise RuntimeError(f"HiGHS failed: {res.message}")
    y0 = res.eqlin.marginals
    x = res.x

    def rc_min_lo(yv):
        lo = INF
        for j in range(kk):
            s = iv_add(iv_pt(yv[j // k]), iv_pt(yv[k + j % k]))
            rc = iv_sub(iv_pt(c[j]), s)
            lo = min(lo, rc[0])
        return lo

    deflated = False
    if rc_min_lo(y0) < 0:                    # 退化骑零 → δ-deflation 修复
        deflated = True
        yv = (1 - delta) * np.asarray(y0)
    else:
        yv = np.asarray(y0)
    rc_lo = rc_min_lo(yv)
    dual_feasible_certified = rc_lo >= 0

    beq_iv = iv_encl(1.0 / k)
    LB = (0.0, 0.0)
    for i in range(2 * k):
        LB = iv_add(LB, iv_mul(beq_iv, iv_pt(yv[i])))
    UB = (0.0, 0.0)
    for j in range(kk):
        UB = iv_add(UB, iv_mul(iv_pt(c[j]), iv_pt(float(x[j]))))
    br = (float(np.nextafter(k * LB[0], -INF)), float(np.nextafter(k * UB[1], INF)))
    return {
        "dual_feasible_certified": bool(dual_feasible_certified),
        "deflated": deflated, "rc_min_lo": rc_lo,
        "LB_lp": LB, "UB_lp": UB, "bracket": br, "bracket_width": br[1] - br[0],
    }


def run(tag, k, R, seed, eps0, factor, eps_final):
    C = gen_C(k, R, seed)
    assign, p, rounds, bids = eps_scaling_auction(C, eps0, factor, eps_final)
    cost = float(sum(C[i, j] for i, j in assign.items()))
    resid = epsCS_residual(C, assign, p)
    cert = certify_bracket(C, k)
    lo, hi = cert["bracket"]
    inside = bool(lo < cost < hi) and cert["dual_feasible_certified"]
    gap = cost - lo
    gap_bound = k * eps_final
    # 阴性对照：交换增量最大的一对分配 → 必须越界拒证
    items = sorted(assign.items())
    worst = None
    for a in range(k):
        for b in range(a + 1, k):
            i1, j1 = items[a]; i2, j2 = items[b]
            c2 = cost - C[i1, j1] - C[i2, j2] + C[i1, j2] + C[i2, j1]
            if worst is None or c2 > worst[0]:
                worst = (float(c2), (i1, j1, i2, j2))
    neg_cost, neg_swap = worst
    neg_rejected = not (lo < neg_cost < hi)
    return {
        "tag": tag, "k": k, "R": R, "seed": seed,
        "eps0": eps0, "factor": factor, "eps_final": eps_final,
        "rounds": rounds, "bids": bids,
        "auction_cost": repr(cost), "epsCS_residual": repr(resid),
        "bracket": [repr(lo), repr(hi)], "bracket_width": repr(cert["bracket_width"]),
        "dual_feasible_certified": cert["dual_feasible_certified"],
        "deflated": cert["deflated"], "rc_min_lo": repr(cert["rc_min_lo"]),
        "gap": repr(gap), "gap_bound_k_eps": repr(gap_bound),
        "inside": inside, "gap_within_bound": bool(gap <= gap_bound),
        "neg_swap": [int(v) for v in neg_swap], "neg_cost": repr(neg_cost), "neg_rejected": bool(neg_rejected),
        "pass": bool(inside and gap <= gap_bound and neg_rejected),
    }


def main():
    results = []
    for spec in INSTANCES:
        r = run(*spec[:7])
        r["note"] = spec[7]
        results.append(r)
        print(f"{r['tag']:22s} cost={float(r['auction_cost']):.16f} bracket=({float(r['bracket'][0]):.13f},{float(r['bracket'][1]):.13f}) "
              f"gap={float(r['gap']):.2e}<={float(r['gap_bound_k_eps']):.0e} inside={r['inside']} "
              f"neg_cost={float(r['neg_cost']):.2f} rejected={r['neg_rejected']} resid={float(r['epsCS_residual']):.1e} "
              f"rounds={r['rounds']} bids={r['bids']} pass={r['pass']}")
    n_ok = sum(1 for r in results if r["pass"])
    print(f"\nTOTAL: {n_ok}/{len(results)} 五字段全过（inside ∧ gap≤k·ε ∧ 阴性拒证）")
    with open("EXT05-BATCH-01-auction-results.json", "w") as fh:
        json.dump({"methodology": "F-X4 拍卖（前向+ε-scaling+价格暖启动）× F-X3 对偶括弧交叉认证；"
                                  "HiGHS 仅候选生成器；区间算术 np.nextafter 外向舍入；δ-deflation=1e-10；"
                                  "判据：cost∈k×[LB_lo,UB_hi] ∧ gap≤k·ε_final ∧ 交换扰动阴性对照越界拒证",
                   "generator": "rng=default_rng(seed); rng.random(k)×2 预抽; C=10^(R·(2·rng.random((k,k))−1))",
                   "results": results}, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
