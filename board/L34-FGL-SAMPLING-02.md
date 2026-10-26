CLASSIFY: L1
# L34-FGL-SAMPLING-02 · R2 案一/案五裁决执行：净室动工硬前置四要素之 G1 补样 + G3 补链 + G4 重编译

- 席别：QF-OS 联邦批十八 L34′ 补样席；执行依据 ADJUD-R2-20261025-01.md 案一（修正升格四要素）与案五（Thm 2.1 入样）；规程沿用 FIDELITY-AUDIT-PROTOCOL-L34-01（三层门禁：L3-4a 陈述层 → L3-4b 强度层 → L3-4c 证据层）；首件 = L34-FGL-SAMPLING-01.md（下称「01 件」）
- 执行时戳：2026-10-25T20:00Z 起（环境时钟 UTC）
- 口径自检：涉 NS 语境一律限 C1「有限维 ODE 截断层」；涉 OpenAI 包沿唯一批准状态语「自评已核、外部复现中、未颁奖」；Clay NS 未解决、未颁奖。本件仅断言抽样层面对齐判定与构建行为登记，不构成任何千禧问题证据链的一环；零代码搬运（CLEANROOM-REDLINE-FGL-01：签名摘录仅为审计对照留痕，不构成移植）
- 只读纪律：portal 仓 /mnt/agents/output/work/FluidGalerkinLean 全程只读（构建在 /tmp 副本）；零 git 变更（portal 仓 `git status --porcelain` 干预前 0 行，本席未做任何提交/改写）；未改动任何既有文件一字节
- 数据纪律：不编数——一切数值（字节数、sha256、job 数、耗时）均来自本席当次命令输出原文

## 〇、版本锚复核（双侧钉死，本次一手复验）

| 侧 | 锚 | 本次复验 |
|---|---|---|
| Lean | wwang-math/FluidGalerkinLean @ `4d023ac47aea65a4a5dbbc20004f5fda0ee18755` | portal 副本 `git rev-parse HEAD` 逐字符一致；/tmp 构建副本同源（cp -a），构建树内 `git rev-parse HEAD` 同值、`git status --porcelain` 0 行 |
| NL | arXiv:2609.33033 v1（Weinan Wang，[v1] 2026-09-27 00:02:19 UTC 唯一版本） | 本次重取 arxiv.org/abs 页 + /html/2609.33033v1 全文 HTML，Thm 2.1 陈述与 §8 证法节逐字摘录自一手 HTML |
| 工具链 | leanprover/lean4:v4.30.0-rc1（仓内 lean-toolchain 逐字） | 自装 tarball 529,531,960 B，sha256 `37c2913cf41b49f33ab2eebc449d12394081817315c9f915af1ff43f1642de42`，`lean --version` 报 commit `714601baf118066cbf3f282361339c6d06665b2a`——与 01 件 §〇 及 SUP-02/04 钉逐项一致 |
| mathlib | rev `8d6f23e07b24c7dda53bb66ba1acaf7b99c9adf6`（lake-manifest.json） | 构建树 .lake/packages/mathlib `git rev-parse HEAD` 同值；八依赖包 rev 全对上 manifest |

## 一、G1 补样：Thm 2.1（任意有界开域全局解端点）三层 diff

### 1.1 Lean 陈述提取（钉 rev 源树一手）

`OpenDomainGlobalBoundedEnclosure.exists_global_solution`（OpenDomainGlobalBoundedEnclosure.lean:11–24）：

```lean
theorem exists_global_solution (U : Set (Fin 2 → ℝ))
    (hOpen : IsOpen U) (hBound : Bornology.IsBounded U) :
    ∃ (Q : BoxIntegral.Box (Fin 2)) (Ω : OpenDomainInBox Q),
      Ω.carrier = U ∧
      ∀ u₀ : OpenDomainL2Sigma Ω,
        Nonempty (OpenDomainGlobalLerayHopf.GlobalSolution Ω
          (boxLadyzhenskayaRealization Q) u₀)
```

结论结构逐层展开（全部一手读源）：

