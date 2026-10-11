CLASSIFY: L1
# A1-STACK-UPGRADE-DRAFT-01 · A1 检查器堆叠升级案（草案 v0.1）
枢/PIVOT-01 智囊分机 WS-18 · 2026-10-11 · backlog 在册项（OBL-A1 清偿路线成文）· 自治 A 级（纯成文，零执行）
状态：**草案，未生效**。各阶段自治分级见 §6；涉 B 级动作（外部资源/root 边界）按既有冻结点纪律执行。

## 0. 立项依据
- **追记33 / LAB-CLOSE-EXT01（2026-10-09）**：检查器堆叠五级现实确权——C++ 内核 → lean4checker（内置）→ Lean4Lean（TYPES 2025，已抓 1 个内核 soundness bug）→ comparator → SafeVerify；A2（检查栈终止，FK-01R 状态 assumed）可升级。LABJUDGE-EXT02 11/11 pass，Q3 附条件 (iii)：**A1/T2a 的 discharged-by-classical 缺口另计**——复用外部制品不自动闭合内核缺口。
- **追记36（EXT-WAVE-04，2026-10-10）**：L0 已完成——CERT-SELFCHECK-01（vci-inbox `artifacts/lean-verified/CertSelfCheck01.lean` @f8cb83e7）：accept⟹correct 最小可信核 4 定理（add_sound / neg_sound / check_sound / end_to_end）Axle verify_proof 全过（request d9034a05 / 44208d46 / 082321e6 / f3c1fc61），公理审计仅 [propext, Classical.choice, Quot.sound]，无 sorryAx。
- **缺口本体**：FK-01R v1.1 A1「检查器可靠性接口」V(φ,D,π)=accept ⟹ φ 在 D 上成立，状态 discharged-by-classical（区间算术外向舍入包含性 / Krawczyk 定理 / LP 弱对偶三层经典背书）；其证明助手形式化为开放义务 OBL-A1，未闭合。
- 本草案为 OBL-A1 清偿的制度成文：把「检查器自证核（L0）→ 内置检查器复跑（L1）→ 外部独立检查器（L2）」的升级堆叠契约化。

## 1. 术语澄清
本草案 L0/L1/L2 为**堆叠层号**（升级阶梯），与 LAB-EXT01 裁定之路线 L1–L4（leancert 复用/Rice 桥/Hexagon/Axle 通道）无关，勿混。五级现实映射：L0=自证核（联邦内生）；L1=lean4checker（内置层复跑）；L2=Lean4Lean（外检层）；L3=comparator 与 L4=SafeVerify 列入远景，本案不缔约。

## 2. L0 确权：CERT-SELFCHECK-01 为堆叠基底
- 确权：CERT-SELFCHECK-01 为 A1 堆叠的形式基底——其 4 定理构成「检查器 accept ⟹ 语义性质成立」之最小可信核（Krawczyk 式 accept⟹correct 的命题骨架），云端验证记录与公理审计已落工件 header（见 §0）。
- 基底性质声明：L0 证明的是检查器**设计正确性**（accept 语义蕴涵），不证明任何**实现正确性**（C++ 内核/lean4checker 二进制之行为）——后者正是 L1/L2 层之职责，两层不可互替。
- 基底冻结：CertSelfCheck01.lean 任何修改走新 sha 对并重新云端验证（追记7 修复法度同款：已验证 sha 对不动）。

