CLASSIFY: L1
# TRUSTBOUNDARY-REGISTRY-01 — L4-3 SeamSpec TrustBoundary 明轨登记 + kernel 化一期 spike 立案书

- 波次/线：EXT-WAVE-18「攻」 WS-H 攻坚线执行席 · 枢/PIVOT-01 体系
- 日期钉：2026-10-21（UTC(Z) 单时钟域；现状类断言均带「截至[日期]」钉，EXT18 卡6）
- 裁决依据：EXT18 生效体卡3——「TrustBoundary 明轨登记即落地（书面裁决+双登记）；kernel 化另立工程卡，spike 验估后分两期（一期 ~1.5k 行带 alignment 标注兼作 schema 试金石；二期旗舰 v0 后议）；下游依赖清单登记」
- 上游：WS-44《NS-SOLUTION-v2 设计书》§六 L4-3 / §八之五卡3；`registry/SIDECAR-SCHEMA-T0T4-01.md`（T0–T4 口径）；`registry/palomar-registry-v1.yaml`（PAL-0001/PAL-0002）；`library/ns/formalization.yaml`；`board/NS-PROOF-FRAME-01.md`（三层分立/REJECTED 格/见证层口径）；`board/FIDELITY-AUDIT-PROTOCOL-L34-01.md`（L3-4a/b/c 三层规程）
- 双登记并轨：本文件为「书面裁决登记」半；「机读登记」半＝本表 §六裁定段与后续注册表新条目（append-only 追加，不改 PAL-0001/0002）
- 语纪律：C1–C3 + C1′–C3′ 全文有效；OpenAI 相关成果口径固定「自评已核、外部复现中、未颁奖」；严禁「NS 已解决」式表述

---

## 一、登记口径（T 级定级规则）

1. 每条信任边界按 SIDECAR-SCHEMA-T0T4-01 §二字段表定级：T 级描述**该边界当前在册证据记录**所达形态（T0 自述 / T1 机器佐证 / T2 注册表见证 / T3 外部审计 / T4 作者背书），非边界对象本身的「可信程度」。
2. 信任性质三态：**TCB**（可信计算基——只能信任、无法在本体系内自证）；**已证伪可审计**（存在可执行的 falsification/复核机制，失配可检出）；**未审计**（机制未跑或证据未获，记「未定+理由」）。
3. 「截至 2026-10-21」口径说明：NsGalerkin 现身为 **9 文件 56 decl / 1192 行**（原 8 文件 51 decl + M1-1 转正 SkewB 5 decl，纯增量加性件）；本文凡引「51 decl」处均标注为 M1-1 前存量口径。

---

## 二、明轨登记表（12 条边界）

