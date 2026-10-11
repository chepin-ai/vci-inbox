CLASSIFY: L1
# CACHE-ANCHOR-CLAUSE-DRAFT-01 · cache-anchor 域限条款（候选案 v0.3 · EXT09-R2B 修订）
枢/PIVOT-01 修订分机 WS-24 · 2026-10-12 · 原版 WS-18 @v0.1 · 自治 A 级（纯成文，零执行）
状态：**候选案 v0.3，未生效**。v0.2 经 EXT09-R2/R2B 判定（10 pass / lvlu 检查点4 单点 fail）；本版按 lvlu-R2B 单点异议补 §2.4 B7 跨案显式衔接条款，供 R3 单线复判。生效路径见 §7（双轮律 → 通过后回填 manifest v1.2）。

## 修订记录
- v0.1（WS-18 · 2026-10-11）：首版候选案。
- v0.2（WS-24 · EXT09-R1 修订）：**制度级重写**。新增 §0.1 判定语义总则（默认拒绝律）；§2 裁决语义重写（BLOCKED 优先于 DONE、缺省态 PENDING、DONE 显式合取+时效字段）；新增 §2.4 BLOCKED 触发器优先级与退出路径；新增 §2.5 fallthrough 存在性证明；新增 §3.1 锚反自指条款；§3 扩为机器可强制的 anchor_only 标注+否定例清单+污染失效路径；新增 §3.3 基础设施抖动/不可信二分；新增 §8 与 A1-STACK DISPUTED 跨案耦合条款。文末附「R1 异议处置表」。
- v0.3（枢线 · EXT09-R2B 修订）：§2.4 新增 B7 触发器（anchor 经 ③§4a 追溯降级/推翻 ⇒ 条目即时作废、回 PENDING 重走 §2 主链）+ 表后显式跨案衔接句，镜像登记于 ③§4a(5)。闭合 lvlu-R2B 检查点4。

## 0. 立项依据
- **出处**：vci-ledger 追记8（WQ-C44）——qfa 闭环表 #6 格闭、#5「cache-anchor 结构性」被推入依赖议题后未开庭，5/6 收尾。本草案即 #5 之开庭成文。
- **先例锚（G6 fallthrough）**：vci-inbox `board/r26fix-stress-matrix-01.manifest.yaml` v1.1.1——G6 格 mathlib@9fe29c4b 官方 cache 缺 4157/8936（ltar 404），按 fallthrough 规则如实记 cold-fallthrough DONE：格保持 hot 标 + fallthrough 备注，裁决按 cold 等价记，未执行编译（build_exit_code=null，runner=pivot-01-extwave05，result_commit 75f80054）。
- **实证旁证**：vci-cache-relay 中继仓（Mathlib cache 442MB+835MB release，dormant，FINDING-20261010-04 附带确权在册）为缓存缺口之基础设施级旁证；R25 实证缺口横跨 pin±3s ~ +1.28h。
- **先例缺口**：G6 记法当时仅有格内 `fallthrough_rule` 单行规则，无制度级条款背书；「何时可记 DONE / 必须记什么 / 何时必须记 BLOCKED」无成文边界——本草案补此结构性缺口。

## 0.1 判定语义总则（默认拒绝律 · EXT09-R1 共性原则）
1. **默认拒绝**：本条款下一切裁决格，**缺省状态 = PENDING**；未经显式满足放行条件，禁止落入 DONE。放行是「证明没问题」，不是「没发现问题」。
2. **禁止缺席推理**：「未观察到 BLOCKED 触发」「未发现问题」「核验无异常返回」均不构成 DONE 依据；DONE 仅能由 §2.3 显式合取条件之**正证据**（存在性核验记录、哈希、日志序号）推出。
3. **互斥与优先级**：DONE 与 BLOCKED 互斥；**BLOCKED 优先于 DONE**——任何 DONE 判定之前，判定程序必须逐条显式核查 §2.4 全部 BLOCKED 触发器并输出「未触发」的**逐项证据**（非空结论须附核验记录指针）；任一触发器命中或核查无法完成，状态直接落 BLOCKED，不得进入 DONE 判定。
4. **状态机**：PENDING →（显式合取满足 ∧ BLOCKED 逐项排除）→ DONE；PENDING →（任一 BLOCKED 触发）→ BLOCKED；BLOCKED →（§2.4 退出路径重验通过）→ 回到 PENDING 重判。**禁止 PENDING→DONE 的隐式跃迁，禁止 DONE→任何状态的静默改写**（DONE 一经落定仅可由判定席复议撤销，撤销留痕）。