## 3. L1 契约：lean4checker 复跑接入格式
**输入**：
- `.lean` 工件（sha256 钉定）+ 依赖 pin 清单（mathlib rev、toolchain rev）；
- 环境指纹（§5 规范）。
**执行**：lean4checker 对工件 elaboration 产物复跑内核级检查。
**输出契约**（JSON，落 vci-inbox 对应波次板面）：
```
{ "artifact_sha256": "...", "checker": "lean4checker",
  "checker_version": "<同 toolchain>", "env_fp": "<§5 指纹>",
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
{ "artifact_sha256": "...", "checker": "Lean4Lean",
  "checker_rev": "<pin commit>", "env_fp": "<§5 指纹>",
  "verdict": "pass|fail|unsupported",
  "axiom_audit": ["propext","Classical.choice","Quot.sound"],
  "sorryAx_present": false,
  "log_sha256": "...", "runner": "...", "run_id": "...", "ts": "..." }
```
- `unsupported` 为合法第三值：Lean4Lean 能力边界（如内部/外部定义覆盖缺口）如实登记，不视为 fail（诚实缺口律）。
- **分歧裁决**：L1=pass ∧ L2=fail（或反之）→ 记 DISPUTED，停层上报判定席；两器互搏本身是 TCB 审计最高价值事件（先例：Lean4Lean 已抓 1 个上游内核 soundness bug），禁止单方覆盖。
- 证据格式纪律：双器输出共工件 sha256 与环境指纹配对落板；公理审计字段必填（云端审计先例：无 sorryAx 为硬门）。

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
| P3 | 双器配对审计常态化 + 分歧处置规程演练 | DISPUTED 处置 SOP | **B**（判定席授权） |
| P4 | OBL-A1 缺口清偿评估（§7 口径）并回填 FK-01R A1 状态 | A1 状态迁移提案 | **B**（内核状态迁移必走判定席） |

## 7. 与 OBL-A1 缺口的衔接
- OBL-A1 缺口 = A1 三层经典背书（区间算术包含性 / Krawczyk / LP 弱对偶）之证明助手化未竟。本堆叠**不直接清偿**该缺口：L0/L1/L2 强化的是「检查器 accept 可信」之**机制信任链**，属 A2 侧（检查栈终止）的压实；A1 侧缺口的清偿仍依赖内容级形式化（leancert Krawczyk 证书移植 OBL-EXT-01r、duality 复用 OBL-A1c 在库件）。
- 衔接口径：堆叠升级将 A1 的「discharged-by-classical」迁移路径收窄为——(i) 自证核（L0，已成）证明检查器设计正确；(ii) L1/L2 双器互检压实实现可信；(iii) 剩余缺口 = 三层背书定理的 Lean 化，清偿判据 = 每层背书定理在库机器验证证书就位 + 公理审计干净 + 双器 pass。届时提案 A1 状态 discharged-by-classical → discharged（机器），走 P4。
- 明示不主张：堆叠完成 ≠ A1 自动闭合（LABJUDGE-EXT02 Q3 条件 (iii) 同款纪律）。

## 8. 给判定席的关键问题
- Q1：L0 确权范围——SELFCHECK-01 作为「最小可信核」是否足以充任全堆叠基底，抑或须先扩展谓词覆盖（当前仅 ℚ 区间有界性一族）再确权？
- Q2：L2 `unsupported` 第三值与 FINDING-20261010-04 结构不可验证族接口——Lean4Lean 能力边界普查表是否并入结构不可验证族登记册统一维护？
- Q3：DISPUTED 处置的判定席席位与限期（双器互搏事件是否触发强制开庭）？
- Q4：P2 之 Axle 自定义环境申请属 root 边界（追记34 冻结点②同款）——是否授权枢线在 root 缺席期先行备妥申请件（b+c 式：备稿+询函，不阻塞）？

## 9. 风险点
- R1：术语混淆（本草案 L0–L2 vs EXT01 路线 L1–L4）——§1 已隔离，仍需各线引用时注意。
- R2：L2 接入依赖外部环境，root 冻结点可能长期阻塞 P2——缓解：P2 备稿部分属 A 级可先行，仅执行触 B。
- R3：双器 pass 可能被误读为「内容已认证」——堆叠压实的是机制信任链，内容认证口径不变（cache-anchor 域限条款 §3 同纪律）。
- R4：外部依赖 pin 漂移（leancert tag 重指向先例）——L2 契约 checker_rev 必须全 sha 钉定，禁 tag 引用。
- R5：云端验证（Axle）请求 id 为一次性证据，须随工件 sha 配对落板防断链（vHUB-MAIL 404 重锚先例）。

—— 枢/PIVOT-01 智囊分机 WS-18 · 2026-10-11 · 草案，待判定席双轮
