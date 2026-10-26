CLASSIFY: L1
# KERNEL-PARANOID-EVAL-01 · QF-OS 联邦批二十五 K-PAR kernel 换装评估席 · Lean v4.35.0 官方 `lake check --paranoid` 多内核流水线接入评估

- 席别：QF-OS 联邦批二十五 K-PAR kernel 换装评估席（评估件，只写文，零 git 操作，不作终裁；换装与否属判定席权限）
- 成文日期钉：**2026-10-26**（UTC(Z) 单时钟域；外部来源时点逐条标注）
- 口径纪律（全件适用，逐字）：涉 NS 表述一律限「**有限维 ODE 截断层**」语境，全件无「NS 已解决」方向表述，Tenet 包状态沿唯一批准语「自评已核、外部复现中、未颁奖」；涉 ζ 表述一律限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」，全件严禁且无「RH 已证/已验证到 T」字样；OpenAI NS 主张与 Hou–Wang–Yang（arXiv:2509.25116）均按「评审中/待评审预印本，结论未确立」登记。
- 名值分离：工具名、PR 号、出口码、数值与其出处分行/分句；「Tenet」一名两义强制区分——**Tenet-repo**＝联邦对 github.com/openai/NavierStokesAndEuler（钉 f9e8bc5，toolchain v4.34.0-rc2）之代号（OBL-NS-02-TENET-RERUN-01/02 在案）；**Tenet.Kernel**＝C#/.NET 独立内核检查器（NuGet 生态，MONITOR-FRONTIER-20261025-01 §六在案）——本件凡「Tenet」未修饰处皆指 Tenet-repo；Tenet.Kernel **不在**官方捆绑清单内。
- 不编数：全部数值引在案文件钉或当次外部来源；本席不新产工时/产能估计（甲席席规），窗钉一律引用既有裁决窗或绝对日期。
- 本地实测如实登记：本席作业环境 `which lean/lake/elan` 三命令全部 not found，`~/.elan` 不存在——**本件一切工具行为断言来自官方发布注记/参考手册/de Moura 博客与在案件，未经本机实测**；凡须实测项已在 §5 验收判据与 §6 风险中显式列出。
- 只读纪律：/mnt/agents/output/vci-inbox 全程只读、零 git；本件为唯一新建件。

---

## 〇、一句话结论

官方 `lake check --paranoid` 流水线**可承接联邦 kernel 层「验证编排」换装**（含 R2B-09 四锚第二通道义务的提前超额兑现与 Tenet 线 A5 双内核空位替补），ζ 线 BLOCKED(B1) 的**环境分量**可由此解除；但它**不产生任何证明内容**——ζ 区间见证层数学未 Lean 化、Tenet 30h 全量构建是导出前提，两者均不在工具换装可达域内（详见 §3/§4）。

---

## 一、官方流水线能力边界核实（来源逐钉）

来源基座：Lean v4.35.0 发布注记（lean-lang.org/doc/reference/latest/releases/v4.35.0/，2026-10-12，本席 2026-10-26 全文核读）；Lake 参考手册 25.1.5.8 节（检索于 2026-10-26）；de Moura 博客两篇（2026-08-24 postmortem、2026-10-15「Lean Now Ships with Verified Kernels」）；在案转录 board/FRONTIER-SCAN-20261026-02.md §1.1。

### 1.1 内核清单（名值分离：「捆绑」与「--paranoid 实跑」两名单存在文档级微差，如实双写）

