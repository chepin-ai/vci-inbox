CLASSIFY: L1
# L34-FGL-SAMPLING-01 · R2B-06 FGL 主定理 5 条 NL↔Lean 抽样三层 diff 登记

- 席别：QF-OS 联邦批十六 L34 审计席（R2B-06）；规程依据 FIDELITY-AUDIT-PROTOCOL-L34-01（三层门禁：L3-4a 陈述层 → L3-4b 强度层 → L3-4c 证据层）
- 执行时戳：2026-10-25T09:37Z（环境时钟；批十六窗 10-27→10-30 派单，本件按执行时刻如实登记）
- 口径自检：涉 NS 语境一律限 C1「有限维 ODE 截断层」；涉 OpenAI 包沿唯一批准状态语「自评已核、外部复现中、未颁奖」；Clay NS 未解决、未颁奖。本件仅断言抽样层面对齐判定，不构成任何千禧问题证据链的一环；零代码搬运（CLEANROOM-REDLINE-FGL-01：数学陈述为公开学术内容可引用，代码不搬入联邦仓——本件引用的签名摘录仅为审计对照留痕，不构成移植）。
- 只读纪律：未做任何 git 变更，未改动任何既有文件一字节。

## 〇、版本锚（双侧钉死，均一手核验）

| 侧 | 锚 | 核验 |
|---|---|---|
| Lean | wwang-math/FluidGalerkinLean @ `4d023ac47aea65a4a5dbbc20004f5fda0ee18755` | portal 副本 /mnt/agents/output/work/FluidGalerkinLean `git rev-parse HEAD` 逐字符一致（本席亲跑） |
| NL | arXiv:2609.33033 v1（Weinan Wang，提交史唯一版本 [v1] Sun, 27 Sep 2026 00:02:19 UTC） | arxiv.org/abs 页 + /html/2609.33033v1 全文 HTML（704,372 B）本席亲取 |
| 编译证据 | SUP-04 GREEN（rc=0、3127/3127、5 主定理 #print axioms 白名单） | 在案，本次未重跑（只读窗） |

覆盖率声明：**5/5 探针定理双侧一手齐备（Lean 签名 5/5、NL 对应陈述 5/5），无降级**。但抽样框本身有缺口，如实登记：论文摘要之旗舰端点 Theorem 2.1（任意有界开域全局解，`OpenDomainGlobalBoundedEnclosure.exists_global_solution`）**不在** SUP-04 探针五定理之列——探针五定理全部为矩形盒域定理。本抽检因此不覆盖开域全局端点；另定理 6.1（有限维变分 Galerkin）、7.2（谱紧性）亦未入样。**抽样框 = 探针白名单 5 条，非论文主定理全集。**

## 一、映射表（编号归属钉桩，L3-4a 检查项 6）

| # | Lean 定理（签名出处） | NL 对应（arXiv 编号） | 粒度 |
|---|---|---|---|
| T1 | `exists_zeroForcing_twoDimensional_lerayHopfSolution`（BoxLerayHopf.lean:1613） | Theorem 2.2（Unforced 2D Leray–Hopf） | 1↔1 |
| T2 | `boxPoincare`（BoxPoincare.lean:190） | Proposition 5.5 式 (15) | 1↔1 |
| T3 | `boxForcing_work_le`（BoxPoincare.lean:249） | Proposition 5.5 式 (17) | 1↔1 |
| T4 | `exists_forced_twoDimensional_galerkinCompactness`（BoxForcedSpectralGalerkin.lean:550） | Theorem 9.1 **仅第二子句**（子列紧性） | 1 NL ↔ 3+ Lean：第一子句（逐层解存在+界 (36)）由仓内 `exists_forcedSolution2D`/`forcedSolution2D_norm_le`/`forcedSolution2D_energy_integral_le` 另行承担（PaperClaimChecks.lean L145–164 钉桩），**不在探针五条内** |
| T5 | `exists_forced_twoDimensional_lerayHopfSolution`（BoxForcedLerayHopf.lean:714） | Theorem 2.3（Forced 2D Leray–Hopf） | 1↔1 |

## 二、L3-4a 陈述层八要素对表（逐条）

### T1 · Thm 2.2 ↔ 零外力二维 Leray–Hopf

结论结构 `BoxLerayEnergyWeakSolutionOn`（BoxLerayHopf.lean:1498–1551，13 字段）逐项对照：