- `GlobalSolution`（OpenDomainGlobalLerayHopf.lean:22–27）三字段：`statePath : Ici 0 → OpenDomainL2Sigma Ω`（全局弱连续轨道）；`localSolution : ∀ n : ℕ, SolutionOn Ω L u₀ (Nat.cast_nonneg n)`（逐整数视界局部解族）；`state_restrict`（轨道与局部解在各 Icc 0 n 上逐点相等）。
- 派生结论四定理（同文件:62–122，均证出非假设）：`GlobalSolution.initial`（statePath 0 = u₀）、`.weaklyContinuous`（∀y，t↦⟪statePath t, y⟫ 连续）、`.energyInequality`（∀n∀t∈Icc 0 n，‖statePath t‖²+2∫_{Iic t}‖openDomainEnergyGradient Ω (energyPath s)‖²∂timeMeasure ≤ ‖u₀‖²）、`.weakEquation`（∀n ∀eta : LerayIntervalTimeTest 0 n，eta.value n = 0 → ∀φ，TestedEquation）。
- `SolutionOn`（OpenDomainLerayHopf.lean:20–36）六字段：`energyPath : Lp (OpenDomainH1ZeroSigma Ω) 2 (timeMeasure 0 T)`；`statePath : Icc 0 T → OpenDomainL2Sigma Ω`；`weaklyContinuous`；`state_eq_energy`（statePath =ᵐ openDomainEnergyToState ∘ energyPath）；`initial`；`energyInequality`；`weakEquation`。
- 空间定义（OpenDomainCore.lean）：`OpenDomainInBox Q`（:72–78：carrier 开 + carrier ⊆ interior Q）；`SmoothOpenDomainField`（:148–167：C¹、无散度、tsupport ⊆ Ω、速度/导数 L²——即 NL 之 𝓓_σ(Ω) 紧支 C¹ 无散度场零延拓）；`OpenDomainL2Sigma Ω` = 速度核对子在 L²(Q;ℝ²) 中闭包（:294–296）= H_Ω；`OpenDomainH1ZeroSigma Ω` = 图核对子在 L²×L² 中闭包（:288–290）= V_Ω；`openDomainEnergyToState`（:378）= J_Ω；`openDomainEnergyGradient`（:394）= G_Ω。
- 弱方程谓词 `TestedEquation`（OpenDomainConcreteWeakEquation.lean:82–95）经三层定义展开（OpenDomainWeakEquationLimit.lean:256–278）：`−∫⟪u,energyToBoxState φ⟫·η′ + ∫diffusionForm Ω (w t) φ·η + ∫convectionForm Ω E (w t) (w t) φ·η = ⟪u₀, energyToBoxState φ⟫·η 0`——三项+初值项结构与 NL 逐字同形。
- 包围盒存在性：`OpenDomainBoundedEnclosure.exists_openDomainInBox`（OpenDomainBoundedEnclosure.lean:34–39）：∀U 有界开 → ∃Q ∃Ω，Ω.carrier = U。

### 1.2 NL 陈述对照（arXiv:2609.33033 v1 §2，一手 HTML 摘录）

**Theorem 2.1 (Global solution on a bounded open domain).** Ω⊂ℝ² 有界开，取辅助矩形 Q 使 Ω̄⊂Q°；𝓓_σ(Ω)=Ω 内紧支 C¹ 无散度场零延拓至 Q；H_Ω = 其在 L²(Q;ℝ²) 闭包，V_Ω = 其速度–梯度图在 L²(Q;ℝ²)×L²(Q;ℝ^{2×2}) 闭包；J_Ω、G_Ω 为坐标映射，b_Ω 为连续对流形。对任意 u₀∈H_Ω：存在 u_c:[0,∞)→H_Ω 与逐整数 N≥0 的 u_V^N∈L²([0,N];V_Ω)，使 (i) u_c(0)=u₀；(ii) ∀y∈H_Ω，t↦(u_c(t),y) 连续；(iii) 在 [0,N] 上 J_Ω u_V^N = u_c a.e.；(iv) ∀t∈[0,N]，‖u_c(t)‖²+2∫₀^t‖G_Ω u_V^N(s)‖²ds ≤ ‖u₀‖²；(v) ∀φ∈V_Ω ∀η∈C¹([0,N]) η(N)=0，弱方程（−∫(u_c,J_Ωφ)η′ + ∫(G_Ωu_V^N,G_Ωφ)η + ∫b_Ω(u_V^N,u_V^N,φ)η = (u₀,J_Ωφ)η(0)）成立。

### 1.3 L3-4a 八要素对表（Thm 2.1 ↔ exists_global_solution）

