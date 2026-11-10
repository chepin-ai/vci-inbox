"""AD-23 以严格7-CZ为已知答案门的规范核心删门重攻；k=6，不宣称数值下界。"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

R=Path(__file__).resolve().parent
R22=R.parent.parent/'ad22/run'
sys.path.insert(0,str(R22))
import ad22_verify as base
sys.path.insert(0,str(R))
import ad23_gauge as gauge
EXACT=None

def raw_indices(edges):
    k=len(edges);ix=[0]
    for i,(a,b) in enumerate(edges):
        for q in (a,b):
            for off in (1,2):ix.append(1+(i*3+q)*3+off)
    ix.extend(range(1+9*k,1+9*(k+1)))
    assert len(ix)==4*k+10 and len(set(ix))==len(ix)
    return ix

def expand(core,edges):
    core=np.asarray(core,float);ix=raw_indices(edges);p=np.zeros(1+9*(len(edges)+1));p[ix]=core
    return p

def core_of(p,edges):
    ph,L,meta=gauge.canonicalize(p,edges);pc=gauge.pack(ph,L);ix=raw_indices(edges)
    return pc[ix],pc,meta

def fj(core,edges):
    p=expand(core,edges);f,J=base.residual_jacobian(p,edges,base.MAJ)
    return f,J[:,raw_indices(edges)]
def f(core,edges):return fj(core,edges)[0]
def j(core,edges):return fj(core,edges)[1]

def exact_source_pack():
    global EXACT
    if EXACT is None:EXACT=json.loads((R/'ad23_maj_7cz_exact.json').read_text())['hits']
    return EXACT

def source_p(h):
    x=np.concatenate([[h['phase_pi_over_8']*np.pi/8],np.asarray(h['local_angles_pi_over_4']).reshape(-1)*(np.pi/4)])
    return x

def delete_warm(h,delete):
    x=source_p(h);edges=[tuple(e) for e in h['edges']];ph,L=gauge.unpack(x);k=len(edges);new=[]
    for j in range(k):
        if j<delete:left,right=L[j],None
        elif j==delete:left,right=L[j+1],L[j]
        else:left,right=L[j+1],None
        new.append([left[q] if right is None else left[q]@right[q] for q in range(3)])
    p=gauge.pack(ph,new);ne=[e for i,e in enumerate(edges) if i!=delete]
    core,pc,meta=core_of(p,ne)
    return core,ne

def known_gate():
    packs=exact_source_pack();es=[]
    for h in packs:
        x=source_p(h);core=x[raw_indices(h['edges'])];ff=f(core,h['edges'])
        es.append(float(np.max(np.abs(ff[:64]+1j*ff[64:]))))
    assert max(es)<2e-12,max(es)
    # Jacobian列选择的独立有限差分门。
    edges=[(0,1),(1,2),(0,1)];rng=np.random.default_rng(236001);c=rng.normal(size=4*len(edges)+10);d=rng.normal(size=len(c));h=1e-6
    J=j(c,edges);fd=(f(c+h*d,edges)-f(c-h*d,edges))/(2*h);err=float(np.max(np.abs(fd-J@d)))
    assert err<2e-5,err
    # 求解器必须先留在精确7-CZ已知答案上。
    h0=packs[4];c0=source_p(h0)[raw_indices(h0['edges'])]
    sol=least_squares(f,c0,jac=j,args=(h0['edges'],),method='lm',max_nfev=100,
                      ftol=1e-14,xtol=1e-14,gtol=1e-14)
    e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])));assert e<2e-12,e
    return {'exact_7cz_sources':len(es),'exact_7cz_max_e':max(es),'jacobian_directional_max':err,'known_solver_e':e}

def solve(task):
    source_idx,delete,restart=task;packs=exact_source_pack();h=packs[source_idx]
    c0,edges=delete_warm(h,delete);rng=np.random.default_rng(236100+source_idx*1000+delete*32+restart)
    scales=[0,1e-6,1e-4,.01,.05,.2,.5,1.]
    if restart<8:c0=c0+rng.normal(scale=scales[restart],size=len(c0));mode='local'
    else:c0=rng.uniform(-np.pi,np.pi,size=len(c0));mode='random'
    t0=time.time()
    try:
        sol=least_squares(f,c0,jac=j,args=(edges,),method='lm',max_nfev=1800,
                          ftol=1e-14,xtol=1e-14,gtol=1e-14)
        e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
        return {'source_idx':source_idx,'source_seq_idx':h['idx'],'source_restart':h['restart'],
                'delete':delete,'restart':restart,'mode':mode,'edges':edges,'e':e,'nfev':int(sol.nfev),
                'status':int(sol.status),'optimality':float(sol.optimality),'seconds':time.time()-t0,
                'x_core':sol.x.tolist()}
    except Exception as exc:
        return {'source_idx':source_idx,'delete':delete,'restart':restart,'mode':mode,
                'error':type(exc).__name__+': '+str(exc),'seconds':time.time()-t0}

def main():
    t0=time.time();gate=known_gate();packs=exact_source_pack();tasks=[(s,d,r) for s in range(len(packs)) for d in range(7) for r in range(16)]
    out=R/'ad23_lower.jsonl';rows=[]
    with out.open('w',buffering=1) as fp:
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs={ex.submit(solve,t):t for t in tasks}
            for n,fut in enumerate(as_completed(futs),1):
                task=futs[fut]
                try:row=fut.result()
                except Exception as exc:row={'source_idx':task[0],'delete':task[1],'restart':task[2],
                                            'error':type(exc).__name__+': '+str(exc)}
                rows.append(row);fp.write(json.dumps(row,separators=(',',':'))+'\n');fp.flush();os.fsync(fp.fileno())
                if n%49==0 or n==len(tasks):print(json.dumps({'done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    valid=[r for r in rows if 'error' not in r];hits=[r for r in valid if r['e']<1e-9];best=min(valid,key=lambda r:r['e'])
    summary={'beat':'AD-23','protocol':'exact7-gated canonical-core delete; 7 sources x 7 deletions x 16 starts',
             'known_answer_gate':gate,'runs':len(rows),'errors':len(rows)-len(valid),'seconds':time.time()-t0,
             'exact_e_lt_1e-9':len(hits),'best':best,'hits':hits,
             'boundary':'新规范坐标与精确已知门下的删门数值扫描；零命中也不证明k=6不存在。'}
    (R/'ad23_lower_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('hits','best')},indent=2))
    print(json.dumps({'best_e':best['e'],'best_source':best['source_idx'],'best_delete':best['delete'],'hits':len(hits)},indent=2))
if __name__=='__main__':main()
