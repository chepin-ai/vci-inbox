"""序91：新有向嵌入/反号分支的切空间与 S² 连续延拓。"""
import itertools,json,math,sys,time
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent.parent;RUN=BASE/'run'
sys.path.insert(0,str(RUN))
from ad21_tangent import ts,TARGETS,ALPHA,polish,project_tangent,realvec,PAULI_STRINGS
import ad21_geometry as g
BASE_REC=json.loads((RUN/'ad21_seq91_base.json').read_text())
PERM=tuple(BASE_REC['perm']);SIGMA=BASE_REC['sigma'];TH0=BASE_REC['theta'];PH0=BASE_REC['phi']
IDX=91;KIND='G2k7_seq91';T=TARGETS['G2'];SEQ=list(itertools.product(ts.PATH,repeat=7))[IDX]

def solve(p,H,alpha=ALPHA,max_nfev=2500):
    return polish(p,SEQ,g.target_of(H,T,alpha),max_nfev=max_nfev)
def emit(f,kind,p,e,nfev,status,H,**spec):
    r={'case':KIND,'form':'G2','idx':IDX,'perm':list(PERM),'sigma':SIGMA,'kind':kind,
       'e':float(e),'nfev':int(nfev),'status':int(status),
       'H_involution_max':float(np.max(np.abs(H@H-np.eye(8)))),'x':np.asarray(p).tolist(),**spec}
    f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush();return r
def theta_nav(f,p0,theta1):
    p=p0;n=max(1,int(math.ceil(abs(theta1-TH0)/(np.pi/24))));out=[]
    for j in range(1,n+1):
        th=TH0+(theta1-TH0)*j/n;H=g.sphere(PERM,SIGMA,th,PH0)
        p,e,nf,st=solve(p,H);r=emit(f,'theta_navigation',p,e,nf,st,H,theta=th,phi=PH0,alpha=ALPHA)
        out.append(r)
        if e>=1e-8:break
    return p,out

def tangent(p0,H0):
    V=g.target_of(H0,T,ALPHA);_,J=ts.f_j(p0,SEQ,V.reshape(-1))
    sv=np.linalg.svd(J,compute_uv=False);rank=int(np.sum(sv>sv[0]*1e-10))
    dth,dph=g.derivatives(PERM,SIGMA,TH0,PH0)
    dirs={}
    for name,d in [('alpha',(-np.sin(ALPHA)*np.eye(8)+1j*np.cos(ALPHA)*H0)@T),
                   ('theta',1j*np.sin(ALPHA)*dth@T),('phi',1j*np.sin(ALPHA)*dph@T)]:
        ratio,step=project_tangent(J,d);dirs[name]={'projection_residual_ratio':ratio,'least_squares_parameter_step':step}
    outside=[]
    for s in PAULI_STRINGS:
        P=g.pm(s);dH=1j*(P@H0-H0@P)
        if np.linalg.norm(dH)<1e-10:continue
        outr,outn=g.outside_fraction(PERM,dH)
        pr,step=project_tangent(J,1j*np.sin(ALPHA)*dH@T)
        outside.append({'pauli':s,'outside_ratio':outr,'outside_norm':outn,
                        'projection_residual_ratio':pr,'least_squares_parameter_step':step})
    outside.sort(key=lambda r:(r['projection_residual_ratio'],-r['outside_ratio']))
    return {'jacobian_rank':rank,'jacobian_singular_max':float(sv[0]),
            'jacobian_singular_min_nonzero':float(sv[rank-1]),'directions':dirs,'outside_candidates':outside}

def main():
    t0=time.time();p0=np.asarray(BASE_REC['x']);H0=g.sphere(PERM,SIGMA,TH0,PH0)
    tan=tangent(p0,H0)
    with (RUN/'ad21_seq91_continuation.jsonl').open('w',buffering=1) as f:
        for sign in [-1,1]:
            for d in [.001,.01,.1]:
                a=ALPHA+sign*d;p,e,nf,st=solve(p0,H0,a,3500)
                emit(f,'alpha_scan',p,e,nf,st,H0,theta=TH0,phi=PH0,alpha=a,delta_alpha=sign*d)
        for th in [TH0,.05,np.pi/4,np.pi/2,3*np.pi/4,np.pi-.05]:
            p,nav=theta_nav(f,p0,th)
            if nav and nav[-1]['e']>=1e-8:continue
            pl=p
            for j in range(1,13):
                ph=PH0+2*np.pi*j/12;H=g.sphere(PERM,SIGMA,th,ph)
                pl,e,nf,st=solve(pl,H)
                emit(f,'phi_loop',pl,e,nf,st,H,theta=th,phi=ph,alpha=ALPHA,latitude_origin=TH0,loop_steps=12)
                if e>=1e-8:break
        for pole in [0.,np.pi]:theta_nav(f,p0,pole)
        cand=[r for r in tan['outside_candidates'] if r['outside_ratio']>.99 and r['projection_residual_ratio']<1e-8]
        if cand:
            chosen=cand[0];P=g.pm(chosen['pauli'])
            for sign in [-1,1]:
                for d in [.001,.01,np.pi/48]:
                    eps=sign*d;C=np.cos(eps)*np.eye(8)+1j*np.sin(eps)*P;H=C@H0@C.conj().T
                    p,e,nf,st=solve(p0,H,ALPHA,4000);dH=1j*(P@H-H@P);outr,outn=g.outside_fraction(PERM,dH)
                    emit(f,'outside_fine',p,e,nf,st,H,theta=TH0,phi=PH0,alpha=ALPHA,pauli=chosen['pauli'],
                         epsilon=eps,outside_ratio=outr,outside_norm=outn)
    rows=[json.loads(s) for s in (RUN/'ad21_seq91_continuation.jsonl').read_text().splitlines() if s.strip()]
    groups={}
    for kind in sorted({r['kind'] for r in rows}):
        rr=[r for r in rows if r['kind']==kind]
        groups[kind]={'count':len(rr),'success_e_lt_1e-8':sum(r['e']<1e-8 for r in rr),
                      'e_min':min(r['e'] for r in rr),'e_max':max(r['e'] for r in rr)}
    out={'beat':'AD-21','case':KIND,'perm':list(PERM),'sigma':SIGMA,'theta':TH0,'phi':PH0,
         'base_e':BASE_REC['e'],'tangent':tan,'records':len(rows),'seconds':time.time()-t0,'groups':groups}
    (RUN/'ad21_seq91_continuation_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
