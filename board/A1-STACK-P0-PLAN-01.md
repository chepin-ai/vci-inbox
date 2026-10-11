CLASSIFY: L1
# A1-STACK-P0-PLAN-01 · A1 检查器堆叠升级案 P0 实施计划（纯设计 · 零执行）
枢/PIVOT-01 执行分机 WS-30 · 2026-10-12 · 自治 A 级（纯成文，零执行）· mirror-surge
上游文档：`board/A1-STACK-UPGRADE-DRAFT-01.md` v0.3（EXT09-R2B 修订，11/11 已过；引用一律给节号）；跨案参照 `board/CACHE-ANCHOR-CLAUSE-DRAFT-01.md` v0.3（②案，§2.4 B7 / §8）。
性质声明：本文仅为 P0 实施计划之**设计**，不实施任何 P0 动作（不建 schema 文件本体、不跑扫描、不写登记条目）；与 WS-27 分工隔离——WS-27 只做 ②案核查器，本案仅预留接口点，不重复实现。

## 0. 范围界定
依草案 §6 分阶段表，P0 行为「本草案成文 + L0 确权登记（§2）」（产出：本案 + SELFCHECK-01 基底登记条目，自治级 A）。枢线指令将 P0 扩展为三工作项，均属成文/登记形态、不含执行环境动作：
- **P0-1 L0 确权落地**（§2）：CERT-SELFCHECK-01 基底登记条目成文化。
- **P0-2 L1/L2 契约 schema_version 首字段规范**（§3/§4 输出契约 + §4b 版本化策略）：两 schema 文件规格。
- **P0-3 DISPUTED 状态机登记格式**（§4a）：字段集 {dispute_id, artifact_sha256, l1_record_ptr, l2_record_ptr, ts_open, dispute_resolver, dispute_timeout_ms, default_action_on_timeout} + schema_version 的登记模板规格。
附工作项 **P0-4**：§4a(6) 30 天补录条款执行清单（见 §3）。
不在 P0 范围：P1–P4（§6 表）全部 B 级项——L1 复跑首跑、L2 接入探针、双器配对常态化、OBL-A1 状态迁移提案，均按既有冻结点纪律挂起（详见各项冻结点标注）。

## 1. P0-1 L0 确权落地（草案 §2）
**交付物形态**：L0 基底登记模板（JSON，建议落 `registry/a1-stack/L0-base-entries.json` 之规格文件 + 一条 CertSelfCheck01 登记条目模板；条目本体于实施波次填入）。
**登记字段集**（全部必填）：
```
{ "schema_version": "1.0",
  "base_id": "CERT-SELFCHECK-01",
  "artifact_path": "artifacts/lean-verified/CertSelfCheck01.lean",
  "artifact_sha256": "...",          // 草案 §0 锚：@f8cb83e7
  "theorems": ["add_sound","neg_sound","check_sound","end_to_end"],
  "axiom_audit": ["propext","Classical.choice","Quot.sound"],
  "sorryAx_present": false,
  "verify_request_ids": ["d9034a05","44208d46","082321e6","f3c1fc61"],
  "env_fp": "<草案 §5 指纹>",
  "lock_status": "locked",           // §2 基底冻结：已验证 sha 对不动
  "ts_register": "<UTC>" }
```
**验收判据（可机检）**：
1. `theorems` 恰为 4 元且与 §0/追记36 名称集合相等；2. `axiom_audit` 为 [propext, Classical.choice, Quot.sound] 子集且 `sorryAx_present=false`（无 sorryAx 硬门，草案 §4 证据格式纪律同款）；3. `verify_request_ids` 恰 4 元且与工件 sha256 配对（草案 §9 R5：一次性证据随工件 sha 配对防断链）；4. `env_fp` 符合 §5 公式 sha256(toolchain‖mathlib_rev‖cache_fp‖runner_id‖os_image) 的字段组成；5. 登记条目首字段为 `schema_version`（§4b 首字段必填律延伸适用）。
**依赖与冻结点**：依赖 = 追记36 已落工件与云端验证记录（已就位，无新增依赖）。冻结点 = §2 基底冻结条款：CertSelfCheck01.lean 任何修改走新 sha 对并重新云端验证（追记7 修复法度）；本登记条目仅指向既有 sha 对，不构成修改。自治级 A，无挂起项。

