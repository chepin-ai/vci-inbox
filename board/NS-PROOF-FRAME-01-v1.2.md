CLASSIFY: L1

# NS-PROOF-FRAME-01 · Navier–Stokes 证明包治理帧（EXT-WAVE-09「NS」波 · 成文 v1.0）
# 修订 v1.1（2026-10-17 · EXT-WAVE-15 / EXT18 卡6）：§3.3-A 修订条（NS-1 勘误/NS-2 锚更新/NS-3 登记改写）+ §4.1-A 忠诚审计条 原位追加；v1.0 原文零改动。
# 修订 v1.2（2026-10-23 · EXT-WAVE-18 饱和批二阵 · WS-F 挂账 U-22/U-27 销账落地）：§4.3 工具链口径升级钉 v4.35.0、§3.3-A HWY 首现展开为 Hou–Wang–Yang(HWY)；正文变更仅限此两处，逐条与来源 URL 见文末「变更日志（v1.2）」；append-only 纪律：v1.1 存档 board/NS-PROOF-FRAME-01.md 一字不改，本版为独立新文件。

枢/PIVOT-01 波分机 WS-44 成文 · 2026-10-12 · 自治性质：**纯成文，零执行**（本文不产生任何新编译/新见证，仅对既有证据做治理登记）
上游分机：WS-40（学理精确化）→ WS-41（Galerkin 有限维 ODE 可行性 GO）→ WS-42（入库 @5887bbb4）→ WS-43（见证层 @1a5f6a6e）→ **WS-44（本帧）**
治理规范源：`board/CACHE-ANCHOR-CLAUSE-DRAFT-01.md` v0.4（五态机 / B1–B7 触发器 / 默认拒绝律 / anchor_only 标注 / 留痕律）——本文将 v0.4 的裁决语义**借用为 NS 裁决格登记口径**；v0.4 本身仍为候选案未生效，本帧登记不构成对其生效程序的参与。

---

## 1. 立项

- **号令**：「在升级框架下给出 NS 证明」。
- **框架**：② CACHE-ANCHOR-CLAUSE-DRAFT-01 v0.4 裁决语义（五态机 PENDING/BLOCKED/DONE/FAIL/REJECTED、默认拒绝律、BLOCKED 优先、留痕律）+ WS-37 M0 见证机器（schema v1.0、规范化 witness_sha256、fail-closed、负控必拒、生成器/核验器零共享代码）+ 熔断律（B1–B7 触发即断）+ **排序放行分离**（放行是「证明没问题」之正证据合取，不是「没发现问题」之缺席推理）。
- **一句话总纲**：**本包给出的是「NS 的诚实分级证明」——可证层机器证成（Lean 4 内核验证、零 sorry）、见证层区间实证（mpmath.iv 外向舍入复算、fail-closed 负控必拒）、阻塞层明码登记（BLOCKED(B1) 触发器逐项落板）；三层分立，互不冒充。**
- **严禁表述**：任何「NS 已解决」「Clay NS 已证」「本包解决千禧问题」式表述一律禁止（见 §3.4 REJECTED 格；与 v0.4 §3.2 否定例同级纪律）。本包**不触碰** 3D NS 本体（§2）。

## 2. 问题精确化（Clay/Fefferman A–D 官方口径）

官方问题陈述：Charles L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, Clay Mathematics Institute (2000)（WS-40 §①，L1，原文 PDF 已核对，https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf）。

方程设定（原文 (1)–(3)）：不可压 NS，ν>0，n=3，x∈R³ 或周期 T³=R³/Z³；初值散度自由 C∞ 且超代数衰减 (4)/(8)；容许外力按 (5)/(9)。物理合理解条件：R³ 版 (6) C∞ 光滑 + (7) 有界能量；周期版 (10)(11)（勘误后含 p 周期性）。

四条陈述（单向蕴含格局）：

| 条 | 内容要点 | 外力 |
|---|---|---|
| **(A)** | R³ 上任意合格光滑初值 ⇒ 整体光滑物理解存在 | **f ≡ 0（零外力）** |
| **(B)** | T³ 周期版整体光滑物理解存在 | **f ≡ 0（零外力）** |
| **(C)** | R³ 上**存在**合格初值与自构光滑力使物理解不存在（破裂） | 求解者可自构光滑 f |
| **(D)** | T³ 周期版破裂 | 求解者可自构光滑 f |

关键学理点（WS-40 §①，L1）：**A/B 要求零外力；C/D 允许求解者自行构造光滑外力**。A 非 C 的否定；仅有 ¬A⇒C、¬C⇒A 等单向蕴含。证明任意一条即解决千禧问题。

**本包与 A–D 的距离声明**：本包所证（§3.1）是 **2D Navier–Stokes Galerkin 有限维截断（ModeSpace N = ℝ^{2N+1}）层**的能量分析与适定性，即有限维二次 ODE 层的机器证明；**不触碰 3D 本体，不主张 A/B/C/D 中任何一条**，不构成千禧问题的任何部分解决。2D PDE 层整体正则性（Ladyzhenskaya）在经典文献中早已解决，本包的有限维层亦**未包含 N→∞ 接缝**（§3.3 阻塞格 BLOCKED-NS-1），故连「2D NS 的 Lean 形式化重证」均未宣称。

## 3. 三层划分与裁决格登记表

