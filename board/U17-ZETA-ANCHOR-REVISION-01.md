CLASSIFY: L1
# U17-ZETA-ANCHOR-REVISION-01 · U-17 家族 ζ-anchor 命名失配并案修订登记与方案（EXT-WAVE-20 批八 · 完成度线）

- 成文席：QF-OS 联邦 W4 框架线席（EXT-WAVE-20 批八 · 完成度线；只写文，不 commit）
- 成文日期钉：2026-10-24（UTC(Z) 单时钟域；现状类断言均带「截至」钉）
- 性质声明（置顶）：**本件为登记与方案，不执行修订本身**——不改 formalization.yaml、不改帧、不改任何既有文件字节。
- 前置义务来源：board/L2-CLEARANCE-U12-U13-01.md §二 便签②（ζ-anchor 命名失配 finding 登记为 U-17 家族前置义务）；结转钩：board/FIRST-STEPS-LEDGER-01-20260930T0715Z.md L458「U-17 家族 ζ-anchor 并案修订前置义务」。
- 纪律钉（全件适用）：涉 NS 表述逐字携带「有限维 ODE 截断层」限定，禁「NS 已解决」式表述，批准状态语「自评已核、外部复现中、未颁奖」；涉 RH 表述逐字携带「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」，禁「RH 已证」式表述；名值分离：decl 名与公理集值分行列出，不以名代值。

---

## 一、finding 照录（自 board/L2-CLEARANCE-U12-U13-01.md §二 便签② 摘准，逐字不转录失真）

> **便签②（登记错位——ζ-anchor 命名失配 finding 及对 U-17 家族的影响评估）**：formalization.yaml alignment L160 登记名为 `NSGalerkin.zetaAnchorImpliesRHCriticalLine`，kernel 实测该名**不解析**（`Unknown constant`，机器原文见 §2）；真实全名为 `ZetaAnchor.zetaAnchorImpliesRHCriticalLine`（ZetaAnchor.lean L18 命名空间）。同条 `NSGalerkin.capAnchorP1` 解析正常。即 yaml alignment 第 5 条 lean 名半错——与 U-17（yaml alignment 第 5 条指帧 §3.2 编号归属不符）同条邻位。
> - **影响评估**：该 finding **不阻塞 U-12 定义层清除**（公理覆盖对真实全名实跑通过，名错位属登记层而非内容层）；但**登记为 U-17 家族前置义务**——U-17 修订案开案时，须将 yaml alignment L160 之名错位（`NSGalerkin.` → `ZetaAnchor.`）与编号归属不符一并处理，二错同条邻位，宜并案修订，不得只修其一即宣称 U-17 族闭合。

机器原文锚（判定件 board/L2-RECALC-WINDOW-01.md L96–97 探针输出）：
```
'ZetaAnchor.zetaAnchorImpliesRHCriticalLine' depends on axioms: [propext, Classical.choice, Quot.sound]
Probe.lean:16:14: error(lean.unknownIdentifier): Unknown constant `NSGalerkin.zetaAnchorImpliesRHCriticalLine`
```

名值分离登记（截至 2026-10-24）：decl 名 `ZetaAnchor.zetaAnchorImpliesRHCriticalLine`（公理集值 = {propext, Classical.choice, Quot.sound}）；decl 名 `NSGalerkin.capAnchorP1`（公理集值 = {propext, Classical.choice, Quot.sound}）。该 decl 为全局尺度临界线命题的 `def : Prop` 陈述件，「区间见证层 PASS、kernel 层未证、非 RH 证据」（便签① 层位钉）。

## 二、影响面普查（grep 仓内 ζ-anchor 相关引用点 · 截至 2026-10-24）

方法留痕：对 vci-inbox 仓 board/、library/、registry/、governance/、specs/、ci/、tests/ 以 `zetaAnchor|ζ-anchor|zeta-anchor|zeta`（大小写不敏感、限 .md/.yaml/.lean/.py/.sh 文本件）检索，命中点分类如下。

### 2.1 失配点（decl 名层，修订对象）