## 1. 定义（精确口径）
- **缓存锚（cache anchor）**：以「指定 rev 之依赖缓存制品（mathlib ltar 等）在缓存源中可获取」为唯一事实依据、对「构建环境可复现性」作出的锚定性断言。缓存锚的证据本体 = 缓存制品的存在性/完整性核验记录（HTTP 状态、计数比 m/N、哈希），**不含任何编译结果**。
- **冷构建（cold build）**：目标 rev 之依赖缓存覆盖率为 0/N（官方 cache 与中继仓均无命中）时，从 import 闭包源码全量构建的执行模式（先例：R25 v9 终局 48min 构建 + 20s 编译）。冷构建产出的是**编译裁决证据**（rc、错误行普查、日志摘要），非缓存锚证据。
- **热验证轨（cache-hit track）**：目标 rev 缓存覆盖率 m/N 且 m>0（全命中为 m=N）时，缓存制品就位后执行的增量编译验证。产出编译裁决证据，其环境等价性由缓存锚+编译证据双重支撑。
- **fallthrough（坠落记法）**：裁决格声明 hot 而缓存锚核验实报 0/N 时，不执行编译，按本条款 §2.3 将裁决等价记为 cold 档位的成文化记法。fallthrough 是**记法降级**，不是执行替代，不产生编译证据。
- **PENDING（缺省挂起态）**：裁决格已立案但放行条件未获正证据满足、且 BLOCKED 逐项排除核查未完成时的持存状态。PENDING 不携带任何「趋向 DONE」的语义。

## 2. 两轨裁决与状态机
### 2.1 cache 命中轨（热验证）
- 前置核验：缓存锚核验 m/N>0，记录制品清单哈希与来源（官方 release / vci-cache-relay）及采集时刻。
- 执行：增量编译，记录 rc、wall、log_digest。
- 裁决：rc=0 且 §2.4 BLOCKED 逐项排除完成 → DONE（热验证）；rc≠0 → FAIL（编译裁决，不得转 fallthrough）。serial_policy `rc_nonzero_continues` 兼容。
- 部分命中（0<m<N）：按热验证执行，但证据必须登记覆盖率 m/N；覆盖率本身不构成降级理由。

### 2.2 cache 缺失轨（cold-fallthrough 记法成文化）
fallthrough 申请自 PENDING 发起；发起即触发 §2.4 BLOCKED 逐项排除核查，核查未完成前不得进入 DONE 判定。

### 2.3 允许记 DONE 的显式合取条件（消除 AND/OR 歧义）
**DONE ⟺ (C1 ∧ C2 ∧ C3) ∧ C4（时效成立）**。四条件全部为**必须同时成立**的合取项，无任何析取豁免；任一条件证据缺失或不可核验，合取不成立，维持 PENDING 或落 BLOCKED（视 §2.4）。
- **C1（双源核验实报）**：格声明 run_mode=hot 且缓存锚核验实报 0/N（双源核验：官方 cache + vci-cache-relay，计数与 404 样本落证据，含采集时刻 ts_collect）。
- **C2（等价依据存在性）**：同 manifest 内至少一格同 rev（或同 artifact）已完成 cold 或 crosscheck 编译裁决且 rc 共识成立（G6 先例：G1 cold DONE rc=0 + ucif2/vinf 双独立 runner CROSSCHECK_OK + log_digest 字节级一致）。等价依据格指针为必填字段，空指针即 C2 不成立。
- **C3（记法完整）**：格保留 hot 标并附 fallthrough 备注，裁决字段显式标 `cold-fallthrough`，`build_exit_code=null`；证据链含 result_commit 指针；§2.5 fallthrough 存在性证明条目就位。
- **C4（时效成立）**：`ts_collect` 距裁决时刻不超过 **TTL = 86400s（24h）**，且核验所用源端 epoch（官方 cache release tag / 中继仓 manifest etag）与登记 `anchor_epoch` 一致。TTL 超时或 epoch 漂移 ⇒ C4 不成立，须重验后方可再判。**时效字段（`ts_collect`/`anchor_epoch`/`ttl_s`）为必填项，缺字段视同 C4 不成立**。

