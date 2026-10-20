CLASSIFY: L1
# SIDECAR-SCHEMA-T0T4-01 — OBL-EXT-06 sidecar schema T0–T4 + G0→G4 阶梯规程 v1

- 波次/线：EXT-WAVE-18「攻」 WS-C 攻坚线 · 枢/PIVOT-01 体系 · L4 判定层旗舰首批落地
- 日期：2026-10-21（UTC(Z) 单时钟域，Q6-b）
- 上游：WS-44《NS-SOLUTION-v2 设计书》§六 L4-2（G0→G4 阶梯）/ L4-4（Palomar 式注册表）；EXT18 判定修正生效体卡3（TrustBoundary 明轨登记）、卡4（Palomar 兼容互认对接）、卡6（钉版本/截止/「截至[日期]」时间戳）；D05 只升不降律
- 下游：`registry/palomar-registry-v1.yaml`（本 schema 的首个实例）
- 激活依据：OBL-EXT-06 standby → 激活（WS-44 §六 L4-4 行「OBL-EXT-06 standby 激活」）

---

## 一、定位与术语

1. **sidecar（侧车）**：随包发放、与包本体同址或指针同址的机读佐证记录。本体（.lean 源、构建产物）留仓内，佐证记录的**指针与哈希**入册——同址原则（WS-44 L4-1 注）。
2. **T 级（T0–T4）＝证据记录分级 schema**：规定一条 sidecar 记录在该级必须携带的字段、证据类型与签名方式。T 级描述**单条证据记录**的形态。
3. **G 级（G0–G4）＝定级阶梯**：描述**一个包整体**当前达到的认证档位。G 级由 T 级证据支撑：Gn 的登记要求对应 Tn 级证据记录齐套（§五）。
4. **append-only**：注册表与本 schema 的登记实例一经签发不删不改；修正以新条目形式追加，旧条目加 superseded 指针保留（与册仓 append-only 并轨，WS-44 L4-4）。
5. 语纪律：全文遵守 C1–C3 + C1′–C3′；OpenAI 相关成果口径固定为「自评已核、外部复现中、未颁奖」。

---

## 二、T0–T4 字段表

通用约定：
- 时间戳一律 UTC(Z) 单时钟域（Q6-b）；凡「现状类」断言必须携带「截至[YYYY-MM-DD]」格式的时间戳钉（EXT18 卡6）。
- 哈希一律 SHA-256、小写 64-hex；commit 钉一律 40-hex 全钉（禁短钉入册；短钉只许出现在叙述性引文中并标注「短钉」）。
- 所有「必填」字段缺失即该记录不构该级；「选填」字段缺失须在 `notes` 写明「未定+理由」（甲席席规：禁编造）。

### T0 — declared（自述声明）

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `record_id` | 是 | string | 全册唯一，`T0-<包名>-<yyyymmdd>` 建议式 |
| `subject.name` / `subject.scope` | 是 | string | 包名 + 范围钉（明确含什么、明确不含什么） |
| `declarant` | 是 | string | 声明主体（团队/个人署名） |
| `claim_text` | 是 | string | 自述断言原文；禁领先语 |
| `as_of` | 是 | date | 「截至[日期]」钉 |
| `created_at` | 是 | UTC(Z) | 记录签发时刻 |
| `self_fingerprint_sha256` | 是 | 64-hex | 记录正文（除本字段）的 SHA-256，自指防伪 |

证据类型：自述文本，不要求机器产物。签名：`self_fingerprint_sha256`（自签）。

### T1 — machine-attested（机器佐证）

T0 全部字段 + 以下：

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `toolchain_pin` | 是 | string | 工具链版本钉（如 `leanprover/lean4:v4.35.0`）+ 其文件 SHA-256 |
| `dependency_pin` | 是 | 64-hex | 依赖清单文件（lake-manifest.json 或等价物）SHA-256 |
| `source_digest` | 是 | 64-hex + recipe | 源码合并流 SHA-256 + 可复现的拼接顺序说明 |
| `machine_checks[]` | 是（≥1） | list | 每项：`tool` / `tool_version` / `run_id` / `verdict` / `log_sha256` / `as_of` |
| `axiom_whitelist` | 是 | list | 允许公理白名单（如 propext/Classical.choice/Quot.sound）；越白名单即不构 T1 |
| `exclusion_pointers[]` | 是 | list | 逐项排除指针（同址原则：本体留仓、指针入册） |

证据类型：CI run 产物、构建日志、扫描输出（sorry-scan / axiom-audit 或等价）。签名：`self_fingerprint_sha256` + 各 run 产物 `log_sha256`。

### T2 — registry-witnessed（注册表见证）