| # | 位置 | 现状（截至 2026-10-24） | 定性 |
|---|---|---|---|
| M1 | `library/ns/formalization.yaml` L160（alignment 第 5 条 `lean:` 字段） | `NSGalerkin.capAnchorP1, NSGalerkin.zetaAnchorImpliesRHCriticalLine`——后半名不解析 | **finding 本位**（便签②）；与 U-17 编号归属不符同条邻位 |
| M2 | `library/ns/formalization.yaml` L96（main_results `declaration:` 字段） | `NSGalerkin.zetaAnchorImpliesRHCriticalLine` | **本普查新发现之同型失配**：同一错误命名空间前缀见于 main_results 段（便签②探针输出 `Unknown constant 'NSGalerkin.zetaAnchorImpliesRHCriticalLine'` 对该名不解析之判定同型适用；建议修订执行时以 kernel 探针对该名复验留痕后并案处理） |

### 2.2 真实名基准（不动）

| 位置 | 内容 |
|---|---|
| `library/ns/NsGalerkin/ZetaAnchor.lean` L18 / L35 / L39 | `namespace ZetaAnchor` / `def zetaAnchorImpliesRHCriticalLine : Prop` / `end ZetaAnchor`——kernel 层唯一权威名源，零修订 |
| `library/ns/NsGalerkin.lean` L11 | `import NsGalerkin.ZetaAnchor`——模块层，零修订 |

### 2.3 登记/引用点（append-only 在册件，不修订，仅普查登记）

| 位置 | 内容 | 处置 |
|---|---|---|
| board/L2-RECALC-WINDOW-01.md L90–101、L136 | 判定件：探针输出、边界发现 2（登记错位）、汇总表「并入 U-17 族修订案」行 | append-only，不动 |
| board/L2-CLEARANCE-U12-U13-01.md §二（便签② L73–74、回炉条款 §二6） | 清除件：finding 照录源 + U-17 前置义务登记 | append-only，不动 |
| board/W-NS-03-REFORGE-CHARTER-01.md U-12 行（L94）、U-17 行（L99） | 挂账源：U-12 指 yaml L91–100 main_results（即 M2 所在段）；U-17 指 yaml L159–162 alignment 第 5 条编号归属不符 | append-only，不动 |
| board/WSF-EVIDENCE-SWEEP-20261023-01.md §一 U-12（L17–21） | 证据件挂账登记 | append-only，不动 |
| board/FIRST-STEPS-LEDGER-01-20260930T0715Z.md L442、L458 | 台账：ζ 锚名错位新发现实录、批八结转钩 | append-only，不动 |
| board/ZETA-INST-01-20261012T2130Z.md L20；board/KI-EXT11-1.md L42 | 四锚描述与「谓词映射，非 RH 蕴含」披露（用无前缀短名，非全名引用，失配不涉及） | append-only，不动；若未来改引全名须用 `ZetaAnchor.` 前缀 |

### 2.4 文件名层 / 工具层引用（非 decl 名层，零影响确认）

| 位置 | 内容 | 定性 |
|---|---|---|
| registry/palomar-registry-v1.yaml L68、L236 | PAL-0001/PAL-0003 recipe 文件序含 `ZetaAnchor.lean` 文件名 | 文件名层，不受 decl 命名失配影响，零修订 |
| board/EXT14-58SCAN-01-20261013T1305Z.md L28；board/FINDING-20261013-01-ADD1-20261013T1900Z.md L35/L46；board/EXT14-SUP-01-20261013T1900Z.md L30/L41 | ZetaAnchor.lean 文件哈希锁定清单（sha256=5a046673…） | 文件哈希层，零修订 |
| ci/gap_probe_zeta.sh；ci/test_witness_zeta.py 及 ci/witness_zeta_{gen,verify}.py | G3′ 缺席探针与 ζ 见证链（有限高度 T=100/1000 截断） | 不引用该 decl 全名，零修订 |

普查结论：失配集中在 formalization.yaml 两处（M1 finding 本位 + M2 同型新发现）；真实名基准、登记件、文件哈希层、工具层均无需触动。

## 三、修订方案（建议案，待归属线按版本程序执行）

### 3.1 命名统一口径建议

