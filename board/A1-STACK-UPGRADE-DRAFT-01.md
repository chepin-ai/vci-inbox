CLASSIFY: L1
# A1-STACK-UPGRADE-DRAFT-01 · A1 检查器堆叠升级案（草案 v0.3 · EXT09-R2B 修订）
枢/PIVOT-01 修订分机 WS-24 · 2026-10-12 · 原版 WS-18 @v0.1 · 自治 A 级（纯成文，零执行）
状态：**草案 v0.3，未生效**。v0.2 经 EXT09-R2/R2B 判定（10 pass / lvlu 检查点4 单点 fail）；本版按 lvlu-R2B 异议在 §4a(5) 增跨案显式衔接（指向 ②§2.4 B7），供 R3 单线复判。各阶段自治分级见 §6；涉 B 级动作（外部资源/root 边界）按既有冻结点纪律执行。

## 修订记录
- v0.1（WS-18 · 2026-10-11）：首版草案（L0 确权 + L1/L2 契约 + 分阶段计划）。
- v0.2（WS-24 · EXT09-R1 修订）：新增 §0.1 默认拒绝语义总则；§4 分歧裁决扩为 §4a DISPUTED 状态机专节（传播方向、解停机制 dispute_resolver/dispute_timeout_ms/default_action_on_timeout、L0 锁正交、回溯效力、冻结范围明示）；§3/§4 契约增 schema 版本化与兼容策略（旧 DISPUTED 记录可解析义务）；新增 §7a 与 cache-anchor 案 BLOCKED 的跨案耦合定序条款。文末附「R1 异议处置表」。
- v0.3（枢线 · EXT09-R2B 修订）：§4a(5) 新增跨案显式衔接——追溯中止/降级 ⇒ cache-anchor 侧条目命中 ②§2.4 B7、作废回 PENDING 重走 §2 主链。闭合 lvlu-R2B 检查点4。

## 0. 立项依据
- **追记33 / LAB-CLOSE-EXT01（2026-10-09）**：检查器堆叠五级现实确权——C++ 内核 → lean4checker（内置）→ Lean4Lean（TYPES 2025，已抓 1 个内核 soundness bug）→ comparator → SafeVerify；A2（检查栈终止，FK-01R 状态 assumed）可升级。LABJUDGE-EXT02 11/11 pass，Q3 附条件 (iii)：**A1/T2a 的 discharged-by-classical 缺口另计**——复用外部制品不自动闭合内核缺口。
- **追记36（EXT-WAVE-04，2026-10-10）**：L0 已完成——CERT-SELFCHECK-01（vci-inbox `artifacts/lean-verified/CertSelfCheck01.lean` @f8cb83e7）：accept⟹correct 最小可信核 4 定理（add_sound / neg_sound / check_sound / end_to_end）Axle verify_proof 全过（request d9034a05 / 44208d46 / 082321e6 / f3c1fc61），公理审计仅 [propext, Classical.choice, Quot.sound]，无 sorryAx。
- **缺口本体**：FK-01R v1.1 A1「检查器可靠性接口」V(φ,D,π)=accept ⟹ φ 在 D 上成立，状态 discharged-by-classical（区间算术外向舍入包含性 / Krawczyk 定理 / LP 弱对偶三层经典背书）；其证明助手形式化为开放义务 OBL-A1，未闭合。
- 本草案为 OBL-A1 清偿的制度成文：把「检查器自证核（L0）→ 内置检查器复跑（L1）→ 外部独立检查器（L2）」的升级堆叠契约化。

## 0.1 判定语义总则（默认拒绝律 · EXT09-R1 共性原则）
本案一切层间放行奉行「默认拒绝、显式满足才放行」：任何层（L1/L2）pass 之采信须以该层契约输出 JSON 的**正证据**（必填字段齐全、schema 版本可解析、哈希可复算）为前提；「未观察到失败」「输出无异常」不构成 pass 依据。DISPUTED 之解除同样须仲裁方显式裁决留痕，禁止以「争议未见后续」默认消散。

## 1. 术语澄清
本草案 L0/L1/L2 为**堆叠层号**（升级阶梯），与 LAB-EXT01 裁定之路线 L1–L4（leancert 复用/Rice 桥/Hexagon/Axle 通道）无关，勿混。五级现实映射：L0=自证核（联邦内生）；L1=lean4checker（内置层复跑）；L2=Lean4Lean（外检层）；L3=comparator 与 L4=SafeVerify 列入远景，本案不缔约。

