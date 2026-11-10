"""AD-23独立精确认验收：不导入构造器/分析器，以SymPy代数域从整数角重建。"""
import hashlib
import json
import time
from pathlib import Path
import sympy as sp

R=Path(__file__).resolve().parent
ZETA=sp.exp(sp.I*sp.pi/8)
K=sp.QQ.algebraic_field(ZETA)
ZERO,ONE=K.zero,K.one
W=K.from_sympy(ZETA)

def wp(n):return W**int(n%16)
def rz(n):return [[wp(-n),ZERO],[ZERO,wp(n)]]
def ry(n):
    c=K.from_sympy(sp.cos(int(n)*sp.pi/8));s=K.from_sympy(sp.sin(int(n)*sp.pi/8))
    return [[c,-s],[s,c]]
def mm(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),ZERO) for j in range(len(B[0]))] for i in range(len(A))]
def md(A,B):return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def kron(A,B):
    return [[A[i][j]*B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]
def eye(n):return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def su2(t):return mm(mm(rz(t[0]),ry(t[1])),rz(t[2]))
def layer(t):return kron(kron(su2(t[0]),su2(t[1])),su2(t[2]))
def cz(e):
    a,b=e;d=[-ONE if (((x>>(2-a))&1) and ((x>>(2-b))&1)) else ONE for x in range(8)]
    return [[d[i] if i==j else ZERO for j in range(8)] for i in range(8)]
def circuit(phase,angles,edges):
    U=layer(angles[-1])
    for j in range(len(edges)-1,-1,-1):U=mm(mm(U,cz(edges[j])),layer(angles[j]))
    return [[wp(phase)*U[i][j] for j in range(8)] for i in range(8)]
def perm(fn):
    A=[[ZERO]*8 for _ in range(8)]
    for x in range(8):A[fn(x)][x]=ONE
    return A
def bits(x):return [(x>>2)&1,(x>>1)&1,x&1]
def code(b):return (b[0]<<2)|(b[1]<<1)|b[2]
def cnot(c,t):
    def f(x):
        b=bits(x)
        if b[c]:b[t]^=1
        return code(b)
    return perm(f)
def toffoli(cs,t):
    def f(x):
        b=bits(x)
        if all(b[q] for q in cs):b[t]^=1
        return code(b)
    return perm(f)
MAJ=mm(mm(toffoli({0,2},1),cnot(1,2)),cnot(1,0))
def nz(A):return sum(A[i][j]!=ZERO for i in range(len(A)) for j in range(len(A[0])))
def dagger(A):
    return [[K.from_sympy(sp.conjugate(K.to_sympy(A[j][i]))) for j in range(len(A))] for i in range(len(A[0]))]
def known_gate():
    trig=0
    for n in range(-8,9):
        c=K.from_sympy(sp.cos(n*sp.pi/8));s=K.from_sympy(sp.sin(n*sp.pi/8))
        assert c*c+s*s==ONE;trig+=1
    A=layer([[1,2,3],[-2,1,4],[3,-1,2]]);C=cz((0,1));Ad=dagger(A)
    assert nz(md(mm(mm(Ad,mm(C,C)),A),eye(8)))==0
    wrong=mm(mm(A,C),mm(Ad,C));wrong_nz=nz(md(wrong,eye(8)));assert wrong_nz>0
    assert nz(md(mm(mm(MAJ,cnot(1,0)),cnot(1,2)),toffoli({0,2},1)))==0
    assert nz(md(mm(MAJ,MAJ),eye(8)))>0
    return {'trig_pythagorean_exact':trig,'ordered_identity':'exact zero','wrong_order_control_nonzero':wrong_nz,
            'maj_toffoli_identity':'exact zero','maj_non_involution':True}

def main():
    t=time.time();src=json.loads((R/'ad23_maj_7cz_exact.json').read_text());rows=[]
    for h in src['hits']:
        U=circuit(h['phase_pi_over_8'],h['local_angles_pi_over_4'],h['edges']);D=md(U,MAJ);n=nz(D)
        assert n==0,(h['idx'],h['restart'],n)
        # 38坐标的规范形状独立检查：前7层首角0，各层空闲位全零。
        edges=h['edges'];angles=h['local_angles_pi_over_4'];shape=True
        for i,(a,b) in enumerate(edges):
            idle=({0,1,2}-{a,b}).pop()
            shape &= all(angles[i][q][0]==0 for q in (a,b)) and angles[i][idle]==[0,0,0]
        assert shape,(h['idx'],h['restart'])
        rows.append({'idx':h['idx'],'restart':h['restart'],'exact_nonzero_residual_entries':n,'canonical_shape':shape})
    raw=(R/'ad23_maj_7cz_exact.json').read_bytes()
    out={'beat':'AD-23','status':'INDEPENDENT_ALL_EXACT_ZERO','engine':'SymPy QQ.algebraic_field(exp(I*pi/8))',
         'known_answer_gate':known_gate(),'hits':rows,'input_sha256':hashlib.sha256(raw).hexdigest(),
         'seconds':time.time()-t,'private_ci_consumption':0,'quantum_machine_consumption':0,
         'boundary':'独立精确零只证明所给7-CZ整数电路实现MAJ；不推出k<=6不存在。'}
    (R/'ad23_exact_verify.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
