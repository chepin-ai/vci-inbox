CLASSIFY: L1

# INFINITY-CMC W5 批次提案 · sorry 普查重要性加权排序（WS-26 / PIVOT-01 联邦枢线 · M2 试点）

> **提案制**：本文档仅为排序提案。**采纳与否归原线（chepin-ai/infinity-cmc 驻留 Agent/用户）；覆写权归原线 lgt-118。** 本分线不推任何改动到 infinity-cmc。
> 基线锚：infinity-cmc @2692b2b9（WS-23 W4/S3 批次后）；sorry 实测 162 + axiom 7（注释/字符串剥离后词边界计数），与总账 164+10 减 W4 已清 5 项对账一致。
> 性质声明：本排序为**可计算代理启发式**（依赖扇出/解锁深度/层级权重加权和），**不是真 SHAP/因果重要性**；仅把附件文献的思想操作化为文本级静态指标。

## 1. 指标定义（代理启发式）

对全仓 10 个 .lean 文件做文本解析（剥离 `/- -/` 块注释与 `--` 行注释后）：

- **依赖扇出 fan-out**：该 sorry/axiom 所在声明的标识符，被仓内其他声明体引用的次数（词边界匹配；匿名 instance 归并到其实例目标的主类型，如 `instance : KählerManifold CICY58Manifold` → 归并 `CICY58Manifold`）。
- **解锁深度 unlock**：直接引用该声明的、自身含 sorry 的声明中所含 sorry 总数（传递闭包一层）。
- **层级权重**：T0=3 / T1=2 / T2=1。因 canonical 普查分层文档未在任何可达仓中找到（见 §5 数据缺口），层级由代理规则赋值：**T0 = fan-out ≥ 4，T1 = fan-out 2–3，T2 = fan-out ≤ 1**。实测分布 T0=19 / T1=43 / T2=107（共 169 项）；T0 落在总账分层带 15–25 内，T1/T2 与总账带（65 / 30–40）不符——如实标注分歧，原因见 §5。
- **综合分** = 0.5·(fan-out/33) + 0.3·(unlock/42) + 0.2·(层级权重/3)。权重沿用任务规定（0.5/0.3/0.2），归一化基数为全仓最大值。

## 2. W5 范围对齐

攻坚排期.md：W5 = S4 物理一 = **Phase2_Physics（28 sorry）：射影空间光滑结构、Kähler 导出、CW 复形；目标 28→≤8**，残余项带 issue 链接注释。排期只定文件级范围、未定项级顺序，故本提案与排期**无名单冲突**，做的是项级排序补足（排序对照见 §4）。

## 3. W5 批次提案：Phase2_Physics 28 sorry / 11 宿主声明排序

| 提案序 | 宿主声明 | sorry 行 | n | fan-out | unlock | 层级 | 综合分 |
|---|---|---|---|---|---|---|---|
| 1 | `inst:SmoothManifoldWithCorners@L51` | L54 | 1 | 33 | 42 | T0 | 1.000 |
| 2 | `inst:KählerManifold CICY58Manifold@L65` | L66,67,68,69 | 4 | 33 | 42 | T0 | 1.000 |
| 3 | `inst:SmoothManifoldWithCorners@L35` | L35 | 1 | 5 | 3 | T0 | 0.297 |
| 4 | `CICY58CellComplex` | L295,296,297,298,299 | 5 | 2 | 6 | T1 | 0.206 |
| 5 | `KählerForm` | L60,61,62 | 3 | 1 | 0 | T2 | 0.082 |
| 6 | `FirstChernClass` | L109 | 1 | 1 | 0 | T2 | 0.082 |
| 7 | `CICY58DerivedEquivalence` | L342,346,350,352,353,354 | 6 | 1 | 0 | T2 | 0.082 |
| 8 | `WeilPeterssonMetric` | L116,117,118,119 | 4 | 0 | 0 | T2 | 0.067 |
| 9 | `relicDensityConstraint` | L183 | 1 | 0 | 0 | T2 | 0.067 |
| 10 | `solutionUnique` | L257 | 1 | 0 | 0 | T2 | 0.067 |
| 11 | `moorePenroseConvergence` | L275 | 1 | 0 | 0 | T2 | 0.067 |

**建议 W5 清除集 = 提案序 1–7（21 个 sorry），残余 7 个（序 8–11）挂 issue 链接注释 —— 达成排期 28→≤8 验收口径（28→7）。**

