CLASSIFY: L1
# FGL-SEAM-SPEC-01-REVIEW-01 · 非转写人复核记录（CLEANROOM-REDLINE-FGL-01 §3）

- **复核席署名**：QF-OS 联邦 CLEANROOM-REDLINE-FGL-01 §3 非转写人复核席（EXT19 复核轨；与 Reader 转写人无涉，未参与规格撰写）。
- **复核日期**：2026-10-21。
- **复核对象**：specs/FGL-SEAM-SPEC-01.md（218 行，自指 SHA-256=9c0e0acd…5f7a99）。
- **取材核验源**：`$HOME/fgl-ro` 不在，按预案 `git clone https://ghfast.top/https://github.com/wwang-math/FluidGalerkinLean $HOME/fgl-review && git checkout 4d023ac47aea65a4a5dbbc20004f5fda0ee18755`；`git rev-parse HEAD` 复现指定哈希（107 个 PDEIdeas 文件）。FGL 客观定性：Weinan Wang 单人 + LLM 辅助、零 sorry、无许可证（licenseInfo=null，默认保留全部权利）。本席仅直读 FGL 源核对数学内容，未做任何 diff/相似度镜像比对，未触碰我方 library 实现文件。

---

## 清单 1 · 数学正确性抽查（12 构件，跨四单元）——判定：通过

| # | 规格构件 | FGL 侧文件 | 数学对照（一句话） |
|---|---|---|---|
| 1 | 单元① 1.1 能量抵消/斜对称 | PDEIdeas/GalerkinSystem.lean | `cancel: ⟪bilin u u, u⟫=0` 为结构字段，`cancel_of_skew` 给出「后两变元反对称 ⇒ 三次抵消」，与规格两个要点逐项相符。 |
| 2 | P1（右端估计） | PDEIdeas/VariationalGalerkin.lean（`rhs_norm_le`、`rhsLipschitzConstant`） | ‖r(t,u)‖≤‖d‖‖u‖+C_b‖u‖²+‖F(t)‖ 逐字相符；球上 Lipschitz 常数恰为 ‖d‖+2C_bR，与规格一致。 |
| 3 | P3（Galerkin 层精确能量等式） | PDEIdeas/VariationalGalerkin.lean（`LocalSolutionOn.energyIdentityOn`） | ‖u(b)‖²+2∫d(u,u)=‖u(a)‖²+2∫F(u)，证明路径（斜对称消对流 + FTC）与规格素描一致。 |
| 4 | P5（能量预算全局延拓） | 同上（`exists_solutionOn_of_energy_budget`） | 统一步长 δ=1/(C+1)、C=‖d‖(R+1)+C_b(R+1)²+M、可达终点集上确界反证，常数与论证结构均复现。 |
| 5 | P7（有限模等度连续+谱尾 ⇒ 强 L²_tH） | PDEIdeas/GalerkinL2Compactness.lean（`totallyBounded_range`、`exists_stronglyConvergent_subsequence`、`compactEmbedding_projectorTail_tendsto`） | 「紧嵌入 ⇒ 尾投影算子范数 →0」与「逐模数紧逼近 ⇒ 值域全有界 ⇒ 强子列」两构件均在，规格概括忠实。 |
| 6 | P8（强-弱同步抽取、伴随识别极限） | PDEIdeas/LeraySpectralWeakCompactness.lean | 模块头明言「时空嵌入的伴随识别两个极限」，`exists_pathwiseRefinement` 给出同子列双收敛，与规格 (i)–(ii) 相符。 |
| 7 | Q1（平面 Ladyzhenskaya，C_L=2·C_GNS） | PDEIdeas/BoxLadyzhenskayaInequality.lean | `planeLadyConstant = 2 * GNS常数`；对 q=‖u‖² 用全空间 GNS、∇q=2⟨u,∇u⟩、Hölder，假设（C¹ 紧支平面向量场）与结论指数逐项相符。 |
| 8 | Q3（盒 Poincaré） | PDEIdeas/BoxPoincare.lean（`boxPoincare`） | GNS 用于 u 本身得 L²≤C‖∇u‖_{L¹}、盒内紧支经 Hölder 转 L²，闭包延拓到能量空间，与规格路线一致。 |
| 9 | Q5（ODE 层唯一性） | PDEIdeas/VariationalGalerkinUniqueness.lean（`eqOn_of_bounded`） | 两条半径 R 有界解在公共区间 EqOn，球上 Lipschitz + Picard 唯一性，与规格一致。 |
| 10 | S2（谱坐标恒等式与权） | PDEIdeas/CompactEmbeddingSpectral.lean | Gram 算子紧/自伴/正/单射；Je_i=σ_i φ_i 与 ⟨Ju,φ_i⟩=σ_i⟨u,e_i⟩ 两恒等式即结构字段 `basis_map`/`basis_inner`；权 ≤1（`compactEmbeddingWeight_norm_le_one`）在 FGL 中以「J 收缩」为显式假设证得——规格表述「把 J 换为 ‖J‖⁻¹J 吸收」为等价数学读法，可接受（差异登记见清单 4 注 a）。 |
| 11 | S5（子空间转移，稠密性不遗传） | PDEIdeas/CompactSubspaceEmbedding.lean（`denseRange_iff`、`isCompactOperator`） | 紧性沿闭嵌入下降、单射继承、稠密性判据恰为 H′⊆closure(J(V′))，与规格逐点相符。 |
| 12 | G1/G2/G4/G5（开域链） | PDEIdeas/OpenDomainCore.lean、OpenDomainBoundedEnclosure.lean、OpenDomainGlobalLerayHopf.lean、PaperClaimChecks.lean | 拓扑支集含于 Ω ⇒ 盒边界条件自动（`zeroDirichletVectorOnBox_of_support_subset`）；围合 `exists_box` 取 R=max 1 (C+1)（规格「坐标上界加一」为其主旨，精度注记见清单 4 注 b）；全局打包=全局路径+逐 [0,n] 局部解族+限制相容、性质作投影定理（`GlobalSolution` 三字段与 `weaklyContinuous/energyInequality/weakEquation` 定理）；PaperClaimChecks 钉住的类型确认全局解仅无迫、受迫仅盒有限时域（`exists_zeroForcing_twoDimensional_lerayHopfSolution` 与 BoxForcedLerayHopf 范围），G5 诚实边界属实。 |