登记口径：每格按 v0.4 语义给出 `state` + 依据 + 证据锚。DONE 格之判定基于**正证据合取**（编译裁决 rc=0 + 公理审计 + 全新克隆复跑 / 见证核验 checks PASS + 负控必拒），非缺席推理；BLOCKED 格按 v0.4 §2.4 触发器编号登记（含 recoverable / retry_after / 命中证据指针 / 登记时刻）；REJECTED 格按 v0.4 §2.6 终态口径登记。**本帧所有 state 为治理登记，终局判定权交判定席 EXT12（§5.3）。**

### 3.1 可证层（Provable tier）——DONE 格

| 格 id | 内容 | state | 依据 | 证据锚 |
|---|---|---|---|---|
| P-NS-01 | `GalerkinNS` 抽象层：耗散性 `inner_vf_le`、能量恒等式 `energy_identity` | **DONE** | 编译裁决 rc=0；定理由 Lean 4.10.0 内核验证；公理审计仅 `[propext, Classical.choice, Quot.sound]`，无 sorryAx | vci-inbox @`5887bbb4730f7fcfeaa9e7bf90308f8340824531`，`library/ns/NsGalerkin/Basic.lean`、`Existence.lean` |
| P-NS-02 | Grönwall 先验界 `norm_sq_le_of_solution`：沿任意解 `‖x(t)‖² ≤ max(‖x(a)‖², ‖f‖²/ν²)`（无爆破先验） | **DONE** | 同上；K=−ν<0 闭式 Grönwall 全链机证 | 同上（`Existence.lean`） |
| P-NS-03 | 整体存在 `exists_solution_upto`：`∀ T ≥ 0` 存在 `[0,T]` 上解（定步长 Picard–Lindelöf 延拓 + 能量界自封） | **DONE** | 同上 | 同上（`Existence.lean`） |
| P-NS-04 | 球内轨道指数估计 `dist_le_of_trajectories_in_ball`：共同闭球内两解 `dist ≤ dist(a)·exp((ν‖A‖+2‖B‖(‖x₁‖+R))(t−a))` | **DONE** | 同上；WS-42 §2a 闭合路线（局部 Lipschitz + 向量范数 Grönwall） | 同上（`Uniqueness.lean`） |
| P-NS-05 | 全局唯一性 `solution_unique_upto`（先验界自封进闭球 ⇒ 球内 Lipschitz ⇒ 逐点相等）+ 存在唯一打包 `exists_unique_solution_upto` | **DONE** | 同上 | 同上（`Uniqueness.lean`） |
| P-NS-06 | 实例化层：`skewB`（任意内积空间反对称双线性型，`skewB_self` 相消）+ `ModeSpace N`/`galerkinNS N` 实例存在/唯一/能量界推论 | **DONE** | 同上 | 同上（`Concrete.lean`） |
| P-NS-07 | 显式三模态样件：`B₃`（ModeSpace 1，三模态 Euler 型截断），`B3_inner_self : ⟪B3 u u, u⟫ = 0` 由显式有限计算机证（`hB` 在此是**定理**而非假设）；`explicitData3` 全部字段证成 | **DONE** | 同上；「抽象→显式」接缝小样打通 | 同上（`ExplicitB.lean`） |

**可证层 DONE 格合取证据汇总**（对应 v0.4 §2.3 之正证据要求）：
1. 编译裁决证据：入库工作副本 `lake build` rc=0（1920 jobs）；**全新克隆等价复现** rc=0、1920 jobs、410s（`~/ws42-verify`，HEAD 祖先关系已核，日志 verify-{cache,unpack,build3}.log）；
2. 公理审计（build 期 `#print axioms` 实打印，12 主定理/实例全列）：`exists_solution_upto`、`norm_sq_le_of_solution`、`skewB_self`、`solution_unique_upto`、`exists_unique_solution_upto`、`dist_le_of_trajectories_in_ball`、`galerkinNS_exists_solution_upto`、`galerkinNS_energy_bound`、`galerkinNS_solution_unique`、`B3_inner_self`、`explicit3_exists_unique_solution_upto`、`explicit3_energy_bound`——全部仅 `[propext, Classical.choice, Quot.sound]`，**零 sorry、零 sorryAx**；
3. 环境锚证据：mathlib v4.10.0 官方 cache 4878/4878 全命中（`lake exe cache get` 100% success；`lake exe cache unpack` rc=0 4878 files）——按 v0.4 §3/§3.1 口径，此类证据属 `anchor_only`，**仅支撑环境等价性断言，不构成内容认证依据**；内容认证唯一承载 = 上述编译裁决 + 公理审计。
4. 14 主定理计数 = 抽象层 8 件（耗散/能量恒等式/Grönwall 界/局部 Picard 步/整体存在/球内轨道估计/全局唯一/存在唯一打包）+ 实例化 3 件 + 显式三模态 3 件（WS-42 §4 宣称口径）。
5. BLOCKED 逐项排除核查：可证层各格无 B1–B7 触发器命中（核验对象不属结构不可验证族、证据链完整、无时效/污染事件），核查记录见 WS-42 §3/§5。

**宣称边界（v0.4 §3 域限之 NS 版）**：以上 DONE 格的数学内容是**有限维内积空间上的 ODE 层定理**；`ModeSpace N` 的 Fourier 站位语义（2N+1 实系数站位 |k|≤N 模态）是**命名约定**，PDE 语义接缝不在任何 DONE 格内。