- **捆绑入发布工具链**（发布注记 Highlights 段）：`lean4lean`（#15048）、`nanoda`（#15099）、`con-leche`（#15130）、`con-ron`（#15153）、`leanchecker-paranoid`（加固内存分配器版 leanchecker，#14884；mimalloc 化 #14982 同版落地）。外部一手实测旁证：v4.35.0-rc3 工具链 bin/ 实测含 `lean4lean`（30MB）、`nanoda_bin`（1.2MB）、`leanexport`（571kB）、`leanchecker`、`leanchecker-paranoid`、`con-leche`、`con-ron`（solveathome.org kk-lower-bound #2597 复跑件，2026-10-17/18，「What the toolchain ships」段）。
- **`--paranoid` 实跑集**：发布注记 Highlights 段文字为「run **all of these** checkers in addition to Lean's own kernel」（即含 con-ron）；而同页 #15145 变更行括号枚举为「`leanchecker-paranoid`, `lean4lean`, `nanoda` and `con-leche`」（**未列 con-ron**）。两处官方文本不一致——**con-ron 是否入 paranoid 实跑集须试点实测以 `lake check --paranoid` 实际日志为准**（列入 §5 验收判据 A-4）。
- 各内核性质（外部来源，逐钉）：nanoda＝Rust 独立实现（Bailey 2026，MONITOR-FRONTIER §六在案）；lean4lean＝Lean 实现（TYPES 2025，A1-STACK-UPGRADE-DRAFT-01 在案「已抓 1 个内核 soundness bug」）；con-leche＝首个以 Lean 编写并在 Lean 内证一致性的内核（其实现与一致性证明由 Claude 完成、Lean FRO Joachim Breitner 重度监督；全 mathlib 导出约 100 秒/8 线程——shengyayun 2026-10-19 转述其 README，二手来源，标中可信度）；con-ron＝con-leche 经 AI 译为 Rust 并以 Aeneas 证 refinement（同前二手来源）；leanchecker-paranoid＝官方内核的加固分配器变体，把内存腐化转为受检中止而非静默错答（de Moura 2026-10-15 博客）。
- **公理闸**：`lake check` 报告被检代码所用公理，**任一非标准公理即失败**（#14990；手册：exit 1 情形之一）。同版 #14953 移除 `Lean.reduceBool/reduceNat/ofReduceBool/ofReduceNat/trustCompiler`——全环境公理检查因此更有鉴别力（发布注记原文逻辑）；含 `native_decide` 的工件在本版公理报告形态本席无实测，列为试点观察项（§6 R-7）。

### 1.2 `--from-export` 语义（#15157/#15050，手册 25.1.5.8 逐字级转写）

- `lake check --from-export=FILE`、`lake comparator --solution-from-export/--challenge-from-export=FILE`、`leanchecker --from-export file.ndjson`：直接检验**既有 leanexport NDJSON 导出件**，跳过构建与再导出；此形态**不需要项目 manifest**。
- 官方列明三用途（#15157 原文义项）：VM 内产出的导出（额外隔离）；第三方产出的导出（如需巨量算力者）；非标准 `lake build` 途径产出的导出。
- **证据边界（手册原文）**：--from-export「establishes only that the checkers accept the export, and **says nothing about the project in the workspace**」——导出件的来源锚定（sha256＋构建日志＋钉）属消费方责任，恰与联邦既有 manifest/sha256 纪律（OBL-NS-02-TENET-RERUN-02 §一 40 样本抽查先例）同构可接。
- 出口码契约（手册）：`lake check` —— **0**＝全部内核接受且仅用标准公理；**1**＝某内核拒绝／用了非标准公理／构建失败；**2**＝检查根本无法运行。`lake comparator` —— 0＝accepted／1＝rejected／2＝无法裁决。此契约即 R2B-02 退出码契约化体例（FSL v59 在案）的官方同构，W2-P0-09 必修项②「exit-code 承载 verdict」现成有据。
- NDJSON 读取器已加固（#15542：拒绝行尾赘字节、重复键、重复绑定索引——此前静默接受）。

### 1.3 对既有 .olean／导出件的输入要求与隔离姿态

