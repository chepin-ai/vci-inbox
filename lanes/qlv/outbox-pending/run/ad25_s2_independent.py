"""AD-25 S² 独立验收：不导入构造器、AD-23/24 验收器或分析模块。

任意角：独立符号恒等式链；theta=0：纯 Fraction 的 Q(w) 多项式基底全矩阵重乘。
数值点只用于交叉证伪，不承担任意角证明。
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
ENDPOINT = R.parent.parent / "ad24/run/ad24_s2_exact.json"
THETA0 = R / "ad25_s2_theta0_11cz_exact.json"


def known_numeric_gate():
    X = np.array([[0, 1], [1, 0]], complex)
    Y = np.array([[0, -1j], [1j, 0]], complex)
    Z = np.diag([1, -1])
    I = np.eye(2)
    P0, P1 = np.diag([1, 0]), np.diag([0, 1])
    worst = 0.0
    for theta in (0.0, 0.31, 1.17):
        U = np.cos(theta / 2) * I + 1j * np.sin(theta / 2) * X
        W = np.kron(I, P0) + np.kron(U, P1)
        worst = max(worst, float(np.max(abs(W @ W.conj().T - np.eye(4)))))
    assert worst < 1e-13
    # 已知错误方向必须能被拒绝。
    H0 = np.kron(Z, X)
    th = 0.73
    U = np.cos(th / 2) * I + 1j * np.sin(th / 2) * X
    W = np.kron(I, P0) + np.kron(U, P1)
    wrong = float(np.max(abs(W.conj().T @ H0 @ W - H0)))
    assert wrong > 1e-3
    return {"controlled_unitary_cases": 3, "unitarity_max": worst,
            "wrong_adjoint_direction_max_abs": wrong}


# ---------- 独立的纯分数 Q(w) 域，w^8=-1 ----------
def F(x=0):
    out = [Fraction(0) for _ in range(8)]
    out[0] = Fraction(x)
    return tuple(out)


ZERO, ONE = F(0), F(1)


def fa(a, b):
    return tuple(x + y for x, y in zip(a, b))


def fn(a):
    return tuple(-x for x in a)


def fs(a, b):
    return fa(a, fn(b))


def fscale(a, x):
    x = Fraction(x)
    return tuple(x * y for y in a)


def fm(a, b):
    out = [Fraction(0) for _ in range(8)]
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            k = i + j
            out[k % 8] += (-x * y if k >= 8 else x * y)
    return tuple(out)


def wp(n):
    n %= 16
    out = [Fraction(0) for _ in range(8)]
    if n < 8:
        out[n] = Fraction(1)
    else:
        out[n - 8] = Fraction(-1)
    return tuple(out)


def cospi8(n):
    return fscale(fa(wp(n), wp(-n)), Fraction(1, 2))


def isinpi8(n):
    return fscale(fs(wp(n), wp(-n)), Fraction(1, 2))


def sinpi8(n):
    return fm(fn(wp(4)), isinpi8(n))


def mm(A, B):
    out = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            acc = ZERO
            for k in range(len(B)):
                acc = fa(acc, fm(A[i][k], B[k][j]))
            row.append(acc)
        out.append(row)
    return out


def md(A, B):
    return [[fs(A[i][j], B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def mscale(A, a):
    return [[fm(a, x) for x in row] for row in A]


def kp(A, B):
    return [[fm(A[i][j], B[k][l]) for j in range(len(A[0])) for l in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def bits(x):
    return [(x >> 2) & 1, (x >> 1) & 1, x & 1]


def esu2(t):
    a, b, c = map(int, t)
    rz_a = [[wp(-a), ZERO], [ZERO, wp(a)]]
    ry_b = [[cospi8(b), fn(sinpi8(b))], [sinpi8(b), cospi8(b)]]
    rz_c = [[wp(-c), ZERO], [ZERO, wp(c)]]
    return mm(mm(rz_a, ry_b), rz_c)


def elayer(t):
    return kp(kp(esu2(t[0]), esu2(t[1])), esu2(t[2]))


def ecz_right(U, edge):
    a, b = edge
    out = [row[:] for row in U]
    for x in range(8):
        bb = bits(x)
        if bb[a] and bb[b]:
            for i in range(8):
                out[i][x] = fn(out[i][x])
    return out


def exact_circuit(phase, angles, edges):
    U = mscale(elayer(angles[-1]), wp(phase))
    for j in range(len(edges) - 1, -1, -1):
        U = mm(ecz_right(U, edges[j]), elayer(angles[j]))
    return U


def exact_target_theta0():
    Ii, Zz = eye(2), [[ONE, ZERO], [ZERO, fn(ONE)]]
    Xx = [[ZERO, ONE], [ONE, ZERO]]
    H = kp(kp(Zz, Xx), Zz)
    T = [[ZERO] * 8 for _ in range(8)]
    for x in range(8):
        b = bits(x)
        if b[0] and b[2]:
            b[1] ^= 1
        T[(b[0] << 2) | (b[1] << 1) | b[2]][x] = ONE
    V = [[fa(fm(cospi8(1), a), fm(isinpi8(1), h)) for a, h in zip(ri, rh)]
         for ri, rh in zip(eye(8), H)]
    return mm(V, T)


def exact_known_gate():
    assert wp(8) == fn(ONE)
    for n in range(-8, 9):
        c, s = cospi8(n), sinpi8(n)
        assert fa(fm(c, c), fm(s, s)) == ONE
    # 目标生成元已知答案：H00=Z0 X1 Z2 必须为对合。
    Ii, Zz = eye(2), [[ONE, ZERO], [ZERO, fn(ONE)]]
    Xx = [[ZERO, ONE], [ONE, ZERO]]
    H00 = kp(kp(Zz, Xx), Zz)
    assert md(mm(H00, H00), eye(8)) == [[ZERO] * 8 for _ in range(8)]
    return {"field_relation": "w^8+1=0", "trigonometric_cases": 17,
            "sphere_endpoint_involution": True,
            "representation": "8-tuple Fraction polynomial basis; no SymPy field and no constructor import"}


def verify_theta0_exact(src, zero):
    edges = [(0, 1), (0, 1)] + [tuple(e) for e in src["edges"]] + [(0, 1), (0, 1)]
    assert len(zero["local_angles_pi_over_4"]) == 12
    U = exact_circuit(zero["phase_pi_over_8"], zero["local_angles_pi_over_4"], edges)
    D = md(U, exact_target_theta0())
    nz = sum(x != ZERO for row in D for x in row)
    assert nz == 0
    return {"status": "THETA_ZERO_11CZ_INDEPENDENT_ALL_EXACT_ZERO",
            "nonzero_residual_entries": nz, "cz_count": len(edges),
            "edges": [list(e) for e in edges],
            "engine": "pure Fraction Q(w), independent polynomial reduction w^8=-1"}


# ---------- 独立符号恒等式 ----------
def symbolic_identities():
    c, s, phi = sp.symbols("c s phi", real=True)
    i = sp.I
    I, X = sp.eye(2), sp.Matrix([[0, 1], [1, 0]])
    Y, Z = sp.Matrix([[0, -i], [i, 0]]), sp.diag(1, -1)
    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    A = sp.diag(sp.exp(i * sp.pi / 4), sp.exp(-i * sp.pi / 4))
    B = sp.Matrix([[c, -s], [s, c]])
    C = B.H * A.H
    CZ = sp.diag(1, 1, 1, -1)
    Wone = (sp.kronecker_product(A * H, I) * CZ *
            sp.kronecker_product(H * B * H, I) * CZ *
            sp.kronecker_product(H * C, I))
    HC, XC = sp.kronecker_product(I, H), sp.kronecker_product(I, X)
    W = sp.expand(HC * XC * Wone * XC * HC)
    U = sp.Matrix([[c*c-s*s, 2*i*c*s], [2*i*c*s, c*c-s*s]])
    direct = sp.kronecker_product(I, sp.diag(1, 0)) + sp.kronecker_product(U, sp.diag(0, 1))
    expected = sp.expand(HC * XC * direct * XC * HC)
    H00 = sp.kronecker_product(Z, X)
    co = (c*c-s*s)**2 - (2*c*s)**2
    si = 2 * (c*c-s*s) * (2*c*s)
    Htheta = ((1+co)/2 * H00 + (co-1)/2 * sp.kronecker_product(Z, I) +
              si/2 * (sp.kronecker_product(Y, I) + sp.kronecker_product(Y, X)))
    CNOT = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    def normal(x):
        # 独立商式约化：反复把首项 s^n 用 s^(n-2)(1-c^2) 替换。
        x = sp.expand(x)
        old = None
        while old != x:
            old = x
            x = sp.expand(x.replace(lambda z: z.is_Pow and z.base == s and z.exp.is_integer and z.exp >= 2,
                                    lambda z: s**(int(z.exp)-2) * (1-c*c)))
        return x

    groups = {
        "w_decomposition": W - expected,
        "w_unitarity": expected * expected.H - sp.eye(4),
        "w_toffoli_commutation": expected * CNOT - CNOT * expected,
        "w_meridian_conjugation": Htheta - expected * H00 * expected.H,
    }
    counts = {name: sum(normal(x) != 0 for x in M) for name, M in groups.items()}
    assert all(v == 0 for v in counts.values()), counts
    Rphi = sp.diag(sp.exp(i*phi/2), sp.exp(-i*phi/2))
    px = sp.simplify(sp.expand_complex(Rphi*X*Rphi.H - (sp.cos(phi)*X-sp.sin(phi)*Y)))
    py = sp.simplify(sp.expand_complex(Rphi*Y*Rphi.H - (sp.cos(phi)*Y+sp.sin(phi)*X)))
    assert px == sp.zeros(2) and py == sp.zeros(2)
    return {"status": "ALL_INDEPENDENT_SYMBOLIC_IDENTITIES_EXACT_ZERO",
            "nonzero_after_normal_form": counts,
            "relation": "c^2+s^2=1; c=cos(theta/4), s=sin(theta/4)",
            "phi_absorption": "R X R^dagger=cos(phi)X-sin(phi)Y; R Y R^dagger=cos(phi)Y+sin(phi)X",
            "consequence": "Rphi W U0 W^dagger Rphi^dagger implements the full S² with 2+7+2 CZ"}


# ---------- 非构造器网格：U(2) 因子显式归一，独立重拼 ----------
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)


def rp(t, P):
    return np.cos(t/2) * I2 + 1j * np.sin(t/2) * P


def rz(a):
    return np.diag([np.exp(-0.5j*a), np.exp(0.5j*a)])


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def k3(a, b, c):
    return np.kron(np.kron(a, b), c)


def cz(edge):
    a, b = edge
    return np.diag([-1 if (bits(x)[a] and bits(x)[b]) else 1 for x in range(8)]).astype(complex)


def toffoli():
    T = np.zeros((8, 8), complex)
    for x in range(8):
        b = bits(x)
        if b[0] and b[2]:
            b[1] ^= 1
        T[(b[0] << 2) | (b[1] << 1) | b[2], x] = 1
    return T


TG = toffoli()


def pm(name):
    return k3({"I": I2, "X": X, "Y": Y, "Z": Z}[name[0]],
              {"I": I2, "X": X, "Y": Y, "Z": Z}[name[1]],
              {"I": I2, "X": X, "Y": Y, "Z": Z}[name[2]])


def sphere(theta, phi):
    return ((1+np.cos(theta))/2 * pm("ZXZ") + (np.cos(theta)-1)/2 * pm("ZIZ") +
            np.sin(theta)*np.cos(phi)/2 * (pm("YIZ")+pm("YXZ")) +
            np.sin(theta)*np.sin(phi)/2 * (pm("XIZ")+pm("XXZ")))


def target(theta, phi):
    return (np.cos(np.pi/8)*np.eye(8) + 1j*np.sin(np.pi/8)*sphere(theta, phi)) @ TG


def normalize_block(raw):
    mats, phase = [], 1+0j
    for layer in raw:
        row = []
        for G in layer:
            p = np.exp(0.5j*np.angle(np.linalg.det(G)))
            S = G/p
            assert abs(np.linalg.det(S)-1) < 1e-10
            row.append(S)
            phase *= p
        mats.append(row)
    return mats, phase


def wblock(theta):
    A, B = rp(np.pi/2, Z), rp(-theta/2, Y)
    C = B.conj().T @ A.conj().T
    raw = [[H@C, X@H, I2], [H@B@H, I2, I2], [A@H, H@X, I2]]
    mats, phase = normalize_block(raw)
    # 从同一规范化块生成逆，相位分支严格配对。
    dmats = [[G.conj().T for G in row] for row in mats[::-1]]
    return (mats, phase), (dmats, phase.conjugate())


def numeric_circuit(phase, mats, edges):
    U = phase * k3(*mats[-1])
    for j in range(len(edges)-1, -1, -1):
        U = U @ cz(edges[j]) @ k3(*mats[j])
    return U


def raw_w_numeric(theta):
    """绕开归一化块，直接重乘原始 2-CZ 分解，作为已知答案。"""
    A, B = rp(np.pi/2, Z), rp(-theta/2, Y)
    C = B.conj().T @ A.conj().T
    raw = [[H@C, X@H, I2], [H@B@H, I2, I2], [A@H, H@X, I2]]
    W = k3(*raw[2]) @ cz((0, 1)) @ k3(*raw[1]) @ cz((0, 1)) @ k3(*raw[0])
    return W


def clone_layers(layers):
    # φ 吸收只允许改动本次拼接副本，禁止写回 W/W†/endpoint 共享层。
    return [[G.copy() for G in row] for row in layers]


def layers_max_delta(a, b):
    return max(float(np.max(abs(x-y))) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def w_block_known_answer_gate():
    records = []
    for th in (0.0, np.pi/11, 1.17):
        expected = raw_w_numeric(th)
        (w, phase), (wd, dphase) = wblock(th)
        ew = float(np.max(abs(numeric_circuit(phase, w, [(0, 1), (0, 1)])-expected)))
        ewd = float(np.max(abs(numeric_circuit(dphase, wd, [(0, 1), (0, 1)])-expected.conj().T)))
        ep = float(abs(phase*dphase-1))
        assert max(ew, ewd, ep) < 2e-10, (th, ew, ewd, ep)
        records.append({"theta": float(th), "w_max_abs": ew, "w_dagger_max_abs": ewd,
                        "phase_pair_error": ep})
    return {"status": "W_AND_W_DAGGER_RAW_KNOWN_ANSWER_PASS", "cases": records}


def independent_grid(src):
    block_gate = w_block_known_answer_gate()  # 先证归一化块本身，再拼未知目标。
    base = [[su2(np.asarray(t)*np.pi/4) for t in layer] for layer in src["local_angles_pi_over_4"]]
    base_snapshot = clone_layers(base)
    edges = [(0, 1), (0, 1)] + [tuple(e) for e in src["edges"]] + [(0, 1), (0, 1)]
    thetas = [0.0, np.pi/11, np.pi/5, 2*np.pi/3, np.pi]
    phis = [-2.7, -0.83, 0.19, 1.21, 2.94]
    records = []
    mutation_max = 0.0
    block_rebuild_max = 0.0
    for th in thetas:
        (w, wp), (wd, wdp) = wblock(th)
        w_snapshot, wd_snapshot = clone_layers(w), clone_layers(wd)
        expected_w = raw_w_numeric(th)
        ew = float(np.max(abs(numeric_circuit(wp, w, [(0, 1), (0, 1)])-expected_w)))
        ewd = float(np.max(abs(numeric_circuit(wdp, wd, [(0, 1), (0, 1)])-expected_w.conj().T)))
        block_rebuild_max = max(block_rebuild_max, ew, ewd)
        assert max(ew, ewd) < 2e-10, (th, ew, ewd)
        for ph in phis:
            mats = clone_layers(wd[:2]) + [[base[0][q] @ wd[2][q] for q in range(3)]]
            mats += clone_layers(base[1:7])
            mats += [[w[0][q] @ base[7][q] for q in range(3)]] + clone_layers(w[1:])
            Rphi = rp(ph, Z)
            mats[0][0] = mats[0][0] @ Rphi.conj().T
            mats[-1][0] = Rphi @ mats[-1][0]
            phase = np.exp(1j*src["phase_pi_over_8"]*np.pi/8) * wp * wdp
            U = numeric_circuit(phase, mats, edges)
            e = float(np.max(abs(U-target(th, ph))))
            assert e < 2e-10, (th, ph, e)
            records.append({"theta": float(th), "phi": ph, "max_abs": e})
        # 旧缺陷会在每个 φ 点原地改写 w[-1][0] 与 wd[0][0]；此门必须为零。
        mutation_max = max(mutation_max, layers_max_delta(w, w_snapshot),
                           layers_max_delta(wd, wd_snapshot), layers_max_delta(base, base_snapshot))
        ew_post = float(np.max(abs(numeric_circuit(wp, w, [(0, 1), (0, 1)])-expected_w)))
        ewd_post = float(np.max(abs(numeric_circuit(wdp, wd, [(0, 1), (0, 1)])-expected_w.conj().T)))
        block_rebuild_max = max(block_rebuild_max, ew_post, ewd_post)
        assert max(ew_post, ewd_post) < 2e-10, (th, ew_post, ewd_post)
    assert mutation_max == 0.0, mutation_max
    return {"points": len(records), "max_abs": max(r["max_abs"] for r in records),
            "w_block_known_answer_gate": block_gate,
            "shared_layer_mutation_max": mutation_max,
            "w_block_pre_post_rebuild_max": block_rebuild_max,
            "records": records, "role": "corroboration only; arbitrary-angle proof is symbolic"}


def main():
    known = known_numeric_gate()  # 已知答案必须先于未知目标。
    exact_gate = exact_known_gate()
    src = json.loads(ENDPOINT.read_text())
    zero = json.loads(THETA0.read_text())
    assert hashlib.sha256(ENDPOINT.read_bytes()).hexdigest() == "ec0f942e4a5404daaf5476126d93f27a00eb7821a056c77c9025b806203065ce"
    symbolic = symbolic_identities()
    exact = verify_theta0_exact(src, zero)
    numeric = independent_grid(src)
    out = {
        "beat": "AD-25",
        "status": "S2_FULL_SPHERE_11CZ_INDEPENDENT_L1_PASS",
        "independence": "no constructor, solver, AD-23 exact module, or AD-24 verifier imported; rebuilt from raw endpoint and integer angles",
        "known_answer_gate_first": known,
        "exact_field_known_answer_gate": exact_gate,
        "symbolic": symbolic,
        "theta0_exact": exact,
        "numeric_crosscheck": numeric,
        "strict_conclusion": "序34整个S²存在11-CZ PATH解析实现；theta=0端点另有7-CZ。11-CZ最优性、全theta 7-CZ与11到9/7消门均仍未解决。",
        "input_sha256": {
            "ad24_s2_exact.json": hashlib.sha256(ENDPOINT.read_bytes()).hexdigest(),
            "ad25_s2_theta0_11cz_exact.json": hashlib.sha256(THETA0.read_bytes()).hexdigest(),
        },
        "private_ci_consumption": 0,
        "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad25_s2_independent.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "symbolic": symbolic["nonzero_after_normal_form"],
                      "theta0_exact": exact["status"], "numeric_points": numeric["points"],
                      "numeric_max_abs": numeric["max_abs"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