| 要素 | NL（Thm 2.1） | Lean | 判定 |
|---|---|---|---|
| 主语/空间 | u₀∈H_Ω；u_c:[0,∞)→H_Ω；u_V^N∈L²([0,N];V_Ω) | `u₀ : OpenDomainL2Sigma Ω`；`statePath : Ici 0 → OpenDomainL2Sigma Ω`；`localSolution n` 之 `energyPath : Lp (OpenDomainH1ZeroSigma Ω) 2 (timeMeasure 0 n)` | 一致 |
| 假设 | Ω⊂ℝ² 有界开 | `(U : Set (Fin 2 → ℝ)) (hOpen : IsOpen U) (hBound : Bornology.IsBounded U)` + ∃Q 包围（Ω.carrier = U，carrier ⊆ interior Q） | 一致（包围盒 NL 行文为 Ω̄⊂Q°、Lean 构造为 Ω⊆Q°——Q 双侧均为存在量化，结论内容不依赖该强弱差；登记为定义注记 D1，非失配） |
| 结论谓词 | (i) 初值 (ii) 弱连续 (iii) J_Ωu_V^N=u_c a.e. (iv) 能量不等式 ∀t∈[0,N] (v) 弱方程 | (i) `GlobalSolution.initial` (ii) `.weaklyContinuous` (iii) `SolutionOn.state_eq_energy` (iv) `.energyInequality`（‖u_c‖²+2∫‖G‖²≤‖u₀‖² 逐字同形）(v) `.weakEquation`（三项=初值项，经 TestedEquation 展开逐字同形） | 一致（五谓词全覆盖） |
| 量化次序 | ∀u₀ ∃u_c；∀N≥0 ∃u_V^N；∀y ∀t ∀φ ∀η | ∀u₀ Nonempty GlobalSolution（statePath 一次给出，localSolution ∀n:ℕ）；结构字段全称量化 | 一致 |
| 常数/界 | 能量不等式常数 2、右端 ‖u₀‖²；无额外数值常数 | 同形（系数 2、右端 ‖u₀‖² 逐字符对得上） | 一致 |
| 定义依赖 | H_Ω/V_Ω（𝓓_σ(Ω) 闭包）、J_Ω、G_Ω、b_Ω、[0,N] 上 Lebesgue | OpenDomainL2Sigma/OpenDomainH1ZeroSigma（SmoothOpenDomainField 核：C¹+无散度+tsupport⊆Ω+L²，与 𝓓_σ(Ω) 逐字段对得上）；openDomainEnergyToState/openDomainEnergyGradient；convectionForm Ω = 盒对流形经等距包含限制（OpenDomainDualDerivative.lean:266–269）；timeMeasure = 区间限制 Lebesgue | 抽查级一致（同 01 件 G2 纪律：定义链核到文档串+关键定义层，未全展开至测度论基元） |
| 边界条件 | 无滑移经 H¹-紧支场闭包承载 | 类型层承载（tsupport ⊆ Ω.carrier ⇒ 盒面零值，`zeroDirichletVectorOnBox_of_support_subset` :123–140） | 一致 |
| 例外/测试类 | η∈C¹([0,N])，η(N)=0 | `LerayIntervalTimeTest 0 n` + `eta.value n = 0`：值在 Icc 内可导 + deriv 仅 interval-integrable 且 MemLp 2（同 01 件 T1/T5 注记）——测试类比 C¹ 更宽 | 方向性差异（Lean 结论更强），非失配 |

### 1.4 L3-4b 强度层四态判定

**等价～略强**（与 T1/T5 同向）：结论谓词全覆盖 NL (i)–(v)；弱方程时间测试类由 C¹ 扩至「可导+导数 L²」，全称量化域扩大 ⇒ 严格更强方向；无弱化项；无不可比项。抗顺从性检查（L3-4c 检查项 4 单向弱化推定）：未触发。

### 1.5 L3-4c 证据层

1. 仓内既有公理审计件 `OpenDomainGlobalAxiomAudit.lean` 载 `#print axioms OpenDomainGlobalBoundedEnclosure.exists_global_solution` 输出为 [propext, Classical.choice, Quot.sound]——该行为**仓内注释文本**，本次 G4 重编译后由本席自建探针独立复核（见 §三），不以仓内文本充证据。
2. 翻译缝审计：NL 侧 arXiv v1 一手 HTML；Lean 侧钉 rev 源树一手签名与结构定义。
3. 判定合成：L3-4a 八要素全核通过（定义依赖/边界条件两项为抽查级）、L3-4b 等价～略强 → **Thm 2.1 单元三层判定通过（陈述层与强度层）**；证据层机器级复核随 G4 结果落定。