**(b) 必须记录的证据字段**：rev_hash、run_mode=hot(fallthrough)、toolchain_version、env_hash、build_exit_code=null、cache 覆盖计数 0/N 与双源核验记录（含 ts_collect、anchor_epoch、ttl_s）、等价依据格指针（同 rev cold/crosscheck 格 id + rc）、verdict=cold-fallthrough、paired_run_id、fallthrough 事件日志序号（§2.5）。qlv 八字段兼容：build_exit_code 以 null 占位并在 verdict 承载 fallthrough 语义。

### 2.4 BLOCKED 触发器（优先级序 · 可恢复性 · 退出路径）
以下触发器按**优先级从高到低**排列；判定程序按序逐项核查，任一命中即落 BLOCKED 并停止后续核查（高优先级遮蔽低优先级，登记最高优先级命中项）。每项附 `recoverable` 与 `retry_after` 缺省值。

| 优先级 | 触发器 | recoverable | retry_after（缺省） | 说明 |
|---|---|---|---|---|
| B1 | 核验对象属 §5 结构不可验证族 | false | — | fallthrough 不适用，转 §5 接口，非重试可解 |
| B2 | 锚完整性失败：制品哈希不符 / 源端 epoch 漂移疑似重指向 | false（本轮） | 重锚波次 | 不可信事件（§3.3），阻断并上报判定席 |
| B3 | C2 等价依据缺失：同 rev 无任何已完成编译裁决格或 crosscheck 共识 | true | 依赖波次完成后重验 | fallthrough 失去等价依据，禁止以「cache 缺」单方记 DONE |
| B4 | 双源不可达：官方 cache 与中继仓均不可达（核验本身无法完成） | true | 3600s 指数退避（上限 4 次） | 基础设施抖动（§3.3），重试路径 |
| B5 | 格声明 run_mode=cold 而执行方以 cache 缺为由请求跳过 | false | — | cold 之本义即无 cache 构建；执行或维持 BLOCKED |
| B6 | C4 时效失效（TTL 超时 / anchor_epoch 不一致） | true | 立即重验 | 重验通过回 PENDING 重判 |
| B7 | anchor 经 ③§4a DISPUTED 追溯降级/推翻（信任源失信/失效） | false（本轮） | 重锚波次 | 跨案显式衔接：命中即关联缓存条目即时作废、回 PENDING 重走 §2 主链，并上报判定席 |

**显式跨案衔接**：anchor 被 ③§4a 追溯降级或推翻即命中 B7（信任源失信/失效），关联缓存条目即时作废并回 PENDING 重走 §2 主链；该衔接镜像登记于 ③§4a(5)。

**退出路径（BLOCKED → 重验 → PENDING → DONE/拒绝）**：
1. BLOCKED 登记必须含：触发器编号（B1–B6）、recoverable、retry_after、命中证据指针、登记时刻。
2. `recoverable=true` 者：到达 retry_after 后执行重验（重新核验或补齐依赖证据），重验输出新证据 → 状态回 PENDING，按 §2.3 重新判定；重验仍触发同一或更高优先级触发器 → 维持 BLOCKED，retry_after 按退避表递增；B4 退避 4 次用尽 → 转 `recoverable=false` 处理并上报。
3. `recoverable=false` 者：不得自动重试，仅可经判定席裁决（改案、转族登记、或拒绝并归档）退出；拒绝须留痕。
4. **禁止路径**：BLOCKED 禁止直达 DONE（必须经 PENDING 重判）；禁止以重试覆盖原 BLOCKED 登记（新证据追加，旧登记保留，R25 回执链纪律）。

### 2.5 fallthrough 存在性证明（区分「未发生」与「发生但未记录」）
- **事件日志**：每次 fallthrough 判定（无论 DONE/BLOCKED/拒绝）必须向波次板面追加一条事件记录，含**单调递增序号 seq**、裁决格 id、判定结果、证据指针、ts。序号由板面单一写入方分配，禁止跳号；跳号即异常事件。
- **存在性判据**：对任一声称「未发生 fallthrough」的格，其判据 = 事件日志中不存在以该格 id 为主体的记录 ∧ 序号连续（无跳号空洞）；两条件缺一，「未发生」之声称不成立，该格不得进入 DONE——**「未记录」视同「可能已发生」，按默认拒绝律处理**。
- 审计接口：任何复核方可按 (格 id, seq 区间) 重放事件日志；日志缺失或序号断裂的波次，其全部 fallthrough DONE 追溯降回 PENDING 待重判。

