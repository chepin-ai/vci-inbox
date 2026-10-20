CLASSIFY: L1
# W-NS-03-REFORGE-CHARTER-01 · W-NS-03 重铸立案书（旗舰示范案例轨 + Gate 0 硬前置）+ 终稿口径逐句 diff 实做

立案席：WS-F 攻坚线执行席（枢/PIVOT-01 体系 · EXT-WAVE-18「攻」）
立案时间戳：2026-10-21
裁决授权：判定席 EXT18 R2 卡1（2026-10-17，三席 4/4 全准）——「W-NS-03 立案=旗舰示范案例轨，不单列预算（旗舰预算内单列案例轨工时行项，甲席附钉）；Gate 0 硬前置；验收钉定理级；口径逐句 diff，终稿 diff 实做不得以立案书 diff 替代（乙席软提醒）」
上游：NS-SOLUTION-v2_DESIGN_WS44 §四 L2-1/§八之五卡1；FIDELITY-AUDIT-PROTOCOL-L34-01（三层审计规程，本文件 §二为其首次实战应用）；ns-frontier_dim02（D02 证书解剖与复用设计，模板一手精读在案）
覆写权纪律：本文件为独立新件，不改动任何既有文件字节；引用既有文件一律带版本钉/行位钉。

---

## 一、立案书

### 1.1 重铸目标（数学内容一句话各）

W-NS-03（原格「完整轨道包络（RadiiPolynomial 级 CAP）」，NS-PROOF-FRAME-01 §3.2，BLOCKED(B1)，登记时刻 2026-10-12T17:14:10Z）语义重铸为下列两件之合取，与「RadiiPolynomial 级周期轨道包络」在联邦见证层**分开记账**（D02 §2 结论）：

1. **NK 时空管**：在空间-时间联合的加权 ℓ¹ Fourier–Chebyshev 系数 Banach 代数上，对数值时空多项式 Ū 以 Newton–Kantorovich 界组（Y、Z₁、Z₂(r)）判别式锁定其 r₀-闭球内 F 的唯一零点，落到函数层即有限时间窗上的**一致常半径时空管** sup_{t∈[0,T]}‖ω̃(t)−ω̄(t)‖_{L∞} ≤ r₀——半径不随 t 变化，**不是** t 的函数型轨道包络（模板：Cadiot–Lessard, Numer. Math. 158(4):1237–1289, 2026, DOI 10.1007/s00211-026-01546-2，Thm 4.5：ν=0.2、N₁=15/N₂=10、73 个 h=0.03 步 + 0.72 末步、r₀=4.54×10⁻⁵）。
2. **捕获区全局化**：在显式捕获盒 X_box(σ₀,σ₁) 上以带 e^{εt} 衰减权的 Picard 型算子收缩不动点论证，证明解在有限窗末进入捕获区并滞留，从而给出全局存在 + 一致指数衰减至 0 的**集合层**结论——不给 t>T 后相对任何数值轨道的逐时刻距离（模板：同上 Lemma 4.2 / Corollary 4.3 / Remark 4.4；Remark 4.4 自将捕获区阈值 0.58 与 Grönwall 直接估计 0.5 并列比较，印证与 W-NS-02（非轨道包络）同一先验族）。

语义定位：NK 段把 W-NS-02（3640 点 Grönwall 采样证书，**非轨道包络**披露在位）所缺的「前 T 时间单位内轨道位置」由先验解析界升级为后验严格管；捕获区段与 W-NS-02 属同一先验族，二者互补合龙、填其 a-posteriori 缺口。**重铸后的 W-NS-03 仍不是轨道包络**，此限定为披露口径组成部分，不可剥离。

### 1.2 旗舰示范案例轨定位

依 EXT18 卡1 + 丙席层序修正（L0→L1→L2(旗舰 alignment)∥练兵件→L3 分批），本轨定位为旗舰三规程的**首件示范案例**：