| 要素 | NL（Thm 2.2） | Lean | 判定 |
|---|---|---|---|
| 主语/空间 | u₀∈H_Q（盒上无散度 L²）；u_H∈L²(I;H_Q)、u_V∈L²(I;V_Q)、u_c:I→H_Q | `u₀ : BoxL2Sigma I`；`state`/`energy`/`weakState` 三代表 | 一致 |
| 假设 | a≤b；Q=[a₁,b₁]×[a₂,b₂] 非退化（a_i<b_i） | `(hab : a ≤ b)`；非退化经类型隐式携带——已一手核实 mathlib @8d6f23e `BoxIntegral.Box.lower_lt_upper : ∀ i, lower i < upper i`（Box/Basic.lean:80） | 一致（隐式假设已显式化回计，检查项 7 通过） |
| 结论谓词 | J u_V=u_H；u_c=u_H a.e.；u_c(a)=u₀；t↦(u_c(t),y) 连续；能量不等式 ∀t；弱方程 ∀φ∀η, η(b)=0 | `state_eq_energy`；`weakState_ae_eq_state`；`weakState_initial`；`weakState_inner_continuous`；`energy_inequality`（‖u_c(t)‖²+2∫‖G‖²≤‖u₀‖²，逐字同形）；`weak_equation`（三项=初值项，逐字同形） | 一致 |
| 量化次序 | ∀a≤b ∀u₀ ∃(u_H,u_V,u_c)；∀y ∀φ ∀η | 同（结构字段全称量化） | 一致 |
| 常数/界 | ‖u_H‖_{L∞}≤‖u₀‖；‖u_c(t)‖≤‖u₀‖；‖u_V‖_{L²(V)}≤R_I(u₀)=√(1+\|I\|)‖u₀‖ | `state_eLpNorm_top_le ≤ ofReal ‖u₀‖`；`weakState_norm_le ≤ ‖u₀‖`；`energy_norm_le ≤ zeroForcingEnergyRadius a b u₀`，该半径定义（BoxSpectralLadyzhenskayaCompactness.lean:514）= √((√μ(univ)·‖u₀‖)²+‖u₀‖²)，μ 为 Icc 上 Lebesgue（intervalSubtypeMeasure，BoxGalerkinSolutionBounds.lean:125）→ = √(1+\|I\|)‖u₀‖ | 一致（常数逐字符可对上） |
| 定义依赖 | H_Q/V_Q/J_Q/G_Q/b_Q（图空间闭包+斜对流形） | BoxL2Sigma/BoxH1ZeroSigma/boxEnergyToState/boxEnergyGradient/Ladyzhenskaya realization convectionForm | 抽查级一致（见 §五缺口 G2） |
| 边界条件 | 面无滑移+无散度（𝓓_σ(Q) 定义载明） | 类型 `*Sigma`/`H1Zero` 承载 | 抽查级一致 |
| 例外 | η∈C¹(I) | `LerayIntervalTimeTest`：value 在 Icc 内可导 + deriv 仅 interval-integrable 且 MemLp 2（VariationalGalerkinTimeTest.lean:20–25；LerayTimeTest.lean:100–104）——**测试类比 C¹ 更宽** | 方向性差异（Lean 结论更强，见 L3-4b），非失配 |

### T2 · Prop 5.5(15) ↔ `boxPoincare`

NL：∃C_Q≥0，‖J_Q v‖_{H_Q}≤C_Q‖G_Q v‖（∀v∈V_Q）。Lean：`theorem boxPoincare (v : BoxH1ZeroSigma I) : ‖boxEnergyToState I v‖ ≤ boxPoincareConstant I * ‖boxEnergyGradient I v‖`，常数为**显式定义见证**（`boxPoincareConstant := (boxPoincareENNReal I).toReal`，非负性另证 `boxPoincareConstant_nonneg`）。八要素逐项：主语/假设/结论/量化/定义依赖全对得上；NL 存在式 vs Lean 见证式——Lean 严格更强（给出具体常数）；NL 未给常数数值，故「常数数值比对」无对象，如实登记。**判定：一致（记号等价+见证强化）。**

### T3 · Prop 5.5(17) ↔ `boxForcing_work_le`