## 3. 域限：缓存锚证据的有效域（机器可强制版）
- **有效域 = 环境等价性断言，且仅限于此**。缓存锚可支撑：「该 rev 之依赖制品在此环境可得/不可得」「两 runner 环境制品级一致（log_digest 字节级一致 = 确定性编译强信号，追记8 定谳）」。
- **缓存锚 ≠ 内容认证**。缓存制品的存在性不蕴涵、不增强、不削弱被编译对象的数学内容真值；内容认证的唯一通道是编译裁决证据（rc + 错误普查 + 公理审计）与独立复跑共识。

### 3.1 anchor_only 强制标注（机器可强制）
- 一切缓存锚派生证据（核验记录、覆盖率、制品清单哈希、cache_fp）在落板时必须携带机器可读标注 `evidence_class: "anchor_only"`。缺标注的记录视为格式不合规，判定程序拒绝受理（默认拒绝律适用）。
- 判定/回填程序硬性校验：凡 `evidence_class=anchor_only` 之记录出现在任何 verdict 的**内容认证依据字段**中，即判违规，该裁决自动落 BLOCKED（B2 同级）并登记违规事件。

### 3.2 否定例清单（禁止把缓存锚当内容证据的场景，枚举即禁令）
以下场景**显式禁止**以缓存锚（含覆盖率、制品哈希一致性、双源可达性）充任或暗示内容证据：
1. 禁止以 cache 命中作为「已验证/定理成立」的简称证据（任何 verdict 内容字段引用 anchor_only 记录即违规）；
2. 禁止以 cache 缺失作为「内容可疑/定理不成立」的反向证据（R25 定谳：cache 缺口是基础设施级诚实缺口，与随件编译失败是两层事实，G6 与 v9 双格已分立承载）；
3. 禁止以双源 0/N 核验本身支撑 fallthrough DONE（§2.3 C2 独立要求等价编译依据）；
4. 禁止以 anchor_epoch 一致性断言制品内容未被篡改后的语义正确性（epoch 一致仅证可得性时序，不证内容）；
5. 禁止在 Hexagon 文稿及任何对外口径中以 cache 指纹支撑数学结论。
- 清单为**可增录封闭集**：增录走判定席；未列场景不自动豁免，遇疑似越域引用按默认拒绝律先停后审。

### 3.3 基础设施抖动 vs 不可信（二分处置）
- **抖动（暂不可用）**：HTTP 超时、5xx、网络分区、relay dormant 未唤醒等**无完整性矛盾**的不可达 → 对应 B4，`recoverable=true`，走重试退避路径，不作安全结论。
- **不可信（阻断）**：制品哈希与登记不符、源端 epoch 非预期漂移、tag 重指向（FINDING-20261010-04 附带确权先例：leancert tag 远端重指向）、清单与计数自相矛盾等**完整性矛盾** → 对应 B2，`recoverable=false`（本轮），立即阻断并上报判定席，禁止重试自愈。
- 判别义务：核验程序必须区分两类并如实分类登记；**无法归类时按不可信处理**（默认拒绝律延伸至分类不确定性）。

### 3.4 锚污染时的失效/降级路径与责任方
- **污染定义**：缓存源制品被重指向、替换、或清单哈希与历史登记不一致（§3.3 不可信事件坐实）。
- **失效路径**：污染坐实 → (i) 该 `anchor_epoch` 及其后继 epoch 下全部 anchor_only 证据即时失效（标记 `invalidated_by: <污染事件 id>`）；(ii) 依赖失效证据的 PENDING 格维持/落 BLOCKED；(iii) 依赖失效证据的 DONE 格追溯降回 PENDING 并在板面公示重判队列。
- **降级路径**：可切换至备用源（官方 ↔ relay 互换）重锚，重锚产物分配新 `anchor_epoch`，旧 epoch 证据不自动迁移；无备用源则该 rev 进入 cold-only 模式（fallthrough 关闭，仅冷构建可产 DONE）。
- **责任方**：污染事件的检测与登记 = 执行 runner（核验程序）；失效标记与降级切换 = 枢线波次官；污染根因确权与重锚授权 = 判定席。三方动作均须落板留痕，缺一环则失效流程不闭合、相关格一律维持 BLOCKED。
- **锚反自指条款**：**锚不可被自身缓存结果所锚定**。任何 `anchor_epoch` 的合法性必须由**独立于该缓存制品本身**的证据支撑（源端签名/发布记录、独立采集的双源交叉核验、或判定席确权条目）；禁止以「制品自述的清单/哈希/元数据」作为该制品自身的锚定依据。检测到自指锚定（证据链闭环于被锚对象自身）即按 B2 阻断并登记违规。

