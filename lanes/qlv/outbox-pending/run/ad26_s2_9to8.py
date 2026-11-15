"""AD-26 S^2：两套已证 9-CZ 模板的定向 9->8 单点攻击。

任何命中都必须再做二维延拓和全参数证书；零命中只覆盖36条指定删门轨。
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
sys.path.insert(0, str(R.parent.parent/"ad22/run"))
import ad22_verify as base
sys.path.insert(0, str(R.parent.parent/"ad23/run"))
import ad23_gauge as gauge
sys.path.insert(0, str(R.parent.parent/"ad25/run"))
import ad25_s2_meridian as s2
import ad26_s2_prune as prune
import ad26_s2_analytic9_89 as a89
import ad26_s2_analytic9 as a010

THETA, PHI = np.pi/7, 0.31


def source(stem):
    if stem == "89":
        core = a89.core(THETA, PHI)
        edges = list(a89.EDGES)
    elif stem == "010":
        core, _ = a010.angles(THETA, PHI)
        edges = list(a010.EDGES)
    else:
        raise ValueError(stem)
    p = prune.expand(core, edges)
    e = float(np.max(abs(base.circuit(p, edges)-s2.target(THETA, PHI))))
    assert e < 2e-12, (stem, e)
    phase, layers = gauge.unpack(p)
    return phase, layers, edges, p, e


def target_fj(core, edges, target):
    f, J = base.residual_jacobian(prune.expand(core, edges), edges, target)
    return f, J[:, prune.raw_indices(edges)]


def solve_at(core, edges, target, xstart=None, max_nfev=900):
    x0 = np.asarray(core if xstart is None else xstart, float)
    sol = least_squares(lambda x: target_fj(x, edges, target)[0], x0,
                        jac=lambda x: target_fj(x, edges, target)[1],
                        method="trf", max_nfev=max_nfev,
                        ftol=1e-14, xtol=1e-14, gtol=1e-14)
    e = float(np.max(abs(base.circuit(prune.expand(sol.x, edges), edges)-target)))
    return sol, e


def known_gates():
    out = {}
    for stem in ("89", "010"):
        ph, layers, edges, p, source_e = source(stem)
        target = s2.target(THETA, PHI)
        core = p[prune.raw_indices(edges)]
        sol, e = solve_at(core, edges, target, max_nfev=150)
        assert e < 2e-12, (stem, e)
        ne, c8, preserve = prune.delete_gates(ph, layers, edges, (0,))
        known8 = base.circuit(prune.expand(c8, ne), ne)
        rng = np.random.default_rng(26300+int(stem == "010"))
        xs = c8+1e-5*rng.normal(size=len(c8))
        sol8, e8 = solve_at(c8, ne, known8, xs, 350)
        assert e8 < 2e-10, (stem, e8)
        bad = core.copy()
        bad[1] += np.pi/4
        bad_e = float(np.max(abs(base.circuit(prune.expand(bad, edges), edges)-target)))
        assert bad_e > 1e-3
        out[stem] = {"source_9cz_max_abs": source_e, "same_point_9cz_solver_max_abs": e,
                     "deleted_self_target_8cz_recovery_max_abs": e8,
                     "merge_canonical_max_abs": preserve,
                     "changed_angle_counterexample_max_abs": bad_e}
    return out


def solve(task):
    stem, delete, kick, ne, core = task
    begin = time.time()
    rng = np.random.default_rng(26400+(1000 if stem == "010" else 0)+10*delete+int(kick*1000))
    xs = np.asarray(core)+kick*rng.normal(size=len(core))
    try:
        sol, e = solve_at(core, ne, s2.target(THETA, PHI), xs, 900)
        return {"topology": stem, "deleted": [delete], "k": 8, "kick": kick,
                "edges": [list(x) for x in ne], "target_max_abs": e,
                "nfev": int(sol.nfev), "status": int(sol.status),
                "optimality": float(sol.optimality), "x_core": sol.x.tolist(),
                "seconds": time.time()-begin}
    except Exception as exc:
        return {"topology": stem, "deleted": [delete], "k": 8, "kick": kick,
                "error": type(exc).__name__+": "+str(exc), "seconds": time.time()-begin}


def main():
    begin = time.time()
    gates = known_gates()
    tasks = []
    max_preserve = 0.0
    for stem in ("89", "010"):
        ph, layers, edges, p, _ = source(stem)
        for delete in range(9):
            ne, core, preserve = prune.delete_gates(ph, layers, edges, (delete,))
            max_preserve = max(max_preserve, preserve)
            for kick in (0.0, 0.02):
                tasks.append((stem, delete, kick, ne, core))
    rows = []
    with ProcessPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(solve, t): (t[0], t[1], t[2]) for t in tasks}
        for n, fut in enumerate(as_completed(futs), 1):
            key = futs[fut]
            try:
                rows.append(fut.result())
            except Exception as exc:
                rows.append({"topology": key[0], "deleted": [key[1]], "kick": key[2],
                             "error": type(exc).__name__+": "+str(exc)})
            print(json.dumps({"done": n, "total": len(tasks), "elapsed": time.time()-begin}), flush=True)
    rows.sort(key=lambda r: (r["topology"], r["deleted"], r["kick"]))
    (R/"ad26_s2_9to8.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    per = {}
    for stem in ("89", "010"):
        rr = [r for r in rows if r["topology"] == stem and "error" not in r]
        assert len(rr) == 18
        hits = [r for r in rr if r["target_max_abs"] < 1e-9]
        best = min(rr, key=lambda r: r["target_max_abs"])
        per[stem] = {"runs": len(rr), "exact_numeric_hits": len(hits),
                     "best": {k: best[k] for k in ("deleted", "kick", "target_max_abs", "nfev", "optimality")},
                     "hit_deletions": [r["deleted"] for r in hits]}
    out = {"beat": "AD-26", "status": "S2_TWO_9CZ_TO8_TARGETED_POINT_COMPLETE",
           "known_answer_gate_first": gates, "theta": THETA, "phi": PHI,
           "merge_canonical_max_abs": max_preserve,
           "protocol": "two exact 9-CZ sources; 9 single deletions per source; kicks 0/0.02; canonical 34-core; TRF max_nfev=900 at one generic point",
           "runs": len(rows), "errors": sum("error" in r for r in rows),
           "exact_numeric_hits": sum(v["exact_numeric_hits"] for v in per.values()), "per_topology": per,
           "evidence_level": "L2 targeted local numerical search at one generic point",
           "boundary": "只覆盖两套9-CZ代表元的18种删门及两种扰动，共36轨；零命中不证明其他拓扑、其他代表元、该点或全S^2的8-CZ不存在。",
           "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False,
           "seconds": time.time()-begin}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/"ad26_s2_9to8_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "exact_numeric_hits": out["exact_numeric_hits"], "per_topology": per,
                      "seconds": out["seconds"], "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