另核：单元① 1.1 Leray–Hopf 三元组定义（OpenDomainLerayHopfStatement.lean `SolutionOn`：能量路径 L²、状态路径、a.e. 相容 u(t)=Jũ(t)、弱连续、初值、能量不等式、时间测试弱方程七字段）与规格 (i)–(iv) 相容；盒 Rellich 紧性确经 Fourier 证明（`boxEnergyToState_isCompactOperator_fourier`，G1 括注属实）。抽查未发现假设/结论/条件层面的失真。

## 清单 2 · 红线合规独立核验——判定：通过

- **零 Lean 标识符/tactic/代码**：对全文做驼峰标识符扫描（剔除方括号来源元数据与数学专名后）零命中；通读未见任何 FGL 声明名、tactic 结构或代码片段。方括号路径仅作来源元数据，符合红线 §2/§5 的引用惯例。
- **摘要隔离**：以「未见 FGL 的 Writer」视角通读，全部构件均以数学需求语言陈述（定义—命题—证明素描—依赖图），无「见某文件某行」式不可理解指涉；接口注记 §6 只述数学性质需求。隔离成立。
- **逐行搬译迹象**：规格按「数学机制」重组（四单元 + 依赖图 + 接口注记），与 FGL 的文件划分/声明顺序不构成逐段对应；命题编号（P/Q/S/G）为规格自建体系。未见结构同构度过高段落。
- 红线 §4（禁镜像比对）：本席复核方式为「直读 FGL 源核对规格数学陈述」，未使用 diff/相似度工具对照任何我方实现，合规。

