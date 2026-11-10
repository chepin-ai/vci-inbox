"""AD-23 MAJ 7-CZ 精确证书：Q(ζ16) 全128实残差等价精确零。

w=exp(iπ/8)，w^8=-1。元素以 Fraction 系数表示在 1,w,...,w^7 上，
乘法后严格约化 w^8=-1。局部角均为 nπ/4，整体相位为 mπ/8：
  Rz(nπ/4)=diag(w^-n,w^n),
  Ry(nπ/4)=[[cos(nπ/8),-sin(nπ/8)],[sin(nπ/8),cos(nπ/8)]].
因此全部矩阵元属于Q(w)。最终不做浮点容差判零，逐矩阵元断言精确零。
"""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import numpy as np

R=Path(__file__).resolve().parent
F=Fraction

class C:
    __slots__=('a',)
    def __init__(self,a=()):
        z=[F(x) for x in a]+[F(0)]*(8-len(a));self.a=tuple(z[:8])
    def __add__(self,o): return C([x+y for x,y in zip(self.a,o.a)])
    def __neg__(self): return C([-x for x in self.a])
    def __sub__(self,o): return self+(-o)
    def __mul__(self,o):
        t=[F(0)]*15
        for i,x in enumerate(self.a):
            if x:
                for j,y in enumerate(o.a):
                    if y:t[i+j]+=x*y
        z=t[:8]
        for k in range(8,15):z[k-8]-=t[k]  # w^8=-1
        return C(z)
    def scale(self,s):return C([F(s)*x for x in self.a])
    def conj(self):
        # w -> w^-1，严格域自同构。
        out=Z
        for r,x in enumerate(self.a):
            if x:out=out+wpow(-r).scale(x)
        return out
    def numeric(self):
        return sum(float(x)*np.exp(1j*np.pi*r/8) for r,x in enumerate(self.a))
    def __repr__(self):return f'C({self.a})'
Z=C();ONE=C([1])
def wpow(n):
    n%=16
    if n<8:return C([1 if i==n else 0 for i in range(8)])
    return -C([1 if i==n-8 else 0 for i in range(8)])
def cispow(n):return wpow(n)
def rz(n):return diag2(wpow(-n),wpow(n))
def ry(n):
    co=(wpow(n)+wpow(-n)).scale(F(1,2))
    si=(wpow(n)-wpow(-n))*wpow(4).scale(F(-1,2))
    return [[co,-si],[si,co]]
def diag2(a,b):return [[a,Z],[Z,b]]
def mm(A,B):
    assert len(A[0])==len(B)
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Z) for j in range(len(B[0]))] for i in range(len(A))]
def md(A,B):return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def kron(A,B):
    return [[A[i][j]*B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]
def eye(n):return [[ONE if i==j else Z for j in range(n)] for i in range(n)]
def dagger(A):return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A[0]))]
def su2(t):return mm(mm(rz(int(t[0])),ry(int(t[1]))),rz(int(t[2])))
def layer(t):return kron(kron(su2(t[0]),su2(t[1])),su2(t[2]))
def cz(edge):
    a,b=edge;d=[]
    for x in range(8):
        neg=((x>>(2-a))&1) and ((x>>(2-b))&1);d.append(-ONE if neg else ONE)
    return [[d[i] if i==j else Z for j in range(8)] for i in range(8)]
def circuit(phase_n,angles,edges):
    k=len(edges);assert len(angles)==k+1
    U=layer(angles[-1])
    for j in range(k-1,-1,-1):U=mm(mm(U,cz(edges[j])),layer(angles[j]))
    return [[wpow(phase_n)*U[i][j] for j in range(8)] for i in range(8)]
def permutation(fn):
    A=[[Z]*8 for _ in range(8)]
    for x in range(8):A[fn(x)][x]=ONE
    return A
def bits(x):return [(x>>2)&1,(x>>1)&1,x&1]
def code(b):return (b[0]<<2)|(b[1]<<1)|b[2]
def cnot(c,t):
    def fn(x):
        b=bits(x)
        if b[c]:b[t]^=1
        return code(b)
    return permutation(fn)
def toffoli(controls,target):
    def fn(x):
        b=bits(x)
        if all(b[q] for q in controls):b[target]^=1
        return code(b)
    return permutation(fn)
MAJ=mm(mm(toffoli({0,2},1),cnot(1,2)),cnot(1,0))
def exact_zero(A):return all(x.a==Z.a for row in A for x in row)
def nonzero_entries(A):return sum(x.a!=Z.a for row in A for x in row)
def max_numeric(A):return max(abs(x.numeric()) for row in A for x in row)

