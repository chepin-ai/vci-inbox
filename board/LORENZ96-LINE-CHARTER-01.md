CLASSIFY: L1
# LORENZ96-LINE-CHARTER-01 — Lorenz-96 批准线（EXT18 卡8a）执行立案书

- 波次/线：EXT-WAVE-18「攻」 WS-J 攻坚线执行席 · 枢/PIVOT-01 体系
- 日期钉：2026-10-21（UTC(Z) 单时钟域；现状类断言均带「截至[日期]」钉，EXT18 卡6）
- 裁决授权：判定席 EXT18 R2 卡8a（2026-10-17，三席 4/4 全准，生效体 2026-10-17T0638Z）
- 上游：NS-SOLUTION-v2_DESIGN_WS44 §三 L1-5 / §八之五 条5（卡8 拆卡）/ 层序修正（丙席）；`board/LAB-CLOSE-EXT15-20261017T0638Z.md`（卡8 拆卡记录）；`registry/TRUSTBOUNDARY-REGISTRY-01.md`（TB-07 见证栈口径、alignment 标注约定参照）；`registry/SIDECAR-SCHEMA-T0T4-01.md`（T0–T4 登记口径）；`board/W-NS-03-REFORGE-CHARTER-01.md`（旗舰示范案例轨立案先例）
- 覆写权纪律：本文件为独立新件，不改动任何既有文件字节；引用既有文件一律带版本钉/行位钉
- 语纪律：C1–C3 + C1′–C3′ 全文有效；OpenAI 相关成果口径固定「自评已核、外部复现中、未颁奖」；严禁「NS 已解决」式表述；本线区间见证语言钉——「区间见证层 PASS、kernel 层未证」（按对象适配）

---

## 一、立案依据

### 1.1 卡8a 原文转录

- EXT18 生效体（WS-44 §八之五 条5，2026-10-17T0638Z）：「**卡8 拆卡：8a Lorenz-96 批准（立案书内成文验收钉：数据集版本+复跑哈希——甲席附钉）；8b 2D IPM 缓议至旗舰 v0 后，先接口 diff 实证复用格数；provenance clean-build 锁死。**」
- LAB-CLOSE-EXT15 §行47 同载：「卡8：拆卡——8a Lorenz-96 批准；8b 2D IPM 缓议至旗舰 v0 后（先接口 diff）。」
- 层序修正（丙席，R2 确认）：「施工序列改为 **L0→L1→L2(旗舰 alignment)∥Lorenz-96 练兵件→L3 接缝重工程按示范案例分批进入**；旗舰优先于定理工程。」
- 设计书定位行（WS-44 §三 L1-5）：「Lorenz-96 训练件｜新造｜与 P1 并行的练兵件（D11 3.0 位）｜小｜产线流程演练报告。」

### 1.2 线定位

本线为 **L2 包络层的平行示范轨**：以 Lorenz-96 低维混沌模型走通「**区间见证 + 捕获区 + 包络声明**」全流程，为 W-NS-03 重铸（NK 时空管 + 捕获区全局化，旗舰示范案例轨）提供**方法论演练场**。三层含义：

1. **方法演练**：见证栈 fail-closed 规程（TB-07：生成器/核验器零共享代码、负控必拒、replay 全哈希链）、CapAnchor 证书声明形态（CapAnchor.lean `capF/capBox/capAnchorStatement`）、LeanCert 复算路径（WS-44 L2-2）在低维对象上先行实跑，误差与摩擦在旗舰轨动用前暴露。
2. **规模可控**：Lorenz-96 为有限维自治 ODE（N 维，标准件 N=36/F=8），无 PDE 接缝、无函数空间层；能量结构初等（§2.2 M1），使全流程可在人日级预算内闭环。
3. **不越位**：本线产物为见证层/登记层制品，不构成任何 PDE、3D 正则性、Fefferman A/B 档位变更；旗舰优先——资源冲突时本线 M 序后延（§四 R3）。

### 1.3 仓内存量盘点（截至 2026-10-21）