T1 全部字段 + 以下：

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `commit_pin` | 是 | 40-hex | 见证对象的全钉 commit |
| `witness.identity` | 是 | string | 见证者身份；主体匿名/隶属未公开者须显式标注「主体匿名性已标注」 |
| `witness.independence` | 是 | string | 独立性声明（与包作者无隶属/无共同署名） |
| `witness.evidence_excerpt` | 是 | string | 见证结论逐字引文（禁转述代替） |
| `witness.source_url` + `witness.accessed_at` | 是 | url + date | 一手来源与直读日期 |
| `witness.scope_limit` | 是 | string | 见证范围与局限如实登记（如内核见证不覆盖语义层） |
| `witness_artifact_sha256[]` | 是 | list | 见证产物（日志/报告）哈希钉；原始产物未获者记「未定+理由」 |
| `dual_kernel` | 是 | record | nanoda 双核（或异构双核）复核结果；未执行记「未定+理由」 |
| `llm_second_review` | 是 | record | LLM 独立二审席书面意见指针（Palomar 要件） |
| `registry_entry_ref` | 是 | string | 注册表条目 id（append-only 签发后回填） |

证据类型：第三方独立复跑/复检产物 + 逐字引文 + 注册表签发记录。签名：注册表签发哈希 + 见证产物哈希。

### T3 — externally-audited（外部审计）

T2 全部字段 + 以下：

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `auditor.identity` / `auditor.affiliation` | 是 | string | 审计方身份与隶属（联邦外第三方） |
| `auditor.independence` | 是 | string | 独立性声明 + 利益冲突排查记录指针 |
| `audit_report.uri` / `audit_report.sha256` | 是 | url + 64-hex | 审计报告位置与哈希 |
| `audit_report.scope` / `audit_report.limitations` | 是 | string | 审计范围与局限（含 statement fidelity 是否覆盖） |
| `audit_date` | 是 | date | 审计完成日期 |
| `auditor_signature` | 是 | string | 审计方可核验署名（detached signature 或等价公开渠道署名指针） |

证据类型：署名审计报告。签名：`auditor_signature`（他签，自指哈希不足以构 T3）。

### T4 — author-endorsed（作者背书）

前置 T2 齐套（T3 非硬前置，见 §5.1 注）+ 以下：

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `endorser.identity` | 是 | string | 背书人（原论文/原成果作者或其正式代表） |
| `endorsement.statement` | 是 | string | 背书文逐字 |
| `endorsement.channel` + `endorsement.date` | 是 | string + date | 公开可核验渠道（主页/署名信函/公开仓）与日期 |
| `contact_verification` | 是 | string | 接触核验记录（如何确认背书出自本人） |
| `endorsement_scope` | 是 | string | 背书覆盖范围（全包 / 指定声明清单；禁默示扩大） |

证据类型：公开渠道背书文。签名：背书人公开渠道署名（以渠道可核验性代签章）。

---

## 三、与 formalization.yaml 上游 v0.4 的兼容映射

上游 formalization.yaml v0.4 四必填顶层块（project / sources / status / automation；review、alignment、fidelity 为通行扩展键）与本 sidecar 的映射如下。本仓 NS 包实例（`library/ns/formalization.yaml`，version 字段自标 "v0.5"＝上游 v0.4 + 联邦 `federation:` 扩展块，schema 容忍未知顶层键、check-jsonschema 仍通过）已按此映射落地。

| sidecar 字段（T 级） | formalization.yaml 键 | 说明 |
|---|---|---|
| T0 `subject.scope` / `claim_text` | `project.description` + `status.scope` | 范围钉双层互载，措辞须一致 |
| T0 `declarant` | `project.authors` / `project.responsible_maintainers` | — |
| T1 `toolchain_pin` / `dependency_pin` | `automation.methods[].tool_setup` | 工具链与依赖钉随构建自述 |
| T1 `machine_checks[]` | `automation.methods[]` + `review.notes` | run_id、verdict、log 指针 |
| T1 `axiom_whitelist` | `status.axioms` / `status.main_results[].axioms` | 白名单逐 decl 承载 |
| T1 sorry-free 判据 | `status.sorry_count` / `status.sorry_in_definitions` | 数值直载 |
| T1 `exclusion_pointers[]` | `federation.exclusion_pointers[]`（扩展块） | 同址原则 |
| T1/T2 三槽哈希 | `federation.certificate.artifact_digests` + 注册表条目 | 发放时实测回填（EXT18 卡4 条件载） |
| T2 `registry_entry_ref` / 定级 | `federation.certificate.grade` / `federation.upgrade_path` | G 级与注册表条目互指 |
| T2 `witness` / `dual_kernel` / `llm_second_review` | `federation.review_rounds[]` + 注册表条目 witness 段 | yaml 载指针，注册表载全文 |
| T3 `auditor` / `audit_report` | `review.status` / `review.reviewers[]` | `self-assessed` → 外部审计后改写 |
| T4 `endorsement` | `sources[].author_endorsement` | 现值 `not-contacted` / `n/a` 即未达 T4 |
| NL↔Lean 对齐（旗舰 L4-5） | `alignment.statements[]` | 状态机：proved / not-formalized（显式登记防范围误读） |
| 语义分歧披露 | `fidelity.divergences` | T3 审计的 statement fidelity 结论落此键 |