## 2. P0-2 L1/L2 契约 schema_version 首字段规范（草案 §3/§4/§4b）
**交付物形态**：两个 JSON Schema 规格文件（设计稿，建议落 `registry/a1-stack/schemas/l1-output.schema.json`、`l2-output.schema.json`）+ 一份校验脚本规格（`spec/l1l2-contract-checker.spec.md`，仅规格不实现）。
**schema 要点**（字段集照录草案 §3/§4 输出契约，不增删）：
- L1（§3）：schema_version(首字段,"1.0") / artifact_sha256 / checker="lean4checker" / checker_version / env_fp / verdict∈{pass,fail} / wall_s / log_sha256 / runner / run_id / ts；BLOCKED 为层外登记（§3 fail 处理条款：环境未备记 BLOCKED 转 §6 阶段门，不在 JSON verdict 值域内）。
- L2（§4）：schema_version(首字段,"1.0") / artifact_sha256 / checker="Lean4Lean" / checker_rev（全 sha 钉定，§4b 禁 tag 引用）/ env_fp / verdict∈{pass,fail,unsupported}（unsupported 合法第三值，诚实缺口律）/ axiom_audit（必填数组）/ sorryAx_present（必填布尔）/ log_sha256 / runner / run_id / ts。
- 版本化规则成文入 schema 注释与规格（§4b）：schema_version 缺失即格式不合规拒绝受理；major 不静默兼容（消费方遇高 major 登记 unsupported_schema 拒绝消费）；minor 纯增字段向后兼容、读侧显式缺省值补全。
**验收判据（可机检）**：
1. 两 schema 均声明 `schema_version` 为必填且为第一键序字段（JSON Schema 以 required + 规格文件键序约定双重表达）；2. 正例/反例样例集（每 schema ≥2 正例、≥3 反例：缺 schema_version / checker_rev 用 tag / verdict 越域）随规格交付，供未来校验脚本对拍；3. L2 的 unsupported 值入 enum 且规格明示「unsupported 不视为 fail」（§4）；4. checker_rev 正则锚定 40 位十六进制全 sha。
**依赖与冻结点**：schema 成文为 A 级；但 **L1/L2 契约终审走判定席双轮律（§6 P1/P2 行注记 B 级）——终审与首跑接入按既有冻结点纪律挂起**，P0 仅交付待终审的规格稿。依赖 = 草案 §3/§4/§4b 条文（已生效基面）；L2 checker_rev 具体 pin 值待 P2 探针波次定（P2 依赖外部环境，追记34 root 冻结点同款边界，挂起）。

