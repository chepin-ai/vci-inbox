CLASSIFY: L1
# CIRC-REWORK-M0-SPEC-01 · CIRC 重做 route B「见证认证」M0 里程碑规格书（v1.0 · 纯设计）

申报线：枢/PIVOT-01 · 执行分机 WS-31 · 2026-10-12 · 自治 A 级（纯成文，零执行）
上游锚：
- board/OBL-CIRC-REWORK-01-DRAFT.md（下称 OBL；仓内钉定文本为 v0.2·EXT09-R1 修订版；EXT09 三案已于 LAB-CLOSE-EXT06-20261011T1430Z §3 记 11/11 pass，v0.3 微补丁仅触 ②§2.4 B7 与 ③§4a(5)，①以 v0.2 文本 + R1 条款处置表为治理基准）
- board/FINDING-20261010-04-CERT-CIRC-LEAN族结构性不可验证.md（下称 FINDING-04）
- artifacts/hexagon-submission/v2/main.tex §5.3（FINDING-04 披露口径，下称「披露锚」）
- artifacts/CERT-CIRC-LEAN-01/family/EXT05-BATCH-01-RESULTS.md 及 EXT05-BATCH-01-results.json（下称 CIRC 结果锚）
- artifacts/CERT-AUCTION-01/README.md 及 family/EXT05-BATCH-01-auction-results.json（下称 AUCTION 结果锚）

本件性质：M0 里程碑的**纯文本设计规格书**。不产生、不修改任何数值结果；文中一切数值仅引用上述仓内已锚定材料，禁止新造。

## 0. 判定语义总则（沿用 EXT09 共性原则）

本里程碑一切验收奉行「默认拒绝、显式满足才放行」（OBL §0.1）：见证复算未获**正证据**（复算输出 + 哈希链 + 证据指针）满足者一律视为未通过；「复算未见异常」不构成通过依据。格式层同律：缺 `schema_version` 的见证文件，核验程序拒绝受理（OBL §9、A1 案 §4b 同款延伸）。

## 1. M0 目标定义：route B「见证认证」的最小可行形态

**目标**：Python 区间层为每个证书实例产出一份自包含的**见证文件（witness）**，使第三方/机器在**无 Lean 环境**条件下，仅凭见证文件 + 复算脚本指针，即可独立复算并核验该实例的区间认证结论（Krawczyk 严格内包 / 对偶括弧三件套），且负控（扰动输入）必被复算拒绝。

见证文件内容五要素（对应 OBL §3 路线 B「显式数值见证」条款）：
1. **输入**：实例全部决定论输入（circulant：k、ε、c 向量、gauge；auction：k、R、seed、ε-schedule、生成器指针）；
2. **区间界**：盒半径、Krawczyk 像盒端点/宽度、括弧端点等，以有理或十进制字符串登记（禁止二进制浮点裸值作为唯一表示）；
3. **外舍入参数**：区间引擎标识与精度参数（mpmath.iv + mp.dps=80；或 np.nextafter 定向舍入）、有理化精度登记（limit_denominator 参数）；
4. **负控记录**：扰动向量、扰动量、复算预条件子声明、负控复算结论（必须拒证）；
5. **复算脚本指针**：脚本仓内路径 + 内容 sha256 + 结果文件 sha256 + 环境指纹，使「见证→复算→比对」闭环可重放。

**M0 边界（非目标）**：
- 不做 Lean 侧任何动作（bridge 引理、Bareiss 核验核属后续里程碑/后续义务）；
- 不改变任何认证判据本身（沿用 CIRC/AUCTION 结果锚的判据，1:1 复原纪律）；
- 不升级对外口径：M0 产物口径 = 「内生 fail-closed 见证复算核验」，**不得**宣称「机器验证证书」全级口径（OBL §10 升级门未过前）。
- 与 OBL §5 里程碑表的关系：本件为 route B 执行线的自有里程碑梯（M0–M4）；OBL §5 之 M1–M4 为治理层节拍，二者并行不悖，接口见 §6。

## 2. 见证文件 schema（JSON · v1.0）

### 2.1 版本与格式纪律（对齐 EXT09 ①§9 / ③§4b，fail-closed）

