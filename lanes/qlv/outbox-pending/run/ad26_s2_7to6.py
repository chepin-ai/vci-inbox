"""AD-26 S^2：两个去重7-CZ代表元的定向7->6单点攻击。"""
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
import ad26_s2_9to8 as prior

R=Path(__file__).resolve().parent;base,s2,prune,gauge=prior.base,prior.s2,prior.prune,prior.gauge
THETA,PHI=prior.THETA,prior.PHI;SELECT={"89d2d0":0,"89d2d6":6}


def source(stem):
    rows=[json.loads(x) for x in (R/"ad26_s2_8to7.jsonl").read_text().splitlines() if x.strip()]
    r=next(r for r in rows if r["deleted"]==[SELECT[stem]] and r["kick"]==.02 and r["target_max_abs"]<1e-9)
    edges=[tuple(e) for e in r["edges"]];p=prune.expand(r["x_core"],edges)
    e=float(np.max(abs(base.circuit(p,edges)-s2.target(THETA,PHI))));assert e<2e-12
    ph,layers=gauge.unpack(p)
    return ph,layers,edges,p,e


def known_gates():
    out={}
    for stem in SELECT:
        ph,layers,edges,p,source_e=source(stem);target=s2.target(THETA,PHI);core=p[prune.raw_indices(edges)]
        sol,e=prior.solve_at(core,edges,target,max_nfev=150);assert e<2e-12
        ne,c6,preserve=prune.delete_gates(ph,layers,edges,(0,));known6=base.circuit(prune.expand(c6,ne),ne)
        rng=np.random.default_rng(26900+SELECT[stem]);xs=c6+1e-5*rng.normal(size=len(c6))
        sol6,e6=prior.solve_at(c6,ne,known6,xs,350);assert e6<2e-10,(stem,e6)
        bad=core.copy();bad[1]+=np.pi/4
        bad_e=float(np.max(abs(base.circuit(prune.expand(bad,edges),edges)-target)));assert bad_e>1e-3
        out[stem]={"source_7cz_max_abs":source_e,"same_point_7cz_solver_max_abs":e,
                   "deleted_self_target_6cz_recovery_max_abs":e6,"merge_canonical_max_abs":preserve,
                   "changed_angle_counterexample_max_abs":bad_e}
    return out


def solve(task):
    stem,delete,kick,ne,core=task;begin=time.time()
    rng=np.random.default_rng(27000+1000*SELECT[stem]+10*delete+int(kick*1000))
    xs=np.asarray(core)+kick*rng.normal(size=len(core))
    try:
        sol,e=prior.solve_at(core,ne,s2.target(THETA,PHI),xs,900)
        return {"topology":stem,"deleted":[delete],"k":6,"kick":kick,"edges":[list(x) for x in ne],
                "target_max_abs":e,"nfev":int(sol.nfev),"status":int(sol.status),
                "optimality":float(sol.optimality),"x_core":sol.x.tolist(),"seconds":time.time()-begin}
    except Exception as exc:
        return {"topology":stem,"deleted":[delete],"k":6,"kick":kick,
                "error":type(exc).__name__+": "+str(exc),"seconds":time.time()-begin}


def main():
    begin=time.time();gates=known_gates();tasks=[];max_preserve=0.
    for stem in SELECT:
        ph,layers,edges,p,_=source(stem)
        for delete in range(7):
            ne,core,preserve=prune.delete_gates(ph,layers,edges,(delete,));max_preserve=max(max_preserve,preserve)
            for kick in (0.,.02): tasks.append((stem,delete,kick,ne,core))
    rows=[]
    with ProcessPoolExecutor(max_workers=4) as pool:
        futs={pool.submit(solve,t):(t[0],t[1],t[2]) for t in tasks}
        for n,fut in enumerate(as_completed(futs),1):
            try: rows.append(fut.result())
            except Exception as exc: rows.append({"topology":futs[fut][0],"error":type(exc).__name__+": "+str(exc)})
            print(json.dumps({"done":n,"total":len(tasks),"elapsed":time.time()-begin}),flush=True)
    rows.sort(key=lambda r:(r.get("topology",""),r.get("deleted",[99]),r.get("kick",-1)))
    (R/"ad26_s2_7to6.jsonl").write_text("".join(json.dumps(r,separators=(",",":"))+"\n" for r in rows))
    per={}
    for stem in SELECT:
        rr=[r for r in rows if r["topology"]==stem and "error" not in r];hits=[r for r in rr if r["target_max_abs"]<1e-9]
        best=min(rr,key=lambda r:r["target_max_abs"])
        per[stem]={"runs":len(rr),"exact_numeric_hits":len(hits),"hit_deletions":[r["deleted"] for r in hits],
                   "best":{k:best[k] for k in ("deleted","kick","target_max_abs","nfev","optimality")}}
    out={"beat":"AD-26","status":"S2_TWO_7CZ_TO6_TARGETED_POINT_COMPLETE","known_answer_gate_first":gates,
         "theta":THETA,"phi":PHI,"merge_canonical_max_abs":max_preserve,
         "protocol":"two numerical 7-CZ sources with distinct edge orders; 7 single deletions per source; kicks 0/0.02; canonical 34-core; TRF max_nfev=900",
         "runs":len(rows),"errors":sum("error" in r for r in rows),
         "exact_numeric_hits":sum(x["exact_numeric_hits"] for x in per.values()),"per_topology":per,
         "evidence_level":"L2 targeted local numerical search at one generic point",
         "boundary":"只覆盖两个7-CZ代表元的14种删门及两种扰动，共28轨；零命中不证明6-CZ不存在，命中仍需延拓与精确证书。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False,"seconds":time.time()-begin}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_7to6_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"runs":len(rows),"errors":out["errors"],
                      "exact_numeric_hits":out["exact_numeric_hits"],"per_topology":per,
                      "seconds":out["seconds"],"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