理由要点：
- 序 1–2（CICY58Manifold 光滑/Kähler 实例簇，5 sorry）：全仓最大扇出枢纽（fan-out 33，unlock 42），Main.lean 主结论 `CICY58_CompleteVerification` 的 `infer_instance` 直接依赖；不消除则主结论第 1 分量永远悬置。
- 序 3（ProjectiveSpace 光滑实例，L35）：序 1 的上游——`CICY58Manifold` 是 `ProjectiveSpace 4 × ProjectiveSpace 4` 子类型，光滑结构须先备。**依赖序修正：执行时序 3 应先于序 1**（综合分未编码文件内定义先后，此处按源码依赖手动标注）。
- 序 4（CICY58CellComplex CW 结构，5 sorry）：排期 W5 三项主题之一「CW 复形」；unlock=6（导出三角等价 `CICY58DerivedEquivalence` 的 6 个 sorry 直接挂在它后面），Main 主结论第 4 分量依赖。
- 序 5–7（KählerForm / FirstChernClass / CICY58DerivedEquivalence）：排期主题「Kähler 导出」+ 主结论第 4 分量收口；KählerForm（序 5）是序 2 metric 字段的素材，执行时序 5 应先于序 2。
- 序 8–11（WeilPeterssonMetric / relicDensityConstraint / solutionUnique / moorePenroseConvergence）：零下游引用、物理数值验证类，不阻塞主结论，留作残余项挂 issue 最经济。

**依赖修正后的建议执行序**：L35 → L54 → KählerForm(L60–62) → KählerManifold inst(L66–69) → CICY58CellComplex(L295–299) → CICY58DerivedEquivalence(L342–354) → FirstChernClass(L109)。

## 4. WS-23 移交三前提（原 Main.lean axiom [107][110][114]）插队位置

W4 已将三 axiom 降格为带前提 theorem，前提解除移交 W5–W7。定位结果：

| 前提 | 解除目标（Lean 锚点） | 所在文件/排期 | 全局提案序 | 建议插队位 |
|---|---|---|---|---|
| [107] MirrorSymmetryProof | `CICY58Mirror` 占位定义（L49, 1 sorry）+ `MirrorPair` 实例化素材（Phase2_3 MirrorPair L277–279, 3 sorry） | Phase3_Advanced(W7) / Phase2_3_Continuation(W6) | 15 / 6 | **W6 之首**：Phase2_3 的 MirrorPair 簇全局序 6（T0），建议提到 W6 批第一项；Phase3_Advanced 的 CICY58Mirror 如资源允许可在 W5 尾部顺手清（仅 1 sorry，占位定义具体化），否则随 W7 |
| [110] SpectralSequenceComputation | `CICY58SpectralSequence`（L123–125, 3 sorry）+ `ConvergesTo` 收敛性 | Phase3_Advanced（W7） | 12 | **W7 之首**；不宜提前入 W5——其依赖 d²=0 谱序列微分块（同文件 L144–145、L114–115），属 W7 主题 |
| [114] AIFormalizationComplete | **无直接 sorry 锚点**：`ProofSketch`/`autoSolver`（Phase3_Advanced L156/L167）已无 sorry，但 `verified` 仅为 Bool 标志，前提解除 = 把 Bool 标志升级为真实证明项存在性，属 AI 管道语义改造 | Phase3_Advanced（W7）或更晚 | — | 不插队；建议在 W7 评审时按排期 R2 口径裁决「假设化保留 vs 语义改造」 |

## 5. 数据缺口与局限（如实声明）

