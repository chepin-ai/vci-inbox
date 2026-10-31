CLASSIFY: L1
# EXT-INTEL-20261031-01-ANALYSIS · QF-OS 联邦批三十三 S4 · arXiv:2610.08144《Navier–Stokes lost in translation》精核分析件

- 席别：批三十三 S4 外部情报精核席；时刻：2026-10-31（as-of；UTC(Z)）；精核源：arXiv abs 页＋HTML 全文（`arxiv.org/abs/2610.08144`、`arxiv.org/html/2610.08144v1`，本拍当次取读）
- 口径纪律（逐字）：OpenAI 包三钉「**自评已核、外部复现中、未颁奖**」；涉 NS 限「**有限维 ODE 截断层**」语境、严禁「NS 已解决」；HWY=**Hou–Wang–Yang** 全名＋「**待评审预印本，结论未确立**」；ζ 纪律（如涉）：「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」
- 名值分离：引文（原文逐字）与本席判语分行；页码/行号/式号钉在案；零 git 写；只交付不入库

## 〇、该文性质钉（先钉后析）

- 题：*Navier–Stokes lost in translation – Why Lean verification of AI autoformalisation does not guarantee correct natural language proofs*
- 作者：A. Bastounis（King's College London）、F. Circelli（Cambridge DAMTP）、A. C. Hansen（Cambridge DAMTP，通讯）
- 性质：**预印本 v1，提交时刻 2026-10-06 10:58:01 UTC（arXiv 版本行在案）；同行评审未竟**（无期刊/会议收录信息在案）；MSC：35Q30、03Dxx（主），68V20、68Txx、03B65（次）
- 对象：OpenAI 宣布之 NS blow-up NL 证明及其 Lean 4 形式化库（openai/NavierStokesAndEuler，commit f9e8bc5 钉在案）
- 作者自载免责（逐字）："We do not make claims about the correctness of OpenAI's NL proof, we only make statements about mistranslations into Lean."——本席照录：该文攻击面是**翻译忠实性**，非 NL 证明对错本身

## 一、失配一坐实摘录（导数阶 4 vs 5——Lemma 8.6 / 式 (8.19)）

**NL 论文侧（源文 p.95，式 (8.19)，本件转写）**：‖N⁻¹F‖_{C^m_y} ≤ C_m‖F‖_{C^{m+4}_y}——输出 m 阶环面导数以源项 **m+4** 阶导数控制。

**Lean 侧（`norm_derivativeWord_inverse_le`，NavierStokes/SmoothFamilyTorusInverse.lean 行 1059–1080，commit f9e8bc5）**：‖N⁻¹F‖_{C^m_y} ≤ K_m‖F‖_{C^{m+5}_y}——两假设 `hfirst/hsecond` 均要求 `w.length + 5` 阶源导数界（红标在案）。

**失配文原文坐实（§3.1，逐字）**：
> "The related Lean codes – on the other hand – all use five additional derivatives, not four."
> "This estimate is then strictly weaker than equation (8.19) due to the extra derivative on the right-hand side."
> 证明路径差（逐字）：NL 论文用 m+4 阶导数配收敛级数 ∑ 1/(1+|k|)³（二维可和）；Lean 码用级数 ∑ 1/(1+|k₁|+|k₂|)⁴（红标指数 4 在案），"thus uses m+5 derivatives instead"，经 `coefficient_seminorm_bound` 引入。
> 附注（逐字，脚注 5）："some such Lean results are actually incomparable with (3.1), due to the mismatch in the type of derivative"（如 `inverse_finiteJets` 用混合导数而非纯环面导数）。

**本席判语**：失配一成立且方向明确——**NL 界（4 阶余量）强于 Lean 界（5 阶余量）**；Lean 编译通过 ≠ NL 命题（8.19) 获证。此即「有限维 ODE 截断层」纪律之外部同构镜鉴：**区间/编译层 PASS 不外推为原命题层 PASS**。

## 二、失配二坐实摘录（压力通量上界项——式 (10.19)）

**NL 论文侧（p.123，式 (10.19)，本件转写）**：|∫ π w·∇χ_R| ≤ (C_T/R)[(B_R+1)B_R^{1/2} + R^{-3/4}B_R^{3/4}]——仅以 B_R（=‖φ_R⁴w‖₆）与 R 为参数。

