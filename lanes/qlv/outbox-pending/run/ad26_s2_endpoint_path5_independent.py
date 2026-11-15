"""AD-26 theta=0 PATH5结构邻域36条保存坐标的独立重建。"""
import hashlib,json,time
from pathlib import Path
import numpy as np
import ad26_s2_independent8_89d2 as low
import ad26_s2_independent6_89d2d6d2 as known

R=Path(__file__).resolve().parent


def expand(core,edges):
    p=np.zeros(1+9*(len(edges)+1));p[low.raw_indices(edges)]=np.asarray(core,float);return p


def main():
    start=time.time();T=low.target(0.,0.)
    positive=float(np.max(abs(low.circuit(known.full6_raw(0.,0.),known.EDGES)-T)));assert positive<2e-12
    bad=known.core(0.,0.);bad[1]+=np.pi/4
    negative=float(np.max(abs(low.circuit(expand(bad,known.EDGES),known.EDGES)-T)));assert negative>1e-3
    cert=json.loads((R/"ad26_s2_endpoint_case5_exact_summary.json").read_text())
    assert cert["status"]=="S2_THETA0_DIAGONAL_AND_UNRESTRICTED_5CZ_EXACT_PASS"
    assert cert["case5b"]["full_target_including_global_phase_nonzero_residual_entries"]==0
    rows=[json.loads(x) for x in (R/"ad26_s2_endpoint_path5.jsonl").read_text().splitlines() if x.strip()]
    src=json.loads((R/"ad26_s2_endpoint_path5_summary.json").read_text())
    assert len(rows)==src["runs"]==36 and src["errors"]==0
    records=[];maxdiff=0.
    for idx,r in enumerate(rows):
        assert "error" not in r and len(r["edges"])==5 and len(r["x_core"])==30
        edges=[tuple(e) for e in r["edges"]];assert all(e in ((0,1),(1,2),(0,2)) for e in edges)
        scope="PATH" if all(e in ((0,1),(1,2)) for e in edges) else "unrestricted_auxiliary"
        e=float(np.max(abs(low.circuit(expand(r["x_core"],edges),edges)-T)))
        maxdiff=max(maxdiff,abs(e-r["target_max_abs"]))
        records.append({"index":idx,"family":r["family"],"label":r["label"],"kick":r["kick"],"scope":scope,
                        "edges":r["edges"],"saved_target_max_abs":r["target_max_abs"],"rebuilt_target_max_abs":e,
                        "exact_numeric_hit":e<1e-9})
    assert maxdiff<2e-14 and not any(r["exact_numeric_hit"] for r in records)
    per={}
    for scope in src["per_scope"]:
        rr=[r for r in records if r["scope"]==scope];best=min(rr,key=lambda r:r["rebuilt_target_max_abs"]);old=src["per_scope"][scope]
        assert len(rr)==old["runs"] and best["label"]==old["best"]["label"] and best["kick"]==old["best"]["kick"]
        assert abs(best["rebuilt_target_max_abs"]-old["best"]["target_max_abs"])<2e-14
        per[scope]={"runs":len(rr),"exact_numeric_hits":0,"best":best}
    assert per["PATH"]["runs"]==src["path_runs"]==24 and per["unrestricted_auxiliary"]["runs"]==12
    out={"beat":"AD-26","status":"S2_THETA0_CASE5_NEIGHBOR_PATH5_INDEPENDENT_REBUILD_PASS",
         "known_answer_gate":{"independent_6cz_max_abs":positive,"changed_angle_counterexample_max_abs":negative,
                              "linked_unrestricted_exact_certificate":cert["status"]},
         "runs":len(rows),"errors":0,"exact_numeric_hits":0,"path_runs":per["PATH"]["runs"],
         "path_exact_numeric_hits":0,"max_saved_metric_rebuild_difference":maxdiff,
         "per_scope":per,"records":records,"evidence_level":"独立L2复验：36条保存坐标逐条全矩阵重建",
         "boundary":"PATH只含24轨，另12轨保留02边、仅作unrestricted辅助；零命中不证明PATH 5-CZ不存在。", 
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/"ad26_s2_endpoint_path5_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"runs":len(rows),"hits":0,"max_saved_metric_rebuild_difference":maxdiff,
                      "best":{k:v["best"]["rebuilt_target_max_abs"] for k,v in per.items()},
                      "seconds":time.time()-start,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