以 kernel 实测真实全名 **`ZetaAnchor.zetaAnchorImpliesRHCriticalLine`**（ZetaAnchor.lean L18 命名空间）为唯一登记口径；formalization.yaml 中 `NSGalerkin.zetaAnchorImpliesRHCriticalLine` 两处（M1 L160、M2 L96）统一改为 `ZetaAnchor.` 前缀；同条 `NSGalerkin.capAnchorP1` 解析正常（便签②），**不动**。修订执行时以 kernel 探针（`#print axioms` 或 `#check`）对新名复验留痕，复验件随修订版落仓——名值分离：名之修订以 kernel 解析值为唯一准据，不以登记件文字互证。

### 3.2 涉及件清单与各件修订归属线

| # | 件 | 修订内容 | 归属线 |
|---|---|---|---|
| R1 | `library/ns/formalization.yaml` | M1（L160 名错位）+ M2（L96 同型名错位）+ U-17 本位（alignment 第 5 条 source 指针「§3.2 见证层锚（CAP 证书锚 / ζ 锚）」编号归属不符——帧 §3.2 实载 W-NS-01/02/03，无 CAP/ζ 锚条目，WSF charter U-17 行 L99 在案）——**三错并案，不得只修其一即宣称 U-17 族闭合**（便签② 逐字义务） | formalization.yaml 归属线；本席建议并入 v0.5 落版窗口一次落版（ADJUD-20261023-02 BC-B3 锚例升格同窗），窗口不合则单开修订批 |
| R2 | NS-PROOF-FRAME-01 帧侧 | U-17 出路二选一（WSF charter U-17 行处置建议逐字：「修订 yaml source 指针（指向 census 增录注记）或帧侧补登记」）——若择「帧侧补登记」（CapAnchor/ZetaAnchor 增录注记入帧），由框架线按帧版本程序在下一修订版办理，措辞程序同 ADJUD-20261023-02 案(a) 先例；择路由判定席裁定，本席不代择 | 框架线（W4）行文 + 判定席择路裁决 |
| R3 | board 各在册登记件（§2.3 清单） | 零修订（append-only 铁律）；修订落地后由监视席/框架线出新登记件回指本件与落地件 | 监视席 / 框架线（登记新件，非改旧件） |
| R4 | palomar-registry-v1.yaml、EXT14 哈希锁定件、ci 工具层（§2.4 清单） | 零修订（普查确认零影响） | —（无义务） |
| R5 | U-12 清除联动 | formalization.yaml alignment 修订落地即触发 board/L2-CLEARANCE-U12-U13-01.md §二6 回炉条款（「formalization.yaml alignment 修订（含 U-17 族并案修订落地）」为明列触发项），U-12 清除自动回炉重审 | L2 复算窗线（重审实跑） |

### 3.3 执行序建议

判定席择路（R2 出路）→ formalization.yaml 修订落版 + kernel 探针复验留痕（R1）→ U-12 回炉重审（R5）→ 监视席新登记件收口、U-17 族闭合判定呈裁（R3）。

## 四、时间盒

- **建议截止：2026-11-18**（对齐 L2-2 复算窗口节奏，自首开 2026-10-23 起约四周，含择路裁决、yaml 落版、复验留痕、回炉重审四段）。
- 逾期处置：U-17 族维持挂账态，任何件不得宣称 U-17 族闭合；逾期事实由监视席下一续扫件登记并呈判定席。
- 本时间盒为建议值，正式约束以判定席裁定或归属线任务单为准。

## 五、纪律自查

1. 本件为登记与方案，未执行修订：未改 formalization.yaml、未改帧、未改任何既有文件字节；仓内既有件全部 append-only 不动。
2. NS C1–C3 / C1′–C3′：涉 NS 处带「有限维 ODE 截断层」逐字；无「NS 已解决」式表述；涉 OpenAI/Clay 状态沿唯一批准口径「自评已核、外部复现中、未颁奖」。
3. RH 行文钉：涉 RH/ζ 处带「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」；zetaAnchorImpliesRHCriticalLine 登记为 Prop 陈述件，非 RH 证据。
4. 名值分离：decl 名与公理集值分行列出（§一）；finding 照录逐字、普查点带位置钉。
5. CLASSIFY: L1 首行在位；本件不 commit，写后复读核验。

—— QF-OS 联邦 W4 框架线席 · EXT-WAVE-20 批八（完成度线）· 2026-10-24 · 纯成文零 commit