- 默认形态：`lake check` 构建**根包 default targets** → 导出 → 内核回放（#14990），要求项目有 manifest；构建与导出在 **bubblewrap 沙箱**内进行（隐藏用户 home、仅依赖解析放行网络，#15005；内核另跑在特权分离进程，#15055）；**沙箱仅 Linux**；`--inadvisably-no-sandbox` 可关沙箱但手册明示「仅自备隔离手段的专家用户」可用——联邦正式跑批**禁用**该旗标（若执行席环境无 bubblewrap，须登记降级形态，见 §6 R-1）。
- **.olean 直读不是本流水线输入面**：官方流水线以 NDJSON 导出为中心；外部一手实测旁证——捆绑 lean4lean 的 olean 模式对所链 Lean commit 之外的 olean 头**拒读**（incompatible header，solveathome 件 logs/13），上游 master 亦不能对 v4.35.0-rc3 构建（Nat.div primitive）——**结论：喂 .olean 的路线不可依，一律走 leanexport NDJSON**。（对照：Tenet.Kernel 直读 .olean 但不在捆绑集。）
- 导出形态与体量参照（外部一手实测，机位 Apple M3 Ultra/96GB，solveathome 件）：三目标闭包导出 22,948 条声明记录/123,032,181 B（两次导出字节全等）；nanoda 0.4.17 检 24,273 声明 13.9s exit 0；lean4lean 检 22,945 声明 34.3s exit 0；**全环境**导出（含 mathlib，407,077 记录/2.41GB）lean4lean 989s accept，**nanoda 2 小时未完、常驻 36.6GB 被终止**——全环境规模下 nanoda 在联邦 2 核/4GB 机位上结构性不可行（在案机位钉：OBL-NS-02-TENET-RERUN-02 §一「2 核/4GB/无 root」）。
- `lake comparator` 配置：`comparator.json` 为默认配置位（#15147），schema 含 challenge_module/solution_module/theorem_names/permitted_axioms——与联邦 Palomar 模板（GO-SUBMISSION-20261031-01 系 Challenge.lean/Solution.lean/comparator.json 双件结构，FRONTIER-SCAN §3.2 在案）**格式天然对齐**。

---

## 二、与联邦既有自组编排的对拍表

联邦现行/在途 kernel 层编排（全部在案）：①L34′ 自建探针 `#print axioms`（`lake env lean` 动态探针＋人工白名单对拍；OBL-NS-02-TENET-RERUN-02 §二 8/8、L34-FGL-SAMPLING-02 §三 G4 重编译后自建探针独立复核先例）；②W11/S2 草案 comparator CI 通道（GHA yaml，`lake comparator` 步，返修中——W2-P0-09 九项必修，预飞闸 2026-11-03）；③A1-STACK 五级检查栈规划（L1 lean4checker／L2 Lean4Lean 需公共 runner 备导出链，「环境未备时记 BLOCKED」原文在案；L3 comparator／L4 SafeVerify 未缔约）；④R2B-09 已裁义务（四锚补 nanoda 或 lean4checker 第二通道重放，窗 2026-11-15，ADJUD-WILDQ-R1-HARVEST-01 在案）。

| 维度 | 联邦自组编排（①–④） | 官方 `lake check [--paranoid]` 流水线 |
|---|---|---|
| **功能** | ①仅公理集列举（单 Lean kernel 通道，无独立内核回放）；②陈述对拍（challenge↔solution）在草案、未实证调用面（ADJUD-WILDQ2-HARVEST-01 §8 在案）；③多级回放停留在规划；④第二通道义务未执行 | 构建＋导出＋**多内核回放**＋公理闸＋沙箱隔离单命令成流；`--paranoid` 全捆绑内核全接受方 PASS；comparator 模式带 theorem_names/permitted_axioms 配置化陈述锚 |
| **成本**（只引实测/在案钉，定性分级） | ①秒级探针＋模块定向构建（在案：2434 jobs/42s、2613 jobs/18s）；③L1/L2 环境备置成本即 B1 挂账本体；④「小件重放，分钟级构建」（收割件 R2B-09 行原文） | 工具链**自带零备置**（联邦主线已钉 v4.35.0，U17-KERNEL-PROBE-01 §1 在案——消除③的 BLOCKED 分量）；回放成本：闭包规模秒–分级（外部钉：22,948 记录→nanoda 13.9s/lean4lean 34.3s，M3 Ultra）；全环境规模 lean4lean 989s、**nanoda 不可行**（2h/36.6GB DNF）——联邦机位只承载闭包级 |
| **证据强度** | ①公理集证据仅证「未用白名单外公理」；**内核实现 bug 对 #print axioms 不可见**——2026-07 嵌套归纳伪造证明实例：官方内核＋leanchecker＋Nanoda 全接受且报零公理（oss-sec 2026-08-02 披露件，#14576/#14577） | ≥4 个独立实现（Rust/Lean/Lean 内证一致性/加固分配器变体）实现多样性证据；覆盖「实现写错」bug 类（con-leche 一致性证明针对此类）；**仍不覆盖共享规格缝隙**（§6 R-4） |
| **审计性** | ①探针源＋输出 txt 落盘（可审计但格式自造）；②日志 grep 取 verdict 曾被裁伪绿通道（ADJUD-WILDQ2-HARVEST-01 §1/§2 成立在案）；退出码闸缺位 | 文档化出口码 0/1/2（手册）；导出件单文件可 sha256 钉源；--from-export 实现**生产侧/检验侧机位分离**（与案 C「非执行席独立重演」立规、WS-37 零共享代码纪律同构）；`--paranoid` 逐内核日志可归档 |

