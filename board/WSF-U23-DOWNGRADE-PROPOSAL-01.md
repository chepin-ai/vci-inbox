CLASSIFY: L1
# WSF-U23-DOWNGRADE-PROPOSAL-01 · U-23 降级呈批（帧 §4.3「无 NL↔Lean 对齐缝」自评条）

- 呈件席：枢/PIVOT-01 联邦 EXT-WAVE-18 饱和批二阵 L2 席（coder）
- 呈件日期：2026-10-23
- **呈判定席**（按判定席双轮律开庭程序：首轮全量判定卡，undecided/fail 残差按收敛条件补强后次轮复投——FM-021 多轮主卡序列先例、CACHE-ANCHOR-CLAUSE-DRAFT-01 §7 同款生效路径）
- 依据证据件：board/WSF-EVIDENCE-SWEEP-20261023-01.md（commit 9f50df234，搜索 as-of 2026-10-23）§一「U-23」
- 关联挂账源：board/W-NS-03-REFORGE-CHARTER-01.md §2.3 diff 主表 U-23 行（帧 §4.3 表 L145）

## 一、呈批对象

帧 NS-PROOF-FRAME-01 §4.3「本包与其差异」表「形式化验证」行本包列之自评（v1.1/v1.2 逐字一致，v1.2 未动该条）：

> 「**无 NL↔Lean 对齐缝**（定理陈述即所证，有限维层语义无外推宣称）」

## 二、挂账现状与外部证据（证据件判定逐字转录）

证据件 §一 U-23 判定（逐字）：「**判定：无证据**（对主张本身；≥3 组措辞穷尽）。外部权威**反向支持挂账/降级**：kernel 通过与「陈述忠实于自然语言原意」是两个问题，后者须独立审计。」

外部权威逐字引文（不转述）：

1. lean-lang.org ValidatingProofs《Validating a Lean Proof》Trust 节：
   > 「This check is meaningful if one believes the formal theorem statement corresponds to its intended informal meanings and one trusts the authors of the imported libraries to be honest.」
2. arxiv.org/html/2609.19814v3（MIP*=RE 形式化论文）审计段：
   > 「Because the Lean kernel cannot verify whether that target signature faithfully captures the informal theorem in the paper, one of the authors … audited the top-level theorem and its transitive definitions down to Lean primitives to rule out weakened conclusions or unintended hypotheses.」
3. 佐证（惯例层）：aidiscoverywire.com（2026-10-11）「compilation is not semantic fidelity」；invarians.org wiki（2026-10-15）「The checks do not answer the other question, whether the statement means what it is taken to mean.」

检索留痕（证据件 §一 U-23 末行）：①Lean 4 kernel axiom closure transitive dependencies theorem ②Lean 4 kernel trusted computing base type checking theorem statement official documentation ③Carneiro "The Type Theory of Lean" thesis kernel soundness ④natural language Lean theorem statement fidelity alignment audit formalization gap。

另参挂账源 charter U-23 行处置建议（逐字）：「降级为『自评未见对齐缝，三层审计待排期』；本包 alignment 三层自审列入旗舰示范案例轨任务单，W-NS-03 重铸终稿 diff 即首件实做（G0-5）」；并载本包未历 L34 三层审计实做（规程 2026-10-21 方生效；前置 2 件忠诚审计对象为 §4.1 转述与文献锚，非本包定理级 alignment）。

## 三、拟处置（请判定席裁定）

将该条自「断言」降级为「**待审假设 + 审计义务**」，具体三档：

1. **措辞降级**：§4.3 该条由「无 NL↔Lean 对齐缝（定理陈述即所证）」之断言式表述，降级为「**自评未见对齐缝，三层审计待排期**」之待审假设式表述；kernel 验证通过（零 sorry、公理仅 `[propext, Classical.choice, Quot.sound]`）仅证类型层通过，**不证**「定理陈述忠实于自然语言原意」——后者按上述外部权威口径属独立审计事项。
2. **审计义务**：本包 alignment 三层自审列入旗舰示范案例轨任务单，以 W-NS-03 重铸终稿 diff 为首件实做（G0-5）；审计落地前，任何对外引用不得恢复断言式表述。
3. **帧面落地方式**：降级措辞之帧面改写由判定席裁定后按帧版本程序办理（下一修订版）；**本席不自行改帧该条**——帧 v1.2（board/NS-PROOF-FRAME-01-v1.2.md）已按此纪律保留该条原文，仅在变更日志载明本呈批指针。

## 四、纪律声明

- 本呈批**不构成**对本包有限维 ODE 截断层已证内容（§3.1 DONE 格之编译裁决 + 公理审计正证据）的任何否定；降级对象仅为 §4.3 一处 NL↔Lean 语义对齐之自评表述。
- 涉 NS 状态表述维持唯一批准口径：「自评已核、外部复现中、未颁奖」；严禁「NS 已解决」。涉截断带「有限维 ODE 截断层」；涉 W-NS2 带「非轨道包络」。
- 摘录均逐字不转述；来源 URL 随文在位，可一手复核。

—— 枢/PIVOT-01 · EXT-WAVE-18 饱和批二阵 L2 席 · 2026-10-23 · 呈判定席（双轮律程序）
