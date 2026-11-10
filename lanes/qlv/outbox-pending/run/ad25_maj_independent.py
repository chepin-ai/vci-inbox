"""AD-25 MAJ 独立验收：不导入构造器、分析模块或旧验收器。

从置换定义、AD-23整数角和AD-25保存的核心坐标重建全部电路；
96条逐一复算target与双割约束，不抄summary命中数。
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
R23 = R.parent.parent / "ad23/run"
I2 = np.eye(2, dtype=complex)
Z = np.diag([1, -1]).astype(complex)
A, B = (0, 1), (1, 2)
ORDERS = ["AABB", "ABAB", "ABBA", "BAAB", "BABA", "BBAA"]
CASES = [(np.pi/3, 0.), (np.pi/2, -2.), (np.pi/2, 2.), (2*np.pi/3, 0.)]


def bits(x):
    return [(x >> 2) & 1, (x >> 1) & 1, x & 1]


def code(b):
    return (b[0] << 2) | (b[1] << 1) | b[2]


def perm(fn):
    m = np.zeros((8, 8), dtype=int)
    for x in range(8):
        m[fn(x), x] = 1
    return m


def cnot(c, t):
    return perm(lambda x: code([bits(x)[q] ^ (bits(x)[c] if q == t else 0) for q in range(3)]))


def toffoli(controls, target):
    def fn(x):
        b = bits(x)
        if all(b[q] for q in controls):
            b[target] ^= 1
        return code(b)
    return perm(fn)


MAJ = toffoli({0, 2}, 1) @ cnot(1, 2) @ cnot(1, 0)


def rz(a):
    return np.diag([np.exp(-.5j*a), np.exp(.5j*a)])


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def cz(edge):
    return np.diag([-1 if bits(x)[edge[0]] and bits(x)[edge[1]] else 1 for x in range(8)]).astype(complex)


def circuit(p, edges):
    p = np.asarray(p, float)
    th = p[1:].reshape(len(edges)+1, 3, 3)
    layers = [np.kron(np.kron(su2(th[i, 0]), su2(th[i, 1])), su2(th[i, 2]))
              for i in range(len(edges)+1)]
    u = np.exp(1j*p[0])*layers[-1]
    for j in range(len(edges)-1, -1, -1):
        u = u @ cz(edges[j]) @ layers[j]
    return u


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


def unfold(m, q):
    others = [x for x in range(3) if x != q]
    a = np.zeros((4, 16), dtype=int)
    for out in range(8):
        for inn in range(8):
            bo, bi = bits(out), bits(inn)
            ro = (bo[others[0]] << 1) | bo[others[1]]
            ri = (bi[others[0]] << 1) | bi[others[1]]
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


def exact_known_gate():
    # 恒等秩1；单CZ跨割秩2；MAJ三割秩4及精确Gram谱。
    assert all(fraction_rank(unfold(np.eye(8, dtype=int), q)) == 1 for q in range(3))
    one = np.diag([-1 if bits(x)[0] and bits(x)[1] else 1 for x in range(8)])
    assert fraction_rank(unfold(one, 0)) == 2 and fraction_rank(unfold(one, 2)) == 1
    cuts = {}
    for q in range(3):
        a = unfold(MAJ, q)
        g = sp.Matrix(a.tolist())*sp.Matrix(a.tolist()).T
        assert fraction_rank(a) == 4
        assert g.eigenvals() == {sp.Integer(3): 2, sp.Integer(1): 2}
        cuts[f"q{q}|rest"] = {"rank": 4, "gram_spectrum": "{3,3,1,1}"}
    hits = json.loads((R23 / "ad23_maj_7cz_exact.json").read_text())["hits"]
    worst = 0.
    for h in hits:
        p = np.concatenate([[h["phase_pi_over_8"]*np.pi/8],
                            np.asarray(h["local_angles_pi_over_4"]).reshape(-1)*np.pi/4])
        worst = max(worst, float(np.max(abs(circuit(p, h["edges"])-MAJ))))
    assert len(hits) == 7 and worst < 2e-12
    return {"single_cuts": cuts, "ad23_7cz_hits": len(hits),
            "ad23_7cz_max_abs": worst}


def unpack_layers(p, edges):
    th = np.asarray(p)[1:].reshape(len(edges)+1, 3, 3)
    return [[su2(th[i, q]) for q in range(3)] for i in range(len(edges)+1)]


def middle(layers, edges, edge, cutq):
    pos = [i for i, e in enumerate(edges) if e == edge]
    assert len(pos) == 2
    i, j = pos
    rest = [q for q in range(3) if q != cutq]
    m = np.eye(2, dtype=complex)
    v = np.eye(4, dtype=complex)
    for l in range(i+1, j+1):
        m = layers[l][cutq] @ m
        v = np.kron(layers[l][rest[0]], layers[l][rest[1]]) @ v
        if l < j:
            assert edges[l] != edge
            v = np.diag([1, 1, 1, -1]).astype(complex) @ v
    b = 2*np.arctan2(abs(m[1, 0]), abs(m[0, 0]))
    zrest = np.kron(Z, I2) if cutq == 0 else np.kron(I2, Z)
    t = float(np.trace(v @ zrest @ v.conj().T @ zrest).real)
    return float(b), t


def verify_numeric_rows():
    rows = [json.loads(s) for s in (R / "ad25_maj_k4_constrained.jsonl").read_text().splitlines() if s.strip()]
    assert len(rows) == 96
    worst_target = worst_constraint = 0.
    per = {name: [] for name in ORDERS}
    for row in rows:
        assert "error" not in row
        name = row["order"]
        edges = [A if x == "A" else B for x in name]
        core = np.asarray(row["x_core"], float)
        p = expand(core, edges)
        target = float(np.max(abs(circuit(p, edges)-MAJ)))
        layers = unpack_layers(p, edges)
        ba, ta = middle(layers, edges, A, 0)
        bb, tb = middle(layers, edges, B, 2)
        ca, cb = CASES[row["case_A_index"]], CASES[row["case_B_index"]]
        cv = np.array([ba-ca[0], ta-ca[1], bb-cb[0], tb-cb[1]])
        ci = float(np.max(abs(cv)))
        worst_target = max(worst_target, abs(target-row["target_max_abs"]))
        worst_constraint = max(worst_constraint, abs(ci-row["constraint_inf"]))
        assert abs(target-row["target_max_abs"]) < 2e-9
        assert abs(ci-row["constraint_inf"]) < 2e-8, (name, ci, row["constraint_inf"])
        per[name].append({"target": target, "constraint": ci,
                          "joint": target < 1e-9 and ci < 1e-7})
    summary = {}
    for name, rr in per.items():
        assert len(rr) == 16
        summary[name] = {"runs": len(rr), "joint_hits": sum(x["joint"] for x in rr),
                         "best_target_rebuilt": min(x["target"] for x in rr),
                         "min_constraint_rebuilt": min(x["constraint"] for x in rr),
                         "max_constraint_rebuilt": max(x["constraint"] for x in rr)}
    assert sum(x["joint_hits"] for x in summary.values()) == 0
    return {"runs": len(rows), "per_order": summary,
            "max_target_rebuild_difference": worst_target,
            "max_constraint_rebuild_difference": worst_constraint,
            "exact_joint_hits": 0,
            "boundary": "只验收96条已跑电路及其坐标；未把暖启动盆未命中升级为六序或k=4不存在证明。"}


def main():
    gate = exact_known_gate()
    numeric = verify_numeric_rows()
    out = {"beat": "AD-25", "status": "MAJ_AD25_INDEPENDENT_L1_L2_PASS",
           "known_answer_gate_first": gate, "numeric96": numeric,
           "strict_interval": "4 <= k <= 7",
           "open": ["k=4六序解析排除或精确构造", "k=5/6更严下界或更小构造"],
           "private_ci_consumption": 0, "quantum_machine_consumption": 0}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_maj_independent.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": numeric["runs"],
                      "joint_hits": 0,
                      "max_target_rebuild_difference": numeric["max_target_rebuild_difference"],
                      "max_constraint_rebuild_difference": numeric["max_constraint_rebuild_difference"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
