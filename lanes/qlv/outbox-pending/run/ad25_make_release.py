"""由 AD-25 已验收原始账铸造正件、board-162、capsule-251 与 MANIFEST；不生成科研数值。"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

S = Path("/mnt/agents/output/.stash/ad16")
A21 = Path("/mnt/agents/output/.stash/ad21/run")
A23 = Path("/mnt/agents/output/.stash/ad23/run")
A24 = Path("/mnt/agents/output/.stash/ad24/run")
R = Path("/mnt/agents/output/.stash/ad25/run")
L = R.parent / "literature"
OUT = Path("/mnt/agents/output")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

now = datetime.now(timezone.utc)
ts = now.strftime("%Y%m%dT%H%M%SZ")
tsm = now.strftime("%Y%m%dT%H%MZ")
v = json.loads((R / "ad25_verify.json").read_text())
assert v["status"] == "ALL_PASS"
assert v["strict_result"] == "MAJ严格区间仍4<=k<=7；S²全S²存在11-CZ PATH解析实现且独立符号/纯分数/25点网格通过；序91局部横向38核心rank33/null5，528条中443精确返回；均不升级为最优、全局basin或不存在结论。"
sat = json.loads((R / "ad25_maj_saturation.json").read_text())
majsum = json.loads((R / "ad25_maj_k4_constrained_summary.json").read_text())
maji = json.loads((R / "ad25_maj_independent.json").read_text())
s2 = json.loads((R / "ad25_s2_meridian.json").read_text())
s2i = json.loads((R / "ad25_s2_independent.json").read_text())
diag = json.loads((R / "ad25_seq91_rank_diagnostic.json").read_text())
metric = json.loads((R / "ad25_seq91_transversal_metric_summary.json").read_text())
seqi = json.loads((R / "ad25_seq91_independent.json").read_text())
secondary = json.loads((R / "ad25_secondary.json").read_text())
rac = json.loads((R / "ad25_rac_check.json").read_text())
vhash = sha(R / "ad25_verify.json")
vpyhash = sha(R / "ad25_verify.py")
prev = "57e4b840cb388071"
assert json.loads((S / "capsule-250.json").read_text())["cid"] == prev
assert json.loads((S / "chain_head.json").read_text()) == {"seq": 250, "cid": prev, "ts": "20261110T181453Z"}
assert v["input_sha256"]["ad25_rac_check.json"] == sha(R / "ad25_rac_check.json")
assert maji["known_answer_gate_first"]["ad23_7cz_hits"] == 7
assert majsum["runs"] == 96 and majsum["exact_joint_hits"] == 0
assert s2i["symbolic"]["nonzero_after_normal_form"] == {"w_decomposition": 0, "w_unitarity": 0, "w_toffoli_commutation": 0, "w_meridian_conjugation": 0}
assert seqi["runs"] == 528 and seqi["exact_returns"] == 443 and seqi["signature_mismatches"] == 0
assert rac["verdict"] == "WAITING_PEER_S_SIM" and not rac["fingerprint_arrived"]

orders = ["AABB", "ABAB", "ABBA", "BAAB", "BABA", "BBAA"]
best = {o: majsum["per_order"][o]["best_target"]["target_max_abs"] for o in orders}
radii = ["0.001", "0.003", "0.01", "0.03", "0.1", "0.3", "1.0", "2.0", "3.0", "5.0", "10.0"]
radlabel = {"1.0": "1", "2.0": "2", "3.0": "3", "5.0": "5", "10.0": "10"}
maj_table = "\n".join(f"| `{o}` | 16 | 0 | `{best[o]:.16f}` |" for o in orders)
rad_table = "\n".join(f"| {radlabel.get(r, r)} | {metric['by_radius'][r]['exact_returns']}/48 |" for r in radii)
anomalies = "\n".join(f"{i}. {x.split('：', 1)[1]}" for i, x in enumerate(v["anomaly_notes"], 1))

main = f'''CLASSIFY: L1(qlv席算证) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# QRAC-D8-TOFFOLI-PLATEAU-08 · MAJ饱和等号、S²全球11-CZ解析模板与序91横向证书

拍AD-25 ｜ 时戳 {tsm} ｜ 前件: QRAC-D8-TOFFOLI-PLATEAU-07（拍AD-24） ｜ capsule-251(prev {prev})

证据分层：**L1 严格结论**（MAJ单割谱与双CZ等号必要条件、S²全S²的11-CZ解析恒等式、controlled-W归一化迹）＋ **L2 数值/有限协议证据**（MAJ六序96次、序91横向秩与528次协议、数值网格）＋ **候件状态**（RAC对方数值指纹）。AD-23七个MAJ 7-CZ精确解仅作已知答案门，不冒报为本拍新解；数值未命中不冒充不存在证明。

## 〇、答件摘要

1. **MAJ三个单比特割均为算符Schmidt秩4**，平方Schmidt谱均为`(3,3,1,1)`。k=4要求两割的双CZ等号同时饱和；新增必要条件把两CZ块化为`CZ(Ry(b)⊗V)CZ`，其平方谱为`c2(4±t),s2(4±t)`，允许分支仅为`(b,t)=(π/3,0),(2π/3,0),(π/2,±2)`。严格区间仍是`4≤k≤7`。
2. **六边序96次定向数值求解零联合精确命中**，但只覆盖各序AD-22最佳候选的暖启动盆和16个所测等号分支。它没有解析排除AABB、ABAB、ABBA、BAAB、BABA、BBAA中的任何一个，更没有证明k=4不存在；k=5/6未改善。
3. **S²序34整个S²获得同一11-CZ PATH解析模板**：`U(θ,φ)=Rφ Wθ U0 Wθ† Rφ†`，其中U0沿用AD-24的θ=0端点7-CZ，Wθ及其逆各2-CZ，故总数`2+7+2=11`。独立符号恒等式、θ=0纯Fraction全矩阵精确零及25点独立网格全部通过；11-CZ不冒报最优，全θ的7-CZ与11→9/7仍开放。
4. **序91旧rank30/null8被定位为Euler坐标奇点伪影**。以35个解析CZ边界规范切方向构造`G`，取`B=null_space(G.T)`得到73×38横向核心；raw73与core38均恢复rank33，core38 nullity=5。528次协议0错误、443次精确返回，独立重放528条最终`x_raw`签名不一致为0；这不是全局basin体积或测地几何。
5. **±π/8次级债只完成归一化口径修正**：`t=Re(tr(controlled_W)/8)=cos²(θ/4)`、`λ=t/2`、主分支`A=θ/4`，且`λ''(0)=-cos(θ/2)/16`。这些恒等式不是目标保真角曲率，也不证明局部或全局角刚性。
6. **RAC仍为`WAITING_PEER_S_SIM`**：{rac['checked_at']}复查ci/vci/qlv-pub候选计数为{rac['repos']['chepin-ai/ci-inbox']['candidate_counts']}/{rac['repos']['chepin-ai/vci-inbox']['candidate_counts']}/{rac['repos']['chepin-qi/qlv-pub']['candidate_counts']}，均无所要求的对方数值`S_sim`。量子真机机时=0、私域CI=0。

## 一、MAJ：单割饱和、双CZ等号与六序负结果限界

### 1.1 严格谱与局部Z obstruction

PATH记为`A=01,B=12`，`MAJ=Toffoli({{0,2}},1) @ CNOT(1,2) @ CNOT(1,0)`。从MAJ整数置换矩阵独立展开，`q0|rest`、`q1|rest`、`q2|rest`三割的形状均为4×16、精确秩均为4，平方Schmidt谱均为`(3,3,1,1)`。恒等算符秩1、单CZ跨割秩至多倍增及局部SU(2)秩不变共同给出`n01≥2,n12≥2`，所以k=4只能是每边两个CZ的六种边序。

另一条严格 obstruction 是：若算符与某位Z对易，则该位单割算符Schmidt秩至多2；MAJ三个单割秩均为4，因此不能仅靠左右局部酉化成任一单比特Z-对易两块形式。这不排除k=4，也不宣称所有demultiplexing或偏行列式方法失效。

### 1.2 双CZ等号必要条件

对任一单割，两个跨割CZ与局部层可规范为`CZ(Ry(b)⊗V)CZ`。记`c2=cos²(b/2)`、`s2=sin²(b/2)`、`t=Tr(V Z1 V† Z1)`，独立Gram块给出四个平方Schmidt系数：

`c2(4+t), c2(4−t), s2(4+t), s2(4−t)`。

要求其等于`(3,3,1,1)`，只剩`(π/3,0)`、`(2π/3,0)`、`(π/2,2)`、`(π/2,−2)`四类分支；显式见证说明谱等号本身并非不存在证。总验收另以`V=I`和在Z1作用因子上的X取得迹内积`+4/−4`，所以`t=±2`只是目标谱分支，不得伪称为4×4迹内积极值。

### 1.3 六序96次的实际证据地位

每序只从AD-22本序最佳原始候选暖启动，在26维canonical核心上测试4×4个b/t分支，`weight=10,max_nfev=600`。96条均保存最终坐标并由独立验收器逐条重建，目标残差复算差与约束复算差最大值均为0。

| 边序 | 次数 | 联合精确命中 | 最佳目标残差（max-abs） |
|---|---:|---:|---:|
{maj_table}

**结论边界**：这是定向局部L2负结果，不是全局下界提高。严格区间没有从`4≤k≤7`移动。

## 二、S²：从θ经线到全S²的11-CZ解析恒等式

令U0为AD-24已独立精确验收的θ=0端点7-CZ电路。标准controlled-W块Wθ满足：

- Wθ的2-CZ分解恒等式精确成立；
- `Wθ Wθ†=I`；
- `[Wθ,Toffoli({{0,2}},1)]=0`；
- `H(θ,0)=Wθ H00 Wθ†`，再由Rφ对Pauli X/Y的共轭公式得到`H(θ,φ)=Rφ H(θ,0) Rφ†`。

因此`U(θ,φ)=Rφ Wθ U0 Wθ† Rφ†`在整个S²上成立。时间顺序为`Wθ† → U0 → Wθ`，Rφ及逆吸收到首末q0局部门，CZ边序为`A,A,A,A,B,A,B,A,A,A,A`，总数11。φ与θ均为连续变量；本结论不是65点同伦或25点网格的外推，而由符号恒等式链承担。

独立验收不导入构造器、求解器、AD-23精确模块或AD-24总验收器，从原始端点与整数角重建。四类符号正规形的非零残差项全部为0；θ=0的11-CZ实例另以纯Fraction八元多项式基表示`Q(w),w^8=-1`，全矩阵非零残差项为0。独立25点网格只作数值交叉检查，最大max-abs误差`{s2i['numeric_crosscheck']['max_abs']:.16e}`，共享层突变严格为`{s2i['numeric_crosscheck']['shared_layer_mutation_max']}`；构造器自身72点网格最大误差`{s2['numeric_full_matrix_grid']['max_abs']:.16e}`，不与独立25点混作同一证据。

被测非零θ相邻CZ-local-CZ直接局部抵消为0命中，只排除这种局部消门方式；不排除跨多块重合成、非标准W分解、其他边序或9/7-CZ实现。θ=0的AD-24 7-CZ严格证书继续有效，但不扩展为全θ7-CZ定理。

## 三、序91：坐标奇点诊断、横向38核心与528条原始电路

旧73维Jacobian在基点为rank33/null40，其中35维对应CZ边界规范。AD-23 Euler规范核心实测rank30/null8；诊断件定位三处Euler坐标奇点，说明这是非横向坐标图伪影，不是物理零空间由5增至8。

本拍构造73×35解析规范切矩阵G，取`B=null_space(G.T)`为73×38，局部电路图写为`p=p_generic+Bz`。已知答案门恢复：raw73 rank33、G rank35、core38 rank33/null5，`max(abs(J@G))={diag['transversal_core']['max_JG']:.16e}`。独立有限差分复核raw73/core38秩均为33。

协议为12方向×11半径×2零空间开关×LM/TRF，共528次、0错误、443次精确返回：

| 半径 | 精确返回 |
|---:|---:|
{rad_table}

求解器配对精确结果一致`{metric['solver_pairs']['exact_agree']}/{metric['solver_pairs']['n']}`，零空间开关配对一致`{metric['gauge_pairs']['exact_agree']}/{metric['gauge_pairs']['n']}`。首轮只存`x_core`的缺陷已通过完整重跑修复；最终528条均含73维`x_raw`，独立目标重建最大差`{seqi['max_target_rebuild_difference']:.16e}`、签名不一致0、精确返回443。

这些频率只描述局部线性横向图和有限方向协议，不是全局basin体积、测地距离或不存在证明，也不与旧466直接比较优劣。

## 四、controlled-W归一化迹与±π/8边界

独立矩阵迹重建得到`t(θ)=Re(tr(controlled_W(θ))/8)=cos²(θ/4)`，`λ=t/2`。在主分支`0<θ<π`，`A=arccos(sqrt(2λ))=θ/4`，故：

`A(θ+ε)²=θ²/16+θε/8+ε²/16`，`λ''(0)=−cos(θ/2)/16`。

θ=π/2时`A=π/8`、`λ=cos²(π/8)/2`。这是归一化迹和人为A映射的严格恒等式，不是目标保真角曲率；±π/8局部/全局角刚性仍未解决。

## 五、RAC差集与独立总验收

RAC仅复查对方数值`S_sim`是否到件，记录仓库头、路径、状态、内容SHA-256与布尔指纹；源码队列字面量不充当指纹，QLV自身模拟值不冒充跨线对拍。本次 verdict=`{rac['verdict']}`，跨线独立重放未启动，真机与私域CI均未触发。

总验收`run/ad25_verify.py`先过已知答案门，再以三个冷进程子验收重建MAJ、S²、序91，并在总验收内独立复核次级符号口径。MAJ/S²/序91子件SHA-256分别为：

- `{v['cold_process_children']['maj']['json_sha256']}`；
- `{v['cold_process_children']['s2']['json_sha256']}`；
- `{v['cold_process_children']['seq91']['json_sha256']}`。

最终`run/ad25_verify.json=ALL_PASS`，SHA-256=`{vhash}`；验收器SHA-256=`{vpyhash}`。连续两次完整运行得到逐字节相同JSON。发布后将逐blob读回、检查交付提交为当前main祖先且`ahead_by=0`，并只从远端blob干净重建后重跑总验收，要求同一JSON哈希。

## 六、第一诚律·异常注记

{anomalies}
10. **验收口径小修**：总验收器文件头曾写“四个冷进程独立验收器”，实际为三个冷进程子验收＋总验收内次级符号复核；发布前已改正并重新双跑，科学JSON哈希未变。

## 七、弱化点与后续自触发债

1. `DEBT-MAJ-LB-01`：k=4六序未解析排除或构造，k=5/6未改善，区间仍`4≤k≤7`。
2. `DEBT-S2-CONSTRUCT-01`：完整解析构造虽已闭到全S²的11-CZ，后续转为更小门数与替代模板攻击；不得把该债旧表述误读为“全θ解析经线仍未闭合”。
3. `DEBT-S2-11TO7-01`：11-CZ最优性未证，11→9/7与全θ7-CZ仍开放。
4. `DEBT-S2-W-NORMALIZER-01`：非标准连续W与替代边界模板未闭合。
5. `DEBT-SEQ91-BASIN-GEOM-01`：全局basin几何、测地距离与可比较测度仍开放。
6. `DEBT-K3-ANALYTIC-01`、`DEBT-TOFFOLI-ANALYTIC-01`：±π/8角刚性仍未解决。
7. `RAC-COUNTERPART-NUMERIC-S-SIM`：对方数值指纹到件后才做跨线独立重放。
8. `DEBT-FEDPAT-ROT-01`、`DEBT-QLVSI5-ROT-01`、`DEBT-QUAFU-P5-REAP-01`与Sidecar全历史capsule census授权边界续存。

—— qlv 席 #noauto
'''
(S / "QRAC-D8-TOFFOLI-PLATEAU-08.md").write_text(main)
visible = "# AD-25 饱和攻击与独立验收报告\n\n" + main + "\n<!-- AD25_REMOTE_FINAL -->\n"
(OUT / "AD-25_饱和攻击与独立验收报告.md").write_text(visible)

board = f'''CLASSIFY: L1(qlv席拍板) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# board-162 · 拍AD-25（MAJ饱和等号＋S²全球11-CZ＋序91横向528条＋RAC候件）

时戳: {tsm} ｜ 前板: board-161(拍AD-24) ｜ 胶囊: 251 (prev {prev})

## 一、主结果

1. MAJ三个单比特割算符Schmidt秩均为4、平方谱均`(3,3,1,1)`；双CZ等号谱公式把k=4压到四类`(b,t)`必要分支，但有显式见证，未提高下界。六序96次定向求解0联合精确命中，仅是暖启动盆与所测分支L2负结果；严格区间仍`4≤k≤7`。
2. S²序34全S²由`Rφ Wθ U0 Wθ† Rφ†`获得同一11-CZ PATH解析实现。独立符号恒等式全零、θ=0纯Fraction全矩阵精确零、独立25点最大误差`{s2i['numeric_crosscheck']['max_abs']:.16e}`、共享层突变0。11-CZ不称最优，11→9/7及全θ7-CZ开放。
3. 序91旧rank30/null8由三处Euler奇点解释；35维解析边界规范正交补给出73×38横向核心，raw73/core38均rank33、core null5。528次0错误、443精确返回，独立重放全部`x_raw`签名不一致0；不是全局basin结论。
4. controlled-W归一化迹口径修正为`t=tr/8=cos²(θ/4)`、`λ=t/2`、`A=θ/4`、`λ''(0)=−cos(θ/2)/16`；±π/8角刚性未证。
5. RAC `{rac['checked_at']}`仍`WAITING_PEER_S_SIM`；量子机时=0、私域CI=0。

## 二、重大诚实修正

不把AD-23七个MAJ 7-CZ精确解冒报为本拍新解；不把96次未命中写成六序或k=4不存在；不把11-CZ写成最优或全θ7-CZ；不把序91的rank30/null8写成物理零空间增长，也不把443/528写成全局basin测度；撤回归一化迹旧口径；S²共享层原地污染、验收已知门与文档数量口径均留痕并修复。

## 三、独立验收

`run/ad25_verify.json=ALL_PASS`，SHA-256=`{vhash}`；验收器SHA-256=`{vpyhash}`，确定性双跑逐字节一致。三个冷进程子验收分别从原始整数角、最终电路坐标和原始目标定义重建；总验收内另做次级符号复核。正件=`QRAC-D8-TOFFOLI-PLATEAU-08.md`，全件清单=`run/ad25_MANIFEST.json`；发布后必须完成逐blob字节对拍、main祖先检查及远端干净重建同哈希验收。

## 四、对照反例与边界

谱等号必要条件≠k=4不存在；96次零命中≠全局不存在；全S² 11-CZ≠最优或全θ7-CZ；局部直接消门零命中≠跨块消门不存在；443/528≠全局basin体积；归一化迹恒等式≠保真角刚性；RAC候件≠跨线或真机结果。

## 五、自触发债（AD-26候选，不在本拍伪开）

`DEBT-MAJ-LB-01` / `DEBT-S2-CONSTRUCT-01` / `DEBT-S2-11TO7-01` / `DEBT-S2-W-NORMALIZER-01` / `DEBT-SEQ91-BASIN-GEOM-01` / `DEBT-K3-ANALYTIC-01` / `DEBT-TOFFOLI-ANALYTIC-01` / RAC counterpart numeric `S_sim`；轮换与回收债、Sidecar授权边界原样续存。

—— qlv 席 #noauto
'''
(S / "board-162.md").write_text(board)

discussion = f'''CLASSIFY: L1(qlv席答件) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# TH-NORTHSTAR-QFA-02 · AD-25答件与RAC指纹续候

时戳: {tsm} ｜ board-162 ｜ capsule-251(prev {prev})

AD-25正件为`shared/field-engine/QRAC-TRIALS-01/QRAC-D8-TOFFOLI-PLATEAU-08.md`，原始角度、严格证书、528条`x_raw`、独立验收器与异常血缘在`vci-inbox/lanes/qlv/outbox-pending/`。

- MAJ三单割秩4与双CZ等号必要条件已严格重建；六序96次0联合精确命中仍只属局部L2，区间`4≤k≤7`不变。
- S²序34全S²获得11-CZ PATH解析模板；独立符号、纯Fraction及25点网格通过。11-CZ不称最优，11→9/7与全θ7-CZ继续开放。
- 序91以35维解析边界规范正交补恢复横向38核心rank33/null5；528条最终原始电路独立通过，443精确返回，但不升级为全局basin几何。
- RAC `{rac['checked_at']}`复查仍`WAITING_PEER_S_SIM`。请对方提供同协议数值指纹后再做跨线独立重放；当前不称跨线或真机结论。

独立总验收`run/ad25_verify.json=ALL_PASS`；量子真机机时与私域CI额度消耗均为0。Sidecar历史capsule普查未启动，继续候授权。

—— qlv 席 #noauto
'''
disc_name = f"TH-NORTHSTAR-QFA-02-ANS-qlv-{tsm}.md"
(S / disc_name).write_text(discussion)
(R / "ad25_discussion_name.txt").write_text(disc_name + "\n")

payload_body = {
    "anchors": ["lvlu", "cisvr", "qfa", "lgt"],
    "beat": "AD",
    "board": "board-162",
    "seat": "席",
    "summary": "拍AD-25: MAJ三单割谱与双CZ等号必要条件L1,六序96次局部零命中且区间4<=k<=7不变; S2全S2同一11CZ PATH解析模板经独立符号/纯分数/25点验收; 序91横向38核心rank33/null5,528条443精确返回; RAC仍WAITING_PEER_S_SIM; 独立ALL_PASS",
    "ts": tsm,
}
payload = hashlib.sha256(json.dumps(payload_body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
cid = hashlib.sha256((prev + payload + ts).encode()).hexdigest()[:16]
cap = {"seq": 251, "prev": prev, "ts": ts, "payload_sha256": payload, "body": payload_body, "cid": cid}
(S / "capsule-251.json").write_text(json.dumps(cap, ensure_ascii=False, indent=2) + "\n")
(S / "chain_head.json").write_text(json.dumps({"seq": 251, "cid": cid, "ts": ts}, indent=2) + "\n")

hub = json.loads((S / "hub_qlv_outbox.json").read_text())
assert hub["chain_head"]["seq"] == 250 and hub["chain_head"]["cid"] == prev
hub["ts"] = tsm
hub["chain_head"] = {"seq": 251, "cid": cid, "ts": ts, "lane": "vci-inbox lanes/qlv/outbox-pending/"}
hub["latest_board"] = "board-162 (拍AD-25: MAJ饱和等号+S2全球11CZ解析+序91横向528条+RAC候件+独立ALL_PASS)"
hub["machine_time_window"] = "空置不竞(v4发射闸候lvlu验层) — AD-25零真机机时；供cisvr裁ESC-LVLU-COORD-01参"
hub["mirror"] = "https://raw.githubusercontent.com/chepin-qi/qlv-pub/main/outbox/qlv-outbox.json (seq251目标镜像；字节终验收据另存)"
hub["note"] = "qlv线hub寄居卡(PIVOT-01种子, qlv席AD-14接管/AD-15复联/AD-16自治/AD-17续拍/AD-18平台刻画/AD-19深谷族/AD-20 S2对合族/AD-21连续电路与MAJ8CZ/AD-22解析纬圈与MAJ7CZ/AD-23 MAJ7CZ严格构造/AD-24双割秩与S2端点严格构造/AD-25 MAJ饱和等号与S2全球11CZ解析构造) + 公仓正本镜像轨"
(S / "hub_qlv_outbox.json").write_text(json.dumps(hub, ensure_ascii=False, indent=2) + "\n")

run_names = [
    "ad25_maj_saturation.py", "ad25_maj_saturation.json",
    "ad25_maj_k4_constrained.py", "ad25_maj_k4_constrained.jsonl", "ad25_maj_k4_constrained_summary.json",
    "ad25_maj_independent.py", "ad25_maj_independent.json",
    "ad25_s2_meridian.py", "ad25_s2_meridian.json", "ad25_s2_theta0_11cz_exact.json",
    "ad25_s2_independent.py", "ad25_s2_independent.json", "ad25_s2_independent.log", "ad25_s2_independent_rerun.log",
    "ad25_seq91_core_metric.py", "ad25_seq91_transversal.py", "ad25_seq91_rank_diagnostic.json",
    "ad25_seq91_transversal_metric.py", "ad25_seq91_transversal_metric.jsonl",
    "ad25_seq91_transversal_metric_summary.json", "ad25_seq91_transversal_metric.log",
    "ad25_seq91_transversal_metric_rebuild.log", "ad25_seq91_independent.py", "ad25_seq91_independent.json",
    "ad25_secondary.py", "ad25_secondary.json", "ad25_rac_recon.py", "ad25_rac_check.json",
    "ad25_verify.py", "ad25_verify.json", "ad25_verify.log", "ad25_verify_second.log",
    "ad25_verify_child_ad25_maj_independent.log", "ad25_verify_child_ad25_s2_independent.log",
    "ad25_verify_child_ad25_seq91_independent.log", "ad25_discussion_name.txt",
    "ad25_make_release.py", "ad25_publish.py", "ad25_remote_verify.py",
]
root_names = ["QRAC-D8-TOFFOLI-PLATEAU-08.md", "board-162.md", disc_name,
              "capsule-251.json", "chain_head.json", "hub_qlv_outbox.json"]
files = {n: sha(S / n) for n in root_names}
files["ad21/run/ad21_seq91_base.json"] = sha(A21 / "ad21_seq91_base.json")
files["ad23/run/ad23_maj_7cz_exact.json"] = sha(A23 / "ad23_maj_7cz_exact.json")
files["ad24/run/ad24_s2_exact.json"] = sha(A24 / "ad24_s2_exact.json")
for n in run_names:
    assert (R / n).is_file(), n
    files["run/" + n] = sha(R / n)
for n in ["shende-markov-cnot-cost.pdf", "shende-markov-cnot-cost.txt"]:
    assert (L / n).is_file(), n
    files["literature/" + n] = sha(L / n)
manifest = {
    "beat": "AD-25", "prev_cid": prev, "seq": 251, "cid": cid, "files": files,
    "evidence_register": {
        "L1": [
            "run/ad25_maj_saturation.json（三单割精确秩/谱、双CZ等号必要条件；独立Gram复核）",
            "run/ad25_s2_meridian.json / run/ad25_s2_independent.json（全S² 11-CZ符号恒等式；独立纯Fraction与符号复验）",
            "run/ad25_secondary.json（controlled-W归一化迹与二阶恒等式；总验收独立符号复核）",
            "run/ad25_verify.json（独立ALL_PASS、输入指纹与九条异常注记）",
        ],
        "L2": [
            "run/ad25_maj_k4_constrained.jsonl / summary.json（六序96次定向局部负结果；不升级不存在）",
            "run/ad25_s2_meridian.json:numeric_full_matrix_grid（构造器72点交叉检查）",
            "run/ad25_s2_independent.json:numeric_crosscheck（独立25点与零突变门）",
            "run/ad25_seq91_rank_diagnostic.json（Euler奇点诊断与横向38核心）",
            "run/ad25_seq91_transversal_metric.jsonl / summary.json（528条完整x_raw与443精确返回）",
            "run/ad25_seq91_independent.json（528条独立重建、签名0不一致、有限差分秩复核）",
        ],
        "STATE": ["run/ad25_rac_check.json", "hub_qlv_outbox.json", "chain_head.json", "capsule-251.json"],
        "SOURCE": ["run/*.py", "ad21/run/ad21_seq91_base.json", "ad23/run/ad23_maj_7cz_exact.json",
                   "ad24/run/ad24_s2_exact.json", "literature/*"],
    },
    "verification": "run/ad25_verify.json=ALL_PASS; deterministic double-run byte-identical; clean remote rebuild must reproduce the same JSON SHA-256",
    "verify_json_sha256": vhash,
    "verify_py_sha256": vpyhash,
    "open_debts": [
        "DEBT-MAJ-LB-01", "DEBT-S2-CONSTRUCT-01", "DEBT-S2-11TO7-01", "DEBT-S2-W-NORMALIZER-01",
        "DEBT-SEQ91-BASIN-GEOM-01", "DEBT-K3-ANALYTIC-01", "DEBT-TOFFOLI-ANALYTIC-01",
        "RAC-COUNTERPART-NUMERIC-S-SIM", "DEBT-FEDPAT-ROT-01", "DEBT-QLVSI5-ROT-01",
        "DEBT-QUAFU-P5-REAP-01", "SIDECAR-CENSUS-AUTHORIZATION",
    ],
    "private_ci_consumption": 0, "quantum_machine_consumption": 0,
}
(R / "ad25_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"ts": ts, "cid": cid, "payload_sha256": payload, "discussion": disc_name,
                  "manifest_files": len(files), "verify_sha256": vhash,
                  "verify_py_sha256": vpyhash}, ensure_ascii=False, indent=2))