对拍结论：①的功能被 `lake check` 的公理报告＋非标准公理即败**完全覆盖且加强**；②的陈述对拍由 `lake comparator --paranoid` 承接，且其返修必修项②⑦（退出码承载、调用面实证）因官方手册出口码契约落地而**有据可依**；③④的环境前置被「工具链自带」结构性消除。

---

## 三、ζ 线 kernel 层 BLOCKED(B1) 解锁可行性评估

（口径钉：本节一切涉 ζ 表述限「有限高度 T=100/1000 截断」语境；见证链状态钉逐字「区间见证层 PASS、kernel 层未证、非 RH 证据」，本节评估不改变该钉。）

**BLOCKED(B1) 的语义分解**（名值分离）：ZETA-INST-01 §Lean 诚锚「kernel 层 W2 预审： BLOCKED(B1) 明码」＋A1-STACK-UPGRADE-DRAFT-01「环境未备（公共 runner 无 lean4checker 导出链）时记 BLOCKED」在案——B1 系基础设施席代号，该 BLOCKED 的**直接分量是「独立内核验证环境未备置」**，而非「证明已写出待重放」。

**可解锁的分量（评估：可行，且在现有钉内零工具链变更）**：
1. 联邦主线已钉 lean v4.35.0＋mathlib v4.35.0（U17-KERNEL-PROBE-01 §1：toolchain tarball sha256 在案、cache 9031/9031/110s；B1-INFRA-20261025-01 §3.1「与最新稳定持平」）——**捆绑内核随既有钉在位，备置成本为零**，B1 环境分量结构性解除。
2. 锚件可检性在案：ZetaAnchor.lean 源码级独立 elaboration RC=0/72s，四锚公理集恰为 [propext, Classical.choice, Quot.sound] 标准三公理（U17-KERNEL-PROBE-01 §3/§4）——与 `lake check` 公理闸相容。
3. R2B-09 义务（四锚 nanoda 或 lean4checker 第二通道，窗 2026-11-15）可由一次 `lake check --paranoid`（或闭包导出＋`--from-export`）**超额兑现**——义务要求 1 个第二通道，流水线给 ≥4 通道。

**不可解锁的分量（如实登记，不夸大）**：
1. **「区间见证层的定理集」目前不存在可导出形态**——见证层数学（IVT 括号、RS 余项、区间包络）实现于 Python/mpmath.iv 侧（ZETA-INST-01 §零共享代码、witness JSON 在案），Lean 侧仅有 Prop 级陈述锚（statement-only，U17-KERNEL-PROBE-01 §5.3 逐字）。paranoid 流水线只能核「喂给它的 Lean 导出」；**对尚未 Lean 化的见证数学无可核之物**。即：换装解「验证编排」，不解「证明内容」。
2. 锚集 paranoid accept 后，证据升格仅限「锚陈述的多内核接受」；ζ 状态钉「区间见证层 PASS、kernel 层未证、非 RH 证据」**不变**——kernel 层「已证」须待见证数学（余项界、区间算术证书）实际 Lean 化并经内核接受后方有议处资格，路线参照在案（FRONTIER-SCAN §3.1 RSInt.rs_Z_C0' 模式：Arb 128-bit ball＋RS 余项定理 Lean 化分层）。
3. 耦合面警示（WILDQ3-ZETA 问九在案）：锚居 library/ns 包内，`lake check` 默认构建根包 default targets＝NS 包全量——**建议以 leanexport 目标闭包导出（锚四件＋其依赖闭包）喂 `--from-export`** 限定作业面，避免 NS 包线故障（W-NS-03 重铸等在途）波及 ζ 侧检验节奏；闭包导出形态与 `--from-export` 的相容性列试点实测项（§5 A-3）。

---

## 四、NS 线 Tenet/OBL 挂账的替代路径影响

