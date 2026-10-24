CLASSIFY: L1
# WSH-M1-MATERIALS-01 · M1 中期复审材料首件——判据 A 三态登记表 + 判据 B 覆盖度基线 + 缺口整改清单 + 时间盒

- 制备席：QF-OS 联邦 W10 制备席（EXT-WAVE-24 批十二·M1 线启动；枢/PIVOT-01 体系）
- 成文时刻（date -u 实测）：**2026-10-24T21:34:12Z**（date -u 实测；UTC(Z) 单时钟域；现状类断言均带「截至 2026-10-24」钉）
- 使命口径：M1 中期复审材料**首件**成文（H2a 子件，预算 2–3pd 在案）；只写文不 commit；本文件为唯一新建件，未改动任何既有文件字节
- 上游证据件（全部已逐件打开复核）：`board/WSH-M0-GATE-01.md`（M0 闭合登记，2026-10-24T18:16:27Z）、`board/ALIGNMENT-MVP-RULING-01.md`（M1 双判据裁定，§一矩阵行 3 / §六）、`board/ALIGNMENT-MVP-CHARTER-DRAFT-01.md`（§2.1 六件交付定义、§1.1 H2a 拆件分估、§2.3 M1 行）、`board/TRUSTBOUNDARY-SPIKE-B-REPORT-01.md`（§四 C2 引理集锁定表、§5.1 V3 行）、`registry/TRUSTBOUNDARY-REGISTRY-01.md`（§4.4 S1–S6 定义母体、§4.3 标注约定、§4.5 V2 验收钉）
- 实测对象：`library/spec/SeamSpec.lean`（450 行）、`library/ns/formalization.yaml`（230 行）、`library/ns/NsGalerkin/*.lean`（13 文件目录实测）；本席实测时刻本仓 HEAD＝`74a32493aa054e4dc94ae6f3ef76b39f088ff035`（git rev-parse HEAD，2026-10-24）
- 语纪律：NS C1–C3 / C1′–C3′ 逐字钉全文有效（§五照录）；严禁「NS 已解决」式表述；涉 OpenAI 成果口径固定「自评已核、外部复现中、未颁奖」；Clay NS 未解决、未颁奖；名值分离（钉名与钉值分列，禁以名代值）
- **性质声明（如实口径）**：本件为 M1 复审窗开启前之**中期材料制备件**（快照登记），非 M1 复审判定书本身；三态登记为截至 2026-10-24 之现状实测，复审判定权属判定席，执行席不得自决（RULING-01 §六.4）

---

## 一、判据 A 登记表（S1–S6 六点三态逐点登记）

判据 A 裁定值照录（RULING-01 §一矩阵行 3 L20／§六.2 L80）：**S1–S6 逐点三态登记（PASS／降级（未定+理由）／FAIL），通过线 PASS ≥4 且 FAIL＝0**。S1–S6 定义摘准自章程 §1.2（L62）所引母体 `registry/TRUSTBOUNDARY-REGISTRY-01.md` §4.4（L90–99）。

**C1 先行件归属说明（应问登记）**：SeamSpec.lean（C1 Spec 环骨架，450 行，bare-lean EXIT 0）对应 **MVP v0 交付定义第 1 件（Spec 环骨架，章程 §2.1-1）**，不直接等同 S1–S6 之任一点；其证据辐射面为：① S1 机制面旁证（全文件零 sorry 零 axiom 批五落账在案）；② S6 之标注承载前置（L-1..L-5 陈述槽与 V1–V5 门谓词机读化在件内， SeamSpec.lean §五 L196–297／§六 L420–432）；③ C2 签收之前置（Spec→Gap 接口契约：无 Spec 条目不得直跳 Adapter，spike B §六.1 L122）。其验证口径为裸 lean 单件 EXIT=0，**不构成主库构建绿证据，亦不构成 C2 引理之数学证明**（WSH-M0-GATE-01 §三.3 在案口径照录）。

