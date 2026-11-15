"""AD-26 S^2：在 6/7/8/9-CZ 解流形上逐步吸附简单角，减少非简单代表元。

吸附只改变同一精确电路的代表元；每次均以全矩阵残差验收。
"""
import hashlib
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent.parent / "ad22/run"))
import ad22_verify as base
sys.path.insert(0, str(R.parent.parent / "ad25/run"))
import ad25_s2_meridian as s2
sys.path.insert(0, str(R))
from ad26_s2_prune import raw_indices, expand

T0, P0 = np.pi/7, 0.31


def solve_free(core, free, edges, theta, phi, max_nfev=500):
    free = np.asarray(free, dtype=int)
    ix = np.asarray(raw_indices(edges), dtype=int)
    target = s2.target(theta, phi)
    def unpack(x):
        c = np.asarray(core).copy()
        c[free] = x
        return c
    def fj(x):
        c = unpack(x)
        f, j = base.residual_jacobian(expand(c, edges), edges, target)
        return f, j[:, ix[free]]
    sol = least_squares(lambda x: fj(x)[0], np.asarray(core)[free], jac=lambda x: fj(x)[1],
                        method="trf", max_nfev=max_nfev, ftol=1e-14, xtol=1e-14, gtol=1e-14)
    c = unpack(sol.x)
    error = float(np.max(abs(base.circuit(expand(c, edges), edges)-target)))
    return c, error, int(sol.nfev), float(sol.optimality)


def candidate(task):
    core, free, j, edges = task
    c = np.asarray(core).copy()
    # 吸附到离当前角最近的 pi/4 整数倍；只允许 2pi 周期内的代表元移动。
    value = (np.pi/4)*np.round(c[j]/(np.pi/4))
    delta = float((value-c[j]+np.pi)%(2*np.pi)-np.pi)
    value = c[j]+delta
    nf = [x for x in free if x != j]
    c[j] = value
    c, error, nfev, opt = solve_free(c, nf, edges, T0, P0)
    return {"j": j, "value": float(value), "delta": float(delta), "core": c.tolist(),
            "free": nf, "target_max_abs": error, "nfev": nfev, "optimality": opt}


