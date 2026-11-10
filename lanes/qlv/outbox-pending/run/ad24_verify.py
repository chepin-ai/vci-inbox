"""AD-24 独立总验收：不导入任何构造、求解或分析模块。

MAJ 秩用 Fraction 行消元；S² 端点用 SymPy 代数域；数值件从原始角度独立重建。
"""
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
PAULI = {
    "I": I2,
    "X": np.array([[0, 1], [1, 0]], complex),
    "Y": np.array([[0, -1j], [1j, 0]], complex),
    "Z": np.diag([1, -1]).astype(complex),
}
ALPHA = np.pi / 8


def bits(x):
    return [(x >> 2) & 1, (x >> 1) & 1, x & 1]


def code(b):
    return (b[0] << 2) | (b[1] << 1) | b[2]


def perm(fn):
    M = np.zeros((8, 8), complex)
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


def toffoli(cs, t):
    def f(x):
        b = bits(x)
        if all(b[q] for q in cs):
            b[t] ^= 1
        return code(b)
    return perm(f)


MAJ = toffoli({0, 2}, 1) @ cnot(1, 2) @ cnot(1, 0)
TG2 = toffoli({0, 2}, 1)


def one(g, q):
    return np.kron(np.kron(g if q == 0 else I2, g if q == 1 else I2), g if q == 2 else I2)


def rz(a):
    return np.diag([np.exp(-0.5j * a), np.exp(0.5j * a)])


def ry(a):
    return np.array([[np.cos(a / 2), -np.sin(a / 2)], [np.sin(a / 2), np.cos(a / 2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def layer(t):
    return np.kron(np.kron(su2(t[0]), su2(t[1])), su2(t[2]))


def cz(edge):
    a, b = edge
    d = np.ones(8, complex)
    for x in range(8):
        bb = bits(x)
        if bb[a] and bb[b]:
            d[x] = -1
    return np.diag(d)


def circuit(p, edges):
    p = np.asarray(p, float)
    k = len(edges)
    assert len(p) == 1 + 9 * (k + 1)
    angles = p[1:].reshape(k + 1, 3, 3)
    U = np.exp(1j * p[0]) * layer(angles[-1])
    for j in range(k - 1, -1, -1):
        U = U @ cz(edges[j]) @ layer(angles[j])
    return U


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
    H = sphere(theta, phi)
    return (np.cos(ALPHA) * np.eye(8) + 1j * np.sin(ALPHA) * H) @ TG2


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


def unfold(M, q):
    n, m = 2 ** q, 2 ** (3 - q)
    A = np.zeros((n * n, m * m), dtype=int)
    for ol in range(n):
        for il in range(n):
            for orr in range(m):
                for ir in range(m):
                    out, inn = (ol << (3 - q)) | orr, (il << (3 - q)) | ir
                    z = M[out, inn]
                    assert abs(z.imag) < 1e-12 and abs(z.real - round(z.real)) < 1e-12
                    A[ol * n + il, orr * m + ir] = int(round(z.real))
    return A


def qperm(p):
    def f(x):
        old = bits(x)
        new = [0] * 3
        for oq in range(3):
            new[p[oq]] = old[oq]
        return code(new)
    return perm(f)


def mapping(M):
    assert np.max(abs(M.imag)) < 1e-12
    return tuple(int(np.argmax(abs(M[:, x]))) for x in range(8))


def verify_maj():
    src = json.loads((R / "ad24_maj_audit.json").read_text())
    ranks = {}
    for q, name in ((1, "0|12"), (2, "1|23")):
        A = unfold(MAJ, q)
        assert np.array_equal(A, np.asarray(src["schmidt_rank_theorem"]["cuts"][name]["unfolded_integer_matrix"]))
        ranks[name] = fraction_rank(A)
        assert ranks[name] == 4
    d = np.ones(8, complex)
    for x in range(8):
        b = bits(x)
        if b[0] and b[1]:
            d[x] = -1
    assert fraction_rank(unfold(np.diag(d), 1)) == 2
    assert fraction_rank(unfold(np.diag(d), 2)) == 1
    assert np.max(abs(MAJ @ cnot(1, 0) @ cnot(1, 2) - TG2)) == 0

    H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
    T = np.diag([1, np.exp(1j * np.pi / 4)])
    Td = T.conj().T
    ops = [
        ("L", H, 2), ("C", 1, 2), ("L", Td, 2), ("C", 0, 2),
        ("L", T, 2), ("C", 1, 2), ("L", Td, 2), ("C", 0, 2),
        ("L", T, 1), ("L", T, 2), ("L", H, 2), ("C", 0, 1),
        ("L", T, 0), ("L", Td, 1),
    ]
    U = np.eye(8, dtype=complex)
    for typ, a, b in ops:
        U = (one(a, b) if typ == "L" else cnot(a, b)) @ U
    P = cnot(0, 1) @ toffoli({0, 1}, 2)
    perr = float(np.max(abs(U - P)))
    assert perr < 1e-12
    tested, hits = 0, 0
    for p in itertools.permutations(range(3)):
        Q = qperm(p)
        for mi in range(8):
            Xin = np.eye(8, dtype=complex)
            for q in range(3):
                if (mi >> q) & 1:
                    Xin = one(PAULI["X"], q) @ Xin
            for mo in range(8):
                Xout = np.eye(8, dtype=complex)
                for q in range(3):
                    if (mo >> q) & 1:
                        Xout = one(PAULI["X"], q) @ Xout
                Pp = Q @ Xout @ P @ Xin @ Q.conj().T
                for c, t in itertools.permutations(range(3), 2):
                    C = cnot(c, t)
                    for M in (C @ Pp, Pp @ C):
                        tested += 1
                        hits += int(mapping(M) == mapping(MAJ))
    assert tested == 4608 and hits == 0
    return {"engine": "Fraction complete row elimination + independently rebuilt finite permutation enumeration",
            "ranks": ranks, "single_cz_known_answers": [2, 1], "peres_numeric_error": perr,
            "peres_direct_cases": tested, "peres_direct_hits": hits,
            "interval_unchanged": src["strict_interval"] == "4 <= k <= 7"}


# 独立代数域：不复用构造器的 Fraction 域实现。
ZETA = sp.exp(sp.I * sp.pi / 8)
K = sp.QQ.algebraic_field(ZETA)
ZERO, ONE = K.zero, K.one
W = K.from_sympy(ZETA)


def wp(n):
    return W ** int(n % 16)


def erz(n):
    return [[wp(-n), ZERO], [ZERO, wp(n)]]


def ery(n):
    c = K.from_sympy(sp.cos(int(n) * sp.pi / 8))
    s = K.from_sympy(sp.sin(int(n) * sp.pi / 8))
    return [[c, -s], [s, c]]


def emm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), ZERO) for j in range(len(B[0]))] for i in range(len(A))]