- 首字段必须 `schema_version: "<major.minor>"`；缺失即格式不合规，核验程序拒绝受理（默认拒绝律延伸至格式层，OBL §9 ①、A1 §4b 同款）。
- major 变更（字段删除/语义变更）不允许向后兼容豁免：旧见证须一次性迁移脚本升级，保留原件哈希与迁移映射表；minor 变更（纯增字段）向后兼容，读取时以显式缺省值补全并登记。
- 核验器按 schema major 分派；遇高于自身支持的 major → fail-closed 拒验并登记 `unsupported_schema`，禁止静默降级解析（③§4b 同款）。
- schema 版本与脚本 sha256 / 依赖 pin 为独立维度，禁止互相替代（③§4b「checker_rev 纪律」延伸至 Python 复算脚本）。
- 本 OBL 存续期间签发的一切见证，其 schema 版本对应解析器/核验器版本指针随见证一并落板（旧证可解析义务，OBL §9 末款）。
- 存量衔接：EXT05-BATCH-01-results.json 与 EXT05-BATCH-01-auction-results.json 现行无 `schema_version`，属 legacy 件；迁移走 §2.1 major 纪律（迁移脚本 + 原件哈希 + 映射表），原始文件不覆写（列入 §7 未决项 U2）。

### 2.2 字段表

通用顶层字段（两族共用）：

| 字段 | 类型 | 必/选 | 语义 |
|---|---|---|---|
| `schema_version` | str | **必填·首字段** | `"1.0"`；缺失/高 major → 拒验 |
| `witness_id` | str | 必填 | 全局唯一，建议 `<family>-<tag>-<yyyymmdd>` |
| `family` | str | 必填 | `"circulant-sinkhorn"` \| `"auction-dual"` |
| `claim` | str | 必填 | circulant=`"unique_root_in_box"`；auction=`"cost_in_dual_bracket"` |
| `inputs` | obj | 必填 | 决定论输入全集（见 2.3/2.4） |
| `interval_engine` | obj | 必填 | `{name, precision, rounding}`：如 `{mpmath.iv, dps:80, outward}` 或 `{numpy.nextafter, directed_endpoints}`（沿用结果锚登记值） |
| `rationalization` | obj | 必填 | limit_denominator 参数登记（circulant 首批 ~1e-13 / 复验批 ~1e-26 精度档，见 CIRC 结果锚） |
| `bounds` | obj | 必填 | 区间界：字符串表示的端点/宽度（见 2.3/2.4） |
| `verdict` | obj | 必填 | `{inside: bool, metrics: {...}}`；metrics 仅登记已锚定量（condJ、K_max_width、K_min_margin / gap、bracket_width 等） |
| `negative_control` | obj | 必填 | 见 2.5；缺失即格式不合规（fail-closed） |
| `replay` | obj | 必填 | `{script_path, script_sha256, results_sha256, env_fp, run_id, ts}` |
| `provenance` | obj | 必填 | `{generator_line: "PIVOT-01 计算线", source_anchors: [仓内路径...]}` |
| `witness_sha256` | str | 必填 | 本文件除本字段外规范化序列化的 sha256 |
| `lean_binding` | obj | 可选·缺省=null | 预留：Lean 核验核接缝（M1+）；M0 恒 null 且**禁止**填写任何 Lean 通过性声明 |
| `notes` | str | 可选 | 自由文本，不承载判定语义 |

### 2.3 circulant-sinkhorn 族 `inputs` / `bounds` 子结构

- `inputs`：`{k: int, eps: str(有理), c: [str(有理)×k], gauge: "f0=0", n: int}`——n=2k−1（11/19，FINDING-04 口径）；c 向量沿用各族既有登记值。
- `bounds`：`{box_radius: "1e-9", center: {ghat: str(有理), ...}, preconditioner: {kind: "rationalized_inverse_jacobian", limit_denominator: "1e10"}, krawczyk_image: {max_width: str, min_margin: str}}`——判据为 K(X)=x̂−C·F(x̂)+(I−C·J(X))·(X−x̂) 严格内包（CIRC 结果锚方法论段原文）。
- `verdict.metrics`：`{condJ, K_max_width, K_min_margin}`——仅登记对应批次已公布值，不得外推新数。

### 2.4 auction-dual 族 `inputs` / `bounds` 子结构

- `inputs`：`{k, R, seed, eps_schedule: {eps0:"0.5", factor:"/5", eps_final:"1e-6"}, generator: "rng=np.random.default_rng(seed); C=10^(R·(2·rng.random((k,k))−1))", solver: "forward-auction + HiGHS(仅作不可信候选生成器)"}`（AUCTION 结果锚复原声明原文口径）。
- `bounds`：`{bracket: {lb_lo: str, ub_hi: str}, bracket_scale: "k×[LB_lo,UB_hi] (Birkhoff)", rc_min_lo: str, delta_deflation: "1e-10", gap: str, gap_bound: "k·eps_final"}`。
- `verdict`：`{inside: bool, gap_within_bound: bool, dual_feasible_certified: bool}`。
- **诚实边界字段（必填）** `honesty_boundary`：固定登记「UB=c·x 以 HiGHS 原始解为候选，primal 可行性信赖至 ~1e-12，未经区间认证」（披露锚 Remark 5.2 原文口径）；该族无 Lean 移植。