## 清单 3 · 哈希复算——判定：**不复现（不中）**

- 约定口径「剔除哈希字段行后计算 SHA-256」实测：`8cd7bc6fcf4d55d83791a5390e8ca2d361dd1459af257ee66ac8aeef26178415` ≠ 自指值 `9c0e0acd…5f7a99`。
- 已系统尝试的替代口径均不中：剔除行后去/留结尾换行、哈希值置空/置 TBD/置 64 个 0、删去值+括注、截断于哈希行之前、剔除 §7.2 元数据行的全部子集组合（含 209–216 行范围、3 种结尾换行处理）、CRLF 变体。
- **定位结论**：差异不像换行/编码问题（文件为 UTF-8/LF，剔除行后字节级复算稳定），最可能是填入哈希字段后文件又经编辑（如尾部 §7.2 或署名行微调），或 Reader 计算哈希时所依据的缓冲内容与落盘终稿不一致。规格正文完整性不受影响，但**自指哈希当前不可验证**，需 Reader 线按约定重算重钉（修订权属 Reader 线，本席不动文件）。

## 清单 4 · 充分性判断——判定：自足（一处措辞建议收紧）

- **自足性**：规格含定义层、命题层（含显式常数与条件）、证明策略素描、单元内/间依赖图、FGL 覆盖边界的诚实注记（Q6、G5、G6），Writer 轨无需回查 FGL 即可实现接缝；未发现必须回查源仓库的缺口。Q6 的「目标构件清单 + 诚实性注记」处理恰当（FGL 未含 PDE 层唯一性，规格明确标注为我方自建需求）。
- **接口注记 2 的 Fourier 理解**：同意技术席 EXT19 R1 精度注记——现文「可用 Fourier 或直接的全空间定理于周期函数」中「直接的全空间定理于周期函数」表述过松：全空间 GNS/Ladyzhenskaya 以紧支（或衰减）为前提，不可直接套用于一般周期函数；周期情形的标准路线是环面自身的不等式（Fourier 级数 + 零均值 Poincaré，或周期 Sobolev 嵌入定理）。**建议修订句**（仅建议，改权属 Reader 线）：
  > 将「（无紧支要求，可用 Fourier 或直接的全空间定理于周期函数，均值条件按所取空间处理）」改为「（无紧支要求；证明应走环面自身路线——经 Fourier 级数与零均值 Poincaré 直接建立 𝕋² 上的 GNS/Ladyzhenskaya，或引用周期 Sobolev 不等式的独立定理；全空间紧支版本不可直接套用于周期函数，均值条件按所取空间处理）」。
  该收紧不改变接口注记的需求实质（Q1–Q4 理解为「在所用域上成立」），属措辞精度补强，不阻塞交付。
- **其他精度注记（非阻塞）**：(a) S2 权 ≤1：FGL 以「J 收缩」为显式假设证权 ≤1，规格「换 ‖J‖⁻¹J 吸收」为等价数学读法，可保留；(b) G2 围合常数：FGL 取 R=max 1 (C+1)，规格「坐标上界加一」略去与 1 取大的细节，数学主旨一致。

---

## 总判

**补强后可交付 Writer 轨**。数学内容经 12 构件跨四单元抽查忠实于 FGL @4d023ac；红线 §1–§5 合规独立核验通过；摘要隔离成立。两处非数学性补强后方可放行：(1) 自指 SHA-256 复算不中，需 Reader 线按约定重算重钉并在取材日志登记原因；(2) 接口注记 2 按上方建议句收紧 Fourier 路线表述（采纳 EXT19 R1 精度注记）。两项均属 Reader 线小改，不涉及规格数学骨架，无需重新复核全规格，改动后由 Reader 线回填复核指针即可。

——QF-OS 联邦 CLEANROOM-REDLINE-FGL-01 §3 非转写人复核席（EXT19 复核轨）· 2026-10-21