### 3.5 禁止延伸条款（保留 v0.1 §3 纪律）
(i) 禁止以 cache 命中作为「已验证」的简称证据；(ii) 禁止以 cache 缺失作为「内容可疑」的反向证据；(iii) fallthrough DONE 之本体价值 = 实证 pin 无 cache（manifest G6 `fallthrough_rule` 原文），不升格为内容裁决。——本条与 §3.1–3.2 并存，§3.1 为机器强制层，本条为语义层。

## 4. 判别顺序
先查结构不可验证族登记册（§5 FINDING 接口），在册者直接 B1 BLOCKED 转 §5；不在册者进入 §2 状态机（PENDING 起步）。

## 5. 与 FINDING-20261010-04（CIRC 结构性）的接口
- FINDING-20261010-04 定谳：CERT-CIRC-LEAN-01 族在自身钉定 leancert v4.34.1 下**结构性**不可验证（checkADSupported 自 4bf84ea91 起不含 Expr.log，11/11 按设计拒证；Matrix.det Leibniz 定义组合爆炸），认证承载层实为 Python 区间算术。
- **条款**：凡经 FINDING 定谳为结构不可验证族（检查器按设计拒证，非环境、非资源、非漂移问题）者，**不适用 fallthrough**——其「无法编译验证」不源于 cache 缺失，坠落记法无的放矢；此类族之裁决只能走：(i) 内容级重构（log 消除化归支持域）后重新验证；或 (ii) 如实登记非 Lean 认证承载层（Python 区间认证口径），并禁止以任何 fallthrough/cold 等价记法冒充机器验证证书。

## 6. 风险点
- R1：C2 等价依据门槛可能使孤立单格 manifest 无法使用 fallthrough——此为有意设计（默认拒绝律），缓解 = 先补 cold/crosscheck 格，不放宽 C2。
- R2：双源核验中 vci-cache-relay 为 dormant 设施，可达性非常备——B4 覆盖（抖动重试，4 次用尽上报）。
- R3：上游 tag 漂移提示缓存源本身可漂移——C4 时效字段 + §3.3 不可信分类 + §3.4 失效路径三重覆盖。
- R4：术语风险——「cold 等价记」易被误读为「等同冷构建已执行」；§1/§3.5 双重锁死：fallthrough 不产生编译证据。
- R5：事件日志单一写入方为单点——缓解：写入方标识落板，跳号即异常（§2.5），多 runner 波次须指定唯一日志写入方。

## 7. 生效程序
1. 本候选案提交判定席，**双轮律**：首轮全量判定卡；undecided/fail 残差按收敛条件补强后次轮复投（FM-021 多轮主卡序列先例）。本 v0.2 即 EXT09-R1 残差补强版，供 R2 复投。
2. 双轮通过后：回填 `board/r26fix-stress-matrix-01.manifest.yaml` 为 **v1.2**——G6 格增 `clause_ref: CACHE-ANCHOR-CLAUSE-01 v1.0` 指针、`supersedes: 1.1.1`、roundtrip_hash 重算（yaml↔json 结构等价规则不变）；v1.1.1 原文保留不改。
3. 回填 commit 与判定闭合登记（LAB-CLOSE 格式）同波落板；条款编号 CACHE-ANCHOR-CLAUSE-01 v1.0 于回填时解冻生效。

## 8. 跨案耦合条款：与 A1-STACK-UPGRADE DISPUTED 的定序（usrm 异议）
- **交互面**：本条款之 BLOCKED（尤其 B2 不可信阻断）与 A1 堆叠案之 DISPUTED（双器分歧停层）可能同时悬置同一工件的裁决链；不定序则存在死锁（L1 等 L2 解停、L2 等 L1 解停；或 fallthrough 重验等 DISPUTED 解停、DISPUTED 仲裁等环境重验）。
- **定序规则**：
  1. **环境层先于检查层**：凡同一工件同时存在本条款 BLOCKED（B2/B4）与 A1 DISPUTED，先解 BLOCKED（环境事实未立，检查层分歧无判定基面）；BLOCKED 退出前，DISPUTED 仲裁程序挂起但**不解除**（争议登记保留，时限计时暂停 `dispute_timeout_ms` 冻结）。
  2. **DISPUTED 不豁免 BLOCKED 核查**：DISPUTED 停层期间，若本条款触发器新命中（如 C4 时效失效），BLOCKED 照常登记，两层状态独立持存、并行可见。
  3. **循环等待禁令**：禁止任何条款以「等待对方状态解除」为唯一退出条件；双方退出路径（§2.4 与 A1 案解停机制）必须各自含**不依赖对方的超时/上报通道**（本案 B4 退避用尽上报判定席；A1 案 `default_action_on_timeout`）。判定席为唯一公共汇合点，死锁检测 = 任一状态持存超过其 timeout 且对方亦无进展时，由先超时方上报。
  4. 状态组合合法集：{PENDING, DONE, FAIL, BLOCKED} × {无争议, DISPUTED} 全部八组合合法，但 (DONE, DISPUTED) 仅允许「向下冻结已生效」形态存在（见 A1 案 §4a 传播条款），禁止新 DONE 在 DISPUTED 未解时落定。

