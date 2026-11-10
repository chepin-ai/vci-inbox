"""AD-25 序91：38维横向核心的规范感知盆宽复测。

仅在 rank33/null5 已知答案门通过后运行12方向×11半径×2零空间开关
×2求解器=528次。频率是既定局部图与有限方向协议结果，不是全局盆体积。
"""
import hashlib
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import ad25_seq91_transversal as tr

ts = tr.ts
ae = __import__("ad21_embeddings")
IDX = tr.IDX
SEQ = tr.SEQ
T = tr.T
V0 = tr.V0
RADII = [.001, .003, .01, .03, .1, .3, 1., 2., 3., 5., 10.]
NDIR = 12


def expand(core):
    return ST["p"] + ST["B"] @ np.asarray(core, float)


def fj(core):
    f, j = ts.f_j(expand(core), SEQ, V0.reshape(-1))
    return f, j @ ST["B"]


def setup():
    st = tr.setup()
    p0 = np.zeros(38)
    j = st["J_core"]
    info = tr.svd_info(j)
    preserve = float(np.max(abs(ts.U_of(st["p"], SEQ)-V0)))
    return st, p0, j, info, preserve


ST, P0, J, INFO, PRESERVE = setup()
SVAL, VR, NULL, SR, RANK = INFO["s"], INFO["Vr"], INFO["N"], INFO["sr"], INFO["rank"]


def classify(x):
    h, angles, e = ae.H_of(x, IDX, T)
    fits = sorted((ae.fit(h, p) for p in __import__("itertools").permutations(range(3))),
                  key=lambda r: r["ansatz_max_delta"])
    f = fits[0]
    return {"direct_e_rebuilt": e,
            "angle_max_dev_rad": float(np.max(np.abs(np.abs(angles)-ae.ALPHA))),
            "H_involution_max": float(np.max(np.abs(h@h-np.eye(8)))),
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
    assert ST["raw"]["rank"] == 33 and ST["G"].shape == (73, 35)
    assert np.min(ST["G_s"]) > 1e-7
    assert np.max(abs(J@NULL)) < 3e-8
    rng = np.random.default_rng(925999)
    d = rng.normal(size=RANK)
    d /= np.linalg.norm(d)
    visible = VR @ (d/SR)
    assert abs(np.linalg.norm(J@visible)-1) < 1e-6
    return {"center_e": e0, "rank": RANK, "core_dimension": len(P0),
            "physical_null_dimension": NULL.shape[1],
            "removed_boundary_gauge_dimension": 73-len(P0),
            "raw73_rank": ST["raw"]["rank"],
            "gauge_tangent_rank": int(np.sum(ST["G_s"] > 1e-7)),
            "null_first_order_max": float(np.max(abs(J@NULL))),
            "visible_unit_norm_error": abs(np.linalg.norm(J@visible)-1),
            "center_target_preservation": PRESERVE,
            "center_signature": c0}


def solve(task):
    direction, radius, null_mode, method = task
    rng = np.random.default_rng(922000+direction)
    d = rng.normal(size=RANK)
    d /= np.linalg.norm(d)
    delta = radius*(VR @ (d/SR))
    if null_mode:
        rng2 = np.random.default_rng(925000+direction)
        z = rng2.normal(size=NULL.shape[1])
        z /= np.linalg.norm(z)
        delta = delta + 3*radius*(NULL @ z)
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
                "x_core": sol.x.tolist(), "x_raw": expand(sol.x).tolist()}
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
    gate = known_gate()
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
    (R / "ad25_seq91_transversal_metric.jsonl").write_text("".join(
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
    old22 = json.loads((tr.R.parent.parent / "ad22/run/ad22_seq91_metric_summary.json").read_text())
    oldex = json.loads((tr.R.parent.parent / "ad22/run/ad22_seq91_metric_extended_summary.json").read_text())
    out = {
        "beat": "AD-25", "status": "SEQ91_TRANSVERSAL38_METRIC_COMPLETE",
        "known_answer_gate_first": gate,
        "metric": "p=p_generic+Bz, B=null_space(G^T); delta=radius*V_r S_r^-1 d; null mode adds 3*radius*N z; N has five columns",
        "runs": len(rows), "errors": len(rows)-len(valid),
        "singular_values": SVAL.tolist(), "summary": summary, "by_radius": by_radius,
        "gauge_pairs": {"n": len(gp), "exact_agree": sum(r["exact_agree"] for r in gp),
                        "signature_agree": sum(r["signature_agree"] for r in gp), "rows": gp},
        "solver_pairs": {"n": len(sp), "exact_agree": sum(r["exact_agree"] for r in sp),
                         "signature_agree": sum(r["signature_agree"] for r in sp), "rows": sp},
        "ad22_raw73_comparison": {
            "base_runs": old22["runs"], "base_exact_returns": sum(v["exact_returns"] for v in old22["summary"].values()),
            "extended_summary_present": bool(oldex),
            "interpretation": "旧73维rank33/null40与横向38维rank33/null5相容：35个精确边界规范方向被移除；不同图和有限方向协议的频率不可直接等同。",
        },
        "rank_anomaly": "AD-23 Euler规范核心在基点rank30/null8为3处坐标奇点的非横向图伪影；不是物理零空间增至8。",
        "boundary": "38维横向核心仍是基点局部线性图与有限方向协议；不是全解流形测地距离、全局吸引盆体积或不存在证明。",
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad25_seq91_transversal_metric_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "by_radius": by_radius,
                      "gauge_exact_agree": f"{out['gauge_pairs']['exact_agree']}/{len(gp)}",
                      "solver_exact_agree": f"{out['solver_pairs']['exact_agree']}/{len(sp)}",
                      "elapsed_log_only": time.time()-start,
                      "sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
