"""AD-26 两个6-CZ代表元6->5全部保存坐标的独立全矩阵重建。"""
import hashlib,json,time
from pathlib import Path
import numpy as np
import ad26_s2_independent8_89d2 as low
import ad26_s2_independent6_89d2d6d2 as known

R=Path(__file__).resolve().parent
THETA,PHI=np.pi/7,0.31


def expand(core,edges):
    p=np.zeros(1+9*(len(edges)+1));p[low.raw_indices(edges)]=np.asarray(core,float)
    return p


def main():
    start=time.time()
    # 判读器先过已知答案门：独立6-CZ公式命中，改角必须失败。
    p6=known.full6_raw(THETA,PHI);T=low.target(THETA,PHI)
    known_hit=float(np.max(abs(low.circuit(p6,known.EDGES)-T)));assert known_hit<2e-12
    bad=known.core(THETA,PHI);bad[1]+=np.pi/4
    known_negative=float(np.max(abs(low.circuit(expand(bad,known.EDGES),known.EDGES)-T)));assert known_negative>1e-3
    rows=[json.loads(x) for x in (R/"ad26_s2_6to5.jsonl").read_text().splitlines() if x.strip()]
    source_summary=json.loads((R/"ad26_s2_6to5_summary.json").read_text())
    assert len(rows)==source_summary["runs"]==24 and source_summary["errors"]==0
    rebuilt=[];max_saved_difference=0.;max_coordinate_rebuild_difference=0.
    for idx,r in enumerate(rows):
        assert "error" not in r and r["k"]==5 and len(r["edges"])==5 and len(r["x_core"])==30
        edges=[tuple(e) for e in r["edges"]];assert all(e in ((0,1),(1,2)) for e in edges)
        p=expand(r["x_core"],edges);assert np.max(abs(p[low.raw_indices(edges)]-np.asarray(r["x_core"])))==0
        U=low.circuit(p,edges);e=float(np.max(abs(U-T)));saved=float(r["target_max_abs"])
        max_saved_difference=max(max_saved_difference,abs(e-saved))
        # 第二次从保存的实数列表重录，禁止复用第一次展开的数组。
        p2=np.zeros(1+9*(len(edges)+1),dtype=np.float64)
        for j,k in enumerate(low.raw_indices(edges)):p2[k]=float(r["x_core"][j])
        U2=low.circuit(p2,edges);max_coordinate_rebuild_difference=max(max_coordinate_rebuild_difference,float(np.max(abs(U-U2))))
        rebuilt.append({"index":idx,"topology":r["topology"],"deleted":r["deleted"],"kick":r["kick"],
                        "edges":r["edges"],"saved_target_max_abs":saved,"rebuilt_target_max_abs":e,
                        "exact_numeric_hit":e<1e-9})
    hits=[r for r in rebuilt if r["exact_numeric_hit"]]
    assert len(hits)==source_summary["exact_numeric_hits"]==0
    assert max_saved_difference<2e-14 and max_coordinate_rebuild_difference==0
    per={}
    for stem in source_summary["per_topology"]:
        rr=[r for r in rebuilt if r["topology"]==stem];best=min(rr,key=lambda r:r["rebuilt_target_max_abs"])
        old=source_summary["per_topology"][stem]
        assert len(rr)==old["runs"]==12
        assert best["deleted"]==old["best"]["deleted"] and best["kick"]==old["best"]["kick"]
        assert abs(best["rebuilt_target_max_abs"]-old["best"]["target_max_abs"])<2e-14
        per[stem]={"runs":len(rr),"exact_numeric_hits":0,"best":best}
    out={"beat":"AD-26","status":"S2_TWO_6CZ_TO5_INDEPENDENT_REBUILD_PASS",
         "source_policy":"只读取原始jsonl保存坐标与汇总；目标、raw解码和电路矩阵复用独立验收原语，不导入6to5求解器或其依赖求解模块。",
         "known_answer_gate":{"independent_6cz_max_abs":known_hit,"changed_angle_counterexample_max_abs":known_negative},
         "theta":THETA,"phi":PHI,"runs":len(rebuilt),"errors":0,"exact_numeric_hits":len(hits),
         "max_saved_metric_rebuild_difference":max_saved_difference,
         "max_full_matrix_second_decode_difference":max_coordinate_rebuild_difference,
         "per_topology":per,"records":rebuilt,
         "evidence_level":"独立L2复验：24条原始保存坐标的逐条全矩阵重建",
         "boundary":"零命中只限两个代表元的指定删门与扰动；不证明5-CZ不存在，也不证明6-CZ最优。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_6to5_independent_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"runs":len(rows),"hits":len(hits),
         "max_saved_metric_rebuild_difference":max_saved_difference,
         "max_full_matrix_second_decode_difference":max_coordinate_rebuild_difference,
         "best":{k:v["best"]["rebuilt_target_max_abs"] for k,v in per.items()},
         "seconds":time.time()-start,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
