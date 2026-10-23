-- CLASSIFY: L1
/-
WS-H · EXT-WAVE-18 饱和批 · L2 席构件：内核/重检器接缝「规格环」骨架（SeamSpec）

## 任务登记（spike-B 报告呈批① · WS-H 一期 M0 启动预备首件）

- 上游：`board/TRUSTBOUNDARY-SPIKE-B-REPORT-01.md` §四（C2 引理集 L-1..L-5 锁定
  论证）、§五（V1–V5 映射）、§六呈批①（C1 Spec 环骨架 350–450 行先行件）；
  `board/TRUSTBOUNDARY-SPIKE-A-01.md`（六重检器 E2E 受理结论，GO+三条件）；
  `specs/FGL-SEAM-SPEC-01.md` 单元③/④（seam 数学语义之本：Remark 2.4 缝——
  图空间 H_Ω ↔ 经典 Sobolev 等同）。
- 定位：C4 标注承载与 C2 引理签收（Spec→Gap 接口契约：无 Spec 条目不得直跳
  Adapter）之共同前置钉桩表——只立规格环骨架，不做数学定理实质证明。

## 设计纪律

1. 仅声明类型、接口签名与陈述槽：抽象性全部经 structure 字段/参数表达，
   义务与引理陈述一律以 Prop 值字段承载，回填席举证即得签收形态。
2. 无占位证明符、无公理声明：能证的 glue 引理（合取单调性、预算带算术、
   信任级 min 代数、槽位依赖秩递减等平凡组合）均给出完整证明。
3. 仅用 Lean 核心库（Init prelude），禁 import mathlib；裸 lean 秒级编译验证。
4. 不接入 NsGalerkin 根聚合、不改 lakefile/lake-manifest；library/spec/ 不在
   任何 lake target 的 roots/globs 覆盖内（核查引文见文件尾 ledger）。

构件清单（七件）：钉与版本类型 / Verdict / 重检器与证书（RecheckerId·
Certificate·RecheckerInterface·PanelAllAccept）/ 义务谓词与信任级（TA-1..6·
T0–T2）/ C2 引理陈述槽（L-1..L-5）/ V1–V5 门谓词 / seam 一致性（Conforms·
SeamSignoff）。工具链钉：Lean 4.35.0（githash eb6cafb…），核心库 only。
-/
set_option autoImplicit false
namespace SeamSpec

/-! ## 一、钉与版本类型（TA-5 版本一致之机读载体） -/
/-- 工具链钉：仓库 / 版本 / githash 三字段（spike-A #7/#18：导出件 meta 头
自带 `lean.githash` 机读钉，本类型即其规格环侧承载形态）。 -/
structure ToolchainPin where
  repo : String    -- 仓库名（如 `leanprover/lean4`）
  version : String -- 版本标签（如 `v4.35.0`）
  githash : String -- 提交哈希（40 位十六进制串）
/-- 本线一期工具链钉（spike-A #5–#8：tarball 字节级对官方 API 核验在案）。 -/
def leanToolchainPin : ToolchainPin where
  repo := "leanprover/lean4"
  version := "v4.35.0"
  githash := "eb6cafb7290e8bd5f2937522d8d804f58f02bafc"
/-- glue 钉锁：一期工具链版本字段恒为 v4.35.0（漂移对照基准，R4 口径）。 -/
theorem leanToolchainPin_version : leanToolchainPin.version = "v4.35.0" := rfl
/-- 导出链钉：仓库 + 修订钉（spike-A #14 漂移活证：匹配钉 5a9a355dc6c5）。 -/
structure ExportChannelPin where
  repo : String -- 仓库名
  rev : String  -- 修订钉（提交哈希前缀或完整哈希）
/-- 一期导出链钉（lean4export "bump toolchain to v4.35.0 (#56)"）。 -/
def lean4exportPin : ExportChannelPin where
  repo := "leanprover/lean4export"
  rev := "5a9a355dc6c5"