**Lean 侧（`exists_uniform_actual_pressure_flux_bound` 之结论，同一记号转写）**：|∫ π w·∇χ_R| ≤ C_T[(B_R^{1/2}+1)(A_R/R + 1/R²) + R^{-7/4}B_R^{3/4}]——**引入 A_R（=(∫χ_R|∇w|²)^{1/2}）依赖**。

**失配文原文坐实（§3.2 图注及正文，逐字）**：
> "The Lean estimate introduces dependence on A_R, losing the paper's bound in terms of B_R alone. Equation (10.17) bounds B_R above using A_R; it cannot eliminate A_R from the Lean estimate to recover (10.19)."
> 证明方法双重改译（逐字要）：Paper 侧"Commutes multiplication by φ_R⁴ with R_iR_j…estimates the local pressure term in L^{3/2}, pairs it with an L^3 factor, and uses interpolation"；Lean 侧"Commutes multiplication by φ_R²…pairs the weighted stress in L^{6/5} with a Riesz-transformed test function in L^6, then bounds that test function using a Sobolev estimate involving its derivative. This introduces A_R/R."（相关 decl：`fluxTest_eq_multiplier_rTest`、`riesz_rTest_bound`/`localized_pair_bound`）

**本席判语**：失配二成立——**界形与证法双改译**；Lean 界含 A_R 项，且 (10.17) 不足以消去 A_R 回到 (10.19)（原文明言 cannot eliminate）——「同名定理号、异数学内容」之坐实。

## 三、SCI=∞ 论证骨架摘录（摘要＋§1/§4 要）

- 两类自动形式化之区分（§1，逐字要）：(i) 把 NL「证明」译为 Lean 证明（成功判据＝编译通过、无 sorry、无额外公理）；(ii) 数学文本之**语义忠实**翻译（定义/定理/证明及其依赖全保内容）。原文钉（逐字）："Meeting the success criterion of (i) does not mean that the original NL proof is correct."
- 核心定理向（摘要逐字）："the problem of resolving ambiguities in mathematical NL text … is arbitrarily high up in the Solvability Complexity Index (SCI) hierarchy/arithmetical hierarchy (the SCI = ∞). Hence, informally, providing semantically faithful AI autoformalisation is harder than any computational problem including the Halting problem (which has SCI = 1)."
- 骨架三段：①NL 歧义消解是语义忠实翻译之必要条件；②该消解问题在 SCI/算术层级中任意高（SCI=∞，严格高于停机问题 SCI=1）；③故类型 (i) 之「编译通过」证书对 NL 论证正确性**不提供证据力**——示例实证＝§2 两个初等例（错 NL 证→对 Lean 证；对 NL 证→异 Lean 证）＋§3 OpenAI NS 包两处失配（本件 §一/§二）。

## 四、对我仓之口径映射（名值分离：外部文之结论名 vs 我仓纪律钉）

1. OpenAI 包三钉维持逐字：「自评已核、外部复现中、未颁奖」——本文属「外部复现中」之**批评性预印本**一例，其自身亦为**待评审**文本（同行评审未竟），双向均不升级。
2. NS 纪律：本文一切内容限于 OpenAI 包 NL↔Lean 翻译忠实性之评析；我仓 NS 线表述继续限「有限维 ODE 截断层」语境，严禁「NS 已解决」；本文不触发 NS 线任何状态变更。
3. HWY 钉维持：HWY（Hou–Wang–Yang 全名）＝「待评审预印本，结论未确立」——本件未引 HWY 实质内容，纪律行照载。
4. ζ 线自律映射（同构镜鉴，非状态变更）：「编译/区间层 PASS ≠ 原命题层 PASS」与我仓 C2′「区间见证层 PASS、kernel 层未证、非 RH 证据」同构——kernel 层未证钉之必要性获外部独立论证支撑（登记，不构成我仓钉之外部背书升级）。

## 附 · 自检

1. 引文全部逐字并带页码/式号/decl 名/行号/commit 钉；本席判语与引文分行。
2. 性质钉先立：预印本 v1 2026-10-06、同行评审未竟；作者免责句照录。
3. 三组口径钉（OpenAI 包／NS／HWY）逐字在位；无「NS 已解决」、无越级表述。
4. 零 git 写；只交付不入库；本件为情报分析件，不改任何规程/裁决文本。

—— QF-OS 联邦批三十三 S4 外部情报精核席 · 2026-10-31 · arXiv:2610.08144 精核完毕（两处失配坐实＋SCI=∞ 骨架＋性质钉）· 零 git 操作