- **schema 规程示范**：重铸件的见证登记以 formalization.yaml v0.5 扩展块体例（G0→G4 阶梯 + alignment 字段 + exclusion_pointers）成文，充任 schema 试金石；
- **alignment 规程示范**：重铸前后 NL 语义（「轨道包络」→「NK 时空管+捕获区全局化」）的陈述改写，作为 NL↔登记对齐的首件 machine-readable 登记单元；
- **审计规程示范**：重铸终稿出具后按 FIDELITY-AUDIT-PROTOCOL-L34-01 三层规程逐句 diff 实做（本文件 §二先行执行降级基线 diff，见 §二.1 降级登记）。

预算纪律：不单列预算；旗舰预算内单列「W-NS-03 案例轨」工时行项（甲席附钉，Gate 0 清单 G0-4）。验收钉定理级：重铸件须有 Lean 侧证书锚定端点（CapAnchor 同族 Krawczyk≈NK 区间算术表述，D02 §3 P8）方可记 DONE。

### 1.3 Gate 0 硬前置清单（逐条；全关方得启动执行工程）

| # | 前置内容 | 现状（截至 2026-10-21） | 关闭判据 | 责任线 |
|---|---|---|---|---|
| G0-1 | RadiiPolynomial Lean 仓库（IlPreteRosso/RadiiPolynomial @162f）公开可见 | **未过**：仓库私有（WS-43 F04；LAB-CLOSE-EXT15 §6「Gate 0=仓库可见性，监测」） | 仓库公开可读且 commit 钉可解析；入 L0-2 依赖钉定簿 | OBL-NS-03 监测线（枢/PIVOT-01） |
| G0-2 | 重铸语义登记口径（「NK 时空管+捕获区全局化」与周期轨道包络分开记账；W-NS-02（非轨道包络）披露口径不动） | **CLOSED**：D02 §6 结论在案；EXT18 Q1/卡1 裁决通过；本文件 §1.1 成文 | 立案书成文（本文件） | WS-F 攻坚线 |
| G0-3 | 模板与 Julia 主路径栈版本钉：Cadiot–Lessard Thm 4.5 一手精读；IntervalArithmetic.jl v1.0.x；RadiiPolynomial.jl v0.11.6（Zenodo DOI 10.5281/zenodo.22684501）；IVP-Cheb.jl（MIT） | 模板精读 DONE（D02 [^8^][^11^][^13^][^14^]）；栈钉版未入册仓 ledger | 版本钉四件齐入依赖钉定簿 | L0-2 依赖钉定线 |
| G0-4 | 旗舰预算内「W-NS-03 案例轨」工时行项（甲席附钉） | 未成行项 | 旗舰预算表增列本行项 | 旗舰 L4-5 预算线 |
| G0-5 | 终稿 diff 义务登记（乙席软提醒：不得以立案书 diff 替代终稿 diff） | 重铸终稿尚不存在；本文件 §二执行降级 diff 并登记 | 重铸终稿出具后 5 工作日内完成 L34 三层逐句 diff 实做并归档 | WS-F + L3-4 审计线 |
| G0-6 | Lean 定理级验收钉端点：CapAnchor 锚定层对 NK 证书的登记适配方案（EXT18 卡1「验收钉定理级」） | CapAnchor.lean 存量在位（11 decl，Krawczyk 4 证书 3 PASS 1 FAIL 诚实登记）；适配方案未成文 | 适配方案成文（证书字段 + #guard_msgs 构建期断言体例） | L2 包络层 + L1 截断层 |

G0-1 未关前，OBL-NS-03 工程（Fourier Banach 代数 M0–M2）**不启动**（WS44 L2-3 原钉维持）。G0-2 为本清单内唯一已关条。

### 1.4 里程碑与人周估算（甲席席规：散布 >1.5 倍或验收钉无版本钉/无截止者退回重写）