| id | 边界名 | 信任对象 | 信任性质 | 当前证据指针 | T 级 | 缺口与关闭路径 |
|---|---|---|---|---|---|---|
| TB-01 | Lean 内核演绎核心 | Lean 4 kernel（v4.35.0 之 kernel 组件） | **TCB**（终极信任基，体系内不可自证；异构内核仅交叉旁证） | runs 39211461961（build 绿）/ 39214080542（sorry=0、公理仅 propext/Classical.choice/Quot.sound）；PAL-0001 evidence.runs | **T1** | 缺口：kernel 正确性依赖社区与异构内核，联邦无双核执行记录。关闭：OBL-NS-02 下一见证窗口执行双核（EXT18 卡7 已授权，钉 f9e8bc5）；kernel 修复 #15241/#15288/#15289 随 v4.35.0 并轨在案（WS44 L0-1） |
| TB-02 | 工具链供应链 | leanprover/lean4:v4.35.0 pin（lean-toolchain 文件 + elan 下载通道） | **TCB**（供应链层；下载完整性信任 elan/官方 release 通道） | PAL-0001 artifact_sha256 toolchain 槽 `ca5f1f60…2330c`；formalization.yaml automation.methods[0].tool_setup | **T1** | 缺口：elan 下载通道完整性未审计——未定+理由：联邦尚无 release 哈希对照规程。关闭：官方 release SHA 对照入册（随 L0-2 依赖钉定簿扩展） |
| TB-03 | mathlib 源码真身 | mathlib4 v4.35.0 @ `56a005855ea17e0b0958f73ec801ae140b0a1679` | **TCB 内经 kernel 复核**（定理经 kernel；信任点在「源码未被替换」） | PAL-0001 dependencies 槽 `c3981e3e…28d07`（lake-manifest.json 全钉，与 yaml 自述 @56a00585 一致，2026-10-21 实测核对） | **T1** | 缺口：mathlib 全量声明语义未逐条审计（体量级不可行）。关闭：Comparator 声明级字节比对（TB-06）+ Tenet 对 mathlib 702,040 checked 0 failed 旁证（PAL-0002 corroboration） |
| TB-04 | cache CDN | mathlib 官方 cache（`lake exe cache get/unpack`） | **已证伪可审计**（anchor_only：命中仅支撑环境等价，不构成内容认证——NS-PROOF-FRAME §3.1 证据 3 口径） | 4.10.0 时代 4878/4878 全命中记录（frame §5.1）；v4.35.0 随 M1-1 迁移三绿 | **T1**（环境等价层；内容认证层不适用） | 缺口：cache 若被污染而无全量重编则不可感知。关闭：关键验收窗全量重编（全新克隆 410s 复现已有一次先例）+ Comparator 比对 |
| TB-05 | 公域 CI 通道 | GitHub Actions ubuntu-latest（runs 宿主） | **未审计**（runner 完整性与日志真实性信任平台方） | runs 39211461961 / 39214080542；产物三槽哈希入 formalization.yaml federation.certificate.artifact_digests（log/statement/proof） | **T1** | 缺口：CI 产物无法独立证明 runner 诚实执行。关闭：本地/异构环境同钉复跑（frame §5.1 复现指令成文）；见证窗口自跑替代转述 |
| TB-06 | Comparator 类外部复核 | `lake comparator` / `lake check` 声明级字节比对 | **已证伪可审计**（机制已设计在案，基线未跑——未定+理由：随 L0-1 节奏，未单列执行窗） | WS44 L3-1 设计行；官方六条信任假设待登记；comparator#77 可写 .lake/ 竞态已入风险簿 | **T0**（设计自述在册，实测记录未产） | 缺口：15–60min 暖缓存基线报告未产出；六条信任假设未逐条入册。关闭：随 L0-1 落地出基线报告；竞态项列入核查器放行清单声明 |
| TB-07 | 见证层采样代码 | witness_ns_gen/verify.py（python 3.12 + mpmath 1.3.0 + numpy + scipy 1.16） | **已证伪可审计**（fail-closed、负控必拒、生成器/核验器零共享代码、replay 全哈希链第三方可重放） | run ws43-ns-20261012T171410Z；W-NS-01（288 例能量相消，max_rel_width 3.99e-50）/ W-NS-02（3640 点 Grönwall，**非轨道包络**披露）DONE；tests 20/20 | **T1** | 缺口：采样证书语义严格限采样点（C2 披露不可剥离）；python/mpmath 运行时本身未审计。关闭：LeanCert 接入复算 CapAnchor 证书（WS44 L2-2，2–4 pd）；W-NS-03 BLOCKED(B1) 维持 |
| TB-08 | NsGalerkin 自有声明 | 自有 56 decl / 9 文件（M1-1 前存量口径 51 decl / 8 文件） | **TCB 内经 kernel 验证**（公理白名单内、零 sorry；机器层缺口为零） | PAL-0001 source-stream 槽 `2cfdcf96…c0172`（1192 行合并流，recipe 在册）；run 39214080542 五 decl 公理审计 | **T1** | 缺口：机器层无；语义层缺口见 TB-09。关闭：维持零漂移（同制 sha256 核验，普查 NS-PACKAGE-CENSUS-01-20261017T0444Z） |
| TB-09 | NL↔Lean alignment 缝 | frame §3.1 ↔ 56 decl 映射、Fefferman 背景陈述、SeamSpec 语义桥 | **未审计**（翻译缝不受内核保护；SCI=∞——审计永不可被编译绿灯吸收，L34 训诫条） | formalization.yaml alignment.statements[]（proved/not-formalized 状态机）；FIDELITY-AUDIT-PROTOCOL-L34-01 三层规程 | **T0**（自述登记） | 缺口：L3-4a/b/c 三层审计未对本包映射对全单元执行；标注无机读载体。关闭：**kernel 化一期（§四）**——标注层 + Gap 环引理簇 + 三层审计首跑 |
| TB-10 | 外部思想源锚 | FGL @4d023ac（**无许可证**）、OpenAI 仓 @f9e8bc5、formal-conjectures @8bf45ed、RadiiPolynomial @162f | **未审计外部依赖**（思想引入非代码信任；FGL 走红线「读思想重写」） | formalization.yaml related_formalizations；board/CLEANROOM-REDLINE-FGL-01（洁净室双人制）；WS44 L0-2/L0-3 | **T0** | 缺口：洁净室留痕待 L1-2 启动方产证；RadiiPolynomial 可见性 Gate 0 未过。关闭：Reader/Writer 分仓留痕（卡5）；外部锚一律 commit 全钉（L0-2，4 钉齐为验收钉） |
| TB-11 | 第三方机器见证 | Tenet 对 openai/NavierStokesAndEuler 全闭包复检（keithadler，主体匿名性已标注） | **已证伪可审计**（第三方独立复跑，指令公开可复现；原始产物未获） | PAL-0002 G2 候选观察条（判据 1 满足/2 部分/4 不满足；scope_limit 载「内核见证不覆盖语义层」） | **T1**（部分 T2 字段在案但不齐套，不构 T2） | 缺口：GAP-PAL0002-1..4（40-hex 全钉/产物三哈希/双核+LLM 二审/独立性核验）。关闭：OBL-NS-02 窗口联邦自跑，自产证据替代转述证据 |
| TB-12 | 册仓/注册表治理通道 | append-only 注册表 + git 托管 + schema 校验（check-jsonschema） | **TCB**（治理层信任基；git 历史与判定席双轮律为托） | palomar-registry-v1.yaml PAL-0001（head 全钉 `1345a48ba81acb606be533dc25ec6bf4e96127ee`、tree `eab2ed09f18e996d0c03fab950d4ef2ce02f357e`）；SIDECAR-SCHEMA-T0T4-01 | **T1**（签发流程在册；self_fingerprint 未定+理由：须入册仓后由 ledger 对定稿实测回填，禁预填） | 缺口：注册表自指哈希未回填；schema 校验 CI 钩子未钉版本。关闭：入册仓后 ledger 实测回填；校验工具版本钉随 L0-2 |