（口径钉：Tenet-repo 状态「自评已核、外部复现中、未颁奖」；一切涉 NS 表述限「有限维 ODE 截断层」语境。）

挂账现状（在案逐钉）：OBL-NS-02＝Tenet-repo 钉 f9e8bc5 全量 2659 模块构建复现——2 核吞吐 ~1.4 模块/分、ETA ≈30h，「结构性不可闭合（ETA 30h ≫ 窗口）」正式结论在案（OBL-NS-02-TENET-RERUN-02 §三）；案 E（ADJUD-R2B §五）延期，候 W2-P2-01 闭包级审计实验，定谳庭＝11-15 双硬钉后首个庭期且不迟于 2026-12-05，裁项 (a)＝「基线声明闭包级全定理公理审计＋残余未建模块声明式登记」替代全量构建、(b)＝无限期挂账；A5 双 kernel **未启动**（RERUN-02 §三末行在案）。OBL-NS-01＝接缝件①②数学路线移植（内容层长程义务）；OBL-NS-03＝RadiiPolynomial Fourier 系数代数扩展评估（内容层中程义务）（FUSION-EXT10-01 §6 在案）。

**评估结论：30h 全量构建不可被换装消除，但挂账的「验证分量」可闭包级部分换装。**

1. **不可换装部分**：导出以构建为前提——`--from-export` 只免去检验侧的构建，不免去生产侧；2659 模块全量导出本身即需全量构建产物（外部参照：OpenAI 官方包全导出 1.5GB/28.6M 行，Arena 复跑 lean4lean 9.5min/lazylean 2.0min 在其机位，FRONTIER-SCAN §2.1 在案；nanoda 对 mathlib 级导出在 96GB 机位 2h DNF——联邦 2 核/4GB 无全量回放承载力）。**30h 构建义务本身不受本流水线影响**。
2. **可换装部分（与案 E 裁项 (a) 同构）**：基线 8 声明闭包（在案实测构建 2434 jobs/42s＋2613 jobs/18s）→ leanexport 闭包导出 → `lake check --paranoid --from-export`——把现行「单内核 `#print axioms` 探针＋人工白名单」的 A3 公理审计升格为「**多内核 accept＋机器公理闸**」，且 A5 双内核空位由捆绑内核替补（无需另启工程）。此为案 E 裁项 (a) 的**现成官方实现**，供 11-15 后定谳庭采择；本席不预判裁决。
3. **工具链错配钉（名值分离）**：Tenet-repo 钉 v4.34.0-rc2，捆绑流水线属 v4.35.0 工具链——**导出须由被检方自有钉的工具链产出**（跨版 leanexport 格式相容性无在案实证，外部先例显示导出器须按目标 toolchain 调钉构建，arXiv:2605.19063 附录做法），检验侧用 v4.35.0 `--from-export` 消费；该跨版相容性列试点前置实测项（§6 R-3）。迁 Tenet-repo 至 v4.35.x 属中风险（B1-INFRA §3.3 在案：4.32 起 breaking 累计），本评估**不建议**为换装而迁钉。
4. OBL-NS-01/03 为证明内容层义务，kernel 换装对其**无直接作用**（工具不解数学缺口），如实登记零影响。

---

## 五、试点建议（最小试点面、验收判据、窗）

**最小试点面**：library/ns 包内 **ζ 四锚闭包**（zetaIsolationAnchor／zetaUniqueZeroAnchor／zetaAnchorImpliesRHCriticalLine＋capAnchorP1，行号钉 U17-KERNEL-PROBE-01 §2）——理由：①既有钉 v4.35.0 零迁移；②构建面在案可复现（cache 9031/9031/110s、锚件独立 elaboration 72s）；③闭包规模远小于全环境，2 核/4GB 承载概率最高；④直接兑现 R2B-09 已裁义务（不新增义务线）；⑤Prop 级陈述锚公理集在案为标准三公理，公理闸预期不触红。

**建议形态**：`lake env leanexport NsGalerkin.ZetaAnchor -- <四锚>` 产 NDJSON 闭包导出（sha256 落盘）→ `lake check --paranoid --from-export=<file>` 检验；同时登记默认形态（`lake check --paranoid` 全包）资源读数作对照。 Tenet 线闭包换装作**第二试点**（待首试点验收后申报，避让案 E 定谳庭节奏）。