| MS | 内容 | 估算（依据） | 版本钉 | 截止钉 |
|---|---|---|---|---|
| MS-0 | 本立案书 + 降级基线 diff（§二） | 1 pd（实做） | — | 2026-10-21（本日交付） |
| MS-1 | 重铸文 v0（语义重铸文 + 定理级验收钉定义 + schema 体例登记） | 1–1.5 pd（依据：WS44 L2-1「重铸文 1 pd」+ D02 模板精读已在案，新造仅语义登记与适配层；散布 1.5× 压线，上限 1.5 pd 封钉） | Cadiot–Lessard, Numer. Math. 158(4):1237–1289 (2026), DOI 10.1007/s00211-026-01546-2；arXiv:2502.20644v1 | **2026-11-15**（判定席 EXT19 R1 裁定钉死，本令即裁定；相对事件钉备选：L4-5 排期裁决登记时刻 + 5 工作日） |
| MS-2 | 重铸终稿 L34 三层逐句 diff 实做（G0-5 关闭） | 0.5–0.7 pd（依据：§二降级基线已铺底，对象单元 ≤40 件） | FIDELITY-AUDIT-PROTOCOL-L34-01（2026-10-21 生效体） | 重铸终稿出具 +5 工作日 |
| MS-3 | Gate 0（G0-1）监测复审窗口 | 0.2 pd/窗口 | 仓库事件驱动 | 2027-01-21（季度复审首窗；外部事件先到先复） |
| MS-4 | 执行工程（OBL-NS-03 M0–M2：ℓ¹_ν(ℤ) 完备赋范 ℂ-代数 + 求值面） | **退回重估**：WS44 L2-3 原估 4.5k–8.5k 行 / 3–6 人月，散布 2.0× > 1.5×，按甲席席规不得直接沿用；须先 spike 验估（≤1 人周）后重报 | arXiv:2610.02335（v1，2026-10-01；注意论文钉 Lean 4.33.0 与 LeanCert v4.35.0 之版本漂移） | Gate 0 全关前不启动，无截止 |

### 1.5 证据纪律（按对象适配钉语）

1. **见证层 ≠ 轨道包络**：重铸件一切对外表述须逐字携带「常半径时空管 ≠ 轨道包络」；捕获区全局化段须同载「集合层结论（落入并滞留 + 指数衰减率），不给逐时刻轨道距离」。
2. **W-NS-02 联动引用**：凡引用 W-NS-02 必逐字携带「非轨道包络」；W-NS-02 不得脱离 W-NS-03 状态单独引用为紧性证据（EXT12-A Known-Issues #3 维持）。
3. **区间见证层钉语按对象适配**：NS 见证层对象——「采样点区间实证、采样点间逐点包络未认证」；CapAnchor/ζ 锚类证书对象——「区间见证层 PASS、kernel 层未证、非 RH 证据」（EXT-WAVE-17 §三钉语体例）；有限高度对象——「有限高度 T=100/1000 截断」。
4. **Cadiot–Lessard 引述限定**：凡引该模板必同载「2D 全局存在系 Lions–Prodi 经典结果，本证书为构造性方法学复现 + 新实例」限定语（D02 §5；论文 §4.1.1 自述）。
5. **禁语与标准表述**：严禁「NS 已解决」（含转述）；涉 OpenAI 结果标准表述「自评已核（self-assessed）、外部复现中、未颁奖；Clay 官方状态 Active」；Clay NS 未解决、未颁奖。
6. **HWY 纪律**：首现展开 Hou–Wang–Yang（HWY），限「报告了/提出」语态，标「待评审预印本，结论未确立」；撤稿/拒稿自动降级。
7. **2610.08144 引述**同载作者立场钉（不证伪其 NL 论证；日期钉 2026-10-06）。
8. **编译通过 ≠ 判定通过**（L34 训诫条）：重铸件的 schema 登记、alignment 宣称均以三层全过为唯一通过定义。

---

## 二、终稿口径逐句 diff（L34 三层规程首次实战）

### 2.1 对象定位与降级登记（显式）

检索结论（`grep -rl "W-NS-0"` 于 vci-inbox 全域 + 「终稿/口径稿/draft/final」关键词扫描）：**W-NS-03 重铸终稿尚不存在**——LAB-CLOSE-EXT16 §7 明记「W-NS-03 终稿 diff 于转正后成帧」，LAB-CLOSE-EXT17 §四行动项「W-NS-03 final diff framing」仍未结。无任何文件自称 W-NS-03 重铸「终稿/口径稿」。

