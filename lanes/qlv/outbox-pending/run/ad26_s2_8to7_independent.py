"""AD-26 S^2 8->7及两种7-CZ网格的独立全矩阵重建。"""
import hashlib
import json
from pathlib import Path
import numpy as np
import ad26_s2_9to8_independent as ind

R=Path(__file__).resolve().parent


def main():
    T=ind.target(ind.THETA,ind.PHI)
    srcrows=[json.loads(x) for x in (R/"ad26_s2_9to8.jsonl").read_text().splitlines() if x.strip()]
    src=next(r for r in srcrows if r["topology"]=="89" and r["deleted"]==[2] and r["kick"]==.02)
    edges=[tuple(e) for e in src["edges"]];p=ind.expand(src["x_core"],edges)
    source_e=float(np.max(abs(ind.circuit(p,edges)-T)));assert source_e<2e-12
    bad=p.copy();bad[2]+=np.pi/4
    bad_e=float(np.max(abs(ind.circuit(bad,edges)-T)));assert bad_e>1e-3
    rows=[json.loads(x) for x in (R/"ad26_s2_8to7.jsonl").read_text().splitlines() if x.strip()]
    assert len(rows)==16;errors=[];max_delta=0.
    for r in rows:
        assert "error" not in r;edges=[tuple(e) for e in r["edges"]];assert len(edges)==7
        e=float(np.max(abs(ind.circuit(ind.expand(r["x_core"],edges),edges)-T)))
        max_delta=max(max_delta,abs(e-r["target_max_abs"]));assert abs(e-r["target_max_abs"])<2e-9
        errors.append(e)
    hits=sum(e<1e-9 for e in errors);assert hits==3
    grids={};grid_total=0;grid_hits=0
    for stem in ("89d2d0","89d2d6"):
        rr=[json.loads(x) for x in (R/f"ad26_s2_continue7_{stem}.jsonl").read_text().splitlines() if x.strip()]
        ss=json.loads((R/f"ad26_s2_continue7_{stem}_summary.json").read_text());assert len(rr)==25
        ee=[]
        for r in rr:
            e=float(np.max(abs(ind.circuit(r["x_raw"],ss["edges"])-ind.target(r["theta"],r["phi"]))))
            assert abs(e-r["target_max_abs"])<2e-9;ee.append(e)
        h=sum(e<1e-9 for e in ee);assert h==ss["exact_numeric_hits"]
        grids[stem]={"grid_points":len(rr),"exact_numeric_hits":h,"worst_max_abs":max(ee),"edges":ss["edges"]}
        grid_total+=len(rr);grid_hits+=h
    out={"beat":"AD-26","status":"S2_8TO7_AND_TWO_7CZ_GRIDS_INDEPENDENT_REBUILD_PASS",
         "source_known_answer_gate":{"source_8cz_max_abs":source_e,"changed_angle_counterexample_max_abs":bad_e},
         "point_runs":len(rows),"point_exact_numeric_hits":hits,"point_max_target_rebuild_difference":max_delta,
         "grid_points":grid_total,"grid_exact_numeric_hits":grid_hits,"per_grid":grids,
         "evidence_level":"L2 independent full-matrix rebuild of 16 point runs and two finite 5x5 grids",
         "boundary":"3条单点命中与50点网格命中均不自行构成全S^2恒等式；需另行精确证书。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_8to7_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"point_hits":hits,"grid_points":grid_total,"grid_hits":grid_hits,
                      "max_target_rebuild_difference":max_delta,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
