"""AD-26 S^2：[8,9] 9-CZ 全参数线性角解析候选。

39 个局部角固定为 pi/4 整数倍；其余坐标仅为 theta/2 与 phi
的一次式。这里输出数值候选；全参数证据等级须由独立符号证书升级。
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent.parent / "ad22/run"))
import ad22_verify as base
sys.path.insert(0, str(R.parent.parent / "ad25/run"))
import ad25_s2_meridian as s2
sys.path.insert(0, str(R))
from ad26_s2_prune import expand

EDGES = [(0,1),(0,1),(0,1),(0,1),(1,2),(0,1),(1,2),(0,1),(0,1)]
FROZEN_N = {1:1,3:6,4:0,6:4,7:0,8:13,10:0,11:3,12:5,13:4,14:12,
            15:4,16:2,17:2,18:0,19:4,20:7,21:0,22:7,23:1,24:3,25:7,
            26:4,27:4,28:15,29:0,30:10,31:3,32:0,34:0,35:2,36:14,
            39:8,40:0,41:6,42:9,43:10,44:0,45:15}
FREE = [0,2,5,9,33,37,38]


def core(theta, phi):
    c = np.zeros(46, dtype=float)
    for j,n in FROZEN_N.items():
        c[j] = n*np.pi/4
    c[0] = 3*np.pi/8
    c[2] = -np.pi/2+phi
    c[5] = np.pi/2+theta/2
    c[9] = 3*np.pi/4+theta/2
    c[33] = -np.pi/2+theta/2
    c[37] = -np.pi/2-phi
    c[38] = -np.pi/2-theta/2
    return c


def matrix(theta, phi):
    return base.circuit(expand(core(theta,phi),EDGES),EDGES)


def main():
    start = time.time()
    src = json.loads((R/"ad26_s2_raw9_89.json").read_text())
    assert [tuple(e) for e in src["edges"]] == EDGES
    source_e = float(np.max(abs(base.circuit(np.asarray(src["x_raw"]),EDGES)-
                                  s2.target(np.pi/7,.31))))
    assert source_e < 2e-12
    th,ph = np.pi/7,.31
    candidate_e = float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
    bad = core(th,ph).copy()
    bad[1] += np.pi/4  # 第0层q0的Ry；不是全局相位core0。
    bad_e = float(np.max(abs(base.circuit(expand(bad,EDGES),EDGES)-s2.target(th,ph))))
    assert candidate_e < 2e-12 and bad_e > 1e-3

    grid = [json.loads(x) for x in
            (R/"ad26_s2_gauge_reduced_89_grid.jsonl").read_text().splitlines() if x.strip()]
    records = []
    for row in grid:
        th,ph = row["theta"],row["phi"]
        e = float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
        records.append({"class":"original_5x5_grid","theta":th,"phi":ph,"target_max_abs":e})
    assert len(records) == 25 and all(r["target_max_abs"] < 2e-12 for r in records)

    rng = np.random.default_rng(26111589)
    points = [(float(t),float(p)) for t,p in
              zip(rng.uniform(0,np.pi,160),rng.uniform(-np.pi,np.pi,160))]
    points += [(t,p) for t in (0.,1e-10,.013,.77,1.9,np.pi-1e-10,np.pi)
               for p in (-np.pi,-2.4,-np.pi/4,0.,.31,np.pi/4,2.5,np.pi)]
    for th,ph in points:
        e = float(np.max(abs(matrix(th,ph)-s2.target(th,ph))))
        records.append({"class":"off_grid_and_poles","theta":th,"phi":ph,"target_max_abs":e})
    assert all(r["target_max_abs"] < 2e-12 for r in records)
    worst = max(records,key=lambda r:r["target_max_abs"])
    out = {
        "beat":"AD-26","status":"S2_9CZ_89_LINEAR_ANGLE_ANALYTIC_CANDIDATE_NUMERIC_PASS",
        "topology":"89","cz_count":9,"edges":[list(e) for e in EDGES],
        "known_answer_gate":{"source_raw9_max_abs":source_e,
                             "candidate_at_source_max_abs":candidate_e,
                             "negative_control":"core1 += pi/4",
                             "negative_control_max_abs":bad_e},
        "angle_recipe":{"frozen_pi_over_4":FROZEN_N,
                        "free_formulas":{"0":"3*pi/8","2":"-pi/2+phi",
                                         "5":"pi/2+theta/2","9":"3*pi/4+theta/2",
                                         "33":"-pi/2+theta/2","37":"-pi/2-phi",
                                         "38":"-pi/2-theta/2"}},
        "original_grid":{"points":25,"worst_max_abs":max(r["target_max_abs"] for r in records[:25])},
        "off_grid":{"points":len(points),"random_points":160,"pole_and_special_points":56,
                    "worst_max_abs":max(r["target_max_abs"] for r in records[25:])},
        "worst":worst,
        "evidence_level":"L2 complete explicit linear-angle candidate with deterministic numeric reconstruction; symbolic certificate still required for L1",
        "boundary":"数值命中不代替全参数恒等式；本结果不证明9-CZ最优，也不预先断言与[0,10]块级同族。",
        "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
        "quantum_machine_launched":False,"quantum_account_quota_verified":False,
    }
    (R/"ad26_s2_analytic9_89_points.jsonl").write_text(
        "".join(json.dumps(r,separators=(",",":"))+"\n" for r in records))
    raw = json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_analytic9_89_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"points":len(records),"worst":worst,
                      "negative_control_max_abs":bad_e,"seconds":time.time()-start,
                      "sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