**降级登记**：依任务规则，diff 对象降级为——(i) `library/ns/formalization.yaml` v0.5（2026-10-19 转正口径，对外自述性质最强之现行口径文件）；(ii) NS-PROOF-FRAME-01.md v1.1 之**对外口径段**（§4.2 联邦纪律口径、§4.3 差异表、附录 EXT12-A §D 合规范表述模板、帧尾纪律重申，及相关证据承载行）。本 diff 为**降级基线**，不替代重铸终稿 diff（G0-5 义务存续）。

方法：按 L34 三层执行——陈述层八要素（量词结构/函数类与定义域/范数与空间/常数与增长因子/结论谓词/编号归属/假设消隐/条件性同载）逐单元对表；强度层四态判定（本审计适配为：主张相对证据**对齐 / 更强 / 更弱 / 不可比**，另加**无证据**态）；证据层核验证据锚在位性与一手性。判定从严：无证据即「无证据」，不得宽贷；本席未能一手复核之转引证据一律记「无证据」并注明转引层级。

### 2.2 diff 主表（A：formalization.yaml v0.5，U-01…U-20）

| # | 句位 | 主张原文（摘） | 对应证据层 | 判定 | 处置建议 |
|---|---|---|---|---|---|
| U-01 | yaml L7–17（project.description） | 「9 files, 56 declarations…no infinite-dimensional PDE seam is claimed here」 | LAB-CLOSE-EXT16 §6（commit 0027e36f，9f/56 decl）+ NS-PACKAGE-CENSUS-01（8f/51 + SkewB 5 = 56） | **对齐** | 无 |
| U-02 | yaml L13 | 「two certificate anchors (CAP anchor, zeta anchor)」 | census drift 注记（CapAnchor 11 decl / ZetaAnchor 4 decl 首次入总账） | **对齐**（计数层） | 无 |
| U-03 | yaml L23–29（sources[0]） | relationship "formalizes" NS-PROOF-FRAME-01 §3.1 | 帧 v1.1 §3.1 七格 DONE 在案；fidelity.divergences 一一对应经同制 sha256 核验 | **对齐** | 无 |
| U-04 | yaml L25（id 短钉） | 「qf-os://…NS-PROOF-FRAME-01.md@58dfb9a94311」 | 短钉 12-hex，非 git 40-hex；qf-os 协议解析规则未登记；本席无法一手核验 | **无证据** | 换 40-hex commit 钉或登记短钉解析规则（同制比对律） |
| U-05 | yaml L31–36（sources[1]） | 「本包不声明证明或证伪其 (A)/(B)/(C)/(D) 任一款」 | 帧 §2 距离声明 + §3.4 REJ-NS-01 | **对齐** | 无 |
| U-06 | yaml L37–42（sources[2]） | 「其口径：自评已核、外部复现中、未颁奖」 | 帧 §4.2 标准表述；EXT-WAVE-17 语言钉 | **对齐** | 无 |
| U-07 | yaml L45–47 | 「其语义失配已由 arXiv:2610.08144 独立揭示（作者立场：不证伪其 NL 论证）」 | FIDELITY-AUDIT §二（Lemma 8.6/(10.19) 两例实锤 + 作者立场钉）；EXT18 卡7 归因锁不主张先发现 | **对齐** | 无（日期钉 2026-10-06 建议随文补） |
| U-08 | yaml L48–50 | FGL「无许可证——洁净室双人制读思想重写，不逐行搬译」 | CLEANROOM-REDLINE-FGL-01；TRUSTBOUNDARY TB-10 | **对齐** | 无 |
| U-09 | yaml L57–61（status.scope） | 「有限维 Galerkin ODE 截断层…四项 BLOCKED(B1)…Clay NS 未解决、未颁奖」 | 帧 §3.3 + 附录 EXT12-A §D 模板逐字一致 | **对齐** | 附注：C1 逐字基准建议判定席明示以附录 D 模板为准（模板串「有限维 Galerkin ODE 截断层」中 Galerkin 嵌入 C1 引文「有限维 ODE 截断层」之内，按记号等价处置） |
| U-10 | yaml L62–63 | sorry_count: 0 / sorry_in_definitions: 0 | run 39214080542 sorry_count=0（EXT16 §4） | **对齐** | 无 |
| U-11 | yaml L64（status.axioms 包级） | axioms: [propext, Classical.choice, Quot.sound]（包级） | 现链公理审计仅 5 decl（inner_vf/inner_vf_le/norm_vf_le/inner_B_antisymm/SkewNonlinearity.antisymm，run 39214080542 axiomsA.log）；旧链 12 decl 审计属 v4.10.0 树且 decl 集不同 | **更强**（主张覆盖全包 56 decl，现链一手证据 5 decl） | 公理审计扩项至 main_results 全 9 件 + 包级闭包扫描后回填；回填前包级字段降级为「已审 5 decl 全三公理，余待审」 |
| U-12 | yaml L91–100（main_results 内 capAnchorP1 / zetaAnchorImpliesRHCriticalLine 之 axioms 字段） | 二 decl 各标 axioms 三公理、sorry 0 | 旧链 12 件 #print axioms 清单不含此二件；新链 5 件清单亦不含；census「axioms: 0」系 `axiom` 关键字扫描，非公理闭包审计 | **无证据** | 扩项公理审计补此二件（随 L2-2 LeanCert 复算窗口并做） |
| U-13 | yaml L76–80（galerkinNS_exists_unique_solution_upto 之 axioms） | 同上 | 旧链 12 件清单有其三组分（galerkinNS_exists_solution_upto / galerkinNS_energy_bound / galerkinNS_solution_unique）但无该打包 decl 本身 | **无证据**（打包 decl 未逐件审计） | 补审，或成文「由三已审组分直接打包」桥接论证留档 |
| U-14 | yaml L117（automation.tool_setup） | 「Lean 4.35.0 + mathlib v4.35.0 @56a00585…runs 39211461961, 39214080542」 | LAB-CLOSE-EXT16 §4/§6 | **对齐** | 无 |
| U-15 | yaml L124–129（fidelity.divergences） | 「51 decl 一一对应…+SkewB 5 decl 纯增量加性件…无弱化」 | census 同制 sha256 核验零漂移；EXT16 §6 | **对齐** | 无 |
| U-16 | yaml L131–138（review） | status "self-assessed"；reviewers 两判定席；「尚无联邦外第三方评审（G3 候选评估随 M4）」 | EXT12 11/11、EXT18 R2 3/3 在案 | **对齐**（联邦外第三方缺位如实披露） | 无 |
| U-17 | yaml L159–162（alignment 第 5 条） | 「NS-PROOF-FRAME-01 §3.2 见证层锚（CAP 证书锚 / ζ 锚）→ capAnchorP1, zetaAnchorImpliesRHCriticalLine」 | 帧 §3.2 实载 W-NS-01/02/03 三件见证，**无「CAP 证书锚 / ζ 锚」条目**（CapAnchor/ZetaAnchor 系 EXT-WAVE-10 后增录，帧 v1.1 未回写）；编号归属要素不符 | **无证据** | 修订 yaml source 指针（指向 census 增录注记）或帧侧补登记——按乙席总原则「裁决先行、登记同步、行文随后」办理 |
| U-18 | yaml L163–167（alignment 第 6 条） | §3.3 阻塞层 → not-formalized | 帧 §3.3/§3.3-A 在案 | **对齐** | 无 |
| U-19 | yaml L176–177（federation.certificate） | grade "G1"、issued_at 2026-10-17T07:00Z | L4-2 阶梯 G1=machine-attested；runs 39211461961/39214080542 在位 | **对齐** | 无 |
| U-20 | yaml L179–182（三槽哈希 + self_fingerprint） | log/statement/proof 三 SHA-256 + 联合指纹 | 本席未复算；系 run 产物登记转引（EXT16 §5 声明解冻依据） | **无证据**（未复算，转引层级二级） | 复算窗口随 LeanCert 接入（L2-2）并做；复算前对外引用须标「登记转引」 |

