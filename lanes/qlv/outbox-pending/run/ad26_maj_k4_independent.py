"""AD-26 MAJ k=4 独立重建验收。

不导入 AD-22/23/25/26 的求解或分析模块。输入仅为原始 JSON 坐标。
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
R22 = R.parent.parent/"ad22/run"
R23 = R.parent.parent/"ad23/run"
A, B = (0, 1), (1, 2)
ORDERS = ("ABAB", "ABBA", "BABA")
CASES = ((np.pi/3, 0.0), (np.pi/2, -2.0), (np.pi/2, 2.0), (2*np.pi/3, 0.0))
FIXED = {"ABAB": ("B", 1), "ABBA": ("A", 2), "BABA": ("A", 1)}
SOURCE = {"ABAB": (5, 7), "ABBA": (6, 1), "BABA": (10, 6)}
I2 = np.eye(2, dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def bits(x):
    return [(x>>2)&1, (x>>1)&1, x&1]


def code(b):
    return (b[0]<<2)|(b[1]<<1)|b[2]


def permutation(fn):
    m = np.zeros((8, 8), dtype=int)
    for x in range(8):
        m[fn(x), x] = 1
    return m


def cnot(c, t):
    return permutation(lambda x: code([bits(x)[q]^(bits(x)[c] if q == t else 0) for q in range(3)]))


def toffoli(controls, target):
    def fn(x):
        b = bits(x)
        if all(b[q] for q in controls):
            b[target] ^= 1
        return code(b)
    return permutation(fn)


MAJ = toffoli({0, 2}, 1)@cnot(1, 2)@cnot(1, 0)


def rz(a):
    return np.diag([np.exp(-0.5j*a), np.exp(0.5j*a)])


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], complex)


def su2(t):
    return rz(t[0])@ry(t[1])@rz(t[2])


def cz(edge):
    return np.diag([-1 if bits(x)[edge[0]] and bits(x)[edge[1]] else 1 for x in range(8)]).astype(complex)


def circuit(p, edges):
    p = np.asarray(p, float)
    k = len(edges)
    assert len(p) == 1+9*(k+1)
    th = p[1:].reshape(k+1, 3, 3)
    u = np.exp(1j*p[0])*np.kron(np.kron(su2(th[-1, 0]), su2(th[-1, 1])), su2(th[-1, 2]))
    for j in range(k-1, -1, -1):
        local = np.kron(np.kron(su2(th[j, 0]), su2(th[j, 1])), su2(th[j, 2]))
        u = u@cz(edges[j])@local
    return u


def seq_edges(name):
    return [A if x == "A" else B for x in name]


def raw_indices(edges):
    ans = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            ans += [1+(i*3+q)*3+1, 1+(i*3+q)*3+2]
    ans += list(range(1+9*len(edges), 1+9*(len(edges)+1)))
    assert len(ans) == 26
    return ans


def expand(core, edges):
    p = np.zeros(1+9*(len(edges)+1))
    p[raw_indices(edges)] = core
    return p


def middle(layers, edges, edge, cutq):
    i, j = [n for n, e in enumerate(edges) if e == edge]
    rest = [q for q in range(3) if q != cutq]
    one = np.eye(2, dtype=complex)
    two = np.eye(4, dtype=complex)
    for l in range(i+1, j+1):
        one = layers[l][cutq]@one
        two = np.kron(layers[l][rest[0]], layers[l][rest[1]])@two
        if l < j:
            assert edges[l] != edge
            two = np.diag([1, 1, 1, -1]).astype(complex)@two
    b = 2*np.arctan2(abs(one[1, 0]), abs(one[0, 0]))
    zrest = np.kron(Z, I2) if cutq == 0 else np.kron(I2, Z)
    t = float(np.trace(two@zrest@two.conj().T@zrest).real)
    return float(b), t


def invariants_full(p, edges):
    th = np.asarray(p)[1:].reshape(len(edges)+1, 3, 3)
    layers = [[su2(th[i, q]) for q in range(3)] for i in range(len(edges)+1)]
    return {"A": middle(layers, edges, A, 0), "B": middle(layers, edges, B, 2)}


def constraint_vector(core, edges, name, free_index):
    inv = invariants_full(expand(core, edges), edges)
    fixed_cut, fixed_index = FIXED[name]
    free_cut = "A" if fixed_cut == "B" else "B"
    ans = []
    for cut, case in ((fixed_cut, CASES[fixed_index]), (free_cut, CASES[free_index])):
        ans += [inv[cut][0]-case[0], inv[cut][1]-case[1]]
    return np.asarray(ans)


def unfold(m, q):
    others = [x for x in range(3) if x != q]
    a = np.zeros((4, 16), dtype=int)
    for out in range(8):
        for inn in range(8):
            bo, bi = bits(out), bits(inn)
            ro = (bo[others[0]]<<1)|bo[others[1]]
            ri = (bi[others[0]]<<1)|bi[others[1]]
            a[2*bo[q]+bi[q], 4*ro+ri] = int(m[out, inn])
    return a


def fraction_rank(a):
    a = [[Fraction(int(x)) for x in row] for row in a]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        z = a[rank][col]
        a[rank] = [x/z for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col] != 0:
                z = a[i][col]
                a[i] = [x-z*y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def known_gate():
    cuts = {}
    for q in range(3):
        a = unfold(MAJ, q)
        gram = sp.Matrix(a.tolist())*sp.Matrix(a.tolist()).T
        assert fraction_rank(a) == 4
        assert gram.eigenvals() == {sp.Integer(3): 2, sp.Integer(1): 2}
        cuts[f"q{q}|rest"] = {"rank": 4, "gram": "{3,3,1,1}"}
    hits = json.loads((R23/"ad23_maj_7cz_exact.json").read_text())["hits"]
    worst = 0.0
    for h in hits:
        p = np.concatenate([[h["phase_pi_over_8"]*np.pi/8],
                            np.asarray(h["local_angles_pi_over_4"]).reshape(-1)*np.pi/4])
        worst = max(worst, float(np.max(abs(circuit(p, h["edges"])-MAJ))))
    assert len(hits) == 7 and worst < 2e-12
    return {"single_cuts": cuts, "ad23_7cz_hits": len(hits), "ad23_7cz_max_abs": worst}


def verify_sources():
    rows = [json.loads(s) for s in (R22/"ad22_maj_multistart.jsonl").read_text().splitlines() if s.strip()]
    out = {}
    for name in ORDERS:
        idx, restart = SOURCE[name]
        found = [r for r in rows if r.get("k") == 4 and r.get("idx") == idx and r.get("restart") == restart]
        assert len(found) == 1
        r = found[0]
        edges = [tuple(e) for e in r["edges"]]
        assert edges == seq_edges(name)
        e = float(np.max(abs(circuit(r["x"], edges)-MAJ)))
        assert abs(e-r["e"]) < 2e-9
        inv = invariants_full(r["x"], edges)
        cut, ci = FIXED[name]
        err = max(abs(inv[cut][0]-CASES[ci][0]), abs(inv[cut][1]-CASES[ci][1]))
        assert err < 1e-5, (name, err, inv)
        out[name] = {"source_idx": idx, "source_restart": restart, "target_max_abs": e,
                     "fixed_cut": cut, "fixed_case_index": ci, "fixed_branch_error": err,
                     "invariants": inv}
    return out


def verify_branch(rows, source_summary):
    assert len(rows) == 24
    max_e = max_c = 0.0
    per = {}
    for r in rows:
        assert "error" not in r
        name = r["order"]
        edges = seq_edges(name)
        core = np.asarray(r["x_core"], float)
        e = float(np.max(abs(circuit(expand(core, edges), edges)-MAJ)))
        cv = constraint_vector(core, edges, name, r["free_case_index"])
        ci = float(np.max(abs(cv)))
        max_e = max(max_e, abs(e-r["target_max_abs"]))
        max_c = max(max_c, abs(ci-r["constraint_inf"]))
        assert abs(e-r["target_max_abs"]) < 2e-9
        assert abs(ci-r["constraint_inf"]) < 2e-8
        assert bool(e < 1e-9 and ci < 1e-7) == r["exact_joint_hit"]
        per.setdefault(name, []).append((e, ci))
    summary = {n: {"runs": len(v), "constraint_closed": sum(ci < 1e-7 for e, ci in v),
                   "exact_joint_hits": sum(e < 1e-9 and ci < 1e-7 for e, ci in v),
                   "best_target": min(e for e, ci in v if ci < 1e-7)} for n, v in per.items()}
    gate_rows = source_summary["known_answer_gate_first"]["branch_continuation"]["self_target_recovery"]
    gate_worst_e = gate_worst_c = 0.0
    for g in gate_rows:
        name = g["order"]
        edges = seq_edges(name)
        source = np.asarray(g["source_core"], float)
        recovered = np.asarray(g["recovered_x_core"], float)
        target = circuit(expand(source, edges), edges)
        e = float(np.max(abs(circuit(expand(recovered, edges), edges)-target)))
        sinv = invariants_full(expand(source, edges), edges)
        rinv = invariants_full(expand(recovered, edges), edges)
        cut, _ = FIXED[name]
        free = "A" if cut == "B" else "B"
        cv = np.array([rinv[cut][0]-sinv[cut][0], rinv[cut][1]-sinv[cut][1],
                       rinv[free][0]-sinv[free][0], rinv[free][1]-sinv[free][1]])
        c = float(np.max(abs(cv)))
        gate_worst_e, gate_worst_c = max(gate_worst_e, e), max(gate_worst_c, c)
        assert e < 2e-8 and c < 2e-7, (name, e, c)
    return {"runs": len(rows), "per_order": summary, "max_target_rebuild_difference": max_e,
            "max_constraint_rebuild_difference": max_c,
            "exact_joint_hits": sum(v["exact_joint_hits"] for v in summary.values()),
            "known_self_target_gate": {"runs": len(gate_rows), "worst_target": gate_worst_e,
                                       "worst_constraint": gate_worst_c}}


def metric_difference(actual, saved):
    return abs(actual-saved)


def verify_direct(rows, summary):
    assert len(rows) == 24
    max_e = max_c = 0.0
    per = {}
    for r in rows:
        assert "error" not in r
        name = r["order"]
        edges = seq_edges(name)
        for prefix, xkey in (("closure", "closure_x_core"), ("final", "x_core")):
            core = np.asarray(r[xkey], float)
            e = float(np.max(abs(circuit(expand(core, edges), edges)-MAJ)))
            cv = constraint_vector(core, edges, name, r["free_case_index"])
            ci = float(np.max(abs(cv)))
            max_e = max(max_e, abs(e-r[prefix]["target_max_abs"]))
            max_c = max(max_c, abs(ci-r[prefix]["constraint_inf"]))
            assert abs(e-r[prefix]["target_max_abs"]) < 2e-9
            assert abs(ci-r[prefix]["constraint_inf"]) < 2e-8
            if prefix == "closure":
                assert ci < 2e-7
            else:
                assert bool(e < 1e-9 and ci < 1e-7) == r["exact_joint_hit"]
                per.setdefault(name, []).append((e, ci))
    # 已知答案门：source_core 自身电路是已知目标，恢复坐标必须重建该目标。
    gate_rows = summary["known_answer_gate_first"]["self_target_recovery"]
    gate_worst_e = gate_worst_c = 0.0
    for g in gate_rows:
        name = g["order"]
        edges = seq_edges(name)
        source = np.asarray(g["source_core"], float)
        target = circuit(expand(source, edges), edges)
        final = np.asarray(g["final_x_core"], float)
        e = float(np.max(abs(circuit(expand(final, edges), edges)-target)))
        inv = invariants_full(expand(final, edges), edges)
        cut, ci = FIXED[name]
        free = "A" if cut == "B" else "B"
        source_inv = invariants_full(expand(source, edges), edges)
        fc = source_inv[cut]  # 自身已知目标门使用原电路实测双割，而非吸附后的允许分支。
        cv = np.array([inv[cut][0]-fc[0], inv[cut][1]-fc[1],
                       inv[free][0]-source_inv[free][0], inv[free][1]-source_inv[free][1]])
        c = float(np.max(abs(cv)))
        gate_worst_e = max(gate_worst_e, e)
        gate_worst_c = max(gate_worst_c, c)
        assert e < 2e-8 and c < 2e-7, (name, e, c)
    rebuilt = {n: {"runs": len(v), "exact_joint_hits": sum(e < 1e-9 and ci < 1e-7 for e, ci in v),
                   "best_final_target": min(e for e, ci in v if ci < 1e-7)} for n, v in per.items()}
    # 改角反例。
    r = rows[0]
    x = np.asarray(r["x_core"], float)
    x[1] += np.pi/8
    counter = float(np.max(abs(circuit(expand(x, seq_edges(r["order"])), seq_edges(r["order"]))-MAJ)))
    assert counter > 1e-4
    return {"runs": len(rows), "per_order": rebuilt, "max_target_rebuild_difference": max_e,
            "max_constraint_rebuild_difference": max_c,
            "exact_joint_hits": sum(v["exact_joint_hits"] for v in rebuilt.values()),
            "known_self_target_gate": {"runs": len(gate_rows), "worst_target": gate_worst_e,
                                       "worst_constraint": gate_worst_c},
            "changed_angle_counterexample_max_abs": counter}


def main():
    gate = known_gate()
    sources = verify_sources()
    branch_rows = [json.loads(s) for s in (R/"ad26_maj_k4_branch.jsonl").read_text().splitlines() if s.strip()]
    direct_rows = [json.loads(s) for s in (R/"ad26_maj_k4_direct.jsonl").read_text().splitlines() if s.strip()]
    branch_summary = json.loads((R/"ad26_maj_k4_branch_summary.json").read_text())
    direct_summary = json.loads((R/"ad26_maj_k4_direct_summary.json").read_text())
    branch = verify_branch(branch_rows, branch_summary)
    direct = verify_direct(direct_rows, direct_summary)
    out = {"beat": "AD-26", "status": "MAJ_K4_BRANCH_DIRECT_INDEPENDENT_REBUILD_PASS",
           "known_answer_gate_first": gate, "source_rebuild": sources,
           "weighted_continuation": branch, "direct_continuation": direct,
           "combined_protocol_runs": branch["runs"]+direct["runs"],
           "combined_exact_joint_hits": branch["exact_joint_hits"]+direct["exact_joint_hits"],
           "evidence_level": "L1 exact known gates + L2 independent numerical rebuild of saved circuits",
           "boundary": "独立验收只证明所保存电路的矩阵与约束读数及已知门有效；未把48条终态零命中升级为六序或k=4不存在证明。",
           "strict_interval": "4 <= k <= 7", "private_ci_consumption": 0,
           "quantum_machine_actual_consumption_seconds": 0, "quantum_machine_launched": False,
           "quantum_account_quota_verified": False}
    assert out["combined_exact_joint_hits"] == 0
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/"ad26_maj_k4_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "combined_protocol_runs": out["combined_protocol_runs"],
                      "combined_exact_joint_hits": out["combined_exact_joint_hits"],
                      "weighted_max_target_delta": branch["max_target_rebuild_difference"],
                      "direct_max_target_delta": direct["max_target_rebuild_difference"],
                      "known_gate": direct["known_self_target_gate"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