/-- glue 钉锁：导出链修订字段恒为在案钉。 -/
theorem lean4exportPin_rev : lean4exportPin.rev = "5a9a355dc6c5" := rfl

/-! ## 二、判定枚举（重检器产出之数据面） -/
/-- 复核判定二值（Comparator 口径："Your solution is okay!" 对应 accept）。 -/
inductive Verdict where
  | accept
  | reject
  deriving DecidableEq, Repr

/-! ## 三、重检器枚举、证书类型与接口签名（TB-06 异构多核并轨之规格形态） -/
/-- 六重检器枚举（spike-A #24 `--paranoid` 并轨口径全名单）。 -/
inductive RecheckerId where
  | leanDefault
  | leanParanoid
  | lean4lean
  | nanoda
  | conLeche
  | conRon
  deriving DecidableEq, Repr
/-- 六重检器全名单（面板遍历基准）。 -/
def RecheckerId.all : List RecheckerId :=
  [.leanDefault, .leanParanoid, .lean4lean, .nanoda, .conLeche, .conRon]
/-- glue：面板基数恒为六（spike 实证口径之钉死）。 -/
theorem RecheckerId.all_length : RecheckerId.all.length = 6 := rfl
/-- 证书（cert）：一次导出+复核跑批之证据打包（纯数据面；义务见 §四）。 -/
structure Certificate where
  exportSha256 : String           -- 导出件 sha256（spike-A #19 双跑字节一致之锚）
  declCount : Nat                 -- 复核声明计数（spike-A #20：59,352 decl）
  verdicts : RecheckerId → Verdict -- 六件面板之逐核判定
  permittedConstants : List String -- 白名单公理（comparator 强制显式声明，#21）
/-- 重检器接口签名：判定函数 + 两条义务陈述槽（Prop 值字段，回填时举证）。 -/
structure RecheckerInterface where
  id : RecheckerId            -- 面板身份
  check : Certificate → Verdict -- 判定函数签名：消费证书证据，产出判定
  deterministic : Prop        -- 义务槽：同钉输入两次判定一致（TA-3 投影）
  sound : Prop                -- 义务槽：本核 accept ⇒ Lean kernel accept（TA-2）
/-- 面板全收谓词：证书所载六核判定全为 accept（TB-06 验收形态）。 -/
def PanelAllAccept (c : Certificate) : Prop :=
  ∀ r : RecheckerId, c.verdicts r = Verdict.accept
/-- glue：全称形态与名单遍历形态等价——面板语义不依赖枚举顺序。 -/
theorem PanelAllAccept.iff_all {c : Certificate} :
    PanelAllAccept c ↔ ∀ r ∈ RecheckerId.all, c.verdicts r = Verdict.accept := by
  constructor
  · intro h r _
    exact h r
  · intro h r
    cases r <;> exact h _ (by decide)

/-! ## 四、义务谓词与信任级（TA-1..TA-6 之规格环承载） -/
/-- 六条信任假设之义务谓词打包（spike-B §三 TA-1..TA-6 逐条对应，Prop 值槽）。 -/
structure ObligationPredicates where
  /-- TA-1 导出器保真性：导出件忠实序列化 kernel 环境，无声明丢失/篡改 -/
  exportFidelity : Prop
  /-- TA-2 复核器正确性：异构核 accept ↔ Lean kernel accept 一致（TCB） -/
  recheckerCorrectness : Prop
  /-- TA-3 环境确定性：同钉输入字节级可复现 -/
  envDeterminism : Prop
  /-- TA-4 缓存完整性：命中件未污染（anchor_only：命中仅证环境等价） -/
  cacheIntegrity : Prop
  /-- TA-5 版本一致：工具链/导出器/复核器/导出格式四方相干 -/
  versionCoherence : Prop
  /-- TA-6 时间测量可信：冷/暖定义、UTC(Z)、机器钉、测量方法四项成文 -/
  timingSoundness : Prop