**T 级分布一句话**（截至 2026-10-21）：12 条边界——T1 级 8 条（TB-01/02/03/04/05/07/08/11）、T0 级 4 条（TB-06/09/10/12）、T2 及以上 0 条；最高边际收益缺口集中于 TB-09（alignment 缝）。

---

## 三、SeamSpec 三环映射（按 WS44 L4-3 展开）

三环定义（SeamSpec.lean 体例，源＝Fefferman 官方陈述 (12)(13) + Temam，**禁以 FGL 自定义为源**——防 Gap 退化恒等）：

- **环一 · Spec 环（语义规格环）**：NL 源的机读规格层——Fefferman (12)(13) 与 Temam 经典陈述的要素化结构（量词/函数类/范数/常数/谓词/编号六要素）。
  - 归入边界：TB-09（缝的 NL 侧）、TB-10（外部思想源的语义锚）。
- **环二 · Gap 环（语义缝环）**：Spec↔Lean 之间缺口的显式登记层——每条缝二态：kernel 化引理闭合 或 TrustBoundary 降级登记（**须判定席裁决，禁静默**，WS44 L4-3）；Remark 2.4（图空间↔经典 Sobolev 等同）为本环首席缺口。
  - 归入边界：TB-09（缝本体）、TB-11（外部见证的语义层免责——内核见证不闭合本环任何缝）。
