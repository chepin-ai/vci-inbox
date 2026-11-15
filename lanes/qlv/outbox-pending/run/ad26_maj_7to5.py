"""AD-26 MAJ：从七个 AD-23 精确证书做 7->5 双删门定向重解。

仅覆盖 7*21*2 条指定轨道；零命中不是 k=5 不存在证明。
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
sys.path.insert(0, str(R.parent.parent / "ad22/run"))
import ad22_verify as base
sys.path.insert(0, str(R.parent.parent / "ad23/run"))
import ad23_gauge as gauge
sys.path.insert(0, str(R))
import ad26_maj_prune as one


def delete_gates(phase, layers, edges, delete):
    delete = set(delete)
    nl, ne = [list(layers[0])], []
    for j, edge in enumerate(edges):
        if j in delete:
            nl[-1] = [layers[j+1][q] @ nl[-1][q] for q in range(3)]
        else:
            ne.append(edge)
            nl.append(list(layers[j+1]))
    p = np.concatenate([[phase], np.asarray([[gauge.zxz(u) for u in row] for row in nl]).reshape(-1)])
    ph, ll, _ = gauge.canonicalize(p, ne)
    pc = gauge.pack(ph, ll)
    preserve = float(np.max(abs(base.circuit(pc, ne)-base.circuit(p, ne))))
    assert preserve < 2e-11, preserve
    return ne, pc[one.raw_indices(ne)], preserve


def known_answer_gate():
    old = one.known_answer_gate()
    ph, ll, ee = one.source_hit(0)
    ne, core, preserve = delete_gates(ph, ll, ee, (0, 6))
    assert len(ne) == 5 and len(core) == 30
    # 双删门的逆操作已知答案：恢复两个 CZ 和原局部层，必须返回原精确证书。
    p = gauge.pack(ph, ll)
    restored = float(np.max(abs(base.circuit(p, ee)-base.MAJ)))
    assert restored < 2e-12
    # k=5 求解器先恢复一个人工已知电路目标；该目标只验收求解器，不是 MAJ 命中。
    known_target = base.circuit(one.expand(core, ne), ne)
    def fj(x):
        f, j = base.residual_jacobian(one.expand(x, ne), ne, known_target)
        return f, j[:, one.raw_indices(ne)]
    x0 = np.asarray(core) + 1e-4*np.sin(np.arange(len(core))+0.37)
    sol = least_squares(lambda x: fj(x)[0], x0, jac=lambda x: fj(x)[1],
                        method="lm", max_nfev=300, ftol=1e-14, xtol=1e-14, gtol=1e-14)
    known_k5 = float(np.max(abs(base.circuit(one.expand(sol.x, ne), ne)-known_target)))
    assert known_k5 < 2e-12, known_k5
    f, j = one.target_fj(core, ne)
    assert f.shape == (128,) and j.shape == (128, 30)
    old.update({"double_delete_restore_max_abs": restored,
                "double_delete_merge_max_abs": preserve,
                "known_k5_solver_max_abs": known_k5,
                "k5_residual_shape": list(f.shape), "k5_jacobian_shape": list(j.shape)})
    return old


def solve(task):
    hit, delete, kick, ne, core = task
    seed = 265000 + 1000*hit + 10*delete[0] + delete[1] + int(kick > 0)
    rng = np.random.default_rng(seed)
    x0 = np.asarray(core) + kick*rng.normal(size=len(core))
    try:
        sol = least_squares(lambda x: one.target_fj(x, ne)[0], x0,
                            jac=lambda x: one.target_fj(x, ne)[1], method="lm", max_nfev=900,
                            ftol=1e-14, xtol=1e-14, gtol=1e-14)
        p = one.expand(sol.x, ne)
        e = float(np.max(abs(base.circuit(p, ne)-base.MAJ)))
        return {"hit": hit, "deleted": list(delete), "kick": kick,
                "edges": [list(x) for x in ne], "target_max_abs": e,
                "nfev": int(sol.nfev), "status": int(sol.status),
                "optimality": float(sol.optimality), "x_core": sol.x.tolist()}
    except Exception as exc:
        return {"hit": hit, "deleted": list(delete), "kick": kick,
                "error": type(exc).__name__+": "+str(exc)}


def main():
    start = time.time()
    gate = known_answer_gate()
    tasks, max_preserve = [], 0.0
    for hit in range(7):
        ph, ll, ee = one.source_hit(hit)
        for delete in itertools.combinations(range(7), 2):
            ne, core, preserve = delete_gates(ph, ll, ee, delete)
            max_preserve = max(max_preserve, preserve)
            for kick in (0.0, 0.03):
                tasks.append((hit, delete, kick, ne, core))
    rows = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        fs = [ex.submit(solve, t) for t in tasks]
        for n, f in enumerate(as_completed(fs), 1):
            rows.append(f.result())
            if n % 42 == 0:
                print(json.dumps({"done": n, "total": len(fs), "seconds": time.time()-start}), flush=True)
    rows.sort(key=lambda r: (r["hit"], r["deleted"], r["kick"]))
    (R / "ad26_maj_7to5.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    good = [r for r in rows if "error" not in r]
    exact = [r for r in good if r["target_max_abs"] < 1e-9]
    best = min(good, key=lambda r: r["target_max_abs"])
    out = {"beat": "AD-26", "status": "MAJ_7TO5_TARGETED_COMPLETE",
           "known_answer_gate_first": gate, "merge_canonical_max_abs": max_preserve,
           "protocol": "7 exact sources x 21 pair deletions x {0,0.03} deterministic kicks; canonical 30-core; LM max_nfev=900",
           "runs": len(rows), "errors": len(rows)-len(good), "exact_numeric_hits": len(exact),
           "best": {k: best[k] for k in ("hit", "deleted", "kick", "target_max_abs", "nfev", "optimality")},
           "exact_hit_indices": [[r["hit"], r["deleted"], r["kick"]] for r in exact],
           "evidence_level": "L2 targeted local numerical search; exact hits, if any, still require algebraic certification",
           "boundary": "只覆盖AD-23七证书的147条双删轨道及指定扰动；零命中不证明k=5不存在，更不改变4<=k<=7。",
           "strict_interval": "4 <= k <= 7", "private_ci_consumption": 0,
           "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad26_maj_7to5_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "exact_numeric_hits": len(exact), "best": out["best"],
                      "seconds": time.time()-start, "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