## 3. P0-3 DISPUTED 状态机登记格式（草案 §4a）
**交付物形态**：DISPUTED 登记册模板（建议 `registry/a1-stack/dispute-registry.template.json` + 册本体规格 `spec/dispute-registry.spec.md`）。
**登记字段集**（照录 §4a 进入条款，全部必填）：
```
{ "schema_version": "1.0",           // §4a(6) 可解析义务
  "dispute_id": "DSP-YYYYMMDD-NN",
  "artifact_sha256": "...",
  "l1_record_ptr": "<L1 输出 JSON 落板指针>",
  "l2_record_ptr": "<L2 输出 JSON 落板指针>",
  "ts_open": "<UTC>",
  "dispute_resolver": "判定席/<具体承审席次>",   // §4a(3)：resolver=判定席独占
  "dispute_timeout_ms": 604800000,               // 缺省 7 天；收紧波次官可定，放宽须判定席批准
  "default_action_on_timeout": "escalate",       // ∈ {hold, demote, escalate}，缺省 escalate
  "status": "open",                              // open | resolved；解除仅由 resolver 显式裁决
  "resolution_ptr": null,                        // 解除时指向裁决书（§4a(3)：裁决书与争议登记配对落板）
  "timeout_frozen": false,                       // §7a/②§8(1)：BLOCKED 耦合挂起时计时冻结并留痕
  "freeze_log": [] }                             // 计时冻结/解冻事件留痕
```
**配套规格要点**（成文入 spec，不实施）：(i) 进入条件 = 仅 §4 分歧裁决触发（含一方 unsupported 之边界分歧）；(ii) 冻结/不冻结范围枚举照录 §4a(2)；(iii) 解除禁隐式（§0.1 默认拒绝律）；(iv) L0 锁正交互不豁免（§4a(4)）；(v) hold 延期上限 2 次后强制 escalate（§4a(3)）；(vi) 册为 append-only，禁止改写既有登记（R25 回执链纪律，§4a(5)）。
**验收判据（可机检）**：
1. 模板 8 字段 + schema_version 全必填，缺任一键即不合规；2. `dispute_timeout_ms` 缺省值恰 604800000；3. `default_action_on_timeout` enum 恰 {hold,demote,escalate}；4. `dispute_resolver` 以「判定席」前缀锚定（resolver 独占性机检钩）；5. 册内 dispute_id 唯一且单调可排序；6. status=resolved 条目必须 resolution_ptr 非空。
**依赖与冻结点**：依赖 = 判定席席位指派（草案 §8 Q3：resolver 承审席次与缺省值裁定——**未决，见 §6**）；规格成文 A 级，册本体启用与首次开庭触发属 P3 配套（§6 P3 B 级，按既有冻结点纪律挂起）。

## 4. P0-4 §4a(6) 30 天补录条款执行清单（legacy 映射）
**义务本体**（§4a(6)）：历史 DISPUTED 记录（含条款生效前以自由文本记于板面者）在生效后 30 天内补录为结构化条目或附 legacy 映射指针，保证任意时点争议史可重放审计。
**执行清单（设计，不实施）**：
1. **扫描范围**：(a) vci-inbox `board/` 全板面（重点：LAB-CLOSE 系列、FINDING-20261010-04 附带确权记录、EXT09 判定记录 LABJUDGE-EXT09-R1-RECORD-01 及其后续 R2/R3 件）中含 L1/L2 双器分歧、DISPUTED、争议停层语义之段落；(b) vci-ledger 追记板面（追记33/追记36 及 EXT-WAVE 系列）同类语义段落；(c) `board/r26fix-stress-matrix-01.manifest.yaml/json` 波次裁决格中争议备注字段。
2. **补录格式**（二选一，§4a(6)）：(i) 结构化条目 = P0-3 字段集全填（l1_record_ptr/l2_record_ptr 无对应物者以 legacy 源段落指针占位并标注 `legacy:true`）；或 (ii) legacy 映射指针条目 = {schema_version, dispute_id, legacy_ref:<板面文件+节锚>, mapped_fields:<可映射字段子集>, unmapped_fields:<无法映射字段清单>, ts_register}。
3. **完成判据（可机检）**：(a) 扫描产出候选段落清单（含命中词证据指针）100% 处置——每条要么转结构化条目、要么挂 legacy 映射、要么登记「非 DISPUTED 语义」排除理由；(b) 补录册可用 P0-3 同一解析器全量解析无异常（§4a(6)/§4b 共用解析器纪律）；(c) 30 天计时起点 = 草案生效日落板登记，终点由枢线复核签认；(d) 补录动作 append-only，原自由文本不删不改（§4a(5) 登记事实效力不撤销）。
4. **承担方**：草案 §8 Q5（补录义务由枢线哪席承担）**未决**——计划先行成文，启动以 Q5 裁定为前提；若裁定逾期，枢线波次官代行并留痕待追认。

