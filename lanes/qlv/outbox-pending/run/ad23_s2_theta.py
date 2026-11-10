"""AD-23 序34经线：core30 精确线性候选的网格外数值证伪实验。

本程序只产生 L2 数值证据，不把 64 点拟合或 63 点外推称为全经线解析定理。
"""
import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

RUN = Path(__file__).resolve().parent
R22 = RUN.parent.parent / "ad22/run"
R21 = RUN.parent.parent / "ad21/run"
import sys
sys.path.insert(0, str(R22))
import ad22_verify as base
sys.path.insert(0, str(RUN))
import ad23_gauge as gauge

EDGES = list(itertools.product(base.PATH, repeat=7))[34]
PERM = (0, 1, 2)
SIGMA = 1
PHASE_INDEX = 30


def raw_indices(edges):
    k = len(edges)
    ix = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            ix.extend([1 + 9 * i + 3 * q + 1, 1 + 9 * i + 3 * q + 2])
    ix.extend(range(1 + 9 * k, 1 + 9 * (k + 1)))
    assert len(ix) == 4 * k + 10
    return ix


IX = raw_indices(EDGES)
FREE = [j for j in range(len(IX)) if j != PHASE_INDEX]


def expand(core):
    p = np.zeros(1 + 9 * (len(EDGES) + 1))
    p[IX] = core
    return p


def fj(core, target):
    f, j = base.residual_jacobian(expand(core), EDGES, target)
    return f, j[:, IX]


def canonical_core(x):
    phase, layers, meta = gauge.canonicalize(np.asarray(x, dtype=float), EDGES)
    packed = gauge.pack(phase, layers)
    return packed[IX]


def target(theta, phi):
    h = base.sphere(PERM, SIGMA, theta, phi)
    return base.target_of(h, base.TARGETS["G2"])


def error(core, theta, phi):
    return float(np.max(np.abs(base.circuit(expand(core), EDGES) - target(theta, phi))))


def solve_fixed(core0, theta, phi):
    core0 = np.asarray(core0, dtype=float).copy()
    core0[PHASE_INDEX] = (np.pi - theta) / 2

    def f(free):
        core = core0.copy()
        core[FREE] = free
        return fj(core, target(theta, phi))[0]

    def j(free):
        core = core0.copy()
        core[FREE] = free
        return fj(core, target(theta, phi))[1][:, FREE]

    sol = least_squares(f, core0[FREE], jac=j, method="lm", max_nfev=2400,
                        ftol=1e-14, xtol=1e-14, gtol=1e-14)
    core = core0.copy()
    core[FREE] = sol.x
    return core, sol


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start = time.time()
    tangent = json.loads((R21 / "ad21_tangent.json").read_text())
    case = next(c for c in tangent["cases"] if c["name"] == "G2k7_seq34")
    phi = case["phi"]
    rows = [json.loads(s) for s in (R21 / "ad21_continuation.jsonl").read_text().splitlines()]
    old = sorted([r for r in rows if r.get("case") == "G2k7_seq34" and
                  r.get("kind") == "theta_navigation" and r["e"] < 1e-8],
                 key=lambda r: r["theta"])
    assert len(old) == 64

    # 旧账线性候选与独立电路重算。
    old_cores = [canonical_core(r["x"]) for r in old]
    old_errors = [error(c, r["theta"], phi) for c, r in zip(old_cores, old)]
    linear_errors = [abs(c[PHASE_INDEX] - (np.pi - r["theta"]) / 2)
                     for c, r in zip(old_cores, old)]
    assert max(old_errors) < 1e-8 and max(linear_errors) < 2e-14

    # 已知答案门：求解器在旧根上必须保持机器零。
    known_theta = old[32]["theta"]
    known_core, known_sol = solve_fixed(old_cores[32], known_theta, phi)
    known_e = error(known_core, known_theta, phi)
    assert known_e < 2e-12, known_e

    # 只替换 core30、其余保持基点值：应作为充分性反例被记录，而非藏起来。
    base_core = canonical_core(case["x_polished"])
    no_refit = []
    for theta in np.linspace(0, np.pi, 65):
        core = base_core.copy()
        core[PHASE_INDEX] = (np.pi - theta) / 2
        no_refit.append(error(core, theta, phi))
    assert max(no_refit) > 0.1

    # 每个新点都是相邻两个旧点的中点；初值仅用旧 raw x 线性插值，随后重解其余37坐标。
    out_path = RUN / "ad23_s2_theta.jsonl"
    results = []
    with out_path.open("w", buffering=1) as fp:
        for n in range(len(old) - 1):
            left, right = old[n], old[n + 1]
            theta = (left["theta"] + right["theta"]) / 2
            x0 = (np.asarray(left["x"]) + np.asarray(right["x"])) / 2
            core0 = canonical_core(x0)
            core, sol = solve_fixed(core0, theta, phi)
            e = error(core, theta, phi)
            row = {
                "interval_index": n, "theta": theta, "phi": phi,
                "bracket_theta": [left["theta"], right["theta"]],
                "core30": core[PHASE_INDEX], "core30_formula": (np.pi - theta) / 2,
                "core30_abs_delta": abs(core[PHASE_INDEX] - (np.pi - theta) / 2),
                "e": e, "nfev": int(sol.nfev), "optimizer_status": int(sol.status),
                "optimality": float(sol.optimality), "x_core": core.tolist(),
            }
            assert row["core30_abs_delta"] == 0.0
            results.append(row)
            fp.write(json.dumps(row, separators=(",", ":")) + "\n")
            fp.flush()
            import os
            os.fsync(fp.fileno())

    hits = [r for r in results if r["e"] < 1e-9]
    report = {
        "beat": "AD-23", "case": "G2k7_seq34", "evidence_level": "L2 numerical only",
        "status": "S2_THETA_OUT_OF_SAMPLE_PASS" if len(hits) == 63 else "S2_THETA_OUT_OF_SAMPLE_PARTIAL",
        "perm": list(PERM), "sigma": SIGMA, "phi": phi, "edges": EDGES,
        "coordinate": {"core_index": 30, "label": "L7q0b", "formula": "(pi-theta)/2"},
        "old_points": len(old), "old_max_circuit_e": max(old_errors),
        "old_max_coordinate_formula_abs_error": max(linear_errors),
        "known_answer_gate_e": known_e,
        "new_off_grid_points": len(results), "new_exact_e_lt_1e-9": len(hits),
        "new_max_e": max(r["e"] for r in results), "new_best_e": min(r["e"] for r in results),
        "single_coordinate_no_refit_points": len(no_refit),
        "single_coordinate_no_refit_max_e": max(no_refit),
        "single_coordinate_no_refit_min_e": min(no_refit),
        "boundary": "旧64点线性关系与新63点冻结坐标求根均为L2；不是全经线解析提升，也不证明该坐标在所有解分支上必要。",
        "raw_sha256": sha256(out_path),
        "seconds": time.time() - start,
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    (RUN / "ad23_s2_theta_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