## 二、G3 补链：证法主干链抽样（3 条链，引理级）

抽样比例登记（裁决授权本席自定）：对三条端点链（Thm 2.1、Thm 2.2、Thm 2.3）各抽**主干层**（端点定理 → 一级承重引理 → 二级承重引理），每条 4–8 环；方法 = 钉 rev 源文件 proof term 一手读（非 #print 机器导览——G4 构建完成前无编译器可用，构建完成后以存活探针补验环节点存在性；凡本表所列引理均附「文件:行」锚，可复验）。

### 链 A · Thm 2.1 ↔ `exists_global_solution`（对照 NL §8 Proof of Theorem 2.1）

| 环 | NL §8 步骤 | Lean 环节点（锚） | 判定 |
|---|---|---|---|
| A1 | 取 Q 使 Ω̄⊂Q°，𝓓_σ(Ω) 零延拓入 𝓓_σ(Q)，V_Ω/H_Ω 为闭子空间 | `exists_openDomainInBox`（OpenDomainBoundedEnclosure.lean:34–39）+ `SmoothOpenDomainField.toBoxField`（OpenDomainCore.lean:175–188）+ `openDomainH1ZeroSigma_le`/`openDomainL2Sigma_le`（:351–359） | 对齐 |
| A2 | J_Ω 紧、值域稠密、单射；紧谱构造给出有限维空间与投影 | `openDomainCompactSpectralRepresentation Ω`（OpenDomainSpectral.lean:53–66：CompactGelfandTriple.spectralRepresentation 作用于 openDomainEnergyToState）+ `openDomainEnergyToState_denseRange`（OpenDomainCore.lean:462） | 对齐 |
| A3 | 逐整数视界 [0,N] 解系数方程，斜消去 ⇒ 精确能量等式 ⇒ 一致界 | `OpenDomainLerayHopfStatement.exists_solution_on`（OpenDomainLerayHopfStatement.lean:39–60：经 `OpenDomainConcreteCompactFamily.exists_strongWeakPathSubsequence`） | 对齐（能量等式层在深部，链外注记：该环本抽样样到一级接口） |
| A4 | 跨视界一致性：ODE 唯一性 ⇒ 短视界限制相容 | `OpenDomainGlobalLocalSolutions.solution_statePath_eqOn`（OpenDomainGlobalLocalSolutions.lean:46–58）经 `D.weakStatePath_eqOn` | 对齐 |
| A5 | 整数视界对角抽取：一条子列在每个视界强 L²(H_Ω) + 弱 L²(V_Ω) | `OpenDomainGlobalProjectedCompactness.exists_projectedSubsequence`（OpenDomainGlobalProjectedCompactness.lean:195–213+：`OpenDomainGlobalWeakCompactness.exists_strongWeakSubsequence` + `CountableCompactSubsequence.exists_coordinatewise_convergent` 逐 (视界 i.1, 投影 j) 坐标收敛） | 对齐（NL「对角抽取+逐投影一致收敛」= Lean ProjectedSubsequence 构造本身） |
| A6 | 重叠识别：lim P_j u^N = lim P_j u^M，P_j 自伴 ⇒ 代表元逐点相等；任意含 t 的视界定义 u_c(t) | `statePathOfSubsequence`（OpenDomainGlobalLerayHopf.lean:29–33：以 Nat.ceil t 视界定义）+ `statePathOfSubsequence_restrict`（:35–46）+ `solutionOfSubsequence`（:48–53） | 对齐 |
| A7 | 弱连续、初值、能量不等式、弱方程随限制成立 | `GlobalSolution.weaklyContinuous`（:73–102）/`.initial`（:62–65）/`.energyInequality`（:104–113）/`.weakEquation`（:115–122） | 对齐 |

**链 A 判定：7/7 环对齐，无失配、无证法替换迹象**（双侧同为「逐视界 Galerkin → 对角抽取 → 重叠识别 → 全局轨道」路线，逐环同名同构）。

### 链 B · Thm 2.2 ↔ `exists_zeroForcing_twoDimensional_lerayHopfSolution`（对照 NL §7.2 Proof of Theorem 2.2 + 图 2）

