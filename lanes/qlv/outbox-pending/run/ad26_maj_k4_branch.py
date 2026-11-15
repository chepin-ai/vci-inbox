"""AD-26 MAJ k=4：固定已满足割的分阶段 TRF/SLSQP 定向续解。

只使用 ABAB、ABBA、BABA 的 AD-22 本序最佳旧轨；不重启六序扫描。
先跑已知答案门，再闭合双割约束，最后延续目标。零命中只覆盖本文件登记的轨道。
"""
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import least_squares, minimize

R = Path(__file__).resolve().parent
R22 = R.parent.parent / "ad22/run"
R23 = R.parent.parent / "ad23/run"
sys.path.insert(0, str(R22))
import ad22_verify as base
sys.path.insert(0, str(R23))
import ad23_gauge as gauge

A, B = (0, 1), (1, 2)
I2 = np.eye(2, dtype=complex)
Z = np.diag([1, -1]).astype(complex)
CASES = [(np.pi/3, 0.0), (np.pi/2, -2.0), (np.pi/2, 2.0), (2*np.pi/3, 0.0)]
# fixed=(割名, 已满足分支下标)；free 为另一割。
TRACKS = {
    "ABAB": {"fixed": ("B", 1), "free": "A", "source_idx": 5, "source_restart": 7},
    "ABBA": {"fixed": ("A", 2), "free": "B", "source_idx": 6, "source_restart": 1},
    "BABA": {"fixed": ("A", 1), "free": "B", "source_idx": 10, "source_restart": 6},
}


def seq_edges(name):
    return [A if x == "A" else B for x in name]


def raw_indices(edges):
    ix = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            for off in (1, 2):
                ix.append(1 + (i*3+q)*3 + off)
    ix.extend(range(1+9*len(edges), 1+9*(len(edges)+1)))
    assert len(ix) == 4*len(edges)+10
    return ix


def expand(core, edges):
    p = np.zeros(1+9*(len(edges)+1))
    p[raw_indices(edges)] = core
    return p


def middle(L, edges, edge, cutq):
    pos = [i for i, e in enumerate(edges) if e == edge]
    assert len(pos) == 2
    i, j = pos
    rest = [q for q in range(3) if q != cutq]
    M = np.eye(2, dtype=complex)
    V = np.eye(4, dtype=complex)
    for l in range(i+1, j+1):
        M = L[l][cutq] @ M
        V = np.kron(L[l][rest[0]], L[l][rest[1]]) @ V
        if l < j:
            assert edges[l] != edge
            V = np.diag([1, 1, 1, -1]).astype(complex) @ V
    angles = gauge.zxz(M)
    Zrest = np.kron(Z, I2) if cutq == 0 else np.kron(I2, Z)
    t = float(np.trace(V @ Zrest @ V.conj().T @ Zrest).real)
    return float(angles[1]), t


def invariants(core, edges):
    _, L = gauge.unpack(expand(core, edges))
    return {"A": middle(L, edges, A, 0), "B": middle(L, edges, B, 2)}


def branch_constraints(core, edges, fixed, free):
    # fixed/free=(割名,(b,t))；顺序固定，便于独立复算。
    inv = invariants(core, edges)
    out = []
    for cut, case in (fixed, free):
        b, t = inv[cut]
        out.extend([b-case[0], t-case[1]])
    return np.asarray(out, float)


def constraint_jac(core, edges, fixed, free):
    h = 2e-6
    cols = []
    for i in range(len(core)):
        d = np.zeros(len(core))
        d[i] = h
        cols.append((branch_constraints(core+d, edges, fixed, free)
                     - branch_constraints(core-d, edges, fixed, free))/(2*h))
    return np.asarray(cols).T


def su2_with_derivative(t):
    a, b, c = t
    dra = np.diag([-0.5j*np.exp(-0.5j*a), 0.5j*np.exp(0.5j*a)])
    drb = np.array([[-0.5*np.sin(b/2), -0.5*np.cos(b/2)],
                    [0.5*np.cos(b/2), -0.5*np.sin(b/2)]])
    drc = np.diag([-0.5j*np.exp(-0.5j*c), 0.5j*np.exp(0.5j*c)])
    return [dra@base.ry(b)@base.rz(c), base.rz(a)@drb@base.rz(c), base.rz(a)@base.ry(b)@drc]