### 2.5 `negative_control` 子结构（两族共用骨架）

| 字段 | 必/选 | 语义 |
|---|---|---|
| `perturbation` | 必填 | circulant：`{kind:"center_shift", target:"g", delta:"1e-6", preconditioner:"recomputed"}`；auction：`{kind:"swap_perturbation", spec:"交换扰动"}` |
| `neg_verdict` | 必填 | circulant=`{neg_inside: bool(必须 false), neg_K_min_margin}`；auction=`{neg_rejected: bool(必须 true), neg_cost}` |
| `same_lineage` | 必填 | 负控脚本与正例脚本同源、同环境指纹声明（OBL §4 AC4 纪律延伸至见证层） |

## 3. 验收判据（谓词化 · 默认拒绝 · 合取无豁免）

判定程序逐条输出 true/false + 证据指针；任一 false 或证据缺失即 M0 不通过。

- **M0-AC1（schema 合规）**：∀ 见证文件 w：schema_version 解析通过 ∧ 必填字段齐 ∧ witness_sha256 复算一致 ∧ 核验器 major 分派未触发 `unsupported_schema`。
- **M0-AC2（circulant 六例复算全过）**：∀ i ∈ 六实例族（k∈{6,10}×ε∈{1,1/2,1/5}）：独立复算（凭见证 + replay 指针，无 Lean）得 inside=true ∧ 度量与见证登记一致（判定容差=逐字符串一致；数值比对仅对字符串解析后的有理/区间量）。
- **M0-AC3（auction 五例复算全过）**：∀ i ∈ 拍卖对偶五例（BENCH k8 seed7、EXT k∈{6,10,12}、SCHED-VAR）：inside=true ∧ gap_within_bound=true ∧ dual_feasible_certified=true，括弧/gap 与见证登记一致。
- **M0-AC4（负控必拒，双向 fail-closed）**：∀ i ∈ 6+5 例：按见证 negative_control 节复算扰动输入 → 必拒（circulant neg_inside=false；auction neg_rejected=true）；任一负控复算放行即整批 M0 不通过并触发证据链审计。
- **M0-AC5（复算独立性）**：复算在**无 Lean 工具链**环境完成（env_fp 中无 lean/mathlib 维度；Python 侧 env_fp 定义列入未决项 U3，未定前以 runner 声明 + 依赖清单哈希代偿并显式登记为 interim）。
- **M0-AC6（口径合规）**：见证及随附文本经 §4 检查表逐项过；出现任何 Lean 可移植/已通过暗示即 false。

## 4. 与 FINDING-04 披露口径的一致性检查表

逐条核对（披露锚 = hexagon v2 §5.3 + FINDING-04 判定节）：

| # | 检查项 | 合规口径 |
|---|---|---|
| C1 | 认证承载层表述 | 「circulant 族认证完全由 Python 区间层承载（outward rounding、严格内包判据、非奇异预条件子、负控）」；witness 是该承载层的**可复算证据化**，不新增认证层级 |
| C2 | Lean 件性质 | 现有 Lean 件 = 「形式化陈述稿（formal statement artifacts）」，非机器验证证书；v4341 修复件钉 ELAB_OK / CHECK_FALSE(structural) 如实 verdict |
| C3 | **禁止声称 Lean 可移植/已通过** | 禁止任何「已移植 leancert」「native_decide 通过」「Lean 机器核验」表述；witness 的 `lean_binding` 恒 null |
| C4 | 结构性根因表述 | 若引述根因，限 FINDING-04 两条：ADSupported 自引入提交 4bf84ea91 起不含 Expr.log；Matrix.det 为 Leibniz 定义、n=11/19 不可机算 |
| C5 | pin 纪律 | 引述 leancert 限 commit oid 钉定 v4.34.1（7f91b6eb35）；tag 漂移（v4.35.0 a5777840 ≠ 钉定）已确权入册，禁采信浮动 tag |
| C6 | 口径升级门 | M0 产物口径上限 = 「内生 fail-closed 见证复算核验」；「机器验证证书」表述须经 OBL §10（外部签名 / 独立核验面）裁定后方可启用 |
| C7 | auction 诚实边界 | 必须携带 honesty_boundary 字段（§2.4），禁止静默修补 UB 侧非区间认证事实 |
| C8 | v1→v2 订正史 | 若对外引述，须维持披露锚「v1 措辞 overstated、已在 v2 订正」的叙事完整性，不得回退至 v1 口径 |