- **环三 · Adapter 环（适配实现环）**：30 行级 Lean 适配层——Spec/Gap 已定条目到 NsGalerkin 现有 decl 的接口定理。
  - 归入边界：TB-08（自有 decl）、TB-03（mathlib 接口）。
- **环下基座（非环成员，三环共同之托）**：TB-01/02/04/05/06/07（TCB 与证据基座）；**环上治理**：TB-12（登记与裁决通道）。

环间接口契约（一句话/接口）：
1. **Spec→Gap**：Spec 环只出 L3-4a 八项钉桩的要素级对照表条目，Gap 环逐条签收（闭合/降级二态），无条目不得直跳 Adapter。
2. **Gap→Adapter**：Adapter 环只对 Gap 环已裁定条目生成适配代码；降级登记的缝以 `not-formalized` 显式状态入 alignment 表（防范围误读先例：formalization.yaml §3.3 条）。
3. **Adapter→基座/治理**：Adapter 环编译产物过 T1 三绿基线（build/sorry-scan/axiom-audit）+ Comparator 字节比对后，方许以新条目回填注册表（append-only）。

---

## 四、kernel 化一期 spike 立案书（本波只立案，不执行代码）

### 4.1 定位与判选原则

- 定位：EXT18 卡3「kernel 化另立工程卡，spike 验估后分两期」之**一期立案**；二期旗舰 v0 后另议，不在本立案范围。
- 判选原则：从 §二信任表挑「T0/未审计 → kernel 可核/T1+」边际收益最高者。结论：TB-09（alignment 缝，全表唯一 T0 且为旗舰 L4-5 前置）收益最高；TB-06（Comparator 实测）随件；TB-07 之 LeanCert 复算留二期候选。

### 4.2 范围：构件清单（~1.5k 行目标，±15% 容差）

| 构件 | 内容 | 行数预算 | 服务边界 | 依据 |
|---|---|---|---|---|
| C1 Spec 环骨架（SeamSpec.lean） | Fefferman (12)(13)+Temam 源的要素化机读结构体（六要素字段 + 编号映射表） | 350–450 行 | TB-09 | WS44 L4-3「Spec 2–4pd」 |
| C2 Gap 环一期核心引理簇 | Remark 2.4 kernel 化之 spike 核心：图空间 H_Ω ↔ 经典 Sobolev 等同的关键引理 3–5 件（D01 九项 W1–W9 中可裁减子集） | 800–950 行 | TB-09（缝本体闭合试样） | WS44 L1-3（全量 4–16pw/1.5k–4k 行，一期取下端子集） |
| C3 Adapter 环 | Spec/Gap 已定条目 ↔ NsGalerkin 现有 56 decl 的接口定理 | 30–50 行 | TB-08↔TB-09 接缝 | WS44 L4-3「Adapter 1pd/30 行级」 |
| C4 alignment 标注层 | 机读标注（§4.3 约定）+ yaml 回填 | 150–250 行（注释+数据） | TB-09 登记载体 | schema 试金石要件（卡3） |
| **合计** | | **1330–1700 行，目标钉 1.5k** | | |

明确排除（防范围蔓延）：LeanCert 复算（L2-2 独立件）、FGL 九项全量移植（L1-2 主工程 24–39pw）、2D IPM（卡8b 缓议至旗舰 v0 后）。

### 4.3 alignment 标注约定（与 FIDELITY-AUDIT-PROTOCOL-L34-01 三层规程的钩子）

1. 每条（NL 命题, Lean 定理）映射对在 Lean 侧挂三态机读标注块：
   - `-- [L34a: 一致 | 记号等价(附论证指针) | 不符]`（陈述层，六要素对表结论；不符项引双侧行号+逐字摘录，L34 留痕要求）；
   - `-- [L34b: 更强 | 等价 | 更弱 | 不可比]`（强度层四态；CONDITIONAL-PASS 挂下游调用链复核义务指针）；
   - `-- [L34c: <run_id>/<log_sha256>]`（证据层锚；编译证据仅为必要条件，判定句三层可拆读）。
