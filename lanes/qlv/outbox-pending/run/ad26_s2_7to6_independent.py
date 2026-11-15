"""AD-26 S^2 7->6及两种6-CZ网格的独立全矩阵重建。"""
import hashlib,json
from pathlib import Path
import numpy as np
import ad26_s2_9to8_independent as ind

R=Path(__file__).resolve().parent;SELECT={"89d2d0":0,"89d2d6":6}


def main():
    T=ind.target(ind.THETA,ind.PHI);sources={}
    srcrows=[json.loads(x) for x in (R/"ad26_s2_8to7.jsonl").read_text().splitlines() if x.strip()]
    for stem,deleted in SELECT.items():
        src=next(r for r in srcrows if r["deleted"]==[deleted] and r["kick"]==.02)
        edges=[tuple(e) for e in src["edges"]];p=ind.expand(src["x_core"],edges)
        e=float(np.max(abs(ind.circuit(p,edges)-T)));assert e<2e-12
        bad=p.copy();bad[2]+=np.pi/4;be=float(np.max(abs(ind.circuit(bad,edges)-T)));assert be>1e-3
        sources[stem]={"source_7cz_max_abs":e,"changed_angle_counterexample_max_abs":be}
    rows=[json.loads(x) for x in (R/"ad26_s2_7to6.jsonl").read_text().splitlines() if x.strip()]
    assert len(rows)==28;per={};max_delta=0.
    for r in rows:
        assert "error" not in r;edges=[tuple(e) for e in r["edges"]];assert len(edges)==6
        e=float(np.max(abs(ind.circuit(ind.expand(r["x_core"],edges),edges)-T)))
        max_delta=max(max_delta,abs(e-r["target_max_abs"]));assert abs(e-r["target_max_abs"])<2e-9
        per.setdefault(r["topology"],[]).append(e)
    for stem,ee in per.items(): assert len(ee)==14
    hits=sum(e<1e-9 for ee in per.values() for e in ee);assert hits==6
    grids={};total=0;ghits=0
    for stem in ("89d2d0d1","89d2d6d2"):
        rr=[json.loads(x) for x in (R/f"ad26_s2_continue6_{stem}.jsonl").read_text().splitlines() if x.strip()]
        ss=json.loads((R/f"ad26_s2_continue6_{stem}_summary.json").read_text());assert len(rr)==25
        ee=[]
        for r in rr:
            e=float(np.max(abs(ind.circuit(r["x_raw"],ss["edges"])-ind.target(r["theta"],r["phi"]))))
            assert abs(e-r["target_max_abs"])<2e-9;ee.append(e)
        h=sum(e<1e-9 for e in ee);assert h==ss["exact_numeric_hits"]
        grids[stem]={"grid_points":25,"exact_numeric_hits":h,"worst_max_abs":max(ee),"edges":ss["edges"]}
        total+=25;ghits+=h
    out={"beat":"AD-26","status":"S2_7TO6_AND_TWO_6CZ_GRIDS_INDEPENDENT_REBUILD_PASS",
         "source_known_answer_gate":sources,"point_runs":len(rows),"point_exact_numeric_hits":hits,
         "point_max_target_rebuild_difference":max_delta,"grid_points":total,"grid_exact_numeric_hits":ghits,
         "per_grid":grids,"evidence_level":"L2 independent full-matrix rebuild of 28 point runs and two finite 5x5 grids",
         "boundary":"6条单点命中与50点网格命中均不自行构成全S^2恒等式；需另行精确证书。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_7to6_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"point_hits":hits,"grid_points":total,"grid_hits":ghits,
                      "max_target_rebuild_difference":max_delta,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