`grep -ril lorenz` 命中：board 文档 3 件（LAB-CLOSE-EXT15 / NS-PROOF-FRAME-01 / W-NS-03-REFORGE-CHARTER-01，均为线定位记载）+ mathlib 依赖内零散字符串（与 Lorenz-96 动力学无关）。**无 Lorenz-96 相关 Lean 代码、无见证制品、无登记条目**——本线为纯新造，无存量迁移负担；provenance clean-build 锁死（卡8 生效体）即：本线全部制品自始建账，不继承任何未登记来源的代码/数据。

### 1.4 成文验收钉（甲席附钉，卡8a 要求：数据集版本 + 复跑哈希）

本线任一里程碑记 DONE 的必要条件（不充即退回，甲席席规）：
- **数据集版本钉**：见证数据集以 `LORENZ96-WITNESS-DS-v<n>` 版本号 + 生成脚本 commit 全钉（40-hex）+ 数据集 SHA-256 入册；版本未定时不许出证。
- **复跑哈希钉**：核验器 replay 链（TB-07 同制：生成器/核验器零共享代码）的 run id + 日志 SHA-256 入册；负控必拒记录随件。
- 截至 2026-10-21 上述两钉对象均**未产出——未定+理由：本文件仅立案，执行未启动**；禁预填哈希（TB-12 self_fingerprint 先例）。

---

## 二、范围与里程碑

### 2.0 范围钉

含：Lorenz-96 标准形（单尺度、单参数 F、循环下标）的文献钉定、Lean 表达、区间见证 spike、捕获区（吸收球/捕获盒）包络声明与 T 级登记。不含（明确排除，防范围蔓延，CapAnchor 立案先例）：2D IPM（卡8b 边界，§三.3）、多尺度 Lorenz-96（two-layer/three-layer 变体）、随机参数化、任何 PDE 化推广、周期轨道 CAP（与 RadiiPolynomial 级工作分开记账，W-NS-03 §1.1 同制）。

### 2.1 M0 — 文献与数学定式钉（来源钉）

- **内容**：标准形钉定 ẋ_i = (x_{i+1} − x_{i−2})·x_{i−1} − x_i + F（i mod N，N ≥ 4）；参数区定式：F ≤ 0 收敛族、第一 Hopf 阈值 F_H(l, n)（如 n=36、l=8 时 F_H ≈ 0.8982）、混沌 onset F ∈ (3,7)（n≥5 多数维）、周期窗（n=4：F ≈ 11.83 周期吸引子，F_LPC ≈ 11.8382 鞍结消失）；已知捕获/平衡结论：唯一齐次平衡 x* = F·𝟙，Jacobian 为循环矩阵、特征值解析可得；吸收球先验 d/dt(½‖x‖²) ≤ −‖x‖² + F√N·‖x‖ ⇒ limsup ‖x‖ ≤ F√N。
- **来源钉（一手，禁转引二手）**：Lorenz (1996, Proc. Seminar on Predictability 1:1–18)；van Kekem & Sterk (2018, Physica D 367:38–60, DOI 10.1016/j.physd.2017.11.008)；van Kekem & Sterk (2019, IJBC 29:1950008, DOI 10.1142/S0218127419500081)；Sterk & van Kekem (2017, Complexity 9419024, DOI 10.1155/2017/9419024)；Karimi & Paul (2010, Chaos 20:043105)。以上 DOI/数值阈为检索转录，**M0 执行时须逐条一手复核**——未复核条目登记为「未定+理由」。
- **交付定义**：定式表一件（未来新件 `board/LORENZ96-MATHFIX-01.md`），每结论带要素级来源钉 + 复核状态机（transcribed/verified/failed），过 L3-4a 要素对照抽样。
- **人周估算**：2–3 pd（散布 1.5×，合规）。依据：模板一手精读先例 D02 约 1 pd（W-NS-03 立案引），本件 5 源 + 数值阈复核 + 定式表成文。
- **版本钉**：文献 DOI/arXiv 钉如上；登记体例 SIDECAR-SCHEMA-T0T4-01（registry 现行版）。
- **截止钉**：2026-10-28。

