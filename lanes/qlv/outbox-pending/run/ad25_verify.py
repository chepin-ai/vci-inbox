"""AD-25 总独立验收：三个冷进程子验收＋总验收内次级符号复核。

不导入任何构造器、求解器、横向核心分析模块或旧总验收器。
子验收只从原始整数角、最终电路坐标和原始目标定义重建。
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import sympy as sp

R = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()


def known_answer_gate():
    """已知答案必须先于未知目标；显式拒绝两条曾误用的捷径。"""
    # t=Tr(V Z1 V† Z1) 在4×4酉矩阵上的极值是±4，不是±2。
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.diag([1, -1]).astype(complex)
    Z1 = np.kron(I2, Z)
    vals = []
    for V in (np.eye(4, dtype=complex), np.kron(I2, X)):
        vals.append(float(np.trace(V @ Z1 @ V.conj().T @ Z1).real))
    assert vals == [4.0, -4.0]

    # 归一化迹 t=tr(W)/8；旧的“再除2充当t”口径必须被拒绝。
    th = np.pi / 8
    t = np.cos(th / 4) ** 2
    wrong_t = t / 2
    assert abs(t - 0.9903926402016152) < 1e-15
    assert t - wrong_t > 0.49
    lam = t / 2
    A = np.arccos(np.sqrt(2 * lam))
    assert abs(A - th / 4) < 1e-15
    return {
        "trace_inner_product_witnesses": vals,
        "trace_inner_product_extrema": [-4, 4],
        "normalized_trace_at_pi_over_8": t,
        "wrong_extra_halving_rejected_by": t - wrong_t,
        "angle_from_lambda": A,
    }


def verify_maj_gram_independently():
    """独立重建双CZ等号引理的Gram块及允许谱分支。"""
    c2, s2, t = sp.symbols("c2 s2 t", real=True)
    G = sp.Matrix([[4*c2, 0, 0, c2*t],
                   [0, 4*s2, -s2*t, 0],
                   [0, -s2*t, 4*s2, 0],
                   [c2*t, 0, 0, 4*c2]])
    ev0 = {sp.expand(k): v for k, v in G[[0, 3], [0, 3]].eigenvals().items()}
    ev1 = {sp.expand(k): v for k, v in G[[1, 2], [1, 2]].eigenvals().items()}
    assert ev0 == {sp.expand(c2*(4+t)): 1, sp.expand(c2*(4-t)): 1}
    assert ev1 == {sp.expand(s2*(4+t)): 1, sp.expand(s2*(4-t)): 1}
    branches = []
    for name, cv, sv, tv in (("pi/3,t0", sp.Rational(3, 4), sp.Rational(1, 4), 0),
                              ("2pi/3,t0", sp.Rational(1, 4), sp.Rational(3, 4), 0),
                              ("pi/2,t+2", sp.Rational(1, 2), sp.Rational(1, 2), 2),
                              ("pi/2,t-2", sp.Rational(1, 2), sp.Rational(1, 2), -2)):
        spectrum = sorted([cv*(4+tv), cv*(4-tv), sv*(4+tv), sv*(4-tv)], reverse=True)
        assert spectrum == [3, 3, 1, 1]
        branches.append({"branch": name, "squared_schmidt": [int(x) for x in spectrum]})
    return {"gram_block_eigenvalues_exact": True, "allowed_branch_witnesses": branches,
            "scope": "必要条件与显式谱见证，不是k=4不存在证明。"}


def verify_controlled_trace_independently():
    """用独立SymPy矩阵迹重建归一化恒等式，不读取secondary的数值中间量。"""
    c, s = sp.symbols("c s", real=True)
    i = sp.I
    I = sp.eye(2)
    X = sp.Matrix([[0, 1], [1, 0]])
    U = c*I + i*s*X
    pp, pm = (I+X)/2, (I-X)/2

    def op(q, A):
        ms = [I, I, I]
        ms[q] = A
        return sp.kronecker_product(ms[0], ms[1], ms[2])

    W = op(1, pm) + op(1, pp)*op(0, U)
    normalized = sp.expand(sp.trace(W)/8)
    assert sp.simplify(normalized-(1+c)/2) == 0  # c=cos(theta/2)
    theta, eps = sp.symbols("theta eps", real=True)
    exact_t = sp.cos(theta/4)**2
    assert sp.simplify(sp.expand_trig(exact_t)-(1+sp.cos(theta/2))/2) == 0
    lam = sp.cos((theta+eps)/4)**2/2
    angle_squared = ((theta+eps)/4)**2
    coeffs = [sp.expand(angle_squared).coeff(eps, n) for n in range(3)]
    assert coeffs == [theta**2/16, theta/8, sp.Rational(1, 16)]
    assert sp.simplify(sp.diff(lam, eps, 2).subs(eps, 0) + sp.cos(theta/2)/16) == 0
    return {
        "symbolic_trace_over_8": "(1+cos(theta/2))/2 = cos(theta/4)^2",
        "lambda": "t/2",
        "A_squared_epsilon_coefficients": [str(x) for x in coeffs],
        "lambda_second_at_epsilon_zero": "-cos(theta/2)/16",
        "known_theta_pi_over_2": {"A": "pi/8", "lambda": "cos(pi/8)^2/2"},
        "boundary": "不是目标保真角曲率，不证明±pi/8局部或全局角刚性。",
    }


def run_child(script, output_name, expected_status):
    output = R / output_name
    if output.exists():
        output.unlink()  # 防止把陈旧通过件当本次运行结果。
    proc = subprocess.run([sys.executable, str(R / script)], cwd=R,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=900, check=False)
    log = R / ("ad25_verify_child_" + Path(script).stem + ".log")
    log.write_bytes(proc.stdout)
    assert proc.returncode == 0, (script, proc.returncode, proc.stdout[-2000:].decode(errors="replace"))
    raw = output.read_bytes()
    doc = json.loads(raw)
    assert doc["status"] == expected_status, (script, doc["status"])
    return doc, {"script": script, "output": output_name, "returncode": proc.returncode,
                 "stdout_sha256": sha(proc.stdout), "json_sha256": sha(raw)}


def main():
    gate = known_answer_gate()
    gram = verify_maj_gram_independently()
    trace = verify_controlled_trace_independently()

    children = {}
    maj, children["maj"] = run_child("ad25_maj_independent.py", "ad25_maj_independent.json",
                                     "MAJ_AD25_INDEPENDENT_L1_L2_PASS")
    s2, children["s2"] = run_child("ad25_s2_independent.py", "ad25_s2_independent.json",
                                   "S2_FULL_SPHERE_11CZ_INDEPENDENT_L1_PASS")
    seq, children["seq91"] = run_child("ad25_seq91_independent.py", "ad25_seq91_independent.json",
                                       "SEQ91_528_RAW_CIRCUITS_INDEPENDENT_PASS")

    assert maj["known_answer_gate_first"]["ad23_7cz_hits"] == 7
    assert maj["numeric96"]["runs"] == 96 and maj["numeric96"]["exact_joint_hits"] == 0
    assert maj["strict_interval"] == "4 <= k <= 7"
    saturation = json.loads((R / "ad25_maj_saturation.json").read_text())
    assert saturation["status"] == "MAJ_SINGLE_CUT_SATURATION_AND_TWO_CZ_EQUALITY_L1_PASS"
    assert all(v["rank"] == 4 for v in saturation["single_qubit_cuts"].values())

    assert s2["theta0_exact"]["nonzero_residual_entries"] == 0
    assert s2["theta0_exact"]["cz_count"] == 11
    assert all(v == 0 for v in s2["symbolic"]["nonzero_after_normal_form"].values())
    assert s2["numeric_crosscheck"]["points"] == 25
    assert s2["numeric_crosscheck"]["shared_layer_mutation_max"] == 0.0
    assert s2["numeric_crosscheck"]["max_abs"] < 2e-10

    assert seq["runs"] == 528 and seq["exact_returns"] == 443
    assert seq["signature_mismatches"] == 0
    assert seq["finite_difference_rank_check"]["raw73_rank"] == 33
    assert seq["finite_difference_rank_check"]["core38_rank"] == 33
    assert seq["finite_difference_rank_check"]["core38_nullity"] == 5
    diag = json.loads((R / "ad25_seq91_rank_diagnostic.json").read_text())
    assert diag["transversal_core"]["gauge_tangent_rank"] == 35
    assert diag["transversal_core"]["max_JG"] < 1e-12
    metric = json.loads((R / "ad25_seq91_transversal_metric_summary.json").read_text())
    assert metric["runs"] == 528 and metric["errors"] == 0
    assert metric["gauge_pairs"]["n"] == metric["solver_pairs"]["n"] == 264

    secondary = json.loads((R / "ad25_secondary.json").read_text())
    assert secondary["status"] == "CONTROLLED_W_NORMALIZED_TRACE_SECOND_ORDER_L1_PASS"
    assert secondary["trace_identity_max_error"] < 1e-12
    assert secondary["debts"] == ["DEBT-TOFFOLI-ANALYTIC-01"]

    rac = json.loads((R / "ad25_rac_check.json").read_text())
    assert rac["verdict"] == "WAITING_PEER_S_SIM" and not rac["fingerprint_arrived"]
    assert rac["private_ci_consumption"] == rac["quantum_machine_consumption"] == 0
    assert all(not item["has_numeric_S_sim"] for repo in rac["repos"].values() for item in repo["candidates"])
    assert all(not item.get("queue_only", False) for repo in rac["repos"].values()
               for item in repo["candidates"] if item.get("source_code_excluded_from_fingerprint"))

    files = [
        "ad25_maj_saturation.json", "ad25_maj_k4_constrained.jsonl",
        "ad25_maj_k4_constrained_summary.json", "ad25_maj_independent.json",
        "ad25_s2_meridian.json", "ad25_s2_theta0_11cz_exact.json", "ad25_s2_independent.json",
        "ad25_seq91_rank_diagnostic.json", "ad25_seq91_transversal_metric.jsonl",
        "ad25_seq91_transversal_metric_summary.json", "ad25_seq91_independent.json",
        "ad25_secondary.json", "ad25_rac_check.json",
    ]
    out = {
        "beat": "AD-25", "status": "ALL_PASS",
        "known_answer_gate_first": gate,
        "maj_gram_independent": gram,
        "controlled_trace_independent": trace,
        "cold_process_children": children,
        "headline": {
            "maj_interval": "4 <= k <= 7", "maj_k4_runs": 96, "maj_k4_joint_hits": 0,
            "s2_full_sphere_cz": 11, "s2_numeric_points": 25,
            "s2_numeric_max_abs": s2["numeric_crosscheck"]["max_abs"],
            "seq91_runs": 528, "seq91_exact_returns": 443,
            "seq91_raw73_rank": 33, "seq91_core38_rank": 33, "seq91_core38_nullity": 5,
            "rac_verdict": rac["verdict"],
        },
        "input_sha256": {name: sha((R / name).read_bytes()) for name in files},
        "strict_result": "MAJ严格区间仍4<=k<=7；S²全S²存在11-CZ PATH解析实现且独立符号/纯分数/25点网格通过；序91局部横向38核心rank33/null5，528条中443精确返回；均不升级为最优、全局basin或不存在结论。",
        "anomaly_notes": [
            "第一诚律·异常注记1：AD-23 Euler规范核心在基点实测rank30/null8；三处Euler奇点导致非横向图伪影，未写成物理零空间由5增至8。新建35维精确边界规范正交补后恢复rank33/null5。",
            "第一诚律·异常注记2：首轮528条只保存x_core，不能让独立验收摆脱横向基；完整重跑528条并补存73维x_raw，443个精确返回保持不变。",
            "第一诚律·异常注记3：序91独立目标初版漏掉sigma=-1分支，已知答案门拒绝后修复；最终528条签名不一致为0。",
            "第一诚律·异常注记4：撤回以未归一化迹导数冒充保真角曲率及cos^2(theta/2)/2旧口径；现仅保留t=Re(tr(W)/8)=cos^2(theta/4)、lambda=t/2与A=theta/4的可证恒等式。",
            "第一诚律·异常注记5：t=±2不是4×4迹内积极值；V=I与在Z1作用因子上的X分别给出±4，未把谱等号条件伪化为V与Z对易。总验收初版把X误放到对易因子时被已知门拒绝，改正反交换因子后才放行。",
            "第一诚律·异常注记6：MAJ六序96次定向求解0联合精确命中，只覆盖暖启动盆和所测分支，未写成六序或k=4全局不存在证明。",
            "第一诚律·异常注记7：S²独立验收初版H00漏Z2且Fraction矩阵累加有误；修复并以H00对合、17个三角已知答案门复验，失败运行不记通过。",
            "第一诚律·异常注记8：S²数值网格曾把φ门原地写回W/W†共享层，导致首点后污染并在(theta=pi/11,phi=-0.83)出现0.10519701069149003；改为纯复制拼接，新增W/W†已知门与零突变门，25点最大误差1.5788995281571398e-15。",
            "第一诚律·异常注记9：RAC源码队列字面量不充当对方数值指纹；本次三仓候选均无数值S_sim，维持WAITING_PEER_S_SIM。",
        ],
        "open_boundaries": [
            "DEBT-MAJ-LB-01：k=4六序未解析排除或构造，k=5/6未改善，区间仍4<=k<=7。",
            "DEBT-S2-CONSTRUCT-01与DEBT-S2-11TO7-01：11-CZ不冒报最优；11到9/7及全theta 7-CZ仍开放。",
            "DEBT-S2-W-NORMALIZER-01：非标准连续W与替代边界模板未闭合。",
            "DEBT-SEQ91-BASIN-GEOM-01：443/528是局部线性横向图和有限方向协议频率，不是全局basin体积、测地距离或旧466的可比优劣。",
            "DEBT-K3-ANALYTIC-01与DEBT-TOFFOLI-ANALYTIC-01：±pi/8角刚性仍未解决。",
            "RAC-COUNTERPART-NUMERIC-S-SIM：对方数值指纹未到件，跨线独立重放未启动。",
            "DEBT-FEDPAT-ROT-01、DEBT-QLVSI5-ROT-01、DEBT-QUAFU-P5-REAP-01与Sidecar授权边界续存。",
        ],
        "private_ci_consumption": 0, "quantum_machine_consumption": 0,
    }
    raw = json.dumps(out, ensure_ascii=False, indent=2).encode() + b"\n"
    (R / "ad25_verify.json").write_bytes(raw)
    print(json.dumps({"status": out["status"], "children": children,
                      "headline": out["headline"], "sha256": sha(raw)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
