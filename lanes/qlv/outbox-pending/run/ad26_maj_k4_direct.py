"""AD-26 MAJ k=4：闭合约后直接 SLSQP，攻击增权路线跨分量问题。"""
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares, minimize
import ad26_maj_k4_branch as m

R = Path(__file__).resolve().parent


def close_then_direct(xstart, edges, target, fixed, free, self_gate=False):
    closure = least_squares(lambda c: m.branch_constraints(c, edges, fixed, free), xstart,
                            jac=lambda c: m.constraint_jac_analytic(c, edges, fixed, free),
                            method="trf", max_nfev=320,
                            ftol=1e-14, xtol=1e-14, gtol=1e-14)
    cm = m.metrics(closure.x, edges, target, fixed, free)
    cm.update({"nfev": int(closure.nfev), "status": int(closure.status),
               "optimality": float(closure.optimality)})
    def objective(c):
        f, J = m.target_fj(c, edges, target)
        return float(0.5*np.dot(f, f)), J.T@f
    options = {"maxiter": 500, "ftol": 1e-15, "disp": False}
    constraint = {"type": "eq",
                  "fun": lambda c: m.branch_constraints(c, edges, fixed, free),
                  "jac": lambda c: m.constraint_jac_analytic(c, edges, fixed, free)}
    sol = minimize(lambda c: objective(c)[0], closure.x, jac=lambda c: objective(c)[1],
                   constraints=constraint, method="SLSQP", options=options)
    total_nfev, total_nit = int(sol.nfev), int(sol.nit)
    # 同一 KKT 点重启可继续降低一阶停止残差；第二轮不是放宽容差。
    sol2 = minimize(lambda c: objective(c)[0], sol.x, jac=lambda c: objective(c)[1],
                    constraints=constraint, method="SLSQP", options=options)
    total_nfev += int(sol2.nfev)
    total_nit += int(sol2.nit)
    sol = sol2
    fm = m.metrics(sol.x, edges, target, fixed, free)
    fm.update({"nfev": total_nfev, "nit": total_nit, "status": int(sol.status),
               "objective": float(sol.fun), "message": str(sol.message),
               "slsqp_passes": 2})
    return closure.x, cm, sol.x, fm


def known_gate(tracks):
    rows = []
    worst_jac = 0.0
    for name in m.TRACKS:
        edges0 = m.seq_edges(name)
        x00 = tracks[name]["core"]
        fixed0 = (m.TRACKS[name]["fixed"][0], m.CASES[m.TRACKS[name]["fixed"][1]])
        free0 = (m.TRACKS[name]["free"][0], m.CASES[0])
        worst_jac = max(worst_jac, float(np.max(abs(
            m.constraint_jac_analytic(x00, edges0, fixed0, free0)
            - m.constraint_jac(x00, edges0, fixed0, free0)))))
    assert worst_jac < 2e-6, worst_jac
    for name in m.TRACKS:
        edges = m.seq_edges(name)
        x0 = tracks[name]["core"]
        target = m.base.circuit(m.expand(x0, edges), edges)
        # 自身已知目标必须使用原电路自身的双割数值；强制吸附到最近允许分支会使已知目标不再保证相容。
        fixed = (m.TRACKS[name]["fixed"][0], tuple(tracks[name]["initial_invariants"][m.TRACKS[name]["fixed"][0]]))
        free = (m.TRACKS[name]["free"][0], tuple(tracks[name]["initial_invariants"][m.TRACKS[name]["free"][0]]))
        rng = np.random.default_rng(26200+m.TRACKS[name]["source_idx"])
        xs = x0+1e-5*rng.normal(size=len(x0))
        xc, cm, x, fm = close_then_direct(xs, edges, target, fixed, free, True)
        assert fm["target_max_abs"] < 2e-8 and fm["constraint_inf"] < 2e-7, (name, fm)
        rows.append({"order": name, "closure": cm, "final": fm,
                     "closure_x_core": xc.tolist(), "final_x_core": x.tolist(),
                     "source_core": x0.tolist()})
    return {"analytic_constraint_jacobian_max_central_difference": worst_jac,
            "self_target_recovery": rows, "ad23_7cz": m.known_7cz_gate()}