---

## 四、G0→G4 阶梯规程

### 4.1 等级定义

| 级 | 名称 | 定义 | 支撑证据 |
|---|---|---|---|
| G0 | declared | 包方自述声明登记入册，范围钉齐、无机器佐证要求 | T0 记录 1 条 |
| G1 | machine-attested | 钉定工具链+依赖下机器检查全绿（build / sorry-scan / axiom-audit 三绿基线或包级等价），自述与机器证据一致 | T1 记录齐套 |
| G2 | registry-witnessed | 独立第三方见证复核完成并逐字归档，40-hex 全钉 + 三 SHA-256 + nanoda 双核（或异构双核）+ LLM 二审，注册表 append-only 签发 | T2 记录齐套 |
| G3 | externally-audited | 联邦外署名审计通过，审计范围与局限入册（含 statement fidelity 是否覆盖的明示） | T3 记录齐套 |
| G4 | author-endorsed | 原成果作者公开渠道背书，背书范围明示 | T4 记录齐套 |

注（升级拓扑）：标准路径 G0→G1→G2→G3→G4 逐级；G4 的 T2 前置为硬要求、T3 非硬前置（作者背书不以待外部审计完成为条件，但未过 G3 者须在条目注明「G3 未达」）。跳级申请禁止（八步仪式逐步过闸）。

### 4.2 八步升级仪式（逐级适用）

1. **申请立案**：升级申请条（目标级、范围钉、「截至[日期]」）入流，判定席受理并编号。
2. **证据冻结**：40-hex commit pin + 三 SHA-256 实测回填；冻结后任何改动即开新条目，禁原地改数。
3. **机器复核**：目标级机器要件全绿——G1＝三绿基线（build / sorry-scan=0 / axiom-audit 不越白名单）；G2 起加双核。
4. **独立见证**（G2 起）：第三方见证证据集齐——逐字引文、一手来源、独立性声明、范围局限；缺项记「未定+理由」，不得凑数。
5. **LLM 二审**：独立二审席对「自述↔证据一致性」出书面意见（Palomar 要件）；编译通过 ≠ 判定通过（SCI=∞ 培训结论，WS-44 L3-4）。
6. **判定席裁定**：双轮律（R1 条件准 → 定向补强 → R2 收敛），裁决文编号归档；八卡条件清单常设合规钩逐钩核查。
7. **append-only 登记**：注册表签发新条目（含自指签发哈希），旧条目永存。
8. **公告并轨**：与册仓 append-only 并轨、history.md 类监控钉就位、对外口径核查（禁领先语；OpenAI 口径钉「自评已核、外部复现中、未颁奖」）。

### 4.3 只升不降闸（D05）

- 定级**只升不降**：新证据只能以新条目形式追加支撑升级；任何级别不因时间经过自动失效。
- 条目一经签发不删不改；发现错误时以新条目登记修正，旧条目加 `superseded_by` 指针保留——append-only 与册仓并轨，无例外。
- 「升」的唯一合法路径是 §4.2 八步仪式；任何越仪式的级别宣称无效并登记为合规事件。

### 4.4 降级/除名的唯一例外通道（判定席裁定）

- **触发情形**（须举证）：（a）哈希失配——登记产物与在册哈希不符，指向产物被替换或登记错误；（b）见证/审计证据被证伪；（c）自述与机器证据矛盾且补正失败。
- **程序**：异议立案 → 证据听证（包方答辩权）→ 判定席双轮律裁定 → 以**新条目**形式登记降级或除名裁定（原条目保留并加裁定指针，append-only 不破）。
- **除名后重入**：须从 G0 重走八步仪式，历史裁定条目随新申请一并呈阅。
- 本通道是降级/除名的**唯一**合法路径；任何个人席位的单方面降级宣告无效（裁决先行、登记同步、行文随后——EXT18 总原则）。

---

## 五、合规自检（本文件行文）

本文件为规程定义件，不含数学断言；不涉及任何「NS 已解决」表述；涉 OpenAI 成果处一律使用「自评已核、外部复现中、未颁奖」口径；全部时间戳为 UTC(Z) 并携带「截至[日期]」钉（卡6）；估算类内容无散布超 1.5 倍项（甲席席规）。未定项：T3/T4 的署名技术形态（detached signature 具体格式）未定——理由：联邦尚未选定签名基础设施，待 G3 首例前由判定席裁定补规。
