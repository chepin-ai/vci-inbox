CLASSIFY: L1
# CACHE-ANCHOR-CLAUSE-DRAFT-01 · cache-anchor 域限条款（候选案 v0.1）
枢/PIVOT-01 智囊分机 WS-18 · 2026-10-11 · backlog 在册项（追记8 闭环表 #5 依赖议题开庭）· 自治 A 级（纯成文，零执行）
状态：**候选案，未生效**。生效路径见 §6（判定席双轮律 → 通过后回填 r26fix-stress-matrix-01.manifest v1.2）。回填前 manifest 现行 v1.1.1 继续有效，本草案不冻结、不阻塞任何在跑裁决。

## 0. 立项依据
- **出处**：vci-ledger 追记8（WQ-C44）——qfa 闭环表 #6 格闭、#5「cache-anchor 结构性」被推入依赖议题后未开庭，5/6 收尾。本草案即 #5 之开庭成文。
- **先例锚（G6 fallthrough）**：vci-inbox `board/r26fix-stress-matrix-01.manifest.yaml` v1.1.1——G6 格 mathlib@9fe29c4b 官方 cache 缺 4157/8936（ltar 404），按 fallthrough 规则如实记 cold-fallthrough DONE：格保持 hot 标 + fallthrough 备注，裁决按 cold 等价记，未执行编译（build_exit_code=null，runner=pivot-01-extwave05，result_commit 75f80054）。
- **实证旁证**：vci-cache-relay 中继仓（Mathlib cache 442MB+835MB release，dormant，FINDING-20261010-04 附带确权在册）为缓存缺口之基础设施级旁证；R25 实证缺口横跨 pin±3s ~ +1.28h。
- **先例缺口**：G6 记法当时仅有格内 `fallthrough_rule` 单行规则，无制度级条款背书；「何时可记 DONE / 必须记什么 / 何时必须记 BLOCKED」无成文边界——本草案补此结构性缺口。

## 1. 定义（精确口径）
- **缓存锚（cache anchor）**：以「指定 rev 之依赖缓存制品（mathlib ltar 等）在缓存源中可获取」为唯一事实依据、对「构建环境可复现性」作出的锚定性断言。缓存锚的证据本体 = 缓存制品的存在性/完整性核验记录（HTTP 状态、计数比 m/N、哈希），**不含任何编译结果**。
- **冷构建（cold build）**：目标 rev 之依赖缓存覆盖率为 0/N（官方 cache 与中继仓均无命中）时，从 import 闭包源码全量构建的执行模式（先例：R25 v9 终局 48min 构建 + 20s 编译）。冷构建产出的是**编译裁决证据**（rc、错误行普查、日志摘要），非缓存锚证据。
- **热验证轨（cache-hit track）**：目标 rev 缓存覆盖率 m/N 且 m>0（全命中为 m=N）时，缓存制品就位后执行的增量编译验证。产出编译裁决证据，其环境等价性由缓存锚+编译证据双重支撑。
- **fallthrough（坠落记法）**：裁决格声明 hot 而缓存锚核验实报 0/N 时，不执行编译，按本条款 §2.2 将裁决等价记为 cold 档位的成文化记法。fallthrough 是**记法降级**，不是执行替代，不产生编译证据。

## 2. 两轨裁决
### 2.1 cache 命中轨（热验证）
- 前置核验：缓存锚核验 m/N>0，记录制品清单哈希与来源（官方 release / vci-cache-relay）。
- 执行：增量编译，记录 rc、wall、log_digest。
- 裁决：rc=0 → DONE（热验证）；rc≠0 → FAIL（编译裁决，不得转 fallthrough）。serial_policy `rc_nonzero_continues` 兼容。
- 部分命中（0<m<N）：按热验证执行，但证据必须登记覆盖率 m/N；覆盖率本身不构成降级理由。

### 2.2 cache 缺失轨（cold-fallthrough 记法成文化）
**(a) 允许记 DONE 的条件（须同时满足）**：
1. 格声明 run_mode=hot 且缓存锚核验实报 0/N（双源核验：官方 cache + vci-cache-relay，计数与 404 样本落证据）；
2. 同 manifest 内至少一格同 rev（或同 artifact）已完成 cold 或 crosscheck 编译裁决且 rc 共识成立（G6 先例：G1 cold DONE rc=0 + ucif2/vinf 双独立 runner CROSSCHECK_OK + log_digest 字节级一致）；
3. 格保留 hot 标并附 fallthrough 备注，裁决字段显式标 `cold-fallthrough`，`build_exit_code=null`；
4. 证据链含 result_commit 指针。
**(b) 必须记录的证据字段**：rev_hash、run_mode=hot(fallthrough)、toolchain_version、env_hash、build_exit_code=null、cache 覆盖计数 0/N 与双源核验记录、等价依据格指针（同 rev cold/crosscheck 格 id + rc）、verdict=cold-fallthrough、paired_run_id。qlv 八字段兼容：build_exit_code 以 null 占位并在 verdict 承载 fallthrough 语义。
**(c) 必须记 BLOCKED 而非 DONE 的情形（任一即触发）**：
1. 同 rev 无任何已完成编译裁决格或 crosscheck 共识——fallthrough 失去等价依据，记 BLOCKED（缺口如实，禁止以「cache 缺」单方记 DONE）；
2. 缓存锚核验自身失败（双源均不可达/哈希不符）——环境事实未立，记 BLOCKED；
3. 裁决对象为 §4 结构不可验证族——fallthrough 不适用，记 BLOCKED 并转 §4 接口；
4. 格声明 run_mode=cold 而执行方以 cache 缺为由请求跳过——cold 之本义即无 cache 构建，无 fallthrough 可言，执行或记 BLOCKED。

