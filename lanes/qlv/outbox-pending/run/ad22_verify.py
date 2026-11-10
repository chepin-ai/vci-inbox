"""AD-22 独立验收器：不导入求解器/分析模块，只从原始JSON角度与边序重建。"""
import hashlib,itertools,json,time
from pathlib import Path
import numpy as np
RUN=Path(__file__).resolve().parent;AD21=RUN.parent.parent/'ad21/run'
ALPHA=np.pi/8;I2=np.eye(2,dtype=complex)
PAULI={'I':I2,'X':np.array([[0,1],[1,0]],complex),'Y':np.array([[0,-1j],[1j,0]],complex),'Z':np.diag([1,-1]).astype(complex)}
PATH=[(0,1),(1,2)];SEQS7=list(itertools.product(PATH,repeat=7))

def load(name):return json.loads((RUN/name).read_text())
def loadl(name):return [json.loads(s) for s in (RUN/name).read_text().splitlines() if s.strip()]
def adload(name):return json.loads((AD21/name).read_text())
def pm(s):return np.kron(np.kron(PAULI[s[0]],PAULI[s[1]]),PAULI[s[2]])
def rz(a):return np.diag([np.exp(-.5j*a),np.exp(.5j*a)])
def ry(a):return np.array([[np.cos(a/2),-np.sin(a/2)],[np.sin(a/2),np.cos(a/2)]],complex)
def su2(t):return rz(t[0])@ry(t[1])@rz(t[2])
def layer(t):return np.kron(np.kron(su2(t[0]),su2(t[1])),su2(t[2]))
def cz(edge):
    a,b=edge;d=np.ones(8,complex)
    for x in range(8):
        if ((x>>(2-a))&1) and ((x>>(2-b))&1):d[x]=-1
    return np.diag(d)
def circuit(p,edges):
    p=np.asarray(p,float);edges=[tuple(e) for e in edges];k=len(edges)
    assert len(p)==1+9*(k+1);th=p[1:].reshape(k+1,3,3)
    U=np.exp(1j*p[0])*layer(th[-1])
    for j in range(k-1,-1,-1):U=U@cz(edges[j])@layer(th[j])
    return U
def toffoli(controls,target):
    T=np.zeros((8,8),complex)
    for x in range(8):
        b=[(x>>2)&1,(x>>1)&1,x&1]
        if all(b[q] for q in controls):b[target]^=1
        T[(b[0]<<2)|(b[1]<<1)|b[2],x]=1
    return T
def cnot(c,t):
    M=np.zeros((8,8),complex)
    for x in range(8):
        b=[(x>>2)&1,(x>>1)&1,x&1]
        if b[c]:b[t]^=1
        M[(b[0]<<2)|(b[1]<<1)|b[2],x]=1
    return M
TARGETS={'G1':toffoli({0,1},2),'G2':toffoli({0,2},1)}
MAJ=toffoli({0,2},1)@cnot(1,2)@cnot(1,0)
def sname(a,b,c,sa,sb):
    s=['I']*3;s[a]=sa;s[b]=sb;s[c]='Z';return ''.join(s)
def basis_names(perm):
    a,b,c=perm;return [sname(a,b,c,'Z','X'),sname(a,b,c,'Z','I'),sname(a,b,c,'Y','I'),sname(a,b,c,'X','I'),sname(a,b,c,'Y','X'),sname(a,b,c,'X','X')]
def sphere(perm,sigma,theta,phi):
    n=basis_names(perm);u=(sigma+np.cos(theta))/2;v=(np.cos(theta)-sigma)/2
    w=np.sin(theta)*np.cos(phi)/2;t=np.sin(theta)*np.sin(phi)/2
    return u*pm(n[0])+v*pm(n[1])+w*(pm(n[2])+pm(n[4]))+t*(pm(n[3])+pm(n[5]))
def target_of(H,T,alpha=ALPHA):return (np.cos(alpha)*np.eye(8)+1j*np.sin(alpha)*H)@T
def realvec(M):
    z=np.asarray(M).reshape(-1);return np.concatenate([z.real,z.imag])
def op(q,A):
    m=[I2,I2,I2];m[q]=A;return np.kron(np.kron(m[0],m[1]),m[2])
