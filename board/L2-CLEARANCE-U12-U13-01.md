CLASSIFY: L1
# L2-CLEARANCE-U12-U13-01 · WS-F 挂账 U-13 / U-12 正式清除成文（EXT-WAVE-19 批七 · 完备化线）

- 成文席：QF-OS 联邦 W2 写作席（只写文，不 commit）
- 清除时间戳（`date -u` 实测）：**2026-10-23T15:07:45Z**
- 证据基件：board/L2-RECALC-WINDOW-01.md（L2-2 复算窗首开判定件，2026-10-23 登记）；方法学/外部基准件：board/WSF-EVIDENCE-SWEEP-20261023-01.md（R2 证据表，U-12 钉 §一「U-12」L17–21、U-13 钉 §一「U-13」L23–25）
- 纪律钉（全件适用）：涉 NS 表述逐字携带「有限维 ODE 截断层」限定；禁「NS 已解决」式表述；批准状态语「自评已核、外部复现中、未颁奖」。涉 RH 表述逐字携带「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」；禁「RH 已证」式表述。名值分离：本件登记的 decl 名与公理集值分行列出，不以名代值。

---

## 一、U-13 正式清除成文 ｜ galerkinNS_exists_unique_solution_upto 打包件公理桥接 —— 清除结论：**可销（PASS 成立）**

### 1. 桥接什么（自 L2-RECALC-WINDOW-01.md §U-13 摘准）
打包 decl `NSGalerkin.galerkinNS_exists_unique_solution_upto` 未逐件进入原 CI 五 decl 审计清单，挂账拟以「由三已审组分直接打包」桥接。三已审组分为：
- `NSGalerkin.GalerkinNS.exists_solution_upto`
- `NSGalerkin.GalerkinNS.norm_sq_le_of_solution`
- `NSGalerkin.GalerkinNS.solution_unique_upto`

源码层旁证（同一判定件登记）：Concrete.lean L136–145 打包体为单行直调 `(GalerkinNS.concreteData a f).exists_unique_solution_upto x₀ hT`。

### 2. 核证方式
实跑探针，非缺席推理：复算窗重建环境（Lean v4.35.0 工具链，`lean --version` 实测 `Lean (version 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)`；工程副本取 PAL-0003 在册钉点 `ca67c869988a2123937c5d696b746399703becdf` 之 library/ns，mathlib cache 8443 件预取、`lake build` rc=0、3291 jobs、零 error、零 sorry 令牌），随后 `lake env lean Probe.lean`（wall=79s）对打包件与三组分各跑 `#print axioms`。

### 3. 核证输出（机器原文，自 L2-RECALC-WINDOW-01.md L79–86 转录）
```
'NSGalerkin.galerkinNS_exists_unique_solution_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.exists_solution_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.norm_sq_le_of_solution' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.solution_unique_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.exists_unique_solution_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
```
判定：打包件公理集 = {propext, Classical.choice, Quot.sound} = 三已审组分公理集之并（三者各为同一集合）；打包未引入任何额外公理（无 sorryAx、无自设公理）。WSF-EVIDENCE-SWEEP-20261023-01.md §一「U-13」所载「桥接方法学成立但须实跑判定」之实跑条件已满足。

### 4. 证据钉（文件 + 行号）
| 钉 | 位置 |
|---|---|
| 判定原文（探针输出、桥接判定、销账建议） | board/L2-RECALC-WINDOW-01.md L77–88（§U-13 节） |
| 环境重建底座（工具链版本、钉点、cache、build rc=0） | board/L2-RECALC-WINDOW-01.md L70–75（§环境重建记录） |
| 判定汇总表 U-13 行 | board/L2-RECALC-WINDOW-01.md L133 |
| 方法学外部锚（#print axioms 传递闭包） | board/WSF-EVIDENCE-SWEEP-20261023-01.md §一「U-13」L23–25 |
| 挂账原义（桥接主张来源） | board/W-NS-03-REFORGE-CHARTER-01.md（经 WSF 扫描件 §U-13 转引） |

### 5. 清除结论与随附义务
- **清除成立**：U-13（打包件公理桥接）自本件登记时刻起销账，判定 = 实跑成立（PASS）。
- 随附义务（非阻塞）：将打包 decl `galerkinNS_exists_unique_solution_upto` 补入 CI 公理审计清单，防回归（源自判定件销账建议 L88）。
- 域限重申：以上公理审计结果仅及 **有限维 ODE 截断层** 之 Lean 定理层，不触碰 3D NS 本体，不构成任何 PDE 层陈述。

### 6. 清除非终局条款
本清除以第 4 节证据钉为唯一承载。**若上游证据钉变动**——包括但不限于：library/ns 源码变更致打包件依赖闭包改变、复算基件（L2-RECALC-WINDOW-01.md）被勘误、工具链/钉点失效——本清除**自动回炉重审**，在重审完成前按挂账态处理，任何下游引用不得援引本清除结论。

---

## 二、U-12 正式清除成文 ｜ capAnchorP1 / zetaAnchorImpliesRHCriticalLine 公理覆盖 —— 清除结论：**可销（定义层 PASS，公理覆盖部分）**，另附两项注记全录