| 验证点 | 定义摘准（章程 §1.2 ← registry §4.4） | 三态（截至 2026-10-24） | 现状实测与证据钉（文件+commit） |
|---|---|---|---|
| **S1** | T1 `axiom_whitelist`（decl 级）：一期对 C1–C3 新增 decl 逐条白名单审计回填 | **PARTIAL** | 机制面在案：`formalization.yaml` `status.axioms`（L71）包级三公理白名单 + `main_results` 9 decl 逐 decl 公理集登记（L73–121）；C1 先行件零 sorry/零 axiom 实证（commit **6d1150e8e**，2026-10-23，批五落账 FSL v47 L431 在案）。缺口：registry §4.4 自陈「现仅包级承载」，**对 C1–C3 新增 decl 之逐条 decl 级白名单审计回填未执行**（C1 之 450 行新增 decl 未逐条入 `axiom_whitelist` 字段；属 C4/C2 同窗行项） |
| **S2** | T1 `machine_checks[]` 六字段齐套：tool/tool_version/run_id/verdict/log_sha256/as_of 全字段实测 | **PARTIAL** | spike B §5.1 V3 行（L96）在案：**六字段中四字段已可实填**（tool=lake comparator／tool_version=v4.35.0／verdict=accepted／as_of=2026-10-22）；**run_id 与 log_sha256 两字段未定+理由在案**（spike 本机跑批无 CI run_id，/tmp 易失层致 log 产物不可跨会话援引——B4 阻塞结转，关闭路径＝一期启动后首个 CI 窗，spike B §5.3 L112–115；责任窗＝M0 开账 2026-10-24 后 10 工作日内，python3 实算截止 **2026-11-06**） |
| **S3** | T1 `exclusion_pointers[]`：Gap 环降级缝（若有）之排除指针首跑（同址原则：本体留仓、指针入册） | **PARTIAL** | 字段机制已实战：`formalization.yaml` `federation.exclusion_pointers` 4 条在案（L211–219：sorry-free／axiom-bounded／scope-exclusion／no-Clay-chain）；alignment 表 `not-formalized` 显式登记先例在案（L191–195，§3.3 阻塞层四项）。缺口：**Gap 环降级缝之排除指针首跑未发生**——C2 引理簇未开工，尚无降级缝可登；属「机制已通、对象未生」态 |
| **S4** | T2 `dual_kernel`：nanoda 对 ~1.5k 行一期构件 dry-run；资源不足记「未定+理由」 | **PARTIAL** | 最小目标实证在案：spike A#24 异构**三核**（nanoda＋con-leche＋con-ron）对同一导出件（最小目标 spike-min，3 decl／345MB NDJSON）全 accept，EXIT=0，超 dual 口径（spike B §5.1 V3 行 L96；基线数据表 §二 行 4/6 L40/L42）。缺口：**对 ~1.5k 行一期构件之 dry-run 未跑**——真实规模基线 B1 未定+理由在案（本机 4GB RAM 不足；关闭路径＝公域 CI 通道，责任窗同 S2，截止 2026-11-06 在案） |
| **S5** | T0 `self_fingerprint_sha256` 回填流程：卡6 发放时实测回填流程首跑（禁预填） | **PASS** | 流程首跑已发生：`formalization.yaml` `federation.certificate.self_fingerprint_sha256`＝`96a2e74d14b1f0375abbc6702e2eef5df4113bd37b18a21bb97b002ce1ec5f34`（L210，WELD V2-1 verdict+yaml+config 联合哈希），随 G1 发放（issued_at 2026-10-17T07:00Z，L205）**发放时实测回填**，非预填。注记（如实）：首跑对象为既有包 G1 刷新，非 MVP 新构件；M2 验收时须对一期构件重跑本流程（义务结转，非本点降级理由） |
| **S6** | `alignment.statements[]` 状态机扩展：proved/not-formalized + `l34` 标注子键联合首跑 | **PARTIAL** | 状态机半边在案：yaml `alignment.statements` 6 条，proved×5／not-formalized×1 状态机运转中（L153–195，python3 re 实算）；U-17 并案修订实证状态机 append-only 维护能力（L170–195，commit 8db7ff181 在案）。缺口：**`l34` 标注子键零回填**——`grep -c "l34" formalization.yaml`＝**0**（本席实测）；yaml 侧 6 条无一挂 `l34` 子键，联合首跑未完成（属 C4a 标注 schema 落地行项） |

