"""AD-21 α 与 ansatz 外方向的小步长残差阶数诊断；保留AD-21粗扫负账。"""
import itertools,json,sys,time
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent.parent;RUN=BASE/'run'
sys.path.insert(0,str(RUN))
from ad21_tangent import ts,TARGETS,ALPHA,form_from_sphere,target_of,polish,pm3,outside_fraction
TANGENT=json.loads((RUN/'ad21_tangent.json').read_text())
DELTAS=[1e-5,3e-5,1e-4,3e-4,1e-3,3e-3,1e-2]

def emit(case,kind,delta,p,e,nfev,status,H,**kw):
    r={'case':case['name'],'form':case['form'],'idx':case['idx'],'kind':kind,'delta':delta,
       'abs_delta':abs(delta),'e':float(e),'nfev':int(nfev),'status':int(status),
       'H_involution_max':float(np.max(np.abs(H@H-np.eye(8)))),'x':np.asarray(p).tolist(),**kw}
    return r

def main():
    t0=time.time();rows=[]
    with (RUN/'ad21_highorder.jsonl').open('w',buffering=1) as f:
        for case in TANGENT['cases']:
            form=case['form'];seq=list(itertools.product(ts.PATH,repeat=7))[case['idx']]
            p0=np.asarray(case['x_polished']);th0,ph0=case['theta'],case['phi'];T=TARGETS[form]
            H0=form_from_sphere(form,th0,ph0)
            for sign in [-1,1]:
                for d in DELTAS:
                    delta=sign*d;a=ALPHA+delta
                    p,e,nfev,status=polish(p0,seq,target_of(H0,T,a),max_nfev=4000)
                    r=emit(case,'alpha_fine',delta,p,e,nfev,status,H0,alpha=a)
                    rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
            candidates=[r for r in case['outside_candidates'] if r['outside_ratio']>.99 and r['projection_residual_ratio']<1e-8]
            if candidates:
                chosen=candidates[0];P=pm3(chosen['pauli'])
                for sign in [-1,1]:
                    for d in DELTAS:
                        eps=sign*d;C=np.cos(eps)*np.eye(8)+1j*np.sin(eps)*P
                        H=C@H0@C.conj().T
                        p,e,nfev,status=polish(p0,seq,target_of(H,T,ALPHA),max_nfev=4000)
                        delta_H=1j*(P@H-H@P);out_ratio,out_norm=outside_fraction(form,delta_H)
                        r=emit(case,'outside_fine',eps,p,e,nfev,status,H,pauli=chosen['pauli'],
                               outside_ratio=out_ratio,outside_norm=out_norm)
                        rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
            print(json.dumps({'event':'case_done','case':case['name'],'elapsed':time.time()-t0}),flush=True)
    groups={}
    for case in TANGENT['cases']:
        for kind in ['alpha_fine','outside_fine']:
            for sign in [-1,1]:
                rr=[r for r in rows if r['case']==case['name'] and r['kind']==kind and np.sign(r['delta'])==sign]
                if not rr:continue
                x=np.array([r['abs_delta'] for r in rr]);y=np.array([max(r['e'],1e-300) for r in rr])
                slope,intercept=np.polyfit(np.log(x),np.log(y),1)
                groups[f"{case['name']}/{kind}/sign{sign}"]={
                    'count':len(rr),'success_e_lt_1e-8':sum(r['e']<1e-8 for r in rr),
                    'loglog_slope':float(slope),'log_intercept':float(intercept),
                    'e_over_delta_median':float(np.median(y/x)),'e_over_delta2_median':float(np.median(y/x**2)),
                    'points':[{'delta':r['delta'],'e':r['e'],'nfev':r['nfev'],'status':r['status']} for r in rr]}
    out={'beat':'AD-21','records':len(rows),'seconds':time.time()-t0,'groups':groups,
         'note':'斜率是固定求解器/边序/起点的有限数值残差阶数，不是全局不可达定理。'}
    (RUN/'ad21_highorder_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
