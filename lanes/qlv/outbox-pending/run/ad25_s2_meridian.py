"""AD-25 S²：由 AD-24 精确端点构造 11-CZ 全 S² 解析电路。

证据分层：
L1 = 精确端点 + 符号 W 分解/对易/共轭恒等式 + 首末 SU(2) 吸收。
L2 = 从原始整数角独立重建的数值全矩阵网格。
消门扫描只覆盖被测相邻 CZ 局部抵消，不是全局不存在证明。
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
SRC = R.parent.parent / "ad24/run/ad24_s2_exact.json"
EX = R.parent.parent / "ad23/run/ad23_exact.py"
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
CZ4 = np.diag([1, 1, 1, -1]).astype(complex)
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
ALPHA = np.pi / 8


def rz(a):
    return np.diag([np.exp(-0.5j * a), np.exp(0.5j * a)])


def ry(a):
    return np.array([[np.cos(a / 2), -np.sin(a / 2)], [np.sin(a / 2), np.cos(a / 2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def rp(t, P):
    return np.cos(t / 2) * I2 + 1j * np.sin(t / 2) * P


def op(q, A):
    ms = [I2, I2, I2]
    ms[q] = A
    return np.kron(np.kron(ms[0], ms[1]), ms[2])


def layer(ms):
    return np.kron(np.kron(ms[0], ms[1]), ms[2])


def cz(edge):
    a, b = edge
    d = np.ones(8, complex)
    for x in range(8):
        bits = [(x >> 2) & 1, (x >> 1) & 1, x & 1]
        if bits[a] and bits[b]:
            d[x] = -1
    return np.diag(d)


def angles_of_su2(U):
    U = np.asarray(U, complex)
    assert abs(np.linalg.det(U) - 1) < 2e-10
    if abs(U[1, 0]) < 1e-10:
        # 对角 SU(2)：保留 2pi 分支，尤其 U=-I。
        out = np.array([-2 * np.angle(U[0, 0]), 0.0, 0.0])
    elif abs(U[0, 0]) < 1e-10:
        # b=pi 时只有 a-c 可观测，取 c=0。
        out = np.array([2 * np.angle(U[1, 0]), np.pi, 0.0])
    else:
        b = 2 * np.arctan2(abs(U[1, 0]), abs(U[0, 0]))
        a = np.angle(U[1, 0]) - np.angle(U[0, 0])
        cc = np.angle(-U[0, 1]) - np.angle(U[0, 0])
        out = np.array([a, b, cc])
        # 主值角可能给出 -U；c 增加 2pi 精确翻转 SU(2) 整体符号。
        if np.max(abs(su2(out) + U)) < 2e-8:
            out[2] += 2 * np.pi
    assert np.max(abs(su2(out) - U)) < 2e-8, (U, out, su2(out))
    return out


def normalize_u2_layers(raw):
    """把每个 U(2) 因子写成标量×SU(2)，标量全部进入总相位。"""
    phase = 1 + 0j
    angles = []
    mats = []
    for q in range(3):
        G = raw[q]
        p = np.exp(0.5j * np.angle(np.linalg.det(G)))
        S = G / p
        assert abs(np.linalg.det(S) - 1) < 2e-10
        phase *= p
        mats.append(S)
        angles.append(angles_of_su2(S))
    return phase, np.asarray(angles), mats


def circuit(phase, angles, edges):
    angles = np.asarray(angles, float)
    k = len(edges)
    assert angles.shape == (k + 1, 3, 3)
    U = np.exp(1j * phase) * layer([su2(angles[-1, q]) for q in range(3)])
    for j in range(k - 1, -1, -1):
        U = U @ cz(edges[j]) @ layer([su2(angles[j, q]) for q in range(3)])
    return U


def toffoli(controls, target):
    T = np.zeros((8, 8), complex)
    for x in range(8):
        b = [(x >> 2) & 1, (x >> 1) & 1, x & 1]
        if all(b[q] for q in controls):
            b[target] ^= 1
        T[(b[0] << 2) | (b[1] << 1) | b[2], x] = 1
    return T


TG2 = toffoli({0, 2}, 1)


def pm(name):
    return np.kron(np.kron(PAULI[name[0]], PAULI[name[1]]), PAULI[name[2]])


def sphere(theta, phi):
    names = ["ZXZ", "ZIZ", "YIZ", "XIZ", "YXZ", "XXZ"]
    u = (1 + np.cos(theta)) / 2
    v = (np.cos(theta) - 1) / 2
    w = np.sin(theta) * np.cos(phi) / 2
    t = np.sin(theta) * np.sin(phi) / 2
    return u * pm(names[0]) + v * pm(names[1]) + w * (pm(names[2]) + pm(names[4])) + t * (pm(names[3]) + pm(names[5]))


def target(theta, phi):
    H0 = sphere(theta, phi)
    return (np.cos(ALPHA) * np.eye(8) + 1j * np.sin(ALPHA) * H0) @ TG2


def controlled_W(theta):
    pp = (I2 + X) / 2
    pminus = (I2 - X) / 2
    return op(1, pminus) + op(1, pp) @ op(0, rp(theta, X))


def w_raw_layers(theta):
    """AD-24 的 2-CZ W 分解，显式写成 q0,q1,q2 的 U(2) 因子。"""
    A = rp(np.pi / 2, Z)
    B = rp(-theta / 2, Y)
    C = B.conj().T @ A.conj().T
    raw = [
        [H @ C, X @ H, I2],
        [H @ B @ H, I2, I2],
        [A @ H, H @ X, I2],
    ]
    L = [layer(x) for x in raw]
    W = L[2] @ cz((0, 1)) @ L[1] @ cz((0, 1)) @ L[0]
    return raw, W


def w_block(theta, dagger=False):
    raw, W = w_raw_layers(theta)
    if dagger:
        # 从同一规范化 W 块取逆，杜绝独立主值分支造成的相位跳变。
        w = w_block(theta, dagger=False)
        mats = [[G.conj().T for G in one] for one in w["mats"][::-1]]
        angles = np.asarray([[angles_of_su2(G) for G in one] for one in mats])
        phase = w["phase"].conjugate()
        expected = W.conj().T
        raw = w["raw"]
    else:
        all_angles = []
        phase = 1 + 0j
        for one in raw:
            p, a, _ = normalize_u2_layers(one)
            phase *= p
            all_angles.append(a)
        angles = np.asarray(all_angles)
        mats = [[su2(a[q]) for q in range(3)] for a in angles]
        expected = W
    U = circuit(np.angle(phase), angles, [(0, 1), (0, 1)])
    err = float(np.max(abs(U - expected)))
    assert err < 2e-8, (theta, dagger, err)
    return {"phase": phase, "angles": angles, "mats": mats,
            "raw": raw, "matrix": expected, "normalization_error": err}


def endpoint_matrices(src):
    angles = np.asarray(src["local_angles_pi_over_4"], float) * np.pi / 4
    return [[su2(angles[i, q]) for q in range(3)] for i in range(8)]


def merged_mats(theta):
    src = json.loads(SRC.read_text())
    wd = w_block(theta, dagger=True)
    w = w_block(theta, dagger=False)
    e = endpoint_matrices(src)
    # 时间顺序：W†、U0、W；两个接缝的局部门分别合并。
    ms = wd["mats"][:2] + [[e[0][q] @ wd["mats"][2][q] for q in range(3)]]
    ms += e[1:7]
    ms += [[w["mats"][0][q] @ e[7][q] for q in range(3)]] + w["mats"][1:]
    assert len(ms) == 12
    phase = src["phase_pi_over_8"] * np.pi / 8 + np.angle(wd["phase"] * w["phase"])
    assert abs(np.exp(1j * phase) - np.exp(1j * src["phase_pi_over_8"] * np.pi / 8)) < 2e-8
    return src, ms, phase, wd, w


def meridian_angles(theta):
    src, ms, phase, _, _ = merged_mats(theta)
    angles = np.asarray([[angles_of_su2(ms[i][q]) for q in range(3)] for i in range(12)])
    edges = [(0, 1), (0, 1)] + [tuple(e) for e in src["edges"]] + [(0, 1), (0, 1)]
    return phase, angles, edges


def full_angles(theta, phi):
    phase, angles, edges = meridian_angles(theta)
    ms = [[su2(angles[i, q]) for q in range(3)] for i in range(12)]
    Rphi = rp(phi, Z)  # = Rz(-phi) = exp(i phi Z/2)
    ms[0][0] = ms[0][0] @ Rphi.conj().T
    ms[-1][0] = Rphi @ ms[-1][0]
    angles = np.asarray([[angles_of_su2(ms[i][q]) for q in range(3)] for i in range(12)])
    return phase, angles, edges


def kp(A, B):
    return sp.kronecker_product(A, B)


def symbolic_proof():
    """在 c=cos(theta/4), s=sin(theta/4), c²+s²=1 上严格约化。"""
    c, s, phi = sp.symbols("c s phi", real=True)
    i = sp.I
    Zs = sp.diag(1, -1)
    Xs = sp.Matrix([[0, 1], [1, 0]])
    Ys = sp.Matrix([[0, -i], [i, 0]])
    Is = sp.eye(2)
    Hs = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    A = sp.diag(sp.exp(i * sp.pi / 4), sp.exp(-i * sp.pi / 4))
    B = sp.Matrix([[c, -s], [s, c]])
    C = B.H * A.H
    L0 = kp(Hs * C, Is)
    L1 = kp(Hs * B * Hs, Is)
    L2 = kp(A * Hs, Is)
    CZ = sp.diag(1, 1, 1, -1)
    Hc = kp(Is, Hs)
    Xc = kp(Is, Xs)
    Wone = L2 * CZ * L1 * CZ * L0
    W = sp.expand(Hc * Xc * Wone * Xc * Hc)
    U = sp.Matrix([[c * c - s * s, 2 * i * c * s], [2 * i * c * s, c * c - s * s]])
    P0 = sp.diag(1, 0)
    P1 = sp.diag(0, 1)
    direct = kp(Is, P0) + kp(U, P1)
    expected = sp.expand(Hc * Xc * direct * Xc * Hc)
    def cs_normal(expr):
        # 精确模去 c²+s²-1；允许 Q(i,sqrt(2)) 系数，不做浮点化。
        def query(z):
            return z.is_Pow and z.base == s and z.exp.is_integer and z.exp >= 2
        def value(z):
            n = int(z.exp)
            return s ** (n % 2) * (1 - c * c) ** (n // 2)
        return sp.expand(sp.expand(expr).replace(query, value))

    def reduced_zero(M):
        return [cs_normal(entry) for entry in M]

    decomposition = reduced_zero(W - expected)
    unitary = reduced_zero(expected * expected.H - sp.eye(4))
    CNOT = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    commutation = reduced_zero(expected * CNOT - CNOT * expected)
    H00 = kp(Zs, Xs)
    co = (c * c - s * s) ** 2 - (2 * c * s) ** 2
    si = 2 * (c * c - s * s) * (2 * c * s)
    u = (1 + co) / 2
    v = (co - 1) / 2
    w = si / 2
    Htheta = u * kp(Zs, Xs) + v * kp(Zs, Is) + w * (kp(Ys, Is) + kp(Ys, Xs))
    conjugation = reduced_zero(Htheta - expected * H00 * expected.H)
    groups = {
        "w_decomposition_4x4": decomposition,
        "w_unitary_4x4": unitary,
        "w_cnot_commutation_4x4": commutation,
        "w_sphere_conjugation_4x4": conjugation,
    }
    counts = {name: sum(x != 0 for x in rows) for name, rows in groups.items()}
    assert all(v == 0 for v in counts.values()), counts

    # phi：R=exp(i phi Z/2)，R X R†=cos(phi)X-sin(phi)Y，R Y R†=cos(phi)Y+sin(phi)X。
    Rphi = sp.diag(sp.exp(i * phi / 2), sp.exp(-i * phi / 2))
    px = sp.simplify(sp.expand_complex(Rphi * Xs * Rphi.H - (sp.cos(phi) * Xs - sp.sin(phi) * Ys)))
    py = sp.simplify(sp.expand_complex(Rphi * Ys * Rphi.H - (sp.cos(phi) * Ys + sp.sin(phi) * Xs)))
    pz = sp.simplify(Rphi * Zs * Rphi.H - Zs)
    assert px == sp.zeros(2) and py == sp.zeros(2) and pz == sp.zeros(2)
    return {
        "status": "ALL_SYMBOLIC_IDENTITIES_EXACT_ZERO",
        "coordinates": "c=cos(theta/4), s=sin(theta/4), relation c^2+s^2-1=0; phi kept symbolic",
        "reduction": "exact normal form by s^n -> s^(n mod 2)(1-c^2)^floor(n/2), equivalent to reduction modulo c^2+s^2-1",
        "nonzero_after_reduction": counts,
        "phi_pauli_conjugation": "RXR^dagger=cos(phi)X-sin(phi)Y; RYR^dagger=cos(phi)Y+sin(phi)X; RZR^dagger=Z exact",
        "theorem": "Wtheta=Tcontrolled 2-CZ block; [Wtheta,Toffoli]=0; H(theta,0)=Wtheta H00 Wtheta^dagger; H(theta,phi)=Rphi H(theta,0) Rphi^dagger.",
        "circuit_consequence": "U(theta,phi)=Rphi Wtheta U0 Wtheta^dagger Rphi^dagger; 2+7+2=11 CZ, unchanged PATH edge sequence, only first/last q0 SU(2) layers absorb Rphi.",
    }


def exact_theta_zero(edges, angles, phase):
    import importlib.util
    spec = importlib.util.spec_from_file_location("ad25_exact_field", EX)
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    ints = np.rint(np.asarray(angles) / (np.pi / 4)).astype(int)
    delta = float(np.max(abs(ints * (np.pi / 4) - angles)))
    nphase = int(np.rint(phase / (np.pi / 8)))
    pdelta = abs(nphase * np.pi / 8 - phase)
    assert delta < 2e-7 and pdelta < 2e-8, (delta, pdelta)
    U = ex.circuit(nphase, ints.tolist(), edges)
    Zz = ex.diag2(ex.ONE, -ex.ONE)
    Xx = [[ex.Z, ex.ONE], [ex.ONE, ex.Z]]
    Ii = ex.eye(2)

    def exop(q, A):
        ms = [Ii, Ii, Ii]
        ms[q] = A
        return ex.kron(ex.kron(ms[0], ms[1]), ms[2])

    H00 = ex.mm(ex.mm(exop(0, Zz), exop(1, Xx)), exop(2, Zz))
    T = ex.toffoli({0, 2}, 1)
    w, wm = ex.wpow(1), ex.wpow(-1)
    co = (w + wm).scale(ex.F(1, 2))
    isi = (w - wm).scale(ex.F(1, 2))
    V = ex.mm([[co * a + isi * h for a, h in zip(ri, rh)] for ri, rh in zip(ex.eye(8), H00)], T)
    nz = ex.nonzero_entries(ex.md(U, V))
    assert nz == 0
    return {"status": "THETA_ZERO_11CZ_ALL_EXACT_ZERO", "exact_nonzero_residual_entries": nz,
            "phase_pi_over_8": nphase, "local_angles_pi_over_4": ints.tolist(),
            "max_integer_snap_rad": delta, "field": "Q(w), w=exp(i*pi/8), w^8+1=0"}


def schmidt2(U):
    A = np.zeros((4, 4), complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    A[2 * a + c, 2 * b + d] = U[2 * a + b, 2 * c + d]
    return np.linalg.svd(A, compute_uv=False)


def cancellation_attack(theta):
    _, angles, edges = meridian_angles(theta)
    ms = [[su2(angles[i, q]) for q in range(3)] for i in range(12)]
    rows = []
    for j in range(len(edges) - 1):
        if edges[j] != edges[j + 1] or edges[j] != (0, 1):
            continue
        L = np.kron(ms[j + 1][0], ms[j + 1][1])
        pair = CZ4 @ L @ CZ4
        sv = schmidt2(pair)
        rows.append({"left_cz_index": j, "rank_1e-9": int(np.sum(sv > 1e-9)),
                     "second_schmidt_coefficient": float(sv[1]), "local_cancellation": bool(sv[1] < 1e-9)})
    # 已知答案：I 的秩为 1，CZ 的秩为 2。
    assert abs(schmidt2(np.eye(4))[1]) < 1e-12 and schmidt2(CZ4)[1] > 0.9
    return rows


def known_answer_gate():
    out = {"w_cases": [], "wrong_adjoint_direction_nonzero": None, "phi_cases": []}
    wrong = 0.0
    for th in (0.0, 0.1, 0.7, 1.3):
        raw, Wraw = w_raw_layers(th)
        W = controlled_W(th)
        ew = float(np.max(abs(Wraw - W)))
        comm = float(np.max(abs(W @ TG2 - TG2 @ W)))
        conj = float(np.max(abs(sphere(th, 0.0) - W @ sphere(0.0, 0.0) @ W.conj().T)))
        ident = float(np.max(abs(W @ W.conj().T - np.eye(8))))
        assert max(ew, comm, conj, ident) < 2e-12, (th, ew, comm, conj, ident)
        if th:
            wrong = max(wrong, float(np.max(abs(sphere(th, 0.0) - W.conj().T @ sphere(0.0, 0.0) @ W))))
        out["w_cases"].append({"theta": th, "decomposition": ew, "unitary": ident,
                               "toffoli_commutation": comm, "sphere_conjugation": conj})
    assert wrong > 1e-3
    out["wrong_adjoint_direction_nonzero"] = wrong
    for ph in (-1.3, -0.2, 0.4, 1.7):
        Rphi = op(0, rp(ph, Z))
        th = 0.7
        comm = float(np.max(abs(Rphi @ TG2 - TG2 @ Rphi)))
        conj = float(np.max(abs(sphere(th, ph) - Rphi @ sphere(th, 0.0) @ Rphi.conj().T)))
        assert max(comm, conj) < 2e-12
        out["phi_cases"].append({"phi": ph, "toffoli_commutation": comm, "sphere_conjugation": conj})
    return out


def main():
    src = json.loads(SRC.read_text())
    src_sha = hashlib.sha256(SRC.read_bytes()).hexdigest()
    assert src_sha == "ec0f942e4a5404daaf5476126d93f27a00eb7821a056c77c9025b806203065ce"
    gate = known_answer_gate()  # 已知答案必须先于未知目标。
    proof = symbolic_proof()

    eangles = np.asarray(src["local_angles_pi_over_4"], float) * np.pi / 4
    endpoint_numeric = float(np.max(abs(circuit(src["phase_pi_over_8"] * np.pi / 8, eangles, src["edges"]) - target(0.0, 0.0))))
    assert endpoint_numeric < 2e-12

    p0, a0, edges = meridian_angles(0.0)
    theta_zero_numeric = float(np.max(abs(circuit(p0, a0, edges) - target(0.0, 0.0))))
    assert theta_zero_numeric < 2e-8
    exact0 = exact_theta_zero(edges, a0, p0)

    records = []
    for th in np.linspace(0, np.pi, 9):
        for ph in np.linspace(-np.pi, np.pi, 8, endpoint=False):
            p, a, e = full_angles(float(th), float(ph))
            U = circuit(p, a, e)
            V = target(float(th), float(ph))
            err = float(np.max(abs(U - V)))
            assert err < 3e-8, (th, ph, err)
            records.append({"theta": float(th), "phi": float(ph), "max_abs": err,
                            "frobenius": float(np.linalg.norm(U - V))})
    max_e = max(r["max_abs"] for r in records)

    cancel = {}
    for th in (0.0, 0.1, 0.7, 1.3):
        rows = cancellation_attack(th)
        cancel[str(th)] = rows
    nonzero_hits = sum(r["local_cancellation"] for th, rows in cancel.items() if th != "0.0" for r in rows)
    out = {
        "beat": "AD-25",
        "status": "S2_FULL_SPHERE_11CZ_L1_PASS",
        "evidence_level": "L1 analytic circuit identity; L2 independent-looking numeric grid is corroboration only",
        "source_endpoint": {"path": str(SRC), "sha256": src_sha,
                            "theta0_7cz_numeric_max_abs": endpoint_numeric},
        "known_answer_gate_first": gate,
        "symbolic_proof": proof,
        "construction": {
            "cz_count": 11,
            "edges": [list(e) for e in edges],
            "time_order": "W(theta)^dagger -> AD-24 U0 -> W(theta), then Rphi on both outer sides",
            "phase": "3*pi/8; W and W^dagger normalization phases cancel",
            "local_layers": 12,
            "phi_absorption": "first q0 SU(2) right-multiplied by Rphi^dagger; last q0 SU(2) left-multiplied by Rphi",
            "theta_zero_11cz_exact": exact0,
            "theta_zero_numeric_max_abs": theta_zero_numeric,
        },
        "numeric_full_matrix_grid": {"points": len(records), "theta_points": 9, "phi_points": 8,
                                      "max_abs": max_e, "records": records},
        "adjacent_cz_cancellation_attack": {
            "scope": "isolated CZ-local-CZ pair on 01; exact local iff two-qubit operator Schmidt rank=1",
            "by_theta": cancel, "nonzero_theta_hits": nonzero_hits,
            "verdict": "NO_TESTED_NONZERO_THETA_LOCAL_PAIR_CANCELLATION" if nonzero_hits == 0 else "CANDIDATE_HITS_REQUIRE_REBUILD",
            "boundary": "只排除被测相邻门直接局部抵消；不排除跨多块重合成、非标准W分解、其他边序或9/7-CZ实现。",
        },
        "strict_conclusion": "序34对应的整个S²目标族存在同一11-CZ PATH模板的解析全矩阵实现；theta=0仍可由AD-24的7-CZ实现。",
        "open_boundaries": [
            "11-CZ不冒报为最优；11到9/7的跨块消门与另一模板仍开放。",
            "数值72点只作交叉检查，任意theta/phi结论由符号恒等式链承担。",
            "旧65点7-CZ同伦仍属L2；本结果不把全theta的7-CZ存在性写成定理。",
            "±pi/8角刚性未由本构造解决。",
        ],
        "private_ci_consumption": 0,
        "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad25_s2_meridian.json").write_bytes(raw)
    exact_raw = json.dumps(exact0, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad25_s2_theta0_11cz_exact.json").write_bytes(exact_raw)
    print(json.dumps({"status": out["status"], "symbolic": proof["nonzero_after_reduction"],
                      "theta0_exact": exact0["status"], "numeric_points": len(records),
                      "numeric_max_abs": max_e, "nonzero_theta_cancellation_hits": nonzero_hits,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