## 5. 接口点（预留，不重复实现）
**与 ②cache-anchor 案 v0.3 的接口**：
- B7 事件面（②§2.4 B7 / ③§4a(5) 镜像条款）：DISPUTED 裁决为追溯中止/降级（demote 或 resolver 裁决推翻）时，登记册须产生机器可读事件条目 {dispute_id, artifact_sha256, action∈{demote, rescind}, ts}，作为 ②侧 B7 触发器的输入面。P0 仅在 spec 中预留 `b7_event` 追加字段位与事件序列号规则；**事件发射器与 ②侧作废执行均不在 P0**。
- 定序面（②§8 / ③§7a）：登记册 `timeout_frozen`/`freeze_log` 字段即定序规则 1（环境层先于检查层、计时冻结留痕）的承载点；BLOCKED 状态本体由 ②案侧登记，本册不复制，仅存挂起事实与指针。
**与 WS-27 核查器的接口**：
- WS-27 只做 ②案核查器（B1–B7 逐项排除核查）。本计划为其预留的**只读消费接口**：(i) DISPUTED 登记册的稳定 JSON 路径与 schema_version 钉定（消费方遇高 major 拒绝消费并登记 unsupported_schema，§4b）；(ii) B7 事件查询面（按 artifact_sha256 反查 open/resolved 争议及其 action）。本计划**不实现**任何核查逻辑、不替 WS-27 定义 B7 判定细则（属 ②案 §2.4 条文本体）。

## 6. 风险与未决项（如实列出）
- **U1 判定席席位/签认人选未定**：草案 §8 Q3（resolver 承审席次、缺省 7 天与 hold 上限 2 次之裁定）与 Q5（30 天补录承担席）悬而未决；**外部签名人选未定**（争议裁决书的外部核验面/签认人无任何提名在册）——P0-3 模板 resolver 字段仅能以前缀锚定占位。
- **U2 草案生效时点**：计划所述「30 天计时起点」以草案正式生效日为准；v0.3 虽已 EXT09 11/11 过，生效回填程序（②案 §7 同款双轮后回填纪律）是否对③案有独立回填件，板上未见，待枢线确认。
- **R-A 术语混淆**（草案 §9 R1）：本案 L0–L2 堆叠层号 vs EXT01 路线 L1–L4，登记模板与 schema 注释中须持续标注隔离。
- **R-B schema 双轨**：P0-2 schema 成文后至 P1 终审（B 级挂起）期间存在「规格先行、终审未至」窗口——窗口内任何 runner 不得据未终审 schema 采信 L1/L2 输出（§0.1 默认拒绝律）。
- **R-C 补录扫描召回率**：自由文本 DISPUTED 记录无固定命中词，扫描可能漏召——缓解：候选清单 + 人工复核双轨，漏召段落一经发现追加补录（append-only 兼容）。
- **R-D demote 滥用通道**（草案 §9 R6）：demote 仅降级口径不销争议；P0-3 spec 已把「争议登记保留且可再升级」写成机检判据 6 的配套不变量。
- **R-E 跨案死锁**：②BLOCKED × ③DISPUTED 定序（§7a/②§8）依赖两案条文镜像一致；两案条文冲突时以判定席裁定为准（③§7a 原文），本计划不新增第三套定序。

## 7. 不做事项（纪律边界）
1. 不创建任何 schema/登记册/脚本本体（P0 实施属后续波次，本文仅设计）；2. 不触碰 WS-27 领域（②案核查器实现、B7 判定细则）；3. 不实施 P1–P4 任一 B 级动作（复跑、Lean4Lean 探针、配对常态化、OBL-A1 状态迁移——均按既有冻结点纪律挂起）；4. 不修改草案 v0.3 与 ②案 v0.3 原文一字。

—— 枢/PIVOT-01 · 执行分机 WS-30 · 2026-10-12 · mirror-surge