def solve(task):
    name, free_index, kick, core = task
    begin = time.time()
    edges = m.seq_edges(name)
    fixed = (m.TRACKS[name]["fixed"][0], m.CASES[m.TRACKS[name]["fixed"][1]])
    free = (m.TRACKS[name]["free"][0], m.CASES[free_index])
    rng = np.random.default_rng(26100+100*m.TRACKS[name]["source_idx"]+10*free_index+int(kick*1000))
    xs = np.asarray(core)+kick*rng.normal(size=len(core))
    try:
        xc, cm, x, fm = close_then_direct(xs, edges, m.base.MAJ, fixed, free)
        return {"order": name, "free_case_index": free_index, "kick": kick,
                "fixed_cut": fixed[0], "free_cut": free[0],
                "closure": cm, "final": fm, "closure_x_core": xc.tolist(), "x_core": x.tolist(),
                "exact_joint_hit": bool(fm["target_max_abs"] < 1e-9 and fm["constraint_inf"] < 1e-7),
                "seconds": time.time()-begin}
    except Exception as exc:
        return {"order": name, "free_case_index": free_index, "kick": kick,
                "error": type(exc).__name__+": "+str(exc), "seconds": time.time()-begin}


def main():
    begin = time.time()
    tracks = m.load_tracks()
    gate = known_gate(tracks)
    tasks = [(name, i, kick, tracks[name]["core"])
             for name in m.TRACKS for i in range(4) for kick in (0.0, 0.02)]
    rows = []
    with ProcessPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(solve, t): (t[0], t[1], t[2]) for t in tasks}
        for n, fut in enumerate(as_completed(futs), 1):
            key = futs[fut]
            try:
                rows.append(fut.result())
            except Exception as exc:
                rows.append({"order": key[0], "free_case_index": key[1], "kick": key[2],
                             "error": type(exc).__name__+": "+str(exc)})
            print(json.dumps({"done": n, "total": len(tasks), "elapsed": time.time()-begin}), flush=True)
    rows.sort(key=lambda r: (list(m.TRACKS).index(r["order"]), r["free_case_index"], r["kick"]))
    (R/"ad26_maj_k4_direct.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    per = {}
    for name in m.TRACKS:
        rr = [r for r in rows if r["order"] == name and "error" not in r]
        assert len(rr) == 8
        closed = [r for r in rr if r["final"]["constraint_inf"] < 1e-7]
        best = min(closed if closed else rr, key=lambda r: r["final"]["target_max_abs"])
        best_closure = min(rr, key=lambda r: r["closure"]["target_max_abs"])
        per[name] = {"runs": len(rr), "final_constraint_closed_runs": len(closed),
                     "exact_joint_hits": sum(r["exact_joint_hit"] for r in rr),
                     "best_final": {"free_case_index": best["free_case_index"], "kick": best["kick"], **best["final"]},
                     "best_closure": {"free_case_index": best_closure["free_case_index"], "kick": best_closure["kick"],
                                      **best_closure["closure"]}}
    out = {"beat": "AD-26", "status": "MAJ_K4_DIRECT_CONSTRAINED_COMPLETE",
           "known_answer_gate_first": gate,
           "protocol": "same 3 tracks, 4 free branches, kicks 0/0.02 as ad26_maj_k4_branch; constraint closure with analytic d(b,t)/d(core) immediately followed by two equality-constrained SLSQP passes, without weighted-TRF basin transfer",
           "runs": len(rows), "errors": sum("error" in r for r in rows),
           "exact_joint_hits": sum(r.get("exact_joint_hit", False) for r in rows), "per_order": per,
           "evidence_level": "L2 targeted local numerical result only",
           "boundary": "与增权保割轨并集仍只覆盖指定旧轨和扰动；不证明六序或k=4全局不存在。",
           "strict_interval": "4 <= k <= 7", "private_ci_consumption": 0,
           "quantum_machine_actual_consumption_seconds": 0, "quantum_machine_launched": False,
           "quantum_account_quota_verified": False, "seconds": time.time()-begin}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/"ad26_maj_k4_direct_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "exact_joint_hits": out["exact_joint_hits"],
                      "best_final": {k: v["best_final"]["target_max_abs"] for k, v in per.items()},
                      "seconds": out["seconds"], "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