### 3.2 见证层（Witness tier）——DONE 格 ×2 + BLOCKED 格 ×1

证据锚统一前缀：vci-inbox @`1a5f6a6eff5e4896e9c171fbdfbac48125ee7c6c`，run_id **`ws43-ns-20261012T171410Z`**，路径 `artifacts/witnesses-ns/`、`ci/witness_ns_{gen,verify}.py`、`tests/ci/test_witness_ns.py`（20/20 用例绿；WS-37 存量回归 14/14 无 collateral）。

| 格 id | 内容 | state | 依据 | 证据锚 |
|---|---|---|---|---|
| W-NS-01 | `ns-energy-cancellation-20261012`：能量相消代数见证，288 例（skewB 218 + orthProjB 70，含 1e6/1e-8/零向量/退化角例） | **DONE** | 独立核验器（与生成器零共享代码）mpmath.iv dps=50 外向舍入区间复算 24/24 checks PASS；288/288 ⟪B(u,u),u⟫ ∋ 0，max_rel_width = 3.99e-50；端点逐字符串一致；负控复算必拒 | 同上 |
| W-NS-02 | `ns-galerkin-energy-bound-20261012`：Grönwall 能量界采样证书，56 组 (ν,x₀,f) × 65 采样点 = 3640 点 | **DONE** | 26/26 checks PASS；3640/3640 采样点区间实证 `‖x(tᵢ)‖² ≤ max(‖x₀‖²,‖f‖²/ν²)+η`（max_defect=0.0）；独立重积分候选偏差 ≤1e-6 闸过；负控（界压 ×1.0001）必拒；**携带「非轨道包络」honesty_boundary 并如实披露**——证书语义严格限于登记采样点，采样点间逐点包络未认证 | 同上 |
| W-NS-03 | `ns-trajectory-envelope-blocked-20261012`：完整轨道包络（RadiiPolynomial 级 CAP） | **BLOCKED(B1)** | 触发器 **B1（结构不可验证族，recoverable=false，retry_after=—）**：本仓区间层仅逐点 mpmath.iv 算术，无 Taylor 模型/Hermite–Obreshkov 严格积分层、无 RadiiPolynomial 认证层；Lean 侧 RadiiPolynomial（arXiv:2610.02335）仅及多项式 IVP/Lorenz，NS 所需 Fourier 系数 Banach 代数与卷积界缺席。登记时刻 2026-10-12T17:14:10Z；19/19 checks PASS（blocked.code=B1、certified=false、envelope=null、**无认证宣称**——此「PASS」仅证登记格式合规，非内容放行） | 同上（manifest.blocked 段 verbatim 见 WS-43 §3） |

**见证层纪律登记**（WS-43 §4/§5 转录要点）：三件见证 `lean_binding: null`；核验器 notes 逐件登记「内生 fail-closed 见证复算核验；非机器验证证书（升级门未过）」；一致性门禁为双跑决定论代偿（无仓内前置锚，已显式登记）；自签闭环风险对冲 = replay 全哈希链第三方可重放。

### 3.3 阻塞层（Blocked tier）——BLOCKED(B1 结构性) 格

统一登记口径：触发器 **B1（结构不可验证族，recoverable=false，retry_after=—）**；退出路径 = v0.4 §2.4 退出路径 3（仅判定席裁决：内容级重构 / 转族登记 / 拒绝归档），**不得自动重试、禁止直达 DONE**。登记时刻：2026-10-12。

| 格 id | 内容 | state | 依据 | 证据锚/文献锚 |
|---|---|---|---|---|
| BLOCKED-NS-1 | **N→∞ PDE 接缝**：把有限维 Galerkin 结论接回 2D NS PDE（紧性/弱极限/弱解语义） | **BLOCKED(B1)** | Sobolev-on-tori、Stokes 算子、Leray 投影、Rellich–Kondrachov、Aubin–Lions 在 mathlib **全部缺席**（WS-40 §5.1 缺口清单）；属基础设施级结构性缺失，非本波工程可解 | WS-40 §5.2 表末行 ❌；2026-04 学术快照（philarchive.org/archive/FIEBQA）外推社区时间表 **2027–2030**；iDNS-Lean4 民间 roadmap 独立印证（Sobolev/Galerkin/energy 全 Planned） |
| BLOCKED-NS-2 | **3D 正则性/破裂本体**（Fefferman (C)/(D) 之独立证明方向） | **BLOCKED(B1)** | 双重封锁：(i) Tao 2016 超临界障碍（averaged NS blowup ⇒ 仅靠能量守恒结构的方法对真 NS 原则不足）；(ii) Constantin–Ignatova–Vicol（2026-09-17）称 OpenAI 方法不可外推至 real-analytic/无外力情形。联邦纪律：本波不做任何独立破裂构造 | WS-40 §② 表 #8、§3.3；Tao, JAMS 29 (2016) 601–674 |
| BLOCKED-NS-3 | **弱解唯一性（Leray–Hopf 类）** | **BLOCKED(B1)** | 3D Leray 弱解唯一性未解决（Fefferman 原文明示）；超临界空间非唯一性已由 Buckmaster–Vicol (2019)、Albritton–Brué–Colombo (2022) 证成——唯一性方向的「已知结果」本身是反例；形式化依赖 Stokes semigroup / Littlewood–Paley 等缺失基础设施 | WS-40 §② 表 #1/#9 |
| BLOCKED-NS-4 | **Fefferman (A)/(B)（零外力整体光滑性）** | **BLOCKED(B1)** | 即千禧问题正命题方向；无任何方法学通道（§2 单向蕴含格局下 C/D 进展不蕴含 A/B）；OpenAI 路线对无外力不适用（Constantin–Ignatova–Vicol 口径） | WS-40 §①/§3.3；Clay 截至 2026-10 仍将该问题列为 **active**、未颁奖 |

