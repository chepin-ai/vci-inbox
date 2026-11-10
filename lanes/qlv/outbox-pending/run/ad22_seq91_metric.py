"""AD-22 序91规范感知盆宽：‖Jδp‖=r 可见扰动、零空间对照、LM/TRF 双求解器。
半径是基点拉回度量中的输出实向量一阶范数，不是73维原始坐标欧氏长度。
"""
import itertools, json, sys, time, os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
AD21=Path('/mnt/agents/output/.stash/ad21');RUN=Path('/mnt/agents/output/.stash/ad22/run')
sys.path.insert(0,str(AD21));sys.path.insert(0,str(AD21/'run'))
import toffoli_solver as ts
import ad21_embeddings as ae
from ad21_tangent import target_of
import ad21_geometry as geometry
BASE=json.loads((AD21/'run/ad21_seq91_base.json').read_text())
IDX=91;SEQ=list(itertools.product(ts.PATH,repeat=7))[IDX]
T=ts.toffoli({0,2},1)
H0=geometry.sphere(tuple(BASE['perm']),BASE['sigma'],BASE['theta'],BASE['phi'])
V0=target_of(H0,T)
RADII=json.loads(os.environ.get('AD22_RADII','[.001,.003,.01,.03,.1,.3,1.,2.]'));NDIR=12
TAG=os.environ.get('AD22_TAG','');STEM='ad22_seq91_metric'+TAG


def canonicalize(p):
    """把每个 Rz-Ry-Rz 三元组化为中间角[0,π]的有界规范；只改参数规范，不改电路。"""
    p=np.asarray(p,float);th=p[1:].reshape(-1,3,3);out=np.zeros_like(th)
    for i in range(th.shape[0]):
        for q in range(3):
            U=ts.su2(th[i,q]);b=2*np.arctan2(abs(U[1,0]),abs(U[0,0]))
            if abs(U[0,0])>1e-14 and abs(U[1,0])>1e-14:
                a=-np.angle(U[0,0])+np.angle(U[1,0]);c=-np.angle(U[0,0])-np.angle(U[1,0])
            elif abs(U[1,0])<=1e-14:
                b=0.;a=-2*np.angle(U[0,0]);c=0.
            else:
                b=np.pi;a=0.;c=2*np.angle(U[1,0])
            out[i,q]=[a,b,c]
    q=np.concatenate([[0.],out.reshape(-1)])
    U0=ts.U_of(p,SEQ);U1=ts.U_of(q,SEQ)
    phase=np.vdot(U1.reshape(-1),U0.reshape(-1))/64
    q[0]=np.angle(phase)
    return q


def metric_setup():
    p=canonicalize(BASE['x'])
    assert np.max(np.abs(ts.U_of(p,SEQ)-ts.U_of(np.asarray(BASE['x']),SEQ)))<1e-9
    _,J=ts.f_j(p,SEQ,V0.reshape(-1));U,s,Vh=np.linalg.svd(J,full_matrices=True)
    # 序91谱间隙：0.2375 >> 2.33e-8 >> 2.45e-14；旧相对阈会把数值伪方向逆放大。
    rank=int(np.sum(s>1e-7));Vr=Vh[:rank].T;N=Vh[rank:].T;sr=s[:rank]
    return p,J,U,s,Vr,N,sr,rank
P0,J,USV,SVAL,VR,NULL,SR,RANK=metric_setup()


def classify(x):
    H,angles,e=ae.H_of(x,IDX,T)
    fits=sorted((ae.fit(H,p) for p in itertools.permutations(range(3))),key=lambda r:r['ansatz_max_delta'])
    f=fits[0]
    return {'direct_e_rebuilt':e,'angle_max_dev_rad':float(np.max(np.abs(np.abs(angles)-ae.ALPHA))),
            'H_involution_max':float(np.max(np.abs(H@H-np.eye(8)))),'best_perm':f['perm'],
            'best_sigma':f['sigma_u_minus_v'],'best_ansatz_max_delta':f['ansatz_max_delta'],
            'runner_up_ansatz_max_delta':fits[1]['ansatz_max_delta']}


def signature_hit(c):
    return (c['direct_e_rebuilt']<.205 and c['angle_max_dev_rad']<1e-5 and c['H_involution_max']<1e-4
            and c['best_perm']==[2,1,0] and c['best_sigma']==-1 and c['best_ansatz_max_delta']<1e-4)


