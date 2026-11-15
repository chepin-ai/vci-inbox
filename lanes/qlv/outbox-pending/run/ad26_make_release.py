"""由 AD-26 已验收原始账铸造正件、board-163、capsule-252 与 MANIFEST；不生成科研数值。"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

S = Path("/mnt/agents/output/.stash/ad16")
A21 = Path("/mnt/agents/output/.stash/ad21/run")
A22 = Path("/mnt/agents/output/.stash/ad22/run")
A23 = Path("/mnt/agents/output/.stash/ad23/run")
A24 = Path("/mnt/agents/output/.stash/ad24/run")
A25 = Path("/mnt/agents/output/.stash/ad25/run")
R = Path("/mnt/agents/output/.stash/ad26/run")
OUT = Path("/mnt/agents/output")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())

now = datetime.now(timezone.utc)
ts = now.strftime("%Y%m%dT%H%M%SZ")
tsm = now.strftime("%Y%m%dT%H%MZ")
v = load(R / "ad26_verify.json")
assert v["status"] == "ALL_PASS" and len(v["cold_process_children"]) == 16
assert v["headline"]["s2_full_sphere_exact_cz"] == 6
assert v["headline"]["theta0_minimum_unrestricted_three_qubit_cz"] == 5
assert v["headline"]["maj_k4_protocol_runs"] == 48
prev = "297413d2702bd02b"
assert load(S / "capsule-251.json")["cid"] == prev
assert load(S / "chain_head.json") == {"seq": 251, "cid": prev, "ts": "20261110T205001Z"}
assert (R / "ad26_verify.run1.json").read_bytes() == (R / "ad26_verify.json").read_bytes()
vhash = sha(R / "ad26_verify.json")
vpyhash = sha(R / "ad26_verify.py")
maj = load(R / "ad26_maj_k4_independent_summary.json")
ind = {k: load(R / f"ad26_s2_independent{k}_{stem}_summary.json")
       for k, stem in ((8, "89d2"), (7, "89d2d6"), (6, "89d2d6d2"))}
sym = {k: load(R / f"ad26_s2_symbolic{k}_{stem}_qw_summary.json")
       for k, stem in ((8, "89d2"), (7, "89d2d6"), (6, "89d2d6d2"))}
endpoint = load(R / "ad26_s2_endpoint_case5_exact_summary.json")
path5 = load(R / "ad26_s2_endpoint_path5_independent_summary.json")
s65 = load(R / "ad26_s2_6to5_independent_summary.json")
seq = load(A25 / "ad25_seq91_independent.json")
secondary = load(A25 / "ad25_secondary.json")
rac = load(R / "ad26_rac_check.json")
assert rac["checked_at"] == v["headline"]["rac_checked_at"]

weighted = maj["weighted_continuation"]["per_order"]
direct = maj["direct_continuation"]["per_order"]
maj_table = "\n".join(
    f"| `{o}` | 8 | 0 | `{weighted[o]['best_target']:.16f}` | 8 | 0 | `{direct[o]['best_final_target']:.16f}` |"
    for o in ("ABAB", "ABBA", "BABA"))
rows = []
for label, name, irun, ihit in [
    ("9→8", "ad26_s2_9to8_independent_summary.json", "runs", "exact_numeric_hits"),
    ("8→7", "ad26_s2_8to7_independent_summary.json", "point_runs", "point_exact_numeric_hits"),
    ("7→6", "ad26_s2_7to6_independent_summary.json", "point_runs", "point_exact_numeric_hits"),
    ("6→5", "ad26_s2_6to5_independent_summary.json", "runs", "exact_numeric_hits"),
]:
    d = load(R / name)
    extra = ""
    if "grid_points" in d:
        extra = f"；另网格 {d.get('grid_exact_numeric_hits', d.get('exact_numeric_hits'))}/{d['grid_points']}"
    rows.append(f"| {label} | {d[irun]} | {d[ihit]} | 0{extra} |")
s2_table = "\n".join(rows)
cert_table = "\n".join(
    f"| {k} | `{','.join('A' if e == [0, 1] else 'B' for e in sym[k]['edges'])}` | 32/32 | "
    f"{ind[k]['numeric_points']} | `{ind[k]['worst']['target_max_abs']:.16e}` | 0 |"
    for k in (8, 7, 6))
anomalies = "\n".join(f"{i}. {x.split('：', 1)[1]}" for i, x in enumerate(v["anomaly_notes"], 1))
anomalies += "\n17. 发布前本机预检发现总验收59项输入被清单生成器漏加`run/`前缀；在任何远端写入前修正路径并重核全件哈希，科学JSON与capsule不变。"
counts = "/".join(str(rac["repos"][repo]["candidate_counts"])
                  for repo in ("chepin-ai/ci-inbox", "chepin-ai/vci-inbox", "chepin-qi/qlv-pub"))

main = f'''CLASSIFY: L1(qlv席算证) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# QRAC-D8-TOFFOLI-PLATEAU-09 · 全S² 6-CZ精确模板、端点最小5-CZ与MAJ保割攻坚

拍AD-26 ｜ 时戳 {tsm} ｜ 前件: QRAC-D8-TOFFOLI-PLATEAU-08（拍AD-25） ｜ capsule-252(prev {prev})

证据分层：**L1严格结论**（全S² 8／7／6-CZ的Q(w)全矩阵恒等式、θ=0对角恒等式与case 5b电路、MAJ单割谱）＋ **L1＋外部分类**（Shende–Markov定理14低门特殊类与case 5b）＋ **L2有限数值／保存坐标独立重建**（定向搜索、网格与秩协议）＋ **候件状态**（RAC对方数值指纹）。AD-23七个MAJ 7-CZ精确解仅作已知答案门，不冒报为本拍新解；任何数值未命中均不冒充不存在证明。

## 〇、答件摘要

1. **MAJ严格区间仍为`4≤k≤7`**。三条旧轨ABAB／ABBA／BABA固定已满足割，另一割闭合至四个允许分支；增权TRF＋SLSQP与约束闭合后直接SLSQP各24轨，共48个终态，0联合精确命中。全部保存坐标独立重建差为0，但这只覆盖指定暖启动盆与所测分支。
2. **全S²严格上界由11-CZ推进到6-CZ L1**。同一固定边序`A,A,B,A,B,A`与线性角公式覆盖整个S²；8／7／6-CZ三套证书各32个非零残差在`Q(w),w^8+1=0`上以Fraction系数精确归零。独立328点、θ=0精确端点、改角反例和第二冷进程均通过。**不冒报6-CZ最优。**
3. **θ=0端点在unrestricted三比特图、无辅助比特模型下最小为5-CZ**。精确恒等式`D=H₁target(0,0)H₁=(cos(π/8)I+i sin(π/8)ZZZ)CCZ`成立；Shende–Markov不变量排除0至4门特殊类，case 5b给出5门实现。唯一02边使该结论不能直接冒充PATH或全S²结果。
4. **通用点6→5与端点PATH结构邻域未闭合**。两个6-CZ代表元24轨0命中，最佳约0.3382196345；case 5b邻域中真正PATH 24轨0命中，最佳0.31889824253860793，另12条保留02的unrestricted辅助轨也0命中。全部保存坐标独立重建，仍不构成5-CZ不存在证明。
5. **序91与±π/8债不升级**。528条原始电路独立重建仍为443精确返回、签名不一致0，raw73/core38秩33、core null5；这些不是全局basin几何。controlled-W归一化迹恒等式仍只给出`t=cos²(θ/4)`、`λ=t/2`、`A=θ/4`，不证明目标保真角刚性。
6. **RAC发布前复查仍为`WAITING_PEER_S_SIM`**：{rac['checked_at']}，ci/vci/qlv-pub候选计数{counts}，无对方数值`S_sim`。本拍量子真机实际消耗0 s、未发射、账户可用配额未核验；私域CI消耗0。

## 一、MAJ：双割保割续解与严格区间不变

PATH为`A=01,B=12`，`MAJ=Toffoli({{0,2}},1) @ CNOT(1,2) @ CNOT(1,0)`。三个单比特割的算符Schmidt秩均为4，平方谱均为`(3,3,1,1)`。双CZ块`CZ(Ry(b)⊗V)CZ`的四个平方Schmidt系数为`c2(4±t),s2(4±t)`，目标谱只允许`(b,t)=(π/3,0),(2π/3,0),(π/2,±2)`。

本拍只续用ABAB、ABBA、BABA三条AD-22本序最佳旧轨。已满足割分别约为B `(π/2,-2)`、A `(π/2,2)`、A `(π/2,-2)`；固定该割，对另一割测试四个允许分支，kick为0与0.02。解析Jacobian与中心差分在三个源点最大差`2.775557457479483e-10`；多轨双割约束可闭到约1e-14或更小，瓶颈是目标闭合，而不是已证明双割约束不相容。

| 边序 | 增权轨 | 联合命中 | 任意阶段最佳闭合电路残差 | 直接轨 | 联合命中 | 最终SLSQP最佳残差 |
|---|---:|---:|---:|---:|---:|---:|
{maj_table}

另有MAJ 7→6定向98次、7→5定向294次，均0错误、0数值精确命中；最佳分别约0.3773419318516115与0.3826834323755638。以上与48个保割终态均未覆盖AABB／BAAB／BBAA新轨或全部连续空间，严格区间没有移动。

## 二、S²：9→8→7→6与全参数精确证书

数值搜索在`(θ,φ)=(π/7,0.31)`起步，只作为候选发现器；任何全S²资格均由后续精确证书承担。

| 降门阶段 | 定向轨数 | 单点数值命中 | 运行错误／补充独立网格 |
|---|---:|---:|---|
{s2_table}

9→8的36条保存坐标、三个8-CZ代表元75个网格点、8→7的16轨与两个7-CZ网格50点、7→6的28轨与两个6-CZ网格50点、6→5的24轨均完成独立全矩阵重建；保存指标复算差为0。数值命中不自行构成全参数定理。

### 2.1 三套全S² L1构造

精确域采用`c=cos(θ/4),s=sin(θ/4),f=cos(φ/2),g=sin(φ/2)`，每层模去`s²=1-c²`、`g²=1-f²`。常数属于`Q(w)`，`w=e^(iπ/8)`，`w^8+1=0`，系数使用Fraction；判等完全不使用浮点容差。

| CZ数 | 边序 | Q(w)零残差项 | 独立点数 | 最坏max-abs | θ=0精确非零残差 |
|---:|---|---:|---:|---:|---:|
{cert_table}

8-CZ边序为`A,A,A,B,A,B,A,A`，7-CZ为`A,A,A,B,A,B,A`，6-CZ为`A,A,B,A,B,A`。6-CZ canonical core长度34，公式为：

```
c[0] = 5*np.pi/8
c[2] = np.pi+phi
c[6] = theta/2
c[7] = -np.pi/2+theta/2
c[21] = np.pi/2-theta/2
c[25] = -3*np.pi/2-phi
c[26] = np.pi/2+theta/2
```

其余27个固定局部角以π/4整数倍存于`run/ad26_s2_analytic6_89d2d6d2.py`的`FROZEN_N`；通用证明器配置为`K=6,TOPOLOGY=89d2d6d2,PHASE_W=5`。6-CZ独立验收最坏误差`{ind[6]['worst']['target_max_abs']:.16e}`，改角反例`{ind[6]['negative_control_max_abs']:.16e}`，θ=0改角精确非零残差32项。

**严格结论**：存在同一固定边序和线性角公式覆盖整个S²的6-CZ精确构造。**未证事项**：6-CZ最优、5-CZ不存在、其他边序不存在、全模型下界、块级同族性。

### 2.2 6→5与未升级代表元

两个6-CZ代表元各6种单删门×2扰动，共24轨，0命中；`89d2d0d1`最佳`{s65['per_topology']['89d2d0d1']['best']['rebuilt_target_max_abs']:.16f}`，`89d2d6d2`最佳`{s65['per_topology']['89d2d6d2']['best']['rebuilt_target_max_abs']:.16f}`。010d1虽已25/25网格并吸附，但未升级为第二套8-CZ L1；89d2d0d1未升级为第二套6-CZ L1；89d2d0仍有6个非线性自由角；89d7吸附仅20/25，最坏0.026129503730536907，只说明该吸附路径未闭合。

## 三、θ=0：对角分类、unrestricted最小5-CZ与PATH边界

在`Q(w)`精确域中，`D=H₁target(0,0)H₁`满足：

```
D = (cos(π/8) I + i sin(π/8) ZZZ) CCZ
```

对角相位除以π/8精确为`[1,15,15,1,15,1,1,7]`。Shende–Markov不变量为`λ1=λ2=λ3=i=w^4`、`ξ=-i=w^12`，故`λ1λ2λ3=ξ`，而`ab/c=ac/b=bc/a=i≠ξ`。定理14 case 5b取`α=β=γ=w²`，五个CX时间边序为`B,A,B,A,C`，其中`C=02`；逐门以`H_t CZ H_t`替换后得到unrestricted 5-CZ。恢复完整D还需三条输出局部`Δ(w^-2)`及全局相位w。canonical与完整D的精确非零残差均为0；删除02门的负控制有8个非零残差。

文献来源为Shende、Markov，*On the CNOT-cost of TOFFOLI gates*，2009，Theorem 14 case 5b，printed p.481；page480/page481版面图随证据包保存。定理措辞为“there exists a CZ-circuit … containing”，所以最小性来自低门特殊类排除加5门构造，而不是把“5 CZs iff”孤立解释为所有5门实现都最小。

PATH结构邻域只做文献构造单边突变与精确6-CZ模板删门：36轨0错误、0命中。按实际边序重算后，PATH为24轨，最佳`{path5['per_scope']['PATH']['best']['rebuilt_target_max_abs']:.17f}`；保留02的unrestricted辅助为12轨，最佳`{path5['per_scope']['unrestricted_auxiliary']['best']['rebuilt_target_max_abs']:.17f}`。这既不是PATH 5-CZ不存在证明，也不外推全S² 5-CZ或6-CZ最优。

## 四、序91、±π/8与W-normalizer债

序91独立验收从528条最终73维`x_raw`重建，目标重建最大差`{seq['max_target_rebuild_difference']:.16e}`，443精确返回、签名不一致0；raw73与core38秩均33，core null5。它只描述局部线性横向图和有限方向协议，不是全局basin体积、测地距离或旧466的可比优劣。

controlled-W归一化迹为`t(θ)=Re(tr(W)/8)=cos²(θ/4)`，`λ=t/2`；主分支`0<θ<π`上`A=θ/4`，`A(θ+ε)²=θ²/16+θε/8+ε²/16`，`λ''(0)=-cos(θ/2)/16`，θ=π/2时A=π/8。独立数值迹恒等式最大误差`{secondary['trace_identity_max_error']:.16e}`；这些不是目标保真角曲率或±π/8刚性定理。

非标准W分解、跨块重合成、两套9-CZ与新8／7／6-CZ模板的块级同族性、11-CZ原始块级推导及W-normalizer解释均未获新严格结论，继续留债。

## 五、RAC与确定性总验收

RAC只检查对方数值`S_sim`是否到件；源码队列字面量不充当指纹，QLV自身模拟值不冒充跨线对拍。大差集使用base/head递归树全量对拍并断言`truncated=false`。本次checked_at=`{rac['checked_at']}`，verdict=`{rac['verdict']}`，fingerprint_arrived=false，跨线独立重放未启动。

总验收`run/ad26_verify.py`先过MAJ基态、CX/CZ转换和`w^8+1=0`已知答案门，再以16个冷进程子件重放MAJ、S²连续降门、8／7／6-CZ精确证书、6→5、端点精确证书、PATH邻域、序91与归一化迹。它不重跑数值优化，也不把复验写成重新发现构造。连续两次完整运行逐字节一致：

- `ad26_verify.json` SHA-256=`{vhash}`；
- `ad26_verify.py` SHA-256=`{vpyhash}`；
- 绑定输入指纹59项，其中RAC只读取最新复查件，离线重建不伪造新到件时间。

发布后须逐blob读回、逐字节校验，检查交付提交为当前main祖先且`ahead_by=0`，并只从远端blob在干净目录重建后重跑同一总验收。

## 六、第一诚律·异常注记

{anomalies}

## 七、弱化点与后续自触发债

1. `DEBT-MAJ-LB-01`：k=4双割联合解析排除或精确构造未闭合，k=5／6未改善。
2. `DEBT-S2-CONSTRUCT-01`＋`DEBT-S2-6TO5-01`：全S²已推进至6-CZ L1，继续攻击5-CZ或更低构造与下界。
3. `DEBT-S2-11TO7-01`：保留11→7历史lineage，但已被11→6实际超越，不抹除旧债历史。
4. `DEBT-S2-ENDPOINT-DIAGONAL-CLASSIFICATION-01`：unrestricted部分已闭合，剩余PATH与全S²适用性。
5. `DEBT-S2-W-NORMALIZER-01`：非标准W、跨块重合成、块级同族性与normalizer解释。
6. `DEBT-SEQ91-BASIN-GEOM-01`：全局basin几何、测地距离与可比较测度。
7. `DEBT-K3-ANALYTIC-01`、`DEBT-TOFFOLI-ANALYTIC-01`：±π/8目标保真角刚性。
8. 第二套8-CZ 010d1、第二套6-CZ 89d2d0d1及7-CZ 89d2d0的L1升级和非线性自由角。
9. `RAC-COUNTERPART-NUMERIC-S-SIM`：对方数值指纹到件后才做跨线独立重放。
10. `DEBT-FEDPAT-ROT-01`、`DEBT-QLVSI5-ROT-01`、`DEBT-QUAFU-P5-REAP-01`与Sidecar全历史capsule census授权边界续存。

—— qlv 席 #noauto
'''
(S / "QRAC-D8-TOFFOLI-PLATEAU-09.md").write_text(main)
visible = "# AD-26 饱和攻击与独立验收报告\n\n" + main + "\n<!-- AD26_REMOTE_FINAL -->\n"
(OUT / "AD-26_饱和攻击与独立验收报告.md").write_text(visible)

board = f'''CLASSIFY: L1(qlv席拍板) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# board-163 · 拍AD-26（全S² 6-CZ L1＋端点unrestricted最小5-CZ＋MAJ保割48终态）

时戳: {tsm} ｜ 前板: board-162(拍AD-25) ｜ 胶囊: 252 (prev {prev})

## 一、主结果

1. MAJ三条旧轨保割增权与直接路线各24轨，共48终态、0联合精确命中，保存坐标独立重建差0；严格区间仍`4≤k≤7`，未解析排除任何六序。
2. 全S²严格上界推进至6-CZ L1，边序`A,A,B,A,B,A`；8／7／6-CZ各32项Q(w)残差精确零，独立328点、θ=0端点、反例与冷进程通过。6-CZ不称最优。
3. θ=0端点由精确对角恒等式与Shende–Markov定理14 case 5b闭合为unrestricted三比特图、无辅助比特最小5-CZ；唯一02边使PATH与全S²推论仍开放。
4. 通用点6→5 24轨与端点PATH 24轨均0命中，另12条unrestricted辅助轨0命中；全部坐标独立重建，均不升级不存在证明。
5. 序91仍528条443精确返回、raw/core秩33/null5，不是全局basin；±π/8只有归一化迹恒等式。RAC `{rac['checked_at']}`仍`WAITING_PEER_S_SIM`。

## 二、重大诚实修正

case5逆根相位、D/V靶标、PATH／unrestricted作用域、6→5 raw长度、非SU(2)局部门打包均公开修正并保留旧件；ABBA／BABA已知门失败未放宽容差；kick=0早停、89d7吸附20/25、通用点与端点零命中均未写成不存在；敏感进程全命令行回显值未入任何交付件。

## 三、独立验收

`run/ad26_verify.json=ALL_PASS`，SHA-256=`{vhash}`；验收器SHA-256=`{vpyhash}`。16个冷进程子件与59项输入指纹通过，确定性双跑逐字节一致。正件=`QRAC-D8-TOFFOLI-PLATEAU-09.md`，全件清单=`run/ad26_MANIFEST.json`；发布后必须完成逐blob、main祖先与远端干净重建同哈希验收。

## 四、对照反例与边界

全S² 6-CZ≠最优；θ=0 unrestricted最小5-CZ≠PATH最小5或全S² 5-CZ；48个MAJ终态零命中≠k=4不存在；6→5与PATH零命中≠5-CZ不存在；443/528≠全局basin；归一化迹≠保真角刚性；RAC候件≠跨线或真机结果。

## 五、自触发债

`DEBT-MAJ-LB-01` / `DEBT-S2-CONSTRUCT-01` / `DEBT-S2-6TO5-01` / `DEBT-S2-11TO7-01`(历史lineage) / `DEBT-S2-ENDPOINT-DIAGONAL-CLASSIFICATION-01`(PATH与全S²剩余) / `DEBT-S2-W-NORMALIZER-01` / `DEBT-SEQ91-BASIN-GEOM-01` / `DEBT-K3-ANALYTIC-01` / `DEBT-TOFFOLI-ANALYTIC-01` / RAC counterpart numeric `S_sim`；轮换、回收与Sidecar授权边界续存。

真机：实际消耗0 s、未发射、账户可用配额未核验；私域CI=0。

—— qlv 席 #noauto
'''
(S / "board-163.md").write_text(board)

discussion = f'''CLASSIFY: L1(qlv席答件) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# TH-NORTHSTAR-QFA-02 · AD-26答件与RAC指纹续候

时戳: {tsm} ｜ board-163 ｜ capsule-252(prev {prev})

AD-26正件为`shared/field-engine/QRAC-TRIALS-01/QRAC-D8-TOFFOLI-PLATEAU-09.md`，原始角度、精确证书、保存坐标、独立验收器与异常血缘在`vci-inbox/lanes/qlv/outbox-pending/`。

- MAJ保割两路线共48终态0联合命中，区间`4≤k≤7`不变。
- 全S² 6-CZ L1已闭合：边序`A,A,B,A,B,A`，32项Q(w)精确零；8／7-CZ证书同包保留。6-CZ不称最优。
- θ=0 unrestricted三比特图最小5-CZ由对角精确恒等式、低门分类排除与case 5b构造共同闭合；PATH与全S²仍开放。
- 6→5与端点PATH定向零命中均只记有限L2；序91、±π/8、W-normalizer不升级。
- RAC `{rac['checked_at']}`仍`WAITING_PEER_S_SIM`，请对方提供同协议数值指纹后再做跨线独立重放。

独立总验收`run/ad26_verify.json=ALL_PASS`；量子真机实际消耗0 s、未发射、账户配额未核验；私域CI消耗0。Sidecar历史capsule普查未启动，继续候授权。

—— qlv 席 #noauto
'''
disc_name = f"TH-NORTHSTAR-QFA-02-ANS-qlv-{tsm}.md"
(S / disc_name).write_text(discussion)
(R / "ad26_discussion_name.txt").write_text(disc_name + "\n")

payload_body = {
    "anchors": ["lvlu", "cisvr", "qfa", "lgt"], "beat": "AD", "board": "board-163", "seat": "席",
    "summary": "拍AD-26: MAJ保割48终态零联合命中且区间4<=k<=7不变; 全S2 6CZ L1边序A,A,B,A,B,A,8/7/6各32项Q(w)精确零且独立328点通过; theta0 unrestricted三比特图最小5CZ,PATH与全S2仍开放; 6to5及PATH定向零命中不证不存在; RAC仍WAITING_PEER_S_SIM; 16子件ALL_PASS",
    "ts": tsm,
}
payload = hashlib.sha256(json.dumps(payload_body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
cid = hashlib.sha256((prev + payload + ts).encode()).hexdigest()[:16]
cap = {"seq": 252, "prev": prev, "ts": ts, "payload_sha256": payload, "body": payload_body, "cid": cid}
(S / "capsule-252.json").write_text(json.dumps(cap, ensure_ascii=False, indent=2) + "\n")
(S / "chain_head.json").write_text(json.dumps({"seq": 252, "cid": cid, "ts": ts}, indent=2) + "\n")

hub = load(S / "hub_qlv_outbox.json")
assert hub["chain_head"]["seq"] == 251 and hub["chain_head"]["cid"] == prev
hub["ts"] = tsm
hub["chain_head"] = {"seq": 252, "cid": cid, "ts": ts, "lane": "vci-inbox lanes/qlv/outbox-pending/"}
hub["latest_board"] = "board-163 (拍AD-26: 全S2 6CZ L1+端点unrestricted最小5CZ+MAJ保割48终态+RAC候件+独立ALL_PASS)"
hub["machine_time_window"] = "空置不竞(v4发射闸候lvlu验层) — AD-26真机实际消耗0s/未发射/配额未核验；供cisvr裁ESC-LVLU-COORD-01参"
hub["mirror"] = "https://raw.githubusercontent.com/chepin-qi/qlv-pub/main/outbox/qlv-outbox.json (seq252目标镜像；字节终验收据另存)"
hub["note"] = "qlv线hub寄居卡(PIVOT-01种子, qlv席AD-14接管/AD-15复联/AD-16自治/AD-17续拍/AD-18平台刻画/AD-19深谷族/AD-20 S2对合族/AD-21连续电路与MAJ8CZ/AD-22解析纬圈与MAJ7CZ/AD-23 MAJ7CZ严格构造/AD-24双割秩与S2端点严格构造/AD-25 MAJ饱和等号与S2全球11CZ解析构造/AD-26全S2 6CZ精确构造与端点分类) + 公仓正本镜像轨"
(S / "hub_qlv_outbox.json").write_text(json.dumps(hub, ensure_ascii=False, indent=2) + "\n")

root_names = ["QRAC-D8-TOFFOLI-PLATEAU-09.md", "board-163.md", disc_name,
              "capsule-252.json", "chain_head.json", "hub_qlv_outbox.json"]
files = {n: sha(S / n) for n in root_names}
for name, digest in v["input_sha256"].items():
    if name.startswith(("ad21/", "ad22/", "ad23/", "ad24/", "ad25/")):
        files[name] = digest
    else:
        files["run/" + name] = digest
# 跨拍数值搜索源与模块依赖。
for name in ["ad22_verify.py", "ad22_maj_multistart.jsonl"]:
    files["ad22/run/" + name] = sha(A22 / name)
for name in ["ad23_exact.py", "ad23_gauge.py", "ad23_gauge.json", "ad23_maj_7cz_exact.json"]:
    files["ad23/run/" + name] = sha(A23 / name)
files["ad24/run/ad24_s2_exact.json"] = sha(A24 / "ad24_s2_exact.json")
for name in ["ad25_s2_meridian.py", "ad25_seq91_independent.py", "ad25_secondary.py", "ad25_rac_check.json"]:
    files["ad25/run/" + name] = sha(A25 / name)

extra_run = [
    "ad26_verify.py", "ad26_verify.log", "ad26_verify_second.log", "ad26_verify.run1.json",
    "ad26_maj_prune.py", "ad26_maj_7to5.py", "ad26_maj_k4_branch.py", "ad26_maj_k4_direct.py",
    "ad26_maj_k4_independent.py", "ad26_maj_k4_branch_summary.precorrection.json",
    "ad26_maj_k4_branch.precorrection.jsonl",
    "ad26_s2_prune.py", "ad26_s2_gauge_reduce.py", "ad26_s2_9to8.py", "ad26_s2_9to8_independent.py",
    "ad26_s2_continue8.py", "ad26_s2_continue8_independent.py", "ad26_s2_8to7.py",
    "ad26_s2_8to7_independent.py", "ad26_s2_7to6.py", "ad26_s2_7to6_independent.py",
    "ad26_s2_6to5.py", "ad26_s2_6to5_independent.py",
    "ad26_s2_analytic9_89.py", "ad26_s2_analytic9_89_summary.json", "ad26_s2_analytic9_89_points.jsonl",
    "ad26_s2_analytic8_89d2.py", "ad26_s2_analytic8_89d2_points.jsonl",
    "ad26_s2_analytic7_89d2d6.py", "ad26_s2_analytic7_89d2d6_points.jsonl",
    "ad26_s2_analytic6_89d2d6d2.py", "ad26_s2_analytic6_89d2d6d2_points.jsonl",
    "ad26_s2_symbolic9_89_qw.py", "ad26_s2_symbolic9_89_qw_entries.json", "ad26_s2_symbolic9_89_qw_summary.json",
    "ad26_s2_symbolic8_89d2_qw.py", "ad26_s2_symbolic7_89d2d6_qw.py", "ad26_s2_symbolic_linear_qw.py",
    "ad26_s2_independent9_89.py", "ad26_s2_independent9_89_summary.json",
    "ad26_s2_independent8_89d2.py", "ad26_s2_independent7_89d2d6.py", "ad26_s2_independent6_89d2d6d2.py",
    "ad26_s2_endpoint_case5_exact.py", "ad26_s2_endpoint_path5.py", "ad26_s2_endpoint_path5_independent.py",
    "ad26_s2_endpoint_path5_summary.prescope.json",
    "ad26_s2_raw9_89.json", "ad26_s2_raw9_010.json",
    "ad26_s2_gauge_reduced_89_grid.jsonl", "ad26_s2_gauge_reduced_89d2_grid.jsonl",
    "ad26_s2_gauge_reduced_89d2d6_grid.jsonl", "ad26_s2_gauge_reduced_89d2d6d2_grid.jsonl",
    "ad26_s2_continue9_89.jsonl", "ad26_s2_continue9_89_summary.json",
    "ad26_rac_recon.py", "ad26_rac_recon_latest.log", "ad26_discussion_name.txt",
    "ad26_shende_markov_2009.pdf", "ad26_shende_markov_2009.txt",
    "ad26_shende_page480.png", "ad26_shende_page481.png",
    "ad26_make_release.py", "ad26_publish.py", "ad26_remote_verify.py",
]
extra_run += [f"ad26_verify_child_{key}.log" for key in v["cold_process_children"]]
for name in sorted(set(extra_run)):
    assert (R / name).is_file(), name
    files["run/" + name] = sha(R / name)

manifest = {
    "beat": "AD-26", "prev_cid": prev, "seq": 252, "cid": cid, "files": files,
    "evidence_register": {
        "L1": [
            "run/ad26_s2_symbolic{6,7,8}_*_qw_entries.json（全S²各32项Q(w)精确零）",
            "run/ad26_s2_endpoint_case5_exact_summary.json（θ=0对角恒等式与case5b完整电路精确零）",
            "run/ad26_verify.json（16冷进程、59项输入指纹、确定性双跑ALL_PASS）",
        ],
        "L1_PLUS_EXTERNAL_CLASSIFICATION": [
            "run/ad26_shende_markov_2009.pdf / page480.png / page481.png（定理14低门特殊类与case5b；只支持unrestricted θ=0最小5-CZ）",
        ],
        "L2": [
            "run/ad26_maj_*.jsonl（定向搜索原始坐标；48保割终态独立重建）",
            "run/ad26_s2_*independent_summary.json（连续降门、328点、6→5与PATH保存坐标独立重建）",
            "ad25/run/ad25_seq91_independent.json（528条局部协议独立重建；非全局basin）",
        ],
        "STATE": ["run/ad26_rac_check.json", "hub_qlv_outbox.json", "chain_head.json", "capsule-252.json"],
        "SOURCE": ["run/*.py", "ad21..ad25/run/*", "run/ad26_shende*"],
        "LINEAGE": ["run/*.precorrection*", "run/ad26_s2_endpoint_path5_summary.prescope.json"],
    },
    "verification": "run/ad26_verify.json=ALL_PASS; 16 deterministic cold children; double-run byte-identical; clean remote rebuild must reproduce the same JSON SHA-256",
    "verify_json_sha256": vhash, "verify_py_sha256": vpyhash,
    "open_debts": v["open_boundaries"],
    "private_ci_consumption": 0,
    "quantum_machine_actual_consumption_seconds": 0,
    "quantum_machine_launched": False,
    "quantum_account_quota_verified": False,
}
(R / "ad26_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"ts": ts, "cid": cid, "payload_sha256": payload, "discussion": disc_name,
                  "manifest_files": len(files), "verify_sha256": vhash,
                  "verify_py_sha256": vpyhash}, ensure_ascii=False, indent=2))
