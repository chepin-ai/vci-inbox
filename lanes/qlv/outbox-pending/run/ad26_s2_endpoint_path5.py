"""AD-26 theta=0：case5b禁边替换与6-CZ模板定向删门的PATH 5-CZ攻击。"""
import hashlib,json,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
import ad26_s2_9to8 as prior
import ad26_s2_analytic6_89d2d6d2 as a6

R=Path(__file__).resolve().parent;base,s2,gauge,prune=prior.base,prior.s2,prior.gauge,prior.prune
A,B,C=(0,1),(1,2),(0,2)


def case5_raw():
    w=np.exp(1j*np.pi/8);H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);I=np.eye(2,dtype=complex)
    layers=[[np.diag([1,1j]) for _ in range(3)]];edges=[]
    def cx(c,t):
        layers[-1][t]=H@layers[-1][t]
        edges.append((c,t));layers.append([H if q==t else I.copy() for q in range(3)])
    def ld(q,eta):layers[-1][q]=np.diag([1,eta])@layers[-1][q]
    cx(1,2);cx(0,1);ld(2,w**-2);cx(1,2);ld(1,w**-2);ld(2,w**-2);cx(0,1);cx(0,2)
    for q in range(3):ld(q,w**-2)
    # 论文构造的是 D=H_1 V H_1；首尾吸收 H_1 后统一搜索原目标 V。
    layers[0][1]=layers[0][1]@H;layers[-1][1]=H@layers[-1][1]
    # Delta 与 H 不是 SU(2)；逐门提出行列式平方根到全局相位后再做 ZXZ 打包。
    total=w;sul=[]
    for layer in layers:
        row=[]
        for U in layer:
            root=np.exp(.5j*np.angle(np.linalg.det(U)));total*=root;row.append(U/root)
        sul.append(row)
    p=gauge.pack(0.,sul);p[0]=np.angle(total)
    return total,p,edges


def solve(task):
    family,label,edges,core,kick=task;begin=time.time()
    seed=26111600+sum((j+1)*ord(x) for j,x in enumerate(label))+int(kick*1000)
    rng=np.random.default_rng(seed);xs=np.asarray(core)+kick*rng.normal(size=len(core))
    try:
        sol,e=prior.solve_at(core,edges,s2.target(0.,0.),xs,1800)
        return {"family":family,"label":label,"kick":kick,"edges":[list(e) for e in edges],
                "target_max_abs":e,"nfev":int(sol.nfev),"status":int(sol.status),
                "optimality":float(sol.optimality),"x_core":sol.x.tolist(),"seconds":time.time()-begin}
    except Exception as exc:
        return {"family":family,"label":label,"kick":kick,"error":type(exc).__name__+": "+str(exc),"seconds":time.time()-begin}