**三态分布一句话（截至 2026-10-24）：PASS×1（S5）／PARTIAL×5（S1/S2/S3/S4/S6）／FAIL×0。**
**对通过线之差距（如实登记，非判定）**：判据 A 通过线 PASS≥4∧FAIL=0；现状 PASS=1＜4，FAIL=0 满足——**若今日即复审则判据 A 不过**；M1 复审窗（2026-12-05 相对钉先到）前须将 ≥3 点由 PARTIAL 抬升 PASS（缺口与整改见 §三）。FAIL=0 之维持为底线义务。

---

## 二、判据 B 覆盖度基线（alignment 标注覆盖度实测）

判据 B 裁定值照录（RULING-01 §一矩阵行 3 L20／§六.3 L81）：**alignment 三态标注覆盖度 ≥50%（相对 V2 验收钉 100% 之线性中点）且随机抽查 ≥10% 经 L3-4a 人工复核一致**。V2 验收钉母体：registry §4.5（L104：「alignment 映射对三态标注覆盖率 100%；随机抽查 ≥10% 经 L3-4a 人工复核一致」）。

### 2.1 覆盖度当前值（自 yaml 实算，截至 2026-10-24）

| 量 | 实测值 | 实测方法与证据钉 |
|---|---|---|
| 标注对象总数（alignment 映射对） | **6 条** | `library/ns/formalization.yaml` `alignment.statements[]` 条目数，python3 re 实算＝6（L153–195；proved×5＋not-formalized×1） |
| 已挂三态标注（L34a/L34b/L34c）之映射对 | **0 条** | ① yaml 侧：`l34` 扩展子键出现次数＝**0**（`grep -c "l34"` 实测）；② Lean 侧：对本仓 `library/ns/NsGalerkin/*.lean` 13 文件与 `library/spec/SeamSpec.lean` 逐一 grep `[L34a` 标注块，命中仅 `Lorenz96.lean`（L177–186／L214–222 等，练兵线先例件，**不在本表 6 条映射对范围内**）——6 条映射对对应之 Lean 侧文件（Basic/Existence/Uniqueness/Concrete/ExplicitB/CapAnchor/ZetaAnchor/SkewB）**零标注块** |
| **覆盖度当前值** | **0/6 ＝ 0.0%** | 名值分离：名＝alignment 标注覆盖度，值＝0.0%（截至 2026-10-24） |
| 判据 B 通过线 | **≥50%（≥3/6 条）**＋抽查 ≥10% | RULING-01 §六.3 裁定值 |
| **差距评估** | **缺口 3 条映射对（50 个百分点）** | 0/6 → ≥3/6；对应行项 C4a（标注 schema 落地 1.5–2pd）＋C4b（逐 decl 标注执行 2–3pd），registry §4.6 在案估算合计 3.5–5pd（0.7–1.0pw），属 H1 线既有预算不新增 |
| 工艺先例注记（如实） | 标注块工艺已有实战先例 | `Lorenz96.lean` 练兵线已产出 L34a/L34a#子键/L34b/L34c 全形态标注块（含「未定+理由」降级形态 L186），工艺可移植；但练兵件成果**不计入**本表覆盖度分子（范围纪律：映射对以 yaml `alignment.statements` 为准） |

### 2.2 抽查 ≥10% 方案（随机抽查规程草案——呈复审席采用，非授权件）