def solve(task):
    direction,radius,null_mode,method,seed=task
    rng=np.random.default_rng(922000+direction)
    d=rng.normal(size=RANK);d/=np.linalg.norm(d)
    visible=VR@(d/SR)
    delta=radius*visible
    if null_mode:
        rng2=np.random.default_rng(923000+direction)
        z=rng2.normal(size=NULL.shape[1]);z/=np.linalg.norm(z)
        delta=delta+3*radius*(NULL@z)
    x0=P0+delta
    raw0=ts.f_resid(x0,SEQ,V0.reshape(-1));initial_output_norm=float(np.linalg.norm(raw0))
    initial_max=float(np.max(np.abs(raw0[:64]+1j*raw0[64:])))
    ts._cache.clear();t0=time.time()
    kwargs=dict(max_nfev=2500,ftol=1e-14,xtol=1e-14,gtol=1e-14)
    sol=least_squares(ts.f_resid,x0,jac=ts.j_resid,args=(SEQ,V0.reshape(-1)),method=method,**kwargs)
    e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])));c=classify(sol.x);sig=signature_hit(c)
    return {'direction':direction,'radius':radius,'null_mode':null_mode,'method':method,'seed':seed,
            'rank':RANK,'initial_output_norm':initial_output_norm,'initial_max_residual':initial_max,
            'e_target':e,'nfev':int(sol.nfev),'status':int(sol.status),'optimality':float(sol.optimality),
            'seconds':time.time()-t0,'classification':c,'signature_hit':sig,
            'exact_return':bool(sig and e<1e-8),'x':sol.x.tolist()}


def main():
    c0=classify(P0);e0=float(np.max(np.abs(ts.U_of(P0,SEQ)-V0)))
    assert e0<1e-8 and signature_hit(c0),(e0,c0)
    # 已知答案：零空间一阶映射必须为零；可见扰动一阶输出范数等于半径。
    assert np.max(np.abs(J@NULL))<3e-8
    tasks=[]
    for d in range(NDIR):
        for radius in RADII:
            for null_mode in [0,1]:
                for method in ['lm','trf']:
                    tasks.append((d,radius,null_mode,method,922000+d))
    rows=[];t0=time.time()
    with (RUN/(STEM+'.jsonl')).open('w',buffering=1) as f:
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs={ex.submit(solve,t):t for t in tasks}
            for n,fut in enumerate(as_completed(futs),1):
                task=futs[fut]
                try:r=fut.result()
                except Exception as exc:r={'direction':task[0],'radius':task[1],'null_mode':task[2],
                    'method':task[3],'seed':task[4],'error':type(exc).__name__+': '+str(exc),
                    'signature_hit':False,'exact_return':False}
                rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
                if n%24==0 or n==len(tasks):print(json.dumps({'done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    valid=[r for r in rows if 'error' not in r]
    summary={}
    for method in ['lm','trf']:
        for null_mode in [0,1]:
            rr=[r for r in valid if r['method']==method and r['null_mode']==null_mode]
            summary[f'{method}/null{null_mode}']={
                'n':len(rr),'exact_returns':sum(r['exact_return'] for r in rr),
                'signature_hits':sum(r['signature_hit'] for r in rr),
                'by_radius':{str(rad):{'n':sum(r['radius']==rad for r in rr),
                    'exact_returns':sum(r['radius']==rad and r['exact_return'] for r in rr),
                    'signature_hits':sum(r['radius']==rad and r['signature_hit'] for r in rr)} for rad in RADII}}
    lookup={(r['direction'],r['radius'],r['null_mode'],r['method']):r for r in valid}
    gauge_pairs=[];solver_pairs=[]
    for d in range(NDIR):
        for rad in RADII:
            for method in ['lm','trf']:
                a=lookup.get((d,rad,0,method));b=lookup.get((d,rad,1,method))
                if a and b:gauge_pairs.append({'direction':d,'radius':rad,'method':method,
                    'exact_agree':a['exact_return']==b['exact_return'],
                    'signature_agree':a['signature_hit']==b['signature_hit'],
                    'e_target_difference':abs(a['e_target']-b['e_target'])})
            for nm in [0,1]:
                a=lookup.get((d,rad,nm,'lm'));b=lookup.get((d,rad,nm,'trf'))
                if a and b:solver_pairs.append({'direction':d,'radius':rad,'null_mode':nm,
                    'exact_agree':a['exact_return']==b['exact_return'],
                    'signature_agree':a['signature_hit']==b['signature_hit'],
                    'e_target_difference':abs(a['e_target']-b['e_target'])})
    out={'beat':'AD-22','center':{'e_target':e0,'classification':c0,'rank':RANK,
            'singular_values':SVAL.tolist(),'canonicalization_max':float(np.max(np.abs(ts.U_of(P0,SEQ)-ts.U_of(np.asarray(BASE['x']),SEQ))))},
         'metric':'delta=radius*V_r S_r^-1 d, ||d||=1; null mode adds 3*radius*N z',
         'runs':len(rows),'errors':len(rows)-len(valid),'seconds':time.time()-t0,'summary':summary,
         'gauge_pairs':{'n':len(gauge_pairs),'exact_agree':sum(r['exact_agree'] for r in gauge_pairs),
                        'signature_agree':sum(r['signature_agree'] for r in gauge_pairs),'rows':gauge_pairs},
         'solver_pairs':{'n':len(solver_pairs),'exact_agree':sum(r['exact_agree'] for r in solver_pairs),
                         'signature_agree':sum(r['signature_agree'] for r in solver_pairs),'rows':solver_pairs},
         'boundary':'基点拉回度量下的局部有限采样；不是全局吸引盆体积，也不是全解流形上的完整测地距离。'}
    (RUN/(STEM+'_summary.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
