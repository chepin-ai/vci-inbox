"""MAJ k≤7 补扫：18个精确8CZ解删门 + k7/k6全边序独立种子。"""
import itertools,json,sys,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
BASE=Path(__file__).resolve().parent.parent;RUN=BASE/'run'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(RUN))
import toffoli_solver as ts
import ad21_maj as m
PATH=ts.PATH

def solve(task):
    source,parent,delete,seed,p,edges=task;ts._cache.clear();t0=time.time()
    sol=least_squares(ts.f_resid,np.asarray(p),jac=ts.j_resid,args=(edges,m.MAJ.reshape(-1)),method='lm',
                      max_nfev=3000,ftol=1e-15,xtol=1e-15,gtol=1e-15)
    e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
    return {'source':source,'parent_deleted':parent,'delete':delete,'seed':seed,'k':len(edges),'edges':edges,
            'e':e,'nfev':int(sol.nfev),'status':int(sol.status),'optimality':float(sol.optimality),
            'seconds':time.time()-t0,'x':sol.x.tolist()}

def main():
    rows0=[json.loads(s) for s in (RUN/'ad21_maj.jsonl').read_text().splitlines() if s.strip()]
    exact8=[r for r in rows0 if r.get('k')==8 and r.get('e',1)<1e-9]
    assert len(exact8)==18
    direct=[]
    for r in exact8:direct.append(float(np.max(np.abs(ts.U_of(r['x'],r['edges'])-m.MAJ))))
    assert max(direct)<1e-9
    tasks=[]
    for pi,r in enumerate(exact8):
        for j in range(8):
            p,e=m.delete_one(r['x'],r['edges'],j)
            tasks.append(('delete_from_exact8',r['deleted'],j,880000+pi*16+j,p,e))
    for k,base_seed in [(7,770000),(6,760000)]:
        for idx,edges in enumerate(itertools.product(PATH,repeat=k)):
            seed=base_seed+idx;rng=np.random.default_rng(seed);p=rng.normal(scale=1.5,size=1+9*(k+1))
            tasks.append((f'global_k{k}',[],idx,seed,p,list(edges)))
    t0=time.time();rows=[]
    with (RUN/'ad21_maj_lower.jsonl').open('w',buffering=1) as f:
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs={ex.submit(solve,t):t for t in tasks}
            for n,fut in enumerate(as_completed(futs),1):
                t=futs[fut]
                try:r=fut.result()
                except Exception as exc:r={'source':t[0],'parent_deleted':t[1],'delete':t[2],'seed':t[3],
                                            'k':len(t[5]),'edges':t[5],'error':type(exc).__name__+': '+str(exc)}
                rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
                if n%25==0 or n==len(tasks):print(json.dumps({'event':'progress','done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    valid=[r for r in rows if 'error' not in r];groups={}
    for source in sorted({r['source'] for r in valid}):
        rr=[r for r in valid if r['source']==source];best=min(rr,key=lambda r:r['e'])
        groups[source]={'n':len(rr),'exact_e_lt_1e-9':sum(r['e']<1e-9 for r in rr),
                        'best':{k:best[k] for k in ['e','seed','delete','parent_deleted','nfev','status']}}
    out={'beat':'AD-21','runs':len(rows),'errors':len(rows)-len(valid),'seconds':time.time()-t0,
         'exact8_parents':len(exact8),'exact8_parent_max_direct_e':max(direct),'groups':groups,
         'boundary':'k≤7零精确若出现，只构成这些删门与全局种子下的L2数值否证，不是解析下界。'}
    (RUN/'ad21_maj_lower_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