| 环 | NL §7.2 步骤 | Lean 环节点（锚） | 判定 |
|---|---|---|---|
| B1 | Prop 5.10/5.11：J*J 谱定理 ⇒ 成对基、Galerkin 空间、提升 E_m、测试投影 | `boxCompactSpectralRepresentation I`（BoxSpectralCompactness.lean:28） | 对齐 |
| B2 | Thm 7.2：谱紧性 ⇒ 子列 m_k 强 L²(I;H_Q)；Hilbert 弱紧 ⇒ 弱 L²(I;V_Q)；同一子列 | `exists_zeroForcing_twoDimensional_strongWeakPath_subsequence`（BoxLerayWeakCompactness.lean:83–89）= `exists_strongWeakSubsequence`（:68–81，LeraySpectralCompactFamily 抽象机）+ `SW.exists_pathwiseRefinement` | 对齐 |
| B3 | 对角子列 ⇒ 每个固定有限投影一致收敛 | `exists_pathwiseRefinement`（B2 内第二分量；结构 `StrongWeakPathSubsequence` 之 `projected_uniform`，01 件 T4 已核字段语义） | 对齐 |
| B4 | J u_V = u_H（Bochner 空间 J 诱导映射连续） | `base.embed_energyLimit`（经 `zeroForcingLeraySpectralCompactFamily2D_embed`，BoxLerayHopf.lean:1570–1573 引用点） | 对齐 |
| B5 | 弱连续代表 u_c、u_c=u_H a.e.、u_c(a)=u₀、逐点界 ‖u_c(t)‖≤‖u₀‖ | `zeroForcingWeaklyContinuousStateRepresentative`（BoxLerayWeakCompactness.lean:107–122）+ `zeroForcing_statePath_initial`（:127–140，经 `canonicalSolution_initial` = NL「Galerkin 初值 = u₀ 之正交投影」） | 对齐 |
| B6 | 能量不等式：X_k(t)=(u_k(t),√2 R_t G u_k) 在 H_Q⊕₂L² 中弱收敛 + 弱下半连续 | `zeroForcing_localEnergyInequality`（BoxLerayHopf.lean:1262–1273+：`restrictedGradientTimeMap` + `pointwise_weak_subsequence`，同一直和弱下半连续路线） | 对齐 |
| B7 | 对流极限：Ladyzhenskaya ⇒ L²(I;L⁴) 强收敛 + 斜性 + Hölder ⇒ 弱方程 | `zeroForcing_limit_timeTested_identity`（BoxLerayHopf.lean:822–，经 `zeroForcing_physicalConvectionIntegral_tendsto`，测试 η(b)=0 逐字） | 对齐 |

**链 B 判定：7/7 环对齐，无失配。**路线级→引理级升级后，01 件 §三之「同名同序」注记逐环坐实；未见 OpenAI 案型证法替换。

### 链 C · Thm 2.3 ↔ `exists_forced_twoDimensional_lerayHopfSolution`（对照 NL §9 Proof of Theorem 2.3）

| 环 | NL §9 步骤 | Lean 环节点（锚） | 判定 |
|---|---|---|---|
| C1 | Thm 9.1 供应子列、极限 u_H/u_V 与半径 R 一致界 | `exists_forced_twoDimensional_strongWeakPath_subsequence`（BoxForcedSpectralGalerkin.lean:534–543；族 `forcedLeraySpectralCompactFamily2D` 载 R=`stateRadius`） | 对齐 |
| C2 | u_c 构造与逐点界沿 Thm 2.2 之构（‖u₀‖↦R） | `forcedWeaklyContinuousStateRepresentative` + `forcedFamily_stateRadius`（BoxForcedLerayHopf.lean:662–684 引用点） | 对齐 |
| C3 | Eq.(4)：以 P^V_{m_k}φ 测试，外力项误差 ≤‖Pϕ−ϕ‖·∫f‖η‖ → 0 | `forced_limit_timeTested_identity`（BoxForcedLerayHopfLimit.lean:968–） | 对齐 |
| C4 | Eq.(3)：W_t(w)=(𝟏_{[a,t]}r,w) 有界泛函 + 有限能量等式 + 弱下半连续 | `forced_localEnergyInequality`（BoxForcedLerayHopf.lean:477–） | 对齐 |
| C5 | 组装：BoxForcedLerayHopfSolutionOn 全字段 | `forcedLerayHopfSolutionOfStrongWeakPath`（BoxForcedLerayHopf.lean:657–691）→ `exists_forced_twoDimensional_energyWeakSolution`（:696–702）→ 端点（:714–721，canonical S） | 对齐 |

