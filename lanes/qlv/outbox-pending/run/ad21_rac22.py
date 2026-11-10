"""RAC(2,2) 零机时双模拟器对拍：16输出χ² + Hamming parityχ²，240发/路/电路。
对方S_sim指纹未到，故本件是QLV侧参考账，不声称跨线/真机对拍。
"""
import hashlib,itertools,json
from pathlib import Path
import numpy as np
from scipy.stats import chi2
RUN=Path(__file__).resolve().parent
MAP={0:0,2:6,3:12,1:7};PH=sorted(MAP.values());IX={q:i for i,q in enumerate(PH)}
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]);S=np.diag([1,1j]);SHOTS=240;ALPHA_HOLM=.01

def build(x1,x2,y):
    g=[]
    def h(q):g.append(('H',(q,),None))
    def cx(c,t):h(t);g.append(('CZ',(c,t),None));h(t)
    h(0);h(1);cx(0,2);cx(1,3)
    if x1:cx(0,1);g.append(('X',(0,),None))
    if x2:g.append(('S',(0,),None));g.append(('Z',(1,),None))
    if y==2:
        for a,b in [(0,1),(2,3)]:
            cx(a,b);cx(b,a);cx(a,b);h(a);th=-np.pi/2
            g.append(('RZ',(b,),th/2));cx(a,b);g.append(('RZ',(b,),-th/2));cx(a,b);g.append(('RZ',(a,),th/2));h(b)
    for q in range(4):g.append(('M',(q,),None))
    return g

def qcis(g):
    out=[]
    for op,qs,p in g:
        if op in ('H','X','Z','S','M'):out.append(f'{op} Q{MAP[qs[0]]}')
        elif op=='CZ':out.append(f'CZ Q{MAP[qs[0]]} Q{MAP[qs[1]]}')
        elif op=='RZ':out.append(f'RZ Q{MAP[qs[0]]} {p:.10f}')
    return '\n'.join(out)

def matrix_sim(g):
    st=np.zeros(16,complex);st[0]=1
    def one(q,U):
        ops=[np.eye(2)]*4;ops[IX[MAP[q]]]=U
        M=np.kron(np.kron(ops[0],ops[1]),np.kron(ops[2],ops[3]));return M
    for op,qs,p in g:
        if op=='M':continue
        if op in ('H','X','Z','S'):st=one(qs[0],{'H':H,'X':X,'Z':Z,'S':S}[op])@st
        elif op=='RZ':st=one(qs[0],np.diag([np.exp(-1j*p/2),np.exp(1j*p/2)]))@st
        elif op=='CZ':
            a,b=IX[MAP[qs[0]]],IX[MAP[qs[1]]];d=np.ones(16)
            for s in range(16):
                if ((s>>(3-a))&1) and ((s>>(3-b))&1):d[s]=-1
            st=d*st
    return np.abs(st)**2

def tensor_sim(g):
    st=np.zeros((2,2,2,2),complex);st[(0,0,0,0)]=1
    def one(q,U):
        nonlocal st;k=IX[MAP[q]]
        z=np.tensordot(U,st,axes=([1],[k]));st=np.moveaxis(z,0,k)
    for op,qs,p in g:
        if op=='M':continue
        if op in ('H','X','Z','S'):one(qs[0],{'H':H,'X':X,'Z':Z,'S':S}[op])
        elif op=='RZ':one(qs[0],np.diag([np.exp(-1j*p/2),np.exp(1j*p/2)]))
        elif op=='CZ':
            a,b=IX[MAP[qs[0]]],IX[MAP[qs[1]]]
            for s in range(16):
                if ((s>>(3-a))&1) and ((s>>(3-b))&1):
                    idx=tuple((s>>(3-i))&1 for i in range(4));st[idx]*=-1
    return np.abs(st.reshape(-1))**2

def bits(s):return [(s>>(3-i))&1 for i in range(4)]
def decode(dist,m):
    ok=0.;sA0,sA1,sB0,sB1=IX[MAP[0]],IX[MAP[1]],IX[MAP[2]],IX[MAP[3]]
    for s,p in enumerate(dist):
        b=bits(s);iA=b[sA0]+2*b[sA1];iB=b[sB0]+2*b[sB1]
        if (m['y']==1 and (iA-iB)%4==m['x1']) or (m['y']==2 and (iA+iB)%4==m['x2']):ok+=p
    return float(ok)
def chi2_two(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float);mask=a+b>0
    stat=float(np.sum((a[mask]-b[mask])**2/(a[mask]+b[mask])));df=int(mask.sum()-1)
    return {'statistic':stat,'df':df,'p_value':float(chi2.sf(stat,df)) if df>0 else 1.0}