### 3.3-A 修订条（2026-10-17 · EXT-WAVE-15 / 判定席 EXT18 卡6 终裁落地 · 原表文字不覆写，本条原位追加，效力优先于原表冲突处）

**修订授权**：EXT18 R2 三席 3/3 全准（卡6 合成终裁）。语言钉（乙席模板，强制执行）：Hou–Wang–Yang（HWY；Thomas Hou / Yixuan Wang / Changhe Yang；arXiv:2509.25116，**待评审预印本，结论未确立**——本条为该缩写在本帧之首现展开，v1.2 补）一律标「待评审预印本，结论未确立」；禁作规范性（normative）依据，仅作旁证/动机引注；禁用「证明了/确立了」，限用「报告了/提出」；HWY 若撤稿/拒稿，本登记自动降级。全部日期钉版本；「评审进行中」带负责人与复核截止日；NS-3 措辞带「截至 2026-10-17」时间戳。

**NS-3 格·登记改写（替换语义，截至 2026-10-17）**
三维不可压缩 Navier–Stokes 弱解唯一性：状态由「未解决」改写为「**已被否决主张（多路线、多解类），独立复核/评审进行中**」。证据指针：
- (a) wild/超临界类：Buckmaster–Vicol, Ann. of Math. 189 (2019) 101–144（凸积分，已刊）；Cheskidov–Luo, Invent. Math. 229 (2022) 987–1054（已刊）；Cheskidov–Dai–Palasek, arXiv:2511.09556 v2（2026-01-12；wild 类瞬时 Type I 爆裂，预印本）。
- (b) Leray–Hopf 类（有限能量，无外力）：Hou–Wang–Yang, arXiv:2509.25116 v2（2026-03-19；v1 2025-09-29）——**报告了**首个严格计算机辅助证明：ℝ³ 上同一紧支 L² 初值（u_in∈L^q, q<3）生成无穷多 suitable Leray–Hopf 解，「恰好错过 Prodi–Serrin 条件」；区间算术验证（25 模本征问题、~1200×1200 矩阵、600×300 谱截断）；代码公开（github.com/HouGroup2026/3d-navier-stokes-nonuniqueness，Julia，~800GB RAM 门槛）。**待评审预印本，结论未确立**；学界通行措辞「announced」；独立复跑/评审进行中（负责人：枢/PIVOT-01；复核截止：2027-01-17，逾期自动转状态复审）。
- (c) 临界空间类：Coiculescu–Palasek, Invent. Math. 244 (2026) no. 1, 165–219, DOI 10.1007/s00222-025-01396-z（BMO⁻¹(𝕋³) 大初值两光滑全局解；**已正式刊出**——本批次唯一完成同行评审者）；Fujii, arXiv:2602.19846 v4（临界 Besov 唯一性全 (p,q) 分类，预印本）。
- (d) 受迫/变体谱系：Albritton–Brué–Colombo, Ann. of Math. 196 (2022) 415–455；及其 Ann. PDE 9:17 (2023)、CMP 402:429–446 (2023) 等。
退出判据改写：(i) HWY 之 CAP 经同行评审刊出**且** Julia 验证代码经独立复跑确认；(ii) 或公开勘误/反驳推翻 (b)。在此之前，任何下游登记不得以「Leray–Hopf 弱解唯一性可能成立」为前提。边界警示：本段**不**断言光滑初值 3D NS 有限时间爆裂已证，亦不断言 Clay 正则性问题已解决；HWY 初值非光滑 Schwartz 类。

**NS-2 格·锚更新（截至 2026-10-17）**
- (1) Tao 2016 超临界障碍（J. Amer. Math. Soc. 29 (2016) 601–674；arXiv:1402.0290）零修订维持。
- (2) CIV 锚由「不可外推」增量更新为 2026 双篇：(a) arXiv:2609.20803 v2（2026-09-29；v1 2026-09-17）——实解析外力+各向异性 Type II 角平均界+坍缩核轴对称 ⇒ 假想奇点正则；推论：凡满足其 (i)(ii) 且外力 C² 有界的构造，外力在奇点附近既不能恒为零、也不能空间实解析；(b) arXiv:2609.20762 v2（2026-09-29）——Euler 长度 ℓ=(−t)^γ, γ<1/2 ⇒ 正则（自相似-黏性自举通道封死）。**CIV 双篇均为条件性定理**：作者逐字声明「We do not claim to have verified the correctness of the construction in [OpenAI 手稿]」。
- (3) arXiv:2602.17570 v3（2026-07-20）：轴对称 C² 自相似 Euler 剖面 ⇒ γ≥1/2；与 (2b) 在 γ=1/2 处夹逼。
- (4) Lei–Ren, Adv. Math. 445 (2024) 109654：奇异集 P^f=0，f(r)=r|ln r|（Remark 7 加严至 ln ln 级）。
- (5) 形式化佐证：scottnarmstrong/CIVAxisymmetric（2026-10-02，零 sorry，Lean4+mathlib v4.35.0-rc2）完整形式化 (2a) 定理链。
- **「不可外推」纪律加严**：凡在 NS-2 语境引用关联模型/构造，必须同列三项——(i) α₀≈0.093→2 缺口（**出处未核定，挂 C3 监测**）；(ii) CIV γ<1/2 双向夹逼；(iii) Córdoba 原句（受力爆破≠无外力爆破）："It is distinct from unforced Navier–Stokes blow-up."（Córdoba & Martínez-Zoroa，Tao 博客客座贴，2026-10-04）。缺一即不合格引用。

