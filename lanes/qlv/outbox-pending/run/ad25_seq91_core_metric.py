"""AD-25 序91：AD-23 全边界规范压缩后的38维核心盆宽复测。

旧73维rank33的40维零空间含35维CZ边界规范；本拍只测38维核心的物理零空间。
528次仅为既定局部坐标/求解器/方向协议，不是全局吸引盆体积。
"""
import hashlib
import itertools
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

R = Path(__file__).resolve().parent
AD21 = R.parent.parent / "ad21"
R22 = R.parent.parent / "ad22/run"
R23 = R.parent.parent / "ad23/run"
sys.path.insert(0, str(AD21))
sys.path.insert(0, str(AD21 / "run"))
import toffoli_solver as ts
import ad21_embeddings as ae
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
RADII = [.001, .003, .01, .03, .1, .3, 1., 2., 3., 5., 10.]
NDIR = 12


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


def expand(core):
    p = np.zeros(73)
    p[RIX] = core
    return p


def fj(core):
    f, J = ts.f_j(expand(core), SEQ, V0.reshape(-1))
    return f, J[:, RIX]


def setup():
    p0 = np.asarray(BASE["x"], float)
    ph, L, meta = gauge.canonicalize(p0, SEQ)
    pc = gauge.pack(ph, L)
    preserve = float(np.max(abs(ts.U_of(pc, SEQ)-ts.U_of(p0, SEQ))))
    assert preserve < 2e-12
    core = pc[RIX]
    _, J = fj(core)
    U, s, Vh = np.linalg.svd(J, full_matrices=True)
    rank = int(np.sum(s > 1e-7))
    Vr, N, sr = Vh[:rank].T, Vh[rank:].T, s[:rank]
    return core, J, U, s, Vr, N, sr, rank, preserve


P0, J, USV, SVAL, VR, NULL, SR, RANK, PRESERVE = setup()


def classify(x):
    H, angles, e = ae.H_of(x, IDX, T)
    fits = sorted((ae.fit(H, p) for p in itertools.permutations(range(3))),
                  key=lambda r: r["ansatz_max_delta"])
    f = fits[0]
    return {"direct_e_rebuilt": e,
            "angle_max_dev_rad": float(np.max(np.abs(np.abs(angles)-ae.ALPHA))),
            "H_involution_max": float(np.max(np.abs(H@H-np.eye(8)))),
            "best_perm": f["perm"], "best_sigma": f["sigma_u_minus_v"],
            "best_ansatz_max_delta": f["ansatz_max_delta"],
            "runner_up_ansatz_max_delta": fits[1]["ansatz_max_delta"]}


def signature_hit(c):
    return (c["direct_e_rebuilt"] < .205 and c["angle_max_dev_rad"] < 1e-5 and
            c["H_involution_max"] < 1e-4 and c["best_perm"] == [2, 1, 0] and
            c["best_sigma"] == -1 and c["best_ansatz_max_delta"] < 1e-4)


def known_gate():
    c0 = classify(expand(P0))
    e0 = float(np.max(abs(ts.U_of(expand(P0), SEQ)-V0)))
    assert e0 < 1e-8 and signature_hit(c0)
    assert RANK == 33 and NULL.shape == (38, 5), (RANK, NULL.shape)
    assert np.max(abs(J@NULL)) < 3e-8
    rng = np.random.default_rng(925999)
    d = rng.normal(size=RANK)
    d /= np.linalg.norm(d)
    visible = VR@(d/SR)
    assert abs(np.linalg.norm(J@visible)-1) < 1e-6
    return {"center_e": e0, "rank": RANK, "core_dimension": len(P0),
            "physical_null_dimension": NULL.shape[1],
            "removed_boundary_gauge_dimension": 73-len(P0),
            "null_first_order_max": float(np.max(abs(J@NULL))),
            "visible_unit_norm_error": abs(np.linalg.norm(J@visible)-1),
            "canonical_preservation": PRESERVE,
            "center_signature": c0}


def solve(task):
    direction, radius, null_mode, method = task
    rng = np.random.default_rng(922000+direction)
    d = rng.normal(size=RANK)
    d /= np.linalg.norm(d)
    delta = radius*(VR@(d/SR))
    if null_mode:
        rng2 = np.random.default_rng(925000+direction)
        z = rng2.normal(size=NULL.shape[1])
        z /= np.linalg.norm(z)
        delta = delta + 3*radius*(NULL@z)
    x0 = P0+delta
    raw0, _ = fj(x0)
    initial_output_norm = float(np.linalg.norm(raw0))
    initial_max = float(np.max(abs(raw0[:64]+1j*raw0[64:])))
    try:
        sol = least_squares(lambda c: fj(c)[0], x0, jac=lambda c: fj(c)[1], method=method,
                            max_nfev=2500, ftol=1e-14, xtol=1e-14, gtol=1e-14)
        e = float(np.max(abs(sol.fun[:64]+1j*sol.fun[64:])))
        c = classify(expand(sol.x))
        sig = signature_hit(c)
        return {"direction": direction, "radius": radius, "null_mode": null_mode,
                "method": method, "rank": RANK,
                "initial_output_norm": initial_output_norm, "initial_max_residual": initial_max,
                "e_target": e, "nfev": int(sol.nfev), "status": int(sol.status),
                "optimality": float(sol.optimality), "classification": c,
                "signature_hit": sig, "exact_return": bool(sig and e < 1e-8),
                "x_core": sol.x.tolist()}
    except Exception as exc:
        return {"direction": direction, "radius": radius, "null_mode": null_mode,
                "method": method, "error": type(exc).__name__+": "+str(exc),
                "signature_hit": False, "exact_return": False}


