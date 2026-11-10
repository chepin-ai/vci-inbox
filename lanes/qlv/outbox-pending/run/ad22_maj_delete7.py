"""AD-22 新7-CZ MAJ解的逐门删除暖启动；目标k=6，不以数值零命中替代下界。"""
import json,sys,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
AD21=Path('/mnt/agents/output/.stash/ad21');RUN=Path('/mnt/agents/output/.stash/ad22/run')
sys.path.insert(0,str(AD21))
import toffoli_solver as ts
sys.path.insert(0,str(RUN))
from ad22_maj_multistart import MAJ,TV


def angles_of_su2(U):
    U=np.asarray(U,complex);U=U/np.sqrt(np.linalg.det(U))
    c=float(np.clip(abs(U[0,0]),0,1));b=2*np.arccos(c);s=np.sin(b/2)
    if s<1e-10:
        if c>.5:
            ac=np.angle(U[1,1])-np.angle(U[0,0]);a,c=ac,0.
        else:
            amc=np.angle(U[1,0])-np.angle(-U[0,1]);a,c=amc,0.
    else:
        a=np.angle(U[1,0])-np.angle(U[0,0]);c=np.angle(-U[0,1])-np.angle(U[0,0])
    return np.array([a,b,c])


def layer(th,i):
    return np.kron(np.kron(ts.su2(th[i,0]),ts.su2(th[i,1])),ts.su2(th[i,2]))


def delete_warm(x,edges,delete):
    k=len(edges);th=np.asarray(x[1:]).reshape(k+1,3,3)
    mats=[[ts.su2(th[i,q]) for q in range(3)] for i in range(k+1)]
    new=[]
    for j in range(k):
        if j<delete:src=(mats[j],None)
        elif j==delete:src=(mats[j+1],mats[j])
        else:src=(mats[j+1],None)
        left,right=src
        new.append([angles_of_su2(left[q] if right is None else left[q]@right[q]) for q in range(3)])
    return np.concatenate([[x[0]],np.asarray(new).reshape(-1)]),[e for i,e in enumerate(edges) if i!=delete]


def self_gate(pack):
    x=np.asarray(pack['x']);edges=[tuple(e) for e in pack['edges']]
    e=float(np.max(np.abs(ts.U_of(x,edges)-MAJ)));assert e<1e-11,e
    # ZYZ抽取已知答案：不删除门，只逐层抽角后必须重建原电路。
    th=x[1:].reshape(len(edges)+1,3,3);th2=[]
    for i in range(len(edges)+1):
        th2.append([angles_of_su2(ts.su2(th[i,q])) for q in range(3)])
    x2=np.concatenate([[x[0]],np.asarray(th2).reshape(-1)])
    ze=float(np.max(np.abs(ts.U_of(x2,edges)-ts.U_of(x,edges))));assert ze<1e-10,ze
    return {'source_7cz_e':e,'zyz_roundtrip_max':ze}


def solve(task):
    source_idx,delete,restart=task
    packs=json.loads((RUN/'ad22_maj_7cz.json').read_text())['hits'];pack=packs[source_idx]
    x0,edges=delete_warm(np.asarray(pack['x']),[tuple(e) for e in pack['edges']],delete)
    rng=np.random.default_rng(226000+source_idx*1000+delete*16+restart)
    scales=[0,1e-6,1e-4,.01,.1,.5,1.5]
    if restart<7:x0=x0+rng.normal(scale=scales[restart],size=len(x0))
    else:x0=rng.uniform(-np.pi,np.pi,size=len(x0))
    ts._cache.clear();t0=time.time()
    try:
        sol=least_squares(ts.f_resid,x0,jac=ts.j_resid,args=(edges,TV),method='lm',max_nfev=2500,
                          ftol=1e-14,xtol=1e-14,gtol=1e-14)
        e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
        return {'source_idx':source_idx,'source_seq_idx':pack['idx'],'delete':delete,'restart':restart,
                'edges':edges,'e':e,'nfev':int(sol.nfev),'status':int(sol.status),
                'optimality':float(sol.optimality),'seconds':time.time()-t0,'x':sol.x.tolist()}
    except Exception as exc:
        return {'source_idx':source_idx,'delete':delete,'restart':restart,
                'error':type(exc).__name__+': '+str(exc),'seconds':time.time()-t0}


def main():
    packs=json.loads((RUN/'ad22_maj_7cz.json').read_text())['hits']
    gates=[self_gate(p) for p in packs];assert max(g['zyz_roundtrip_max'] for g in gates)<1e-10
    tasks=[(s,d,r) for s in range(len(packs)) for d in range(7) for r in range(8)]
    rows=[];t0=time.time()
    # 先关闭全部worker，再由父进程一次性写账，避免fork继承流式文件句柄造成NUL空洞。
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(solve,t):t for t in tasks}
        for n,fut in enumerate(as_completed(futs),1):
            task=futs[fut]
            try:r=fut.result()
            except Exception as exc:r={'source_idx':task[0],'delete':task[1],'restart':task[2],
                                      'error':type(exc).__name__+': '+str(exc)}
            rows.append(r)
            if n%49==0 or n==len(tasks):print(json.dumps({'done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    (RUN/'ad22_maj_delete7.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))
    valid=[r for r in rows if 'error' not in r];hits=[r for r in valid if r['e']<1e-9]
    best=min(valid,key=lambda r:r['e'])
    out={'beat':'AD-22','known_answer_gates':gates,'runs':len(rows),'errors':len(rows)-len(valid),
         'seconds':time.time()-t0,'exact_e_lt_1e-9':len(hits),'best':best,'hits':hits,
         'boundary':'7个新解×7删门×8起点的暖启动数值扫描；不证明k=6不存在。'}
    (RUN/'ad22_maj_delete7_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['hits','best','known_answer_gates']},indent=2))
    print(json.dumps({'best_e':best['e'],'best_source':best['source_idx'],'best_delete':best['delete'],'hits':len(hits)},indent=2))
if __name__=='__main__':main()
