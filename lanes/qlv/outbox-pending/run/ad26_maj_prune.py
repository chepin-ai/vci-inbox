"""AD-26 MAJ：从 AD-23 精确 7-CZ 证书定向删门并重解。

不重复 AD-22 低起点扫描。零命中只覆盖本协议轨道，不是不存在证明。
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
R22 = R.parent.parent / "ad22/run"
R23 = R.parent.parent / "ad23/run"
sys.path.insert(0, str(R22))
import ad22_verify as base
sys.path.insert(0, str(R23))
import ad23_gauge as gauge

A, B = (0, 1), (1, 2)


def raw_indices(edges):
    ix = [0]
    for i, (a, b) in enumerate(edges):
        for q in (a, b):
            ix.extend([1 + (i*3+q)*3 + 1, 1 + (i*3+q)*3 + 2])
    ix.extend(range(1 + 9*len(edges), 1 + 9*(len(edges)+1)))
    assert len(ix) == 4*len(edges) + 10
    return ix


def expand(core, edges):
    p = np.zeros(1 + 9*(len(edges)+1))
    p[raw_indices(edges)] = core
    return p


def target_fj(core, edges):
    f, j = base.residual_jacobian(expand(core, edges), edges, base.MAJ)
    return f, j[:, raw_indices(edges)]


def source_hit(index):
    hits = json.loads((R23 / "ad23_maj_7cz_exact.json").read_text())["hits"]
    h = hits[index]
    phase = h["phase_pi_over_8"] * np.pi/8
    layers = [[base.su2(np.asarray(a)*np.pi/4) for a in row]
              for row in h["local_angles_pi_over_4"]]
    edges = [tuple(e) for e in h["edges"]]
    p = np.concatenate([[phase], np.asarray(h["local_angles_pi_over_4"]).reshape(-1)*np.pi/4])
    assert np.max(abs(base.circuit(p, edges)-base.MAJ)) < 2e-12
    return phase, layers, edges


def delete_gate(phase, layers, edges, j):
    # 原顺序 L_j -> CZ_j -> L_{j+1}；删 CZ 后合并为 L_{j+1}L_j。
    nl = [list(x) for x in layers]
    merged = [nl[j+1][q] @ nl[j][q] for q in range(3)]
    nl[j:j+2] = [merged]
    ne = edges[:j] + edges[j+1:]
    p = np.concatenate([[phase], np.asarray([[gauge.zxz(u) for u in row] for row in nl]).reshape(-1)])
    ph, ll, _ = gauge.canonicalize(p, ne)
    pc = gauge.pack(ph, ll)
    preserve = np.max(abs(base.circuit(pc, ne)-base.circuit(p, ne)))
    assert preserve < 2e-11, preserve
    return ne, pc[raw_indices(ne)], float(preserve)


def known_answer_gate():
    # 七个旧精确解仅作已知答案门；另测删门/恢复恒等式及 k=7 求解器。
    max_source = 0.0
    for i in range(7):
        ph, ll, ee = source_hit(i)
        p = gauge.pack(ph, ll)
        max_source = max(max_source, float(np.max(abs(base.circuit(p, ee)-base.MAJ))))
    ph, ll, ee = source_hit(0)
    ne, c, pres = delete_gate(ph, ll, ee, 2)
    # 已知恒等：在删除处恢复同一个 CZ，并把合并层拆回原两层，必须逐矩阵复原。
    assert ee[:2] + ee[3:] == ne
    rebuilt = base.circuit(gauge.pack(ph, ll), ee)
    assert np.max(abs(rebuilt-base.MAJ)) < 2e-12
    core = gauge.pack(ph, ll)[raw_indices(ee)]
    sol = least_squares(lambda x: target_fj(x, ee)[0], core,
                        jac=lambda x: target_fj(x, ee)[1], method="lm", max_nfev=100,
                        ftol=1e-14, xtol=1e-14, gtol=1e-14)
    known_e = float(np.max(abs(base.circuit(expand(sol.x, ee), ee)-base.MAJ)))
    assert known_e < 2e-12
    return {"ad23_sources": 7, "ad23_max_abs": max_source,
            "known_k7_solver_max_abs": known_e, "merge_canonical_max_abs": pres}


def solve(task):
    hit, j, kick, ne, core = task
    rng = np.random.default_rng(260000 + 100*hit + 10*j + int(kick > 0))
    x0 = np.asarray(core) + kick*rng.normal(size=len(core))
    try:
        sol = least_squares(lambda x: target_fj(x, ne)[0], x0,
                            jac=lambda x: target_fj(x, ne)[1], method="lm", max_nfev=700,
                            ftol=1e-14, xtol=1e-14, gtol=1e-14)
        p = expand(sol.x, ne)
        e = float(np.max(abs(base.circuit(p, ne)-base.MAJ)))
        return {"hit": hit, "deleted": j, "kick": kick, "edges": [list(x) for x in ne],
                "target_max_abs": e, "nfev": int(sol.nfev), "status": int(sol.status),
                "optimality": float(sol.optimality), "x_core": sol.x.tolist()}
    except Exception as exc:
        return {"hit": hit, "deleted": j, "kick": kick,
                "error": type(exc).__name__ + ": " + str(exc)}


def main():
    start = time.time()
    gate = known_answer_gate()
    tasks = []
    max_preserve = 0.0
    for hit in range(7):
        ph, ll, ee = source_hit(hit)
        for j in range(7):
            ne, core, pres = delete_gate(ph, ll, ee, j)
            max_preserve = max(max_preserve, pres)
            for kick in (0.0, 0.03):
                tasks.append((hit, j, kick, ne, core))
    rows = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        fs = [ex.submit(solve, t) for t in tasks]
        for n, f in enumerate(as_completed(fs), 1):
            rows.append(f.result())
            if n % 14 == 0:
                print(json.dumps({"done": n, "total": len(fs), "seconds": time.time()-start}), flush=True)
    rows.sort(key=lambda r: (r["hit"], r["deleted"], r["kick"]))
    (R / "ad26_maj_7to6.jsonl").write_text("".join(json.dumps(r, separators=(",", ":"))+"\n" for r in rows))
    good = [r for r in rows if "error" not in r]
    exact = [r for r in good if r["target_max_abs"] < 1e-9]
    best = min(good, key=lambda r: r["target_max_abs"])
    out = {"beat": "AD-26", "status": "MAJ_7TO6_TARGETED_COMPLETE",
           "known_answer_gate_first": gate, "merge_canonical_max_abs": max_preserve,
           "protocol": "7 exact sources x 7 single deletions x {0,0.03} deterministic kicks; canonical 34-core; LM max_nfev=700",
           "runs": len(rows), "errors": len(rows)-len(good), "exact_numeric_hits": len(exact),
           "best": {k: best[k] for k in ("hit", "deleted", "kick", "target_max_abs", "nfev", "optimality")},
           "exact_hit_indices": [[r["hit"], r["deleted"], r["kick"]] for r in exact],
           "evidence_level": "L2 targeted local numerical search; exact hits, if any, still require algebraic certification",
           "boundary": "只覆盖AD-23七证书的49条删门轨道及指定扰动；零命中不证明k=6不存在，更不改变4<=k<=7。",
           "strict_interval": "4 <= k <= 7", "private_ci_consumption": 0,
           "quantum_machine_actual_consumption_seconds": 0,
           "quantum_machine_launched": False, "quantum_account_quota_verified": False}
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode()+b"\n"
    (R / "ad26_maj_7to6_summary.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "runs": len(rows), "errors": out["errors"],
                      "exact_numeric_hits": len(exact), "best": out["best"],
                      "seconds": time.time()-start, "sha256": hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