**链 C 判定：5/5 环对齐，无失配。**

### G3 汇总

- 抽样 3 条链（案一要求 T1/T5 两条，本席增 Thm 2.1 一条以配套 G1），共 19 环，**对齐 19/19，失配 0**。
- 残余限定（如实登记）：本抽样为主干层（端点→一/二级承重引理），未展开至全部叶级证明脚本；A3 之「精确能量等式」等深部环节以接口存在性+类型签名核，未逐 tactic 复读。证法链覆盖率由 0% 升至「三端点主干 19 环」，非全链。

## 三、G4 重编译：钉 rev `4d023ac` 全量重建 + 公理白名单复核（本席当次一手）

**结局：GREEN（rc=0 + 3127/3127 + 6 定理公理白名单 + 零 sorry）。** 非复用 SUP-04 旧证，系本次在 /tmp 副本全新构建。

### 3.1 环境钉（与 SUP-02/04 逐项一致）

- 构建树：/tmp/fgl-l34r/src（portal 副本 cp -a；portal 仓全程只读）；构建前 `git rev-parse HEAD` = `4d023ac47aea65a4a5dbbc20004f5fda0ee18755`，`git status --porcelain` = 0 行。
- 工具链：自装 lean-4.30.0-rc1-linux，tarball 529,531,960 B、sha256 `37c2913cf41b49f33ab2eebc449d12394081817315c9f915af1ff43f1642de42`、`lean --version` commit `714601baf118066cbf3f282361339c6d06665b2a`（经 ghfast 镜像下载；直连 github TLS 在本环境不可用，与 SUP-01 记录在案事实一致）。
- 依赖：`lake exe cache get` 终态 rc=0、「No files to download」（首轮克隆+缓存已就位后之复跑确认）；mathlib HEAD = `8d6f23e07b24c7dda53bb66ba1acaf7b99c9adf6`（与 manifest 钉逐字符一致）；batteries/aesop/Qq/Cli/plausible/proofwidgets/importGraph/LeanSearchClient 八包 rev 全部与 lake-manifest.json 对上；mathlib 缓存落地 .olean 计 7902 件。
- 加固规程：构建日志由独立 sync 守护每 240s（≤5min 达标）增量 cp 至 /mnt/agents/output/fgl-build-log/l34r-g4/（sync-daemon.log 逐拍留痕，自首拍 20:18:24Z 至末拍连续）；本窗未发生命名空间擦除，无 BLOCKED 情形，零 retry。

### 3.2 构建终态（/mnt/agents/output/fgl-build-log/l34r-g4/ 全量在案）

- `BUILD_RC.txt`：`BUILD_RC=0 ELAPSED_S=13931 START=2026-10-25T20:18:24Z END=2026-10-26T00:10:35Z JOBS=3127/3127 PROBE_RC=0`。
- `build-full.log`：末行 `Build completed successfully (3127 jobs).`；✔ 行 105 条（仅实编模块打印，mathlib 全缓存命中不打印）；`grep -ci error` = **0**。jobs 终数 3127 与 SUP-04 逐字符一致；并行度实测 2 个 lean 进程并发（2 核机默认，同 SUP-04）。
- 耗时 13,931s（SUP-04 为 13,776s，同量级）；重件抽对：BoxLerayHopf 1154s（SUP-04：1162s）、OpenDomainUnforcedGalerkin 1522s（SUP-04：1441s）——同一量级，无异常膨胀。
- 构建树赛后 `git status --porcelain`（剔除 untracked）= 0 行：tracked 源文件零改动（仅 .lake 未跟踪物与本席探针文件 L34RProbe.lean 为新增未跟踪，均在 /tmp 副本，不触 portal）。

### 3.3 公理审计探针（本席自建 /tmp 探针，非仓内文件；`axioms-probe-output.txt` 原文）

```
'OpenDomainGlobalBoundedEnclosure.exists_global_solution' depends on axioms: [propext, Classical.choice, Quot.sound]
'exists_zeroForcing_twoDimensional_lerayHopfSolution' depends on axioms: [propext, Classical.choice, Quot.sound]
'boxPoincare' depends on axioms: [propext, Classical.choice, Quot.sound]
'boxForcing_work_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'exists_forced_twoDimensional_galerkinCompactness' depends on axioms: [propext, Classical.choice, Quot.sound]
'exists_forced_twoDimensional_lerayHopfSolution' depends on axioms: [propext, Classical.choice, Quot.sound]
```