/-- 义务全结合取（六条全结之规格形态）。 -/
def ObligationPredicates.All (o : ObligationPredicates) : Prop :=
  o.exportFidelity ∧ o.recheckerCorrectness ∧ o.envDeterminism ∧
    o.cacheIntegrity ∧ o.versionCoherence ∧ o.timingSoundness
/-- glue：义务合取之拆解（合取即其自身之六元组读法，elim 方向）。 -/
theorem ObligationPredicates.All.decompose {o : ObligationPredicates} :
    o.All → o.exportFidelity ∧ o.recheckerCorrectness ∧ o.envDeterminism ∧
      o.cacheIntegrity ∧ o.versionCoherence ∧ o.timingSoundness := fun h => h
/-- glue：义务合取单调性——逐条强化可抬升全结合取（C4 逐条签收总成组合子）。 -/
theorem ObligationPredicates.All.mono {o o' : ObligationPredicates}
    (h1 : o.exportFidelity → o'.exportFidelity)
    (h2 : o.recheckerCorrectness → o'.recheckerCorrectness)
    (h3 : o.envDeterminism → o'.envDeterminism)
    (h4 : o.cacheIntegrity → o'.cacheIntegrity)
    (h5 : o.versionCoherence → o'.versionCoherence)
    (h6 : o.timingSoundness → o'.timingSoundness) :
    o.All → o'.All := fun h =>
  ⟨h1 h.1, h2 h.2.1, h3 h.2.2.1, h4 h.2.2.2.1, h5 h.2.2.2.2.1, h6 h.2.2.2.2.2⟩
/-- 信任级三值（SIDECAR-SCHEMA-T0T4-01 §一.1 形态之子集；数值越高越稳固）。 -/
inductive TrustLevel where
  | T0
  | T1
  | T2
  deriving DecidableEq, Repr
/-- 信任级数值投影（排序基准）。 -/
def TrustLevel.rank : TrustLevel → Nat
  | .T0 => 0
  | .T1 => 1
  | .T2 => 2
/-- 信任级取弱（面板汇总运算：面板信任级＝逐件 min，木桶口径）。 -/
def TrustLevel.min : TrustLevel → TrustLevel → TrustLevel
  | .T0, _ => .T0
  | _, .T0 => .T0
  | .T1, _ => .T1
  | _, .T1 => .T1
  | .T2, .T2 => .T2
/-- glue：min 交换律。 -/
theorem TrustLevel.min_comm (a b : TrustLevel) :
    TrustLevel.min a b = TrustLevel.min b a := by
  cases a <;> cases b <;> rfl
/-- glue：min 结合律（面板汇总顺序无关性之基）。 -/
theorem TrustLevel.min_assoc (a b c : TrustLevel) :
    TrustLevel.min (TrustLevel.min a b) c =
      TrustLevel.min a (TrustLevel.min b c) := by
  cases a <;> cases b <;> cases c <;> rfl
/-- glue：min 幂等律。 -/
theorem TrustLevel.min_idem (a : TrustLevel) :
    TrustLevel.min a a = a := by
  cases a <;> rfl
/-- glue：min 之数值投影即数值 min（运算与排序相干）。 -/
theorem TrustLevel.rank_min (a b : TrustLevel) :
    (TrustLevel.min a b).rank = Nat.min a.rank b.rank := by
  cases a <;> cases b <;> rfl
/-- glue：取弱不升——min 之秩不超过左进项（右件由 min_comm 立得）。 -/
theorem TrustLevel.rank_min_le_left (a b : TrustLevel) :
    (TrustLevel.min a b).rank ≤ a.rank := by
  cases a <;> cases b <;> decide
/-- glue：min 之秩不超过右进项（交换律 + 左件版之组合）。 -/
theorem TrustLevel.rank_min_le_right (a b : TrustLevel) :
    (TrustLevel.min a b).rank ≤ b.rank := by
  rw [TrustLevel.min_comm]
  exact TrustLevel.rank_min_le_left _ _
/-- 面板信任级：列表逐件取弱（空面板约定为 T2 顶元，min 成幺半群）。 -/
def panelTrustLevel : List TrustLevel → TrustLevel
  | [] => .T2
  | l :: ls => TrustLevel.min l (panelTrustLevel ls)
/-- glue：面板信任级不高于首件（木桶口径之逐件投影首例）。 -/
theorem panelTrustLevel_cons_le_head (l : TrustLevel) (ls : List TrustLevel) :
    (panelTrustLevel (l :: ls)).rank ≤ l.rank := by
  show (TrustLevel.min l (panelTrustLevel ls)).rank ≤ l.rank
  exact TrustLevel.rank_min_le_left _ _
/-- spike-B §三终稿建议之 T 级分布在册实例：T1×4（TA-1/2/3/5）+ T0×2。 -/
def spikeBTrustPanel : List TrustLevel := [.T1, .T1, .T1, .T1, .T0, .T0]
/-- glue：spike-B 面板汇总为 T0——「面板信任级＝最弱件」之活例
（TA-4/TA-6 未定项决定面板下限）。 -/
theorem spikeBTrustPanel_level : panelTrustLevel spikeBTrustPanel = .T0 := rfl

/-! ## 五、C2 引理陈述槽（L-1..L-5 锁定集之钉桩表）
spike-B §四锁定：主选 4 件（L-1..L-4）+ 缓冲 1 件（L-5），行数带 800–950
（含簇内公共底座）；服务对象＝Remark 2.4 缝。槽位一律为 Prop 值字段，
本骨架只钉「陈述之型」，证明回填属 C2 增量（见文件尾 ledger §三）。 -/
/-- C2 引理槽位枚举（L-1..L-5）。 -/
inductive LemmaSlotId where
  | l1
  | l2
  | l3
  | l4
  | l5
  deriving DecidableEq, Repr
/-- 槽位 → 规格指针（FGL-SEAM-SPEC-01 单元③/④ + 数学模块锚）。 -/
def LemmaSlotId.specAnchor : LemmaSlotId → String
  | .l1 => "单元③ 3.1 图空间实现 [BoxSobolevClosure/OpenDomainCore]"
  | .l2 => "单元③ 3.2 S5 紧性的子空间转移 [CompactSubspaceEmbedding]"
  | .l3 => "单元④ 4.2 G1 紧性遗传 [OpenDomainGelfandTriple]"
  | .l4 => "单元④ 4.2 G2 有界开域围合 [OpenDomainBoundedEnclosure]"
  | .l5 => "单元③ 3.2 S1 指标可数性 / S3 收缩性（缓冲件）"
/-- 槽位行数预算下界（spike-B §四锁定清单逐件口径）。 -/
def LemmaSlotId.budgetLo : LemmaSlotId → Nat
  | .l1 => 250
  | .l2 => 150
  | .l3 => 150
  | .l4 => 80
  | .l5 => 80
/-- 槽位行数预算上界（同口径）。 -/
def LemmaSlotId.budgetHi : LemmaSlotId → Nat
  | .l1 => 300
  | .l2 => 200
  | .l3 => 200
  | .l4 => 120
  | .l5 => 100
/-- glue：主选 4 件预算合计 630–820 行（spike-B 行数闭合论证之钉）。 -/
theorem LemmaSlotId.mainBudgetLo :
    budgetLo .l1 + budgetLo .l2 + budgetLo .l3 + budgetLo .l4 = 630 := rfl
theorem LemmaSlotId.mainBudgetHi :
    budgetHi .l1 + budgetHi .l2 + budgetHi .l3 + budgetHi .l4 = 820 := rfl
/-- glue：带缓冲件合计 710–920 行——两口径均落入 800–950 行带容差覆盖域。 -/
theorem LemmaSlotId.withBufferBudgetLo :
    budgetLo .l1 + budgetLo .l2 + budgetLo .l3 + budgetLo .l4 + budgetLo .l5
      = 710 := rfl
theorem LemmaSlotId.withBufferBudgetHi :
    budgetHi .l1 + budgetHi .l2 + budgetHi .l3 + budgetHi .l4 + budgetHi .l5
      = 920 := rfl
/-- 槽位证明依赖（spike-B §四锁定链：L-3 ← L-1+L-2 直上；余为底层/独立）。 -/
def LemmaSlotId.dependsOn : LemmaSlotId → List LemmaSlotId
  | .l1 => []
  | .l2 => []
  | .l3 => [.l1, .l2]
  | .l4 => []
  | .l5 => []
/-- 槽位深度秩（依赖层级之机读化：底层 0，L-3 为第三环 1）。 -/
def LemmaSlotId.depthRank : LemmaSlotId → Nat
  | .l1 => 0
  | .l2 => 0
  | .l3 => 1
  | .l4 => 0
  | .l5 => 0
/-- glue：依赖严格沿秩递减方向——回填顺序自下而上可行（无环之秩证）。 -/
theorem LemmaSlotId.dependsOn_depthRank_le {s d : LemmaSlotId}
    (h : d ∈ s.dependsOn) : d.depthRank ≤ s.depthRank := by
  cases s <;> cases d <;> first
    | exact absurd h (by decide)
    | decide
/-- glue：无自依赖（槽位图无自环）。 -/
theorem LemmaSlotId.not_self_dep {s : LemmaSlotId} : s ∉ s.dependsOn := by
  cases s <;> decide
/-- C2 引理陈述槽打包：五件 Prop 值字段，各对应锁定清单一件之**陈述之型**。
回填席以 mathlib 底座实例化各槽（如图空间闭包等同之实际命题），
举证后即得 C2Signoff 签收形态。 -/
structure C2LemmaSlots where
  /-- L-1 图空间实现：光滑发散自由场图点 (u,Du) 在 L²×L² 之闭包＝H¹_{0,σ}，
  J＝分量投影（免 Stokes 算子/椭圆正则性） -/
  l1_graphSpaceRealization : Prop
  /-- L-2 S5 紧性的子空间转移：闭子空间沿闭嵌入继承紧性/单射/收缩，
  稠密性显式携带 -/
  l2_compactSubspaceTransfer : Prop
  /-- L-3 G1 紧性遗传：J_Ω 经盒闭子空间包含与盒 J_Q 交换，S5+盒 Rellich
  ⇒ J_Ω 紧（盒 Rellich 为引用口径，不入本簇行数） -/
  l3_openDomainCompactness : Prop
  /-- L-4 G2 有界开域围合：任意有界开平面集 U 存在矩形 Q 使 U⊂int(Q) -/
  l4_boundedEnclosure : Prop
  /-- L-5 缓冲件：S1 指标可数性 或 S3 收缩性自动成立（纳入条件：主选提前
  闭合且行数结余 ≥100，禁挤占主选件行数） -/
  l5_buffer : Prop
/-- 五槽陈述全结合取。 -/
def C2LemmaSlots.All (s : C2LemmaSlots) : Prop :=
  s.l1_graphSpaceRealization ∧ s.l2_compactSubspaceTransfer ∧
    s.l3_openDomainCompactness ∧ s.l4_boundedEnclosure ∧ s.l5_buffer
/-- C2 引理签收形态：对给定陈述槽打包逐槽举证（证明作为字段值，
非占位定理——抽象性由槽打包之参数表达）。 -/
structure C2Signoff (s : C2LemmaSlots) where
  l1 : s.l1_graphSpaceRealization
  l2 : s.l2_compactSubspaceTransfer
  l3 : s.l3_openDomainCompactness
  l4 : s.l4_boundedEnclosure
  l5 : s.l5_buffer
/-- glue：签收即全体陈述成立（Spec→Gap 接口契约之机读形态）。 -/
theorem C2Signoff.all {s : C2LemmaSlots} (sg : C2Signoff s) : s.All :=
  ⟨sg.l1, sg.l2, sg.l3, sg.l4, sg.l5⟩
/-- glue：陈述槽合取之单调性——陈述细化（逐槽蕴含）沿全结合取抬升，
「陈述修订不破坏已签收总成」之机读组合子。 -/
theorem C2LemmaSlots.All.mono {s s' : C2LemmaSlots}
    (h1 : s.l1_graphSpaceRealization → s'.l1_graphSpaceRealization)
    (h2 : s.l2_compactSubspaceTransfer → s'.l2_compactSubspaceTransfer)
    (h3 : s.l3_openDomainCompactness → s'.l3_openDomainCompactness)
    (h4 : s.l4_boundedEnclosure → s'.l4_boundedEnclosure)
    (h5 : s.l5_buffer → s'.l5_buffer) :
    s.All → s'.All := fun h =>
  ⟨h1 h.1, h2 h.2.1, h3 h.2.2.1, h4 h.2.2.2.1, h5 h.2.2.2.2⟩

/-! ## 六、V1–V5 门谓词（验收钉之规格环形态）
spike-B §五映射：V1 build 绿 / V2 标注覆盖度 / V3 schema 回填 /
V4 spike 回退闸 / V5 合规钩。门谓词为 Prop 值字段，实证回填时举证。 -/
/-- 验收门枚举（V1–V5）。 -/
inductive GateId where
  | v1
  | v2
  | v3
  | v4
  | v5
  deriving DecidableEq, Repr
/-- 门 → 验收钉题名（registry/裁决书口径转写）。 -/
def GateId.title : GateId → String
  | .v1 => "V1 build 绿（v4.35.0 + mathlib 钉版 零占位、白名单三公理）"
  | .v2 => "V2 标注覆盖度 100%（L34a/b/c 三态 + ≥10% 抽查人工复核）"
  | .v3 => "V3 schema 字段回填（S1–S6 全实测，未定 ≤1）"
  | .v4 => "V4 spike 回退闸（spike 验估 ≤2pw）"
  | .v5 => "V5 合规钩（八卡常设钩 + 对外口径）"
/-- 门谓词打包：五条 Prop 值字段，各对应一钉之验收条件。 -/
structure GatePredicates where
  /-- V1：工具链+依赖钉版下零占位构建绿，白名单公理不越单 -/
  v1_buildGreen : Prop
  /-- V2：L34 三态标注全覆盖且抽查复核通过 -/
  v2_annotationCoverage : Prop
  /-- V3：S1–S6 验证点字段全实测回填（未定项 ≤1） -/
  v3_schemaBackfill : Prop
  /-- V4：spike 实耗 ≤2pw 闸内（spike-B §5.2 自查：2.0–3.0pd ≈ 0.4–0.6pw） -/
  v4_spikeWithinBudget : Prop
  /-- V5：叙事合规常设钩就位且适用范围在案 -/
  v5_complianceHooks : Prop
/-- 五门全绿合取。 -/
def GatePredicates.All (g : GatePredicates) : Prop :=
  g.v1_buildGreen ∧ g.v2_annotationCoverage ∧ g.v3_schemaBackfill ∧
    g.v4_spikeWithinBudget ∧ g.v5_complianceHooks
/-- glue：由逐门举证总成全绿（intro 方向）。 -/
theorem GatePredicates.All.intro {g : GatePredicates}
    (h1 : g.v1_buildGreen) (h2 : g.v2_annotationCoverage)
    (h3 : g.v3_schemaBackfill) (h4 : g.v4_spikeWithinBudget)
    (h5 : g.v5_complianceHooks) : g.All :=
  ⟨h1, h2, h3, h4, h5⟩
/-- glue：全绿合取之拆解（elim 方向，五元组读法）。 -/
theorem GatePredicates.All.decompose {g : GatePredicates} :
    g.All → g.v1_buildGreen ∧ g.v2_annotationCoverage ∧ g.v3_schemaBackfill ∧
      g.v4_spikeWithinBudget ∧ g.v5_complianceHooks := fun h => h
/-- glue：门谓词合取之单调性——逐门强化可抬升全绿合取
（验收条件细化不破坏已过闸总成之机读组合子）。 -/
theorem GatePredicates.All.mono {g g' : GatePredicates}
    (h1 : g.v1_buildGreen → g'.v1_buildGreen)
    (h2 : g.v2_annotationCoverage → g'.v2_annotationCoverage)
    (h3 : g.v3_schemaBackfill → g'.v3_schemaBackfill)
    (h4 : g.v4_spikeWithinBudget → g'.v4_spikeWithinBudget)
    (h5 : g.v5_complianceHooks → g'.v5_complianceHooks) :
    g.All → g'.All := fun h =>
  ⟨h1 h.1, h2 h.2.1, h3 h.2.2.1, h4 h.2.2.2.1, h5 h.2.2.2.2⟩

/-! ## 七、seam 一致性（conformance）定义与签收形态
规格环总成：证书（数据面）+ 义务（TA 槽）+ 引理槽（C2 桩）+ 门（V 钉）
四位一体；一致性＝四面全结之合取。 -/
/-- seam 见证打包：一致性判定之全部输入。 -/
structure SeamWitness where
  cert : Certificate               -- 证书（导出+复核跑批证据）
  obligations : ObligationPredicates -- 义务谓词打包（TA-1..TA-6 槽）
  slots : C2LemmaSlots             -- C2 引理陈述槽打包
  gates : GatePredicates           -- 门谓词打包（V1–V5 钉）
/-- seam 一致性：①六重检器面板全收；②义务六条全结；③C2 五槽陈述全结；
④V 五门全绿——四者合取为接缝闭合之规格环判定形态。
（页脚训诫口径：本定义为机器层必要条件之规格化；语义缝 TB-09 之闭合判定
须经 L3-4a/b/c 三层人工审计与判定席裁决，永不被编译绿灯吸收。） -/
def Conforms (w : SeamWitness) : Prop :=
  PanelAllAccept w.cert ∧ w.obligations.All ∧ w.slots.All ∧ w.gates.All
/-- glue：一致性之总成构造（intro 方向）。 -/
theorem Conforms.intro {w : SeamWitness}
    (hc : PanelAllAccept w.cert) (ho : w.obligations.All)
    (hs : w.slots.All) (hg : w.gates.All) : Conforms w :=
  ⟨hc, ho, hs, hg⟩
/-- glue：一致性之四面拆解（elim 方向）与门绿投影。 -/
theorem Conforms.decompose {w : SeamWitness} :
    Conforms w → PanelAllAccept w.cert ∧ w.obligations.All ∧ w.slots.All ∧
      w.gates.All := fun h => h
theorem Conforms.gatesAll {w : SeamWitness} (h : Conforms w) :
    w.gates.All := h.2.2.2
/-- glue：一致性之细化单调——四面各自强化（蕴含细化）可抬升总成；
回填席逐面加固证据时，已得一致性沿本组合子自动转移。 -/
theorem Conforms.refine {w w' : SeamWitness}
    (hc : PanelAllAccept w.cert → PanelAllAccept w'.cert)
    (ho : w.obligations.All → w'.obligations.All)
    (hs : w.slots.All → w'.slots.All)
    (hg : w.gates.All → w'.gates.All) :
    Conforms w → Conforms w' := fun h =>
  ⟨hc h.1, ho h.2.1, hs h.2.2.1, hg h.2.2.2⟩
/-- seam 签收形态：一致性之证明作为字段值入档（Spec→Gap→签收 闭环之
终端记录型）。 -/
structure SeamSignoff (w : SeamWitness) where
  conformance : Conforms w -- 一致性举证
/-- glue：签收即五门全绿（验收钉面之直接投影）。 -/
theorem SeamSignoff.gatesAll {w : SeamWitness} (s : SeamSignoff w) :
    w.gates.All :=
  Conforms.gatesAll s.conformance
/-- glue：C2 签收 + 其余三面 ⇒ seam 一致性——C2 引理回填进入总成之标准
通道（C2Signoff 经 C2Signoff.all 化入第三面）。 -/
theorem conforms_of_c2Signoff {w : SeamWitness}
    (hp : PanelAllAccept w.cert) (ho : w.obligations.All)
    (hg : w.gates.All) (sg : C2Signoff w.slots) : Conforms w :=
  Conforms.intro hp ho sg.all hg
end SeamSpec
/-
## 文件尾 ledger（SeamSpec · C1 规格环骨架 · 对应 spike-B §六呈批①）

### 一、呈批①逐条对拍

证书（cert）类型→`Certificate`；重检器接口签名→`RecheckerId`×6 +
`RecheckerInterface` + `PanelAllAccept`；义务谓词（Prop 值字段）→
`ObligationPredicates`（TA-1..6）；L-1..L-5 陈述槽（可证字段类型而非占位
定理）→`LemmaSlotId` + `C2LemmaSlots` + `C2Signoff`；V1–V5 门谓词→`GateId` +
`GatePredicates`；seam 一致性→`SeamWitness` + `Conforms` + `SeamSignoff`；
零占位/零公理、可证 glue 尽证→全文定理均闭证（合取单调性×3、预算带算术×4、
min 代数×5、槽位依赖秩×2、面板/钉锁等价若干）；行数带 350–450→实测 450 行。

### 二、L-1..L-5 槽位清单 与 V 门映射

L-1 图空间实现（单元③3.1，250–300 行，槽 `l1_graphSpaceRealization`）；
L-2 S5 紧性子空间转移（③3.2，150–200，槽 `l2_compactSubspaceTransfer`）；
L-3 G1 紧性遗传（④4.2，150–200，槽 `l3_openDomainCompactness`，依赖 L-1+L-2）；
L-4 G2 有界开域围合（④4.2，80–120，槽 `l4_boundedEnclosure`）；
L-5 缓冲 S1/S3（③3.2，80–100，槽 `l5_buffer`，主选提前闭合且结余 ≥100 方启动）。
V1↔`v1_buildGreen`；V2↔`v2_annotationCoverage`；V3↔`v3_schemaBackfill`；
V4↔`v4_spikeWithinBudget`；V5↔`v5_complianceHooks`。

### 三、lakefile 核查（lake build 行为不变之据）

`library/ns/lakefile.lean`（HEAD d956cdb21 原文）：`@[default_target]
lean_lib NsGalerkin where`——未配 roots/globs，默认 `Glob.one `NsGalerkin`，
仅覆 library/ns/NsGalerkin/；`artifacts/CERT-CIRC-LEAN-01/lakefile.toml`
`roots = ["CertCircLean01"]` 亦不覆 library/spec/。本件未改任何
lakefile/lake-manifest/根聚合文件，`lake build` 目标集合不变。

### 四、下一增量（C2 引理回填路径）

C2 各引理件于 mathlib 底座之独立模块内以实际命题实例化 `C2LemmaSlots` 五槽，
举证构造 `C2Signoff`，经 `conforms_of_c2Signoff` 化入 seam 一致性总成；回填
顺序按 `LemmaSlotId.dependsOn_depthRank_le` 自下而上（L-1/L-2/L-4→L-3，L-5 缓冲
视结余）；任一主选件行数上穿 1.5 倍即触发降级登记备选轨（呈判定席，禁静默）。
-/