def middle_analytic_jac(core, edges, edge, cutq, deriv_param):
    """直接对 M,V 乘积求导；deriv_param 是完整46维向量的坐标下标。"""
    p = expand(core, edges)
    th = p[1:].reshape(len(edges)+1, 3, 3)
    L = [[base.su2(th[i, q]) for q in range(3)] for i in range(len(edges)+1)]
    i, j = [n for n, e in enumerate(edges) if e == edge]
    rest = [q for q in range(3) if q != cutq]
    M = np.eye(2, dtype=complex)
    V = np.eye(4, dtype=complex)
    dM = np.zeros((2, 2), complex)
    dV = np.zeros((4, 4), complex)
    layer_d = q_d = comp_d = None
    if deriv_param > 0:
        z = deriv_param-1
        layer_d, q_d, comp_d = z//9, (z%9)//3, z%3
    for l in range(i+1, j+1):
        dL = su2_with_derivative(th[l, cutq])[comp_d] if l == layer_d and q_d == cutq else np.zeros((2, 2), complex)
        dM = dL@M + L[l][cutq]@dM
        M = L[l][cutq]@M
        dlr = np.zeros((2, 2), complex)
        if l == layer_d and q_d in rest:
            dlr = su2_with_derivative(th[l, q_d])[comp_d]
        parts = [L[l][rest[0]], L[l][rest[1]]]
        dparts = [dlr if q_d == rest[0] else np.zeros((2, 2), complex),
                  dlr if q_d == rest[1] else np.zeros((2, 2), complex)]
        LV = np.kron(parts[0], parts[1])
        dLV = np.kron(dparts[0], parts[1])+np.kron(parts[0], dparts[1])
        dV = dLV@V + LV@dV
        V = LV@V
        if l < j:
            C4 = np.diag([1, 1, 1, -1]).astype(complex)
            dV = C4@dV
            V = C4@V
    x, y = abs(M[0, 0]), abs(M[1, 0])
    b = 2*np.arctan2(y, x)
    if min(x, y) < 1e-12:
        raise ValueError("analytic b derivative at ZXZ singular point")
    dx = np.real(np.conj(M[0, 0])*dM[0, 0])/x
    dy = np.real(np.conj(M[1, 0])*dM[1, 0])/y
    db = 2*(x*dy-y*dx)/(x*x+y*y)
    Zrest = np.kron(Z, I2) if cutq == 0 else np.kron(I2, Z)
    t = float(np.trace(V@Zrest@V.conj().T@Zrest).real)
    dt = 2*float(np.real(np.trace(dV@Zrest@V.conj().T@Zrest)))
    return b, t, db, dt


def constraint_jac_analytic(core, edges, fixed, free):
    nfull = 1+9*(len(edges)+1)
    J = np.zeros((4, nfull))
    for row, (cut, _) in enumerate((fixed, free)):
        edge, cutq = (A, 0) if cut == "A" else (B, 2)
        for col in range(nfull):
            try:
                _, _, db, dt = middle_analytic_jac(core, edges, edge, cutq, col)
            except ValueError:
                h = 2e-6
                d = np.zeros(nfull)
                d[col] = h
                def at_full(pp):
                    cc = pp[raw_indices(edges)]
                    return invariants(cc, edges)[cut]
                bp, tp = at_full(expand(core, edges)+d)
                bm, tm = at_full(expand(core, edges)-d)
                db, dt = (bp-bm)/(2*h), (tp-tm)/(2*h)
            J[2*row, col] = db
            J[2*row+1, col] = dt
    return J[:, raw_indices(edges)]


def target_fj(core, edges, target):
    f, J = base.residual_jacobian(expand(core, edges), edges, target)
    return f, J[:, raw_indices(edges)]


def metrics(core, edges, target, fixed, free):
    e = float(np.max(abs(base.circuit(expand(core, edges), edges)-target)))
    cv = branch_constraints(core, edges, fixed, free)
    return {"target_max_abs": e, "constraint_inf": float(np.max(abs(cv))),
            "constraint_vector": cv.tolist(), "invariants": invariants(core, edges)}


