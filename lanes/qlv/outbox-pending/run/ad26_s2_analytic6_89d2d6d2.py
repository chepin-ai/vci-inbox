"""AD-26 S^2：89d2d6d2边序的6-CZ全参数线性角解析候选。"""
import hashlib,json,time
from pathlib import Path
import numpy as np
import ad26_s2_analytic8_89d2 as low

R=Path(__file__).resolve().parent;base,s2,expand=low.base,low.s2,low.expand
EDGES=[(0,1),(0,1),(1,2),(0,1),(1,2),(0,1)]
FROZEN_N={1:2,3:15,4:14,5:2,8:4,9:1,10:14,11:4,12:6,13:2,14:14,15:1,
          16:4,17:1,18:0,19:4,20:10,22:13,23:2,24:10,27:0,28:4,29:2,
          30:2,31:1,32:0,33:4}
FREE=[0,2,6,7,21,25,26]
K=6;TOPOLOGY="89d2d6d2";PHASE_W=5
FREE_SPEC={2:(4,0,1),6:(0,1,0),7:(14,1,0),21:(2,-1,0),25:(10,0,-1),26:(2,1,0)}


def core(theta,phi):
    c=np.zeros(34)
    for j,n in FROZEN_N.items(): c[j]=n*np.pi/4
    c[0]=5*np.pi/8;c[2]=np.pi+phi;c[6]=theta/2;c[7]=-np.pi/2+theta/2
    c[21]=np.pi/2-theta/2;c[25]=-3*np.pi/2-phi;c[26]=np.pi/2+theta/2
    return c


def matrix(theta,phi): return base.circuit(expand(core(theta,phi),EDGES),EDGES)


def main():
    start=time.time();rr=[json.loads(x) for x in (R/"ad26_s2_7to6.jsonl").read_text().splitlines() if x.strip()]
    src=next(r for r in rr if r["topology"]=="89d2d6" and r["deleted"]==[2] and r["kick"]==.02)
    assert [tuple(e) for e in src["edges"]]==EDGES;th,ph=np.pi/7,.31
    source_e=float(np.max(abs(base.circuit(expand(np.asarray(src["x_core"]),EDGES),EDGES)-s2.target(th,ph))))
    candidate_e=float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
    bad=core(th,ph).copy();bad[1]+=np.pi/4
    bad_e=float(np.max(abs(base.circuit(expand(bad,EDGES),EDGES)-s2.target(th,ph))))
    assert source_e<2e-12 and candidate_e<2e-12 and bad_e>1e-3
    grid=[json.loads(x) for x in (R/"ad26_s2_gauge_reduced_89d2d6d2_grid.jsonl").read_text().splitlines() if x.strip()]
    records=[]
    for row in grid:
        th,ph=row["theta"],row["phi"];e=float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
        records.append({"class":"original_5x5_grid","theta":th,"phi":ph,"target_max_abs":e})
    assert len(records)==25 and all(r["target_max_abs"]<2e-12 for r in records)
    rng=np.random.default_rng(26111662)
    points=[(float(t),float(p)) for t,p in zip(rng.uniform(0,np.pi,160),rng.uniform(-np.pi,np.pi,160))]
    points += [(t,p) for t in (0.,1e-10,.013,.77,1.9,np.pi-1e-10,np.pi)
               for p in (-np.pi,-2.4,-np.pi/4,0.,.31,np.pi/4,2.5,np.pi)]
    for th,ph in points:
        e=float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
        records.append({"class":"off_grid_and_poles","theta":th,"phi":ph,"target_max_abs":e})
    assert all(r["target_max_abs"]<2e-12 for r in records);worst=max(records,key=lambda r:r["target_max_abs"])
    out={"beat":"AD-26","status":"S2_6CZ_89D2D6D2_LINEAR_ANGLE_ANALYTIC_CANDIDATE_NUMERIC_PASS",
         "topology":"89d2d6d2","cz_count":6,"edges":[list(e) for e in EDGES],
         "known_answer_gate":{"source_raw6_max_abs":source_e,"candidate_at_source_max_abs":candidate_e,
                              "negative_control":"core1 += pi/4","negative_control_max_abs":bad_e},
         "angle_recipe":{"frozen_pi_over_4":FROZEN_N,"free_formulas":{"0":"5*pi/8 (global phase)",
             "2":"pi+phi","6":"theta/2","7":"-pi/2+theta/2","21":"pi/2-theta/2",
             "25":"-3*pi/2-phi","26":"pi/2+theta/2"}},
         "original_grid":{"points":25,"worst_max_abs":max(r["target_max_abs"] for r in records[:25])},
         "off_grid":{"points":len(points),"random_points":160,"pole_and_special_points":56,
                     "worst_max_abs":max(r["target_max_abs"] for r in records[25:])},"worst":worst,
         "evidence_level":"L2 complete explicit linear-angle candidate; exact symbolic certificate required for L1",
         "boundary":"数值命中不代替全参数恒等式；本结果不证明6-CZ最优，也不排除5-CZ或其他6-CZ拓扑。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    (R/"ad26_s2_analytic6_89d2d6d2_points.jsonl").write_text("".join(json.dumps(r,separators=(",",":"))+"\n" for r in records))
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_analytic6_89d2d6d2_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"points":len(records),"worst":worst,"negative_control_max_abs":bad_e,
                      "seconds":time.time()-start,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