1. **抽样框**：复审执行时刻 yaml `alignment.statements[]` 全量映射对（若 C4 扩表则以下检时刻实测总数为准，名值分离）。
2. **抽样量**：⌈总数 ×10%⌉ 且 **≥1 条**；按当前 6 条框＝1 条（下限），若扩表至 56 decl 级逐 decl 映射则 ≥6 条。
3. **随机化规程**：以复审执行日 date -u 之 UTC 日期戳（YYYYMMDD）为种子，python3 `random.Random(seed).sample` 抽取，种子与抽中清单随复审报告成文登记（可复现）。
4. **复核工序**：抽中条目逐条过 L3-4a 陈述层八要素对表（FIDELITY-AUDIT-PROTOCOL-L34-01），复核席＝**独立审计席**（RULING-01 §四.3：签发/复核席与作者相互独立，禁自审）；一致性判定＝标注块三态与人工对表结论逐字一致。
5. **不一致处置**：任一抽中条不一致即判据 B 不过，当日触发状态复审（RULING-01 §六.4），处置权属判定席。

---

## 三、缺口与整改清单（逐缺口列整改动作／归属线／建议截止）

| # | 缺口（对应验证点/判据） | 整改动作 | 归属线（预算在案钉） | 建议截止 |
|---|---|---|---|---|
| G-1 | 覆盖度 0/6＝0%（判据 B；S6 之 l34 半面） | C4a 标注 schema 落地（yaml `l34` 子键 + Lean 侧三态标注块首跑）＋C4b 逐 decl 标注执行，优先覆盖 6 条映射对达 ≥3 条 | H1 线 C4 标注层 3.5–5pd 在案（registry §4.6 L121–123；不新增预算） | **2026-12-05**（M1 相对钉，先到为准）前达 ≥50% |
| G-2 | S1 decl 级白名单回填未执行 | C1 新增 decl（SeamSpec 15 structure/inductive＋31 glue 定理，FSL v47 L431 在案数）逐条 axiom_whitelist 审计回填；随 C4a 同窗执行 | H1 线 C4a 内含；nanoda 白名单机制在案（spike A#20） | 2026-12-05 前 |
| G-3 | S2 run_id/log_sha256 两字段未定 | B1 真实规模基线 CI 跑批同窗回填（公域 CI 通道，artifact 三哈希＋run_id＋log_sha256 入册，spike B §六呈批 2 跑批要件四项照录） | 算力线既有额度沿用（C-1，无新增）；B1/B2/B4 责任窗在案 | **2026-11-06**（M0 开账＋10 工作日，python3 实算） |
| G-4 | S4 一期构件 dry-run 未跑 | 随 B1 CI 跑批对 ~1.5k 行构件执行 nanoda（＋con-leche/con-ron）dry-run；资源不足则记「未定+理由」（schema 允许降级，非 FAIL） | 算力线 C-3 在案；同 G-3 同窗 | 2026-11-06（随 B1 窗） |
| G-5 | C2 引理簇未开工（S3 之降级缝对象未生；MVP 交付件 2 直接缺口） | 启动 C2 主选 4 件 kernel 化（spike B §四锁定 L-1..L-4 在案，行数带 630–820）；建议低爆险件 L-4（80–120 行）、L-2（150–200 行）先行，L-1 缝本体随后；SeamSpec 陈述槽（§五 L264–297）为签收桩 | H1 线 C2 3.5–4.5pw 在案（registry §4.6 L119） | M1 前至少 1–2 件落件（支撑 S3/S6 抬升）；全簇不晚于 M2 **2026-12-31** |
| G-6 | S5 重跑义务（PASS 维持条件） | M2 验收时对一期构件新版重跑 self_fingerprint 实测回填流程 | H1/H3 线，卡6 发放时回填规程在案 | 2026-12-31（随 M2） |
| G-7 | 抽查复核主体待定 | §2.2 抽查规程呈复审席采用；独立审计席人选与排期随 M1 复审窗启动确认 | H2a 本件已含规程草案；复核工时属复审席侧 | 2026-12-05 复审窗启动时 |

**整改纪律照录**：任一缺口整改引发估爆/超耗，回判定席复议，申报时限 5 工作日内，禁静默扩项（RULING-01 §三.4）；降级缝落 `not-formalized` 显式登记须判定席裁决，禁静默（WS44 L4-3 / spike B §四 L83）。

