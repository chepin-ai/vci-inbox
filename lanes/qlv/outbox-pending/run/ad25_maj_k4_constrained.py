"""AD-25 MAJ k=4：六边序逐序双割等号约束暖启动攻击。

只复用 AD-22 每个边序自己的最佳原始候选，不做低起点扫描。
零命中只覆盖本序该暖启动盆与16个 b/t 分支，不是连续空间不存在证明。
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
sys.path.insert(0, str(R22))
import ad22_verify as base
sys.path.insert(0, str(R23))
import ad23_gauge as gauge

A, B = (0, 1), (1, 2)
I2 = np.eye(2, dtype=complex)
Z = np.diag([1, -1]).astype(complex)
ORDERS = ["AABB", "ABAB", "ABBA", "BAAB", "BABA", "BBAA"]
CASES = [(np.pi/3, 0.0), (np.pi/2, -2.0), (np.pi/2, 2.0), (2*np.pi/3, 0.0)]


def seq_edges(name):
    return [A if x == "A" else B for x in name]


def raw_indices(edges):
    ix = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            for off in (1, 2):
                ix.append(1 + (i*3+q)*3 + off)
    ix.extend(range(1+9*len(edges), 1+9*(len(edges)+1)))
    assert len(ix) == 4*len(edges)+10
    return ix


def expand(core, edges):
    p = np.zeros(1+9*(len(edges)+1))
    p[raw_indices(edges)] = core
    return p


def cz4():
    return np.diag([1, 1, 1, -1]).astype(complex)


def middle(L, edges, edge, cutq):
    pos = [i for i, e in enumerate(edges) if e == edge]
    assert len(pos) == 2
    i, j = pos
    rest = [q for q in range(3) if q != cutq]
    M = np.eye(2, dtype=complex)
    V = np.eye(4, dtype=complex)
    # 时间顺序：L_{i+1}, CZ_{i+1}, ..., L_j。
    for l in range(i+1, j+1):
        M = L[l][cutq] @ M
        V = np.kron(L[l][rest[0]], L[l][rest[1]]) @ V
        if l < j:
            assert edges[l] != edge
            V = cz4() @ V
    angles = gauge.zxz(M)
    Zrest = np.kron(Z, I2) if cutq == 0 else np.kron(I2, Z)
    t = float(np.trace(V @ Zrest @ V.conj().T @ Zrest).real)
    return float(angles[1]), t


def invariants(core, edges):
    _, L = gauge.unpack(expand(core, edges))
    return middle(L, edges, A, 0), middle(L, edges, B, 2)


def constraints(core, edges, ca, cb):
    (ba, ta), (bb, tb) = invariants(core, edges)
    return np.array([ba-ca[0], ta-ca[1], bb-cb[0], tb-cb[1]])


def target_fj(core, edges):
    f, J = base.residual_jacobian(expand(core, edges), edges, base.MAJ)
    return f, J[:, raw_indices(edges)]


def known_answer_gate():
    src = json.loads((R23 / "ad23_maj_7cz_exact.json").read_text())["hits"]
    worst = 0.0
    for h in src:
        p = np.concatenate([[h["phase_pi_over_8"]*np.pi/8],
                            np.asarray(h["local_angles_pi_over_4"]).reshape(-1)*np.pi/4])
        e = float(np.max(abs(base.circuit(p, h["edges"])-base.MAJ)))
        worst = max(worst, e)
    assert len(src) == 7 and worst < 2e-12
    h = src[4]
    edges = [tuple(e) for e in h["edges"]]
    p = np.concatenate([[h["phase_pi_over_8"]*np.pi/8],
                        np.asarray(h["local_angles_pi_over_4"]).reshape(-1)*np.pi/4])
    core = p[raw_indices(edges)]
    sol = least_squares(lambda c: target_fj(c, edges)[0], core,
                        jac=lambda c: target_fj(c, edges)[1], method="lm", max_nfev=100,
                        ftol=1e-14, xtol=1e-14, gtol=1e-14)
    e = float(np.max(abs(base.circuit(expand(sol.x, edges), edges)-base.MAJ)))
    assert e < 2e-12
    return {"exact_7cz_sources": len(src), "exact_7cz_max_abs": worst,
            "known_solver_max_abs": e}


def warm_starts():
    rows = [json.loads(s) for s in (R22 / "ad22_maj_multistart.jsonl").read_text().splitlines() if s.strip()]
    out = {}
    for name in ORDERS:
        edges = seq_edges(name)
        candidates = [r for r in rows if r.get("k") == 4 and "error" not in r and
                      [tuple(e) for e in r["edges"]] == edges]
        assert len(candidates) == 8, (name, len(candidates))
        best = min(candidates, key=lambda r: r["e"])
        p = np.asarray(best["x"], float)
        ph, L, meta = gauge.canonicalize(p, edges)
        pc = gauge.pack(ph, L)
        preserve = float(np.max(abs(base.circuit(pc, edges)-base.circuit(p, edges))))
        assert preserve < 2e-12
        core = pc[raw_indices(edges)]
        inv = invariants(core, edges)
        out[name] = {"core": core, "source_e": float(best["e"]),
                     "source_idx": best["idx"], "source_restart": best["restart"],
                     "initial_invariants": inv, "canonical_preservation": preserve}
    return out


def solve(task):
    name, ia, ib, core = task
    edges = seq_edges(name)
    ca, cb = CASES[ia], CASES[ib]
    weight = 10.0

    def fun(c):
        return np.concatenate([target_fj(c, edges)[0], weight*constraints(c, edges, ca, cb)])

    def jac(c):
        J = target_fj(c, edges)[1]
        h = 2e-6
        C = []
        for i in range(len(c)):
            d = np.zeros(len(c))
            d[i] = h
            C.append((constraints(c+d, edges, ca, cb)-constraints(c-d, edges, ca, cb))/(2*h))
        return np.vstack([J, weight*np.asarray(C).T])

    try:
        sol = least_squares(fun, np.asarray(core), jac=jac, method="lm", max_nfev=600,
                            ftol=1e-14, xtol=1e-14, gtol=1e-14)
        p = expand(sol.x, edges)
        e = float(np.max(abs(base.circuit(p, edges)-base.MAJ)))
        co = constraints(sol.x, edges, ca, cb)
        inv = invariants(sol.x, edges)
        return {"order": name, "case_A_index": ia, "case_B_index": ib,
                "case_A": [ca[0]/np.pi, ca[1]], "case_B": [cb[0]/np.pi, cb[1]],
                "target_max_abs": e, "constraint_inf": float(np.max(abs(co))),
                "constraint_vector": co.tolist(),
                "final_invariants": {"A": list(inv[0]), "B": list(inv[1])},
                "nfev": int(sol.nfev), "status": int(sol.status),
                "optimality": float(sol.optimality), "x_core": sol.x.tolist()}
    except Exception as exc:
        return {"order": name, "case_A_index": ia, "case_B_index": ib,
                "error": type(exc).__name__+": "+str(exc)}


def slim(row):
    keys = ["order", "case_A_index", "case_B_index", "case_A", "case_B",
            "target_max_abs", "constraint_inf", "nfev", "status", "optimality"]
    return {k: row[k] for k in keys if k in row}


def main():
    start = time.time()
    gate = known_answer_gate()  # 已知答案先于未知目标。
    warm = warm_starts()
    tasks = [(name, ia, ib, warm[name]["core"]) for name in ORDERS
             for ia in range(len(CASES)) for ib in range(len(CASES))]
    rows = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(solve, t): (t[0], t[1], t[2]) for t in tasks}
        for n, fut in enumerate(as_completed(futs), 1):
            key = futs[fut]
            try:
                rows.append(fut.result())
            except Exception as exc:
                rows.append({"order": key[0], "case_A_index": key[1], "case_B_index": key[2],
                             "error": type(exc).__name__+": "+str(exc)})
            if n % 16 == 0:
                print(json.dumps({"done": n, "total": len(tasks), "elapsed": time.time()-start}), flush=True)
    rows.sort(key=lambda r: (ORDERS.index(r["order"]), r["case_A_index"], r["case_B_index"]))
    raw_lines = "".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows)
    (R / "ad25_maj_k4_constrained.jsonl").write_text(raw_lines)

    per = {}
    for name in ORDERS:
        rr = [r for r in rows if r["order"] == name and "error" not in r]
        assert len(rr) == 16
        best = min(rr, key=lambda r: r["target_max_abs"])
        near = [r for r in rr if r["constraint_inf"] < 1e-2]
        best_near = min(near, key=lambda r: r["target_max_abs"]) if near else None
        hits = [r for r in rr if r["target_max_abs"] < 1e-9 and r["constraint_inf"] < 1e-7]
        per[name] = {
            "source_best_e": warm[name]["source_e"],
            "source_idx": warm[name]["source_idx"], "source_restart": warm[name]["source_restart"],
            "initial_invariants": {"A": list(warm[name]["initial_invariants"][0]),
                                   "B": list(warm[name]["initial_invariants"][1])},
            "runs": len(rr), "exact_joint_hits": len(hits),
            "best_target": slim(best),
            "best_target_with_constraint_inf_lt_1e-2": slim(best_near) if best_near else None,
            "max_constraint_inf": max(r["constraint_inf"] for r in rr),
            "min_constraint_inf": min(r["constraint_inf"] for r in rr),
        }
    hits = sum(v["exact_joint_hits"] for v in per.values())
    out = {
        "beat": "AD-25",
        "status": "MAJ_K4_SIX_ORDER_CONSTRAINED_NUMERIC_COMPLETE",
        "known_answer_gate_first": gate,
        "protocol": "each order uses only its own AD-22 best raw candidate; canonical 26-core; 4x4 b/t cases; weight=10; max_nfev=600",
        "runs": len(rows), "errors": sum("error" in r for r in rows),
        "per_order": per, "exact_joint_hits": hits,
        "evidence_level": "L2 targeted local numerical falsification only",
        "boundary": "每序仅覆盖AD-22本序最佳候选的暖启动盆及16个等号分支；任何零命中均不证明该边序或k=4全局不存在。六序解析排除仍开放。",
        "strict_interval": "4 <= k <= 7",
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_maj_k4_constrained_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "exact_joint_hits": hits,
                      "per_order_best": {k: v["best_target"]["target_max_abs"] for k, v in per.items()},
                      "seconds": time.time()-start,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
