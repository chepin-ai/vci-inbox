"""AD-22 完整可达 Pauli 切空间的混合二阶 jet。
每个外方向基底系数固定为1，其余外方向、全部可达内方向及电路零空间均参与优化。
四种外方向 chart 覆盖其非零线性组合（投影意义下）；仍只报多种子局部数值证书。
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(RUN))
from ad22_outside_all import (TAN, SEEDS, setup_case, ts, ALPHA, TARGETS, realvec, pm3)


def solve_chart(st, out_paulis, in_paulis, fixed_index, h=1e-4):
    fixed=out_paulis[fixed_index]
    variable_paulis=in_paulis+[p for i,p in enumerate(out_paulis) if i!=fixed_index]
    Ps={s:pm3(s) for s in [fixed]+variable_paulis}
    H0,T=st['H0'],st['T'];J,Q,N,p0,seq,V0=st['J'],st['Q'],st['N'],st['p0'],st['seq'],st['V0'];tv=V0.reshape(-1)
    def dH(P): return 1j*(P@H0-H0@P)
    d0=realvec(1j*np.sin(ALPHA)*dH(Ps[fixed])@T)
    D=np.column_stack([realvec(1j*np.sin(ALPHA)*dH(Ps[s])@T) for s in variable_paulis])
    p10,*_=np.linalg.lstsq(J,d0,rcond=1e-11)
    A,*_=np.linalg.lstsq(J,D,rcond=1e-11)
    W=np.column_stack([A,N]); m=len(variable_paulis)
    cache={}
    def parts(y,hh=h):
        key=(y.tobytes(),hh)
        if key in cache:return cache[key]
        c=y[:m];z=y[m:]
        p1=p10+W@y
        P=Ps[fixed].copy()
        for ci,s in zip(c,variable_paulis):P=P+ci*Ps[s]
        H2=2*P@H0@P-P@P@H0-H0@P@P
        v2=realvec(1j*np.sin(ALPHA)*H2@T)
        Jp=ts.f_j(p0+hh*p1,seq,tv)[1];Jm=ts.f_j(p0-hh*p1,seq,tv)[1]
        D2=(Jp@p1-Jm@p1)/(2*hh)
        BW=(Jp@W-Jm@W)/(2*hh)
        fun=Q.T@(D2-v2)
        jac=2*(Q.T@BW)
        for j,s in enumerate(variable_paulis):
            R=Ps[s]
            dH2=2*(R@H0@P+P@H0@R)-(R@P+P@R)@H0-H0@(R@P+P@R)
            dv2=realvec(1j*np.sin(ALPHA)*dH2@T)
            jac[:,j]-=Q.T@dv2
        rr=D2-v2
        cache[key]=(fun,jac,rr,p1)
        return cache[key]
    starts=[np.zeros(W.shape[1])]
    for seed in SEEDS[1:]:
        rng=np.random.default_rng(seed+10000*fixed_index)
        y=np.zeros(W.shape[1]);y[:m]=rng.normal(scale=.45,size=m);y[m:]=rng.normal(scale=.7,size=N.shape[1]);starts.append(y)
    runs=[]
    for si,y0 in enumerate(starts):
        t0=time.time()
        sol=least_squares(lambda y:parts(y)[0],y0,jac=lambda y:parts(y)[1],max_nfev=700,
                          ftol=1e-13,xtol=1e-13,gtol=1e-13)
        fun,jac,rr,p1=parts(sol.x)
        runs.append({'start_index':si,'seed':SEEDS[si],'cokernel_norm':float(np.linalg.norm(fun)),
                     'rhs_norm':float(np.linalg.norm(rr)),'nfev':int(sol.nfev),'status':int(sol.status),
                     'optimality':float(sol.optimality),'seconds':time.time()-t0,'y':sol.x.tolist()})
        if np.linalg.norm(fun)<1e-8:break
    best=min(runs,key=lambda r:r['cokernel_norm'])
    return {'fixed_pauli':fixed,'variable_paulis':variable_paulis,'rank':st['rank'],
            'nullity':N.shape[1],'variable_count':W.shape[1],
            'best_cokernel_norm':best['cokernel_norm'],'best_rhs_norm':best['rhs_norm'],
            'best_start_index':best['start_index'],'runs':runs}


def main():
    indep=json.loads((RUN/'ad22_outside_all.json').read_text())['independent_directions']
    rows=[]
    for case in TAN['cases']:
        st=setup_case(case);outs=indep[case['name']]['independent_pauli']
        ins=[r['pauli'] for r in case['outside_candidates']
             if r['projection_residual_ratio']<1e-8 and r['outside_ratio']<1e-8]
        for j in range(len(outs)):
            r=solve_chart(st,outs,ins,j);r['case']=case['name'];rows.append(r)
            print(json.dumps({'case':r['case'],'fixed':r['fixed_pauli'],'best':r['best_cokernel_norm'],
                              'start':r['best_start_index'],'nfev':r['runs'][r['best_start_index']]['nfev']}),flush=True)
    out={'beat':'AD-22','protocol':'four projective charts per case; all accessible internal/outside Pauli coefficients and circuit nullspace optimized',
         'rows':rows,'outside_min':min(r['best_cokernel_norm'] for r in rows),
         'boundary':'固定秩、中心差分、六个确定性起点的局部数值证书；非二次系统全局不存在证明。'}
    (RUN/'ad22_mixed_jet.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'outside_min':out['outside_min'],'rows':[{'case':r['case'],'fixed':r['fixed_pauli'],'best':r['best_cokernel_norm']} for r in rows]},indent=2))
if __name__=='__main__':main()