def local_R(a,delta):return op(a,rz(-delta))
def controlled_W(a,b,delta):
    X=PAULI['X'];pp=(I2+X)/2;pm_=(I2-X)/2;t=delta
    Rx=np.cos(t/2)*I2+1j*np.sin(t/2)*X
    return op(b,pm_)+op(b,pp)@op(a,Rx)
def close(a,b,tol=3e-9):return bool(np.isfinite(a) and np.isfinite(b) and abs(a-b)<=tol*max(1.,abs(a),abs(b)))

def residual_jacobian(p,edges,T):
    p=np.asarray(p,float);k=len(edges);th=p[1:].reshape(k+1,3,3);mats=[]
    for i in range(k+1):
        mats.append(layer(th[i]))
        if i<k:mats.append(cz(edges[i]))
    n=len(mats);pre=[None]*(n+1);pre[0]=np.eye(8,dtype=complex)
    for j in range(n):pre[j+1]=mats[j]@pre[j]
    post=[None]*(n+1);post[n-1]=np.eye(8,dtype=complex)
    for j in range(n-2,-1,-1):post[j]=post[j+1]@mats[j+1]
    phase=np.exp(1j*p[0]);U=phase*pre[n];F=U.reshape(-1)-T.reshape(-1)
    f=np.concatenate([F.real,F.imag]);J=np.zeros((128,len(p)));dU=1j*U
    J[:,0]=np.concatenate([dU.reshape(-1).real,dU.reshape(-1).imag]);col=1
    for i in range(k+1):
        base=[su2(th[i,q]) for q in range(3)]
        for q in range(3):
            a,b,c=th[i,q];dra=np.diag([-.5j*np.exp(-.5j*a),.5j*np.exp(.5j*a)])
            drb=np.array([[-.5*np.sin(b/2),-.5*np.cos(b/2)],[.5*np.cos(b/2),-.5*np.sin(b/2)]])
            drc=np.diag([-.5j*np.exp(-.5j*c),.5j*np.exp(.5j*c)])
            for dl in [dra@ry(b)@rz(c),rz(a)@drb@rz(c),rz(a)@ry(b)@drc]:
                parts=list(base);parts[q]=dl;dL=np.kron(np.kron(parts[0],parts[1]),parts[2])
                dU=phase*(post[2*i]@dL@pre[2*i]);J[:,col]=np.concatenate([dU.reshape(-1).real,dU.reshape(-1).imag]);col+=1
    return f,J

def extract_H(x,idx,T):
    U=circuit(x,SEQS7[idx]);vals,vecs=np.linalg.eig(U@T);angles=np.angle(vals)
    K=vecs@np.diag(angles)@np.linalg.inv(vecs);H=(K/ALPHA);return (H+H.conj().T)/2,angles,float(np.max(np.abs(U-T)))
def fit_one(H,perm,sigma):
    names=basis_names(perm);co=np.array([float((np.trace(pm(s)@H)/8).real) for s in names]);u,v,w,t=co[:4]
    th=float(np.arccos(np.clip(u+v,-1,1)));ph=float(np.arctan2(t,w));H0=sphere(perm,sigma,th,ph)
    return {'perm':list(perm),'sigma':int(sigma),'theta':th,'phi':ph,'delta':float(np.max(np.abs(H-H0))),'H0_involution':float(np.max(np.abs(H0@H0-np.eye(8))))}
def classify(x,idx,T):
    H,angles,direct=extract_H(x,idx,T);ff=sorted([fit_one(H,p,s) for p in itertools.permutations(range(3)) for s in [1,-1]],key=lambda r:r['delta']);best=ff[0]
    return {'direct_e_rebuilt':direct,'angle_max_dev_rad':float(np.max(np.abs(np.abs(angles)-ALPHA))),
            'H_involution_max':float(np.max(np.abs(H@H-np.eye(8)))),'best_perm':best['perm'],'best_sigma':best['sigma'],
            'best_ansatz_max_delta':best['delta'],'runner_up_ansatz_max_delta':ff[1]['delta']}
def basin_hit(e,c):return bool(e<.205 and c['angle_max_dev_rad']<1e-5 and c['H_involution_max']<1e-4 and c['best_perm']==[2,1,0] and c['best_sigma']==-1 and c['best_ansatz_max_delta']<1e-4)