## 5. 见证生成-复算信任基声明（设计立场）

- Python 层为**见证生成器**；复算核验不信赖生成器正确性——见证无效/被篡改则复算结论分歧，fail-closed（OBL §3 路线 B 信任基条款的 M0 落地：以独立复算替代 Lean 核验位）。
- 闭形式解（circulant g* 闭式）仅作负控 ground truth，证书不咨询之（披露锚 §5.1 原文纪律），见证文件不携带闭形式字段。
- 自签闭环风险（OBL §6 R5）在 M0 不消失：见证生成与复算同出联邦计算线；对冲靠（i）replay 指针全哈希链可第三方重放，（ii）OBL §10 升级门后续裁定。本规格书不声称消解该风险。

## 6. M1–M4 接口预留（仅接口名 + 一句话契约，不展开）

| 接口 | 一句话契约 |
|---|---|
| `IF-M1-witness-generator-freeze` | M1 冻结见证生成器：输入=仓内锚定判据/脚本，输出=符合 §2 schema 的 11 例（6+5）见证文件 + 生成日志哈希；冻结后改动走新 sha 对纪律 |
| `IF-M2-independent-replayer` | M2 独立复算器：输入=见证文件 + replay 指针，输出=逐例 verdict JSON（含 schema_version），与生成器零共享代码路径为达标形态 |
| `IF-M3-negative-control-suite` | M3 负控/扰动套件：输入=见证 negative_control 节，输出=必拒实证 + 扰动覆盖清单，失败路径须可复现（复跑逐字节一致） |
| `IF-M4-disclosure-alignment-gate` | M4 披露对齐与升级闸：输入=M1–M3 证据包 + §4 检查表，输出=对外口径裁定申请（上限仍受 OBL §10 约束），不合规即降级登记 |
| `IF-X-lean-bridge`（远景，非本梯承诺） | Lean 核验核接缝：消费见证 `lean_binding` 字段，schema major 不变前提下启用；是否成义务待 OBL §8 问题 1/4 裁定 |

## 7. 未决项（如实登记）

- **U1**：leancert 替代库/超越函数检查器评估待 WS-32 文献收割输入；M0 不依赖其结论，评估结果仅影响 `IF-X-lean-bridge` 是否激活。
- **U2**：存量 EXT05-BATCH-01 两份 results.json 的 legacy 迁移（补 schema_version、迁移脚本、映射表）排期未定；迁移前旧件以「原件哈希 + 本规格 §2.1 legacy 条款」受保护，不覆写。
- **U3**：Python 侧 env_fp 规范未定（A1 §5 为 Lean 向定义）；M0-AC5 暂以 runner 声明 + 依赖清单哈希代偿（interim，须显式登记）。
- **U4**：witness_sha256 的规范化序列化规则（键序/空白/Unicode）未冻结，M1 前须定稿，否则跨实现哈希不可比。
- **U5**：OBL §8 问题 1（显式 checker+见证是否视同机器验证证书）、问题 2（witness schema 是否纳入公理审计面，类比 F-VERIFY-05 教训）、问题 7（外部签名人选）均待判定席裁定；本规格按「不视同、暂不入审计面、口径降级」的保守缺省设计。
- **U6**：仓内 OBL 文本为 v0.2，而 LAB-CLOSE-EXT06 记三案 11/11 pass @v0.3；v0.3 微补丁记录仅触 ②③，①是否另有 manifest v1.2 回写义务影响本 M0 范围，待枢线确权（本件先按 v0.2 文本 + R1 处置表设计）。
- **U7**：路线 A（log 消除）若后续叠加，改写后方程的见证 schema 兼容走 minor 升版（纯增 `equation_form` 字段），本版不预留语义。

## 8. 纪律声明

本件为纯设计文本：零代码、零执行、零新数值。文中全部数值（盒半径 1e-9、mp.dps=80、limit_denominator 精度档、负控扰动 1e-6、δ-deflation 1e-10、ε-schedule 0.5→/5→1e-6、cond/K 宽量级、五例 auction 锚值等）均逐字引用 §0 所列仓内锚定材料；任何超出锚定材料的数值声明即视为本规格书缺陷，按默认拒绝律处置。

—— 枢/PIVOT-01 · WS-31 · 2026-10-12