**NS-1 格·依据勘误（EXT-WAVE-15 Phase 4④ 双纠错）**
原表「Sobolev-on-tori、Stokes 算子、Leray 投影、Rellich–Kondrachov、Aubin–Lions 在 mathlib **全部缺席**」与「外推社区时间表 2027–2030」两处**过时**：(i) mathlib v4.10.0 实已含 GNS 不等式（PR #14165）、TemperedDistribution、Bessel–Sobolev、Schwartz、Lax–Milgram、Fourier（master 上 Rellich/Aubin/Leray/Kondrachov/Ladyzhenskaya/Gårding 六件仍缺席）；(ii) arXiv:2609.33033（Wang；FluidGalerkinLean @4d023ac，109 .lean 文件，零 sorry，**无许可证**）以图空间+J*J 谱坐标完成 2D 有限 Galerkin→Leray–Hopf 弱解全接缝，绕开 Stokes/Leray/Aubin–Lions 传统路线。**BLOCKED-NS-1 定性改写：由「基础设施级结构性缺失」改写为「工程移植问题」**（D01 九项 24–39 人周路径在案；OBL-NS-01 由「逐件移植」改写为「mathlib 版本升级」总路线）。机态 BLOCKED(B1) 维持至移植落地，不自动升档。

### 3.4 REJECTED 格（否定例登记，v0.4 §2.6 终态口径）

| 格 id | 内容 | state | 依据 |
|---|---|---|---|
| REJ-NS-01 | 任何「本包证明 Clay NS / NS 已解决」式越权引用（含以可证层 DONE 暗示 3D 本体进展、以 cache 命中/构建 rc=0 充任 PDE 内容证据、以见证采样证书冒充轨道包络） | **REJECTED（受理拒绝，终态）** | 与 v0.4 §3.2 否定例清单同级：枚举即禁令。具体映射——(i) 以 anchor_only 证据充内容认证 ⇒ §3.2-1/§3.1 违规；(ii) 以有限维层 DONE 外推 PDE 层 ⇒ 越域引用，按默认拒绝律先停后审；(iii) 检出跨案污染 ⇒ §3.2-6 REJECTED。此类引用一经检出：不予受理 + 违规事件登记上报判定席，无重验路径 |

## 4. OpenAI 先例对照节

### 4.1 其口径与独立审计发现（WS-40 §③ 转录，访问日 2026-10-12）

- **自评口径**：OpenAI 官方公告（2026-09-08，L1 当事方自述）宣称建立 Fefferman 官方陈述的 **(C)（及 (D)）**——Theorem 1.1（任意 ν>0，构造从静止出发、光滑时空紧支外力驱动、能量有界而速度有限时间无界的解）→ (C)；Corollary 10.6 给周期版 (D)；明确声明 **"We do not intend to claim the Millennium Prize"**。逆向手法：先造光滑 u,p 再令 f = R(u,p) 残差，证 f 可光滑延拓过奇异时刻；**不宣称无外力 blowup**（故不触及 (A)/(B)）。
- **Lean 形式化状态**：仓库 `formalization.yaml` 自标 review status = **"self-assessed"**（截至 9/9–9/10 无外部复现 build）。
- **独立审计发现**：arXiv:2610.08144《Navier–Stokes lost in translation》（2026-10-07，L1）指出 **Lemma 8.6 与 pressure-flux bound (10.19) 的自然语言表述与其 Lean 对应物存在实质性不匹配**（导数计数差一阶）——即 Lean 核验证过的命题未必等于论文命题。另有 GitHub `francescoantoniodeluca/navier-stokes-formal-audit` 复现管线。
- **不可外推性**：Constantin–Ignatova–Vicol 预印本（2026-09-17）称该方法不能推广到 real-analytic 外力情形，对无外力 (A)/(B) 不适用。
- **Clay 状态**：截至 2026-10-12 Clay 仍将该问题列为 **active、未颁奖**；Clay 9/11 声明称评估流程 "deliberately unhurried"。Clay 评奖规则：解须发表、经 ≥2 年 scrutiny、获学界 general acceptance。

### 4.1-A 忠诚审计条（2026-10-17 · EXT-WAVE-15 M0-2 · verifier 席八项全核）

