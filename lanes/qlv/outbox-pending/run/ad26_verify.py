"""AD-26 确定性总验收：冷进程重放证书与保存坐标，不重跑数值优化。

总验收只把子进程的确定性 JSON 作为证据；stdout 中的耗时不得进入证书。
RAC 只读取发布前最新复查件，离线干净重建不伪造新的到件检查时间。
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
R25 = R.parent.parent / "ad25/run"
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())


def known_answer_gate():
    """先用有限已知答案自证目标、CX/CZ 转换和精确相位域。"""
    def bits(x):
        return [(x >> 2) & 1, (x >> 1) & 1, x & 1]

    def code(b):
        return (b[0] << 2) | (b[1] << 1) | b[2]

    def permutation(fn):
        m = np.zeros((8, 8), dtype=int)
        for x in range(8):
            m[fn(x), x] = 1
        return m

    def cnot(c, t):
        return permutation(lambda x: code([bits(x)[q] ^ (bits(x)[c] if q == t else 0)
                                          for q in range(3)]))

    def toffoli():
        def fn(x):
            b = bits(x)
            if b[0] and b[2]:
                b[1] ^= 1
            return code(b)
        return permutation(fn)

    maj = toffoli() @ cnot(1, 2) @ cnot(1, 0)
    expected = np.zeros((8, 8), dtype=int)
    for x in range(8):
        a, b, c = bits(x)
        expected[code([a ^ b, (a & b) ^ (a & c) ^ (b & c), b ^ c]), x] = 1
    assert np.array_equal(maj, expected)
    assert not np.array_equal(maj, toffoli())

    h = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    i2 = sp.eye(2)
    cz = sp.diag(1, 1, 1, -1)
    converted = sp.kronecker_product(i2, h) * cz * sp.kronecker_product(i2, h)
    cx01 = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    assert converted == cx01
    assert cz != cx01
    w = sp.exp(sp.I * sp.pi / 8)
    assert sp.simplify(w**8 + 1) == 0
    return {
        "maj_basis_map": "q0=a xor b; q1=ab xor ac xor bc; q2=b xor c; all 8 inputs exact",
        "maj_nonidentity_negative_control": True,
        "H_target_CZ_H_target_equals_CX_max_abs": 0.0,
        "CZ_without_H_conjugation_negative_control": "CZ != CX exact",
        "cyclotomic_relation": "w=exp(i*pi/8), w^8+1=0 exact",
    }


def run_child(key, script, outputs, expected_status, cwd=R, args=()):
    outputs = [outputs] if isinstance(outputs, str) else list(outputs)
    for name in outputs:
        p = cwd / name
        if p.exists():
            p.unlink()  # 拒绝把陈旧通过件当本次运行结果。
    proc = subprocess.run([sys.executable, str(cwd / script), *args], cwd=cwd,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=1200, check=False)
    (R / f"ad26_verify_child_{key}.log").write_bytes(proc.stdout)
    assert proc.returncode == 0, (key, proc.returncode, proc.stdout[-3000:].decode(errors="replace"))
    docs = {}
    for name in outputs:
        raw = (cwd / name).read_bytes()
        docs[name] = json.loads(raw)
    primary = docs[outputs[-1]]
    assert primary["status"] == expected_status, (key, primary["status"])
    return docs, {
        "script": script, "args": list(args), "outputs": outputs,
        "returncode": proc.returncode,
        "json_sha256": {name: sha((cwd / name).read_bytes()) for name in outputs},
    }


def assert_zero_machine(doc):
    assert doc["private_ci_consumption"] == 0
    assert doc["quantum_machine_actual_consumption_seconds"] == 0
    assert doc["quantum_machine_launched"] is False
    assert doc["quantum_account_quota_verified"] is False


def check_symbolic(k, stem, docs, entries_name, summary_name, expected_edges):
    entries = docs[entries_name]
    summary = docs[summary_name]
    assert summary["cz_count"] == k and summary["topology"] == stem
    assert summary["edges"] == [list(e) for e in expected_edges]
    assert summary["proof"]["nonzero_residual_entries"] == 32
    assert summary["proof"]["passed_entries"] == 32
    assert summary["proof"]["numerics_in_identity_decision"] is False
    assert summary["proof"]["entries_sha256"] == sha((R / entries_name).read_bytes())
    assert len(entries["entries"]) == 32
    assert all(x["pass"] and x["reduced_term_count"] == 0 for x in entries["entries"])
    assert summary["field_known_answer_gate"]["wrong_order_control_nonzero"] == 32
    assert_zero_machine(summary)


def check_independent(k, doc, symbolic):
    assert doc["numeric_points"] == 328
    assert doc["theta_zero_exact"]["exact_nonzero_residual_entries"] == 0
    assert doc["theta_zero_exact"]["negative_control_nonzero_entries"] > 0
    assert doc["worst"]["target_max_abs"] < 4e-15
    assert doc["negative_control_max_abs"] > 1e-3
    assert doc["linked_symbolic_certificate"]["sha256"] == symbolic["json_sha256"][
        f"ad26_s2_symbolic{k}_" + ("89d2_qw_summary.json" if k == 8 else
                                   "89d2d6_qw_summary.json" if k == 7 else "89d2d6d2_qw_summary.json")]
    assert_zero_machine(doc)


def main():
    gate = known_answer_gate()
    children = {}

    docs, children["maj_k4"] = run_child(
        "maj_k4", "ad26_maj_k4_independent.py", "ad26_maj_k4_independent_summary.json",
        "MAJ_K4_BRANCH_DIRECT_INDEPENDENT_REBUILD_PASS")
    maj = docs["ad26_maj_k4_independent_summary.json"]
    assert maj["combined_protocol_runs"] == 48 and maj["combined_exact_joint_hits"] == 0
    assert maj["strict_interval"] == "4 <= k <= 7"
    assert maj["weighted_continuation"]["max_target_rebuild_difference"] == 0.0
    assert maj["direct_continuation"]["max_target_rebuild_difference"] == 0.0
    assert_zero_machine(maj)

    docs, children["s2_9to8"] = run_child(
        "s2_9to8", "ad26_s2_9to8_independent.py", "ad26_s2_9to8_independent_summary.json",
        "S2_TWO_9CZ_TO8_INDEPENDENT_REBUILD_PASS")
    s98 = docs["ad26_s2_9to8_independent_summary.json"]
    assert (s98["runs"], s98["exact_numeric_hits"], s98["max_target_rebuild_difference"]) == (36, 7, 0.0)

    docs, children["s2_continue8"] = run_child(
        "s2_continue8", "ad26_s2_continue8_independent.py", "ad26_s2_continue8_independent_summary.json",
        "S2_8CZ_GRID_INDEPENDENT_REBUILD_PASS")
    sc8 = docs["ad26_s2_continue8_independent_summary.json"]
    assert (sc8["grid_points"], sc8["exact_numeric_hits"], sc8["max_target_rebuild_difference"]) == (75, 75, 0.0)

    docs, children["s2_8to7"] = run_child(
        "s2_8to7", "ad26_s2_8to7_independent.py", "ad26_s2_8to7_independent_summary.json",
        "S2_8TO7_AND_TWO_7CZ_GRIDS_INDEPENDENT_REBUILD_PASS")
    s87 = docs["ad26_s2_8to7_independent_summary.json"]
    assert (s87["point_runs"], s87["point_exact_numeric_hits"]) == (16, 3)
    assert (s87["grid_points"], s87["grid_exact_numeric_hits"], s87["point_max_target_rebuild_difference"]) == (50, 50, 0.0)

    docs, children["s2_7to6"] = run_child(
        "s2_7to6", "ad26_s2_7to6_independent.py", "ad26_s2_7to6_independent_summary.json",
        "S2_7TO6_AND_TWO_6CZ_GRIDS_INDEPENDENT_REBUILD_PASS")
    s76 = docs["ad26_s2_7to6_independent_summary.json"]
    assert (s76["point_runs"], s76["point_exact_numeric_hits"]) == (28, 6)
    assert (s76["grid_points"], s76["grid_exact_numeric_hits"], s76["point_max_target_rebuild_difference"]) == (50, 50, 0.0)

    sym8docs, children["symbolic8"] = run_child(
        "symbolic8", "ad26_s2_symbolic8_89d2_qw.py",
        ["ad26_s2_symbolic8_89d2_qw_entries.json", "ad26_s2_symbolic8_89d2_qw_summary.json"],
        "S2_8CZ_89D2_FULL_SPHERE_DIRECT_L1_EXACT_PASS")
    check_symbolic(8, "89d2", sym8docs, "ad26_s2_symbolic8_89d2_qw_entries.json",
                   "ad26_s2_symbolic8_89d2_qw_summary.json",
                   [(0, 1), (0, 1), (0, 1), (1, 2), (0, 1), (1, 2), (0, 1), (0, 1)])
    docs, children["independent8"] = run_child(
        "independent8", "ad26_s2_independent8_89d2.py", "ad26_s2_independent8_89d2_summary.json",
        "S2_8CZ_89D2_INDEPENDENT_REBUILD_PASS")
    ind8 = docs["ad26_s2_independent8_89d2_summary.json"]
    check_independent(8, ind8, children["symbolic8"])

    sym7docs, children["symbolic7"] = run_child(
        "symbolic7", "ad26_s2_symbolic7_89d2d6_qw.py",
        ["ad26_s2_symbolic7_89d2d6_qw_entries.json", "ad26_s2_symbolic7_89d2d6_qw_summary.json"],
        "S2_7CZ_89D2D6_FULL_SPHERE_DIRECT_L1_EXACT_PASS")
    check_symbolic(7, "89d2d6", sym7docs, "ad26_s2_symbolic7_89d2d6_qw_entries.json",
                   "ad26_s2_symbolic7_89d2d6_qw_summary.json",
                   [(0, 1), (0, 1), (0, 1), (1, 2), (0, 1), (1, 2), (0, 1)])
    docs, children["independent7"] = run_child(
        "independent7", "ad26_s2_independent7_89d2d6.py", "ad26_s2_independent7_89d2d6_summary.json",
        "S2_7CZ_89D2D6_INDEPENDENT_REBUILD_PASS")
    ind7 = docs["ad26_s2_independent7_89d2d6_summary.json"]
    check_independent(7, ind7, children["symbolic7"])

    sym6docs, children["symbolic6"] = run_child(
        "symbolic6", "ad26_s2_symbolic_linear_qw.py",
        ["ad26_s2_symbolic6_89d2d6d2_qw_entries.json", "ad26_s2_symbolic6_89d2d6d2_qw_summary.json"],
        "S2_6CZ_89D2D6D2_FULL_SPHERE_DIRECT_L1_EXACT_PASS", args=("ad26_s2_analytic6_89d2d6d2",))
    check_symbolic(6, "89d2d6d2", sym6docs, "ad26_s2_symbolic6_89d2d6d2_qw_entries.json",
                   "ad26_s2_symbolic6_89d2d6d2_qw_summary.json",
                   [(0, 1), (0, 1), (1, 2), (0, 1), (1, 2), (0, 1)])
    docs, children["independent6"] = run_child(
        "independent6", "ad26_s2_independent6_89d2d6d2.py", "ad26_s2_independent6_89d2d6d2_summary.json",
        "S2_6CZ_89D2D6D2_INDEPENDENT_REBUILD_PASS")
    ind6 = docs["ad26_s2_independent6_89d2d6d2_summary.json"]
    check_independent(6, ind6, children["symbolic6"])

    docs, children["s2_6to5"] = run_child(
        "s2_6to5", "ad26_s2_6to5_independent.py", "ad26_s2_6to5_independent_summary.json",
        "S2_TWO_6CZ_TO5_INDEPENDENT_REBUILD_PASS")
    s65 = docs["ad26_s2_6to5_independent_summary.json"]
    assert (s65["runs"], s65["errors"], s65["exact_numeric_hits"]) == (24, 0, 0)
    assert s65["max_saved_metric_rebuild_difference"] == 0.0
    assert s65["max_full_matrix_second_decode_difference"] == 0.0

    docs, children["endpoint_exact"] = run_child(
        "endpoint_exact", "ad26_s2_endpoint_case5_exact.py", "ad26_s2_endpoint_case5_exact_summary.json",
        "S2_THETA0_DIAGONAL_AND_UNRESTRICTED_5CZ_EXACT_PASS")
    endpoint = docs["ad26_s2_endpoint_case5_exact_summary.json"]
    assert endpoint["diagonal_identity"]["nonzero_residual_entries"] == 0
    assert endpoint["diagonal_identity"]["cx_to_cz_nonzero_residual_entries"] == 0
    assert endpoint["case5b"]["canonical_nonzero_residual_entries"] == 0
    assert endpoint["case5b"]["full_target_including_global_phase_nonzero_residual_entries"] == 0
    assert endpoint["case5b"]["delete_02_negative_control_nonzero_entries"] == 8
    assert endpoint["case5b"]["cx_edges_in_time_order"] == [[1, 2], [0, 1], [1, 2], [0, 1], [0, 2]]
    assert endpoint["minimum_unrestricted_three_qubit_cz"] == 5
    assert_zero_machine(endpoint)

    docs, children["endpoint_path5"] = run_child(
        "endpoint_path5", "ad26_s2_endpoint_path5_independent.py",
        "ad26_s2_endpoint_path5_independent_summary.json",
        "S2_THETA0_CASE5_NEIGHBOR_PATH5_INDEPENDENT_REBUILD_PASS")
    path5 = docs["ad26_s2_endpoint_path5_independent_summary.json"]
    assert (path5["runs"], path5["errors"], path5["exact_numeric_hits"]) == (36, 0, 0)
    assert (path5["path_runs"], path5["path_exact_numeric_hits"]) == (24, 0)
    assert path5["per_scope"]["unrestricted_auxiliary"]["runs"] == 12
    assert path5["max_saved_metric_rebuild_difference"] == 0.0

    docs, children["seq91"] = run_child(
        "seq91", "ad25_seq91_independent.py", "ad25_seq91_independent.json",
        "SEQ91_528_RAW_CIRCUITS_INDEPENDENT_PASS", cwd=R25)
    seq = docs["ad25_seq91_independent.json"]
    assert (seq["runs"], seq["exact_returns"], seq["signature_mismatches"]) == (528, 443, 0)
    assert seq["finite_difference_rank_check"]["raw73_rank"] == 33
    assert seq["finite_difference_rank_check"]["core38_rank"] == 33
    assert seq["finite_difference_rank_check"]["core38_nullity"] == 5

    docs, children["secondary"] = run_child(
        "secondary", "ad25_secondary.py", "ad25_secondary.json",
        "CONTROLLED_W_NORMALIZED_TRACE_SECOND_ORDER_L1_PASS", cwd=R25)
    secondary = docs["ad25_secondary.json"]
    assert secondary["trace_identity_max_error"] < 1e-12
    assert secondary["debts"] == ["DEBT-TOFFOLI-ANALYTIC-01"]

    # 数值搜索汇总只绑定原始账，不把重放证书写成重新发现。
    attack = {}
    for name, runs, hits in [("ad26_maj_7to6_summary.json", 98, 0),
                             ("ad26_maj_7to5_summary.json", 294, 0),
                             ("ad26_maj_k4_branch_summary.json", 24, 0),
                             ("ad26_maj_k4_direct_summary.json", 24, 0),
                             ("ad26_s2_9to8_summary.json", 36, 7),
                             ("ad26_s2_8to7_summary.json", 16, 3),
                             ("ad26_s2_7to6_summary.json", 28, 6),
                             ("ad26_s2_6to5_summary.json", 24, 0),
                             ("ad26_s2_endpoint_path5_summary.json", 36, 0)]:
        doc = load(R / name)
        assert doc["runs"] == runs and doc["errors"] == 0
        hit_key = "exact_joint_hits" if "exact_joint_hits" in doc else "exact_numeric_hits"
        assert doc[hit_key] == hits
        attack[name] = {"runs": runs, "errors": 0, hit_key: hits,
                        "best": doc.get("best", doc.get("per_scope"))}

    rac = load(R / "ad26_rac_check.json")
    assert rac["verdict"] == "WAITING_PEER_S_SIM" and rac["fingerprint_arrived"] is False
    assert all(not item["has_numeric_S_sim"] for repo in rac["repos"].values() for item in repo["candidates"])
    assert_zero_machine(rac)

    input_names = [
        "ad26_maj_7to6.jsonl", "ad26_maj_7to6_summary.json",
        "ad26_maj_7to5.jsonl", "ad26_maj_7to5_summary.json",
        "ad26_maj_k4_branch.jsonl", "ad26_maj_k4_branch_summary.json",
        "ad26_maj_k4_direct.jsonl", "ad26_maj_k4_direct_summary.json",
        "ad26_maj_k4_independent_summary.json",
        "ad26_s2_9to8.jsonl", "ad26_s2_9to8_summary.json", "ad26_s2_9to8_independent_summary.json",
        "ad26_s2_continue8_independent_summary.json",
        "ad26_s2_8to7.jsonl", "ad26_s2_8to7_summary.json", "ad26_s2_8to7_independent_summary.json",
        "ad26_s2_7to6.jsonl", "ad26_s2_7to6_summary.json", "ad26_s2_7to6_independent_summary.json",
        "ad26_s2_6to5.jsonl", "ad26_s2_6to5_summary.json", "ad26_s2_6to5_independent_summary.json",
        "ad26_s2_analytic8_89d2_summary.json", "ad26_s2_analytic7_89d2d6_summary.json",
        "ad26_s2_analytic6_89d2d6d2_summary.json",
        "ad26_s2_symbolic8_89d2_qw_entries.json", "ad26_s2_symbolic8_89d2_qw_summary.json",
        "ad26_s2_symbolic7_89d2d6_qw_entries.json", "ad26_s2_symbolic7_89d2d6_qw_summary.json",
        "ad26_s2_symbolic6_89d2d6d2_qw_entries.json", "ad26_s2_symbolic6_89d2d6d2_qw_summary.json",
        "ad26_s2_independent8_89d2_summary.json", "ad26_s2_independent7_89d2d6_summary.json",
        "ad26_s2_independent6_89d2d6d2_summary.json",
        "ad26_s2_endpoint_case5_exact_summary.json",
        "ad26_s2_endpoint_path5.jsonl", "ad26_s2_endpoint_path5_summary.json",
        "ad26_s2_endpoint_path5_independent_summary.json", "ad26_rac_check.json",
    ]
    for stem in ("89d2", "89d7", "010d1"):
        input_names += [f"ad26_s2_continue8_{stem}.jsonl", f"ad26_s2_continue8_{stem}_summary.json"]
    for k, stems in ((7, ("89d2d0", "89d2d6")), (6, ("89d2d0d1", "89d2d6d2"))):
        for stem in stems:
            input_names += [f"ad26_s2_continue{k}_{stem}.jsonl", f"ad26_s2_continue{k}_{stem}_summary.json"]
    inputs = {name: sha((R / name).read_bytes()) for name in sorted(set(input_names))}
    for name in ("ad25_seq91_rank_diagnostic.json", "ad25_seq91_transversal_metric.jsonl",
                 "ad25_seq91_transversal_metric_summary.json", "ad25_seq91_independent.json",
                 "ad25_secondary.json"):
        inputs["ad25/run/" + name] = sha((R25 / name).read_bytes())
    inputs["ad21/run/ad21_seq91_base.json"] = sha((R25.parent.parent / "ad21/run/ad21_seq91_base.json").read_bytes())

    out = {
        "beat": "AD-26", "status": "ALL_PASS",
        "known_answer_gate_first": gate,
        "cold_process_children": children,
        "headline": {
            "maj_interval": "4 <= k <= 7", "maj_k4_protocol_runs": 48, "maj_k4_joint_hits": 0,
            "s2_full_sphere_exact_cz": 6, "s2_full_sphere_6cz_edges": [[0, 1], [0, 1], [1, 2], [0, 1], [1, 2], [0, 1]],
            "s2_8_7_6_symbolic_passed_entries": [32, 32, 32],
            "s2_8_7_6_independent_points": [328, 328, 328],
            "s2_6to5_runs": 24, "s2_6to5_hits": 0,
            "theta0_minimum_unrestricted_three_qubit_cz": 5,
            "theta0_path_runs": 24, "theta0_path_hits": 0,
            "theta0_unrestricted_auxiliary_runs": 12,
            "seq91_runs": 528, "seq91_exact_returns": 443,
            "rac_checked_at": rac["checked_at"], "rac_verdict": rac["verdict"],
        },
        "attack_summaries": attack,
        "input_sha256": inputs,
        "strict_result": "MAJ严格区间仍4<=k<=7；全S²存在同一固定边序A,A,B,A,B,A与线性角公式的6-CZ L1精确构造，8/7/6-CZ各32项Q(w)残差精确归零且独立328点与theta=0端点通过；theta=0端点在unrestricted三比特图、无辅助比特模型下最小5-CZ；PATH与全S²的5-CZ及6-CZ最优性仍开放。",
        "anomaly_notes": [
            "第一诚律·异常注记1：case 5b逆平方根初次误读为-i；实际alpha=beta=gamma=w^2，逆根为w^-2。Q(w)重证后canonical与完整D残差均精确为0。",
            "第一诚律·异常注记2：端点证书曾以矩阵变量覆盖路径变量R；改名Rdiag后重跑，科学断言未放宽。",
            "第一诚律·异常注记3：6→5第二解码器曾把5-CZ raw长度误写为6-CZ的64；改为1+9*(len(edges)+1)=55，24轨保存指标与第二解码差均为0。",
            "第一诚律·异常注记4：Delta与H不是SU(2)，不能直接进入SU(2)打包器；逐门提取行列式平方根到总全局相位后再打包，未删除局部相位或放宽容差。",
            "第一诚律·异常注记5：文献case 5b实现D=H1 V H1而非V；母体首尾吸收H1后统一搜索V，已知答案门误差9.868075478780918e-16。",
            "第一诚律·异常注记6：前四边A/B突变仍保留末尾02边，初版作用域误分已纠正；PATH为24轨，另12轨只记unrestricted auxiliary，prescope汇总保留。",
            "第一诚律·异常注记7：运行秒数只留stdout，不进入确定性JSON；端点、6→5与PATH独立证书可跨冷进程逐字节一致。",
            "第一诚律·异常注记8：MAJ增权路线区分任意阶段最佳闭合电路与最终SLSQP点；ABBA/BABA自身已知门失败未通过放宽容差掩盖，改固定原电路实测双割后恢复。",
            "第一诚律·异常注记9：S²多条kick=0删门轨nfev=1且残差较大，不解释为不可能；kick=0.02后的命中只作候选，L1另由精确证书承担。",
            "第一诚律·异常注记10：8-CZ候选首次把x_core误作x_raw；按raw_indices扩展后已知门通过。010d1后台工作目录问题只属运行环境，不构成科学负结果。",
            "第一诚律·异常注记11：89d7规范吸附仅20/25网格闭合，最坏0.026129503730536907；只登记该吸附路径未闭合，不判边序不存在。",
            "第一诚律·异常注记12：一次进程全命令行诊断回显了敏感环境变量；其值未写入本报告、仓库、MANIFEST或回执，后续仅读取PID/etime/stat与日志。",
            "第一诚律·异常注记13：通用点6→5的24轨与端点PATH的24轨均零命中，只覆盖指定代表元、删门/突变和扰动；均非5-CZ不存在证明。",
            "第一诚律·异常注记14：Shende--Markov定理14使用there exists a CZ-circuit containing；最小5来自低门特殊类排除加case 5b构造，不能孤立截取成所有5门实现皆最小。",
            "第一诚律·异常注记15：RAC大差集不能用单次compare文件列表充当全量差集；使用base/head递归树并断言truncated=false，源码队列字面量不充当数值指纹。",
            "第一诚律·异常注记16：既有LM漂移、代数分支、符号超时、动态raw解码和独立目标sigma=-1等修正继续保留；本拍不把局部数值频率换名为全局几何或角刚性。",
        ],
        "open_boundaries": [
            "DEBT-MAJ-LB-01：k=4双割联合解析排除或精确构造未闭合，k=5/6未改善，区间仍4<=k<=7。",
            "DEBT-S2-CONSTRUCT-01 / DEBT-S2-6TO5-01：全S²上界已推进至6-CZ L1；5-CZ或更低构造与下界仍开放。",
            "DEBT-S2-11TO7-01：保留11→7历史lineage，但已被11→6实际超越，不抹除旧账。",
            "DEBT-S2-ENDPOINT-DIAGONAL-CLASSIFICATION-01：unrestricted theta=0最小5-CZ已闭合；PATH适用性与全S²推论仍开放。",
            "DEBT-S2-W-NORMALIZER-01：非标准W分解、跨块重合成、块级同族性与W-normalizer解释未闭合。",
            "DEBT-SEQ91-BASIN-GEOM-01：443/528仍是局部横向图有限协议频率，不是全局basin体积或测地距离。",
            "DEBT-K3-ANALYTIC-01 / DEBT-TOFFOLI-ANALYTIC-01：±pi/8目标保真角刚性仍未解决。",
            "第二套8-CZ 010d1、第二套6-CZ 89d2d0d1及7-CZ 89d2d0的L1升级与非线性自由角债务续存。",
            "RAC-COUNTERPART-NUMERIC-S-SIM：对方数值指纹未到件，跨线独立重放未启动。",
            "DEBT-FEDPAT-ROT-01、DEBT-QLVSI5-ROT-01、DEBT-QUAFU-P5-REAP-01与Sidecar授权边界续存。",
        ],
        "private_ci_consumption": 0,
        "quantum_machine_actual_consumption_seconds": 0,
        "quantum_machine_launched": False,
        "quantum_account_quota_verified": False,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad26_verify.json").write_bytes(raw)
    print(json.dumps({"status": "ALL_PASS", "children": len(children),
                      "headline": out["headline"], "sha256": sha(raw)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