def pair_rows(valid):
    lookup = {(r["direction"], r["radius"], r["null_mode"], r["method"]): r for r in valid}
    gauge_pairs, solver_pairs = [], []
    for d in range(NDIR):
        for rad in RADII:
            for method in ["lm", "trf"]:
                a = lookup.get((d, rad, 0, method)); b = lookup.get((d, rad, 1, method))
                if a and b:
                    gauge_pairs.append({"direction": d, "radius": rad, "method": method,
                        "exact_agree": a["exact_return"] == b["exact_return"],
                        "signature_agree": a["signature_hit"] == b["signature_hit"],
                        "e_target_difference": abs(a["e_target"]-b["e_target"])})
            for nm in [0, 1]:
                a = lookup.get((d, rad, nm, "lm")); b = lookup.get((d, rad, nm, "trf"))
                if a and b:
                    solver_pairs.append({"direction": d, "radius": rad, "null_mode": nm,
                        "exact_agree": a["exact_return"] == b["exact_return"],
                        "signature_agree": a["signature_hit"] == b["signature_hit"],
                        "e_target_difference": abs(a["e_target"]-b["e_target"])})
    return gauge_pairs, solver_pairs


def main():
    start = time.time()
    gate = known_gate()  # 已知答案先于未知目标。
    tasks = [(d, rad, nm, method) for d in range(NDIR) for rad in RADII
             for nm in [0, 1] for method in ["lm", "trf"]]
    rows = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(solve, t): t for t in tasks}
        for n, fut in enumerate(as_completed(futs), 1):
            task = futs[fut]
            try:
                rows.append(fut.result())
            except Exception as exc:
                rows.append({"direction": task[0], "radius": task[1], "null_mode": task[2],
                             "method": task[3], "error": type(exc).__name__+": "+str(exc),
                             "signature_hit": False, "exact_return": False})
            if n % 48 == 0:
                print(json.dumps({"done": n, "total": len(tasks), "elapsed": time.time()-start}), flush=True)
    rows.sort(key=lambda r: (r["direction"], RADII.index(r["radius"]), r["null_mode"], r["method"]))
    (R / "ad25_seq91_core_metric.jsonl").write_text("".join(
        json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    valid = [r for r in rows if "error" not in r]
    summary = {}
    for method in ["lm", "trf"]:
        for nm in [0, 1]:
            rr = [r for r in valid if r["method"] == method and r["null_mode"] == nm]
            summary[f"{method}/null{nm}"] = {
                "n": len(rr), "exact_returns": sum(r["exact_return"] for r in rr),
                "signature_hits": sum(r["signature_hit"] for r in rr),
                "by_radius": {str(rad): {"n": sum(r["radius"] == rad for r in rr),
                    "exact_returns": sum(r["radius"] == rad and r["exact_return"] for r in rr),
                    "signature_hits": sum(r["radius"] == rad and r["signature_hit"] for r in rr)}
                    for rad in RADII}}
    by_radius = {}
    for rad in RADII:
        rr = [r for r in valid if r["radius"] == rad]
        by_radius[str(rad)] = {"n": len(rr), "exact_returns": sum(r["exact_return"] for r in rr),
                               "signature_hits": sum(r["signature_hit"] for r in rr)}
    gp, sp = pair_rows(valid)
    old22 = json.loads((R22 / "ad22_seq91_metric_summary.json").read_text())
    oldex = json.loads((R22 / "ad22_seq91_metric_extended_summary.json").read_text())
    out = {
        "beat": "AD-25", "status": "SEQ91_CORE38_METRIC_COMPLETE",
        "known_answer_gate_first": gate,
        "metric": "AD-23 canonical 38-core; delta=radius*V_r S_r^-1 d; physical null adds 3*radius*N z; N has five columns",
        "runs": len(rows), "errors": len(rows)-len(valid),
        "singular_values": SVAL.tolist(), "summary": summary, "by_radius": by_radius,
        "gauge_pairs": {"n": len(gp), "exact_agree": sum(r["exact_agree"] for r in gp),
                        "signature_agree": sum(r["signature_agree"] for r in gp), "rows": gp},
        "solver_pairs": {"n": len(sp), "exact_agree": sum(r["exact_agree"] for r in sp),
                         "signature_agree": sum(r["signature_agree"] for r in sp), "rows": sp},
        "ad22_raw73_comparison": {
            "base_runs": old22["runs"], "base_exact_returns": sum(v["exact_returns"] for v in old22["summary"].values()),
            "extended_summary_present": bool(oldex),
            "interpretation": "旧40维零空间含35维边界规范；本拍物理核心零空间为5维，频率不可直接等同。",
        },
        "boundary": "38维核心仍是基点局部坐标与有限方向协议；不是全解流形测地距离、全局吸引盆体积或不存在证明。",
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_seq91_core_metric_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "by_radius": by_radius,
                      "gauge_exact_agree": f"{out['gauge_pairs']['exact_agree']}/{len(gp)}",
                      "solver_exact_agree": f"{out['solver_pairs']['exact_agree']}/{len(sp)}",
                      "seconds": time.time()-start,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