### 2.2 M1 — ODE 模型 Lean 表达（取舍分析在案）

**对象事实**（M0 复核后锁定）：Lorenz-96 非线性项满足**对角相消** Σ_i x_i(x_{i+1}−x_{i−2})x_{i−1} = 0（循环重指标恒等式），故 `⟪B x x, x⟫ = 0` 成立；但**全称斜对称** `⟪B u v, w⟫ = −⟪B u w, v⟫` 一般不成立（取 u≠x 时循环和非零），即 Lorenz-96 落在 `GalerkinNS.hskew` 对角假设层、**不落在** `SkewNonlinearity` 全斜对称层（SkewB.lean L69）。

| 选项 | 内容 | 利 | 弊 |
|---|---|---|---|
| A · 复用 `GalerkinNS` 实例化 | E = `EuclideanSpace ℝ (Fin N)`，A = 恒等连续线性映射（阻尼 −x_i），ν 槽位填 1，B = 循环双线性形，f = F·𝟙 | 直接继承 Existence/Uniqueness/能量不等式（Basic.lean `inner_vf_le` L73 等 56 decl 存量）；零新证存在性；CapAnchor 同族邻接 | 语义重映射（ν 槽位=阻尼系数 1）须 alignment 标注显式化；全斜对称不适用须在侧车声明 |
| B · 独立轻结构 `Lorenz96` | 显式向量场 + 自证 Cauchy–Lipschitz | 无语义错位；教学洁净 | 存在唯一性/能量球重证 ~200–400 行重复劳动；脱离 CapAnchor 邻接，演练价值降 |
| **裁定：A 为主 + B 为壳** | 数学内容走 A（实例化继承）；`Lorenz96` 命名空间作显式定义壳（cyclic 索引、vf 定义、diag 恒等式证明），与 `GalerkinNS` 实例的接缝以 alignment 标注（TRUSTBOUNDARY §4.3 约定）显式登记 | 两者之长 | 接缝标注成本 ~0.5 pd，已计入估算 |

- **交付定义**：`Lorenz96` 壳模块 + `GalerkinNS` 实例化 + 对角恒等式 `inner_Bxx_eq_zero` 编译零 sorry；hskew 满足、SkewNonlinearity 不实例化的原因注记入侧车；公理审计维持白名单（propext/Classical.choice/Quot.sound）。
- **人周估算**：3–4 pd（散布 1.33×，合规）。依据：M1-1 斜对称封装先例 1–2 pd（WS-44 L1-1）+ 显式循环双线性形构造与实例化摩擦实报。
- **版本钉**：`leanprover/lean4:v4.35.0`（lean-toolchain 现钉）；mathlib @ `56a005855ea17e0b0958f73ec801ae140b0a1679`（lake-manifest 现钉，TB-03）。
- **截止钉**：2026-11-11。

### 2.3 M2 — 区间见证 spike（CapAnchor/LeanCert 复用面）

- **内容**：双证制 spike——(a) **平衡态证书**：对 x* = F·𝟙 以 Krawczyk/Moore 区间算子出存在唯一性证书（Jacobian 循环矩阵解析谱作负控参照；此件低风险先行）；(b) **捕获盒见证**：对 (N=36, F=8) 数值轨道给出候选盒，区间验证向量场在盒面严格内指（trapping）——声明层级为**区间见证层 PASS、kernel 层未证**，不许外推为吸引子刻画或轨道包络。
- **复用面**：证书声明形态复用 CapAnchor.lean（`CapParams/capLin/capF/capBox/capAnchorStatement`，P1 先例 center ![0.6, 0.8, -0.25] / r 0.0474531328121258）；见证栈复用 witness_ns_gen/verify.py 制（python 3.12 + mpmath 1.3.0 + numpy + scipy 1.16，TB-07）；kernel 侧复算路径 = LeanCert（WS-44 L2-2，注意论文钉 4.33.0 版本漂移、接入以 v4.35.0 释出版为准）。
- **交付定义**：证书 JSON 两件 + 负控必拒记录 + replay 复跑哈希（§1.4 钉）；LeanCert 复算一致或不一致实报（不一致即 FINDING 立案，禁静默）。
- **人周估算**：4–5 pd（散布 1.25×，合规）。依据：LeanCert 接入估 2–4 pd（WS-44 L2-2）+ 见证栈存量零新造成本（TB-07）− spike 范围裁减（仅平衡态 + 单盒）。
- **版本钉**：见证栈钉如上（TB-07 行位钉）；LeanCert 版本钉 **默认钉 `v4.35.0 @ d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e`**（WS-I 2026-10-21 官源实测）；启动窗若已释出更新则按 append-only 新条目重钉并登记漂移。
- **截止钉**：2026-11-25。