## 2. L0 确权：CERT-SELFCHECK-01 为堆叠基底
- 确权：CERT-SELFCHECK-01 为 A1 堆叠的形式基底——其 4 定理构成「检查器 accept ⟹ 语义性质成立」之最小可信核（Krawczyk 式 accept⟹correct 的命题骨架），云端验证记录与公理审计已落工件 header（见 §0）。
- 基底性质声明：L0 证明的是检查器**设计正确性**（accept 语义蕴涵），不证明任何**实现正确性**（C++ 内核/lean4checker 二进制之行为）——后者正是 L1/L2 层之职责，两层不可互替。
- 基底冻结：CertSelfCheck01.lean 任何修改走新 sha 对并重新云端验证（追记7 修复法度同款：已验证 sha 对不动）。

## 3. L1 契约：lean4checker 复跑接入格式
**输入**：
- `.lean` 工件（sha256 钉定）+ 依赖 pin 清单（mathlib rev、toolchain rev）；
- 环境指纹（§6 规范）。
**执行**：lean4checker 对工件 elaboration 产物复跑内核级检查。
**输出契约**（JSON，落 vci-inbox 对应波次板面）：
```
{ "schema_version": "1.0",
  "artifact_sha256": "...", "checker": "lean4checker",
  "checker_version": "<同 toolchain>", "env_fp": "<§6 指纹>",
  "verdict": "pass|fail", "wall_s": <int>,
  "log_sha256": "<完整日志哈希>", "runner": "<runner 标识>",
  "run_id": "<CI run / request id>", "ts": "<UTC>" }
```
- fail 处理：如实登记 FAIL + 日志哈希，禁止重试覆盖（R25 回执链纪律）；fail 不升格为内容证伪，仅登记检查层事实。
- 环境未备（公共 runner 无 lean4checker 导出链）时记 BLOCKED，转 §6 阶段门。

## 4. L2 契约：Lean4Lean 外检接入与证据格式
**输入**：L1 同款工件 + 环境指纹 + L1 输出（配对审计）。
**执行**：Lean4Lean 外部检查器对工件环境导出独立重检（独立于内置内核的第二实现）。
**输出契约**（JSON）：
```
{ "schema_version": "1.0",
  "artifact_sha256": "...", "checker": "Lean4Lean",
  "checker_rev": "<pin commit>", "env_fp": "<§6 指纹>",
  "verdict": "pass|fail|unsupported",
  "axiom_audit": ["propext","Classical.choice","Quot.sound"],
  "sorryAx_present": false,
  "log_sha256": "...", "runner": "...", "run_id": "...", "ts": "..." }
```
- `unsupported` 为合法第三值：Lean4Lean 能力边界（如内部/外部定义覆盖缺口）如实登记，不视为 fail（诚实缺口律）。
- **分歧裁决**：L1=pass ∧ L2=fail（或反之）→ 记 DISPUTED，按 §4a 状态机处置；两器互搏本身是 TCB 审计最高价值事件（先例：Lean4Lean 已抓 1 个上游内核 soundness bug），禁止单方覆盖。
- 证据格式纪律：双器输出共工件 sha256 与环境指纹配对落板；公理审计字段必填（云端审计先例：无 sorryAx 为硬门）。

## 4a. DISPUTED 状态机（EXT09-R1 新增专节）
**进入**：仅由 §4 分歧裁决触发（L1 与 L2 verdict 不一致，含一方 `unsupported` 而另一方 pass/fail 之边界分歧）；登记字段 = {dispute_id, artifact_sha256, l1_record_ptr, l2_record_ptr, ts_open, dispute_resolver, dispute_timeout_ms, default_action_on_timeout}，全部必填。

**(1) 传播方向（定向传播律）**：
- **向上不传播**：DISPUTED 不影响更上层/既有的元层断言与 L0 基底确权；禁止以双器分歧动摇已完成之 L0 定理地位。
- **向下强制传播**：凡依赖该争议工件 verdict 的下层消费（后续波次以该工件 pass 为前置的核验、回填、口径升级、证书签发），在 DISPUTED 未解期间**一律冻结**；下层消费者不得越过争议层继续消费其 pass 结论（消费请求须先查争议登记册，命中即拒，默认拒绝律适用）。

**(2) 冻结范围明示**：DISPUTED 期间冻结且仅冻结——(i) 以该工件 L1/L2 verdict 为依据的新裁决落定；(ii) 该工件参与的双器配对审计结论采信；(iii) 依赖该工件的 OBL-A1 状态迁移提案。**不冻结**：该工件之 BLOCKED/FAIL 等独立状态登记、其他无依赖工件的全部流程、L0 基底的既有确权。