### 1. 挂账原义与定位订正
挂账（WSF-EVIDENCE-SWEEP-20261023-01.md §一「U-12」L17–21）：二 decl 公理字段未被审计清单覆盖；审计方法学有 Lean 官方依据，具体公理集须随 L2-2 复算窗实跑。定位订正（判定件 L92）：二 decl **不在** artifacts/CERT-CIRC-LEAN-01，实在 library/ns——`NSGalerkin.capAnchorP1`（NsGalerkin/CapAnchor.lean L131）、`ZetaAnchor.zetaAnchorImpliesRHCriticalLine`（NsGalerkin/ZetaAnchor.lean L35）；故无需 CERT-CIRC-LEAN-01 构建。

### 2. 核证方式与输出（同一次 Probe.lean 运行，机器原文自判定件 L93–98 转录）
```
'NSGalerkin.capAnchorP1' depends on axioms: [propext, Classical.choice, Quot.sound]
'ZetaAnchor.zetaAnchorImpliesRHCriticalLine' depends on axioms: [propext, Classical.choice, Quot.sound]
Probe.lean:16:14: error(lean.unknownIdentifier): Unknown constant `NSGalerkin.zetaAnchorImpliesRHCriticalLine`
```
名值分离登记：decl 名（值）如下——`NSGalerkin.capAnchorP1`（公理集 = {propext, Classical.choice, Quot.sound}）；`ZetaAnchor.zetaAnchorImpliesRHCriticalLine`（公理集 = {propext, Classical.choice, Quot.sound}）。二 decl 公理集均 = 三公理白名单，无 sorryAx；审计覆盖缺口（原 CI 五 decl 清单不含此二件）经本探针补足实跑证据。

### 3. 清除结论
**U-12 定义层公理覆盖部分清除成立（PASS）**，自本件登记时刻起销账。清除域严格限于「#print axioms 覆盖二 decl 之定义性依赖闭包」一事，不扩及任何证明性断言。

### 4. 便签全录（照录判定件，两项注记入档）

**便签①（层位钉——覆盖为定义层，非证明层）**：二 decl 均为 `def : Prop` 陈述锚（CapAnchor.lean L101/L130「no proof is asserted here (external proof layer DONE; kernel layer BLOCKED(B1)」；ZetaAnchor.lean L34「No proof asserted」）。#print axioms 覆盖其定义性依赖闭包，**不构成任何证明性断言**。涉 RH 行文钉维持逐字：「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」；zetaAnchorImpliesRHCriticalLine 为全局尺度临界线命题的 Prop 陈述件，**非 RH 证据**。本便签不阻塞 U-12 定义层清除，但构成清除域的硬边界。

**便签②（登记错位——ζ-anchor 命名失配 finding 及对 U-17 家族的影响评估）**：formalization.yaml alignment L160 登记名为 `NSGalerkin.zetaAnchorImpliesRHCriticalLine`，kernel 实测该名**不解析**（`Unknown constant`，机器原文见 §2）；真实全名为 `ZetaAnchor.zetaAnchorImpliesRHCriticalLine`（ZetaAnchor.lean L18 命名空间）。同条 `NSGalerkin.capAnchorP1` 解析正常。即 yaml alignment 第 5 条 lean 名半错——与 U-17（yaml alignment 第 5 条指帧 §3.2 编号归属不符）同条邻位。
- **影响评估**：该 finding **不阻塞 U-12 定义层清除**（公理覆盖对真实全名实跑通过，名错位属登记层而非内容层）；但**登记为 U-17 家族前置义务**——U-17 修订案开案时，须将 yaml alignment L160 之名错位（`NSGalerkin.` → `ZetaAnchor.`）与编号归属不符一并处理，二错同条邻位，宜并案修订，不得只修其一即宣称 U-17 族闭合。

**便签③（CERT-CIRC-LEAN-01 依赖成本评估）**：artifacts/CERT-CIRC-LEAN-01 依赖 leancert @v4.34.1 + 第二套工具链（约 600MB 下载；leancert 无 cache 通道，4GB RAM 下 OOM 风险有 TB-06 B1 记录在案），评估 ≫30min，复算窗未开销，**该件构建验证记 PARTIAL**。此不影响 U-12 清除——二 decl 实在 library/ns，公理覆盖已在 NsGalerkin 工程内闭环。

### 5. 证据钉（文件 + 行号）
| 钉 | 位置 |
|---|---|
| 判定原文（定位订正、探针输出、两项边界发现、销账建议） | board/L2-RECALC-WINDOW-01.md L90–102（§U-12 节） |
| CERT-CIRC-LEAN-01 成本评估 | board/L2-RECALC-WINDOW-01.md L122–124 |
| 判定汇总表 U-12 行与新发现行 | board/L2-RECALC-WINDOW-01.md L134、L136 |
| 方法学外部锚（#print axioms 白名单） | board/WSF-EVIDENCE-SWEEP-20261023-01.md §一「U-12」L17–21 |
| 环境重建底座 | board/L2-RECALC-WINDOW-01.md L70–75 |

### 6. 清除非终局条款
本清除以第 5 节证据钉为唯一承载。**若上游证据钉变动**——包括但不限于：library/ns 源码变更致二 decl 依赖闭包改变、formalization.yaml alignment 修订（含 U-17 族并案修订落地）、复算基件被勘误、工具链/钉点失效——本清除**自动回炉重审**，在重审完成前按挂账态处理；便签②之 U-17 家族前置义务不随本清除销账，独立存续至 U-17 修订案闭合。

---

—— QF-OS 联邦 W2 写作席 · EXT-WAVE-19 批七（完备化线）· 2026-10-23T15:07:45Z · 纯成文零 commit