NL：ℱ∈V_Q′、f≥0、\|ℱ(w)\|≤f‖w‖（∀w）⟹ 2ℱ(v)≤(1+C_Q²)f²+‖G_Q v‖²_{L²}。Lean：`(F : BoxH1ZeroSigma I →L[ℝ] ℝ) (f : ℝ) (hf : 0 ≤ f) (hbound : ∀ w, ‖F w‖ ≤ f * ‖w‖) (v) : 2 * F v ≤ (1 + boxPoincareConstant I ^ 2) * f ^ 2 + boxGradientDiffusion I v v`；`boxGradientDiffusion_self`（BoxSobolevClosure.lean:291–296）证 `boxGradientDiffusion I u u = ‖boxEnergyGradient I u‖ ^ 2`。八要素逐项**字面一致**：常数 (1+C_Q²) 同形；实数范数=\|·\| 同义；假设形状（对偶范数主函数）同。**判定：一致（本次抽检中贴合度最高的一对）。**

### T4 · Thm 9.1 第二子句 ↔ `exists_forced_twoDimensional_galerkinCompactness`

NL 第二子句：∃m_k→∞，J E_{m_k}U_{m_k}→u_H 强于 L²(I;H_Q)，E_{m_k}U_{m_k}⇀u_V 弱于 L²(I;V_Q)，J u_V=u_H，每个固定有限维投影在 I 上一致收敛。Lean 结论 `StrongWeakPathSubsequence`（LeraySpectralWeakCompactness.lean:70–78，extends StrongWeakSubsequence:58–67）：`state_strong`（Lp 范数拓扑收敛=L² 强）；`energy_weak`（对一切 L² 测试内积收敛=Hilbert 空间弱收敛）；`embed_energyLimit`（J u_V=u_H）；`projected_uniform`（→ᵇ 有界连续函数 sup 范数收敛=一致收敛）；`ExtractedSubsequence` 严格子列。逐项对上。**判定：一致（限第二子句；第一子句归属仓内另三条定理，编号映射粒度差异登记为 F1）。**

### T5 · Thm 2.3 ↔ `exists_forced_twoDimensional_lerayHopfSolution`

假设：NL「admissible forcing + 控制函数 f」↔ Lean `BoxDualForcing`（BoxForcedSpectralGalerkin.lean:33–49：value=⟪rep,·⟫ Riesz 表示、continuous、bound 连续非负、`norm_le` 逐点界）——**逐字段一致**。结论结构 `BoxForcedLerayHopfSolutionOn`（BoxForcedLerayHopf.lean:597–651）：弱连续、初值、a.e. 一致、embed 恒等、能量不等式 (3) 逐字同形（含外力功项 2∫Φ(u_V)）、弱方程 (4) 逐字同形（含 ∫Φ(φ)η 项）。显式半径：NL R=(‖u₀‖²+(1+C_Q²)∫f²)^{1/2} ↔ Lean `stateRadius`=√(‖u₀‖²+∫workMajorant)，`workMajorant t=(1+boxPoincareConstant²)·bound²`（同文件:105–106）→ **R 逐字符可对上**；‖u_H‖_{L∞}≤R ↔ `state_eLpNorm_top_le`；‖G u_V‖≤R ↔ `gradient_norm_le ≤ stateRadius`；‖u_V‖≤√(1+\|I\|)R ↔ `energy_norm_le ≤ energyRadius`=√((√\|I\|·R)²+R²)（:150–154）。**判定：一致。**测试函数类同 T1 之扩大注记。

## 三、L3-4b 强度层四态判定（逐条）

| # | 四态判定 | 依据 |
|---|---|---|
| T1 | **等价～略强** | 结论字段全覆盖 NL 各谓词；弱方程测试类由 C¹ 扩至「可导+导数 L²」——全称量化域扩大 ⇒ 严格更强方向；无弱化项 |
| T2 | **更强** | 存在式 → 显式见证式（常数被钉为 boxPoincareConstant） |
| T3 | **等价** | 字面同形 |
| T4 | **等价**（限第二子句） | 收敛模式逐件对应；强弱通道+一致投影+严格子列全在 |
| T5 | **等价～略强** | 同 T1 测试类注记；半径界常数全对上 |

无「严格更弱」、无「不可比」、无单向弱化——**L3-4c 检查项 4（抗顺从性：单向弱化推定）未发现触发实例**。证法一致性抽检（检查项 4）：未做全主干引理链比对（FGL 只宣称形式化命题而非逐证明移植，且本窗只读），登记为未覆盖项 G3；未发现证法替换型迹象（Lean 侧路线=图空间+J*J 谱坐标，与 NL §5–§9 结构同名同序）。

