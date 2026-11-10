"""AD-22 MAJ k=4..7 全边序×8独立起点；解析下界4与已知8解双门自证。
成功只认 max|U-MAJ|<1e-9；任何零精确都只是本批数值否证。
"""
import itertools,json,sys,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
AD21=Path('/mnt/agents/output/.stash/ad21');RUN=Path('/mnt/agents/output/.stash/ad22/run')
sys.path.insert(0,str(AD21))
import toffoli_solver as ts
PATH=ts.PATH


def cnot(c,t):
    M=np.zeros((8,8),complex)
    for x in range(8):
        b=[(x>>2)&1,(x>>1)&1,x&1]
        if b[c]:b[t]^=1
        M[(b[0]<<2)|(b[1]<<1)|b[2],x]=1
    return M
MAJ=ts.toffoli({0,2},1)@cnot(1,2)@cnot(1,0);TV=MAJ.reshape(-1)


def known_answer_gate():
    pack=json.loads((AD21/'run/ad21_maj_8cz.json').read_text())['solutions'][0]
    x=np.asarray(pack['x']);edges=[tuple(e) for e in pack['edges']]
    e=float(np.max(np.abs(ts.U_of(x,edges)-MAJ)));assert e<1e-11,e
    rng=np.random.default_rng(224000);x0=x+rng.normal(scale=1e-5,size=len(x))
    sol=least_squares(ts.f_resid,x0,jac=ts.j_resid,args=(edges,TV),method='lm',max_nfev=2500,
                      ftol=1e-15,xtol=1e-15,gtol=1e-15)
    ep=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
    assert ep<1e-8,ep
    ident=float(np.max(np.abs(MAJ@cnot(1,0)@cnot(1,2)-ts.toffoli({0,2},1))))
    assert ident<1e-12,ident
    return {'known_8cz_rebuilt_e':e,'perturbed_8cz_solver_e':ep,'perturbed_nfev':int(sol.nfev),
            'maj_toffoli_identity_max':ident,'strict_lower_bound':4,
            'lower_bound_basis':'Toffoli path-CZ >=6 and MAJ=Toffoli*CNOT*CNOT; independently OSR=4 at both PATH cuts'}


def solve(task):
    k,idx,restart=task;edges=list(itertools.product(PATH,repeat=k))[idx]
    seed=224100+k*100000+idx*16+restart;rng=np.random.default_rng(seed)
    n=1+9*(k+1)
    if restart%3==0:p0=rng.normal(scale=1.5,size=n)
    elif restart%3==1:p0=rng.uniform(-np.pi,np.pi,size=n)
    else:
        # 确定性低差异角度覆盖，不用合成残差或近似替代。
        from scipy.stats import qmc
        p0=(qmc.Sobol(d=n,scramble=True,seed=seed).random(1)[0]*2-1)*np.pi
    ts._cache.clear();t0=time.time()
    try:
        sol=least_squares(ts.f_resid,p0,jac=ts.j_resid,args=(edges,TV),method='lm',max_nfev=1800,
                          ftol=1e-14,xtol=1e-14,gtol=1e-14)
        e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
        return {'k':k,'idx':idx,'restart':restart,'seed':seed,'edges':edges,'e':e,'nfev':int(sol.nfev),
                'status':int(sol.status),'optimality':float(sol.optimality),'seconds':time.time()-t0,
                'x':sol.x.tolist()}
    except Exception as exc:
        return {'k':k,'idx':idx,'restart':restart,'seed':seed,'edges':edges,
                'error':type(exc).__name__+': '+str(exc),'seconds':time.time()-t0}


def main():
    gate=known_answer_gate();tasks=[(k,idx,r) for k in [4,5,6,7]
                                    for idx in range(2**k) for r in range(8)]
    rows=[];t0=time.time()
    with (RUN/'ad22_maj_multistart.jsonl').open('w',buffering=1) as f:
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs={ex.submit(solve,t):t for t in tasks}
            for n,fut in enumerate(as_completed(futs),1):
                task=futs[fut]
                try:r=fut.result()
                except Exception as exc:r={'k':task[0],'idx':task[1],'restart':task[2],
                                          'error':type(exc).__name__+': '+str(exc)}
                rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
                if n%96==0 or n==len(tasks):print(json.dumps({'done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    valid=[r for r in rows if 'error' not in r];by={}
    for k in [4,5,6,7]:
        rr=[r for r in valid if r['k']==k];best=min(rr,key=lambda r:r['e'])
        by[str(k)]={'runs':len(rr),'exact_e_lt_1e-9':sum(r['e']<1e-9 for r in rr),
                    'best_e':best['e'],'best_idx':best['idx'],'best_restart':best['restart'],
                    'best_edges':best['edges'],'best_x':best['x'],'best_nfev':best['nfev'],
                    'per_sequence_best_median':float(np.median([min(r['e'] for r in rr if r['idx']==idx)
                                                               for idx in range(2**k)]))}
    out={'beat':'AD-22','known_answer_gate':gate,'runs':len(rows),'errors':len(rows)-len(valid),
         'seconds':time.time()-t0,'by_k':by,
         'boundary':'全边序×8起点的L2数值否证；不是连续参数空间的全局不存在或解析下界。'}
    (RUN/'ad22_maj_multistart_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
