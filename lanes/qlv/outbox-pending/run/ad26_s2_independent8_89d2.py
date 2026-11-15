"""AD-26 S^2 89d2 8-CZ 独立重建验收；不导入候选或符号证明器。"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent
EDGES = [(0,1),(0,1),(0,1),(1,2),(0,1),(1,2),(0,1),(0,1)]
FROZEN_N = {1:0,2:14,3:2,4:12,7:0,8:0,10:12,11:0,12:12,13:2,14:6,
            15:4,16:0,17:0,18:0,19:1,20:2,21:1,22:0,23:4,24:0,25:0,
            26:13,27:1,28:12,30:14,31:2,32:14,35:0,36:4,37:2,38:13,
            39:2,40:0,41:15}
I2=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
PAULI={"I":I2,"X":X,"Y":Y,"Z":Z}


def rz(a): return np.diag([np.exp(-.5j*a),np.exp(.5j*a)])
def ry(a): return np.array([[np.cos(a/2),-np.sin(a/2)],[np.sin(a/2),np.cos(a/2)]],complex)
def su2(a): return rz(a[0])@ry(a[1])@rz(a[2])


def cz(edge):
    a,b=edge;d=np.ones(8,complex)
    for x in range(8):
        bits=[(x>>2)&1,(x>>1)&1,x&1]
        if bits[a] and bits[b]: d[x]=-1
    return np.diag(d)


def circuit(p,edges):
    a=np.asarray(p[1:]).reshape(len(edges)+1,3,3)
    U=np.exp(1j*p[0])*np.kron(np.kron(su2(a[-1,0]),su2(a[-1,1])),su2(a[-1,2]))
    for j in range(len(edges)-1,-1,-1):
        L=np.kron(np.kron(su2(a[j,0]),su2(a[j,1])),su2(a[j,2]))
        U=U@cz(edges[j])@L
    return U


def toffoli():
    T=np.zeros((8,8),complex)
    for x in range(8):
        b=[(x>>2)&1,(x>>1)&1,x&1]
        if b[0] and b[2]: b[1]^=1
        T[(b[0]<<2)|(b[1]<<1)|b[2],x]=1
    return T


def pm(names): return np.kron(np.kron(PAULI[names[0]],PAULI[names[1]]),PAULI[names[2]])


def target(theta,phi):
    u,v=(1+np.cos(theta))/2,(np.cos(theta)-1)/2
    w,t=np.sin(theta)*np.cos(phi)/2,np.sin(theta)*np.sin(phi)/2
    H=u*pm("ZXZ")+v*pm("ZIZ")+w*(pm("YIZ")+pm("YXZ"))+t*(pm("XIZ")+pm("XXZ"))
    return (np.cos(np.pi/8)*np.eye(8)+1j*np.sin(np.pi/8)*H)@toffoli()


def raw_indices(edges):
    ix=[0]
    for i,(a,b) in enumerate(edges):
        for q in (a,b): ix.extend([1+(i*3+q)*3+1,1+(i*3+q)*3+2])
    ix.extend(range(1+9*len(edges),1+9*(len(edges)+1)))
    assert len(ix)==4*len(edges)+10
    return ix


def core(theta,phi):
    c=np.zeros(42)
    for j,n in FROZEN_N.items(): c[j]=n*np.pi/4
    c[0]=5*np.pi/8;c[5]=np.pi/2+theta/2;c[6]=np.pi+phi
    c[9]=np.pi/2-theta/2;c[29]=np.pi/2-theta/2
    c[33]=-3*np.pi/2-phi;c[34]=np.pi/2+theta/2
    return c


def full8_raw(theta,phi):
    p=np.zeros(82);p[raw_indices(EDGES)]=core(theta,phi)
    return p


def exact_theta_zero(p):
    spec=importlib.util.spec_from_file_location("ad26_independent_89d2_exact_field",R.parent.parent/"ad23/run/ad23_exact.py")
    ex=importlib.util.module_from_spec(spec);spec.loader.exec_module(ex)
    angles=np.asarray(p[1:]).reshape(9,3,3);ints=np.rint(angles/(np.pi/4)).astype(int)
    snap=float(np.max(abs(ints*np.pi/4-angles)));nphase=int(np.rint(p[0]/(np.pi/8)))
    assert snap<2e-8 and nphase==5
    U=ex.circuit(nphase,ints.tolist(),EDGES)
    Zz=ex.diag2(ex.ONE,-ex.ONE);Xx=[[ex.Z,ex.ONE],[ex.ONE,ex.Z]];Ii=ex.eye(2)
    def exop(q,A):
        ms=[Ii,Ii,Ii];ms[q]=A
        return ex.kron(ex.kron(ms[0],ms[1]),ms[2])
    H00=ex.mm(ex.mm(exop(0,Zz),exop(1,Xx)),exop(2,Zz));T=ex.toffoli({0,2},1)
    w,wm=ex.wpow(1),ex.wpow(-1)
    co,isi=(w+wm).scale(ex.F(1,2)),(w-wm).scale(ex.F(1,2))
    V=ex.mm([[co*a+isi*h for a,h in zip(ri,rh)] for ri,rh in zip(ex.eye(8),H00)],T)
    nz=ex.nonzero_entries(ex.md(U,V));bad=ints.tolist();bad[0][0][0]+=1
    nzb=ex.nonzero_entries(ex.md(ex.circuit(nphase,bad,EDGES),V))
    assert nz==0 and nzb!=0
    return {"field":"Q(w), w=exp(i*pi/8), w^8+1=0","exact_nonzero_residual_entries":nz,
            "negative_control":"first local angle +pi/4","negative_control_nonzero_entries":nzb,
            "max_integer_snap_rad":snap,"phase_pi_over_8":nphase}


def main():
    start=time.time();exact0=exact_theta_zero(full8_raw(0.,0.));records=[]
    for theta in np.linspace(0,np.pi,41):
        for phi in (-np.pi,-2.4,-.7,0.,.31,1.2,2.5,np.pi):
            e=float(np.max(abs(circuit(full8_raw(float(theta),float(phi)),EDGES)-target(float(theta),float(phi)))))
            records.append({"theta":float(theta),"phi":float(phi),"target_max_abs":e})
    assert all(r["target_max_abs"]<2e-12 for r in records)
    th,ph=.7,.4;bad=core(th,ph).copy();bad[1]+=np.pi/4
    badp=np.zeros(82);badp[raw_indices(EDGES)]=bad
    negative=float(np.max(abs(circuit(badp,EDGES)-target(th,ph))));assert negative>1e-3
    path=R/"ad26_s2_symbolic8_89d2_qw_summary.json";symbolic=json.loads(path.read_text())
    assert symbolic["status"]=="S2_8CZ_89D2_FULL_SPHERE_DIRECT_L1_EXACT_PASS" and symbolic["proof"]["passed_entries"]==32
    out={"beat":"AD-26","status":"S2_8CZ_89D2_INDEPENDENT_REBUILD_PASS",
         "source_policy":"固定角与线性公式在本文件重复录入；未导入analytic8_89d2或符号证明器；目标和电路独立重建。",
         "theta_zero_exact":exact0,"numeric_points":len(records),"worst":max(records,key=lambda r:r["target_max_abs"]),
         "negative_control_max_abs":negative,
         "linked_symbolic_certificate":{"path":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                                        "status":symbolic["status"],"passed_entries":32},
         "evidence_level":"独立数值/精确端点重建；全参数L1由已链接Q(w)稀疏多项式证明器承担",
         "boundary":"独立重建不证明8-CZ最优，也不排除7-CZ或其他拓扑。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_independent8_89d2_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"points":len(records),"worst":out["worst"],
                      "theta_zero_exact":exact0,"negative_control_max_abs":negative,
                      "seconds":time.time()-start,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