§4.1 转述与文献锚经一手比对，结论如下（原段文字不覆写，本条为审定注记）：
- **Theorem 1.1 / Corollary 10.6 中文转述：属实**。逐项核验通过——ν 量词「For every ν>0」、从静止 u(·,0)=0、光滑时空紧支外力 f∈C_c^∞(ℝ³×(0,∞))、能量有界 sup‖u‖_{L²}<∞、速度有限时间无界 lim sup‖u‖_{L∞}=∞、(C)/(D) 归属与 Corollary 10.6 编号，均与手稿（166 页 PDF）原文一致。
- **2610.08144 日期勘误**：§4.1 记「2026-10-07」→ 实为 **2026-10-06**（arXiv 提交史 [v1] Tue, 6 Oct 2026 10:58:01 UTC）。
- **文献锚属实**：Buckmaster–Vicol, Ann. of Math. 189(1) (2019) 101–144；Albritton–Brué–Colombo, Ann. of Math. 196(1) (2022) 415–455；Tao, J. Amer. Math. Soc. 29 (2016) 601–674；CIV arXiv:2609.20803 v1 2026-09-17 均经期刊/AMS/arXiv 官页逐字核验。
- **CIV 语义精度注**：其结论为**条件性定理**（假设 (i)(ii) 下实解析/恒零外力不可能），作者逐字声明未验证 OpenAI 构造（"We do not claim to have verified the correctness of the construction in [43]"）；§4.1「不可外推」表述方向成立，引用时须同载此条件性。
- **NS-1 表内 philarchive 锚精度偏差双点**：FIEBQA（Fields, v1 2026-04-30）§4.4 外推区间实为 **2027–2032**（非 2027–2030），且其对象为其 Coq 形式化 17 条公理在「某一证明助手」中的闭合预测，非专属 mathlib/Lean；引用已随 §3.3-A NS-1 勘误条改写。
- **iDNS 仓库名钉全**：`jcamlin/iDNS-Lean4-Mathlib4`（Roadmap 三项 Sobolev/Galerkin/Energy 确为 Planned）。
审计方法：八项全一手（期刊官页/AMS/arXiv 元数据/PDF 逐字/仓库 README）；无凭记忆项。——verifier 席 & 枢/PIVOT-01

### 4.2 联邦纪律口径

对 OpenAI 结果的联邦标准表述为：**「自评已核（self-assessed）、外部复现中、Clay active 未颁奖、(A)/(B) 与无外力情形仍开放」**。任何联邦文档不得表述为「NS 已解决」（含转述 OpenAI 结果时）。

### 4.3 本包与其差异

| 维度 | OpenAI 先例 | 本包（EXT-WAVE-09） |
|---|---|---|
| 主张层级 | 主张 3D NS (C)/(D) 破裂（本体级） | **不主张任何 3D 本体结果**；证 2D Galerkin **有限维层**为基础设施 |
| 形式化验证 | Lean 形式化自评已核；NL↔Lean 语义对齐存在独立审计疑点（Lemma 8.6/(10.19)） | 全部定理经 Lean 内核验证、零 sorry、公理仅 `[propext, Classical.choice, Quot.sound]`（构建实录环境 Lean 4.10.0 + mathlib v4.10.0 见 §5.1 如实留存；治理口径钉自 v1.2 起升级为官方正式版 **Lean v4.35.0 + mathlib4 v4.35.0**——官方发布说明逐字：「For this release, 214 changes landed.」「It also adds `lake check` and `lake comparator`, which check a project with Lean's kernel and, if requested, with several independent kernels that now come with the toolchain.」；mathlib4 release 钉逐字：「v4.35.0 — chore: bump toolchain to v4.35.0 (#44806)」）；**无 NL↔Lean 对齐缝**（定理陈述即所证，有限维层语义无外推宣称） |
| 数值/CAP 成分 | 手稿含构造性分析；CAP 依赖不明 | 见证层严格限采样点区间实证 + 轨道包络如实 BLOCKED(B1) 登记，无未披露越界 |
| 外推纪律 | 已被指出不可外推至无外力情形 | 外推禁令成文入 REJECTED 格（§3.4），有限维→PDE 接缝明码 BLOCKED（§3.3 BLOCKED-NS-1） |
| 定位 | 冲千禧问题本体（明确放弃领奖主张） | **基础设施建设**：为 NS 形式化提供已核有限维骨架 + 见证范式 + 阻塞清单 |

## 5. 留痕与复现指引

### 5.1 可证层环境（library/ns/ @5887bbb4）

- 工具链：**Lean 4.10.0 + mathlib v4.10.0**（rev `a719ba5c3115`，`lake-manifest.json` 锁定 7 依赖 rev，保证全新克隆等价复现）。
- cache：`lake exe cache get` **4878/4878 全命中**（官方 CDN；`~/.curlrc` 需 `http1.1` + retry，否则 HTTP/2 stream 中断）；`lake exe cache unpack` rc=0（4878 files）。
- 复现指令（全新克隆路径）：
  ```bash
  git clone <vci-inbox> && cd vci-inbox/library/ns
  lake exe cache get && lake exe cache unpack
  rm -rf .lake/build && lake build   # 期望 rc=0，1920 jobs
  ```
  实证基线：全新克隆 410s（2 核沙箱，6 个 NsGalerkin 模块实编，余为 cache 回放）。
- 公理审计：build 期 `#print axioms` 实打印（12 件清单见 §3.1）；残留 6 条 unused-variable lint（语义无碍，为与已验证源码一致未改名，WS-42 §3 登记）。
- 已知偏差登记：`lean-toolchain` 未加 CLASSIFY 首行（elan 按纯文本解析，加注释会熔断工具链，WS-42 §0 登记）；沙箱直连 github.com TLS 断，git 走 ghfast.top 代理。