**(3) 解停机制**：
- `dispute_resolver`：仲裁层 = 判定席（唯一有权解停方；席位与开庭程序按判定席双轮律，双器互搏事件触发强制开庭）；角色字段在登记时指定具体承审席次。
- `dispute_timeout_ms`：缺省 604800000（7 天）；波次官可按工件关键度收紧，放宽须判定席批准。计时自 ts_open 起；若因 cache-anchor 案 BLOCKED 耦合挂起（§7a），计时冻结并留痕。
- `default_action_on_timeout ∈ {hold, demote, escalate}`（登记时必选其一，缺省 `escalate`）：
  - `hold`：维持 DISPUTED 与冻结，resolver 须出具延期理由并复位计时（最多 2 次，其后强制 escalate）；
  - `demote`：该工件之堆叠结论降级为「L1 单器通过（有争议）」口径，禁止用于任何口径升级，争议登记保留待后续复验；
  - `escalate`：上报判定席全席开庭，超时升级事件本身作为 TCB 审计条目落板。
- **解除**：仅由 dispute_resolver 显式裁决（维持一方 verdict / 双方重验 / 工件报废重发），裁决书与争议登记配对落板；解除后冻结按 (2) 范围逐项解除并留痕。禁止隐式解停（默认拒绝律）。

**(4) L0 锁与 DISPUTED 正交**：L0 基底冻结（§2 基底冻结条款，已验证 sha 对不动）与 DISPUTED 状态**正交互不豁免**——(i) 工件处于 L0 锁保护不豁免其被 DISPUTED（确权锁不豁免争议）；(ii) DISPUTED 之存在或解除均不自动解除/修改任何 L0 锁（争议不自动解锁）；L0 锁变更只能走 §2 新 sha 对重验流程，与争议流程无快捷通道。

**(5) 回溯效力**：DISPUTED 停层时，已产出的 L1/L2 证书/记录的效力规则——
- 已落板的 L1/L2 输出记录**保持其登记事实效力**（「某时刻某器报某 verdict」之事实不撤销，R25 回执链纪律：禁止抹除改写）；
- 但其**结论采信效力**追溯中止：凡在 DISPUTED 开启后、基于争议 verdict 已推进的下游动作（若因登记延迟漏冻结），一经发现即回滚至冻结点，回滚留痕；
- 争议解除后，解除前冻结期内未发生的动作按新裁决重新判定，禁止以冻结期内「本应完成」为由补办。
- **跨案显式衔接（②§2.4 B7）**：追溯中止/降级生效时，凡以被中止 verdict 或其 anchor 为依据的 cache-anchor 侧条目即时命中 ②§2.4 B7（信任源失信/失效）→ 条目作废、回 PENDING 重走 ②§2 主链。

**(6) DISPUTED 记录可解析义务**：DISPUTED 登记条目含 `schema_version`；历史 DISPUTED 记录（含本条款生效前以自由文本记于板面者）在生效后 30 天内由枢线补录为结构化条目或附 legacy 映射指针，保证任意时点争议史可重放审计（与 §4b 兼容策略共用解析器纪律）。

## 4b. L1/L2 契约 schema 版本化与兼容策略（EXT09-R1 新增）
- L1/L2 输出 JSON 首字段 `schema_version: "<major.minor>"` 必填；缺失即格式不合规，判定程序拒绝受理（默认拒绝律延伸至格式层）。
- major 变更不允许静默兼容：消费方遇高于自身支持的 major → 拒绝消费并登记 `unsupported_schema`；minor 变更（纯增字段）向后兼容，读取时以显式缺省值补全。
- 契约变更走判定席：schema major 升版须附迁移脚本与旧记录映射表；旧版记录（含 DISPUTED 登记）在冻结期内保持可解析（§4a(6)）。
- checker_rev 全 sha 钉定不变（R4 纪律），schema 版本与 checker_rev 为两个独立维度，禁止互相替代。