def known_answer_gate():
    rng=np.random.default_rng(220022);mu=ms=0.
    for k in [0,1,2,7]:
        edges=[PATH[(3*j+1)%2] for j in range(k)];p=rng.normal(size=1+9*(k+1));U=circuit(p,edges)
        mu=max(mu,float(np.max(np.abs(U@U.conj().T-np.eye(8)))))
    for perm in itertools.permutations(range(3)):
        for sigma in [-1,1]:
            for th in np.linspace(.02,np.pi-.02,5):
                for ph in np.linspace(-np.pi,np.pi,6,endpoint=False):
                    H=sphere(perm,sigma,th,ph);ms=max(ms,float(np.max(np.abs(H@H-np.eye(8)))))
    old=adload('ad21_maj_8cz.json')['solutions'][0];e8=float(np.max(np.abs(circuit(old['x'],old['edges'])-MAJ)))
    ident=float(np.max(np.abs(MAJ@cnot(1,0)@cnot(1,2)-toffoli({0,2},1))))
    assert mu<3e-13 and ms<3e-13 and e8<1e-11 and ident<1e-12,(mu,ms,e8,ident)
    return {'random_circuit_unitarity_max':mu,'sphere_involution_max':ms,'ad21_known_8cz_e':e8,'maj_toffoli_identity':ident}

def verify_sphere():
    pack=load('ad22_sphere_closed.json');me=md=0.
    for r in pack['phi_circuits']:
        a,b,c=r['perm'];T=toffoli({a,c},b);H=sphere(tuple(r['perm']),r['sigma'],r['theta'],r['phi']);V=target_of(H,T)
        e=float(np.max(np.abs(circuit(r['x'],SEQS7[r['idx']])-V)));assert close(e,r['e'],3e-9),(r['case'],r['delta_phi'],e,r['e'])
        me=max(me,e);md=max(md,abs(e-r['e']))
    assert len(pack['phi_circuits'])==75 and me<1e-8
    rng=np.random.default_rng(227000);mh=mv=mc=mp=0.;count=0
    for perm in itertools.permutations(range(3)):
        a,b,c=perm;T=toffoli({a,c},b)
        for sigma in [-1,1]:
            for _ in range(24):
                th0,ph0=rng.uniform(.03,np.pi-.03),rng.uniform(-np.pi,np.pi);th,ph=rng.uniform(0,np.pi),rng.uniform(-np.pi,np.pi)
                H0=sphere(perm,sigma,th0,ph0);H=sphere(perm,sigma,th,ph);R0=local_R(a,ph0);W0=controlled_W(a,b,th0);R=local_R(a,ph)
                pole=sphere(perm,sigma,0.,0.);H00=R0@W0@pole@W0.conj().T@R0.conj().T
                A=R@controlled_W(a,b,th-th0)@R0.conj().T;V0=target_of(H0,T);V=target_of(H,T)
                mh=max(mh,float(np.max(np.abs(H-A@H0@A.conj().T))));mv=max(mv,float(np.max(np.abs(V-A@V0@A.conj().T))))
                mc=max(mc,float(np.max(np.abs(A@T-T@A))));mp=max(mp,float(np.max(np.abs(H0-H00))));count+=1
    assert count==288 and max(mh,mv,mc,mp)<2e-12,(mh,mv,mc,mp)
    return {'phi_circuits':75,'max_phi_circuit_e':me,'max_record_delta':md,'global_cases':count,
            'sphere_identity_max':mh,'target_identity_max':mv,'toffoli_commutation_max':mc,'pole_identity_max':mp,
            'boundary':'解析纬圈为同7-CZ模板定理；全S²目标共轭不等于theta经线同模板电路覆盖。'}