**验收判据**（逐条可机检）：
- A-1 导出件 sha256 双次导出字节全等（外部先例形态）且落盘归档；
- A-2 `lake check --paranoid --from-export` 出口码＝0，逐内核 accept 日志全归档（leanchecker-paranoid/lean4lean/nanoda/con-leche[/con-ron]）；
- A-3 闭包导出喂 `--from-export` 的相容性实证（若官方实现拒收部分闭包导出，降级为全包 default-targets 形态并登记资源读数）；
- A-4 paranoid 实跑内核名单以日志实测为准，裁决 §1.1 的 con-ron 文档级微差；
- A-5 **阴性控制**：对导出件做 ≥1 件定向篡改（单声明证明项置换，solveathome 14/14 控制先例形态），全部内核必须 reject（exit≠0）——无阴性控制的 accept 不采信（沿 2026-07 伪造事件教训）；
- A-6 公理报告恰为标准三公理，无白名单外条目；
- A-7 资源读数（墙钟/内存峰值）落册，不预设阈值、只登记实测（甲席席规：不产新估计）。

**窗**：首试点承接 **R2B-09 既有窗（2026-11-15 前）**，执行避让 11-04 S2 执行日与 11-08/11-15 硬钉期算力争用（案 E 随裁纪律），建议落 **2026-11-03 预飞闸后至 11-06 前**的隙窗（与 W2-P0-09 comparator 调用面实证同窗并验，一次环境两用）；若 bubblewrap 在执行席不可用则顺延并登记降级形态（§6 R-1），不抢窗。

---

## 六、风险与不适配面如实登记

- **R-1 沙箱依赖**：bubblewrap 沙箱仅 Linux；联邦 CI 席位 bubblewrap 可用性无在案实证（本席机位无 lean/lake，无法实测）。`--inadvisably-no-sandbox` 存在但官方明示仅自备隔离者可用——正式跑批禁用；若执行席无 bubblewrap，须以「自备隔离＋降级登记」形态跑，证据强度降级标注（沿案 C 备通道降格先例精神）。
- **R-2 资源天花板**：全环境/大闭包导出在联邦 2 核/4GB 机位不可行（外部钉：nanoda 全环境 2h/36.6GB DNF＠96GB 机位）；任何「全 mathlib 级 paranoid 回放」须外部算力或 Arena 托管，联邦现行机位只承诺闭包级。
- **R-3 跨工具链导出相容性**：Tenet-repo（v4.34.0-rc2）/FGL（v4.30.0-rc1）产出的 NDJSON 喂 v4.35.0 检验器无在案实证；外部先例显示导出器与内核版本须配对调钉（arXiv:2605.19063 附录）；lean4lean olean 模式跨 commit 拒读已实证（solveathome）——**一律走 NDJSON、逐线做相容性首验**。
- **R-4 多内核非绝对**：2026-07 嵌套归纳伪造证明曾被官方内核＋leanchecker＋Nanoda 同时接受（oss-sec 2026-08-02；修复 v4.32.2 在案，FRONTIER-SCAN §4.4）——共享规格缝隙类缺陷不被实现多样性覆盖；con-leche 一致性证明覆盖「实现偏离规格」类、不覆盖「规格本身歧义」类。PASS 门槛「≥2 独立实现 accept」维持（FRONTIER-SCAN §4.4 接入建议在案），但不得表述为「内核绝对无误」。
- **R-5 证据边界**：`--from-export` 只对导出件负责、不对 workspace 项目负责（手册原文）；导出→检验链的名值绑定（sha256＋构建日志＋钉）是联邦侧义务，缺环则 accept 无所指。内核 accept **不证陈述贴合自然语言原意**（Arena 对 OpenAI 包复核的同限定在案，FRONTIER-SCAN §2.1）；陈述锚须走 comparator（challenge/solution＋permitted_axioms）而非 check。
- **R-6 与在途返修的接口**：W11/S2 comparator 通道返修（W2-P0-09 九项，预飞闸 2026-11-03）应采官方出口码契约（0/1/2）替代日志 grep verdict——若返修件与本件建议冲突，以判定席裁定为准；本件不改动在途返修义务。
- **R-7 公理闸边缘**：#14953 移除 trustCompiler 后含 `native_decide` 工件的公理报告形态无在案实测；现行锚件/Tenet 基线 8 声明公理集均为标准三公理（在案），预期不触红，但扩面至含 native_decide 的模块前须先实测其公理报告是否被闸误判。
- **R-8 文档级微差**：--paranoid 实跑集 Highlights 段（含 con-ron）与 #15145 行（未列 con-ron）不一致（§1.1）——以试点 A-4 实测为准，行文暂按「≥4 内核」保守表述。
- **R-9 前沿漂移**：v4.36.0-rc 系列已有 breaking 先例（reduceBool/reduceNat 移除等，FRONTIER-SCAN 监测项 5 在案）；联邦钉维持 v4.35.0 不动（B1-INFRA §3.3 建议在案），本件不建议任何随换装触发的钉迁移。
- **R-10 换装非证**：一切 paranoid accept 结果不改变 ζ 状态钉「区间见证层 PASS、kernel 层未证、非 RH 证据」与 Tenet 钉「自评已核、外部复现中、未颁奖」；工具换装是**验证编排层**事项，不构成任何数学主张的状态变更，禁借换装行文升格（沿 WILDQ3 问八 C3′ 延伸注记精神）。