### 2.4 M3 — 包络声明与登记（schema T 级）

- **内容**：出具本线包络声明：「吸收球 limsup‖x‖ ≤ F√N（解析先验，kernel 层）+ 捕获盒 trapping（区间见证层）」的合取式分层声明——每层证据形态分别记账，**合取不升格任一层级**；按 SIDECAR-SCHEMA-T0T4-01 登记：声明文本 T0 自述 + 编译/见证记录 T1 机器佐证，目标条目 T1（T2 注册表见证留待旗舰注册表窗口，不本线自封）。
- **交付定义**：sidecar 条目一件（T0/T1 字段齐套、self_fingerprint 实测回填、append-only 追加）+ 产线流程演练报告（WS-44 L1-5 验收钉）——报告须含与 W-NS-03 案例轨的规程 diff（§三.1）。
- **人周估算**：2–3 pd（散布 1.5×，合规）。依据：PAL-0001 首条登记 3–5 pd（WS-44 L4-4），本件范围裁至单条目 + 报告，取下端。
- **版本钉**：schema 钉 SIDECAR-SCHEMA-T0T4-01（registry 现行版）；登记目标仓 = palomar-registry-v1.yaml 追加条目（不改 PAL-0001/0002）。
- **截止钉**：2026-12-09。

---

## 三、与 W-NS-03 的接口与卡8b 边界

### 3.1 回流旗舰线的产物/规程（演练场职责）

1. **区间见证 SOP 实跑沉淀**：fail-closed / 零共享代码 / replay 哈希链在 Lorenz-96 上的端到端执行记录 → 回流为 W-NS-03 Gate 0-3（Julia 栈钉定与 NK 证书生成规程）的操作模板与摩擦清单。
2. **捕获区论证模板预演**：能量先验（吸收球）→ 候选盒 → 区间 trapping 验证的论证链，与 W-NS-03 捕获区全局化段（Cadiot–Lessard Lemma 4.2 / Cor 4.3 模板）同构 → 回流论证链检查表。
3. **CapAnchor 第二实例**：证书声明形态从 P1 单例到 Lorenz-96 第二例的泛化反馈 → 回流 L2-2 LeanCert 接入的接口设计（哪些字段应泛化出 `CapParams`）。
4. **schema 第二试件**：sidecar 条目第二实例 → 回流 T 级字段表的压力测试记录（W-NS-03 案例轨为 schema 试金石第一例，本线为平行第二例，互为对照）。

### 3.2 接口纪律

本线不阻塞 W-NS-03 Gate 0 任何条款；两线共享见证栈时 W-NS-03 窗口优先（旗舰优先，丙席层序）。两线制品分开记账：Lorenz-96 见证结论不写入 NS 包 alignment 表，不升格 NS 任何档位（§九 合规自检同制）。

### 3.3 与卡8b（2D IPM 缓议）的边界

本线**不做 IPM**：不立项、不预研、不做接口 diff——2D IPM 缓议至旗舰 v0 后，届时先接口 diff 实证复用格数（卡8b 生效体原文）。Lorenz-96 为有限维 ODE，与 P1 IPM 谱截断无共享代码路径；凡以本线名义出现的 IPM 相关制品一律退回（防范围误读，formalization.yaml §3.3 条先例）。