## 9. 给判定席的关键问题（R2 开庭题面）
- Q1（保留）：C2「同 rev 已有编译裁决共识」门槛在本版已按默认拒绝律坐实为合取硬条件，R2 请裁定是否维持。
- Q2（保留）：部分命中（0<m<N）维持 §2.1「按热验证执行+登记覆盖率」从简？
- Q3（保留）：§5 结构不可验证族登记册的维护权与增录程序归谁？
- Q4（保留）：本条款生效后溯及既有 G6 记法（建议：溯及确认，G6 为先例锚不改动，仅增 clause_ref 指针）？
- Q5（新增）：TTL=86400s 与 B4 退避上限 4 次之缺省值是否合适，抑或应由波次官按 manifest 粒度覆写？

## R1 异议处置表（EXT09-R1 · 案② 逐条）
| # | 异议（来源线） | 处置 | 所在章节 |
|---|---|---|---|
| 1 | DONE/BLOCKED 互斥与优先级，DONE 判定前须显式排除全部 BLOCKED 触发（cfts/ucif2/usrm/lgt） | 采纳：互斥+BLOCKED 优先成文，DONE 前置逐项排除核查并要求逐项证据 | §0.1(3)(4)、§2.3 引言 |
| 2 | 默认态=BLOCKED 或 PENDING，严禁默认放行（cfts/lvlu） | 采纳：缺省=PENDING，默认拒绝律总则化，「没发现问题≠证明没问题」明文禁止缺席推理 | §0.1、§1 PENDING 定义 |
| 3 | DONE 四条件消除 AND/OR 歧义，写显式合取 + TTL/epoch 时效字段（lgt） | 采纳：DONE ⟺ (C1∧C2∧C3)∧C4，新增 C4 时效项（ts_collect/anchor_epoch/ttl_s 必填，TTL 缺省 24h） | §2.3 |
| 4 | BLOCKED 触发器加优先级序 + recoverable + retry_after + 退出路径（lgt/ucif2） | 采纳：B1–B6 优先级表含 recoverable/retry_after 缺省；退出路径 BLOCKED→重验→PENDING→DONE/拒绝成文，禁止直达与覆盖 | §2.4 |
| 5 | fallthrough 存在性证明：事件日志+序号区分「未发生」与「未记录」（ucif2） | 采纳：事件日志+单调 seq，序号断裂则「未发生」不成立且追溯降级 | §2.5 |
| 6 | 锚反自指条款（ucif2） | 采纳：锚不可被自身缓存结果锚定，自指检测即 B2 阻断 | §3.4 末段 |
| 7 | 「缓存锚≠内容认证」机器可强制：anchor_only 标注+否定例清单+污染失效/降级路径与责任方（qtlv/lgt/cfts/lvlu） | 采纳：§3.1 强制标注+违规自动 BLOCKED；§3.2 五条否定例封闭清单；§3.4 失效/降级路径+三方责任分工 | §3.1–§3.4 |
| 8 | 区分基础设施抖动（重试）与不可信（阻断）（cfts） | 采纳：二分定义+判别义务+无法归类按不可信处理，分别映射 B4/B2 | §3.3 |
| 跨案 | ②BLOCKED 与 ③DISPUTED 交互定序防死锁（usrm） | 采纳：环境层先于检查层、计时冻结、循环等待禁令、判定席为公共汇合点 | §8 |

—— 枢/PIVOT-01 · 2026-10-11 · v0.3 供 EXT09-R3(lvlu 单线)复判（v0.2 WS-24 · v0.1 WS-18）
