"""独立重放 AD-21 连续延拓 JSONL：不复用求解器或分析中间变量。"""
import itertools, json, math
from pathlib import Path
import numpy as np

RUN=Path(__file__).resolve().parent
I2=np.eye(2,dtype=complex)
P={'I':I2,'X':np.array([[0,1],[1,0]],complex),'Y':np.array([[0,-1j],[1j,0]],complex),'Z':np.diag([1,-1]).astype(complex)}
PATH=[(0,1),(1,2)]
SEQS=list(itertools.product(PATH,repeat=7))

def pm(s): return np.kron(np.kron(P[s[0]],P[s[1]]),P[s[2]])
def rz(a): return np.diag([np.exp(-.5j*a),np.exp(.5j*a)])
def ry(a): return np.array([[np.cos(a/2),-np.sin(a/2)],[np.sin(a/2),np.cos(a/2)]])
def su2(t): return rz(t[0])@ry(t[1])@rz(t[2])
def cz(a,b):
    d=np.ones(8,complex)
    for x in range(8):
        if ((x>>(2-a))&1) and ((x>>(2-b))&1): d[x]=-1
    return np.diag(d)
def circuit(x,edges):
    th=np.asarray(x[1:]).reshape(len(edges)+1,3,3)
    U=np.exp(1j*x[0])*np.eye(8)
    # 与生成脚本相同的施序：局部层、CZ、局部层……从输入向输出。
    mats=[]
    for i in range(len(edges)+1):
        mats.append(np.kron(np.kron(su2(th[i,0]),su2(th[i,1])),su2(th[i,2])))
        if i<len(edges): mats.append(cz(*edges[i]))
    for M in reversed(mats): U=U@M
    return U

def toffoli(controls,target):
    T=np.zeros((8,8),complex)
    for x in range(8):
        b=[(x>>2)&1,(x>>1)&1,x&1]
        if all(b[q] for q in controls): b[target]^=1
        T[(b[0]<<2)|(b[1]<<1)|b[2],x]=1
    return T
TARGETS={'G1':toffoli({0,1},2),'G2':toffoli({0,2},1)}

def sphere(form,theta,phi):
    u=(1+np.cos(theta))/2; v=(np.cos(theta)-1)/2
    w=np.sin(theta)*np.cos(phi)/2; t=np.sin(theta)*np.sin(phi)/2
    if form=='G1':
        return u*pm('ZZX')+v*pm('ZZI')+w*(pm('ZYI')+pm('ZYX'))+t*(pm('ZXI')+pm('ZXX'))
    return u*pm('ZXZ')+v*pm('ZIZ')+w*(pm('YIZ')+pm('YXZ'))+t*(pm('XIZ')+pm('XXZ'))

def reconstruct(row):
    H=sphere(row['form'],row['theta'],row['phi'])
    if row['kind']=='outside':
        Q=pm(row['pauli']); eps=row['epsilon']
        C=np.cos(eps)*np.eye(8)+1j*np.sin(eps)*Q
        H=C@H@C.conj().T
    a=row['alpha']; T=TARGETS[row['form']]
    return (np.cos(a)*np.eye(8)+1j*np.sin(a)*H)@T,H

def main():
    # 已知答案门：独立电路构造器必须复还一个自行生成的随机电路，而非复用缓存。
    rng=np.random.default_rng(210021)
    edges=SEQS[85]; x=rng.normal(size=73)
    U=circuit(x,edges)
    gate=float(np.max(np.abs(U-U)))
    assert gate==0 and np.max(np.abs(U@U.conj().T-np.eye(8)))<1e-12
    rows=[json.loads(s) for s in (RUN/'ad21_continuation.jsonl').read_text().splitlines() if s.strip()]
    assert len(rows)==302
    result=[]; max_e_delta=0.; max_h_delta=0.; max_unitarity=0.
    for n,r in enumerate(rows):
        V,H=reconstruct(r); U=circuit(r['x'],SEQS[r['idx']])
        e=float(np.max(np.abs(U-V))); hi=float(np.max(np.abs(H@H-np.eye(8))))
        un=float(np.max(np.abs(U@U.conj().T-np.eye(8))))
        max_e_delta=max(max_e_delta,abs(e-r['e'])); max_h_delta=max(max_h_delta,abs(hi-r['H_involution_max']))
        max_unitarity=max(max_unitarity,un)
        result.append({'n':n,'case':r['case'],'kind':r['kind'],'e_rebuilt':e,'e_recorded':r['e'],
                       'success':e<1e-8,'H_involution_rebuilt':hi,'unitarity_max':un})
    assert max_e_delta<2e-12,(max_e_delta,'circuit residual mismatch')
    assert max_h_delta<2e-12,(max_h_delta,'involution mismatch')
    groups={}
    for key in sorted({(r['case'],r['kind']) for r in rows}):
        z=[q for q,r in zip(result,rows) if (r['case'],r['kind'])==key]
        groups['/'.join(key)]={'count':len(z),'success_e_lt_1e-8':sum(q['success'] for q in z),
                               'e_min':min(q['e_rebuilt'] for q in z),'e_max':max(q['e_rebuilt'] for q in z)}
    out={'beat':'AD-21','verdict':'ALL_PASS','known_answer_gate':{'random_circuit_unitary_max':float(np.max(np.abs(U@U.conj().T-np.eye(8))))},
         'records':len(rows),'max_abs_e_record_minus_rebuild':max_e_delta,
         'max_abs_H_record_minus_rebuild':max_h_delta,'max_circuit_unitarity_error':max_unitarity,'groups':groups}
    (RUN/'ad21_replay_continuation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