def parity_counts(counts):
    return [int(sum(c for s,c in enumerate(counts) if sum(bits(s))%2==par)) for par in [0,1]]
def holm(rows,key):
    m=len(rows);order=sorted(range(m),key=lambda i:rows[i][key]['p_value']);adj=[0.]*m;running=0.
    for rank,i in enumerate(order):
        running=max(running,(m-rank)*rows[i][key]['p_value']);adj[i]=min(1.,running)
    return adj

def main():
    # 已知答案门：H|0>与Bell态先在两条独立实现上同时通过。
    bell=[('H',(0,),None),('H',(2,),None),('CZ',(0,2),None),('H',(2,),None)]
    # 使用自定义H+CZ+H=CNOT(0→2)，随后两个模拟器应给出00/11（逻辑0,2）。
    g0=[('H',(0,),None)]
    assert np.max(np.abs(matrix_sim(g0)-tensor_sim(g0)))<1e-14
    a,b=matrix_sim(bell),tensor_sim(bell)
    assert np.max(np.abs(a-b))<1e-14 and abs(a[0]-.5)<1e-14 and abs(a[12]-.5)<1e-14,(a,b)
    metas=[{'x1':x1,'x2':x2,'y':y} for x1,x2 in itertools.product([0,1],[0,1]) for y in [1,2]]
    rows=[]
    for i,m in enumerate(metas):
        g=build(m['x1'],m['x2'],m['y']);txt=qcis(g);da,db=matrix_sim(g),tensor_sim(g)
        delta=float(np.max(np.abs(da-db)));sa,sb=decode(da,m),decode(db,m)
        ca=np.bincount(np.random.default_rng(20261110+i).choice(16,size=SHOTS,p=da),minlength=16)
        cb=np.bincount(np.random.default_rng(20261210+i).choice(16,size=SHOTS,p=db),minlength=16)
        rows.append({'index':i,**m,'qcis_sha256':hashlib.sha256(txt.encode()).hexdigest(),'qcis':txt,
                     'distribution_max_abs_delta':delta,'S_matrix':sa,'S_tensor':sb,
                     'shots_per_simulator':SHOTS,'counts_matrix':ca.tolist(),'counts_tensor':cb.tolist(),
                     'success_counts_matrix':int(round(decode(ca,m))),'success_counts_tensor':int(round(decode(cb,m))),
                     'chi2_16outcome':chi2_two(ca,cb),'parity_counts_matrix':parity_counts(ca),'parity_counts_tensor':parity_counts(cb),
                     'chi2_hamming_parity':chi2_two(parity_counts(ca),parity_counts(cb))})
    adj16=holm(rows,'chi2_16outcome');adjp=holm(rows,'chi2_hamming_parity')
    for r,a,p in zip(rows,adj16,adjp):r['holm_p_16outcome']=a;r['holm_p_hamming_parity']=p
    exact_ok=all(r['distribution_max_abs_delta']<1e-12 and r['S_matrix']>1-1e-12 and r['S_tensor']>1-1e-12 for r in rows)
    shots_ok=all(r['success_counts_matrix']==SHOTS and r['success_counts_tensor']==SHOTS for r in rows)
    stats_ok=all(r['holm_p_16outcome']>=ALPHA_HOLM and r['holm_p_hamming_parity']>=ALPHA_HOLM for r in rows)
    out={'beat':'AD-21','verdict':'ALL_PASS' if exact_ok and shots_ok and stats_ok else 'CHECK',
         'scope':'QLV侧零机时双模拟器参考账；非跨线S_sim对拍，非真机结果',
         'known_answer_gate':'H|0>与逻辑0,2 Bell态，矩阵/张量双实现通过',
         'shots':SHOTS,'seed_matrix_base':20261110,'seed_tensor_base':20261210,
         'holm_alpha':ALPHA_HOLM,'exact_ok':exact_ok,'shots_success_ok':shots_ok,'sampling_compatibility_ok':stats_ok,
         'S_sim_mean_matrix':float(np.mean([r['S_matrix'] for r in rows])),'S_sim_mean_tensor':float(np.mean([r['S_tensor'] for r in rows])),
         'min_holm_p_16outcome':min(adj16),'min_holm_p_hamming_parity':min(adjp),'circuits':rows}
    (RUN/'ad21_rac22_xval.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='circuits'},indent=2))
    print('per_circuit',json.dumps([{'i':r['index'],'chi2_p':r['chi2_16outcome']['p_value'],'parity_p':r['chi2_hamming_parity']['p_value'],
                                   'holm16':r['holm_p_16outcome'],'holm_parity':r['holm_p_hamming_parity']} for r in rows]))
if __name__=='__main__':main()