2. 要素级钉桩以 `-- [L34a#量词|函数类|范数|常数|谓词|编号|隐式假设|条件性]: …` 子键承载（L3-4a 八项清单一一对应）。
3. yaml 侧回填：`alignment.statements[].l34` 扩展子键（schema 容忍未知键先例＝federation 块，check-jsonschema 仍通过）；Gap 降级缝落 `status: not-formalized` 显式登记。
4. 标注即 L3-4a 对照表的 Lean 侧承载件：审计档案与标注块同源生成，禁双写漂移。

### 4.4 schema 试金石验证点（T 级字段首次实战清单）

| 验证点 | 字段（SIDECAR-SCHEMA-T0T4-01） | 首次实战内容 |
|---|---|---|
| S1 | T1 `axiom_whitelist`（decl 级） | 现仅包级承载；一期对 C1–C3 新增 decl 逐条白名单审计回填 |
| S2 | T1 `machine_checks[]` 六字段齐套 | Comparator verdict 首跑：tool/tool_version/run_id/verdict/log_sha256/as_of 全字段实测（TB-06 转 T1） |
| S3 | T1 `exclusion_pointers[]` | Gap 环降级缝（若有）的排除指针首跑（同址原则：本体留仓、指针入册） |
| S4 | T2 `dual_kernel` | nanoda 对 1.5k 行构件 dry-run；资源不足则记「未定+理由」（schema §二通用约定允许） |
| S5 | T0 `self_fingerprint_sha256` 回填流程 | 卡6 发放时实测回填流程首跑（禁预填） |
| S6 | `alignment.statements[]` 状态机扩展 | proved/not-formalized + l34 标注子键联合首跑 |

### 4.5 验收钉（版本钉齐）

- **V1 build 绿**：一期构件在 leanprover/lean4:**v4.35.0** + mathlib @**56a005855ea17e0b0958f73ec801ae140b0a1679** 零 sorry 编译通过；公理审计不越白名单（propext/Classical.choice/Quot.sound）。
- **V2 标注覆盖度**：alignment 映射对三态标注覆盖率 **100%**；随机抽查 ≥10% 经 L3-4a 人工复核一致（复核记录入审计档案）。
- **V3 schema 字段回填**：S1–S6 六验证点字段全部实测入 formalization.yaml/注册表新条目；「未定+理由」项 ≤1。
- **V4 spike 回退闸**：spike 验估 ≤2 人周（卡2 先例）；超闸即回判定席复议范围，禁静默扩项。
- **V5 合规钩**：八卡条件清单常设合规钩逐钩核查；对外口径核查（禁领先语）。

### 4.6 人周估算（带依据；散布 ≤1.5 倍，甲席席规；R1 重修版）

**R1 重修说明（判定席 EXT19 R1 令一）**：原版 spike 验估 3–5pd（极比 1.67）与 C4 标注层 3–5pd（极比 1.67）超 ≤1.5 席规线；本版按令拆件分估，spike 拆「Comparator 并轨实测」+「验估报告成文」两子件，C4 拆「标注 schema 落地」+「逐 decl 标注执行」两子件，合计行改如实合计（取消取整收高）。