def ekron(A, B):
    return [[A[i][j] * B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]


def elayer(t):
    def esu2(a):
        return emm(emm(erz(a[0]), ery(a[1])), erz(a[2]))
    return ekron(ekron(esu2(t[0]), esu2(t[1])), esu2(t[2]))


def ecz(edge):
    a, b = edge
    d = [-ONE if (bits(x)[a] and bits(x)[b]) else ONE for x in range(8)]
    return [[d[i] if i == j else ZERO for j in range(8)] for i in range(8)]


def exact_nonzero(A):
    return sum(A[i][j] != ZERO for i in range(len(A)) for j in range(len(A[0])))


def verify_endpoint_exact():
    src = json.loads((R / "ad24_s2_exact.json").read_text())
    angles = src["local_angles_pi_over_4"]
    edges = src["edges"]
    U = elayer(angles[-1])
    for j in range(len(edges) - 1, -1, -1):
        U = emm(emm(U, ecz(edges[j])), elayer(angles[j]))
    U = [[wp(src["phase_pi_over_8"]) * U[i][j] for j in range(8)] for i in range(8)]
    Zz = [[ONE, ZERO], [ZERO, -ONE]]
    Xx = [[ZERO, ONE], [ONE, ZERO]]
    Ii = [[ONE, ZERO], [ZERO, ONE]]

    def op(q, A):
        ms = [Ii, Ii, Ii]
        ms[q] = A
        return ekron(ekron(ms[0], ms[1]), ms[2])

    H0 = emm(emm(op(0, Zz), op(1, Xx)), op(2, Zz))
    Tex = [[ZERO] * 8 for _ in range(8)]
    for x in range(8):
        b = bits(x)
        if b[0] and b[2]:
            b[1] ^= 1
        Tex[code(b)][x] = ONE
    co = K.from_sympy(sp.cos(sp.pi / 8))
    isi = K.from_sympy(sp.I * sp.sin(sp.pi / 8))
    V = emm([[co * a + isi * h for a, h in zip(ri, rh)] for ri, rh in zip(
        [[ONE if i == j else ZERO for j in range(8)] for i in range(8)], H0)], Tex)
    nz = exact_nonzero([[U[i][j] - V[i][j] for j in range(8)] for i in range(8)])
    assert nz == 0
    # 三角已知答案门。
    for n in range(-8, 9):
        c = K.from_sympy(sp.cos(n * sp.pi / 8))
        s = K.from_sympy(sp.sin(n * sp.pi / 8))
        assert c * c + s * s == ONE
    return {"engine": "SymPy QQ.algebraic_field(exp(I*pi/8)) independent of constructor",
            "exact_nonzero_residual_entries": nz, "trig_known_answer_cases": 17,
            "status": "INDEPENDENT_ENDPOINT_ALL_EXACT_ZERO"}


def read_jsonl(name):
    return [json.loads(s) for s in (R / name).read_text().splitlines() if s.strip()]


def fourier(rows):
    theta = np.array([r["theta"] for r in rows])
    G = np.empty((len(rows), 8, 3, 2, 2), complex)
    for i, r in enumerate(rows):
        a = np.asarray(r["x"])[1:].reshape(8, 3, 3)
        for l in range(8):
            for q in range(3):
                G[i, l, q] = su2(a[l, q])
    ans = []
    for freqs in ([0, .5, 1], [0, .25, .5, .75, 1], [0, .125, .25, .375, .5, .625, .75, .875, 1]):
        A = np.stack([np.exp(2j * f * theta) for f in freqs], axis=1)
        coef = np.linalg.lstsq(A, G.reshape(len(rows), -1), rcond=None)[0]
        error = np.max(abs((A @ coef).reshape(G.shape) - G), axis=0)
        ge = error.max(axis=(2, 3))
        ans.append({"frequencies": freqs, "fit_gates_lt_1e-8": int(np.sum(ge < 1e-8)),
                    "max_scalar_entry_error": float(error.max())})
    return ans


def verify_s2_numeric():
    src = json.loads((R / "ad24_s2_scans.json").read_text())
    scan = {}
    V0 = target(0.0, src["phi"])
    for key in ("k3", "k4", "k5", "k7_AA"):
        errors = [float(np.max(abs(circuit(r["x"], r["edges"]) - V0))) for r in src[key]]
        scan[key] = {"runs": len(errors), "hits": int(sum(e < 1e-9 for e in errors)), "best": min(errors)}
    assert scan["k7_AA"]["hits"] == 1 and all(scan[k]["hits"] == 0 for k in ("k3", "k4", "k5"))
    hom = {}
    for name, frozen in (("ad24_s2_legacy_homotopy.jsonl", False), ("ad24_s2_homotopy.jsonl", True)):
        rows = read_jsonl(name)
        errors = [float(np.max(abs(circuit(r["x"], r["edges"]) - target(r["theta"], r["phi"])))) for r in rows]
        assert len(rows) == 65 and max(errors) < 1e-12
        item = {"points": len(rows), "max_e": max(errors), "fourier": fourier(rows)}
        if frozen:
            formulas = {0: lambda t: 3 * np.pi / 8, 56: lambda t: np.pi / 2 + t / 2,
                        57: lambda t: np.pi / 2, 65: lambda t: np.pi / 2 - t / 2}
            deltas = [abs(np.asarray(r["x"])[i] - fn(r["theta"])) for r in rows for i, fn in formulas.items()]
            assert max(deltas) == 0
            item["frozen_coordinate_max_delta"] = max(deltas)
        hom[name] = item
    return {"scans": scan, "homotopy": hom,
            "evidence_boundary": "数值重建不升级为全经线解析证书，也不把低k未命中当作不存在。"}


def known_numeric_gate():
    rng = np.random.default_rng(240024)
    worst_u = worst_h = 0.0
    for k in (1, 2, 7):
        edges = [(0, 1) if j % 2 == 0 else (1, 2) for j in range(k)]
        p = rng.normal(size=1 + 9 * (k + 1))
        U = circuit(p, edges)
        worst_u = max(worst_u, float(np.max(abs(U @ U.conj().T - np.eye(8)))))
    for th in np.linspace(0, np.pi, 9):
        for ph in np.linspace(-np.pi, np.pi, 8, endpoint=False):
            H = sphere(th, ph)
            worst_h = max(worst_h, float(np.max(abs(H @ H - np.eye(8)))))
    assert worst_u < 1e-12 and worst_h < 1e-12
    return {"random_circuit_unitarity_max": worst_u, "sphere_involution_max": worst_h,
            "cases": "3 random circuits + 72 sphere points"}


def main():
    start = time.time()
    # 已知答案必须先于未知目标。
    numeric_gate = known_numeric_gate()
    maj = verify_maj()
    exact = verify_endpoint_exact()
    numeric = verify_s2_numeric()
    rac = json.loads((R / "ad24_rac_check.json").read_text())
    assert rac["verdict"] == "WAITING_PEER_S_SIM" and not rac["fingerprint_arrived"]
    assert rac["private_ci_consumption"] == rac["quantum_machine_consumption"] == 0
    assert all(not item["has_numeric_S_sim"] for repo in rac["repos"].values() for item in repo["candidates"])
    assert all(not item.get("queue_only", False) for repo in rac["repos"].values()
               for item in repo["candidates"] if item.get("source_code_excluded_from_fingerprint"))
    files = ["ad24_maj_audit.json", "ad24_s2_endpoint.json", "ad24_s2_exact.json",
             "ad24_s2_scans.json", "ad24_s2_legacy_homotopy.jsonl", "ad24_s2_homotopy.jsonl",
             "ad24_s2_summary.json", "ad24_rac_check.json"]
    out = {
        "beat": "AD-24", "status": "ALL_PASS",
        "known_answer_gate_first": numeric_gate,
        "maj_independent": maj,
        "s2_exact_independent": exact,
        "s2_numeric_independent": numeric,
        "rac": {
            "checked_at": rac["checked_at"], "verdict": rac["verdict"],
            "fingerprint_arrived": rac["fingerprint_arrived"],
            "heads": {name: repo["head"] for name, repo in rac["repos"].items()},
            "candidate_counts": {name: repo["candidate_counts"] for name, repo in rac["repos"].items()},
        },
        "input_sha256": {name: hashlib.sha256((R / name).read_bytes()).hexdigest() for name in files},
        "strict_result": "MAJ区间4<=k<=7不变；S² theta=0端点7-CZ为独立L1精确零；全theta解析经线未闭合。",
        "anomaly_notes": [
            "第一诚律·异常注记1：原始S²命中角不全在pi/4网格，未直接取整伪造证书；先冻结/重解得到数值闭合的全网格构造，再做精确域零验收。",
            "第一诚律·异常注记2：Peres五CNOT初次重建遗漏尾部局部门并混用T约定；最终按Shende-Markov Fig.1删最右CNOT且保留尾部T/Tdag，独立全矩阵误差3.1401849173675503e-16。",
            "第一诚律·异常注记3：signA=-1的W候选未过已知答案门，不用于结论；仅signA=+1标准分解通过三点已知门，新端点边界归一化及576个Clifford候选仍零命中。",
            "第一诚律·异常注记4：独立验收器初版Sphere基标签与Kronecker行索引有误，修正为ZXZ/ZIZ/YIZ/XIZ/YXZ/XXZ及len(A)外循环后重跑；失败运行不记通过。",
            "第一诚律·异常注记5：RAC源码队列字面量不充当对方数值指纹；本次三仓候选均无数值S_sim，维持WAITING_PEER_S_SIM。",
        ],
        "open_boundaries": [
            "MAJ严格区间仍4<=k<=7；k=4六种Schmidt饱和边序未解析排除，k=5/6无更小严格构造。",
            "S²仅theta=0端点为L1；65点冻结坐标同伦为L2，完整解析theta经线未闭合。",
            "标准controlled-W及576个Clifford边界归一化失败只覆盖被测形式，非标准连续W或其他模板仍开放。",
            "±pi/8角刚性、序91全局basin几何未解决。",
            "RAC对方数值S_sim未到件，跨线独立对拍未启动。",
        ],
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad24_verify.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "known_answer_gate_first": numeric_gate,
                      "maj": maj, "exact": exact,
                      "legacy_max_e": numeric["homotopy"]["ad24_s2_legacy_homotopy.jsonl"]["max_e"],
                      "frozen_max_e": numeric["homotopy"]["ad24_s2_homotopy.jsonl"]["max_e"],
                      "seconds": time.time() - start, "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