def main():
    start=time.time();phase,p,edges=case5_raw();p[0]=np.angle(phase)
    target=s2.target(0.,0.);case_e=float(np.max(abs(base.circuit(p,edges)-target)));assert case_e<2e-12,case_e
    ph,ll,_=gauge.canonicalize(p,edges);pc=gauge.pack(ph,ll);core=pc[prune.raw_indices(edges)]
    sol,self_e=prior.solve_at(core,edges,target,core+1e-5*np.random.default_rng(26111601).normal(size=len(core)),500)
    assert self_e<2e-10,self_e
    p6=a6.expand(a6.core(0.,0.),a6.EDGES);e6=float(np.max(abs(base.circuit(p6,a6.EDGES)-target)));assert e6<2e-12,e6
    tasks=[]
    # 仅文献构造的一条边突变：A<->B四处，C->A/B一处，共6个结构邻近边序。
    for j,old in enumerate(edges):
        choices=[A,B] if old==C else ([B] if old==A else [A])
        for new in choices:
            ne=list(edges);ne[j]=new;label=f"case5_edge{j}_{old[0]}{old[1]}to{new[0]}{new[1]}"
            phv,lv,_=gauge.canonicalize(p,ne);pv=gauge.pack(phv,lv);cv=pv[prune.raw_indices(ne)]
            for kick in (0.,.02,.1):tasks.append(("case5_edge_mutation",label,ne,cv,kick))
    ph6,l6=gauge.unpack(p6)
    for delete in range(6):
        ne,c5,preserve=prune.delete_gates(ph6,l6,list(a6.EDGES),(delete,));assert preserve<3e-11
        for kick in (0.,.02,.1):tasks.append(("exact6_deletion",f"delete{delete}",ne,c5,kick))
    rows=[]
    with ProcessPoolExecutor(max_workers=4) as pool:
        fs=[pool.submit(solve,t) for t in tasks]
        for n,f in enumerate(as_completed(fs),1):
            rows.append(f.result());print(json.dumps({"done":n,"total":len(fs),"elapsed":time.time()-start}),flush=True)
    rows.sort(key=lambda r:(r.get("family",""),r.get("label",""),r.get("kick",-1)))
    (R/"ad26_s2_endpoint_path5.jsonl").write_text("".join(json.dumps(r,separators=(",",":"))+"\n" for r in rows))
    good=[r for r in rows if "error" not in r];hits=[r for r in good if r["target_max_abs"]<1e-9]
    per={}
    for family in sorted(set(r["family"] for r in good)):
        rr=[r for r in good if r["family"]==family];hh=[r for r in rr if r["target_max_abs"]<1e-9];best=min(rr,key=lambda r:r["target_max_abs"])
        per[family]={"runs":len(rr),"exact_numeric_hits":len(hh),"hit_labels":[r["label"] for r in hh],
                     "best":{k:best[k] for k in ("label","kick","target_max_abs","nfev","optimality")}}
    path_rows=[r for r in good if all(tuple(e) in (A,B) for e in r["edges"])]
    aux_rows=[r for r in good if r not in path_rows]
    assert len(path_rows)==24 and len(aux_rows)==12
    def scope(rows):
        hh=[r for r in rows if r["target_max_abs"]<1e-9];best=min(rows,key=lambda r:r["target_max_abs"])
        return {"runs":len(rows),"exact_numeric_hits":len(hh),"hit_labels":[r["label"] for r in hh],
                "best":{k:best[k] for k in ("label","kick","target_max_abs","nfev","optimality")}}
    per_scope={"PATH":scope(path_rows),"unrestricted_auxiliary":scope(aux_rows)}
    out={"beat":"AD-26","status":"S2_THETA0_CASE5_NEIGHBOR_PATH5_COMPLETE",
         "known_answer_gate_first":{"unrestricted_case5_max_abs":case_e,"same_target_solver_recovery_max_abs":self_e,
                                    "exact_6cz_template_max_abs":e6},
         "theta":0.,"phi":0.,"protocol":"case5b六条单边突变加精确6-CZ模板六条删门；kick 0/0.02/0.1；TRF max_nfev=1800",
         "runs":len(rows),"errors":len(rows)-len(good),"exact_numeric_hits":len(hits),
         "path_runs":len(path_rows),"path_exact_numeric_hits":per_scope["PATH"]["exact_numeric_hits"],
         "per_family":per,"per_scope":per_scope,
         "evidence_level":"L2 structural-neighborhood numerical search at theta=0",
         "boundary":"PATH仅含02->A/B六轨与指定6-CZ模板删门十八轨，共24轨；前四边A<->B仍含02的12轨只作unrestricted辅助。零命中不证明PATH 5-CZ不存在。任何命中仍须精确证书，且不得外推全S^2。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False,"seconds":time.time()-start}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_endpoint_path5_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"runs":len(rows),"errors":out["errors"],"hits":len(hits),
                      "path_runs":len(path_rows),"path_hits":out["path_exact_numeric_hits"],
                      "per_scope":per_scope,"seconds":out["seconds"],"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