## 3. 域限：缓存锚证据的有效域
- **有效域 = 环境等价性断言，且仅限于此**。缓存锚可支撑：「该 rev 之依赖制品在此环境可得/不可得」「两 runner 环境制品级一致（log_digest 字节级一致 = 确定性编译强信号，追记8 定谳）」。
- **缓存锚 ≠ 内容认证**。缓存制品的存在性不蕴涵、不增强、不削弱被编译对象的数学内容真值；内容认证的唯一通道是编译裁决证据（rc + 错误普查 + 公理审计）与独立复跑共识。禁止以缓存锚覆盖率、制品哈希一致性直接断言定理成立/不成立。
- **禁止延伸条款**：(i) 禁止以 cache 命中作为「已验证」的简称证据；(ii) 禁止以 cache 缺失作为「内容可疑」的反向证据（R25 定谳：cache 缺口是基础设施级诚实缺口，与随件编译失败是两层事实，G6 与 v9 双格已分立承载）；(iii) fallthrough DONE 之本体价值 = 实证 pin 无 cache（manifest G6 `fallthrough_rule` 原文），不升格为内容裁决。

## 4. 与 FINDING-20261010-04（CIRC 结构性）的接口
- FINDING-20261010-04 定谳：CERT-CIRC-LEAN-01 族在自身钉定 leancert v4.34.1 下**结构性**不可验证（checkADSupported 自 4bf84ea91 起不含 Expr.log，11/11 按设计拒证；Matrix.det Leibniz 定义组合爆炸），认证承载层实为 Python 区间算术。
- **条款**：凡经 FINDING 定谳为结构不可验证族（检查器按设计拒证，非环境、非资源、非漂移问题）者，**不适用 fallthrough**——其「无法编译验证」不源于 cache 缺失，坠落记法无的放矢；此类族之裁决只能走：(i) 内容级重构（log 消除化归支持域）后重新验证；或 (ii) 如实登记非 Lean 认证承载层（Python 区间认证口径），并禁止以任何 fallthrough/cold 等价记法冒充机器验证证书。
- 判别顺序：先查结构不可验证族登记册（FINDING 接口），不在册者方可进入 §2 两轨裁决。

## 5. 生效程序
1. 本候选案提交判定席，**双轮律**：首轮全量判定卡；undecided/fail 残差按收敛条件补强后次轮复投（FM-021 多轮主卡序列先例）。
2. 双轮通过后：回填 `board/r26fix-stress-matrix-01.manifest.yaml` 为 **v1.2**——G6 格增 `clause_ref: CACHE-ANCHOR-CLAUSE-01 v1.0` 指针、`supersedes: 1.1.1`、roundtrip_hash 重算（yaml↔json 结构等价规则不变）；v1.1.1 原文保留不改（v1.1.1 RE-ANCHOR ADDENDUM 同款纪律）。
3. 回填 commit 与判定闭合登记（LAB-CLOSE 格式）同波落板；条款编号 CACHE-ANCHOR-CLAUSE-01 v1.0 于回填时解冻生效。

## 6. 给判定席的关键问题（开庭题面）
- Q1：§2.2(a) 条件 2「同 rev 已有编译裁决共识」是否为过强门槛？是否存在合法场景：同 rev 无任何编译证据、仅凭双源 cache 0/N 核验即可记 cold-fallthrough DONE？（WS-18 倾向：否——无等价依据之 fallthrough 即无内容锚，应记 BLOCKED。）
- Q2：部分命中（0<m<N）轨是否需独立第三轨，抑或维持 §2.1「按热验证执行+登记覆盖率」从简？
- Q3：§4 结构不可验证族登记册的维护权与增录程序归谁（FINDING 自动入册 vs 判定席逐案裁定）？
- Q4：本条款生效后是否溯及既有 G6 记法（建议：溯及确认，G6 为先例锚不改动，仅增 clause_ref 指针）？

## 7. 风险点
- R1：条件 2 过强可能使孤立单格 manifest 无法使用 fallthrough——缓解：Q1 开庭裁决。
- R2：双源核验中 vci-cache-relay 为 dormant 设施，可达性非常备——缓解：§2.2(c)2 已覆盖（核验失败即 BLOCKED）。
- R3：上游 tag 漂移（FINDING-20261010-04 附带确权：leancert tag 远端重指向）提示缓存源本身可漂移；覆盖率核验必须记录采集时刻与样本哈希，防事后重指向抵赖。
- R4：术语风险——「cold 等价记」易被误读为「等同冷构建已执行」；§1/§3 已双重锁死：fallthrough 不产生编译证据。

—— 枢/PIVOT-01 智囊分机 WS-18 · 2026-10-11 · 候选案，待判定席双轮