def continuation(core, edges, target, fixed, free, max_nfev=240, slsqp_iter=220):
    """约束先闭合；随后增权 TRF；最后等式约束 SLSQP。保存每段指标。"""
    x = np.asarray(core, float).copy()
    history = []
    try:
        sol = least_squares(lambda c: branch_constraints(c, edges, fixed, free), x,
                            jac=lambda c: constraint_jac(c, edges, fixed, free),
                            method="trf", max_nfev=max_nfev,
                            ftol=1e-14, xtol=1e-14, gtol=1e-14)
        x = sol.x
        m = metrics(x, edges, target, fixed, free)
        m.update({"stage": "constraint_closure", "nfev": int(sol.nfev),
                  "status": int(sol.status), "optimality": float(sol.optimality)})
        history.append(m)
        for weight in (1.0, 10.0, 100.0, 1000.0):
            def fun(c):
                return np.concatenate([target_fj(c, edges, target)[0],
                                       weight*branch_constraints(c, edges, fixed, free)])
            def jac(c):
                return np.vstack([target_fj(c, edges, target)[1],
                                  weight*constraint_jac(c, edges, fixed, free)])
            sol = least_squares(fun, x, jac=jac, method="trf", max_nfev=max_nfev,
                                ftol=1e-14, xtol=1e-14, gtol=1e-14)
            x = sol.x
            m = metrics(x, edges, target, fixed, free)
            m.update({"stage": f"joint_trf_w{weight:g}", "nfev": int(sol.nfev),
                      "status": int(sol.status), "optimality": float(sol.optimality)})
            history.append(m)
        # 在最后一站直接以 ||f||² 为目标、双割四式为等式约束。
        def objective(c):
            f, J = target_fj(c, edges, target)
            return float(0.5*np.dot(f, f)), J.T@f
        sol = minimize(lambda c: objective(c)[0], x, jac=lambda c: objective(c)[1],
                       constraints={"type": "eq",
                                    "fun": lambda c: branch_constraints(c, edges, fixed, free),
                                    "jac": lambda c: constraint_jac(c, edges, fixed, free)},
                       method="SLSQP", options={"maxiter": slsqp_iter, "ftol": 1e-13, "disp": False})
        x = sol.x
        m = metrics(x, edges, target, fixed, free)
        m.update({"stage": "joint_slsqp", "nfev": int(sol.nfev), "nit": int(sol.nit),
                  "status": int(sol.status), "optimality": float(sol.fun),
                  "message": str(sol.message)})
        history.append(m)
        candidates = [h for h in history if h["constraint_inf"] < 1e-7]
        if candidates:
            best = min(candidates, key=lambda h: h["target_max_abs"])
        else:
            best = min(history, key=lambda h: h["target_max_abs"]+100*h["constraint_inf"])
        # best 对应的坐标需重跑到该阶段之外不可恢复，因此始终保存最终坐标；
        # 若历史最佳不是最终站，则按最小复合指标选最终或闭合约，不冒充历史最佳坐标。
        final = history[-1]
        chosen = final if best is final else best
        if chosen is not final:
            # 重放至最佳阶段，保证坐标与指标一一对应。
            x2 = np.asarray(core, float).copy()
            sol2 = least_squares(lambda c: branch_constraints(c, edges, fixed, free), x2,
                                 jac=lambda c: constraint_jac(c, edges, fixed, free),
                                 method="trf", max_nfev=max_nfev,
                                 ftol=1e-14, xtol=1e-14, gtol=1e-14)
            x2 = sol2.x
            if chosen["stage"] != "constraint_closure":
                upto = ["joint_trf_w1", "joint_trf_w10", "joint_trf_w100", "joint_trf_w1000"].index(chosen["stage"])
                for weight in (1.0, 10.0, 100.0, 1000.0)[:upto+1]:
                    def fun2(c):
                        return np.concatenate([target_fj(c, edges, target)[0],
                                               weight*branch_constraints(c, edges, fixed, free)])
                    def jac2(c):
                        return np.vstack([target_fj(c, edges, target)[1],
                                          weight*constraint_jac(c, edges, fixed, free)])
                    sol2 = least_squares(fun2, x2, jac=jac2, method="trf", max_nfev=max_nfev,
                                         ftol=1e-14, xtol=1e-14, gtol=1e-14)
                    x2 = sol2.x
            check = metrics(x2, edges, target, fixed, free)
            assert abs(check["target_max_abs"]-chosen["target_max_abs"]) < 1e-8
            assert abs(check["constraint_inf"]-chosen["constraint_inf"]) < 1e-7
            x = x2
        return x, chosen, history, None
    except Exception as exc:
        return x, None, history, type(exc).__name__+": "+str(exc)