def verify_maj():
    rows=loadl('ad22_maj_multistart.jsonl');assert len(rows)==1920
    assert len({(r['k'],r['idx'],r['restart']) for r in rows})==1920
    groups={};hits=[];md=0.
    for r in rows:
        assert 'error' not in r;e=float(np.max(np.abs(circuit(r['x'],r['edges'])-MAJ)));assert close(e,r['e'],3e-9),(r['k'],r['idx'],r['restart'],e,r['e'])
        md=max(md,abs(e-r['e']));g=groups.setdefault(r['k'],{'runs':0,'exact':0,'best_e':np.inf,'best_idx':None,'best_restart':None})
        g['runs']+=1;g['exact']+=int(e<1e-9)
        if e<g['best_e']:g.update(best_e=e,best_idx=r['idx'],best_restart=r['restart'])
        if e<1e-9:hits.append({'k':r['k'],'idx':r['idx'],'restart':r['restart'],'edges':r['edges'],'x':r['x'],'independent_e':e})
    assert [groups[k]['exact'] for k in [4,5,6,7]]==[0,0,0,7],groups
    assert all(groups[k]['runs']==128*2**(k-4) for k in [4,5,6,7])
    dele=loadl('ad22_maj_delete7.jsonl');assert len(dele)==392 and len({(r['source_idx'],r['delete'],r['restart']) for r in dele})==392
    dbest=np.inf;dhits=0;dd=0.
    for r in dele:
        assert 'error' not in r;e=float(np.max(np.abs(circuit(r['x'],r['edges'])-MAJ)));assert close(e,r['e'],3e-9),(r['source_idx'],r['delete'],r['restart'],e,r['e'])
        dbest=min(dbest,e);dhits+=int(e<1e-9);dd=max(dd,abs(e-r['e']))
    assert dhits==0
    return {'multistart_runs':1920,'max_record_delta':md,'by_k':groups,'hits7':hits,
            'delete7_runs':392,'delete7_exact':dhits,'delete7_best_e':dbest,'delete7_max_record_delta':dd,
            'strict_interval':'4 <= k <= 7','boundary':'k=4,5,6及删门零命中均为L2数值否证，不宣称7最优。'}


def verify_basin():
    base=adload('ad21_seq91_base.json');H=sphere(tuple(base['perm']),base['sigma'],base['theta'],base['phi']);V=target_of(H,TARGETS['G2'])
    allrows=[];files={}
    for fn in ['ad22_seq91_metric.jsonl','ad22_seq91_metric_extended.jsonl']:
        rows=loadl(fn);out=[];md=0.
        for r in rows:
            e=float(np.max(np.abs(circuit(r['x'],SEQS7[91])-V)));assert close(e,r['e_target'],3e-8),(fn,r['direction'],r['radius'],r['method'],r['null_mode'],e,r['e_target'])
            exact=bool(e<1e-8);assert exact==r['exact_return']
            if e<.205:
                c=classify(r['x'],91,TARGETS['G2']);sig=basin_hit(e,c)
            else:sig=False
            assert sig==r['signature_hit'],(fn,r['direction'],r['radius'],r['method'],r['null_mode'],e,sig,r['signature_hit'])
            q=dict(r);q['independent_e']=e;q['independent_exact']=exact;q['independent_signature']=sig;out.append(q);md=max(md,abs(e-r['e_target']))
        files[fn]={'records':len(out),'exact':sum(q['independent_exact'] for q in out),'signature':sum(q['independent_signature'] for q in out),'max_record_delta':md};allrows+=out
    assert files['ad22_seq91_metric.jsonl']['records']==384 and files['ad22_seq91_metric.jsonl']['exact']==384
    assert files['ad22_seq91_metric_extended.jsonl']['records']==144 and files['ad22_seq91_metric_extended.jsonl']['exact']==82
    gauge=solver=0;gn=sn=0
    for direction in range(12):
        for radius in sorted({q['radius'] for q in allrows}):
            for method in ['lm','trf']:
                z=[q for q in allrows if q['direction']==direction and q['radius']==radius and q['method']==method];assert len(z)==2
                gn+=1;gauge+=int(len({(q['independent_exact'],q['independent_signature']) for q in z})==1)
            for null in [0,1]:
                z=[q for q in allrows if q['direction']==direction and q['radius']==radius and q['null_mode']==null];assert len(z)==2
                sn+=1;solver+=int(len({(q['independent_exact'],q['independent_signature']) for q in z})==1)
    _,J=residual_jacobian(base['x'],SEQS7[91],V);sv=np.linalg.svd(J,compute_uv=False);rank=int(np.sum(sv>1e-7));assert rank==33 and 1e-8<sv[33]<1e-7
    return {'files':files,'total_runs':len(allrows),'total_exact':sum(q['independent_exact'] for q in allrows),
            'gauge_pair_agreement':[gauge,gn],'solver_pair_agreement':[solver,sn],'rank_absolute_threshold':rank,
            'singular_rank_boundary':[float(sv[32]),float(sv[33])],
            'boundary':'r<=2全返回非无限盆宽证明；r>=3分歧非全局吸引盆体积或解流形测地距离。'}