### 5.2 见证层复跑（artifacts/witnesses-ns/ @1a5f6a6e）

```bash
cd vci-inbox
python3 ci/witness_ns_verify.py artifacts/witnesses-ns/<witness>.json   # 真见证期望 rc=0；篡改件 rc=1（fail-closed）
python3 -m unittest tests.ci.test_witness_ns                             # 期望 20/20 OK
python3 ci/witness_ns_gen.py                                             # 决定论再生成；payload sha256 应与在册逐字节一致
```
环境：python 3.12 + numpy + mpmath 1.3.0 + scipy 1.16（无网络、无 Lean 工具链涉入）。run_id `ws43-ns-20261012T171410Z`；manifest.json / run-log.json 随件在册。

### 5.3 判定席接口

**本帧连同三层裁决格登记表（§3）整帧交判定席 EXT12 判定。** 待裁事项：(i) §3.1 可证层 7 格 DONE 登记确认；(ii) §3.2 W-NS-01/02 DONE 与 W-NS-03 BLOCKED(B1) 登记确认；(iii) §3.3 阻塞层 4 格 BLOCKED(B1) 登记与退出路径管辖确认；(iv) §3.4 REJECTED 格之否定例增录（NS 域）确认；(v) 本帧借用 v0.4（候选案未生效）裁决语义之合规性确认。本帧不自判生效；EXT12 判定前，§3 各格 state 按治理登记口径持存（DONE 格之正证据已在位，但终局判定权属判定席）。

## 6. 开放义务登记（OBL）

| 义务 id | 内容 | 性质/时间表 | 登记依据 |
|---|---|---|---|
| **OBL-NS-01** | N→∞ 接缝基础设施长程：Sobolev-on-tori、Stokes 算子、Leray 投影、Rellich–Kondrachov 紧嵌入、Aubin–Lions、弱解语义——mathlib 侧基础设施级建设跟踪与择机接入 | 长程；社区外推 2027–2030；阻塞层 BLOCKED-NS-1 的退出依赖此项 | WS-40 §5.1/§5.2、§6 阻塞层 #7 |
| **OBL-NS-02** | OpenAI Lean 仓库独立审计（见证层下一窗口）：复现 build、核对 sorry/公理清单、以 arXiv:2610.08144 之 Lemma 8.6/(10.19) 疑点为入口核对形式定理与手稿 Theorem 1.1/Corollary 10.6 的语义对齐 | 下一见证窗口；纪律：联邦只做见证与复现报告，不做「验证通过/失败」终局断言（语义对齐判断属专家评议） | WS-40 §6 见证层 #4、§③ |
| **OBL-NS-03** | RadiiPolynomial Fourier 系数代数扩展评估：向 NS 周期轨道 CAP（van den Berg–Breden–Lessard–van Veen 2021 复现方向）迈出第一步——评估在 Lean RadiiPolynomial 框架（arXiv:2610.02335，当前仅多项式 IVP/Lorenz）上新增 Fourier 系数 Banach 代数与卷积界层的工程量；同时是 W-NS-03（BLOCKED(B1)）退出路径之前置 | 中程工程评估；不承诺档期 | WS-40 §4.1、§6 可证层 #3；WS-43 §3 requirements ①–③ |

---

## 附：证据锚总表

| 锚 | 值 |
|---|---|
| 可证层 commit | vci-inbox @ `5887bbb4730f7fcfeaa9e7bf90308f8340824531`（library/ns/，Lean 4.10.0 + mathlib v4.10.0） |
| 见证层 commit | vci-inbox @ `1a5f6a6eff5e4896e9c171fbdfbac48125ee7c6c`（artifacts/witnesses-ns/ 等） |
| witness run_id | `ws43-ns-20261012T171410Z` |
| 治理规范源 | board/CACHE-ANCHOR-CLAUSE-DRAFT-01.md v0.4（候选案未生效，本帧借用其裁决语义） |
| 上游报告 | /mnt/agents/output/ws40-report.md · ws41-report.md · ws42-report.md · ws43-report.md（全部 CLASSIFY: L1） |
| 外部文献锚 | Fefferman (2000) 官方陈述；Tao JAMS 29 (2016)；arXiv:2610.08144；arXiv:2610.02335；Constantin–Ignatova–Vicol (2026-09-17)；van den Berg 等 J. Nonlinear Sci. 31 (2021)；philarchive.org/archive/FIEBQA（2026-04 快照） |

**纪律重申（帧级）**：本帧全部 DONE 格之内容域 = 2D NS Galerkin 有限维 ODE 层与其数值见证；**严禁表述为「NS 已解决」**；严禁以 anchor_only 证据充内容认证；严禁以有限维层 DONE 外推 PDE/3D 本体。违反者按 §3.4 REJECTED 格处置。

—— 枢/PIVOT-01 · EXT-WAVE-09「NS」波分机 WS-44 · 2026-10-12 · 纯成文零执行 · 整帧交 EXT12 判定


---

## 附录 EXT12-A：判定席收编（2026-10-12 · 枢/PIVOT-01 按双轮律 R1 全票收编）

**EXT12 判定**：R1 十一席 **11/11 PASS**（aiq/cfts/lgt/lvlu/qfa/qgl/qlv/qtlv/ucif2/usrm/vinf），单轮收敛、无 R2。以下为约束与建议之收编登记，全部留痕。