## 5. 环境指纹规范（env_fp）
`env_fp = sha256( toolchain_version ‖ mathlib_rev ‖ cache_fp ‖ runner_id ‖ os_image )`
- **toolchain_version**：elan toolchain 全名（例 leanprover/lean4:v4.35.0-rc2 / lean-4.28.0 云端环境名）；
- **mathlib_rev**：依赖 pin 全 sha（例 9fe29c4b379922f49446b28b76cbe4fce041c8b3）；
- **cache_fp**：缓存覆盖率 m/N + 制品清单哈希 + 来源（官方 / vci-cache-relay）+ 采集时刻（cache-anchor 域限条款 §3 纪律：cache 指纹支撑环境等价性，不承载内容认证）；
- **runner_id**：runner 标识（pivot-01 / pivot-01-extwave05 / ucif2-ebb17146 / vinf-c9ddc7e8 / axle-cloud …）；
- 指纹与 log_digest 并列登记：两独立 runner log_digest 字节级一致 = 确定性编译强信号（追记8 定谳）沿用为跨 runner 等价判据。

## 6. 分阶段实施计划与自治分级
| 段 | 内容 | 产出 | 自治级 |
|---|---|---|---|
| P0 | 本草案成文 + L0 确权登记（§2） | 本案 + SELFCHECK-01 基底登记条目 | **A**（本波即成） |
| P1 | L1 契约终审 + lean4checker 复跑首跑（对 CertSelfCheck01.lean / T2aTemplate.lean 两已验工件） | L1 输出 JSON ×2 + 日志哈希 | **B**（复跑需执行环境；契约终审走判定席双轮律） |
| P2 | L2 契约终审 + Lean4Lean 接入探针（能力边界普查：supported/unsupported 分类） | L2 输出 JSON + 边界普查表 | **B**（Lean4Lean 环境需外部机器或 Axle 自定义环境申请——追记34 root 冻结点同款边界） |
| P3 | 双器配对审计常态化 + 分歧处置规程演练（按 §4a 状态机） | DISPUTED 处置 SOP | **B**（判定席授权） |
| P4 | OBL-A1 缺口清偿评估（§7 口径）并回填 FK-01R A1 状态 | A1 状态迁移提案 | **B**（内核状态迁移必走判定席） |

## 7. 与 OBL-A1 缺口的衔接
- OBL-A1 缺口 = A1 三层经典背书（区间算术包含性 / Krawczyk / LP 弱对偶）之证明助手化未竟。本堆叠**不直接清偿**该缺口：L0/L1/L2 强化的是「检查器 accept 可信」之**机制信任链**，属 A2 侧（检查栈终止）的压实；A1 侧缺口的清偿仍依赖内容级形式化（leancert Krawczyk 证书移植 OBL-EXT-01r、duality 复用 OBL-A1c 在库件）。
- 衔接口径：堆叠升级将 A1 的「discharged-by-classical」迁移路径收窄为——(i) 自证核（L0，已成）证明检查器设计正确；(ii) L1/L2 双器互检压实实现可信；(iii) 剩余缺口 = 三层背书定理的 Lean 化，清偿判据 = 每层背书定理在库机器验证证书就位 + 公理审计干净 + 双器 pass。届时提案 A1 状态 discharged-by-classical → discharged（机器），走 P4。
- 明示不主张：堆叠完成 ≠ A1 自动闭合（LABJUDGE-EXT02 Q3 条件 (iii) 同款纪律）。

## 7a. 跨案耦合条款：与 cache-anchor 案 BLOCKED 的定序（usrm 异议）
- **交互面**：本案 DISPUTED 与 cache-anchor 案 BLOCKED（尤其 B2 不可信阻断）可能同时悬置同一工件之裁决链；不定序则存在死锁（L1 等 L2 解停、L2 等 L1 解停；DISPUTED 仲裁等环境重验、环境重验等 DISPUTED 解停）。
- **定序规则**（与 cache-anchor 案 §8 镜像一致，两案条文冲突时以判定席裁定为准）：
  1. **环境层先于检查层**：同一工件同时存在 BLOCKED（B2/B4）与 DISPUTED 时，先解 BLOCKED；BLOCKED 退出前，DISPUTED 仲裁挂起但登记保留，`dispute_timeout_ms` 计时冻结并留痕。
  2. **独立持存**：DISPUTED 不豁免 cache-anchor BLOCKED 核查，反之亦然；两层状态并行登记、互不遮蔽。
  3. **循环等待禁令**：双方退出路径必须各自含不依赖对方的超时/上报通道（本案 `default_action_on_timeout`；cache-anchor 案 B4 退避用尽上报）；判定席为唯一公共汇合点，任一状态超时且对方无进展即由先超时方上报，强制开庭解死锁。
  4. 合法状态组合与 (DONE, DISPUTED) 约束依 cache-anchor 案 §8(4) 同款执行：DISPUTED 未解期间禁止新 DONE/新 pass 采信落定。