def setup_case(case):
    form=case['form'];perm=(1,2,0) if form=='G1' else (0,1,2);p0=np.asarray(case['x_polished']);seq=SEQS7[case['idx']]
    th,ph=case['theta'],case['phi'];H0=sphere(perm,1,th,ph);T=TARGETS[form];V0=target_of(H0,T)
    _,J=residual_jacobian(p0,seq,V0);U,s,Vh=np.linalg.svd(J,full_matrices=True);rank=int(np.sum(s>s[0]*1e-10));Q=U[:,rank:];N=Vh[rank:].T
    return {'case':case,'form':form,'perm':perm,'p0':p0,'seq':seq,'th':th,'ph':ph,'H0':H0,'T':T,'V0':V0,'J':J,'Q':Q,'N':N,'rank':rank}
def form_terms(form,u,v,w,t):
    perm=(1,2,0) if form=='G1' else (0,1,2);n=basis_names(perm)
    return u*pm(n[0])+v*pm(n[1])+w*(pm(n[2])+pm(n[4]))+t*(pm(n[3])+pm(n[5]))
def direction(st,kind,pauli=None):
    th,ph,form,H0,T=st['th'],st['ph'],st['form'],st['H0'],st['T']
    if kind in ('theta','phi'):
        du,dv=-np.sin(th)/2,-np.sin(th)/2;dw,dt=np.cos(th)*np.cos(ph)/2,np.cos(th)*np.sin(ph)/2
        dth=form_terms(form,du,dv,dw,dt);dph=form_terms(form,0,0,-np.sin(th)*np.sin(ph)/2,np.sin(th)*np.cos(ph)/2)
        if kind=='theta':dH=dth;H2=form_terms(form,-np.cos(th)/2,-np.cos(th)/2,-np.sin(th)*np.cos(ph)/2,-np.sin(th)*np.sin(ph)/2)
        else:dH=dph;H2=form_terms(form,0,0,-np.sin(th)*np.cos(ph)/2,-np.sin(th)*np.sin(ph)/2)
    else:
        P=pm(pauli);dH=1j*(P@H0-H0@P);H2=2*(P@H0@P-H0)
    d=realvec(1j*np.sin(ALPHA)*dH@T);v2=realvec(1j*np.sin(ALPHA)*H2@T);p10,*_=np.linalg.lstsq(st['J'],d,rcond=1e-11)
    return d,v2,p10

