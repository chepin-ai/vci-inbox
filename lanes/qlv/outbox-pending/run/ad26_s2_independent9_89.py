"""AD-26 S^2 [8,9] 9-CZ 独立重建验收。

固定角与线性公式在本文件重复录入；不导入解析候选或任一符号证明器。
目标和电路独立重建；theta=0 使用 Q(w) 精确矩阵并设改角反例门。
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent
EDGES = [(0,1),(0,1),(0,1),(0,1),(1,2),(0,1),(1,2),(0,1),(0,1)]
FROZEN_N = {1:1,3:6,4:0,6:4,7:0,8:13,10:0,11:3,12:5,13:4,14:12,
            15:4,16:2,17:2,18:0,19:4,20:7,21:0,22:7,23:1,24:3,25:7,
            26:4,27:4,28:15,29:0,30:10,31:3,32:0,34:0,35:2,36:14,
            39:8,40:0,41:6,42:9,43:10,44:0,45:15}
I2 = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],complex)
Y = np.array([[0,-1j],[1j,0]],complex)
Z = np.diag([1,-1]).astype(complex)
PAULI = {"I":I2,"X":X,"Y":Y,"Z":Z}


def rz(a):
    return np.diag([np.exp(-.5j*a),np.exp(.5j*a)])


def ry(a):
    return np.array([[np.cos(a/2),-np.sin(a/2)],[np.sin(a/2),np.cos(a/2)]],complex)


def su2(a):
    return rz(a[0])@ry(a[1])@rz(a[2])


def cz(edge):
    a,b = edge
    d = np.ones(8,complex)
    for x in range(8):
        bits = [(x>>2)&1,(x>>1)&1,x&1]
        if bits[a] and bits[b]: d[x] = -1
    return np.diag(d)


def circuit(p,edges):
    a = np.asarray(p[1:]).reshape(len(edges)+1,3,3)
    U = np.exp(1j*p[0])*np.kron(np.kron(su2(a[-1,0]),su2(a[-1,1])),su2(a[-1,2]))
    for j in range(len(edges)-1,-1,-1):
        L = np.kron(np.kron(su2(a[j,0]),su2(a[j,1])),su2(a[j,2]))
        U = U@cz(edges[j])@L
    return U


def toffoli():
    T = np.zeros((8,8),complex)
    for x in range(8):
        b = [(x>>2)&1,(x>>1)&1,x&1]
        if b[0] and b[2]: b[1] ^= 1
        T[(b[0]<<2)|(b[1]<<1)|b[2],x] = 1
    return T


def pm(names):
    return np.kron(np.kron(PAULI[names[0]],PAULI[names[1]]),PAULI[names[2]])


def target(theta,phi):
    u,v = (1+np.cos(theta))/2,(np.cos(theta)-1)/2
    w,t = np.sin(theta)*np.cos(phi)/2,np.sin(theta)*np.sin(phi)/2
    H = (u*pm("ZXZ")+v*pm("ZIZ")+w*(pm("YIZ")+pm("YXZ"))+
         t*(pm("XIZ")+pm("XXZ")))
    return (np.cos(np.pi/8)*np.eye(8)+1j*np.sin(np.pi/8)*H)@toffoli()


def raw_indices(edges):
    ix = [0]
    for i,(a,b) in enumerate(edges):
        for q in (a,b):
            ix.extend([1+(i*3+q)*3+1,1+(i*3+q)*3+2])
    ix.extend(range(1+9*len(edges),1+9*(len(edges)+1)))
    assert len(ix)==4*len(edges)+10
    return ix


def core(theta,phi):
    c = np.zeros(46)
    for j,n in FROZEN_N.items(): c[j] = n*np.pi/4
    c[0] = 3*np.pi/8
    c[2] = -np.pi/2+phi
    c[5] = np.pi/2+theta/2
    c[9] = 3*np.pi/4+theta/2
    c[33] = -np.pi/2+theta/2
    c[37] = -np.pi/2-phi
    c[38] = -np.pi/2-theta/2
    return c


def full9_raw(theta,phi):
    p = np.zeros(91)
    p[raw_indices(EDGES)] = core(theta,phi)
    return p


def exact_theta_zero(p):
    ex_path = R.parent.parent/"ad23/run/ad23_exact.py"
    spec = importlib.util.spec_from_file_location("ad26_independent_89_exact_field",ex_path)
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    angles = np.asarray(p[1:]).reshape(10,3,3)
    ints = np.rint(angles/(np.pi/4)).astype(int)
    snap = float(np.max(abs(ints*np.pi/4-angles)))
    nphase = int(np.rint(p[0]/(np.pi/8)))
    assert snap<2e-8 and nphase==3
    U = ex.circuit(nphase,ints.tolist(),EDGES)
    Zz = ex.diag2(ex.ONE,-ex.ONE)
    Xx = [[ex.Z,ex.ONE],[ex.ONE,ex.Z]]
    Ii = ex.eye(2)
    def exop(q,A):
        ms = [Ii,Ii,Ii];ms[q] = A
        return ex.kron(ex.kron(ms[0],ms[1]),ms[2])
    H00 = ex.mm(ex.mm(exop(0,Zz),exop(1,Xx)),exop(2,Zz))
    T = ex.toffoli({0,2},1)
    w,wm = ex.wpow(1),ex.wpow(-1)
    co,isi = (w+wm).scale(ex.F(1,2)),(w-wm).scale(ex.F(1,2))
    V = ex.mm([[co*a+isi*h for a,h in zip(ri,rh)] for ri,rh in zip(ex.eye(8),H00)],T)
    nz = ex.nonzero_entries(ex.md(U,V))
    bad = ints.tolist();bad[0][0][0] += 1
    Ub = ex.circuit(nphase,bad,EDGES)
    nzb = ex.nonzero_entries(ex.md(Ub,V))
    assert nz==0 and nzb!=0
    return {"field":"Q(w), w=exp(i*pi/8), w^8+1=0","exact_nonzero_residual_entries":nz,
            "negative_control":"first local angle +pi/4","negative_control_nonzero_entries":nzb,
            "max_integer_snap_rad":snap,"phase_pi_over_8":nphase}


def main():
    start = time.time()
    exact0 = exact_theta_zero(full9_raw(0.,0.))
    records = []
    for theta in np.linspace(0,np.pi,41):
        for phi in (-np.pi,-2.4,-.7,0.,.31,1.2,2.5,np.pi):
            U = circuit(full9_raw(float(theta),float(phi)),EDGES)
            e = float(np.max(abs(U-target(float(theta),float(phi)))))
            records.append({"theta":float(theta),"phi":float(phi),"target_max_abs":e})
    assert all(r["target_max_abs"]<2e-12 for r in records)
    th,ph = .7,.4
    bad = core(th,ph).copy();bad[1] += np.pi/4
    badp = np.zeros(91);badp[raw_indices(EDGES)] = bad
    negative = float(np.max(abs(circuit(badp,EDGES)-target(th,ph))))
    assert negative>1e-3
    symbolic_path = R/"ad26_s2_symbolic9_89_qw_summary.json"
    symbolic = json.loads(symbolic_path.read_text())
    assert symbolic["status"]=="S2_9CZ_89_FULL_SPHERE_DIRECT_L1_EXACT_PASS"
    assert symbolic["proof"]["passed_entries"]==32
    out = {"beat":"AD-26","status":"S2_9CZ_89_INDEPENDENT_REBUILD_PASS",
           "source_policy":"固定角与线性公式在本文件重复录入；未导入analytic9_89或符号证明器；目标和电路独立重建。",
           "theta_zero_exact":exact0,"numeric_points":len(records),
           "worst":max(records,key=lambda r:r["target_max_abs"]),
           "negative_control_max_abs":negative,
           "linked_symbolic_certificate":{"path":symbolic_path.name,
                "sha256":hashlib.sha256(symbolic_path.read_bytes()).hexdigest(),
                "status":symbolic["status"],"passed_entries":32},
           "evidence_level":"独立数值/精确端点重建；全参数L1由已链接的Q(w)稀疏多项式证明器承担",
           "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
           "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw = json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_independent9_89_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"points":len(records),"worst":out["worst"],
                      "theta_zero_exact":exact0,"negative_control_max_abs":negative,
                      "seconds":time.time()-start,"sha256":hashlib.sha256(raw).hexdigest()},
                     ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