### 2.3 diff 主表（B：NS-PROOF-FRAME-01 v1.1 对外口径段，U-21…U-30）

| # | 句位 | 主张原文（摘） | 对应证据层 | 判定 | 处置建议 |
|---|---|---|---|---|---|
| U-21 | 帧 §4.2（L138） | 「自评已核（self-assessed）、外部复现中、Clay active 未颁奖、(A)/(B) 与无外力情形仍开放」 | OpenAI 仓 formalization.yaml review 字段（frontier_dim02 F2）；Clay 状态钉；CIV 双篇条件性定理（§4.1-A 同载义务） | **对齐** | 无 |
| U-22 | 帧 §4.3 表（L145） | 「全部定理 Lean 4.10.0 内核验证、零 sorry、公理仅三公理」 | 现链已迁 v4.35.0，三项全绿（runs 39211461961/39214080542，EXT16 §5 声明冻结解除） | **更弱**（口径保守且版本过时；证据已支持 v4.35.0 更强表述） | 帧 v1.2 升级口径并钉工具链版本；升级前引用须带「截至 2026-10-17」时间戳 |
| U-23 | 帧 §4.3 表（L145） | 「无 NL↔Lean 对齐缝（定理陈述即所证，有限维层语义无外推宣称）」 | 本包未历 L34 三层审计实做（规程 2026-10-21 方生效；前置 2 件忠诚审计对象为 §4.1 转述与文献锚，非本包定理级 alignment） | **无证据**（自评未审） | 降级为「自评未见对齐缝，三层审计待排期」；本包 alignment 三层自审列入旗舰示范案例轨任务单，W-NS-03 重铸终稿 diff 即首件实做（G0-5） |
| U-24 | 帧 §4.3 表（L146） | 「见证层严格限采样点区间实证 + 轨道包络如实 BLOCKED(B1) 登记，无未披露越界」 | §3.2 W-NS-01/02 DONE 携披露；W-NS-03 19/19 checks 注记「PASS 仅证登记格式合规」 | **对齐** | 无 |
| U-25 | 帧附录 EXT12-A §D（L229） | 「本包在有限维 Galerkin ODE 截断层完成 7 项形式化证明（Lean4，零 sorry），在见证层给出 2 项数值实证（携非轨道包络披露），四项 BLOCKED(B1)。Clay NS 未解决、未颁奖。」 | §3.1 七格 DONE（正证据合取）/§3.2 两件/§3.3 四格 | **对齐** | 附注：「7 项」与「14 主定理计数」粒度注记已挂 EXT12-A C-1，下修订版对齐引用面 |
| U-26 | 帧尾纪律重申（L201） | 「严禁表述为『NS 已解决』；严禁以 anchor_only 证据充内容认证；严禁以有限维层 DONE 外推 PDE/3D 本体」 | REJ-NS-01 终态登记；§3.1 anchor_only 域限 | **对齐** | 无 |
| U-27 | 帧 §3.3-A 修订授权行（L88）vs (b) 条（L93） | 「HWY 一律标『待评审预印本…』」（首现未展开） | (b) 条 Hou–Wang–Yang 全名展开在 L93，晚于 L88 首现；HWY 语态钉「报告了」在 (b) 条在位 | **更弱**（语态钉执行偏差：首现未展开） | 帧 v1.2 将 L88 HWY 展开为 Hou–Wang–Yang（HWY） |
| U-28 | 帧 §4.1（L121） | 「arXiv:2610.08144（2026-10-07）」 | §4.1-A 勘误 2026-10-06；FIDELITY-AUDIT §一清账 CLOSED | **对齐**（经修订条覆盖；覆写权纪律不改原文） | 无 |
| U-29 | 帧 §3.2 W-NS-02 行（L70） | 「携带『非轨道包络』honesty_boundary 并如实披露——证书语义严格限于登记采样点」 | C2 强制条件；TRUSTBOUNDARY TB-07 在案 | **对齐** | 无 |
| U-30 | 帧 §6 OBL-NS-03 行（L186） | 「当前仅多项式 IVP/Lorenz…中程工程评估；不承诺档期」 | arXiv:2610.02335 §6.2 逐字「left to separate work」；仓库私有（G0-1） | **对齐** | 无 |

