"""AD-24 S²：端点精确证书、结构化扫描、65点经线与低阶 Fourier 闸。

L1 仅限整数角端点的精确零；所有网格/同伦/拟合结果均为 L2。
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent
R23 = R.parent.parent / "ad23/run"
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
CZ4 = np.diag([1, 1, 1, -1]).astype(complex)
PATH = [(0, 1), (1, 2)]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ex = load_module("ad24_exact_field", R23 / "ad23_exact.py")
base = load_module("ad24_numeric_base", R23.parent.parent / "ad22/run/ad22_verify.py")


def rz(a):
    return np.diag([np.exp(-0.5j * a), np.exp(0.5j * a)])


def ry(a):
    return np.array([[np.cos(a / 2), -np.sin(a / 2)], [np.sin(a / 2), np.cos(a / 2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def rp(t, P):
    return np.cos(t / 2) * I2 + 1j * np.sin(t / 2) * P


def readl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def circuit(p, edges):
    return base.circuit(np.asarray(p, float), edges)


def target(theta, phi, T):
    H0 = base.sphere((0, 1, 2), 1, theta, phi)
    return base.target_of(H0, T)


def exact_endpoint(src):
    phase = src["phase_pi_over_8"]
    angles = src["local_angles_pi_over_4"]
    edges = src["edges"]
    U = ex.circuit(phase, angles, edges)
    Zz = ex.diag2(ex.ONE, -ex.ONE)
    Xx = [[ex.Z, ex.ONE], [ex.ONE, ex.Z]]
    Ii = ex.eye(2)

    def op(q, A):
        ms = [Ii, Ii, Ii]
        ms[q] = A
        return ex.kron(ex.kron(ms[0], ms[1]), ms[2])

    H0 = ex.mm(ex.mm(op(0, Zz), op(1, Xx)), op(2, Zz))
    T = ex.toffoli({0, 2}, 1)
    w, wm = ex.wpow(1), ex.wpow(-1)
    co = (w + wm).scale(ex.F(1, 2))
    isi = (w - wm).scale(ex.F(1, 2))
    V = ex.mm([[co * a + isi * h for a, h in zip(ri, rh)] for ri, rh in zip(ex.eye(8), H0)], T)
    D = ex.md(U, V)
    nz = ex.nonzero_entries(D)
    numeric_target = np.array([[V[i][j].numeric() for j in range(8)] for i in range(8)])
    expected = target(0.0, src["phi"], base.TARGETS["G2"])
    cross = float(np.max(abs(numeric_target - expected)))
    assert nz == 0 and cross < 1e-14, (nz, cross)
    out = dict(src)
    out.update({
        "status": "ENDPOINT_ALL_EXACT_ZERO",
        "evidence_level": "L1 exact arithmetic in Q(exp(i*pi/8))",
        "exact_nonzero_residual_entries": nz,
        "exact_full_residual": "0",
        "target_numeric_crosscheck": cross,
        "exact_field": "Q(w), w=exp(i*pi/8), w^8+1=0, Fraction coefficients",
        "boundary": "仅证明theta=0端点的同边序7-CZ实现；不单独证明全theta经线或k最优。",
    })
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad24_s2_exact.json").write_bytes(raw)
    return out


def summarize_scans(src):
    out = {}
    for k in (3, 4, 5):
        rows = src[f"k{k}"]
        errors = []
        for r in rows:
            T = base.TARGETS["G2"]
            V = target(0.0, src["phi"], T)
            e = float(np.max(abs(circuit(r["x"], r["edges"]) - V)))
            errors.append(e)
            assert abs(e - r["e"]) < 2e-8, (k, e, r["e"])
        out[f"k{k}"] = {"runs": len(rows), "hits_lt_1e-9": int(sum(e < 1e-9 for e in errors)),
                         "best_independent_e": float(min(errors))}
    rows = src["k7_AA"]
    errors = [float(np.max(abs(circuit(r["x"], r["edges"]) - target(0.0, src["phi"], base.TARGETS["G2"])))) for r in rows]
    out["k7_AA"] = {"runs": len(rows), "hits_lt_1e-9": int(sum(e < 1e-9 for e in errors)),
                     "best_independent_e": float(min(errors)),
                     "hit_edges": [r["edges"] for r, e in zip(rows, errors) if e < 1e-9]}
    return out


def local_matrices(rows):
    G = np.empty((len(rows), 8, 3, 2, 2), complex)
    for i, r in enumerate(rows):
        angles = np.asarray(r["x"], float)[1:].reshape(8, 3, 3)
        for layer in range(8):
            for q in range(3):
                G[i, layer, q] = su2(angles[layer, q])
    return G


def fourier_report(rows):
    theta = np.array([r["theta"] for r in rows])
    G = local_matrices(rows)
    reports = []
    for freqs in ([0, .5, 1], [0, .25, .5, .75, 1], [0, .125, .25, .375, .5, .625, .75, .875, 1]):
        A = np.stack([np.exp(2j * f * theta) for f in freqs], axis=1)
        coef = np.linalg.lstsq(A, G.reshape(len(rows), -1), rcond=None)[0]
        error = np.max(abs((A @ coef).reshape(G.shape) - G), axis=0)
        gate_error = error.max(axis=(2, 3))
        reports.append({"frequencies": freqs, "basis": "exp(2*i*f*theta)",
                        "fit_gates_lt_1e-8": int(np.sum(gate_error < 1e-8)), "total_gates": 24,
                        "max_scalar_entry_error": float(error.max()),
                        "median_gate_error": float(np.median(gate_error)),
                        "gate_errors": gate_error.tolist()})
    return reports


def summarize_homotopy(rows, phi, frozen=False):
    T = base.TARGETS["G2"]
    rebuilt = []
    for r in rows:
        e = float(np.max(abs(circuit(r["x"], r["edges"]) - target(r["theta"], r["phi"], T))))
        assert abs(e - r["e"]) < 2e-8, (r["theta"], e, r["e"])
        rebuilt.append(e)
    out = {"points": len(rows), "hits_lt_1e-9": int(sum(e < 1e-9 for e in rebuilt)),
           "max_independent_e": float(max(rebuilt)), "max_recorded_nfev": int(max(r["nfev"] for r in rows)),
           "fourier": fourier_report(rows)}
    if frozen:
        formulas = {
            0: lambda th: 3 * np.pi / 8,
            56: lambda th: np.pi / 2 + th / 2,
            57: lambda th: np.pi / 2,
            65: lambda th: np.pi / 2 - th / 2,
        }
        deltas = {str(i): max(abs(np.asarray(r["x"])[i] - fn(r["theta"])) for r in rows) for i, fn in formulas.items()}
        assert max(deltas.values()) == 0
        out["frozen_coordinates"] = {
            "0": "phase=3*pi/8", "56": "L6q0b=pi/2+theta/2",
            "57": "L6q0c=pi/2", "65": "L7q0b=pi/2-theta/2",
            "max_abs_delta_by_raw_index": deltas,
            "status": "在其余34核心坐标重解后65/65数值闭合；坐标式仍属L2分支证据，不是全经线严格定理。",
        }
    return out


def W_decomp(theta):
    A = rp(np.pi / 2, Z)
    B = rp(-theta / 2, Y)
    C = B.conj().T @ A.conj().T
    U = rp(theta, X)
    assert np.max(abs(A @ B @ C - I2)) < 1e-12
    assert np.max(abs(A @ X @ B @ X @ C - U)) < 1e-12
    L2 = np.kron(A @ H, I2)
    L1 = np.kron(H @ B @ H, I2)
    L0 = np.kron(H @ C, I2)
    Wone = L2 @ CZ4 @ L1 @ CZ4 @ L0
    direct = np.zeros((4, 4), complex)
    for q1 in (0, 1):
        P = np.diag([1, 0]) if q1 == 0 else np.diag([0, 1])
        direct += np.kron(U if q1 else I2, P)
    Xc, Hc = np.kron(I2, X), np.kron(I2, H)
    W = Hc @ Xc @ Wone @ Xc @ Hc
    L2 = Hc @ Xc @ L2
    L0 = L0 @ Xc @ Hc
    expected = Hc @ Xc @ direct @ Xc @ Hc
    return W, [L0, L1, L2], expected


def offdiag(M):
    return float(np.max(abs(M - np.diag(np.diag(M)))))


def boundary_attack(endpoint):
    known = []
    for th in (0.1, 0.7, 1.3):
        W, layers, expected = W_decomp(th)
        known.append(float(np.max(abs(W - expected))))
    assert max(known) < 1e-12
    angles = np.asarray(endpoint["local_angles_pi_over_4"], float) * np.pi / 4
    L = [[su2(angles[i, q]) for q in range(3)] for i in range(8)]
    B7 = np.kron(L[7][0], L[7][1])
    B0 = np.kron(L[0][0], L[0][1])
    _, layers, _ = W_decomp(0.7)
    W0 = layers[0]
    defects = {}
    for side, B in (("left", W0 @ B7), ("right", B0 @ W0.conj().T)):
        N = B @ CZ4 @ B.conj().T @ CZ4
        defects[side] = {"offdiagonal_max": offdiag(N), "criterion": "N=B CZ B^dagger CZ diagonal is necessary for tested local collapse"}
    # Clifford 已知答案/边界穷举：24*24 个两比特局部门。
    cliff = []
    for a, b, c in itertools.product(range(4), repeat=3):
        U = rz(a * np.pi / 2) @ ry(b * np.pi / 2) @ rz(c * np.pi / 2)
        if not any(min(np.max(abs(U - phase * V)) for phase in (1, -1, 1j, -1j)) < 1e-8 for V in cliff):
            cliff.append(U)
    assert len(cliff) == 24
    hits = 0
    for U, V in itertools.product(cliff, repeat=2):
        L0 = np.kron(U, V)
        good = True
        for B in (L0 @ B7, B0 @ L0.conj().T):
            N = B @ CZ4 @ B.conj().T @ CZ4
            if offdiag(N) > 1e-8:
                good = False
            else:
                sv = np.linalg.svd(np.diag(N).reshape(2, 2), compute_uv=False)
                if sv[1] > 1e-8:
                    good = False
        hits += int(good)
    return {"known_answer_w_errors": known, "standard_decomposition_theta": 0.7,
            "standard_boundary_defects": defects, "clifford_boundary_cases": 576,
            "clifford_boundary_hits": hits,
            "boundary": "标准W分解及576个Clifford边界局部门均未满足双边界局部归一化；不排除非标准连续W分解或另一7-CZ模板。"}


def main():
    endpoint = exact_endpoint(json.loads((R / "ad24_s2_endpoint.json").read_text()))
    scans = json.loads((R / "ad24_s2_scans.json").read_text())
    legacy = readl(R / "ad24_s2_legacy_homotopy.jsonl")
    rows = readl(R / "ad24_s2_homotopy.jsonl")
    out = {
        "beat": "AD-24", "status": "S2_ENDPOINT_L1_AND_MERIDIAN_L2_PASS",
        "endpoint_exact": {
            "status": endpoint["status"], "exact_nonzero_residual_entries": endpoint["exact_nonzero_residual_entries"],
            "edges": endpoint["edges"], "sha256": hashlib.sha256((R / "ad24_s2_exact.json").read_bytes()).hexdigest(),
        },
        "structured_scans": summarize_scans(scans),
        "legacy_raw_homotopy": summarize_homotopy(legacy, rows[0]["phi"], frozen=False),
        "frozen_homotopy": summarize_homotopy(rows, rows[0]["phi"], frozen=True),
        "controlled_W_boundary_attack": boundary_attack(endpoint),
        "strict_conclusion": "theta=0端点7-CZ构造为L1；65点全区间数值同伦与四个冻结坐标为L2；完整解析经线仍未闭合。",
        "negative_result_boundary": "低k未命中、Fourier不闭合和边界归一化失败均只覆盖被测分支/基/分解，不是解析不存在。",
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad24_s2_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "endpoint_exact": out["endpoint_exact"],
                      "scans": out["structured_scans"],
                      "legacy_max_e": out["legacy_raw_homotopy"]["max_independent_e"],
                      "frozen_max_e": out["frozen_homotopy"]["max_independent_e"],
                      "frozen_fourier": [{k: r[k] for k in ("frequencies", "fit_gates_lt_1e-8", "max_scalar_entry_error")} for r in out["frozen_homotopy"]["fourier"]],
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