---

## 四、时间盒

1. **本件制备工时自评（对 H2a 预算 2–3pd）**：自评实耗 **≈2pd**（构成如实登记：上游四件＋registry 母体逐件复核 ≈0.7pd；yaml/Lean/git 三侧实测与实算 ≈0.5pd；本件成文 ≈0.8pd）——落在 H2a 预算带 2–3pd（章程 §1.1 H2 拆件分估表 L35，裁定值）之内，不超上限；如实入账，随收波登记。
2. **M1 复审窗双钉提示（名值分离）**：相对事件钉＝M0 启动时刻 2026-10-24T18:16:27Z＋42 日＝**2026-12-05**（python3 date 实算）；绝对日期钉＝**2026-12-27**（RULING-01 §一矩阵行 5 裁定值）；**双钉并存、先到为准——相对钉 2026-12-05 先到，复审窗以 2026-12-05 起算为准**（WSH-M0-GATE-01 §二.5 登记在案）。截至本件成文日 2026-10-24，距相对钉 **42 天**（python3 实算）。M2 钉照录：相对 M0＋40 工作日／绝对 **2026-12-31**，先到为准；M1→M2 间隙整改余量以 H4 缓冲（0.8–1.2pw）为限，判据任一不过即当日触发状态复审，**禁借间隙静默顺延**（RULING-01 §二-5 L35／§六.5 L83）。
3. **处置权提示**：本件所有三态与差距登记均为制备席实测快照；M1 复审之判定与不过后之处置路径（继续／缩范围／回退重估）权属判定席，执行席不得自决（RULING-01 §六.4 L82）。

---

## 五、合规自检（本文件行文）

1. **NS C1–C3 逐字钉**：C1「任何对外引用本包必须逐字携带『有限维 ODE 截断层』限定；不得上推为 PDE 层陈述」、C2「W-NS2 之引用必须逐字携带『非轨道包络』披露」、C3「OBL-NS-01/02/03 未闭环前，本包不得被引用为『Clay NS 证据链的一环』」——本件为内部治理材料件，不构成对外引用；无「NS 已解决」式表述。
2. **RH C1′–C3′ 逐字钉**：C1′「有限高度 T=100/1000 截断」、C2′「区间见证层 PASS、kernel 层未证、非 RH 证据」、C3′ 严禁「RH 已证/已验证到 T」——本件涉 ζ 锚对象处（§一 S1/S5 证据钉、§二 yaml 条目）随文携带 C2′ 钉语（formalization.yaml L183 在案口径照录），滤网在位零越界。
3. **批准措辞钉**：涉 OpenAI 成果口径逐字「**自评已核、外部复现中、未颁奖**」；Clay NS 未解决、未颁奖。
4. **名值分离**：全部钉以「钉名＋钉值」分列（如「覆盖度当前值 0/6＝0.0%」「M1 相对钉 2026-12-05」），未以名代值；全部日期钉为绝对日期（UTC(Z)）或标明相对事件钉算术（python3 实算）。
5. **如实登记自检**：三态分布 PASS×1／PARTIAL×5／FAIL×0 逐点有实测证据钉支撑，无粉饰（S2/S4 之 spike 最小实证未升格为全量 PASS；S5 之 PASS 附重跑义务注记）；「若今日即复审则判据 A 不过」之差距句如实载入。
6. **append-only／不 commit**：本件仅新建 `board/WSH-M1-MATERIALS-01.md` 一件，未改动任何既有文件字节，未执行任何 git 写操作（git status --porcelain 实测为空，截至 2026-10-24）。
7. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** SeamSpec bare-lean EXIT 0 与 spike 六复核器全 accept 均为机器层必要条件证据；语义缝（TB-09）闭合判定须经 L3-4a/b/c 三层人工审计与判定席裁决，永不可被编译绿灯吸收。

—— QF-OS 联邦 W10 制备席 · 枢/PIVOT-01 体系 · EXT-WAVE-24 批十二 · 2026-10-24
