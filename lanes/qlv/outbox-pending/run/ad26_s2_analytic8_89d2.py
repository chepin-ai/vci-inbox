"""AD-26 S^2：89d2 边序的 8-CZ 全参数线性角解析候选。"""
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent.parent/"ad22/run"))
import ad22_verify as base
sys.path.insert(0, str(R.parent.parent/"ad25/run"))
import ad25_s2_meridian as s2
sys.path.insert(0, str(R))
from ad26_s2_prune import expand

EDGES = [(0,1),(0,1),(0,1),(1,2),(0,1),(1,2),(0,1),(0,1)]
FROZEN_N = {1:0,2:14,3:2,4:12,7:0,8:0,10:12,11:0,12:12,13:2,14:6,
            15:4,16:0,17:0,18:0,19:1,20:2,21:1,22:0,23:4,24:0,25:0,
            26:13,27:1,28:12,30:14,31:2,32:14,35:0,36:4,37:2,38:13,
            39:2,40:0,41:15}
FREE = [0,5,6,9,29,33,34]


def core(theta, phi):
    c = np.zeros(42, dtype=float)
    for j,n in FROZEN_N.items():
        c[j] = n*np.pi/4
    c[0] = 5*np.pi/8
    c[5] = np.pi/2+theta/2
    c[6] = np.pi+phi
    c[9] = np.pi/2-theta/2
    c[29] = np.pi/2-theta/2
    c[33] = -3*np.pi/2-phi
    c[34] = np.pi/2+theta/2
    return c


def matrix(theta, phi):
    return base.circuit(expand(core(theta,phi),EDGES),EDGES)


def main():
    start = time.time()
    rows9 = [json.loads(x) for x in (R/"ad26_s2_9to8.jsonl").read_text().splitlines() if x.strip()]
    src = next(r for r in rows9 if r["topology"] == "89" and r["deleted"] == [2] and r["kick"] == 0.02)
    assert [tuple(e) for e in src["edges"]] == EDGES
    th,ph = np.pi/7,.31
    source_e = float(np.max(abs(base.circuit(expand(np.asarray(src["x_core"]),EDGES),EDGES)-s2.target(th,ph))))
    candidate_e = float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
    bad = core(th,ph).copy()
    bad[1] += np.pi/4
    bad_e = float(np.max(abs(base.circuit(expand(bad,EDGES),EDGES)-s2.target(th,ph))))
    assert source_e < 2e-12 and candidate_e < 2e-12 and bad_e > 1e-3
    grid = [json.loads(x) for x in (R/"ad26_s2_gauge_reduced_89d2_grid.jsonl").read_text().splitlines() if x.strip()]
    records = []
    for row in grid:
        th,ph = row["theta"],row["phi"]
        e = float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
        records.append({"class":"original_5x5_grid","theta":th,"phi":ph,"target_max_abs":e})
    assert len(records) == 25 and all(r["target_max_abs"] < 2e-12 for r in records)
    rng = np.random.default_rng(261116892)
    points = [(float(t),float(p)) for t,p in zip(rng.uniform(0,np.pi,160),rng.uniform(-np.pi,np.pi,160))]
    points += [(t,p) for t in (0.,1e-10,.013,.77,1.9,np.pi-1e-10,np.pi)
               for p in (-np.pi,-2.4,-np.pi/4,0.,.31,np.pi/4,2.5,np.pi)]
    for th,ph in points:
        e = float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
        records.append({"class":"off_grid_and_poles","theta":th,"phi":ph,"target_max_abs":e})
    assert all(r["target_max_abs"] < 2e-12 for r in records)
    worst = max(records,key=lambda r:r["target_max_abs"])
    out = {"beat":"AD-26","status":"S2_8CZ_89D2_LINEAR_ANGLE_ANALYTIC_CANDIDATE_NUMERIC_PASS",
           "topology":"89d2","cz_count":8,"edges":[list(e) for e in EDGES],
           "known_answer_gate":{"source_raw8_max_abs":source_e,"candidate_at_source_max_abs":candidate_e,
                                "negative_control":"core1 += pi/4","negative_control_max_abs":bad_e},
           "angle_recipe":{"frozen_pi_over_4":FROZEN_N,
                           "free_formulas":{"0":"5*pi/8 (global phase)","5":"pi/2+theta/2","6":"pi+phi",
                                            "9":"pi/2-theta/2","29":"pi/2-theta/2","33":"-3*pi/2-phi",
                                            "34":"pi/2+theta/2"}},
           "original_grid":{"points":25,"worst_max_abs":max(r["target_max_abs"] for r in records[:25])},
           "off_grid":{"points":len(points),"random_points":160,"pole_and_special_points":56,
                       "worst_max_abs":max(r["target_max_abs"] for r in records[25:])},
           "worst":worst,
           "evidence_level":"L2 complete explicit linear-angle candidate; exact symbolic certificate required for L1",
           "boundary":"数值命中不代替全参数恒等式；本结果不证明8-CZ最优，也不排除其他7-CZ拓扑。",
           "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
           "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    (R/"ad26_s2_analytic8_89d2_points.jsonl").write_text("".join(json.dumps(r,separators=(",",":"))+"\n" for r in records))
    raw = json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_analytic8_89d2_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"points":len(records),"worst":worst,
                      "negative_control_max_abs":bad_e,"seconds":time.time()-start,
                      "sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