### 2.4 判定汇总表（各态计数）

| 判定态 | 计数 | 单元 |
|---|---|---|
| 对齐 | 21 | U-01/02/03/05/06/07/08/09/10/14/15/16/18/19/21/24/25/26/28/29/30 |
| 更强 | 1 | U-11（包级 axioms 主张超现链一手审计覆盖） |
| 更弱 | 2 | U-22（工具链口径过时）、U-27（HWY 首现未展开） |
| 不可比 | 0 | — |
| 无证据 | 6 | U-04（短钉无法核验）、U-12（cap/zeta 二 decl 公理字段）、U-13（打包 decl 公理字段）、U-17（alignment 编号归属不符）、U-20（三槽哈希未复算）、U-23（「无对齐缝」自评未审） |

合计 30 单元（U-01…U-30；其中 U-03/U-04 由 yaml sources[0] 一条拆为关系语义与钉位两单元）。**三级判定合成（L3-4c 第 5 条）**：任何单层 FAIL 即整体 FAIL——U-11/U-12/U-13/U-17/U-20/U-23 六件按证据层从严登记，均未达「对齐」，formalization.yaml v0.5 对外口径整体记 **CONDITIONAL-PASS（附六项处置义务）**；NS-PROOF-FRAME-01 对外口径段记 **CONDITIONAL-PASS（附三项处置义务：U-22/U-23/U-27）**。处置义务汇入旗舰示范案例轨任务单，关闭后复审升态。