## 8. 给判定席的关键问题
- Q1：L0 确权范围——SELFCHECK-01 作为「最小可信核」是否足以充任全堆叠基底，抑或须先扩展谓词覆盖（当前仅 ℚ 区间有界性一族）再确权？
- Q2：L2 `unsupported` 第三值与 FINDING-20261010-04 结构不可验证族接口——Lean4Lean 能力边界普查表是否并入结构不可验证族登记册统一维护？
- Q3（已部分闭合）：DISPUTED 处置的判定席席位与限期——本版 §4a(3) 坐实 resolver=判定席、timeout 缺省 7 天、强制开庭；R2 请裁定缺省值与 `hold` 延期上限 2 次是否合适？
- Q4：P2 之 Axle 自定义环境申请属 root 边界（追记34 冻结点②同款）——是否授权枢线在 root 缺席期先行备妥申请件（b+c 式：备稿+询函，不阻塞）？
- Q5（新增）：历史自由文本 DISPUTED 记录的 30 天补录义务（§4a(6)）由枢线哪席承担？

## 9. 风险点
- R1：术语混淆（本草案 L0–L2 vs EXT01 路线 L1–L4）——§1 已隔离，仍需各线引用时注意。
- R2：L2 接入依赖外部环境，root 冻结点可能长期阻塞 P2——缓解：P2 备稿部分属 A 级可先行，仅执行触 B。
- R3：双器 pass 可能被误读为「内容已认证」——堆叠压实的是机制信任链，内容认证口径不变（cache-anchor 域限条款 §3 同纪律）。
- R4：外部依赖 pin 漂移（leancert tag 重指向先例）——L2 契约 checker_rev 必须全 sha 钉定，禁 tag 引用。
- R5：云端验证（Axle）请求 id 为一次性证据，须随工件 sha 配对落板防断链（vHUB-MAIL 404 重锚先例）。
- R6（新增）：`demote` 超时下架可能被滥用为「绕过仲裁」通道——缓解：demote 仅降级口径不销争议，争议登记保留且可再升级；resolver 由判定席独占。

## R1 异议处置表（EXT09-R1 · 案③ 逐条）
| # | 异议（来源线） | 处置 | 所在章节 |
|---|---|---|---|
| 1 | DISPUTED 传播方向：向上不传播、向下强制传播（ucif2） | 采纳：§4a(1) 定向传播律，下层消费越过争议层即拒 | §4a(1) |
| 2 | 解停机制：dispute_resolver + dispute_timeout_ms + default_action_on_timeout ∈ {hold, demote, escalate}（lgt/qtlv/cfts/usrm） | 采纳：§4a(3) 三字段必填，resolver=判定席独占解停，timeout 缺省 7 天，缺省动作 escalate，hold 延期上限 2 次 | §4a(3) |
| 3 | L0 锁与 DISPUTED 正交：确权锁不豁免争议、争议不自动解锁（ucif2） | 采纳：§4a(4) 双向正交条款，L0 锁变更无快捷通道 | §4a(4)、§2 |
| 4 | L1/L2 契约 schema 版本化+兼容策略；旧 DISPUTED 记录须可解析（ucif2/qtlv/lgt） | 采纳：§4b 版本化契约（major/minor 规则+迁移义务）+ §4a(6) 30 天补录义务 | §4b、§4a(6) |
| 5 | DISPUTED 回溯效力：已产出 L1/L2 证书在停层时的效力规则（qtlv） | 采纳：§4a(5)——登记事实效力不撤销、结论采信效力追溯中止、漏冻结动作回滚留痕 | §4a(5) |
| 6 | DISPUTED 时 L1/L2 冻结范围明示（cfts） | 采纳：§4a(2) 冻结三项/不冻结三项枚举 | §4a(2) |
| 跨案 | ②BLOCKED 与 ③DISPUTED 交互定序防状态机死锁（usrm） | 采纳：§7a 镜像条款（环境层先于检查层、计时冻结、循环等待禁令、判定席汇合点） | §7a |
| 共性 | 默认拒绝、显式满足才放行 | 采纳：§0.1 总则；pass 采信与争议解除均须正证据，禁止隐式解停 | §0.1、§4a(3) |

—— 枢/PIVOT-01 · 2026-10-11 · v0.3 供 EXT09-R3(lvlu 单线)复判（v0.2 WS-24 · v0.1 WS-18）