| 项 | 估算 | 散布极比 | 依据分解 |
|---|---|---|---|
| spike 子件 A · Comparator 并轨实测 | **2–3 pd** | 1.50 | TB-06 暖缓存基线 15–60min 机制已设计（WS44 L3-1），余量为六条信任假设逐条入册 + 基线报告首跑排障 |
| spike 子件 B · 验估报告成文 | **1–1.5 pd** | 1.50 | L0-1 spike 报告成文先例工作量；含 C2 可裁减引理集锁定论证 |
| **spike 验估合计** | **3–4.5 pd（0.6–0.9 pw）**（回退闸 2 pw 维持，见 V4） | 1.50 | A+B 如实相加；L0-1 spike 3–5pd 先例拆件后收窄在案 |
| 一期主体 · C1 Spec 环骨架 | **4 pd（0.8 pw）** | 1.00（点估） | WS44 L4-3「Spec 2–4pd」取上限 |
| 一期主体 · C2 Gap 引理簇 | **3.5–4.5 pw** | ≈1.29 | D01 九项 24–39pw 总量按 3–5/9 引理比例折算，与 L1-3 下端 4pw 互证（未变） |
| 一期主体 · C3 Adapter 环 | **1 pd（0.2 pw）** | 1.00（点估） | WS44 L4-3「Adapter 1pd/30 行级」（未变） |
| 一期主体 · C4a 标注 schema 落地 | **1.5–2 pd** | ≈1.33 | §4.3 三态标注块 + yaml `l34` 扩展子键 schema 首跑；R2 接口漂移风险计入余量 |
| 一期主体 · C4b 逐 decl 标注执行 | **2–3 pd** | 1.50 | 56 decl 存量映射对 + C1–C3 新增 decl 逐条挂标注；与审计档案同源生成（§4.3 条4） |
| 一期主体 · C4 标注层合计 | **3.5–5 pd（0.7–1.0 pw）** | ≈1.43 | C4a+C4b 如实相加 |
| **一期主体合计** | **5.2–6.5 pw** | 1.25 | C1+C2+C3+C4 如实合计：0.8+3.5+0.2+0.7=5.2；0.8+4.5+0.2+1.0=6.5 |
| **合计（spike+一期）** | **5.8–7.4 pw** | ≈1.28 | spike 0.6–0.9pw + 一期 5.2–6.5pw 如实相加（R1 令一：原 6–8pw 系低栏取整收高，本版改如实口径） |

全表逐行极比均 ≤1.50，最大值 1.50（spike 子件 A/B、spike 合计、C4b）；自检逐行复核见 §七。

### 4.7 截止钉（R1 重修版：建议钉转硬，判定席 EXT19 R1 令二）

以下两钉均已转硬：每条采**相对事件钉 + 绝对日期钉双钉并存，以先到者为准**；相对事件钉之「受理」＝判定席 EXT19 受理编号在注册表登记时刻（注册事件，机器可核验）。

- **spike 验估报告截止（硬钉）**：
  - 相对事件钉：判定席 EXT19 受理编号登记时刻 **+ 10 工作日**；
  - 绝对日期钉：**2026-11-04**（UTC(Z)，判定席 EXT19 R1 裁定钉死，R1 裁决令即裁定文书）；
  - 两钉并存，以先到者为准。
- **一期验收（V1–V5 全过）截止（硬钉）**：
  - 相对事件钉：判定席 EXT19 受理编号登记时刻 **+ 40 工作日**；
  - 绝对日期钉：**2026-12-31**（UTC(Z)，判定席 EXT19 R1 裁定钉死）；
  - 两钉并存，以先到者为准；逾期按八卡条件清单常设合规钩触发状态复审。

---

## 五、风险登记

| id | 风险 | 等级 | 缓解 |
|---|---|---|---|
| R1 | **Gap 层深度估爆**：Remark 2.4 kernel 化 WS44 自估散布 4–16pw（4 倍），1.5k 行目标可能不足闭合核心引理簇 | 高 | spike 验估闸先行（卡3 明文分工）；C2 锁 3–5 引理可裁减集；估爆时转 TrustBoundary 降级登记备选轨——**须判定席裁决，禁静默**（WS44 L4-3）；一期范围蔓延按 V4 回退 |
| R2 | **标注规程接口漂移**：L34 三层标注 × 本登记 × yaml schema 三方接口无实战先例，存在「标注写了 schema 不收」风险 | 中 | §4.3 约定先过 WS-G 席会签；S6/V3 为硬验收钉；扩键沿用 schema 容忍未知顶层键先例（federation 块已实证 check-jsonschema 通过） |
| R3 | **anchor_only 证据误升级**：一期 build 绿/Comparator 绿被下游误读为「语义缝已闭合」 | 中 | REJECTED 格纪律（frame §3.4：以编译 rc=0 充内容证据＝越权引用）；L3-4c 训诫「编译通过 ≠ 判定通过」写入一期验收文；Adapter 环放行强制三层全过 |
| R4 | **供应链版本漂移**：LeanCert 论文钉 4.33.0 vs 工具链 v4.35.0 已有漂移先例（WS44 L2-2 注） | 低 | 外部锚一律 commit 40-hex 全钉 + 发放时实测回填（卡6）；漂移检出即开新条目（append-only，旧条目 superseded 保留） |