---

## 四、风险簿（带缓解）

| # | 风险 | 等级 | 缓解 |
|---|---|---|---|
| R1 | **全斜对称误判**：Lorenz-96 非线性仅对角相消（hskew 层），不具全称斜对称；若误按 `SkewNonlinearity` 实例化则编译受阻且返工 | 中 | M1 裁定「A 为主+B 为壳」明确只用 hskew 对角层；首件任务单 T2 先行独立验证循环和恒等式，失败即暴露于 spike 阶段、不进主线；侧车显式声明 SkewNonlinearity 不实例化及原因 |
| R2 | **见证语义越界**：trapping 盒见证被（内/外部）误读为吸引子刻画、轨道包络或混沌存在的证明 | 高 | 语言钉「区间见证层 PASS、kernel 层未证」随每件证书不可剥离；M3 声明采分层合取式、合取不升格；登记文本过 L3-4 三层审计逐句 diff（W-NS-03 卡1 同制：终稿 diff 实做）；周期窗/混沌结论一律引文献钉、不自证 |
| R3 | **旗舰资源争用**：层序「旗舰优先于定理工程」，本线与 W-NS-03/L4 窗口冲突 | 中 | 本线为平行练兵件，工时行项单列（甲席附钉先例）；冲突时本线 M 序整体后延不抢占；截止钉允许经判定席顺移一次（顺移须书面裁决+登记，乙席总原则） |
| R4 | **来源转录失配**：文献数值阈（F_H、周期窗等）二手转录错误（SCI=∞ 训诫：编译绿 ≠ 判定过） | 中 | M0 一手复核为交付定义组成部分；未复核条目记「未定+理由」禁入定式表；L3-4a 要素对照抽样复核；DOI/arXiv 全钉禁裸引 |
| R5 | **LeanCert 版本漂移**：论文钉 4.33.0 与 v4.35.0 释出版的接口差（WS-44 L2-2 已注） | 低 | M2 启动窗以当窗释出版全钉入册；复算不一致即 FINDING 立案禁静默；LeanCert 不可用时降级为见证层单证 + 缺口登记（TB-06 同制） |

---

## 五、首件可执行任务单（3 件，每件 ≤ 2 pd，带验收钉）

| # | 任务 | 预算 | 验收钉（版本钉 + 截止钉） |
|---|---|---|---|
| T1 | **文献定式表 v0**：Lorenz (1996) + van Kekem & Sterk 2018/2019 + Sterk & van Kekem 2017 + Karimi & Paul 2010 五源一手复核；标准形/F 参数区/F_H 阈/周期窗/吸收球先验逐条来源钉；未复核条记「未定+理由」 | 2 pd | 交付 `board/LORENZ96-MATHFIX-01.md`（未来新件）；五源 DOI/arXiv 全钉、每结论复核状态机齐；过 L3-4a 要素对照抽样 ≥3 条；截止 2026-10-28 |
| T2 | **循环和恒等式 Lean spike**：`Lorenz96` 壳命名空间内构造循环双线性形 B 并证 `inner_Bxx_eq_zero : ⟪B x x, x⟫_ℝ = 0`（Fin N 循环重指标），同件负面试证 SkewNonlinearity 全条件不可实例化（反例或 sorry-free 注记） | 2 pd | `leanprover/lean4:v4.35.0` + mathlib @56a005855ea17e0b0958f73ec801ae140b0a1679 下编译绿、sorry-scan = 0、公理白名单内；CI run id + 日志 SHA-256 随件；截止 2026-11-04 |
| T3 | **平衡态区间证书 spike**：对 x* = F·𝟙（N=36、F=8）以 Krawczyk 算子出存在唯一性证书（witness 栈：python 3.12 + mpmath 1.3.0 + numpy + scipy 1.16，TB-07 同制），负控（扰动盒外点）必拒 | 2 pd | 证书 JSON + 生成/核验零共享代码说明 + replay 复跑哈希 + 负控拒收记录齐（§1.4 双钉首件落地）；声明带语言钉「区间见证层 PASS、kernel 层未证」；截止 2026-11-04 |