PROBE_RC=0。**6/6 仅标准三公理，无 sorryAx、无自定义公理**——其中 Thm 2.1 端点（首行）系本次新入样定理，白名单与原五条同格；仓内 `OpenDomainGlobalAxiomAudit.lean` 注释所载输出获独立复核成立。

### 3.4 源树对抗扫描（portal 钉树，本次一手）

- `sorry`/`admit` 全树 grep（107 个 PDEIdeas .lean + 根部，含注释与标识符子串口径的宽匹配复核）：**计 0**；`sorryAx` 引用 **计 0**；`axiom` 声明：**0 条**（仅 PaperAxiomAudit.lean 注释行提及 axioms 字样）。

### 3.5 G4 对 01 件的更新

01 件 §五 G4「未重跑编译」**销记**：本次重编译 GREEN 与 SUP-04 结论一致（rc=0、3127/3127、白名单同），且把 Thm 2.1 端点纳入公理审计。「编译通过 ≠ 判定通过」结构性立场不变——本节证据仅支撑「陈述为真之机器级证据在位」，陈述保真判定由 §一/§二人工工序独立承担。

## 四、四要素履行状态表（对 ADJUD-R2-20261025-01 案一验收口径）

| 要素 | 状态 | 证据锚 |
|---|---|---|
| ① 现行 5 条 PASS 登记有效 | **履行** | 01 件三层全过 5/5；本件 §〇 双侧钉复验一致，无推翻项 |
| ② G1 补样（Thm 2.1 三层 diff） | **履行** | 本件 §一：八要素全核一致（定义依赖/边界条件为抽查级，沿 01 件 G2 纪律）、强度层等价～略强、证据层随 §三 GREEN 落定——三层齐备 |
| ③ G3 补链（主干引理链抽样） | **履行**（抽样式，非全链式，符合裁决「抽样式而非全链式」口径） | 本件 §二：3 链 19 环全对齐、0 失配；残余限定（深部叶级未展开）如实登记 |
| ④ G4 重编译一次 | **履行** | 本件 §三：rc=0、3127/3127、6 定理白名单、零 sorry、日志全程 ≤5min 增量同步出 /tmp 至 portal，无环境杀、无 retry |

**四要素齐备：硬前置之 L34 侧义务全部履行。** 残余风险登记（不构成未履行，供判定席裁量）：(a) G2 定义链深度限定自 01 件沿袭未扩（本次未派该窗）；(b) G3 为主干抽样而非全链；(c) 论文主定理全集覆盖由 4/9 升至 5/9 编号单元（Thm 2.1 入样），Thm 6.1、7.2、Prop 5.1–5.4 仍未入样。

## 五、结论性判定（抽样层）

1. Thm 2.1 开域全局端点 NL↔Lean **对齐**（陈述层八要素全过、强度层等价～略强、证据层 GREEN+白名单）；G1 缺口闭合。论文摘要旗舰句（任意有界开域全局 Leray–Hopf 弱解存在，「有限维 ODE 截断层」语境下的 Galerkin 构造）之 Lean 对应物在钉 rev 下逐要素核到，未发现失配。
2. 证法主干链 3 条 19 环**全对齐**——开域全局链（§8↔OpenDomainGlobal* 六文件链）、盒域无力链（§7.2↔BoxLerayHopf/BoxLerayWeakCompactness）、盒域受迫链（§9↔BoxForced*）逐环同名同构；未发现证法替换型迹象；G3 由 0% 升至主干抽样级。
3. 钉 rev 重编译 GREEN 独立复现 SUP-04 结论（rc=0、3127/3127、三公理白名单扩至 6 定理含 Thm 2.1）；G4 销记。
4. 程序性内核复核不变：上述全部对齐判定无一可由构建绿灯推出；「编译通过 ≠ 判定通过」继续成立。对「FGL 全蓝本保真」之外推口径由 01 件「拒绝」升级为「**在 5/9 编号单元+三端点主干链范围内有限成立**」，残余单元（Thm 6.1/7.2/Prop 5.1–5.4）与定义链全展开（G2）仍为未闭合项，不建议据此外推至未覆盖部分。

—— QF-OS 联邦批十八 L34′ 补样席 · R2 案一/案五执行 · 执行窗 2026-10-25T20:00Z→2026-10-26T00:15Z · portal 只读、零 git 变更、不编数