def load_tracks():
    rows = [json.loads(s) for s in (R22/"ad22_maj_multistart.jsonl").read_text().splitlines() if s.strip()]
    out = {}
    for name, tr in TRACKS.items():
        edges = seq_edges(name)
        candidates = [r for r in rows if r.get("k") == 4 and "error" not in r
                      and [tuple(e) for e in r["edges"]] == edges]
        assert len(candidates) == 8
        best = min(candidates, key=lambda r: r["e"])
        assert best["idx"] == tr["source_idx"] and best["restart"] == tr["source_restart"]
        p = np.asarray(best["x"], float)
        ph, L, _ = gauge.canonicalize(p, edges)
        pc = gauge.pack(ph, L)
        assert np.max(abs(base.circuit(pc, edges)-base.circuit(p, edges))) < 2e-12
        core = pc[raw_indices(edges)]
        inv = invariants(core, edges)
        fixed_case = CASES[tr["fixed"][1]]
        fixed_err = max(abs(inv[tr["fixed"][0]][0]-fixed_case[0]),
                        abs(inv[tr["fixed"][0]][1]-fixed_case[1]))
        assert fixed_err < 1e-5, (name, fixed_err, inv)
        out[name] = {"core": core, "source_e": float(best["e"]), "initial_invariants": inv,
                     "source_idx": best["idx"], "source_restart": best["restart"],
                     "fixed_branch_error": fixed_err}
    return out


def known_7cz_gate():
    src = json.loads((R23/"ad23_maj_7cz_exact.json").read_text())["hits"]
    worst = 0.0
    for h in src:
        p = np.concatenate([[h["phase_pi_over_8"]*np.pi/8],
                            np.asarray(h["local_angles_pi_over_4"]).reshape(-1)*np.pi/4])
        worst = max(worst, float(np.max(abs(base.circuit(p, h["edges"])-base.MAJ))))
    assert len(src) == 7 and worst < 2e-12
    return {"ad23_hits": len(src), "max_abs": worst}


def known_continuation_gate(tracks):
    """每条旧轨以自身电路为已知目标；小扰动后必须恢复，不冒充 MAJ 命中。"""
    rows = []
    for name, tr in tracks.items():
        edges = seq_edges(name)
        x0 = tr["core"]
        target = base.circuit(expand(x0, edges), edges)
        # 自身已知目标使用原电路实测双割；允许分支吸附只用于未知 MAJ 轨道。
        fixed = (TRACKS[name]["fixed"][0], tuple(tr["initial_invariants"][TRACKS[name]["fixed"][0]]))
        free = (TRACKS[name]["free"][0], tuple(tr["initial_invariants"][TRACKS[name]["free"][0]]))
        rng = np.random.default_rng(26000+TRACKS[name]["source_idx"])
        xstart = x0 + 1e-5*rng.normal(size=len(x0))
        x, best, history, error = continuation(xstart, edges, target, fixed, free,
                                                max_nfev=180, slsqp_iter=160)
        assert error is None, (name, error)
        rebuilt = metrics(x, edges, target, fixed, free)
        assert rebuilt["target_max_abs"] < 2e-8 and rebuilt["constraint_inf"] < 2e-7, (name, rebuilt)
        rows.append({"order": name, "target": "own_old_circuit_known_answer",
                     "start_perturbation_inf": float(np.max(abs(xstart-x0))),
                     "source_core": x0.tolist(), "recovered_x_core": np.asarray(x).tolist(),
                     "final": rebuilt, "stages": [h["stage"] for h in history]})
    # 改角反例：同一验收器必须能判非零。
    name = "ABAB"
    edges = seq_edges(name)
    x = tracks[name]["core"].copy()
    x[1] += np.pi/8
    counter = float(np.max(abs(base.circuit(expand(x, edges), edges)-base.MAJ)))
    assert counter > 1e-3
    return {"self_target_recovery": rows, "changed_angle_counterexample_max_abs": counter}