def main():
    start = time.time()
    stem = sys.argv[1] if len(sys.argv) > 1 else "010"
    select8 = {"89d2": ("89", 2), "89d7": ("89", 7), "010d1": ("010", 1)}
    select7 = {"89d2d0": ("89d2", 0), "89d2d6": ("89d2", 6)}
    select6 = {"89d2d0d1": ("89d2d0", 1), "89d2d6d2": ("89d2d6", 2)}
    assert stem in {"010", "89", *select8, *select7, *select6}
    if stem in select8 or stem in select7 or stem in select6:
        topology, deleted = (select8 | select7 | select6)[stem]
        source_name = ("ad26_s2_9to8.jsonl" if stem in select8 else
                       "ad26_s2_8to7.jsonl" if stem in select7 else "ad26_s2_7to6.jsonl")
        source_rows = [json.loads(s) for s in (R/source_name).read_text().splitlines() if s.strip()]
        found = [r for r in source_rows if r["topology"] == topology and r["deleted"] == [deleted]
                 and r["kick"] == 0.02 and r["target_max_abs"] < 1e-9]
        assert len(found) == 1
        src = found[0]
        edges = [tuple(e) for e in src["edges"]]
        ix = np.asarray(raw_indices(edges), dtype=int)
        core = np.asarray(src["x_core"], dtype=float)
    else:
        src = json.loads((R / f"ad26_s2_raw9_{stem}.json").read_text())
        edges = [tuple(e) for e in src["edges"]]
        ix = np.asarray(raw_indices(edges), dtype=int)
        core = np.asarray(src["x_raw"])[ix]
    free = list(range(len(core)))
    core, e0, n0, o0 = solve_free(core, free, edges, T0, P0, 150)
    assert e0 < 2e-12
    accepted, rejected = [], []
    for round_no in range(len(core)):
        tasks = [(core, free, j, edges) for j in free]
        rows = []
        with ProcessPoolExecutor(max_workers=8) as ex:
            fs = [ex.submit(candidate, t) for t in tasks]
            for f in as_completed(fs):
                rows.append(f.result())
        hits = [r for r in rows if r["target_max_abs"] < 1e-9]
        if not hits:
            rejected.append({"round": round_no, "tested": len(rows),
                             "best": min(({"j": r["j"], "target_max_abs": r["target_max_abs"]} for r in rows),
                                         key=lambda x: x["target_max_abs"])})
            break
        # 优先最小吸附位移，其次较少函数调用，避免无谓换盆。
        hits.sort(key=lambda r: (abs(r["delta"]), r["nfev"], r["j"]))
        chosen = hits[0]
        core = np.asarray(chosen.pop("core"))
        free = chosen.pop("free")
        accepted.append({"round": round_no, **chosen, "tested": len(rows), "feasible": len(hits)})
        print(json.dumps({"round": round_no, "freeze": chosen["j"], "value": chosen["value"],
                          "delta": chosen["delta"], "feasible": len(hits), "free": len(free)}), flush=True)
    # 固定吸附角后，在同一 5x5 网格上重走连续延拓。
    thetas = [0.20, 0.32, T0, 0.58, 0.74]
    phis = [-0.32, 0.0, P0, 0.62, 0.94]
    grid, centers = [], {}
    for theta in sorted(thetas, key=lambda t: (abs(t-T0), t)):
        c0 = core if not centers else centers[min(centers, key=lambda t: abs(t-theta))].copy()
        c, error, nfev, opt = solve_free(c0, free, edges, theta, P0)
        centers[theta] = c.copy()
        grid.append({"theta": theta, "phi": P0, "target_max_abs": error, "nfev": nfev,
                     "optimality": opt, "core": c.tolist()})
        for phi in sorted((p for p in phis if p != P0), key=lambda p: (abs(p-P0), p)):
            same = [r for r in grid if r["theta"] == theta]
            prev = min(same, key=lambda r: abs(r["phi"]-phi))
            c, error, nfev, opt = solve_free(np.asarray(prev["core"]), free, edges, theta, phi)
            grid.append({"theta": theta, "phi": phi, "target_max_abs": error, "nfev": nfev,
                         "optimality": opt, "core": c.tolist()})
    hits = [r for r in grid if r["target_max_abs"] < 1e-9]
    worst = max(grid, key=lambda r: r["target_max_abs"])
    out = {"beat": "AD-26", "status": f"S2_{len(edges)}CZ_SIMPLE_ANGLE_REDUCTION_COMPLETE",
           "topology": stem, "edges": [list(e) for e in edges], "known_answer_gate_first": e0,
           "initial_core_dimension": len(ix), "final_free_dimension": len(free),
           "frozen_simple_angles": accepted, "last_rejected_round": rejected[-1] if rejected else None,
           "grid_points": len(grid), "grid_exact_numeric_hits": len(hits),
           "grid_worst": {k: worst[k] for k in ("theta", "phi", "target_max_abs", "nfev")},
           "evidence_level": "L2 exact-at-numerical-tolerance representative reduction and finite-grid continuation",
           "boundary": "简单角吸附和网格命中仍不是全参数符号恒等式；不能吸附更多角不排除其他代表元或其他拓扑。",
           "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False}
    (R / f"ad26_s2_gauge_reduced_{stem}_grid.jsonl").write_text(
        "".join(json.dumps(r, separators=(",", ":"))+"\n" for r in grid))
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / f"ad26_s2_gauge_reduced_{stem}_summary.json").write_bytes(raw)
    print(json.dumps({"frozen": len(accepted), "free": len(free), "grid_hits": len(hits),
                      "grid_points": len(grid), "worst": out["grid_worst"],
                      "seconds": time.time()-start, "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
