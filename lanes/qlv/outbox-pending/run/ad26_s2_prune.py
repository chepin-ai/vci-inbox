"""AD-26 S^2：解析 11-CZ 模板的跨块定向删门与全局重解。

在一个非特殊 (theta,phi) 点搜索；任何命中还须回到全参数恒等式。
零命中只覆盖指定解析轨道及扰动，不是 9/10-CZ 不存在证明。
"""
import hashlib
import itertools
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

R = Path(__file__).resolve().parent
R22 = R.parent.parent / "ad22/run"
R23 = R.parent.parent / "ad23/run"
R25 = R.parent.parent / "ad25/run"
sys.path.insert(0, str(R22))
import ad22_verify as base
sys.path.insert(0, str(R23))
import ad23_gauge as gauge
sys.path.insert(0, str(R25))
import ad25_s2_meridian as s2

THETA = np.pi/7
PHI = 0.31


def raw_indices(edges):
    ix = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            ix.extend([1+(i*3+q)*3+1, 1+(i*3+q)*3+2])
    ix.extend(range(1+9*len(edges), 1+9*(len(edges)+1)))
    assert len(ix) == 4*len(edges)+10
    return ix


def expand(core, edges):
    p = np.zeros(1+9*(len(edges)+1))
    p[raw_indices(edges)] = core
    return p


def target_fj(core, edges):
    f, j = base.residual_jacobian(expand(core, edges), edges, s2.target(THETA, PHI))
    return f, j[:, raw_indices(edges)]


def source():
    phase, angles, edges = s2.full_angles(THETA, PHI)
    assert np.max(abs(base.circuit(np.concatenate([[phase], angles.reshape(-1)]), edges)
                      - s2.target(THETA, PHI))) < 2e-12
    layers = [[base.su2(a) for a in row] for row in angles]
    return phase, layers, edges


def delete_gates(phase, layers, edges, delete):
    delete = set(delete)
    nl, ne = [list(layers[0])], []
    for j, edge in enumerate(edges):
        if j in delete:
            nl[-1] = [layers[j+1][q] @ nl[-1][q] for q in range(3)]
        else:
            ne.append(edge)
            nl.append(list(layers[j+1]))
    assert len(nl) == len(ne)+1
    p = np.concatenate([[phase], np.asarray([[gauge.zxz(u) for u in row] for row in nl]).reshape(-1)])
    ph, ll, _ = gauge.canonicalize(p, ne)
    pc = gauge.pack(ph, ll)
    preserve = float(np.max(abs(base.circuit(pc, ne)-base.circuit(p, ne))))
    assert preserve < 3e-11, preserve
    return ne, pc[raw_indices(ne)], preserve


def known_answer_gate():
    ph, ll, ee = source()
    p = gauge.pack(ph, ll)
    source_e = float(np.max(abs(base.circuit(p, ee)-s2.target(THETA, PHI))))
    core = p[raw_indices(ee)]
    sol = least_squares(lambda x: target_fj(x, ee)[0], core,
                        jac=lambda x: target_fj(x, ee)[1], method="trf", max_nfev=100,
                        ftol=1e-14, xtol=1e-14, gtol=1e-14)
    e = float(np.max(abs(base.circuit(expand(sol.x, ee), ee)-s2.target(THETA, PHI))))
    assert source_e < 2e-12 and e < 2e-12
    # θ=0 独立已知答案，防止只对非零点自洽。
    p0, a0, e0 = s2.full_angles(0.0, 0.0)
    zero_e = float(np.max(abs(base.circuit(np.concatenate([[p0], a0.reshape(-1)]), e0)
                             - s2.target(0.0, 0.0))))
    assert zero_e < 2e-12
    return {"source_11cz_max_abs": source_e, "known_11cz_solver_max_abs": e,
            "theta_zero_max_abs": zero_e}


def solve(task):
    delete, kick, ne, core = task
    seed = 261000 + sum((i+1)*d for i, d in enumerate(delete)) + int(kick > 0)
    rng = np.random.default_rng(seed)
    x0 = np.asarray(core) + kick*rng.normal(size=len(core))
    try:
        sol = least_squares(lambda x: target_fj(x, ne)[0], x0,
                            jac=lambda x: target_fj(x, ne)[1], method="trf", max_nfev=900,
                            ftol=1e-14, xtol=1e-14, gtol=1e-14)
        p = expand(sol.x, ne)
        e = float(np.max(abs(base.circuit(p, ne)-s2.target(THETA, PHI))))
        return {"deleted": list(delete), "k": len(ne), "kick": kick,
                "edges": [list(x) for x in ne], "target_max_abs": e,
                "nfev": int(sol.nfev), "status": int(sol.status),
                "optimality": float(sol.optimality), "x_core": sol.x.tolist()}
    except Exception as exc:
        return {"deleted": list(delete), "k": len(ne), "kick": kick,
                "error": type(exc).__name__+": "+str(exc)}


def main():
    start = time.time()
    gate = known_answer_gate()
    ph, ll, ee = source()
    tasks = []
    max_preserve = 0.0
    for size in (1, 2):
        for delete in itertools.combinations(range(11), size):
            ne, core, pres = delete_gates(ph, ll, ee, delete)
            max_preserve = max(max_preserve, pres)
            for kick in (0.0, 0.02):
                tasks.append((delete, kick, ne, core))
    rows = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        fs = [ex.submit(solve, t) for t in tasks]
        for n, f in enumerate(as_completed(fs), 1):
            rows.append(f.result())
            if n % 22 == 0:
                print(json.dumps({"done": n, "total": len(fs), "seconds": time.time()-start}), flush=True)
    rows.sort(key=lambda r: (r["k"], r["deleted"], r["kick"]))
    (R / "ad26_s2_11to9_point.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    good = [r for r in rows if "error" not in r]
    exact = [r for r in good if r["target_max_abs"] < 1e-9]
    per = {}
    for k in (10, 9):
        rr = [r for r in good if r["k"] == k]
        best = min(rr, key=lambda r: r["target_max_abs"])
        eh = [r for r in rr if r["target_max_abs"] < 1e-9]
        per[str(k)] = {"runs": len(rr), "exact_numeric_hits": len(eh),
                       "best": {x: best[x] for x in ("deleted", "kick", "target_max_abs", "nfev", "optimality")},
                       "exact_hit_deletions": [r["deleted"] for r in eh]}
    out = {"beat": "AD-26", "status": "S2_11TO9_TARGETED_POINT_COMPLETE",
           "known_answer_gate_first": gate, "theta": THETA, "phi": PHI,
           "merge_canonical_max_abs": max_preserve,
           "protocol": "analytic 11-CZ source; 11 single + 55 pair deletions; kicks {0,0.02}; canonical cores; one generic point",
           "runs": len(rows), "errors": len(rows)-len(good), "per_k": per,
           "evidence_level": "L2 targeted local numerical search at one generic point",
           "boundary": "只覆盖所测点、66条删门轨道及指定扰动；零命中不证明该点或全S^2的9/10-CZ不存在。任何数值命中也尚不是全参数构造。",
           "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad26_s2_11to9_point_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "per_k": per, "seconds": time.time()-start,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