def verify_outside():
    tan=adload('ad21_tangent.json');cases={c['name']:c for c in tan['cases']};pack=load('ad22_outside_all.json');rows=[];md=0.
    for r in pack['rows']:
        st=setup_case(cases[r['case']]);d,v2,p10=direction(st,r['kind'],r.get('pauli'));J,Q,N,p0,seq,V0=st['J'],st['Q'],st['N'],st['p0'],st['seq'],st['V0']
        best=r['runs'][r['best_start_index']];z=np.asarray(best['z']);p1=p10+N@z;h=1e-4
        D2=(residual_jacobian(p0+h*p1,seq,V0)[1]@p1-residual_jacobian(p0-h*p1,seq,V0)[1]@p1)/(2*h)
        val=float(np.linalg.norm(Q.T@(D2-v2)));assert close(val,r['best_cokernel_norm'],2e-6),(r['case'],r['kind'],r.get('pauli'),val,r['best_cokernel_norm'])
        rows.append({'case':r['case'],'kind':r['kind'],'pauli':r.get('pauli'),'independent_cokernel':val});md=max(md,abs(val-r['best_cokernel_norm']))
    gates=[r['independent_cokernel'] for r in rows if r['kind']!='outside'];outs=[r['independent_cokernel'] for r in rows if r['kind']=='outside']
    assert max(gates)<1e-6 and min(outs)>1.
    mixed=load('ad22_mixed_jet.json');mr=[];mmd=0.
    for r in mixed['rows']:
        st=setup_case(cases[r['case']]);fixed=r['fixed_pauli'];variable=r['variable_paulis'];Ps={s:pm(s) for s in [fixed]+variable};H0,T=st['H0'],st['T'];J,Q,N,p0,seq,V0=st['J'],st['Q'],st['N'],st['p0'],st['seq'],st['V0']
        dh=lambda P:1j*(P@H0-H0@P);d0=realvec(1j*np.sin(ALPHA)*dh(Ps[fixed])@T);D=np.column_stack([realvec(1j*np.sin(ALPHA)*dh(Ps[s])@T) for s in variable])
        p10,*_=np.linalg.lstsq(J,d0,rcond=1e-11);A,*_=np.linalg.lstsq(J,D,rcond=1e-11);W=np.column_stack([A,N]);m=len(variable)
        best=r['runs'][r['best_start_index']];y=np.asarray(best['y']);c=y[:m];p1=p10+W@y;P=Ps[fixed].copy()
        for ci,s in zip(c,variable):P=P+ci*Ps[s]
        H2=2*P@H0@P-P@P@H0-H0@P@P;v2=realvec(1j*np.sin(ALPHA)*H2@T);h=1e-4
        D2=(residual_jacobian(p0+h*p1,seq,V0)[1]@p1-residual_jacobian(p0-h*p1,seq,V0)[1]@p1)/(2*h)
        val=float(np.linalg.norm(Q.T@(D2-v2)));assert close(val,r['best_cokernel_norm'],2e-6),(r['case'],fixed,val,r['best_cokernel_norm'])
        mr.append({'case':r['case'],'fixed':fixed,'independent_cokernel':val});mmd=max(mmd,abs(val-r['best_cokernel_norm']))
    assert min(r['independent_cokernel'] for r in mr)>2.
    return {'outside_rows':rows,'known_answer_gate_max':max(gates),'outside_min':min(outs),'max_record_delta':md,
            'mixed_rows':mr,'mixed_min':min(r['independent_cokernel'] for r in mr),'mixed_max_record_delta':mmd,
            'boundary':'固定秩、中心差分与多种子最优点的独立残差复核；非二次系统全局不存在证明。'}


def main():
    t0=time.time();checks={'known_answer_gate':known_answer_gate()}
    for name,fn in [('sphere_closed',verify_sphere),('maj',verify_maj),('seq91_basin',verify_basin),('outside_second_order',verify_outside)]:
        print(json.dumps({'event':'verify_start','check':name}),flush=True);checks[name]=fn();print(json.dumps({'event':'verify_pass','check':name,'elapsed':time.time()-t0}),flush=True)
    names=['ad22_sphere_closed.json','ad22_maj_multistart.jsonl','ad22_maj_multistart_summary.json','ad22_maj_7cz.json',
           'ad22_maj_delete7.jsonl','ad22_maj_delete7_summary.json','ad22_seq91_metric.jsonl','ad22_seq91_metric_extended.jsonl',
           'ad22_outside_all.json','ad22_mixed_jet.json']
    hashes={n:hashlib.sha256((RUN/n).read_bytes()).hexdigest() for n in names}
    out={'beat':'AD-22','status':'ALL_PASS','seconds':time.time()-t0,'checks':checks,'input_sha256':hashes,
         'rac':'对方S_sim指纹未到件；未启动跨线对拍；量子机时=0。','private_ci_consumption':0,'quantum_machine_consumption':0,
         'anomaly_notes':['rank34奇异值伪方向原始账保留；绝对阈1e-7后rank33重跑。',
                          '独立MAJ重建器初版因子顺序错误，作废后以AD-21已知8-CZ门复验。',
                          '删门流式JSONL两次NUL空洞均保留；关闭进程池后第三次完整392条入账。',
                          '进程自检曾误回显环境变量；不转录、不入仓，后续禁止完整命令行诊断。']}
    (RUN/'ad22_verify.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'seconds':out['seconds'],'maj':{k:v for k,v in checks['maj'].items() if k!='hits7'},
                      'basin':checks['seq91_basin'],'sphere':{k:v for k,v in checks['sphere_closed'].items() if k!='boundary'},
                      'outside_min':checks['outside_second_order']['outside_min'],'mixed_min':checks['outside_second_order']['mixed_min']},indent=2))
if __name__=='__main__':main()