def integerize(x):
    x=np.asarray(x,float);local=np.rint(x[1:]/(np.pi/4)).astype(int);phase=int(np.rint(x[0]/(np.pi/8)))
    assert np.max(np.abs(local*(np.pi/4)-x[1:]))<1e-10
    assert abs(phase*(np.pi/8)-x[0])<1e-10
    return phase,local.reshape(-1,3,3).tolist(),float(np.max(np.abs(local*(np.pi/4)-x[1:])))
def known_answer_gate():
    # 域公理、共轭和已知数值交叉检查。
    assert exact_zero([[wpow(8)+ONE]]) and wpow(16).a==ONE.a
    cross=0.
    for n in range(-17,18):
        for name,A,fn in [('rz',rz(n),lambda:np.diag([np.exp(-1j*n*np.pi/8),np.exp(1j*n*np.pi/8)])),
                          ('ry',ry(n),lambda:np.array([[np.cos(n*np.pi/8),-np.sin(n*np.pi/8)],[np.sin(n*np.pi/8),np.cos(n*np.pi/8)]]))]:
            B=fn();cross=max(cross,max(abs(A[i][j].numeric()-B[i,j]) for i in range(2) for j in range(2)))
            assert exact_zero(md(mm(A,dagger(A)),eye(2))),(name,n)
    assert cross<2e-14,cross
    # 反序陷阱已知答案：A† CZ CZ A=I；穿插为A CZ A† CZ一般不成立。
    A=layer([[[1,2,3],[-2,1,4],[3,-1,2]]][0]);CZ=cz((0,1))
    ident=mm(mm(dagger(A),mm(CZ,CZ)),A)
    assert exact_zero(md(ident,eye(8)))
    wrong=mm(mm(A,CZ),mm(dagger(A),CZ));assert not exact_zero(md(wrong,eye(8)))
    # MAJ解析恒等式及非对合边界。
    identity=md(mm(mm(MAJ,cnot(1,0)),cnot(1,2)),toffoli({0,2},1))
    assert exact_zero(identity)
    maj2=mm(MAJ,MAJ);non_involution=nonzero_entries(md(maj2,eye(8)))
    assert non_involution>0
    return {'field_relation':'w^8+1=0 exact','rz_ry_cases':35,'rz_ry_unitarity':'exact zero',
            'numeric_crosscheck_max':cross,'ordered_identity':'A^dagger CZ CZ A = I exact',
            'wrong_order_control_nonzero':nonzero_entries(md(wrong,eye(8))),
            'maj_toffoli_identity':'exact zero','maj_squared_nonidentity_entries':non_involution}

def main():
    gate=known_answer_gate();src=json.loads((R/'ad23_gauge.json').read_text())
    out={'beat':'AD-23','status':'ALL_EXACT_ZERO','evidence':'L1 exact arithmetic; not numerical interval certification',
         'field':'Q(w), w=exp(i*pi/8), w^8+1=0, Fraction coefficients',
         'known_answer_gate':gate,'strict_interval':'4 <= k <= 7','hits':[]}
    for h in src['hits']:
        phase,angles,delta=integerize(h['x_canonical']);U=circuit(phase,angles,h['edges']);D=md(U,MAJ)
        nz=nonzero_entries(D);assert nz==0,(h['idx'],h['restart'],nz,max_numeric(D))
        out['hits'].append({'idx':h['idx'],'restart':h['restart'],'edges':h['edges'],
                            'phase_pi_over_8':phase,'local_angles_pi_over_4':angles,
                            'source_canonical_x':h['x_canonical'],'max_source_snap_delta_rad':delta,
                            'exact_nonzero_residual_entries':nz,'exact_full_residual':'0',
                            'numeric_max_abs_for_display':max_numeric(D)})
    out['boundary']='7个不同来源数值解经35维通用规范压缩后均给出严格7-CZ构造；上界7升为L1。k=4,5,6不存在仍未证，严格区间保持4<=k<=7。'
    raw=json.dumps(out,indent=2,ensure_ascii=False).encode()+b'\n';(R/'ad23_maj_7cz_exact.json').write_bytes(raw)
    print(json.dumps({'status':out['status'],'hits':len(out['hits']),
                      'all_full_residuals_exact_zero':all(h['exact_nonzero_residual_entries']==0 for h in out['hits']),
                      'known_answer_gate':gate,'sha256':hashlib.sha256(raw).hexdigest()},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
