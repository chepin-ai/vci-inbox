"""AD-23 总验收：重跑三个互不导入构造器的验收器，并核对全部输入指纹与边界。"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def execute(script, log, timeout=240):
    proc = subprocess.run([sys.executable, str(RUN / script)], cwd=RUN,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=timeout, check=False)
    (RUN / log).write_bytes(proc.stdout)
    assert proc.returncode == 0, (script, proc.returncode, proc.stdout[-1500:].decode(errors="replace"))


def main():
    # 每个验收器均从原始件重建，不导入对应求解器、规范器或 AD-22 分析器。
    execute("ad23_exact_verify.py", "ad23_exact_verify.log")
    execute("ad23_lower_verify.py", "ad23_lower_verify.log")
    execute("ad23_s2_theta_verify.py", "ad23_s2_theta_verify.log")

    exact = json.loads((RUN / "ad23_exact_verify.json").read_text())
    lower = json.loads((RUN / "ad23_lower_verify.json").read_text())
    s2 = json.loads((RUN / "ad23_s2_theta_verify.json").read_text())
    gauge = json.loads((RUN / "ad23_gauge.json").read_text())
    certificate = json.loads((RUN / "ad23_maj_7cz_exact.json").read_text())
    rac = json.loads((RUN / "ad23_rac_check.json").read_text())

    assert exact["status"] == "INDEPENDENT_ALL_EXACT_ZERO"
    assert len(exact["hits"]) == 7
    assert all(h["exact_nonzero_residual_entries"] == 0 and h["canonical_shape"] for h in exact["hits"])
    assert exact["input_sha256"] == sha(RUN / "ad23_maj_7cz_exact.json")
    assert certificate["status"] == "ALL_EXACT_ZERO" and len(certificate["hits"]) == 7
    assert certificate["strict_interval"] == "4 <= k <= 7"

    assert gauge["coordinate_formula"] == "4*k+10; k=7 gives 38" and len(gauge["hits"]) == 7
    assert len(gauge["known_answer_gate"]["random_cases"]) == 12
    assert gauge["known_answer_gate"]["max_matrix_error"] < 2e-12

    assert lower["status"] == "INDEPENDENT_LOWER_PASS" and lower["runs"] == lower["unique_tasks"] == 784
    assert lower["errors"] == lower["independent_exact_e_lt_1e-9"] == 0
    assert lower["input_sha256"] == sha(RUN / "ad23_lower.jsonl")
    assert lower["summary_sha256"] == sha(RUN / "ad23_lower_summary.json")
    assert lower["strict_interval_unchanged"] == "4 <= k <= 7"

    assert s2["status"] == "INDEPENDENT_S2_THETA_PASS" and s2["evidence_level"] == "L2 numerical only"
    assert s2["old_points"] == 64 and s2["new_off_grid_points"] == s2["new_exact_e_lt_1e-9"] == 63
    assert s2["coordinate"] == {"core_index": 30, "label": "L7q0b", "formula": "(pi-theta)/2"}
    assert s2["new_raw_sha256"] == sha(RUN / "ad23_s2_theta.jsonl")
    assert s2["summary_sha256"] == sha(RUN / "ad23_s2_theta_summary.json")

    assert rac["verdict"] == "WAITING_PEER_S_SIM" and not rac["fingerprint_arrived"]
    assert rac["quantum_machine_consumption"] == rac["private_ci_consumption"] == 0
    assert all(item.get("has_numeric_S_sim") is False for repo in rac["repos"].values() for item in repo["candidates"])
    assert all(not item.get("queue_only", False) for repo in rac["repos"].values()
               for item in repo["candidates"] if item.get("source_code_excluded_from_fingerprint"))

    checks = {
        "gauge": {
            "formula": gauge["coordinate_formula"], "random_cases": 12,
            "max_matrix_error": gauge["known_answer_gate"]["max_matrix_error"], "compressed_hits": 7,
        },
        "maj_exact": {
            "hits": 7, "all_128_real_residuals_exact_zero": True,
            "engine": exact["engine"], "known_answer_gate": exact["known_answer_gate"],
            "strict_interval": "4 <= k <= 7", "upper_bound_evidence": "L1 exact construction",
        },
        "maj_lower": {
            "runs": lower["runs"], "unique_tasks": lower["unique_tasks"],
            "independent_zero_hits": lower["independent_exact_e_lt_1e-9"],
            "best_e": lower["independent_best"]["e"], "max_record_delta": lower["max_recorded_e_delta"],
            "evidence_level": "L2 negative numerical scan; not nonexistence",
        },
        "s2_theta": {
            "coordinate": s2["coordinate"], "old_points": 64,
            "old_max_formula_delta": s2["old_max_core30_formula_delta"],
            "new_off_grid_points": 63, "new_max_e": s2["new_max_e"],
            "wrong_phi_control_e": s2["wrong_phi_control_e"],
            "evidence_level": "L2 only; full meridian analytic lift open",
        },
        "rac": {
            "checked_at": rac["checked_at"], "verdict": rac["verdict"],
            "fingerprint_arrived": False,
            "heads": {name: repo["head"] for name, repo in rac["repos"].items()},
            "candidate_counts": {name: repo["candidate_counts"] for name, repo in rac["repos"].items()},
        },
    }
    report = {
        "beat": "AD-23", "status": "ALL_PASS", "checks": checks,
        "input_sha256": {
            "ad23_gauge.json": sha(RUN / "ad23_gauge.json"),
            "ad23_maj_7cz_exact.json": sha(RUN / "ad23_maj_7cz_exact.json"),
            "ad23_lower.jsonl": sha(RUN / "ad23_lower.jsonl"),
            "ad23_s2_theta.jsonl": sha(RUN / "ad23_s2_theta.jsonl"),
            "ad23_rac_check.json": sha(RUN / "ad23_rac_check.json"),
        },
        "anomaly_notes": [
            "第一诚律·异常注记1：原始角网格周期映射与全局相位π/4误吸附均不作废原账；最终局部门用π/4、全局相位用π/8，并由分圆域全矩阵精确零取代浮点吸附判据。",
            "第一诚律·异常注记2：wpow(0)构造、Rz数值参考半角及CZ²无效反序对照已修正；独立已知门改用有序dagger恒等式与非平凡A CZ A† CZ对照。",
            "第一诚律·异常注记3：S²早期L6q1b/core27/core29标签误判不进入结论；最终全坐标重算为core30=L7q0b，单坐标不重解最大残差0.423712066106791，故只记坐标证据。",
            "第一诚律·异常注记4：删门独立重建与记录最大差6.307504518687779e-11，来自最大3543825.6501064003的未约化角及求值次序；命中只按独立残差判定，零命中不升级为下界。",
            "第一诚律·异常注记5：RAC差集首次IncompleteRead，按传输纪律重试一次成功；源码内队列字面量曾造成queue_only误标，修正为源码不充当指纹、队列只认报告件后重跑。",
        ],
        "strict_interval": "4 <= k <= 7",
        "open_boundaries": [
            "k=4,5,6精确代数否证或更优解析下界未建立。",
            "序34其余核心角、序85/91经线以及全S²同模板解析覆盖未闭合。",
            "±π/8角刚性与外方向全局不可达仍未证明。",
            "RAC对方数值S_sim未到件，跨线独立对拍未启动。",
        ],
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    (RUN / "ad23_verify.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "ALL_PASS", "checks": checks, "strict_interval": report["strict_interval"],
                      "private_ci_consumption": 0, "quantum_machine_consumption": 0}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