---

## 三、与既有纪律的衔接（C1/C2/C3 逐条落进立案书条文）

- **C1 落条**：本立案书及其下游一切对外引用（含 MS-1 重铸文、MS-2 diff 报告、schema 登记条目）必须逐字携带「有限维 ODE 截断层」限定；不得上推为 PDE 层陈述。重铸件语义（NK 时空管 + 捕获区全局化）虽面向 2D NS PDE 实例，其联邦交付层仍登记为见证层数值证书 + Lean 证书锚定端点，**不构成** PDE 层定理宣称；2D 全局存在系 Lions–Prodi 经典结果（§1.5-4 限定语同载）。违反 ⇒ 降格 undecided 并触发 REJECTED 格（G16）。
- **C2 落条**：本立案书引用 W-NS-02 之处（§1.1 两处——第 2 条捕获区段 EXT19 R1 已补钉、语义定位段原携带；§1.5-2；U-29）均已逐字携带「非轨道包络」；下游一切引用 W-NS-02 之文件同样逐字携带，且 W-NS-02 不得脱离 W-NS-03 状态单独引用为紧性证据。违反 ⇒ 降格 undecided。
- **C3 落条**：OBL-NS-01/02/03 未闭环前，本包（含重铸后 W-NS-03）不得被引用为「Clay NS 证据链的一环」；重铸件的 Cadiot–Lessard 模板引述同载「2D 全局存在系 Lions–Prodi 经典结果，本证书为构造性方法学复现 + 新实例」限定语，本身即 C3 之对象化执行。违反 ⇒ 越权引用按 G16 拒绝。

**合规自检（本文件行文）**：全文未出现「NS 已解决」式表述；OpenAI 结果引用维持「自评已核、外部复现中、未颁奖」；HWY 未于本文件首现引用（无需展开）；2610.08144 引述已同载作者立场钉与日期钉 2026-10-06；W-NS-02 引用逐字带「非轨道包络」；本文件仅新建此一件，未改任何既有文件，未执行 git 远端写操作。Clay NS 未解决、未颁奖。

—— WS-F 攻坚线执行席 · 枢/PIVOT-01 体系 · EXT-WAVE-18「攻」· 2026-10-21
