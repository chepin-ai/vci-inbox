"""AD-25 序91秩异常诊断与38维横向核心。

AD-23 的 Euler 规范核心在基点有3个奇异三元组，解析 Jacobian 与独立
有限差分均给 rank=30；这不是物理解的零空间增至8的证据。
本件用35个精确边界规范方向的正交补构造局部线性38维横向核心。
已知答案门要求 raw rank=33、gauge rank=35、core rank=33/null=5。
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import null_space

R = Path(__file__).resolve().parent
AD21 = R.parent.parent / "ad21"
R23 = R.parent.parent / "ad23/run"
sys.path.insert(0, str(AD21))
sys.path.insert(0, str(AD21 / "run"))
import toffoli_solver as ts
import ad21_geometry as geometry
from ad21_tangent import target_of
sys.path.insert(0, str(R23))
import ad23_gauge as gauge

BASE = json.loads((AD21 / "run/ad21_seq91_base.json").read_text())
IDX = 91
SEQ = list(itertools.product(ts.PATH, repeat=7))[IDX]
T = ts.toffoli({0, 2}, 1)
H0 = geometry.sphere(tuple(BASE["perm"]), BASE["sigma"], BASE["theta"], BASE["phi"])
V0 = target_of(H0, T)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)


def raw_indices(edges):
    ix = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            for off in (1, 2):
                ix.append(1 + (i*3+q)*3 + off)
    ix.extend(range(1+9*len(edges), 1+9*(len(edges)+1)))
    assert len(ix) == 4*len(edges)+10
    return ix


RIX = raw_indices(SEQ)


def rv(a):
    a = np.asarray(a).reshape(-1)
    return np.concatenate([a.real, a.imag])


def svd_info(j, threshold=1e-7):
    u, s, vh = np.linalg.svd(j, full_matrices=True)
    rank = int(np.sum(s > threshold))
    return {"U": u, "s": s, "Vh": vh, "rank": rank,
            "Vr": vh[:rank].T, "N": vh[rank:].T, "sr": s[:rank]}


def canonical_ad23():
    p0 = np.asarray(BASE["x"], float)
    ph, layers, meta = gauge.canonicalize(p0, SEQ)
    pc = gauge.pack(ph, layers)
    assert np.max(abs(ts.U_of(pc, SEQ)-ts.U_of(p0, SEQ))) < 2e-12
    return pc


def canonical_ad22(p):
    """复写旧有界 Euler 代表，仅用于同点对照，不承接其秩断言。"""
    p = np.asarray(p, float)
    th = p[1:].reshape(-1, 3, 3)
    out = np.zeros_like(th)
    for i in range(th.shape[0]):
        for q in range(3):
            u = ts.su2(th[i, q])
            b = 2*np.arctan2(abs(u[1, 0]), abs(u[0, 0]))
            if abs(u[0, 0]) > 1e-14 and abs(u[1, 0]) > 1e-14:
                a = -np.angle(u[0, 0])+np.angle(u[1, 0])
                c = -np.angle(u[0, 0])-np.angle(u[1, 0])
            elif abs(u[1, 0]) <= 1e-14:
                b, a, c = 0., -2*np.angle(u[0, 0]), 0.
            else:
                b, a, c = np.pi, 0., 2*np.angle(u[1, 0])
            out[i, q] = [a, b, c]
    q = np.concatenate([[0.], out.reshape(-1)])
    phase = np.vdot(ts.U_of(q, SEQ).reshape(-1), ts.U_of(p, SEQ).reshape(-1))/64
    q[0] = np.angle(phase)
    return q


def random_gauge_representative(p, seed=925913):
    """用有限精确规范移动取得非奇异 Euler 代表；矩阵逐次不变。"""
    rng = np.random.default_rng(seed)
    ph, layers = gauge.unpack(p)
    layers = [[u.copy() for u in layer] for layer in layers]
    for i, (a, b) in enumerate(SEQ):
        idle = ({0, 1, 2}-{a, b}).pop()
        for q in (a, b):
            angle = float(rng.normal(scale=.23))
            layers[i][q] = ts.mRz(-angle) @ layers[i][q]
            layers[i+1][q] = layers[i+1][q] @ ts.mRz(angle)
        g = ts.su2(rng.normal(scale=.31, size=3))
        layers[i][idle] = g.conj().T @ layers[i][idle]
        layers[i+1][idle] = layers[i+1][idle] @ g
    out = gauge.pack(ph, layers)
    assert np.max(abs(ts.U_of(out, SEQ)-ts.U_of(p, SEQ))) < 2e-12
    return out


def euler_delta(theta, du):
    derivatives = ts.dsu2(theta)
    design = np.column_stack([rv(d) for d in derivatives])
    delta, _, _, _ = np.linalg.lstsq(design, rv(du), rcond=None)
    rebuilt = sum(delta[j]*derivatives[j] for j in range(3))
    err = float(np.max(abs(rebuilt-du)))
    assert err < 2e-10, (err, theta)
    return delta


def gauge_tangents(p):
    """35个解析切向量：L_i->exp(-hA)L_i, L_{i+1}->L_{i+1}exp(hA)。"""
    p = np.asarray(p, float)
    th = p[1:].reshape(8, 3, 3)
    columns, labels = [], []
    for i, (a, b) in enumerate(SEQ):
        idle = ({0, 1, 2}-{a, b}).pop()
        for q, generators in ((a, [("Z", Z)]), (b, [("Z", Z)]),
                              (idle, [("X", X), ("Y", Y), ("Z", Z)])):
            for generator_name, pauli in generators:
                generator = -.5j*pauli
                col = np.zeros(73)
                du0 = -generator @ ts.su2(th[i, q])
                du1 = ts.su2(th[i+1, q]) @ generator
                d0 = euler_delta(th[i, q], du0)
                d1 = euler_delta(th[i+1, q], du1)
                col[1+(i*3+q)*3:1+(i*3+q+1)*3] = d0
                col[1+((i+1)*3+q)*3:1+((i+1)*3+q+1)*3] = d1
                columns.append(col)
                labels.append({"boundary": i, "qubit": q,
                               "generator": generator_name})
    g = np.column_stack(columns)
    assert g.shape == (73, 35)
    return g, labels


def finite_difference_core(p, basis, h=1e-4):
    cols = []
    for j in range(basis.shape[1]):
        d = basis[:, j]*h
        du = (ts.U_of(p+d, SEQ)-ts.U_of(p-d, SEQ))/(2*h)
        cols.append(rv(du))
    return np.column_stack(cols)


def setup():
    p_ad22 = canonical_ad22(np.asarray(BASE["x"], float))
    p = random_gauge_representative(p_ad22)
    _, j_raw = ts.f_j(p, SEQ, V0.reshape(-1))
    raw = svd_info(j_raw)
    g, labels = gauge_tangents(p)
    gs = np.linalg.svd(g, compute_uv=False)
    assert np.min(gs) > 1e-7
    basis = null_space(g.T)
    assert basis.shape == (73, 38)
    core = svd_info(j_raw @ basis)
    return {"p": p, "J_raw": j_raw, "raw": raw, "G": g, "G_s": gs,
            "gauge_labels": labels, "B": basis, "J_core": j_raw @ basis,
            "core": core}


def main():
    pc = canonical_ad23()
    _, jpc = ts.f_j(pc, SEQ, V0.reshape(-1))
    canonical_raw = svd_info(jpc)
    canonical_core = svd_info(jpc[:, RIX])
    fd = finite_difference_core(pc, np.eye(73)[:, RIX])
    canonical_fd = svd_info(fd)
    th = pc[1:].reshape(8, 3, 3)
    singular = []
    for i, (a, b) in enumerate(SEQ):
        for q in (a, b):
            angles = th[i, q]
            if abs(np.sin(angles[1]/2)) < 1e-10 or abs(np.cos(angles[1]/2)) < 1e-10:
                singular.append({"layer": i, "qubit": q, "angles": angles.tolist()})

    st = setup()
    raw, core = st["raw"], st["core"]
    jg = float(np.max(abs(st["J_raw"] @ st["G"])))
    orth = float(np.max(abs(st["G"].T @ st["B"])))
    fd_trans = svd_info(finite_difference_core(st["p"], st["B"]))
    center_e = float(np.max(abs(ts.U_of(st["p"], SEQ)-V0)))
    canonical_e = float(np.max(abs(ts.U_of(pc, SEQ)-V0)))
    # 已知答案门先于任何528次未知求解。
    assert canonical_e < 1e-10 and center_e < 1e-10
    assert canonical_core["rank"] == 30 and canonical_fd["rank"] == 30
    assert len(singular) == 3
    assert raw["rank"] == 33, raw["s"][28:36]
    assert st["G"].shape == (73, 35) and np.min(st["G_s"]) > 1e-7
    assert jg < 2e-8 and orth < 1e-10
    assert core["rank"] == 33 and core["N"].shape == (38, 5), core["s"][28:36]
    assert fd_trans["rank"] == 33
    assert np.max(abs(st["J_core"] @ core["N"])) < 3e-8

    out = {
        "beat": "AD-25",
        "status": "SEQ91_RANK30_CHART_SINGULARITY_DIAGNOSED_TRANSVERSAL38_PASS",
        "target_center_error": center_e,
        "canonical_ad23": {
            "center_error": canonical_e,
            "raw73_rank": canonical_raw["rank"],
            "core38_rank": canonical_core["rank"],
            "core38_finite_difference_rank": canonical_fd["rank"],
            "core38_singular_values": canonical_core["s"].tolist(),
            "finite_difference_singular_values": canonical_fd["s"].tolist(),
            "euler_singularities": singular,
            "raw73_singular_values_28_to_35": canonical_raw["s"][28:36].tolist(),
        },
        "transversal_core": {
            "construction": "B=null_space(G^T), G=35 analytic exact-boundary-gauge tangents; p=p_generic+Bz",
            "raw73_rank": raw["rank"], "raw73_nullity": 73-raw["rank"],
            "gauge_tangent_rank": int(np.sum(st["G_s"] > 1e-7)),
            "core38_rank": core["rank"], "core38_nullity": core["N"].shape[1],
            "core38_finite_difference_rank": fd_trans["rank"],
            "core38_singular_values": core["s"].tolist(),
            "finite_difference_singular_values": fd_trans["s"].tolist(),
            "gauge_tangent_singular_values": st["G_s"].tolist(),
            "max_JG": jg, "max_GT_B": orth,
            "max_Jcore_null": float(np.max(abs(st["J_core"] @ core["N"]))),
            "center_raw": st["p"].tolist(), "basis_B": st["B"].tolist(),
        },
        "verdict": "rank30/null8是AD-23 Euler规范基点坐标的非横向奇点；不是物理零空间由5增至8的证据。横向38核心恢复rank33/null5。",
        "boundary": "秩结论是基点局部切空间结论；横向核心是局部线性规范图，不证明全局解流形维数、全局吸引盆体积或全局测地几何。",
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw_bytes = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_seq91_rank_diagnostic.json").write_bytes(raw_bytes)
    print(json.dumps({"status": out["status"],
                      "canonical_rank": canonical_core["rank"],
                      "singularities": len(singular),
                      "transversal_rank": core["rank"],
                      "transversal_null": core["N"].shape[1],
                      "max_JG": jg, "sha256": hashlib.sha256(raw_bytes).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
