"""AD-26 S^2：从已证89d2 8-CZ定向8->7单点攻击。"""
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
import ad26_s2_9to8 as prior
import ad26_s2_analytic8_89d2 as a8

R=Path(__file__).resolve().parent
base,s2,prune,gauge=prior.base,prior.s2,prior.prune,prior.gauge
THETA,PHI=prior.THETA,prior.PHI


def source():
    core=a8.core(THETA,PHI);edges=list(a8.EDGES);p=prune.expand(core,edges)
    e=float(np.max(abs(base.circuit(p,edges)-s2.target(THETA,PHI))));assert e<2e-12
    phase,layers=gauge.unpack(p)
    return phase,layers,edges,p,e


def known_gates():
    ph,layers,edges,p,source_e=source();target=s2.target(THETA,PHI)
    core=p[prune.raw_indices(edges)];sol,e=prior.solve_at(core,edges,target,max_nfev=150);assert e<2e-12
    ne,c7,preserve=prune.delete_gates(ph,layers,edges,(0,));known7=base.circuit(prune.expand(c7,ne),ne)
    rng=np.random.default_rng(26700);xs=c7+1e-5*rng.normal(size=len(c7))
    sol7,e7=prior.solve_at(c7,ne,known7,xs,350);assert e7<2e-10,e7
    bad=core.copy();bad[1]+=np.pi/4
    bad_e=float(np.max(abs(base.circuit(prune.expand(bad,edges),edges)-target)));assert bad_e>1e-3
    return {"source_8cz_max_abs":source_e,"same_point_8cz_solver_max_abs":e,
            "deleted_self_target_7cz_recovery_max_abs":e7,"merge_canonical_max_abs":preserve,
            "changed_angle_counterexample_max_abs":bad_e}


def solve(task):
    delete,kick,ne,core=task;begin=time.time();rng=np.random.default_rng(26800+10*delete+int(kick*1000))
    xs=np.asarray(core)+kick*rng.normal(size=len(core))
    try:
        sol,e=prior.solve_at(core,ne,s2.target(THETA,PHI),xs,900)
        return {"topology":"89d2","deleted":[delete],"k":7,"kick":kick,"edges":[list(x) for x in ne],
                "target_max_abs":e,"nfev":int(sol.nfev),"status":int(sol.status),
                "optimality":float(sol.optimality),"x_core":sol.x.tolist(),"seconds":time.time()-begin}
    except Exception as exc:
        return {"topology":"89d2","deleted":[delete],"k":7,"kick":kick,
                "error":type(exc).__name__+": "+str(exc),"seconds":time.time()-begin}


def main():
    begin=time.time();gates=known_gates();ph,layers,edges,p,_=source();tasks=[];max_preserve=0.
    for delete in range(8):
        ne,core,preserve=prune.delete_gates(ph,layers,edges,(delete,));max_preserve=max(max_preserve,preserve)
        for kick in (0.,.02): tasks.append((delete,kick,ne,core))
    rows=[]
    with ProcessPoolExecutor(max_workers=4) as pool:
        futs={pool.submit(solve,t):(t[0],t[1]) for t in tasks}
        for n,fut in enumerate(as_completed(futs),1):
            try: rows.append(fut.result())
            except Exception as exc: rows.append({"topology":"89d2","error":type(exc).__name__+": "+str(exc)})
            print(json.dumps({"done":n,"total":len(tasks),"elapsed":time.time()-begin}),flush=True)
    rows.sort(key=lambda r:(r.get("deleted",[99]),r.get("kick",-1)))
    (R/"ad26_s2_8to7.jsonl").write_text("".join(json.dumps(r,separators=(",",":"))+"\n" for r in rows))
    valid=[r for r in rows if "error" not in r];hits=[r for r in valid if r["target_max_abs"]<1e-9]
    best=min(valid,key=lambda r:r["target_max_abs"])
    out={"beat":"AD-26","status":"S2_89D2_8TO7_TARGETED_POINT_COMPLETE","known_answer_gate_first":gates,
         "theta":THETA,"phi":PHI,"merge_canonical_max_abs":max_preserve,
         "protocol":"one exact 8-CZ source; 8 single deletions; kicks 0/0.02; canonical 38-core; TRF max_nfev=900 at one generic point",
         "runs":len(rows),"errors":sum("error" in r for r in rows),"exact_numeric_hits":len(hits),
         "hit_deletions":[r["deleted"] for r in hits],
         "best":{k:best[k] for k in ("deleted","kick","target_max_abs","nfev","optimality")},
         "evidence_level":"L2 targeted local numerical search at one generic point",
         "boundary":"只覆盖89d2代表元的8种删门及两种扰动，共16轨；命中仍需延拓与精确证书，零命中不证明7-CZ不存在。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False,"seconds":time.time()-begin}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_8to7_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"runs":len(rows),"errors":out["errors"],
                      "exact_numeric_hits":len(hits),"best":out["best"],"seconds":out["seconds"],
                      "sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