---

## 六、裁定段（书面裁决登记 · 卡3「登记即落地」执行记录）

1. TrustBoundary 明轨登记**自立案时点生效**：§二 12 条边界、§三三环映射即为本包信任面之在册口径；后续任何等级/来源/归因变更按「裁决先行、登记同步、行文随后」（EXT18 总原则）以新条目追加。
2. kernel 化一期 spike **立案**：范围 §4.2、验收 §4.5、估算 §4.6、截止 §4.7；二期旗舰 v0 后另议。
3. 下游依赖清单登记（卡3 末句）：本登记下游＝kernel 化一期工程卡（依赖 TB-09/TB-06/TB-08 现状钉）、L4-5 旗舰输出（依赖 §4.3 标注约定）、OBL-NS-02 见证窗口（依赖 TB-01/TB-11 关闭路径）、LeanCert 接入评估（依赖 TB-07）。

## 七、合规自检（本文件行文）

本文件为治理登记件，不含新数学断言；不涉及任何「NS 已解决」表述；涉 OpenAI 成果处一律「自评已核、外部复现中、未颁奖」；全部时间戳 UTC(Z) 并带「截至[日期]」钉（卡6）；版本钉：Lean v4.35.0 / mathlib @56a005855ea17e0b0958f73ec801ae140b0a1679 / schema SIDECAR-SCHEMA-T0T4-01 v1 / registry palomar-registry/v1。未定项一处已按「未定+理由」登记（TB-02 elan 对照规程）；§4.7 截止钉已经判定席 EXT19 R1 裁定转硬（相对事件钉+绝对日期钉双钉并存），不再属未定项。Clay NS 未解决、未颁奖。

**估算散布逐行自检（如实口径，判定席 EXT19 R1 令三重修）**：原稿自检句「估算散布最大极比 1.4 ≤1.5」仅在排除两条超线行后成立，系误报，兹改写为逐行实算口径。R1 重修前超线行：spike 验估 3–5pd（极比 1.67，超线）、C4 标注层 3–5pd（极比 1.67，超线）。处置指针：§4.6 按令拆件——spike 拆「Comparator 并轨实测」（子件 A，2–3pd，极比 1.50）+「验估报告成文」（子件 B，1–1.5pd，极比 1.50）；C4 拆「标注 schema 落地」（C4a，1.5–2pd，极比 ≈1.33）+「逐 decl 标注执行」（C4b，2–3pd，极比 1.50）。重修后全表逐行实算：spike 子件 A＝1.50、spike 子件 B＝1.50、spike 合计 3–4.5pd＝1.50、C1＝1.00（点估）、C2 3.5–4.5pw≈1.29、C3＝1.00（点估）、C4a≈1.33、C4b＝1.50、C4 合计 3.5–5pd≈1.43、一期主体合计 5.2–6.5pw＝1.25、总计 5.8–7.4pw≈1.28——**全部 11 行散布极比 ≤1.50，最大值 1.50，符合甲席席规**（极比＝上栏/下栏，同单位实算）。合计行口径：R1 令一落实，取消原「5.3–6.8pw 取整 5–7pw / 6–8pw」低栏取整收高做法，改如实相加（spike 0.6–0.9pw + 一期 5.2–6.5pw = 5.8–7.4pw）。

—— WS-H 攻坚线执行席 · 枢/PIVOT-01 体系 · EXT-WAVE-18「攻」· 2026-10-21
