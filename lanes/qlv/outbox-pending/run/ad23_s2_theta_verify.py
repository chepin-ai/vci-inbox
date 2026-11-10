"""AD-23 序34经线独立复验；不导入构造器、规范器或 AD-22 模块。"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

RUN = Path(__file__).resolve().parent
R21 = RUN.parent.parent / "ad21/run"
I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
EDGES = list(itertools.product([(0, 1), (1, 2)], repeat=7))[34]
PERM = (0, 1, 2)
SIGMA = 1
ALPHA = np.pi / 8


def su2(t):
    a, b, c = t
    rz = lambda x: np.diag([np.exp(-0.5j * x), np.exp(0.5j * x)])
    ry = np.array([[np.cos(b / 2), -np.sin(b / 2)], [np.sin(b / 2), np.cos(b / 2)]], complex)
    return rz(a) @ ry @ rz(c)


def zxz(u):
    b = 2 * np.arctan2(abs(u[1, 0]), abs(u[0, 0]))
    s, c = np.sin(b / 2), np.cos(b / 2)
    if s < 1e-12:
        a, c = -2 * np.angle(u[0, 0]), 0.0
    elif c < 1e-12:
        a, c = 2 * np.angle(u[1, 0]), 0.0
    else:
        alpha = -2 * np.angle(u[0, 0])
        beta = 2 * np.angle(u[1, 0])
        a, c = (alpha + beta) / 2, (alpha - beta) / 2
    return np.array([a, b, c])


def canonical_core(raw):
    raw = np.asarray(raw, dtype=float)
    angles = raw[1:].reshape(8, 3, 3)
    layers = [[su2(angles[i, q]) for q in range(3)] for i in range(8)]
    for i, (a, b) in enumerate(EDGES):
        idle = ({0, 1, 2} - {a, b}).pop()
        for q in (a, b):
            t = zxz(layers[i][q])
            rot = np.diag([np.exp(0.5j * t[0]), np.exp(-0.5j * t[0])])
            layers[i][q] = rot @ layers[i][q]
            layers[i + 1][q] = layers[i + 1][q] @ rot.conj().T
        g = layers[i][idle].copy()
        layers[i][idle] = g.conj().T @ layers[i][idle]
        layers[i + 1][idle] = layers[i + 1][idle] @ g
    packed = np.concatenate(([raw[0]], np.asarray([[zxz(layers[i][q]) for q in range(3)] for i in range(8)]).ravel()))
    keep = [0]
    for i, (a, b) in enumerate(EDGES):
        for q in (a, b):
            keep.extend([1 + 9 * i + 3 * q + 1, 1 + 9 * i + 3 * q + 2])
    keep.extend(range(64, 73))
    return packed[keep]


def expand(core):
    p = np.zeros(73)
    cursor = 0
    p[0] = core[cursor]
    cursor += 1
    for i, (a, b) in enumerate(EDGES):
        for q in (a, b):
            p[1 + 9 * i + 3 * q + 1:1 + 9 * i + 3 * q + 3] = core[cursor:cursor + 2]
            cursor += 2
    p[64:] = core[cursor:]
    return p


def cz(edge):
    a, b = edge
    d = np.ones(8, dtype=complex)
    for x in range(8):
        if ((x >> (2 - a)) & 1) and ((x >> (2 - b)) & 1):
            d[x] = -1
    return np.diag(d)


def circuit_from_raw(raw):
    angles = np.asarray(raw)[1:].reshape(8, 3, 3)
    layers = [np.kron(np.kron(su2(t[0]), su2(t[1])), su2(t[2])) for t in angles]
    u = np.exp(1j * raw[0]) * layers[-1]
    for j in range(6, -1, -1):
        u = u @ cz(EDGES[j]) @ layers[j]
    return u


def circuit(core):
    return circuit_from_raw(expand(core))


def toffoli(controls, target):
    out = np.zeros((8, 8), complex)
    for column in range(8):
        bits = [(column >> 2) & 1, (column >> 1) & 1, column & 1]
        if all(bits[q] for q in controls):
            bits[target] ^= 1
        out[4 * bits[0] + 2 * bits[1] + bits[2], column] = 1
    return out


def pm(name):
    return np.kron(np.kron(PAULI[name[0]], PAULI[name[1]]), PAULI[name[2]])


def sphere(theta, phi):
    # perm=(0,1,2), sigma=1 的六个基向量逐项重建。
    names = ["ZXZ", "ZIZ", "YIZ", "XIZ", "YXZ", "XXZ"]
    u = (SIGMA + np.cos(theta)) / 2
    v = (np.cos(theta) - SIGMA) / 2
    w = np.sin(theta) * np.cos(phi) / 2
    t = np.sin(theta) * np.sin(phi) / 2
    return u * pm(names[0]) + v * pm(names[1]) + w * (pm(names[2]) + pm(names[4])) + t * (pm(names[3]) + pm(names[5]))


def target(theta, phi):
    return (np.cos(ALPHA) * I8 + 1j * np.sin(ALPHA) * sphere(theta, phi)) @ toffoli({0, 2}, 1)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    summary = json.loads((RUN / "ad23_s2_theta_summary.json").read_text())
    phi = summary["phi"]
    new_path = RUN / "ad23_s2_theta.jsonl"
    new = [json.loads(s) for s in new_path.read_text().splitlines()]
    assert len(new) == 63

    old_all = [json.loads(s) for s in (R21 / "ad21_continuation.jsonl").read_text().splitlines()]
    old = sorted([r for r in old_all if r.get("case") == "G2k7_seq34" and
                  r.get("kind") == "theta_navigation" and r["e"] < 1e-8], key=lambda r: r["theta"])
    assert len(old) == 64
    old_e, old_coordinate_delta = [], []
    for r in old:
        core = canonical_core(r["x"])
        old_e.append(float(np.max(np.abs(circuit(core) - target(r["theta"], phi)))))
        old_coordinate_delta.append(abs(core[30] - (np.pi - r["theta"]) / 2))
    assert max(old_e) < 2e-12 and max(old_coordinate_delta) < 2e-14

    new_e, deltas, involution, unitary = [], [], [], []
    wrong_target_control = []
    for n, r in enumerate(new):
        assert r["interval_index"] == n
        assert r["theta"] == (r["bracket_theta"][0] + r["bracket_theta"][1]) / 2
        assert r["core30"] == (np.pi - r["theta"]) / 2
        core = np.asarray(r["x_core"], dtype=float)
        assert core.shape == (38,) and np.all(np.isfinite(core))
        rebuilt = circuit(core)
        e = float(np.max(np.abs(rebuilt - target(r["theta"], phi))))
        assert abs(e - r["e"]) < 1e-9
        new_e.append(e)
        deltas.append(abs(e - r["e"]))
        h = sphere(r["theta"], phi)
        involution.append(float(np.max(np.abs(h @ h - I8))))
        v = target(r["theta"], phi)
        unitary.append(float(np.max(np.abs(v @ v.conj().T - I8))))
        if n == 31:
            wrong_target_control.append(float(np.max(np.abs(rebuilt - target(r["theta"], phi + 0.05)))))
    assert max(new_e) < 1e-9
    assert max(involution + unitary) < 2e-12
    assert min(wrong_target_control) > 1e-3

    report = {
        "beat": "AD-23", "status": "INDEPENDENT_S2_THETA_PASS", "evidence_level": "L2 numerical only",
        "method": "raw angles -> independent gauge -> independent Pauli/Toffoli targets -> independent 8x8 circuits",
        "old_points": len(old), "old_max_e": max(old_e),
        "old_max_core30_formula_delta": max(old_coordinate_delta),
        "new_off_grid_points": len(new), "new_max_e": max(new_e),
        "new_exact_e_lt_1e-9": sum(e < 1e-9 for e in new_e),
        "max_new_record_delta": max(deltas), "max_target_involution_error": max(involution),
        "max_target_unitarity_error": max(unitary), "wrong_phi_control_e": wrong_target_control[0],
        "coordinate": {"core_index": 30, "label": "L7q0b", "formula": "(pi-theta)/2"},
        "boundary": "127个数值点与63个网格外求根不构成连续经线解析定理；单坐标公式不充分，其他核心角仍待解析化。",
        "new_raw_sha256": sha256(new_path), "summary_sha256": sha256(RUN / "ad23_s2_theta_summary.json"),
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    (RUN / "ad23_s2_theta_verify.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
