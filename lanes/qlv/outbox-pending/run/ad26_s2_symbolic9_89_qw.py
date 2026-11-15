"""AD-26 S^2：[8,9] 9-CZ 全 S^2 的 Q(w) 稀疏多项式证书。

w=exp(i*pi/8), w^8=-1；所有常量属于 Q(w)，由 AD-23 的分数系数
精确域承担。矩阵元为 c,s,f,g 的稀疏多项式，逐层模去
s^2=1-c^2、g^2=1-f^2。恒等式判定完全不使用浮点容差。
"""
import hashlib
import importlib.util
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import ad26_s2_analytic9_89 as numeric89
from ad26_s2_prune import raw_indices

spec = importlib.util.spec_from_file_location("ad26_qw_field",R.parent.parent/"ad23/run/ad23_exact.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

EDGES = [(0,1),(0,1),(0,1),(0,1),(1,2),(0,1),(1,2),(0,1),(0,1)]
FROZEN_N = {1:1,3:6,4:0,6:4,7:0,8:13,10:0,11:3,12:5,13:4,14:12,
            15:4,16:2,17:2,18:0,19:4,20:7,21:0,22:7,23:1,24:3,25:7,
            26:4,27:4,28:15,29:0,30:10,31:3,32:0,34:0,35:2,36:14,
            39:8,40:0,41:6,42:9,43:10,44:0,45:15}
FREE_SPEC = {2:(-2,0,1),5:(2,1,0),9:(3,1,0),33:(-2,1,0),
             37:(-2,0,-1),38:(-2,-1,0)}
raw_to_core = {raw:j for j,raw in enumerate(raw_indices(EDGES))}


class P:
    __slots__ = ("d",)
    def __init__(self,d=None):
        self.d = {m:a for m,a in (d or {}).items() if a.a != ex.Z.a}
    def __add__(self,o):
        out = dict(self.d)
        for m,a in o.d.items():
            out[m] = out[m]+a if m in out else a
            if out[m].a == ex.Z.a: del out[m]
        return P(out)
    def __neg__(self):
        return P({m:-a for m,a in self.d.items()})
    def __sub__(self,o):
        return self+(-o)
    def __mul__(self,o):
        out = {}
        for m,a in self.d.items():
            for n,b in o.d.items():
                k = tuple(x+y for x,y in zip(m,n))
                out[k] = out[k]+a*b if k in out else a*b
        return P(out)
    def __rmul__(self,n):
        if isinstance(n,int): return self.scale_int(n)
        return NotImplemented
    def scale_field(self,a):
        return P({m:a*x for m,x in self.d.items()})
    def scale_int(self,n):
        return P({m:x.scale(Fraction(n)) for m,x in self.d.items()})
    def signature(self):
        return str(sorted((m,tuple(str(x) for x in a.a)) for m,a in self.d.items()))


Z = P()
ONE = P({(0,0,0,0):ex.ONE})
def mono(q):
    m = [0,0,0,0];m[q] = 1
    return P({tuple(m):ex.ONE})
C,S,F,G = (mono(q) for q in range(4))
IP = P({(0,0,0,0):ex.wpow(4)})


def ground(a):
    return P({(0,0,0,0):a})


def zeros(n,m=None):
    m = n if m is None else m
    return [[Z for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zeros(n)
    for i in range(n): out[i][i] = ONE
    return out


def matmul(A,B):
    assert len(A[0]) == len(B)
    out = zeros(len(A),len(B[0]))
    for i,row in enumerate(A):
        for k,a in enumerate(row):
            if not a.d: continue
            for j,b in enumerate(B[k]):
                if b.d: out[i][j] = out[i][j]+a*b
    return out


def kron(A,B):
    out = zeros(len(A)*len(B),len(A[0])*len(B[0]))
    for i in range(len(A)):
        for j in range(len(A[0])):
            if not A[i][j].d: continue
            for k in range(len(B)):
                for l in range(len(B[0])):
                    if B[k][l].d: out[i*len(B)+k][j*len(B[0])+l] = A[i][j]*B[k][l]
    return out


def kron3(A,B,D):
    return kron(kron(A,B),D)


def madd(A,B):
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def msub(A,B):
    return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mscale(a,A):
    return [[a*x for x in row] for row in A]


def reduce_poly(p):
    # 直接展开二项式：s^es=(1-c^2)^(es//2)*s^(es%2)，g 同理。
    out = Z
    for (ec,es,ef,eg),a in p.d.items():
        ns,ng = es//2,eg//2
        for k in range(ns+1):
            for l in range(ng+1):
                factor = (-1)**(k+l)*math.comb(ns,k)*math.comb(ng,l)
                mon = (ec+2*k,es%2,ef+2*l,eg%2)
                out = out+P({mon:a.scale(Fraction(factor))})
    return out


def reduce_matrix(A):
    return [[reduce_poly(x) for x in row] for row in A]


def const_ground_cs(n):
    # ex.ry(n) 的角为 n*pi/4；其矩阵元正是 cos/sin(n*pi/8)。
    co,si = ex.ry(n)[0][0],ex.ry(n)[1][0]
    return ground(co),ground(si)


def angle_spec(j):
    if j is None: return 0,0,0
    if j in FREE_SPEC: return FREE_SPEC[j]
    return FROZEN_N[j],0,0


def half_angle_poly(j):
    n,a,b = angle_spec(j)
    ca,sa = {-1:(C,-S),0:(ONE,Z),1:(C,S)}[a]
    cb,sb = {-1:(F,-G),0:(ONE,Z),1:(F,G)}[b]
    co,si = ca*cb-sa*sb,sa*cb+ca*sb
    cn,sn = const_ground_cs(n)
    return cn*co-sn*si,sn*co+cn*si


def symbolic_su2(layer,q):
    mats = []
    for comp in range(3):
        raw = 1+(layer*3+q)*3+comp
        j = raw_to_core.get(raw,None)
        co,si = half_angle_poly(j)
        if comp == 1:
            mat = [[co,-si],[si,co]]
        else:
            mat = [[co-IP*si,Z],[Z,co+IP*si]]
        mats.append(mat)
    return matmul(matmul(mats[0],mats[1]),mats[2])


def sym_cz(edge):
    a,b = edge
    out = zeros(8)
    for x in range(8):
        bits = [(x>>2)&1,(x>>1)&1,x&1]
        out[x][x] = -ONE if bits[a] and bits[b] else ONE
    return out


def toffoli_sym():
    out = zeros(8)
    for x in range(8):
        bits = [(x>>2)&1,(x>>1)&1,x&1]
        if bits[0] and bits[2]: bits[1] ^= 1
        out[(bits[0]<<2)|(bits[1]<<1)|bits[2]][x] = ONE
    return out


I2 = eye(2)
Z2 = [[ONE,Z],[Z,-ONE]]
X2 = [[Z,ONE],[ONE,Z]]
Y2 = [[Z,-IP],[IP,Z]]
PAULI = {"I":I2,"X":X2,"Y":Y2,"Z":Z2}


def pm(names):
    return kron3(PAULI[names[0]],PAULI[names[1]],PAULI[names[2]])


def build_full_sphere():
    phase = ground(ex.wpow(3))
    U = mscale(phase,kron3(symbolic_su2(9,0),symbolic_su2(9,1),symbolic_su2(9,2)))
    U = reduce_matrix(U)
    for j in range(8,-1,-1):
        L = kron3(symbolic_su2(j,0),symbolic_su2(j,1),symbolic_su2(j,2))
        U = reduce_matrix(matmul(matmul(U,sym_cz(EDGES[j])),L))
        print(json.dumps({"built_layer":j}),flush=True)
    co = (C*C-S*S)*(C*C-S*S)-(2*C*S)*(2*C*S)
    si = 4*C*S*(C*C-S*S)
    cp,spf = F*F-G*G,2*F*G
    half = ground(ex.ONE.scale(Fraction(1,2)))
    u,v = (ONE+co)*half,(co-ONE)*half
    w,z = si*cp*half,si*spf*half
    H = zeros(8)
    for coeff,names in [(u,"ZXZ"),(v,"ZIZ"),(w,"YIZ"),(w,"YXZ"),(z,"XIZ"),(z,"XXZ")]:
        H = madd(H,mscale(coeff,pm(names)))
    ca,sa = const_ground_cs(1)
    target = matmul(madd(mscale(ca,eye(8)),mscale(IP*sa,H)),toffoli_sym())
    return U,target,msub(U,target)


def poly_eval(p,values):
    out = 0j
    for mon,a in p.d.items():
        out += a.numeric()*values[0]**mon[0]*values[1]**mon[1]*values[2]**mon[2]*values[3]**mon[3]
    return out


def numeric_known_answer_gate(U,residual):
    theta,phi = np.pi/7,.31
    values = [np.cos(theta/4),np.sin(theta/4),np.cos(phi/2),np.sin(phi/2)]
    actual = np.asarray([[poly_eval(x,values) for x in row] for row in U])
    expected = numeric89.s2.target(theta,phi)
    error = float(np.max(abs(actual-expected)))
    direct = float(np.max(abs(numeric89.matrix(theta,phi)-expected)))
    assert error < 2e-12 and direct < 2e-12,(error,direct)
    nonzero = sum(bool(x.d) for row in residual for x in row)
    assert nonzero > 0
    return {"theta":theta,"phi":phi,"symbolic_matrix_numeric_max_abs":error,
            "independent_numeric_constructor_max_abs":direct,
            "nonzero_residual_entries_before_certificate":nonzero}


def main():
    start = time.time()
    field_gate = ex.known_answer_gate()
    U,target,residual = build_full_sphere()
    gate = numeric_known_answer_gate(U,residual)
    certificates = []
    for row in range(8):
        for col in range(8):
            expr = residual[row][col]
            if not expr.d: continue
            reduced = reduce_poly(expr)
            cert = {"entry":[row,col],
                    "raw_polynomial_sha256":hashlib.sha256(expr.signature().encode()).hexdigest(),
                    "reduced_term_count":len(reduced.d),"pass":not reduced.d}
            certificates.append(cert)
            print(json.dumps({"entry":[row,col],"pass":cert["pass"],
                              "terms":cert["reduced_term_count"],
                              "elapsed":time.time()-start}),flush=True)
    assert certificates and all(x["pass"] for x in certificates)
    cert_out = {"beat":"AD-26","status":"S2_9CZ_89_QW_ALL_ENTRIES_EXACT_PASS",
                "coefficient_field":"Q(w),w=exp(i*pi/8),w^8+1=0,Fraction coefficients",
                "relations":["c^2+s^2=1","f^2+g^2=1"],"entries":certificates}
    cert_raw = json.dumps(cert_out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_symbolic9_89_qw_entries.json").write_bytes(cert_raw)
    out = {"beat":"AD-26","status":"S2_9CZ_89_FULL_SPHERE_DIRECT_L1_EXACT_PASS",
           "evidence_level":"L1 exact Q(w)-coefficient polynomial full-matrix identity on the whole S^2",
           "topology":"89","cz_count":9,"edges":[list(e) for e in EDGES],
           "field_known_answer_gate":field_gate,"numeric_known_answer_gate":gate,
           "proof":{"method":"sparse polynomial matrices with exact Q(w) coefficients; reduce all residuals modulo two circle relations",
                    "nonzero_residual_entries":len(certificates),
                    "passed_entries":sum(x["pass"] for x in certificates),
                    "entries_file":"ad26_s2_symbolic9_89_qw_entries.json",
                    "entries_sha256":hashlib.sha256(cert_raw).hexdigest(),
                    "numerics_in_identity_decision":False},
           "numeric_companion":{"path":"ad26_s2_analytic9_89_summary.json",
                                "sha256":hashlib.sha256((R/"ad26_s2_analytic9_89_summary.json").read_bytes()).hexdigest(),
                                "points":241},
           "strict_conclusion":"整个 S^2 目标族存在同一 [8,9] 边序的9-CZ精确构造；所有角均为pi/4整数倍及theta/2、phi一次式。9-CZ不冒报为最优。",
           "boundary":"第二套精确模板不证明与[0,10]块级同族，不给出7/8-CZ或其他拓扑的不存在性。",
           "first_honesty_anomaly_note":"通用Sympy展开与复代数数域两条路线分别因表达式爆炸和转换开销超时；均非电路反例。本版以Q(w)稀疏精确算术完成判等。",
           "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
           "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw = json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_symbolic9_89_qw_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"entries":len(certificates),
                      "seconds":time.time()-start,
                      "entries_sha256":hashlib.sha256(cert_raw).hexdigest(),
                      "summary_sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
