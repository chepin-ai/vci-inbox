"""AD-26 S^2：不同 8/7-CZ 边序代表元的二维连续延拓。"""
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent.parent/"ad22/run"))
import ad22_verify as base
sys.path.insert(0, str(R.parent.parent/"ad25/run"))
import ad25_s2_meridian as s2
from ad26_s2_prune import raw_indices, expand

THETA0, PHI0 = np.pi/7, 0.31
THETAS = [0.20, 0.32, THETA0, 0.58, 0.74]
PHIS = [-0.32, 0.0, PHI0, 0.62, 0.94]
K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
assert K in (6, 7, 8)
SELECT = ({"89d2": ("89", 2), "89d7": ("89", 7), "010d1": ("010", 1)} if K == 8 else
          {"89d2d0": (0,), "89d2d6": (6,)} if K == 7 else
          {"89d2d0d1": ("89d2d0", 1), "89d2d6d2": ("89d2d6", 2)})


def fj(core, edges, theta, phi):
    f, j = base.residual_jacobian(expand(core, edges), edges, s2.target(theta, phi))
    return f, j[:, raw_indices(edges)]


def solve_at(core, edges, theta, phi, max_nfev=900):
    sol = least_squares(lambda x: fj(x, edges, theta, phi)[0], np.asarray(core),
                        jac=lambda x: fj(x, edges, theta, phi)[1], method="trf",
                        max_nfev=max_nfev, ftol=1e-14, xtol=1e-14, gtol=1e-14)
    p = expand(sol.x, edges)
    error = float(np.max(abs(base.circuit(p, edges)-s2.target(theta, phi))))
    return sol, p, error


def source(stem):
    if K == 8:
        topology, deleted = SELECT[stem]
        rows = [json.loads(s) for s in (R/"ad26_s2_9to8.jsonl").read_text().splitlines() if s.strip()]
        found = [r for r in rows if r["topology"] == topology and r["deleted"] == [deleted]
                 and r["kick"] == 0.02 and r["target_max_abs"] < 1e-9]
    else:
        source_name = "ad26_s2_8to7.jsonl" if K == 7 else "ad26_s2_7to6.jsonl"
        rows = [json.loads(s) for s in (R/source_name).read_text().splitlines() if s.strip()]
        if K == 7:
            deleted = SELECT[stem][0]
            found = [r for r in rows if r["deleted"] == [deleted]
                     and r["kick"] == 0.02 and r["target_max_abs"] < 1e-9]
        else:
            topology, deleted = SELECT[stem]
            found = [r for r in rows if r["topology"] == topology and r["deleted"] == [deleted]
                     and r["kick"] == 0.02 and r["target_max_abs"] < 1e-9]
    assert len(found) == 1, (stem, len(found))
    r = found[0]
    edges = [tuple(e) for e in r["edges"]]
    p0 = expand(r["x_core"], edges)
    return r, edges, p0


def run_topology(stem):
    begin = time.time()
    src, edges, p0 = source(stem)
    core0 = p0[raw_indices(edges)]
    source_error = float(np.max(abs(base.circuit(p0, edges)-s2.target(THETA0, PHI0))))
    assert source_error < 2e-12
    _, _, known_error = solve_at(core0, edges, THETA0, PHI0, 180)
    assert known_error < 2e-12
    _, _, near_error = solve_at(core0, edges, THETA0+0.01, PHI0, 350)
    assert near_error < 2e-12, (stem, near_error)
    gate = {"source_point_max_abs": source_error, "same_point_solver_max_abs": known_error,
            "theta_plus_0.01_solver_max_abs": near_error}
    rows, cores = [], {}
    for theta in sorted(THETAS, key=lambda t: (abs(t-THETA0), t)):
        core = core0.copy()
        if theta != THETA0:
            previous = min((t for t in cores if ("mid", t) in cores), key=lambda t: abs(t-theta), default=None)
            if previous is not None:
                core = cores[("mid", previous)].copy()
        sol, p, error = solve_at(core, edges, theta, PHI0)
        cores[("mid", theta)] = sol.x.copy()
        rows.append({"path": "theta", "theta": theta, "phi": PHI0, "target_max_abs": error,
                     "nfev": int(sol.nfev), "status": int(sol.status),
                     "optimality": float(sol.optimality), "x_raw": p.tolist()})
        print(json.dumps({"topology": stem, "path": "theta", "theta": theta,
                          "error": error, "nfev": int(sol.nfev)}), flush=True)
        for phi in sorted((x for x in PHIS if x != PHI0), key=lambda x: (abs(x-PHI0), x)):
            candidates = [PHI0]+[r["phi"] for r in rows if r["path"] == "phi" and r["theta"] == theta]
            previous_phi = min(candidates, key=lambda x: abs(x-phi))
            if previous_phi == PHI0:
                previous_core = cores[("mid", theta)]
            else:
                previous_core = np.asarray(next(r["x_raw"] for r in rows if r["path"] == "phi"
                                                  and r["theta"] == theta and r["phi"] == previous_phi))[raw_indices(edges)]
            sol, p, error = solve_at(previous_core, edges, theta, phi)
            cores[("phi", theta, phi)] = sol.x.copy()
            rows.append({"path": "phi", "theta": theta, "phi": phi, "target_max_abs": error,
                         "nfev": int(sol.nfev), "status": int(sol.status),
                         "optimality": float(sol.optimality), "x_raw": p.tolist()})
            print(json.dumps({"topology": stem, "path": "phi", "theta": theta, "phi": phi,
                              "error": error, "nfev": int(sol.nfev)}), flush=True)
    rows.sort(key=lambda r: (r["theta"], r["phi"]))
    (R/f"ad26_s2_continue{K}_{stem}.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    good = [r for r in rows if r["target_max_abs"] < 1e-9]
    best, worst = min(rows, key=lambda r: r["target_max_abs"]), max(rows, key=lambda r: r["target_max_abs"])
    out = {"beat": "AD-26", "status": f"S2_{K}CZ_GRID_CONTINUATION_COMPLETE",
           "topology": stem, "source_deleted": src["deleted"], "source_topology": src["topology"],
           "edges": [list(e) for e in edges], "known_answer_gate_first": gate,
           "theta_values": THETAS, "phi_values": PHIS, "grid_points": len(rows),
           "exact_numeric_hits": len(good), "nonhits": len(rows)-len(good),
           "best": {k: best[k] for k in ("theta", "phi", "target_max_abs", "nfev")},
           "worst": {k: worst[k] for k in ("theta", "phi", "target_max_abs", "nfev")},
           "evidence_level": "L2 numerical continuation on a finite 5x5 grid with fixed gate topology",
           "boundary": f"网格命中不是全S^2恒等式；非命中只表示当前暖启动轨道未闭合，不证明{K}-CZ不存在。",
           "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False,
           "seconds": time.time()-begin}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/f"ad26_s2_continue{K}_{stem}_summary.json").write_bytes(raw)
    print(json.dumps({"topology": stem, "grid_points": len(rows), "hits": len(good),
                      "worst": out["worst"], "seconds": out["seconds"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2), flush=True)


def main():
    for stem in SELECT:
        run_topology(stem)


if __name__ == "__main__":
    main()