def solve_task(task):
    name, free_index, kick, core = task
    start = time.time()
    edges = seq_edges(name)
    fixed = (TRACKS[name]["fixed"][0], CASES[TRACKS[name]["fixed"][1]])
    free = (TRACKS[name]["free"][0], CASES[free_index])
    rng = np.random.default_rng(26100+100*TRACKS[name]["source_idx"]+10*free_index+int(kick*1000))
    xstart = np.asarray(core)+kick*rng.normal(size=len(core))
    x, best, history, error = continuation(xstart, edges, base.MAJ, fixed, free)
    row = {"order": name, "fixed_cut": fixed[0], "fixed_case": list(fixed[1]),
           "free_cut": free[0], "free_case_index": free_index,
           "free_case": [free[1][0]/np.pi, free[1][1]], "kick": kick,
           "history": history, "seconds": time.time()-start}
    if error is not None:
        row["error"] = error
    else:
        row.update(best)
        row["x_core"] = np.asarray(x).tolist()
        row["exact_joint_hit"] = bool(row["target_max_abs"] < 1e-9 and row["constraint_inf"] < 1e-7)
    return row


def main():
    begin = time.time()
    gate7 = known_7cz_gate()
    tracks = load_tracks()
    gate = known_continuation_gate(tracks)
    tasks = [(name, i, kick, tracks[name]["core"])
             for name in TRACKS for i in range(len(CASES)) for kick in (0.0, 0.02)]
    rows = []
    with ProcessPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(solve_task, t): (t[0], t[1], t[2]) for t in tasks}
        for n, fut in enumerate(as_completed(futs), 1):
            key = futs[fut]
            try:
                rows.append(fut.result())
            except Exception as exc:
                rows.append({"order": key[0], "free_case_index": key[1], "kick": key[2],
                             "error": type(exc).__name__+": "+str(exc)})
            print(json.dumps({"done": n, "total": len(tasks), "elapsed": time.time()-begin}), flush=True)
    rows.sort(key=lambda r: (list(TRACKS).index(r["order"]), r["free_case_index"], r["kick"]))
    (R/"ad26_maj_k4_branch.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    per = {}
    for name in TRACKS:
        rr = [r for r in rows if r["order"] == name and "error" not in r]
        assert len(rr) == 8
        closed = [r for r in rr if r["constraint_inf"] < 1e-7]
        pool = closed if closed else rr
        best = min(pool, key=lambda r: r["target_max_abs"])
        per[name] = {
            "source_idx": tracks[name]["source_idx"], "source_restart": tracks[name]["source_restart"],
            "source_e": tracks[name]["source_e"], "initial_invariants": tracks[name]["initial_invariants"],
            "fixed_branch_error": tracks[name]["fixed_branch_error"],
            "runs": len(rr), "constraint_closed_runs": len(closed),
            "exact_joint_hits": sum(r["exact_joint_hit"] for r in rr),
            "best": {k: best[k] for k in ("free_case_index", "kick", "target_max_abs", "constraint_inf", "invariants")},
        }
    hits = [r for r in rows if "error" not in r and r["exact_joint_hit"]]
    out = {
        "beat": "AD-26", "status": "MAJ_K4_BRANCH_PRESERVING_CONTINUATION_COMPLETE",
        "known_answer_gate_first": {"ad23_7cz": gate7, "branch_continuation": gate},
        "protocol": "3 preselected orders; fixed already-satisfied cut; 4 free-cut branches; kicks 0 and 0.02; constraint TRF then weighted TRF w=1,10,100,1000 then equality-constrained SLSQP",
        "runs": len(rows), "errors": sum("error" in r for r in rows),
        "exact_joint_hits": len(hits), "per_order": per,
        "evidence_level": "L2 targeted local numerical result only",
        "boundary": "仅覆盖ABAB/ABBA/BABA三条指定旧轨的保割续解、四自由割分支与两种确定性扰动；不覆盖AABB/BAAB/BBAA新轨，不证明任何边序或k=4全局不存在。",
        "strict_interval": "4 <= k <= 7",
        "private_ci_consumption": 0, "quantum_machine_actual_consumption_seconds": 0,
        "quantum_machine_launched": False, "quantum_account_quota_verified": False,
        "seconds": time.time()-begin,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R/"ad26_maj_k4_branch_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "exact_joint_hits": len(hits),
                      "per_order": {k: v["best"] for k, v in per.items()},
                      "seconds": out["seconds"], "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
