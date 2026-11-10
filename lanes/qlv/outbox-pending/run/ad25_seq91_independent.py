"""AD-25 序91独立验收：只用最终73维原始电路坐标重算528条。

不导入求解器、横向核心构造、嵌入分类器或旧验收器；不读取x_core作判读。
目标、H谱、六排列ansatz签名和精确返回均独立重建。
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent
BASE = json.loads((R.parent.parent / "ad21/run/ad21_seq91_base.json").read_text())
DIAG = json.loads((R / "ad25_seq91_rank_diagnostic.json").read_text())
I2 = np.eye(2, dtype=complex)
PAULI = {"I": I2, "X": np.array([[0, 1], [1, 0]], complex),
         "Y": np.array([[0, -1j], [1j, 0]], complex), "Z": np.diag([1, -1]).astype(complex)}
ALPHA = np.pi/8


def bits(x):
    return [(x >> 2) & 1, (x >> 1) & 1, x & 1]


def rz(a):
    return np.diag([np.exp(-.5j*a), np.exp(.5j*a)])


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def cz(edge):
    return np.diag([-1 if bits(x)[edge[0]] and bits(x)[edge[1]] else 1 for x in range(8)]).astype(complex)


def circuit(p, edges):
    th = np.asarray(p)[1:].reshape(len(edges)+1, 3, 3)
    layers = [np.kron(np.kron(su2(th[i, 0]), su2(th[i, 1])), su2(th[i, 2]))
              for i in range(len(edges)+1)]
    u = np.exp(1j*p[0])*layers[-1]
    for j in range(len(edges)-1, -1, -1):
        u = u @ cz(edges[j]) @ layers[j]
    return u


def toffoli():
    m = np.zeros((8, 8), complex)
    for x in range(8):
        b = bits(x)
        if b[0] and b[2]:
            b[1] ^= 1
        m[(b[0] << 2) | (b[1] << 1) | b[2], x] = 1
    return m


T = toffoli()
PATH = [(0, 1), (1, 2)]
SEQ = list(itertools.product(PATH, repeat=7))[91]


def pm(s):
    return np.kron(np.kron(PAULI[s[0]], PAULI[s[1]]), PAULI[s[2]])


def string_for(a, b, c, sa, sb, sc="Z"):
    s = ["I"]*3
    s[a], s[b], s[c] = sa, sb, sc
    return "".join(s)


def basis_names(perm):
    a, b, c = perm
    return [string_for(a, b, c, "Z", "X"), string_for(a, b, c, "Z", "I"),
            string_for(a, b, c, "Y", "I"), string_for(a, b, c, "X", "I"),
            string_for(a, b, c, "Y", "X"), string_for(a, b, c, "X", "X")]


def sphere(theta, phi):
    names = basis_names(BASE["perm"])
    sigma = BASE["sigma"]
    u, v = (sigma+np.cos(theta))/2, (np.cos(theta)-sigma)/2
    w, t = np.sin(theta)*np.cos(phi)/2, np.sin(theta)*np.sin(phi)/2
    return u*pm(names[0])+v*pm(names[1])+w*(pm(names[2])+pm(names[4]))+t*(pm(names[3])+pm(names[5]))


V0 = (np.cos(ALPHA)*np.eye(8)+1j*np.sin(ALPHA)*sphere(BASE["theta"], BASE["phi"])) @ T


def fit(h, perm):
    names = basis_names(perm)
    co = np.array([float((np.trace(pm(s)@h)/8).real) for s in names])
    u, v, w, t = co[:4]
    theta = float(np.arccos(np.clip(u+v, -1, 1)))
    phi = float(np.arctan2(t, w))
    branches = []
    for sigma in [1, -1]:
        us, vs = (sigma+np.cos(theta))/2, (np.cos(theta)-sigma)/2
        ws, ts = np.sin(theta)*np.cos(phi)/2, np.sin(theta)*np.sin(phi)/2
        h0 = us*pm(names[0])+vs*pm(names[1])+ws*(pm(names[2])+pm(names[4]))+ts*(pm(names[3])+pm(names[5]))
        branches.append({"perm": list(perm), "sigma": sigma,
                         "delta": float(np.max(abs(h-h0)))})
    return min(branches, key=lambda r: r["delta"])


def classify(u):
    vals, vecs = np.linalg.eig(u@T)
    angles = np.angle(vals)
    k = vecs @ np.diag(angles) @ np.linalg.inv(vecs)
    h = (k/ALPHA+(k/ALPHA).conj().T)/2
    fits = sorted((fit(h, p) for p in itertools.permutations(range(3))), key=lambda r: r["delta"])
    f = fits[0]
    return {"direct_e_rebuilt": float(np.max(abs(u-T))),
            "angle_max_dev_rad": float(np.max(np.abs(np.abs(angles)-ALPHA))),
            "H_involution_max": float(np.max(abs(h@h-np.eye(8)))),
            "best_perm": f["perm"], "best_sigma": f["sigma"],
            "best_ansatz_max_delta": f["delta"],
            "runner_up_ansatz_max_delta": fits[1]["delta"]}


def signature(c):
    return (c["direct_e_rebuilt"] < .205 and c["angle_max_dev_rad"] < 1e-5 and
            c["H_involution_max"] < 1e-4 and c["best_perm"] == [2, 1, 0] and
            c["best_sigma"] == -1 and c["best_ansatz_max_delta"] < 1e-4)


def known_gate():
    u = circuit(np.asarray(BASE["x"], float), SEQ)
    e = float(np.max(abs(u-V0)))
    c = classify(u)
    assert e < 1e-8 and signature(c)
    # 已知错误排列/分支必须被识别为runner-up，不得靠目标矩阵直接指定签名。
    assert c["runner_up_ansatz_max_delta"] > .1
    return {"center_e": e, "center_signature": c}


def fd_rank(center, basis=None, h=1e-5):
    center = np.asarray(center, float)
    if basis is None:
        basis = np.eye(len(center))
    cols = []
    for j in range(basis.shape[1]):
        d = basis[:, j]*h
        du = (circuit(center+d, SEQ)-circuit(center-d, SEQ))/(2*h)
        z = du.reshape(-1)
        cols.append(np.concatenate([z.real, z.imag]))
    s = np.linalg.svd(np.column_stack(cols), compute_uv=False)
    return int(np.sum(s > 1e-7)), s


def main():
    gate = known_gate()
    rows = [json.loads(s) for s in (R / "ad25_seq91_transversal_metric.jsonl").read_text().splitlines() if s.strip()]
    assert len(rows) == 528 and all("error" not in r for r in rows)
    worst = 0.
    mismatches = []
    rebuilt = []
    for n, row in enumerate(rows):
        assert len(row["x_raw"]) == 73
        u = circuit(np.asarray(row["x_raw"], float), SEQ)
        e = float(np.max(abs(u-V0)))
        c = classify(u)
        sig = signature(c)
        exact = bool(sig and e < 1e-8)
        worst = max(worst, abs(e-row["e_target"]))
        if sig != row["signature_hit"] or exact != row["exact_return"]:
            mismatches.append({"row": n, "direction": row["direction"], "radius": row["radius"],
                               "method": row["method"], "null_mode": row["null_mode"],
                               "stored": [row["signature_hit"], row["exact_return"]],
                               "rebuilt": [sig, exact]})
        rebuilt.append({**{k: row[k] for k in ("direction", "radius", "method", "null_mode")},
                        "e": e, "sig": sig, "exact": exact})
    assert not mismatches, mismatches[:5]
    by_radius = {}
    for rad in sorted(set(r["radius"] for r in rebuilt)):
        rr = [r for r in rebuilt if r["radius"] == rad]
        by_radius[str(rad)] = {"n": len(rr), "exact_returns": sum(r["exact"] for r in rr),
                               "signature_hits": sum(r["sig"] for r in rr)}
    summary = json.loads((R / "ad25_seq91_transversal_metric_summary.json").read_text())
    assert by_radius == summary["by_radius"]
    center = np.asarray(DIAG["transversal_core"]["center_raw"], float)
    basis = np.asarray(DIAG["transversal_core"]["basis_B"], float)
    raw_rank, raw_s = fd_rank(center)
    core_rank, core_s = fd_rank(center, basis)
    assert raw_rank == 33 and core_rank == 33
    out = {"beat": "AD-25", "status": "SEQ91_528_RAW_CIRCUITS_INDEPENDENT_PASS",
           "known_answer_gate_first": gate, "runs": len(rows),
           "max_target_rebuild_difference": worst, "signature_mismatches": len(mismatches),
           "exact_returns": sum(r["exact"] for r in rebuilt), "by_radius": by_radius,
           "finite_difference_rank_check": {"raw73_rank": raw_rank, "core38_rank": core_rank,
               "core38_nullity": 38-core_rank,
               "raw_boundary_singular_values": raw_s[30:35].tolist(),
               "core_boundary_singular_values": core_s[30:36].tolist(),
               "note": "只复核横向代表和最终电路；rank30的Euler规范伪影由单独诊断件承担。"},
           "boundary": "528条最终电路及签名独立一致；有限方向局部协议仍不是全局basin体积或测地几何。",
           "private_ci_consumption": 0, "quantum_machine_consumption": 0}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_seq91_independent.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows),
                      "exact_returns": out["exact_returns"], "mismatches": len(mismatches),
                      "raw_rank": raw_rank, "core_rank": core_rank,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
