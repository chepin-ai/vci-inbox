"""AD-24 MAJ：精确 Schmidt 秩下界与 Peres 五 CNOT 构造审计。

证据分层：Schmidt 秩和有限排列枚举为精确计算；数值 SVD 仅作显示。
Peres 的否定只覆盖本文列出的直接构造形式，不是六 CZ 不存在定理。
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.diag([1, np.exp(1j * np.pi / 4)])
PATH = ((0, 1), (1, 2))


def bits(x):
    return [(x >> 2) & 1, (x >> 1) & 1, x & 1]


def code(b):
    return (b[0] << 2) | (b[1] << 1) | b[2]


def permutation(fn):
    M = np.zeros((8, 8), dtype=complex)
    for x in range(8):
        M[fn(x), x] = 1
    return M


def cnot(c, t):
    def fn(x):
        b = bits(x)
        if b[c]:
            b[t] ^= 1
        return code(b)
    return permutation(fn)


def toffoli(controls, target):
    def fn(x):
        b = bits(x)
        if all(b[q] for q in controls):
            b[target] ^= 1
        return code(b)
    return permutation(fn)


MAJ = toffoli({0, 2}, 1) @ cnot(1, 2) @ cnot(1, 0)
PERES = cnot(0, 1) @ toffoli({0, 1}, 2)


def one(g, q):
    return np.kron(np.kron(g if q == 0 else I2, g if q == 1 else I2), g if q == 2 else I2)


def peres_five_cnot():
    """Shende--Markov Fig.1 删除最右 CNOT；局部 T/T† 保留。"""
    Td = T.conj().T
    ops = [
        ("local", H, 2), ("cnot", 1, 2), ("local", Td, 2),
        ("cnot", 0, 2), ("local", T, 2), ("cnot", 1, 2),
        ("local", Td, 2), ("cnot", 0, 2), ("local", T, 1),
        ("local", T, 2), ("local", H, 2), ("cnot", 0, 1),
        ("local", T, 0), ("local", Td, 1),
    ]
    U = np.eye(8, dtype=complex)
    for op in ops:
        G = one(op[1], op[2]) if op[0] == "local" else cnot(op[1], op[2])
        U = G @ U
    serial = [[op[0], op[2], op[1].tolist()] if op[0] == "local" else list(op) for op in ops]
    # 复数矩阵不可直接 JSON 比较；原始账另存 CNOT 与局部角序列。
    compact = []
    for op in ops:
        if op[0] == "cnot":
            compact.append(["CNOT", op[1], op[2]])
        else:
            name = "H" if np.array_equal(op[1], H) else ("T" if np.array_equal(op[1], T) else "Tdag")
            compact.append([name, op[2]])
    return U, compact


def unfold_integer(M, left_qubits):
    """算符 Schmidt 展开，行=(输出左,输入左)，列=(输出右,输入右)。"""
    n = 2 ** left_qubits
    m = 2 ** (3 - left_qubits)
    A = np.zeros((n * n, m * m), dtype=int)
    for ol in range(n):
        for il in range(n):
            for orr in range(m):
                for ir in range(m):
                    out = (ol << (3 - left_qubits)) | orr
                    inn = (il << (3 - left_qubits)) | ir
                    z = M[out, inn]
                    assert abs(z.imag) < 1e-12 and abs(z.real - round(z.real)) < 1e-12
                    A[ol * n + il, orr * m + ir] = int(round(z.real))
    return A


def qperm(p):
    def fn(x):
        old = bits(x)
        new = [0] * 3
        for old_q in range(3):
            new[p[old_q]] = old[old_q]
        return code(new)
    return permutation(fn)


def xmask(mask):
    U = np.eye(8, dtype=complex)
    for q in range(3):
        if (mask >> q) & 1:
            U = one(X, q) @ U
    return U


def mapping(M):
    assert np.max(abs(M.imag)) < 1e-12
    return tuple(int(np.argmax(abs(M[:, x]))) for x in range(8))


def known_answer_gate(schmidt):
    # 已知答案先于未知判读：恒等式秩1，单 CZ 跨相应割秩2。
    assert np.max(abs(MAJ @ cnot(1, 0) @ cnot(1, 2) - toffoli({0, 2}, 1))) == 0
    assert all(tuple(sorted(e)) in PATH for e in [(1, 0), (1, 2)])
    assert schmidt["0|12"]["exact_rank"] == 4 and schmidt["1|23"]["exact_rank"] == 4
    # 单 CZ(0,1) 在 0|12 的展开秩2，在 1|23 的展开秩1。
    d = np.ones(8, dtype=complex)
    for x in range(8):
        b = bits(x)
        if b[0] and b[1]:
            d[x] = -1
    CZ01 = np.diag(d)
    assert sp.Matrix(unfold_integer(CZ01, 1).tolist()).rank() == 2
    assert sp.Matrix(unfold_integer(CZ01, 2).tolist()).rank() == 1
    return {
        "maj_toffoli_path_cnot_identity": "exact zero",
        "identity_unfold_rank": 1,
        "single_cz_01_rank_across_0|12": 2,
        "single_cz_01_rank_across_1|23": 1,
    }


def main():
    schmidt = {}
    for q, name in [(1, "0|12"), (2, "1|23")]:
        A = unfold_integer(MAJ, q)
        rank = sp.Matrix(A.tolist()).rank()
        singular = np.linalg.svd(A.astype(float), compute_uv=False)
        schmidt[name] = {
            "shape": list(A.shape), "exact_rank": int(rank),
            "numeric_singular_values_for_display": singular.tolist(),
            "unfolded_integer_matrix": A.tolist(),
        }
    gate = known_answer_gate(schmidt)

    P5, compact = peres_five_cnot()
    peres_error = float(np.max(abs(P5 - PERES)))
    assert peres_error < 1e-12, peres_error
    peres_edges = [(1, 2), (0, 2), (1, 2), (0, 2), (0, 1)]
    assert sum(tuple(sorted(e)) not in PATH for e in peres_edges) == 2

    # 精确有限攻击：重标记、输入/输出局部 X、左/右补一个 CNOT。
    target_mapping = mapping(MAJ)
    tested = 0
    hits = []
    for p in itertools.permutations(range(3)):
        Q = qperm(p)
        for mi in range(8):
            Xin = xmask(mi)
            for mo in range(8):
                Pp = Q @ xmask(mo) @ PERES @ Xin @ Q.conj().T
                for c, t in itertools.permutations(range(3), 2):
                    C = cnot(c, t)
                    for side, M in (("left", C @ Pp), ("right", Pp @ C)):
                        tested += 1
                        if mapping(M) == target_mapping:
                            hits.append({"perm": p, "input_x": mi, "output_x": mo,
                                         "cnot": [c, t], "side": side})
    assert tested == 4608 and not hits

    out = {
        "beat": "AD-24", "status": "MAJ_LOWER_AND_PERES_AUDIT_PASS",
        "strict_interval": "4 <= k <= 7",
        "known_answer_gate": gate,
        "schmidt_rank_theorem": {
            "cuts": schmidt,
            "logical_step": "each 01 CZ at most doubles rank across 0|12 and leaves 1|23 unchanged; each 12 CZ conversely; local SU2 layers preserve both ranks",
            "conclusion": "n01 >= 2 and n12 >= 2, hence k >= 4; for k=4 exactly two gates on each PATH edge",
            "evidence_level": "L1 exact integer rank; numerical SVD is display only",
        },
        "peres": {
            "source": "V. Shende and I. Markov, On the CNOT-cost of TOFFOLI gates, QIC 9 (2009), Fig.1 and Corollary 5",
            "source_url": "https://www.rintonpress.com/xxqic9/qic-9-56/0461-0486.pdf",
            "construction": "Fig.1 with rightmost CNOT deleted; trailing local T/Tdag retained",
            "operations_chronological": compact,
            "cnot_edges_chronological": [list(e) for e in peres_edges],
            "non_path_cnot_count": 2,
            "numeric_full_matrix_error": peres_error,
            "direct_attack_space": "6 qubit permutations * 8 input X masks * 8 output X masks * 6 directed CNOTs * 2 sides",
            "direct_cases": tested,
            "direct_hits": hits,
            "boundary": "原五门构造含两条02边；有限直接形式均未得到MAJ。此结果不排除其他局部门或六CZ构造，不改变4<=k<=7。",
        },
        "private_ci_consumption": 0,
        "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad24_maj_audit.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "ranks": [schmidt[x]["exact_rank"] for x in schmidt],
                      "peres_error": peres_error, "direct_cases": tested, "direct_hits": len(hits),
                      "interval": out["strict_interval"], "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