1. **canonical 普查文档未找到**：总账「164 sorry + 10 axiom，T0(15–25)/T1(65)/T2(30–40) 分层」仅在 vci-inbox board/FIRST-STEPS-LEDGER-01（v26/v28 节）与 LAB-CLOSE-EXT06 中被转述，164 项清单与分层规则原文在 infinity-cmc、sorry-resolver、vci-inbox、HUB-MAIL 四仓（含 git 历史）均不存在。本文层级为**代理规则赋值**（fan-out 阈值），T0=19 落在 15–25 带内属巧合性一致，T1=43/T2=107 与总账带不符——可能总账分层只覆盖子集（三带合计 110–130 < 164），或分层维度不同（如按攻坚难度而非依赖度）。**禁止据本文反推总账分层原义。**
2. **跨文件同名合流**：仓内 26 个标识符在多文件重复定义（如 `CICY58Manifold` 在 Framework 与 Phase2_Physics 各有一份；各 Phase 文件互不 import，仅 Main import Phase1/Phase2_Physics/Phase3_Advanced）。文本级引用无法区分同名实体，fan-out 为**上界估计**。
3. **Mathlib 引用未剔除**：`SSet`、`ToricVariety` 等疑似真实/虚构 Mathlib 名被计入；虚构 import（如 `Mathlib.Geometry.Manifold.Kähler`）表明仓内声明关系本就不完整。
4. **unlock 仅一层**，未做传递闭包；文本解析不含 Lean  elaborator 语义，实例隐式使用（typeclass inference）不可见。
5. 综合分权重 0.5/0.3/0.2 为任务规定值，未做敏感性分析；序 8–11 四项同分（0.067），其内部次序任意。

## 6. 全局 Top-20（供 W6–W8 参考，详见 WS-26 报告）

| 序 | 文件 | 宿主声明 | sorry 行 | n | fan-out | unlock | 层级 | 综合分 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | InfinityCMC_Framework | `inst:KählerManifold CICY58Manifold@L287` | L288,289,290,291,292… | 8 | 33 | 42 | T0 | 1.000 |  |
| 2 | Phase2_Physics | `inst:SmoothManifoldWithCorners@L51` | L54 | 1 | 33 | 42 | T0 | 1.000 |  |
| 3 | Phase2_Physics | `inst:KählerManifold CICY58Manifold@L65` | L66,67,68,69 | 4 | 33 | 42 | T0 | 1.000 |  |
| 4 | InfinityCMC_Framework | `inst:DerivedTriangularEquivalence where@L503` | L513,515,516,519,520… | 16 | 3 | 22 | T1 | 0.336 |  |
| 5 | Phase3_Deep_Continuation | `CICY58NewtonPolytope` | L172 | 1 | 6 | 2 | T0 | 0.305 |  |
| 6 | Phase2_3_Continuation | `MirrorPair` | L277,278,279 | 3 | 5 | 4 | T0 | 0.304 |  |
| 7 | Phase2_Physics | `inst:SmoothManifoldWithCorners@L35` | L35 | 1 | 5 | 3 | T0 | 0.297 |  |
| 8 | Phase3_Deep_Dive | `c_instanton` | L176 | 1 | 4 | 4 | T0 | 0.289 |  |
| 9 | Phase3_Deep_Dive | `danilov_khovanskii_formula` | L73 | 1 | 3 | 4 | T1 | 0.207 |  |
| 10 | Phase4_Final_Push | `SWModulus` | L161 | 1 | 3 | 4 | T1 | 0.207 |  |
| 11 | Phase2_Physics | `CICY58CellComplex` | L295,296,297,298,299 | 5 | 2 | 6 | T1 | 0.206 |  |
| 12 | Phase3_Advanced | `CICY58SpectralSequence` | L123,124,125 | 3 | 3 | 1 | T1 | 0.186 |  |
| 13 | Phase3_Deep_Dive | `polar_dual_dimension` | L83 | 1 | 2 | 3 | T1 | 0.185 |  |
| 14 | InfinityCMC_Framework | `exteriorDerivative` | L142 | 1 | 3 | 0 | T1 | 0.179 |  |
| 15 | Phase3_Advanced | `CICY58Mirror` | L49 | 1 | 3 | 0 | T1 | 0.179 |  |
| 16 | Phase2_3_Continuation | `leray_serre_convergence` | L336,342 | 2 | 2 | 2 | T1 | 0.178 |  |
| 17 | Phase3_Advanced | `DifferentialSpectralSequence` | L144,145 | 2 | 2 | 2 | T1 | 0.178 |  |
| 18 | Phase3_Deep_Continuation | `PeriodRigidity` | L55 | 1 | 2 | 2 | T1 | 0.178 | axiom |
| 19 | Phase3_Deep_Continuation | `SingularityStructure` | L74 | 1 | 2 | 2 | T1 | 0.178 |  |
| 20 | Phase3_Deep_Continuation | `SingularityStructure` | L69 | 1 | 2 | 2 | T1 | 0.178 | axiom |

—— PIVOT-01 联邦枢线 执行分机 WS-26 · M2 试点 · 2026-10-11