## 四、L3-4c 证据层

1. 编译证据：SUP-04 GREEN 在案（rc=0、3127/3127、5 主定理 #print axioms=[propext, Classical.choice, Quot.sound]、零 sorry）——仅构成「Lean 陈述为真」之机器级证据，本窗未重跑。
2. 翻译缝审计：本件即翻译缝抽检工序本身；NL 侧取自 arXiv v1 全文一手 HTML（非联邦转录二手），Lean 侧取自钉定源树一手签名与结构定义（非登记件转述）。
3. 判定合成：5/5 单元 L3-4a 通过、L3-4b 等价/更强、L3-4c 编译证据在位 → **抽样单元级三层全过 5/5**（受 §五缺口限定）。

## 五、缺口与覆盖率（如实登记）

- **G1（抽样框缺口）**：探针五条均为矩形盒域定理；论文摘要旗舰 Theorem 2.1（任意有界开域全局端点 `OpenDomainGlobalBoundedEnclosure.exists_global_solution`）未入样。5 条 = 作者自选公理审计白名单，非随机抽样，存在选择偏差（端点定理通常是打磨最精处）。
- **G2（定义链深度）**：BoxL2Sigma/BoxH1ZeroSigma 与 NL H_Q/V_Q（𝓓_σ(Q) 闭包）的逐字等价、convectionForm 对 ∫(u·∇)v·w 的代表性与斜性、J_Q 紧性，本抽检核到「定义文档串+关键引理（boxGradientDiffusion_self、半径定义、BoxDualForcing 字段、Box.lower_lt_upper、时间测试结构）」层级，**未展开全部定义链至 measure-theoretic 基元**。失配若藏于该层（OpenAI 案 Lemma 8.6 型恰是常数/指数层——本抽检已覆盖常数层且全对上），残余风险集中在定义语义层。
- **G3（证法链）**：L3-4b 检查项 4 证法一致性仅做到路线级（图空间+谱坐标同名同序），未做主干引理链逐环比对。
- **G4（环境）**：未重新编译（只读纪律）；GitHub api 速率受限，mathlib Box 定义经 ghfast 镜像于钉 rev 一手取得（Box/Basic.lean:80）。

**覆盖率汇总**：探针单元 5/5 双侧一手；八要素 5×8=40 项全核（其中「定义依赖/边界条件」两项为抽查级而非全链级，余 30 项逐字级）；论文主定理全集覆盖 4/9 编号单元（Thm 2.2、2.3、9.1、Prop 5.5；未覆盖 Thm 2.1、6.1、7.2、Prop 5.1–5.4 等）；证法链 0%（路线级注记除外）。

## 六、结论：对「构建绿 = 陈述保真」的抽样层证据判定

1. **本次抽样未发现任何 NL↔Lean 失配**（无 OpenAI 2610.08144 案的差一阶型/证法替换型实例）；5 条主定理陈述层全部对齐、强度层无弱化——在抽样范围内，**「构建绿+公理白名单」伴随的陈述保真成立**，这对 W3 之「该案必有失配」的强形式构成**削弱证据**。
2. 但同等强度地**支持 W3 的程序性内核**：SUP-04 的 GREEN 本身（rc=0+白名单）对本次核出的任何潜在失配确无检出力——本件的全部对齐证据来自独立的陈述层人工工序，无一项可由编译绿灯推出。「编译通过 ≠ 判定通过」在本案再次结构性成立（此次是「编译通过 ∧ 抽样判定亦通过」，两事仍须分别证成）。
3. 对 GO 窗的含义：W3 建议之「FGL 主定理链 L34 抽样三层 diff」前置，本件已在探针 5 条范围内执行并 PASS（带 G1–G4 限定）；若判定席要求覆盖 Thm 2.1 开域端点与定义链全展开（G1/G2），需另派专窗——该两项是本件**未闭合**的残余风险，不构成对现行 5 条 PASS 的推翻，但构成对「FGL 全蓝本保真」外推的拒绝。

—— QF-OS 联邦批十六 L34 审计席 · R2B-06 · 执行于 2026-10-25T09:37Z · 只读、零 git 变更
