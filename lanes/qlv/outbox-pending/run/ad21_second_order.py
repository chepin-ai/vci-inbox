"""二阶可解性：零空间优化 + 余核绝对范数 + S²已知答案门。
F(p,eps)=0 的二阶可解条件为 Q^T(F_pp[p1,p1]-V2)=0，允许 p1 加任意零空间分量。
"""
import itertools,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
BASE=Path(__file__).resolve().parent.parent;RUN=BASE/'run'
sys.path.insert(0,str(RUN))
from ad21_tangent import (ts,TARGETS,ALPHA,form_terms,form_from_sphere,sphere_derivatives,
                          target_of,realvec,pm3)
TAN=json.loads((RUN/'ad21_tangent.json').read_text())

def analyze(case,kind,h=1e-4,z=None):
    form=case['form'];p0=np.asarray(case['x_polished']);seq=list(itertools.product(ts.PATH,repeat=7))[case['idx']]
    th,ph=case['theta'],case['phi'];H0=form_from_sphere(form,th,ph);T=TARGETS[form];V0=target_of(H0,T)
    _,J=ts.f_j(p0,seq,V0.reshape(-1));U,s,Vh=np.linalg.svd(J,full_matrices=True)
    rank=case['jacobian_rank'];Q=U[:,rank:];N=Vh[rank:].T
    if kind in ['theta','phi']:
        dth,dph=sphere_derivatives(form,th,ph);dH={'theta':dth,'phi':dph}[kind]
        if kind=='theta':H2=form_terms(form,-np.cos(th)/2,-np.cos(th)/2,-np.sin(th)*np.cos(ph)/2,-np.sin(th)*np.sin(ph)/2)
        else:
            w=np.sin(th)*np.cos(ph)/2;t=np.sin(th)*np.sin(ph)/2;H2=form_terms(form,0,0,-w,-t)
        extra={}
    else:
        chosen=[r for r in case['outside_candidates'] if r['outside_ratio']>.99 and r['projection_residual_ratio']<1e-8][0]
        P=pm3(chosen['pauli']);dH=1j*(P@H0-H0@P);H2=2*(P@H0@P-H0);extra={'pauli':chosen['pauli']}
    d=realvec(1j*np.sin(ALPHA)*dH@T);p10,*_=np.linalg.lstsq(J,d,rcond=1e-11)
    v2=realvec(1j*np.sin(ALPHA)*H2@T)
    def rhs(zv,hh=h):
        p1=p10+N@zv
        D2=(ts.f_j(p0+hh*p1,seq,V0.reshape(-1))[1]@p1-ts.f_j(p0-hh*p1,seq,V0.reshape(-1))[1]@p1)/(2*hh)
        return D2-v2
    if z is None:
        t0=time.time();sol=least_squares(lambda zv:Q.T@rhs(zv),np.zeros(N.shape[1]),max_nfev=180,
                                         ftol=1e-12,xtol=1e-12,gtol=1e-12)
        z=sol.x;nfev=int(sol.nfev);optimality=float(sol.optimality);seconds=time.time()-t0
    else:nfev=0;optimality=0.;seconds=0.
    rr=rhs(z);co=Q.T@rr
    stability=[]
    for hh in [1e-3,3e-4,1e-4,3e-5,1e-5]:
        rh=rhs(z,hh);stability.append({'h':hh,'cokernel_norm':float(np.linalg.norm(Q.T@rh)),'rhs_norm':float(np.linalg.norm(rh))})
    return {'kind':kind,**extra,'jacobian_rank':rank,'nullity':N.shape[1],
            'first_order_residual_ratio':float(np.linalg.norm(J@p10-d)/np.linalg.norm(d)),
            'cokernel_norm_at_zero_nullspace':float(np.linalg.norm(Q.T@rhs(np.zeros(N.shape[1])))),
            'cokernel_norm_optimized':float(np.linalg.norm(co)),'rhs_norm_optimized':float(np.linalg.norm(rr)),
            'cokernel_ratio_optimized':float(np.linalg.norm(co)/np.linalg.norm(rr)) if np.linalg.norm(rr)>1e-12 else 0.,
            'nullspace_optimization_nfev':nfev,'nullspace_optimization_optimality':optimality,'seconds':seconds,
            'finite_difference_stability':stability}

def main():
    rows=[]
    for case in TAN['cases']:
        for kind in ['theta','phi','outside']:
            r=analyze(case,kind);r['case']=case['name'];rows.append(r)
            print(json.dumps({'case':r['case'],'kind':kind,'cokernel_norm':r['cokernel_norm_optimized'],
                              'ratio':r['cokernel_ratio_optimized'],'nfev':r['nullspace_optimization_nfev']}),flush=True)
    gate={r['case']+'/'+r['kind']:r['cokernel_norm_optimized'] for r in rows if r['kind'] in ['theta','phi']}
    assert all(v<1e-6 for v in gate.values()),gate
    outside={r['case']:r['cokernel_norm_optimized'] for r in rows if r['kind']=='outside'}
    assert all(v>1e-3 for v in outside.values()),outside
    out={'beat':'AD-21','verdict':'ALL_PASS','known_answer_gate_cokernel_max':max(gate.values()),
         'known_answer_gate':gate,'outside_cokernel_norm':outside,'rows':rows,
         'boundary':'二阶有限差分/固定秩阈值的局部数值证书；不是全局不可达定理，也不替代有限电路重建。'}
    (RUN/'ad21_second_order.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'verdict':out['verdict'],'gate':gate,'outside':outside},indent=2))
if __name__=='__main__':main()