---

## 六、合规自检（本文件行文）

本线为 Lorenz-96（有限维 ODE）批准线之**立案**，截至 2026-10-21 未产出任何代码/见证/登记制品；凡未产出的钉（数据集版本、复跑哈希）均标「未定+理由」未预填；LeanCert 版本钉已于 §2.3 落全钉（v4.35.0 @ d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e）。本文件不改变 NS 包任何档位：NS 截断层 9 文件 56 decl 零 sorry 存量口径不动，PDE 接缝/3D 正则性/Leray–Hopf 唯一性/Fefferman A B 各项 BLOCKED(B1) 登记不动，Clay NS **未解决、未颁奖**；OpenAI 相关成果口径「自评已核、外部复现中、未颁奖」；区间见证语言钉「区间见证层 PASS、kernel 层未证」已按对象适配至本线全部见证声明。一切等级/来源/归因/语态变更遵循「裁决先行、登记同步、行文随后」（乙席总原则）。

## §2.3-ERRATA-01（append-only 勘误，依 LORENZ96-M2-ROUTE-RULING-01 授权）

**§2.3-ERRATA-01（append-only 勘误，2026-10-22，依 LORENZ96-M2-ROUTE-RULING-01 §三授权追加；上文本节各行原文保留、语义以本段为准）**

1. **M2(b) 对象变更**：原「捕获盒见证」件经 `research/lorenz96_m2b_trapping_01.md` 决定性否定（轴对齐盒对 (N=36, F=8) 结构性不适用：72/72 面外指违例、400×400 均匀盒扫描可行对数=0），**降格为已闭合否定发现存档**；M2(b) 替换为**分层捕获声明**：(b-i) **吸收球 trapping**（R = √N|F| = 48，S2 Prop 7 一手钉；解析真，kernel 可 Lean 化——`inner_cyclicB_self` 对角相消与 GalerkinNS 能量不等式供给件在案），目标出 kernel 层 Lean 证明 + 区间见证层正控证书；(b-ii) **逐坐标数值包络**（双初值数值轨道包络 + margin 规则如实登记），声明层级**区间见证层、不主张 kernel**。
2. **语言钉适配**：(b-i) 吸收球 Lean 证明达成前携带「kernel 层未证」，达成后按实改记「kernel 层已证（定理钉+公理审计）」；(b-ii) 数值包络**恒**携带「区间见证层 PASS 或候选、kernel 层未证」，**禁**外推为吸引子刻画或轨道包络（§四 R2 不变、不加宽）。
3. **交付定义更新**：M2 交付 = (a) 平衡态证书（已达成，LORENZ96-M0-T3-KRAWCZYK-01）+ (b-i) 吸收球 trapping 证明与正控证书 + (b-ii) 数值包络见证件 + 负控必拒记录 + replay 复跑哈希（§1.4 双钉不变）+ Jacobian 谱负控参照（原 (a) 内既有要求，续行）。
4. **挂账状态**：G3（拓扑替代路线）经本裁决 CLOSED；G4（章程回注）以本段追加为 CLOSED 的执行动作；G1/G2（严格区间证书+replay 哈希、浮点舍入控制）**不销账**，对象改以新拓扑（球面正控 + 包络层）承接，仍禁预填哈希。
5. **风险簿追加（append-only）**：R6｜**轴对齐盒拓扑风险实报**：轴对齐捕获盒对强混沌 Lorenz-96 结构性不适用（量程~26 vs 盒宽≲1）——教训：捕获集拓扑选择须先验核对系统的正交/耗散结构所在方向（径向 vs 面法向）；等级：已实报闭合；缓解：本勘误 §2.3-ERRATA-01 条1 分层路线。

- 执行 commit 哈希回填：**53494f1f3**（§2.3-ERRATA-01 append-only 追加执行笔，2026-10-22 落仓）