---

## 附一、来源与依据钉清单

外部（本席 2026-10-26 检索/核读）：lean-lang.org v4.35.0 发布注记全文（#14884/#14885/#14953/#14990/#15005/#15048/#15050/#15055/#15096/#15099/#15130/#15145/#15146/#15147/#15153/#15156/#15157/#15542）；Lake 参考手册 25.1.5.8（出口码 0/1/2、--from-export 证据边界、manifest 要求、Linux-only）；de Moura 博客 2026-08-24/2026-10-15；oss-sec 2026-08-02 嵌套归纳伪造披露（#14576/#14577）；solveathome.org kk-lower-bound #2597 复跑件（工具链 bin 清单、22,948/407,077 记录、13.9s/34.3s/989s、nanoda 2h DNF/36.6GB、olean 头拒读、14/14 阴性控制）；shengyayun 2026-10-19（con-leche/con-ron 性质，二手转述标中可信度）；arXiv:2605.19063 附录（导出器跨版调钉先例）。

在案：FRONTIER-SCAN-20261026-02 §1.1/§2.1/§3.1/§4.4；WILDQ3-ZETA-20261026-01 问八/问九；ADJUD-R2B-20261026-01 案 E/案 H；ZETA-INST-01-20261012T2130Z §Lean 诚锚/§零共享代码；U17-KERNEL-PROBE-01 §1–§5；OBL-NS-02-TENET-RERUN-02 §一–§三；ADJUD-WILDQ-R1-HARVEST-01 R2B-09；ADJUD-WILDQ2-HARVEST-01 §1/§2/§8 与 W2-P0-09 表；A1-STACK-UPGRADE-DRAFT-01 五级栈与 BLOCKED 语义；B1-INFRA-20261025-01 §3.1/§3.3；MONITOR-FRONTIER-20261025-01 §六/§七；FUSION-EXT10-01 §6；WSH-S2-BLOCKER-DRAFT-01 §一（comparator yaml L112–115）。

## 附二、纪律自查

1. C1/C1′：涉 NS 限「有限维 ODE 截断层」语境；涉 ζ 限「有限高度 T=100/1000 截断」语境；状态钉逐字「区间见证层 PASS、kernel 层未证、非 RH 证据」未篡字；全件无「NS 已解决」「RH 已证/已验证到 T」字样；Tenet 唯一批准语在位。
2. 名值分离：Tenet-repo/Tenet.Kernel 双义强制区分；内核名、PR 号、出口码与来源分行；con-ron 微差双写不裁决。
3. 不编数：全部数值带外部来源钉或在案钉；本席零新产工时/产能估计；窗钉全部引用既有裁决窗（R2B-09 11-15、预飞闸 11-03、案 E 避让纪律）。
4. 本地实测如实登记：本机无 lean/lake/elan（三命令 not found 实测），无本机实测冒充。
5. append-only／零 git：vci-inbox 全程只读；本件为唯一新建件；不 commit。

—— QF-OS 联邦批二十五 K-PAR kernel 换装评估席 · 2026-10-26 · 只交付不 commit