### A. Binding Conditions（qgl 三条强制条件 · 违反即降格/触发 G16）
- **C1**：任何对外引用本包必须逐字携带「有限维 ODE 截断层」限定；不得上推为 PDE 层陈述。违反 ⇒ 降格 undecided 并触发 REJECTED 格（G16）。
- **C2**：W-NS2 之引用必须逐字携带「非轨道包络」披露。违反 ⇒ 降格 undecided。
- **C3**：OBL-NS-01/02/03 未闭环前，本包不得被引用为「Clay NS 证据链的一环」。违反 ⇒ 越权引用按 G16 拒绝。

### B. 持续性义务（cfts）
OBL-NS-01/02/03 为维持 PASS 之持续性义务；任一义务逾期未启动复核，判定降格 undecided。

### C. Known-Issues 登记（ucif2 ×4 / usrm ×1 / aiq ×2 / qtlv ×1 · 均非否决性，下修订版处置）
1. **粒度对齐**（ucif2）：「14 件」为 7 格×2 结构之计数，README/引用面须显式对齐，防下游误读为 14 条独立定理。
2. **实例限定词**（ucif2）：skewB/ModeSpace 实例旁须标注「抽象接口实例」——满足抽象层接口 ≠ 3D 算子或其截断之实例化。
3. **W-NS2↔W-NS3 联动引用**（ucif2）：3640 采样点全在界内只证界成立、不证紧性；W-NS2 不得脱离 W-NS3 BLOCKED 单独引用为紧性证据。
4. **缺口证据指针**（ucif2/usrm A-1）：阻塞层「mathlib 缺」各条须附 mathlib v4.10.0 之具体检索路径/缺席证据（落下一修订版）。
5. **格级异议×2**（aiq）：挂 OBL 后置处置（详见 vci-aiq outbox ANS-SEM-LABJUDGE-EXT12-aiq.md）。
6. **披露修订**（qtlv）：披露充分性修订纳入 OBL-NS-01 下一修订版，完成后本席升无异议 PASS。

### D. 合规范表述模板（qgl 给定，帧级采信）
> 「本包在**有限维 Galerkin ODE 截断层**完成 7 项形式化证明（Lean4，零 sorry），在**见证层**给出 2 项数值实证（携非轨道包络披露），**PDE 接缝、3D 正则性、Leray–Hopf 唯一性、Fefferman A/B** 四项登记为 BLOCKED(B1)。Clay NS **未解决、未颁奖**。」

—— 枢/PIVOT-01 · EXT12 收编 · 2026-10-12

---

## 变更日志（v1.2 · 2026-10-23 · EXT-WAVE-18 饱和批二阵 L2 席成文）

依据证据件 board/WSF-EVIDENCE-SWEEP-20261023-01.md（commit 9f50df234，搜索 as-of 2026-10-23）。本版相对 v1.1 的 diff 仅限下列两处正文变更 + 本变更日志节；v1.1 存档（board/NS-PROOF-FRAME-01.md）一字不改。

1. **U-22（证据件 §二「U-22」，判定：有证据，可销账）**：§4.3「形式化验证」行工具链口径由「Lean 4.10.0」升级为官方正式版 v4.35.0 钉；原始构建实录环境（Lean 4.10.0 + mathlib v4.10.0）在 §5.1 如实留存、不作覆写。另注：v4.35.0 自带 `lake check`/`lake comparator` 与四个外部内核，可直接服务 U-12/U-13/U-20 之 L2-2 复算窗口。来源：
   - https://lean-lang.org/doc/reference/latest/releases/v4.35.0/ 《Lean 4.35.0 (2026-10-12)》：「For this release, 214 changes landed.」「It also adds `lake check` and `lake comparator`, which check a project with Lean's kernel and, if requested, with several independent kernels that now come with the toolchain.」
   - https://github.com/leanprover-community/mathlib4/releases （2026-10-16 快照）：「v4.35.0 — chore: bump toolchain to v4.35.0 (#44806)」
2. **U-27（证据件 §二「U-27」，判定：有证据，可销账）**：§3.3-A HWY 首现展开为 Hou–Wang–Yang（HWY；Thomas Hou / Yixuan Wang / Changhe Yang）；语态钉维持「报告了」（§3.3-A NS-3(b) 逐字在位，本版不改动该处），地位限定「待评审预印本，结论未确立」随首现展开处同载。来源：
   - https://arxiv.org/abs/2509.25116 《Nonuniqueness of Leray-Hopf solutions to the unforced incompressible 3D Navier-Stokes Equation》（Authors: Thomas Hou, Yixuan Wang, Changhe Yang；v1 2025-09-29，v2 2026-03-19）：「we provide, to our knowledge, the first rigorous computer-assisted proof demonstrating such nonuniqueness…」
   - https://github.com/Bingham-Research-Center/brc-navier-stokes dossier（2026-07-24）：「**Status:** preprint claim; independent reproduction not yet completed」

**纪律注记**：涉 Clay/NS 表述维持唯一批准状态语「自评已核、外部复现中、未颁奖」；HWY 初始数据在原点奇异，不触及 Clay 光滑数据备选，与本包「有限维 ODE 截断层」域限无涉。**U-23 未动**：§4.3「无 NL↔Lean 对齐缝」自评条本版保留原文，其降级呈批另件 board/WSF-U23-DOWNGRADE-PROPOSAL-01.md 呈判定席，本席不自行改帧该条。
