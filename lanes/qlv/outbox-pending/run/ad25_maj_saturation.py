"""AD-25 MAJ：三个单比特割精确饱和与 k=4 双 CZ 等号引理。

不读取任何分析中间矩阵；MAJ 从原始置换定义重建。
秩与 Gram 谱为精确 L1；随机酉测试仅交叉检查解析公式，不承担证明。
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def bits(x):
    return [(x >> 2) & 1, (x >> 1) & 1, x & 1]


def code(b):
    return (b[0] << 2) | (b[1] << 1) | b[2]


def perm(fn):
    M = np.zeros((8, 8), dtype=int)
    for x in range(8):
        M[fn(x), x] = 1
    return M


def cnot(c, t):
    def f(x):
        b = bits(x)
        if b[c]:
            b[t] ^= 1
        return code(b)
    return perm(f)


def toffoli(controls, target):
    def f(x):
        b = bits(x)
        if all(b[q] for q in controls):
            b[target] ^= 1
        return code(b)
    return perm(f)


MAJ = toffoli({0, 2}, 1) @ cnot(1, 2) @ cnot(1, 0)


def unfold_single(M, q):
    """左=q，右=其余位按原标签升序；返回 4x16 整数算符展开。"""
    others = [x for x in range(3) if x != q]
    A = np.zeros((4, 16), dtype=int)
    for out in range(8):
        for inn in range(8):
            bo, bi = bits(out), bits(inn)
            ro = (bo[others[0]] << 1) | bo[others[1]]
            ri = (bi[others[0]] << 1) | bi[others[1]]
            z = M[out, inn]
            assert isinstance(z, (int, np.integer))
            A[2 * bo[q] + bi[q], 4 * ro + ri] = int(z)
    return A


def fraction_rank(A):
    A = [[Fraction(int(x)) for x in row] for row in A]
    nr, nc = len(A), len(A[0])
    rank = 0
    for col in range(nc):
        pivot = next((i for i in range(rank, nr) if A[i][col] != 0), None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        z = A[rank][col]
        A[rank] = [x / z for x in A[rank]]
        for i in range(nr):
            if i != rank and A[i][col] != 0:
                z = A[i][col]
                A[i] = [x - z * y for x, y in zip(A[i], A[rank])]
        rank += 1
        if rank == nr:
            break
    return rank


def known_answer_gate():
    ident = np.eye(8, dtype=int)
    assert all(fraction_rank(unfold_single(ident, q)) == 1 for q in range(3))
    CZ01 = np.diag([-1 if (bits(x)[0] and bits(x)[1]) else 1 for x in range(8)])
    CZ12 = np.diag([-1 if (bits(x)[1] and bits(x)[2]) else 1 for x in range(8)])
    ranks = {
        "CZ01_q0": fraction_rank(unfold_single(CZ01, 0)),
        "CZ01_q2": fraction_rank(unfold_single(CZ01, 2)),
        "CZ12_q2": fraction_rank(unfold_single(CZ12, 2)),
        "CZ12_q0": fraction_rank(unfold_single(CZ12, 0)),
    }
    assert ranks == {"CZ01_q0": 2, "CZ01_q2": 1, "CZ12_q2": 2, "CZ12_q0": 1}
    # 任一 Z-对易两块形式的已知答案：该割秩至多 2。
    controlled = perm(lambda x: code([bits(x)[0], bits(x)[1], bits(x)[2] ^ (bits(x)[0] and bits(x)[1])]))
    assert fraction_rank(unfold_single(controlled, 0)) <= 2
    return {"identity_rank_each_cut": 1, "single_cz_ranks": ranks,
            "z_commuting_controlled_form_rank": fraction_rank(unfold_single(controlled, 0))}


def exact_cuts():
    out = {}
    for q in range(3):
        A = unfold_single(MAJ, q)
        rank = fraction_rank(A)
        G = sp.Matrix(A.tolist()) * sp.Matrix(A.tolist()).T
        ev = G.eigenvals()
        assert rank == 4 and ev == {sp.Integer(3): 2, sp.Integer(1): 2}, (q, rank, ev)
        assert sum(int(k) * int(v) for k, v in ev.items()) == 8
        out[f"q{q}|rest"] = {
            "shape": list(A.shape), "rank": rank,
            "gram_eigenvalues_with_multiplicity": {str(k): int(v) for k, v in ev.items()},
            "schmidt_coefficients": ["sqrt(3)", "sqrt(3)", "1", "1"],
            "unfolded_integer_matrix": A.tolist(),
        }
    return out


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], complex)


def numeric_unfold(U, q=0):
    others = [x for x in range(3) if x != q]
    A = np.zeros((4, 16), complex)
    for out in range(8):
        for inn in range(8):
            bo, bi = bits(out), bits(inn)
            ro = (bo[others[0]] << 1) | bo[others[1]]
            ri = (bi[others[0]] << 1) | bi[others[1]]
            A[2*bo[q]+bi[q], 4*ro+ri] = U[out, inn]
    return A


def canonical_matrix(b, V):
    C = np.kron(np.diag([1, 1, 1, -1]), I2)
    return C @ np.kron(ry(b), V) @ C


def canonical_spectrum(b, V):
    U = canonical_matrix(b, V)
    actual = np.linalg.svd(numeric_unfold(U, 0), compute_uv=False) ** 2
    ZZ = np.kron(Z, I2)
    t = float(np.trace(V @ ZZ @ V.conj().T @ ZZ).real)
    c, s = np.cos(b/2)**2, np.sin(b/2)**2
    predicted = np.sort([c*(4+t), c*(4-t), s*(4+t), s*(4-t)])[::-1]
    return actual, predicted, t


def equality_lemma():
    # 解析 Gram 矩阵：c2=cos²(b/2), s2=sin²(b/2), t=Tr(V Z1 V† Z1)。
    c2, s2, t = sp.symbols("c2 s2 t", real=True)
    G = sp.Matrix([[4*c2, 0, 0, c2*t],
                   [0, 4*s2, -s2*t, 0],
                   [0, -s2*t, 4*s2, 0],
                   [c2*t, 0, 0, 4*c2]])
    # 分成两个 2x2 块，精确核对四个特征值。
    blocks = [G[[0, 3], [0, 3]], G[[1, 2], [1, 2]]]
    ev0 = {sp.expand(k): v for k, v in blocks[0].eigenvals().items()}
    ev1 = {sp.expand(k): v for k, v in blocks[1].eigenvals().items()}
    assert ev0 == {sp.expand(c2*(4+t)): 1, sp.expand(c2*(4-t)): 1}
    assert ev1 == {sp.expand(s2*(4+t)): 1, sp.expand(s2*(4-t)): 1}
    witnesses = []
    for name, b, a in (("t0_c2_3over4", np.pi/3, np.pi/2),
                       ("tabs2_c2_1over2", np.pi/2, np.pi/3)):
        V = np.kron(ry(a), I2)
        actual, predicted, tv = canonical_spectrum(b, V)
        err = float(np.max(abs(actual-predicted)))
        target_err = float(np.max(abs(actual-np.array([3, 3, 1, 1]))))
        assert err < 2e-12 and target_err < 2e-12
        witnesses.append({"case": name, "b_over_pi": b/np.pi, "V": f"Ry({a/np.pi}*pi)_1 tensor I_2",
                          "t": tv, "squared_schmidt": actual.tolist(),
                          "formula_error": err, "target_spectrum_error": target_err})
    rng = np.random.default_rng(250025)
    worst = 0.0
    for _ in range(8):
        Q, RR = np.linalg.qr(rng.normal(size=(4, 4)) + 1j*rng.normal(size=(4, 4)))
        Q = Q @ np.diag(np.diag(RR) / abs(np.diag(RR)))
        b = float(rng.uniform(0.05, np.pi-0.05))
        actual, predicted, tv = canonical_spectrum(b, Q)
        worst = max(worst, float(np.max(abs(actual-predicted))))
    assert worst < 2e-11
    return {
        "reduction": "two cross-cut CZ imply local equivalence to CZ (Ry(b) tensor V) CZ by ZYZ and commuting outer Rz through CZ",
        "gram_eigenvalues": ["c2*(4+t)", "c2*(4-t)", "s2*(4+t)", "s2*(4-t)"],
        "definitions": "c2=cos(b/2)^2; s2=sin(b/2)^2; c2+s2=1; t=Tr(V Z_1 V^dagger Z_1)",
        "target_spectrum_consequences": [
            {"b": "pi/3 or 2*pi/3", "t": "0"},
            {"b": "pi/2", "t": "+2 or -2"},
        ],
        "allowed_b": ["pi/3", "pi/2", "2*pi/3"],
        "explicit_witnesses": witnesses,
        "random_unitary_crosscheck": {"cases": 8, "max_spectrum_formula_error": worst},
        "scope_boundary": "必要等号条件；两个显式见证说明该谱本身不排除 k=4，也不提高下界。",
    }


def edge_order_classes():
    rows = []
    for seq in itertools.product("AB", repeat=4):
        if seq.count("A") != 2:
            continue
        name = "".join(seq)
        pa = [i for i, x in enumerate(seq) if x == "A"]
        pb = [i for i, x in enumerate(seq) if x == "B"]
        ia = sum(x == "B" for x in seq[pa[0]+1:pa[1]])
        ib = sum(x == "A" for x in seq[pb[0]+1:pb[1]])
        rows.append({"order": name, "A_positions": pa, "B_positions": pb,
                     "opposite_cz_between_A": ia, "opposite_cz_between_B": ib,
                     "class": {(0, 0): "adjacent-pair", (1, 1): "alternating"}.get((ia, ib), "nested")})
    assert len(rows) == 6
    return rows


def main():
    gate = known_answer_gate()  # 已知答案先于未知目标。
    cuts = exact_cuts()
    lemma = equality_lemma()
    orders = edge_order_classes()
    out = {
        "beat": "AD-25",
        "status": "MAJ_SINGLE_CUT_SATURATION_AND_TWO_CZ_EQUALITY_L1_PASS",
        "known_answer_gate_first": gate,
        "single_qubit_cuts": cuts,
        "local_z_commutation_obstruction": {
            "lemma": "若算符与某位 Z 对易，则该位单割算符 Schmidt 秩至多2；左右局部酉保持秩。MAJ三个单割秩均4，故不能经左右局部酉化成任一单比特 Z-对易两块形式。",
            "consequence": "Shende–Markov Definition 16–Theorem 18 的 mux-spectrum 不能直接以 MAJ 本身作为 Z-对易 P 使用；不清中期中间块或辅助位路线。",
            "not_claimed": "不排除 k=4，也不宣称所有 demultiplexing/偏行列式证明技术失效。",
        },
        "two_cz_equality_lemma": lemma,
        "k4_six_edge_orders": orders,
        "k5_k6_touch_patterns": {
            "k5": [[2, 3], [3, 2]],
            "k6": [[2, 4], [3, 3], [4, 2]],
            "notation": "[n01,n12]; 单割秩仅给出 n01>=2,n12>=2",
        },
        "strict_result": "MAJ三个单比特割均为秩4、谱(sqrt3,sqrt3,1,1)；k=4两割均为双CZ等号情形，新增b/t必要条件。严格区间仍4<=k<=7。",
        "open_boundaries": [
            "六边序尚未解析排除或构造；等号谱条件有显式见证，不能当作不存在证明。",
            "k=5/6未改善；k=4仍是唯一可能取得新下界或更小构造的边界。",
            "mux-spectrum直接迁移受阻不等于相关文献方法全部不可用。",
        ],
        "private_ci_consumption": 0,
        "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad25_maj_saturation.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "ranks": {k: v["rank"] for k, v in cuts.items()},
                      "allowed_b": lemma["allowed_b"], "six_orders": [x["order"] for x in orders],
                      "formula_crosscheck_max": lemma["random_unitary_crosscheck"]["max_spectrum_formula_error"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
