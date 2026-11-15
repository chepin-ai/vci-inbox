"""AD-26 S^2 89d2d6 7-CZ独立重建；公式重录，不导入候选或证明器。"""
import hashlib,importlib.util,json,time
from pathlib import Path
import numpy as np
import ad26_s2_independent8_89d2 as low

R=Path(__file__).resolve().parent
EDGES=[(0,1),(0,1),(0,1),(1,2),(0,1),(1,2),(0,1)]
FROZEN_N={3:4,4:12,5:2,6:4,7:0,8:2,9:2,10:12,12:14,13:1,14:2,15:4,
          16:2,17:14,18:0,19:1,20:4,21:1,22:0,23:4,24:0,26:13,27:2,
          28:10,31:0,32:4,33:2,34:13,35:9,36:0,37:6}


def core(theta,phi):
    c=np.zeros(38)
    for j,n in FROZEN_N.items(): c[j]=n*np.pi/4
    c[0]=7*np.pi/8;c[1]=12*np.pi-theta/2;c[2]=-np.pi/2+phi;c[11]=-np.pi/2+theta/2
    c[25]=np.pi/2-theta/2;c[29]=-3*np.pi/2-phi;c[30]=np.pi/2+theta/2
    return c


def full7_raw(theta,phi):
    p=np.zeros(73);p[low.raw_indices(EDGES)]=core(theta,phi);return p


def exact_theta_zero(p):
    spec=importlib.util.spec_from_file_location("ad26_independent_7_exact_field",R.parent.parent/"ad23/run/ad23_exact.py")
    ex=importlib.util.module_from_spec(spec);spec.loader.exec_module(ex)
    angles=np.asarray(p[1:]).reshape(8,3,3);ints=np.rint(angles/(np.pi/4)).astype(int)
    snap=float(np.max(abs(ints*np.pi/4-angles)));nphase=int(np.rint(p[0]/(np.pi/8)))
    assert snap<2e-8 and nphase==7
    U=ex.circuit(nphase,ints.tolist(),EDGES);Zz=ex.diag2(ex.ONE,-ex.ONE)
    Xx=[[ex.Z,ex.ONE],[ex.ONE,ex.Z]];Ii=ex.eye(2)
    def exop(q,A):
        ms=[Ii,Ii,Ii];ms[q]=A;return ex.kron(ex.kron(ms[0],ms[1]),ms[2])
    H00=ex.mm(ex.mm(exop(0,Zz),exop(1,Xx)),exop(2,Zz));T=ex.toffoli({0,2},1)
    w,wm=ex.wpow(1),ex.wpow(-1);co,isi=(w+wm).scale(ex.F(1,2)),(w-wm).scale(ex.F(1,2))
    V=ex.mm([[co*a+isi*h for a,h in zip(ri,rh)] for ri,rh in zip(ex.eye(8),H00)],T)
    nz=ex.nonzero_entries(ex.md(U,V));bad=ints.tolist();bad[0][0][0]+=1
    nzb=ex.nonzero_entries(ex.md(ex.circuit(nphase,bad,EDGES),V));assert nz==0 and nzb!=0
    return {"field":"Q(w), w=exp(i*pi/8), w^8+1=0","exact_nonzero_residual_entries":nz,
            "negative_control":"first local angle +pi/4","negative_control_nonzero_entries":nzb,
            "max_integer_snap_rad":snap,"phase_pi_over_8":nphase}


def main():
    start=time.time();exact0=exact_theta_zero(full7_raw(0.,0.));records=[]
    for theta in np.linspace(0,np.pi,41):
        for phi in (-np.pi,-2.4,-.7,0.,.31,1.2,2.5,np.pi):
            e=float(np.max(abs(low.circuit(full7_raw(float(theta),float(phi)),EDGES)-low.target(float(theta),float(phi)))))
            records.append({"theta":float(theta),"phi":float(phi),"target_max_abs":e})
    assert all(r["target_max_abs"]<2e-12 for r in records)
    th,ph=.7,.4;bad=core(th,ph).copy();bad[1]+=np.pi/4;badp=np.zeros(73);badp[low.raw_indices(EDGES)]=bad
    negative=float(np.max(abs(low.circuit(badp,EDGES)-low.target(th,ph))));assert negative>1e-3
    path=R/"ad26_s2_symbolic7_89d2d6_qw_summary.json";symbolic=json.loads(path.read_text())
    assert symbolic["status"]=="S2_7CZ_89D2D6_FULL_SPHERE_DIRECT_L1_EXACT_PASS" and symbolic["proof"]["passed_entries"]==32
    out={"beat":"AD-26","status":"S2_7CZ_89D2D6_INDEPENDENT_REBUILD_PASS",
         "source_policy":"固定角与线性公式重录；未导入analytic7_89d2d6或符号证明器；复用独立8-CZ验收器的无状态电路/目标原语。",
         "theta_zero_exact":exact0,"numeric_points":len(records),"worst":max(records,key=lambda r:r["target_max_abs"]),
         "negative_control_max_abs":negative,
         "linked_symbolic_certificate":{"path":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                                        "status":symbolic["status"],"passed_entries":32},
         "evidence_level":"独立数值/精确端点重建；全参数L1由已链接Q(w)稀疏多项式证明器承担",
         "boundary":"独立重建不证明7-CZ最优，也不排除6-CZ或其他拓扑。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_independent7_89d2d6_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"points":len(records),"worst":out["worst"],"theta_zero_exact":exact0,
                      "negative_control_max_abs":negative,"seconds":time.time()-start,
                      "sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
