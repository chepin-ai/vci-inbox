"""序91窄盆：64个全局新种子 + 24方向×8半径局部扰动；两账分离。"""
import itertools,json,sys,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
BASE=Path(__file__).resolve().parent.parent;RUN=BASE/'run'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(RUN))
import toffoli_solver as ts
import ad21_embeddings as ae
T=ts.toffoli({0,2},1);IDX=91;SEQ=list(itertools.product(ts.PATH,repeat=7))[IDX]
RADII=[.001,.003,.01,.03,.1,.3,1.,2.]
SEED_GLOBAL=910000;SEED_DIRECTION=910100

def center_record():
    rows=[json.loads(s) for s in (RUN/'ad20_g2k7_scan.jsonl').read_text().splitlines() if s.strip()]
    return next(r['best'] for r in rows if r['idx']==IDX)
CENTER=center_record()

def classify(x):
    H,angles,e=ae.H_of(x,IDX,T)
    fits=sorted((ae.fit(H,p) for p in itertools.permutations(range(3))),key=lambda r:r['ansatz_max_delta'])
    f=fits[0]
    return {'direct_e_rebuilt':e,'angle_max_dev_rad':float(np.max(np.abs(np.abs(angles)-ae.ALPHA))),
            'H_involution_max':float(np.max(np.abs(H@H-np.eye(8)))),
            'best_perm':f['perm'],'best_sigma':f['sigma_u_minus_v'],
            'best_ansatz_max_delta':f['ansatz_max_delta'],
            'runner_up_ansatz_max_delta':fits[1]['ansatz_max_delta']}
def is_hit(e,c):
    return (e<.205 and c['angle_max_dev_rad']<1e-5 and c['H_involution_max']<1e-4
            and c['best_perm']==[2,1,0] and c['best_sigma']==-1 and c['best_ansatz_max_delta']<1e-4)

def solve(task):
    kind,seed,p0,meta=task;rng=np.random.default_rng(seed)
    ts._cache.clear();t0=time.time()
    sol=least_squares(ts.f_resid,np.asarray(p0),jac=ts.j_resid,args=(SEQ,T.reshape(-1)),method='lm',
                      max_nfev=2500,ftol=1e-15,xtol=1e-15,gtol=1e-15)
    e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
    c=classify(sol.x)
    r={'kind':kind,'seed':seed,**meta,'e':e,'nfev':int(sol.nfev),'status':int(sol.status),
       'optimality':float(sol.optimality),'seconds':time.time()-t0,'classification':c,'x':sol.x.tolist()}
    r['hit']=is_hit(e,c)
    return r

def wilson(k,n,z=1.959963984540054):
    if n==0:return [None,None]
    ph=k/n;den=1+z*z/n;cen=(ph+z*z/(2*n))/den
    half=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/den
    return [float(cen-half),float(cen+half)]

def main():
    center=np.asarray(CENTER['x']);c0=classify(center)
    assert is_hit(CENTER['e'],c0),('center fails preregistered hit',CENTER['e'],c0)
    tasks=[]
    for r in range(64):
        rng=np.random.default_rng(SEED_GLOBAL+r);p0=rng.normal(scale=1.5,size=73)
        tasks.append(('global',SEED_GLOBAL+r,p0,{'restart':r}))
    for d in range(24):
        rng=np.random.default_rng(SEED_DIRECTION+d);v=rng.normal(size=73);v/=np.linalg.norm(v)
        for radius in RADII:
            tasks.append(('local',SEED_DIRECTION+d,center+radius*v,{'direction':d,'radius':radius}))
    t0=time.time();rows=[]
    with (RUN/'ad21_seq91_basin.jsonl').open('w',buffering=1) as f:
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs={ex.submit(solve,t):t for t in tasks}
            for n,fut in enumerate(as_completed(futs),1):
                t=futs[fut]
                try:r=fut.result()
                except Exception as exc:r={'kind':t[0],'seed':t[1],**t[3],'error':type(exc).__name__+': '+str(exc),'hit':False}
                rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
                if n%20==0 or n==len(tasks):print(json.dumps({'event':'progress','done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    valid=[r for r in rows if 'error' not in r];glob=[r for r in valid if r['kind']=='global'];loc=[r for r in valid if r['kind']=='local']
    directions=[]
    for d in range(24):
        rr=sorted([r for r in loc if r['direction']==d],key=lambda r:r['radius'])
        contiguous=0
        for r in rr:
            if r['hit']:contiguous=r['radius']
            else:break
        directions.append({'direction':d,'contiguous_hit_radius':contiguous,
                           'hits':sum(r['hit'] for r in rr),'nonmonotonic':any(r['hit'] for r in rr if r['radius']>contiguous)})
    gh=sum(r['hit'] for r in glob)
    out={'beat':'AD-21','center':{'e':CENTER['e'],'seed':CENTER['seed'],'classification':c0},
         'preregistered_hit':'e<0.205; angle_dev<1e-5; H_involution<1e-4; perm=[2,1,0]; sigma=-1; ansatz_delta<1e-4',
         'radii_solver_coordinate':RADII,'runs':len(rows),'errors':len(rows)-len(valid),'seconds':time.time()-t0,
         'global':{'n':len(glob),'hits':gh,'frequency':gh/len(glob) if glob else None,'wilson95':wilson(gh,len(glob)),
                   'e_min':min(r['e'] for r in glob),'hit_seeds':[r['seed'] for r in glob if r['hit']]},
         'local':{'n':len(loc),'hits':sum(r['hit'] for r in loc),
                  'by_radius':{str(rad):{'n':sum(r['radius']==rad for r in loc),'hits':sum(r['radius']==rad and r['hit'] for r in loc)} for rad in RADII},
                  'directions':directions},
         'boundary':'半径是73维原始求解器坐标的欧氏扰动；非规范不变几何盆宽，亦非全局吸引概率。'}
    (RUN/'ad21_seq91_basin_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
