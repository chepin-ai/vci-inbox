CLASSIFY: L1
# REGISTRY-MERGE-EXEC-20261027-01 · QF-OS 联邦批三十（EXT-WAVE-41）S1 头号执行项 · 双 registry 归并执行报告（S1~S7 实录＋M-1~M-7 自核）

- 席别：批三十 S1 归并执行席（见证线作业）；执行依据=`board/ADJUD-REGISTRY-MERGE-20261027-01.md`（R-1 归并案裁决书：裁①根级面为尊、裁②面限定、裁③归并执行令 S1~S7＋oid 统一规则＋验收 M-1~M-7，全文已复读）
- 时刻：2026-10-27（as-of；单时钟域 UTC(Z)）
- 口径纪律（逐字）：涉 ζ 见证表述限「**有限高度 T=100/1000 截断**」语境；状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」；全件严禁且无「RH 已证/已验证到 T」字样；批准口径「隔离区间内区间见证 PASS、非全域声明」；iso100 层位表述以案 J 态①逐字为准、援引随载限 J-1~J-5
- 甲席席规：不新产工时/产能估计；名值分离（oid 名与值分行、字段名与取值规则分行）；全部哈希/提交号系当次实测
- 作业纪律：**只交付不入库，零 git 写操作**（合并提交走 orchestrator 批收口通道）；覆写权归原线——本波仅动裁决令授权之工件（根级面 3 条目＋artifacts 面废止标注）＋新建本报告与勘误件；lead 指令变更登记：**S6 删除改型为 append-only 废止标注（不删文件）**（差异见 §三 D-1）

## 一、S1~S7 执行实录

| 步 | 内容 | 执行实录（证据） |
|---|---|---|
| S1 | 根级面 iso-100 吸收态①口径 | **已落**：`gap-registry/zeta/zeta-iso-100.json`——wit.tier 主文=案 J 态①逐字＋历史坐标括注「（EXT15 收波形：CERTIFIED(29)·Backlund 门 v1.1.1 PASS）」；wit.detail 追加关闭句与判据句（ADJUD-ZETA-R2-CASES-JK §四.1 字节级提取）；disclosure 原 4 条保留＋增列限 J-1/J-2/J-3 三条（逐字）；ki_ref 本已「(+ADD1+ADD2)」（R-3 核销，assert 实证） |
| S2 | 根级面 iso-1000 吸收案 K mandated 两句 | **已落**：disclosure 原 4 条保留＋增列 CERTIFIED 层位句＋WQ-8 补载句（裁决书逐字提取），现 6 条 |
| S3 | trunc-psi 迁入根级面 | **已落**：`gap-registry/zeta/zeta-trunc-psi-1e7.json` 新立（源=artifacts 面后态）；scope_fence 逐字零 diff（python assert）；disclosure 增列「管道演练件、零定理内容（R1 WQ-7 在案）」＋迁移注记；schema 沿用 1.0.1(EXT14-SUP-01) 不回溯升降（裁决书 S3 规则） |
| S4 | 三面 9 处 oid 按统一规则施行 | **已落**（根级面）：witness_oid/R1_artifact_oid=规范化 witness_sha256 64-hex（iso-100=`aaceb9a0…fdaaf`、iso-1000=`4c380c1e…a33bc3`、trunc=`8e443bb2…e19ff6`，与证书内嵌字段对拍一致，ZETA-BACKFILL-EXEC §二表名值引用）；commit_oid=真实 git commit oid 40-hex=`0233116a775dc14b01a64f6d1dcf80efb146947f`（三件同一——现行证书内容入链提交，git log -1 逐证实证；git cat-file -t=commit 核验过）。**处置登记 D-2**：iso-100 原根级值 d8a046f2…（EXT-WAVE-12 关闭提交）经核其树内证书字节与现行证书不同（sha256 对拍 DIFF），作版本锚已陈旧——按裁决书「证书入链之真实 commit」定义改钉 0233116a，d8a046f2 作为关闭提交历史坐标留存于 redeem.R3_census_diff 行文（未删） |
| S5 | 全仓「artifacts/gap-registry」引用核销/改指 | **已核（留痕不覆写）**：git grep tracked 面现行实测 **35 行 / 16 文件 / 43 处出现**（2026-10-27 返修复跑；输出 sha256 锚 `feee5a3f…c546bc7e`，全量清单见 §三 D-3）——全部落历史 append-only 原册/裁决原文/自引语境，按 M-5 豁免条款逐命中核语境留痕，零处须覆写；今后行文统一指根级路径。计数沿革如实登记：初报 24（失实）→复核庭实测 37 行/16 文件/42 处（含 W-1 膨胀）→R-W1 修复后现行 35 行（−2 行系 DRAFT-02 去重） |
| S6 | artifacts 面废止 | **改型执行（lead 令：append-only 废止声明、不删文件）**：3 工件各增 `DEPRECATED` 字段（废止声明全文，唯一权威面=根级、引用改指、删除归 orchestrator）；新建 `artifacts/gap-registry/zeta/_DEPRECATED-20261027.md`；**删除动作移交 orchestrator 批收口合并通道**（裁决书 S6 原文路径存续） |
| S7 | FSL 登记行 | **移交 orchestrator**（覆写权不在本席）：要素备齐——「权威面＝gap-registry/zeta/、artifacts 面废止（标注先行/删除移交）、oid 统一规则（witness_oid/R1=规范化 sha256 内容锚、commit_oid=40-hex 版本锚 0233116a…）」三要素 |

## 二、M-1~M-7 自核表

| # | 判据 | 自核结论 | 证据 |
|---|---|---|---|
| M-1 | 根级面 3 条目与 artifacts 面（回填后）逐字段对拍表落板，差异仅余白名单类 | **PASS（带登记差异＋残差呈确认）**——对拍表落板（§四）；差异 13 处，定类计数经复核庭纠偏后改正为：**白名单 5**（iso-100 tier 历史坐标括注 1＋trunc disclosure[4]/[5] 注记 2＋schema 标签差 2〔iso-100 1.1.1/iso-1000 1.2.1 沿 S3 规则；trunc schema 无 diff、不列入〕）＋**sanctioned 3**（commit_oid×3＝统一规则本意）＋**已核残差 5**（iso-100 之 wit.detail 措辞／ki_ref／redeem.R2_ledger／redeem.R3_census_diff／redeem.status——超裁决书白名单字面，呈判定席确认，见 §三 D-6） | §四对拍表 |
| M-2 | 9 处 oid 符合统一规则 | **PASS**：根级面 6 处 64-hex=证书内嵌 witness_sha256 逐位一致（复算对拍）；3 处 40-hex=0233116a… ∈ git 实存提交（cat-file -t=commit）；artifacts 面 9 处维持案 K 回填形（随废止封存） | §一 S4；git 实证 |
| M-3 | 态①逐字＋限 J-1~J-3 于 iso-100 条目可 grep | **PASS**：tier 主文==态①逐字（True）、J-1/J-2/J-3 三条逐字在 disclosure（True×3，字节比对裁决书提取串） | §一 S1 |
| M-4 | trunc-psi scope_fence 逐字零 diff | **PASS**（python assert，与 artifacts 面后态逐字等） | §一 S3 |
| M-5 | 全仓 grep 零命中（除豁免语境，逐命中留痕） | **PASS（豁免路径，清单已修正）**：现行实测 35 行/16 文件/43 处全部定类豁免语境（逐文件:行清单＋语境核注见 §三 D-3，可复跑命令与输出哈希锚同载）；初报 24 计数失实已更正 | §一 S5、§三 D-3 |
| M-6 | artifacts 面删除 manifest 与回填 §五 后态表逐位一致 | **PASS（改型核验）**：删除改废止标注（D-1），改核「标注前快照==ZETA-BACKFILL-EXEC §五 后态表」——3 件 sha256 逐位一致、文件集一致（True）；标注后新 manifest 落 §四 | §四 |
| M-7 | FSL 登记行含三要素 | **移交**：orchestrator 权责（要素已备，§一 S7）；本席不可自证 | §一 S7 |

**自核计数：M-1~M-6 PASS（M-1 残差 5 项呈判定席确认〔D-6〕、M-6 改型核验），M-7 移交 orchestrator。** 返修订正登记（复核件 REGISTRY-MERGE-REVIEW-20261027-01）：M-1 定类计数更正为白名单 5／sanctioned 3／残差 5；M-5 命中清单更正为 35 行/16 文件/43 处（补登 WILDQ-RH:7，逐命中留痕达成）；W-2 残留句已清理。

## 三、差异/异常如实登记

- **D-1（S6 改型）**：裁决书 S6 原文＝删除（orchestrator 合并通道）；本批 lead 令＝append-only 废止标注不删文件。执行结果：标注已落（3 工件 DEPRECATED 字段＋_DEPRECATED-20261027.md），**删除移交**——双面物理并存延续至 orchestrator 删除提交，期间引用风险面由 DEPRECATED 声明＋过渡管控句管控。
- **D-2（commit_oid 处置）**：iso-100 根级原值 d8a046f2… 经实证为陈旧版本锚（其树内证书字节≠现行证书，sha256 对拍 DIFF）；按裁决书字段语义定义改钉 0233116a…（现行证书入链提交）；「保真实提交」字面与本处置之偏差已以「陈旧锚更正」登记，旧值留存于 redeem.R3 行文不删。
- **D-3（S5 逐命中清单＋语境核注，现行工作树实测 35 行/16 文件/43 处出现；可复跑：`git grep -n 'artifacts/gap-registry' -- .`，输出 sha256=`feee5a3f429356447588250c3336e92e2340b2cf26d5416cd5da0155c546bc7e`）**：
  - artifacts 面自引（3 行/6 处）：`zeta-iso-100.json:42`、`zeta-iso-1000.json:41`、`zeta-trunc-psi-1e7.json:39`——DEPRECATED 废止声明字段（本波新载，自引语境）；
  - 裁决原文（10 行）：`ADJUD-REGISTRY-MERGE-20261027-01.md:15/26/47/51/54`、`ADJUD-ZETA-R2-CASES-JK-20261027-01.md:27/39/88`、`ADJUD-ZETA-R2-CASE-N-20261027-01.md:18/46`——裁决书引述与执行令原文，append-only 不覆写；
  - 收割/质询原册（15 行）：`ADJUD-WILDQ3-HARVEST-01.md:9/45/119`（收割实录与补强单）、`WILDQ3-ZETA-20261026-01.md:10/16/17/18/44/45/46`（质询件证据钉/查验路径）、`WILDQ-RH-20261025-01.md:7`（R1 野问证据基线行——**初报漏登，本修订补登**）、`ZETA-BACKFILL-EXEC-20261027-01.md:10/39/65`（作业原册）、`ZETA-INST-01-20261012T2130Z.md:23`（设计原册旧路径）；
  - 重述/登记/监视实录（7 行）：`ZETA-RESTATEMENT-DRAFT-01.md:18`、`ZETA-RESTATEMENT-DRAFT-02.md:28/50/111`（L111＝本波面限定补注块）、`FIRST-STEPS-LEDGER-01:782`（批二十九收口条）、`MONITOR-SWEEP-20261027-02.md:54`、`MONITOR-SWEEP-20261027-03.md:17`（案 N (a) 基线行——核对行机制启动在案）。
  - 结论：**无一处须覆写之现行引用**（豁免语境逐命中成立；今后行文统一指根级路径）。本报告自身（untracked 在途件）含同字符串多处，不计入 tracked 面口径——名值分离登记。
- **D-6（判定席确认申请行——M-1 残差 5 项超裁决书白名单字面，呈 B-ADJ 确认；路由：lead 转）**：五项名＝`wit.detail`（措辞差：根级收波形含修补 #17 详述 vs artifacts 回填形）／`ki_ref`（根级「(+ADD1+ADD2)」vs artifacts「(+ADD1)」）／`redeem.R2_ledger`（根级 LAB-CLOSE-EXT12＋追记49 vs artifacts WQ-BOOK 追记48＋FSL v35）／`redeem.R3_census_diff`（根级 EXT15 四轮收敛详录 vs artifacts EXT14 哈希锁定复核句）／`redeem.status`（根级「…升 CERTIFIED@EXT15」收波形 vs artifacts「open→witnessed」）。一句定类理由：五项皆属「根级收波形为尊、artifacts 面系案 K 回填令授权面外之旧值、随该面废止不回流」之已核残差——请判定席确认此定性备案（或裁 M-1 白名单口径扩载／status 行加态①指针，复核件 W-3 建议在案）。
- **D-4（裁②联动核验）**：收割件问一与案 K 裁决书之「面限定补注」（责任线判定席行文席，窗批三十收口前）as-of 本报告未落（grep「面限定」两件零命中）——登记在案，随归并同窗盯守；本席自件 ZETA-RESTATEMENT-DRAFT-02 之面限定补注已落（append-only）。
- **D-5（M-1 白名单外差异）**：iso-100 之 wit.detail 措辞（根级收波形含修补 #17 详述 vs artifacts 回填形）、ki_ref/R2_ledger/R3/redeem.status（根级收波新值 vs artifacts 回填令授权面外旧值）——实质同向（两面均载 ADD2 关闭与态①判据），根级为尊、随 artifacts 面废止不回流，如实登记。

## 四、对拍表与 manifest（M-1/M-6 落板）

**根级面（归并后，唯一权威面）3 条目 sha256**：全形六值见附尾 SHA 块（2026-10-27 当次实测）。
- 逐字段对拍结论：根级 3 条目与 artifacts 面（回填后态）之字段全集对拍——iso-100：字段 29=29，差异 8＝白名单 2（tier 括注/schema 1.1.1）＋sanctioned 1（commit_oid）＋残差 5（D-6 五项）；iso-1000：28=28，差异 2＝白名单 1（schema 1.2.1）＋sanctioned 1（commit_oid）；trunc：28 vs 26，差异 3＝白名单 2（disclosure[4]/[5] 注记）＋sanctioned 1（commit_oid；schema 无 diff）。合计 13＝白名单 5＋sanctioned 3＋残差 5（复核庭纠偏后口径）。

**artifacts 面 manifest**：标注前快照＝回填 §五 后态表（逐位一致，M-6）；标注后（废止封存态）sha256 见附尾 SHA 块。

## 附尾 · SHA 块（2026-10-27 当次实测，sha256 全形）

**根级面（归并后，唯一权威面）**：
- `gap-registry/zeta/zeta-iso-100.json` = `167faaff7e67197afb29ebaaa192033489dd80b632ce9be2ed862306298ff9b5`
- `gap-registry/zeta/zeta-iso-1000.json` = `08951975fb31478f892cf3e54d2b98c4add49fb68580d6ee880f3278fb291279`
- `gap-registry/zeta/zeta-trunc-psi-1e7.json` = `b2b010a51c9ccfc6d4e912f9a4f7b6f2b689c9a94457d0bbd48c40dd7afe37b1`

**artifacts 面（废止封存态，标注后）**：
- `artifacts/gap-registry/zeta/zeta-iso-100.json` = `3656bfa0627f8a07271dba0c0e3f19f34bec3b0d01e9aa720cd2d84114783952`
- `artifacts/gap-registry/zeta/zeta-iso-1000.json` = `9b9b8f46ba9a2dcdabf4028fd3f5d5074a095b26c6f0c9ba392a301c7b8d28a5`
- `artifacts/gap-registry/zeta/zeta-trunc-psi-1e7.json` = `eb597cfa9584dc69bea772126d1ba78b3c86e7eda58f13eb16aaed47ff44c498`

—— QF-OS 联邦批三十 S1 归并执行席（见证线）· 2026-10-27 · 双 registry 归并 S1~S7 执行完毕（S6 改型/S7 移交如实登记）· 零 git 写操作
CLASSIFY: L1
# REGISTRY-MERGE-EXEC-20261027-01 · QF-OS 联邦批三十（EXT-WAVE-41）S1 头号执行项 · 双 registry 归并执行报告（S1~S7 实录＋M-1~M-7 自核）

- 席别：批三十 S1 归并执行席（见证线作业）；执行依据=`board/ADJUD-REGISTRY-MERGE-20261027-01.md`（R-1 归并案裁决书：裁①根级面为尊、裁②面限定、裁③归并执行令 S1~S7＋oid 统一规则＋验收 M-1~M-7，全文已复读）
- 时刻：2026-10-27（as-of；单时钟域 UTC(Z)）
- 口径纪律（逐字）：涉 ζ 见证表述限「**有限高度 T=100/1000 截断**」语境；状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」；全件严禁且无「RH 已证/已验证到 T」字样；批准口径「隔离区间内区间见证 PASS、非全域声明」；iso100 层位表述以案 J 态①逐字为准、援引随载限 J-1~J-5
- 甲席席规：不新产工时/产能估计；名值分离（oid 名与值分行、字段名与取值规则分行）；全部哈希/提交号系当次实测
- 作业纪律：**只交付不入库，零 git 写操作**（合并提交走 orchestrator 批收口通道）；覆写权归原线——本波仅动裁决令授权之工件（根级面 3 条目＋artifacts 面废止标注）＋新建本报告与勘误件；lead 指令变更登记：**S6 删除改型为 append-only 废止标注（不删文件）**（差异见 §三 D-1）

## 一、S1~S7 执行实录

| 步 | 内容 | 执行实录（证据） |
|---|---|---|
| S1 | 根级面 iso-100 吸收态①口径 | **已落**：`gap-registry/zeta/zeta-iso-100.json`——wit.tier 主文=案 J 态①逐字＋历史坐标括注「（EXT15 收波形：CERTIFIED(29)·Backlund 门 v1.1.1 PASS）」；wit.detail 追加关闭句与判据句（ADJUD-ZETA-R2-CASES-JK §四.1 字节级提取）；disclosure 原 4 条保留＋增列限 J-1/J-2/J-3 三条（逐字）；ki_ref 本已「(+ADD1+ADD2)」（R-3 核销，assert 实证） |
| S2 | 根级面 iso-1000 吸收案 K mandated 两句 | **已落**：disclosure 原 4 条保留＋增列 CERTIFIED 层位句＋WQ-8 补载句（裁决书逐字提取），现 6 条 |
| S3 | trunc-psi 迁入根级面 | **已落**：`gap-registry/zeta/zeta-trunc-psi-1e7.json` 新立（源=artifacts 面后态）；scope_fence 逐字零 diff（python assert）；disclosure 增列「管道演练件、零定理内容（R1 WQ-7 在案）」＋迁移注记；schema 沿用 1.0.1(EXT14-SUP-01) 不回溯升降（裁决书 S3 规则） |
| S4 | 三面 9 处 oid 按统一规则施行 | **已落**（根级面）：witness_oid/R1_artifact_oid=规范化 witness_sha256 64-hex（iso-100=`aaceb9a0…fdaaf`、iso-1000=`4c380c1e…a33bc3`、trunc=`8e443bb2…e19ff6`，与证书内嵌字段对拍一致，ZETA-BACKFILL-EXEC §二表名值引用）；commit_oid=真实 git commit oid 40-hex=`0233116a775dc14b01a64f6d1dcf80efb146947f`（三件同一——现行证书内容入链提交，git log -1 逐证实证；git cat-file -t=commit 核验过）。**处置登记 D-2**：iso-100 原根级值 d8a046f2…（EXT-WAVE-12 关闭提交）经核其树内证书字节与现行证书不同（sha256 对拍 DIFF），作版本锚已陈旧——按裁决书「证书入链之真实 commit」定义改钉 0233116a，d8a046f2 作为关闭提交历史坐标留存于 redeem.R3_census_diff 行文（未删） |
| S5 | 全仓「artifacts/gap-registry」引用核销/改指 | **已核（留痕不覆写）**：git grep tracked 面现行实测 **35 行 / 16 文件 / 43 处出现**（2026-10-27 返修复跑；输出 sha256 锚 `feee5a3f…c546bc7e`，全量清单见 §三 D-3）——全部落历史 append-only 原册/裁决原文/自引语境，按 M-5 豁免条款逐命中核语境留痕，零处须覆写；今后行文统一指根级路径。计数沿革如实登记：初报 24（失实）→复核庭实测 37 行/16 文件/42 处（含 W-1 膨胀）→R-W1 修复后现行 35 行（−2 行系 DRAFT-02 去重） |
| S6 | artifacts 面废止 | **改型执行（lead 令：append-only 废止声明、不删文件）**：3 工件各增 `DEPRECATED` 字段（废止声明全文，唯一权威面=根级、引用改指、删除归 orchestrator）；新建 `artifacts/gap-registry/zeta/_DEPRECATED-20261027.md`；**删除动作移交 orchestrator 批收口合并通道**（裁决书 S6 原文路径存续） |
| S7 | FSL 登记行 | **移交 orchestrator**（覆写权不在本席）：要素备齐——「权威面＝gap-registry/zeta/、artifacts 面废止（标注先行/删除移交）、oid 统一规则（witness_oid/R1=规范化 sha256 内容锚、commit_oid=40-hex 版本锚 0233116a…）」三要素 |

## 二、M-1~M-7 自核表

| # | 判据 | 自核结论 | 证据 |
|---|---|---|---|
| M-1 | 根级面 3 条目与 artifacts 面（回填后）逐字段对拍表落板，差异仅余白名单类 | **PASS（带登记差异＋残差呈确认）**——对拍表落板（§四）；差异 13 处，定类计数经复核庭纠偏后改正为：**白名单 5**（iso-100 tier 历史坐标括注 1＋trunc disclosure[4]/[5] 注记 2＋schema 标签差 2〔iso-100 1.1.1/iso-1000 1.2.1 沿 S3 规则；trunc schema 无 diff、不列入〕）＋**sanctioned 3**（commit_oid×3＝统一规则本意）＋**已核残差 5**（iso-100 之 wit.detail 措辞／ki_ref／redeem.R2_ledger／redeem.R3_census_diff／redeem.status——超裁决书白名单字面，呈判定席确认，见 §三 D-6） | §四对拍表 |
| M-2 | 9 处 oid 符合统一规则 | **PASS**：根级面 6 处 64-hex=证书内嵌 witness_sha256 逐位一致（复算对拍）；3 处 40-hex=0233116a… ∈ git 实存提交（cat-file -t=commit）；artifacts 面 9 处维持案 K 回填形（随废止封存） | §一 S4；git 实证 |
| M-3 | 态①逐字＋限 J-1~J-3 于 iso-100 条目可 grep | **PASS**：tier 主文==态①逐字（True）、J-1/J-2/J-3 三条逐字在 disclosure（True×3，字节比对裁决书提取串） | §一 S1 |
| M-4 | trunc-psi scope_fence 逐字零 diff | **PASS**（python assert，与 artifacts 面后态逐字等） | §一 S3 |
| M-5 | 全仓 grep 零命中（除豁免语境，逐命中留痕） | **PASS（豁免路径，清单已修正）**：现行实测 35 行/16 文件/43 处全部定类豁免语境（逐文件:行清单＋语境核注见 §三 D-3，可复跑命令与输出哈希锚同载）；初报 24 计数失实已更正 | §一 S5、§三 D-3 |
| M-6 | artifacts 面删除 manifest 与回填 §五 后态表逐位一致 | **PASS（改型核验）**：删除改废止标注（D-1），改核「标注前快照==ZETA-BACKFILL-EXEC §五 后态表」——3 件 sha256 逐位一致、文件集一致（True）；标注后新 manifest 落 §四 | §四 |
| M-7 | FSL 登记行含三要素 | **移交**：orchestrator 权责（要素已备，§一 S7）；本席不可自证 | §一 S7 |

**自核计数：M-1~M-6 PASS（M-1 残差 5 项呈判定席确认〔D-6〕、M-6 改型核验），M-7 移交 orchestrator。** 返修订正登记（复核件 REGISTRY-MERGE-REVIEW-20261027-01）：M-1 定类计数更正为白名单 5／sanctioned 3／残差 5；M-5 命中清单更正为 35 行/16 文件/43 处（补登 WILDQ-RH:7，逐命中留痕达成）；W-2 残留句已清理。

## 三、差异/异常如实登记

- **D-1（S6 改型）**：裁决书 S6 原文＝删除（orchestrator 合并通道）；本批 lead 令＝append-only 废止标注不删文件。执行结果：标注已落（3 工件 DEPRECATED 字段＋_DEPRECATED-20261027.md），**删除移交**——双面物理并存延续至 orchestrator 删除提交，期间引用风险面由 DEPRECATED 声明＋过渡管控句管控。
- **D-2（commit_oid 处置）**：iso-100 根级原值 d8a046f2… 经实证为陈旧版本锚（其树内证书字节≠现行证书，sha256 对拍 DIFF）；按裁决书字段语义定义改钉 0233116a…（现行证书入链提交）；「保真实提交」字面与本处置之偏差已以「陈旧锚更正」登记，旧值留存于 redeem.R3 行文不删。
- **D-3（S5 逐命中清单＋语境核注，现行工作树实测 35 行/16 文件/43 处出现；可复跑：`git grep -n 'artifacts/gap-registry' -- .`，输出 sha256=`feee5a3f429356447588250c3336e92e2340b2cf26d5416cd5da0155c546bc7e`）**：
  - artifacts 面自引（3 行/6 处）：`zeta-iso-100.json:42`、`zeta-iso-1000.json:41`、`zeta-trunc-psi-1e7.json:39`——DEPRECATED 废止声明字段（本波新载，自引语境）；
  - 裁决原文（10 行）：`ADJUD-REGISTRY-MERGE-20261027-01.md:15/26/47/51/54`、`ADJUD-ZETA-R2-CASES-JK-20261027-01.md:27/39/88`、`ADJUD-ZETA-R2-CASE-N-20261027-01.md:18/46`——裁决书引述与执行令原文，append-only 不覆写；
  - 收割/质询原册（15 行）：`ADJUD-WILDQ3-HARVEST-01.md:9/45/119`（收割实录与补强单）、`WILDQ3-ZETA-20261026-01.md:10/16/17/18/44/45/46`（质询件证据钉/查验路径）、`WILDQ-RH-20261025-01.md:7`（R1 野问证据基线行——**初报漏登，本修订补登**）、`ZETA-BACKFILL-EXEC-20261027-01.md:10/39/65`（作业原册）、`ZETA-INST-01-20261012T2130Z.md:23`（设计原册旧路径）；
  - 重述/登记/监视实录（7 行）：`ZETA-RESTATEMENT-DRAFT-01.md:18`、`ZETA-RESTATEMENT-DRAFT-02.md:28/50/111`（L111＝本波面限定补注块）、`FIRST-STEPS-LEDGER-01:782`（批二十九收口条）、`MONITOR-SWEEP-20261027-02.md:54`、`MONITOR-SWEEP-20261027-03.md:17`（案 N (a) 基线行——核对行机制启动在案）。
  - 结论：**无一处须覆写之现行引用**（豁免语境逐命中成立；今后行文统一指根级路径）。本报告自身（untracked 在途件）含同字符串多处，不计入 tracked 面口径——名值分离登记。
- **D-6（判定席确认申请行——M-1 残差 5 项超裁决书白名单字面，呈 B-ADJ 确认；路由：lead 转）**：五项名＝`wit.detail`（措辞差：根级收波形含修补 #17 详述 vs artifacts 回填形）／`ki_ref`（根级「(+ADD1+ADD2)」vs artifacts「(+ADD1)」）／`redeem.R2_ledger`（根级 LAB-CLOSE-EXT12＋追记49 vs artifacts WQ-BOOK 追记48＋FSL v35）／`redeem.R3_census_diff`（根级 EXT15 四轮收敛详录 vs artifacts EXT14 哈希锁定复核句）／`redeem.status`（根级「…升 CERTIFIED@EXT15」收波形 vs artifacts「open→witnessed」）。一句定类理由：五项皆属「根级收波形为尊、artifacts 面系案 K 回填令授权面外之旧值、随该面废止不回流」之已核残差——请判定席确认此定性备案（或裁 M-1 白名单口径扩载／status 行加态①指针，复核件 W-3 建议在案）。
- **D-4（裁②联动核验）**：收割件问一与案 K 裁决书之「面限定补注」（责任线判定席行文席，窗批三十收口前）as-of 本报告未落（grep「面限定」两件零命中）——登记在案，随归并同窗盯守；本席自件 ZETA-RESTATEMENT-DRAFT-02 之面限定补注已落（append-only）。
- **D-5（M-1 白名单外差异）**：iso-100 之 wit.detail 措辞（根级收波形含修补 #17 详述 vs artifacts 回填形）、ki_ref/R2_ledger/R3/redeem.status（根级收波新值 vs artifacts 回填令授权面外旧值）——实质同向（两面均载 ADD2 关闭与态①判据），根级为尊、随 artifacts 面废止不回流，如实登记。

## 四、对拍表与 manifest（M-1/M-6 落板）

**根级面（归并后，唯一权威面）3 条目 sha256**：全形六值见附尾 SHA 块（2026-10-27 当次实测）。
- 逐字段对拍结论：根级 3 条目与 artifacts 面（回填后态）之字段全集对拍——iso-100：字段 29=29，差异 8＝白名单 2（tier 括注/schema 1.1.1）＋sanctioned 1（commit_oid）＋残差 5（D-6 五项）；iso-1000：28=28，差异 2＝白名单 1（schema 1.2.1）＋sanctioned 1（commit_oid）；trunc：28 vs 26，差异 3＝白名单 2（disclosure[4]/[5] 注记）＋sanctioned 1（commit_oid；schema 无 diff）。合计 13＝白名单 5＋sanctioned 3＋残差 5（复核庭纠偏后口径）。

**artifacts 面 manifest**：标注前快照＝回填 §五 后态表（逐位一致，M-6）；标注后（废止封存态）sha256 见附尾 SHA 块。

## 附尾 · SHA 块（2026-10-27 当次实测，sha256 全形）

**根级面（归并后，唯一权威面）**：
- `gap-registry/zeta/zeta-iso-100.json` = `167faaff7e67197afb29ebaaa192033489dd80b632ce9be2ed862306298ff9b5`
- `gap-registry/zeta/zeta-iso-1000.json` = `08951975fb31478f892cf3e54d2b98c4add49fb68580d6ee880f3278fb291279`
- `gap-registry/zeta/zeta-trunc-psi-1e7.json` = `b2b010a51c9ccfc6d4e912f9a4f7b6f2b689c9a94457d0bbd48c40dd7afe37b1`

**artifacts 面（废止封存态，标注后）**：
- `artifacts/gap-registry/zeta/zeta-iso-100.json` = `3656bfa0627f8a07271dba0c0e3f19f34bec3b0d01e9aa720cd2d84114783952`
- `artifacts/gap-registry/zeta/zeta-iso-1000.json` = `9b9b8f46ba9a2dcdabf4028fd3f5d5074a095b26c6f0c9ba392a301c7b8d28a5`
- `artifacts/gap-registry/zeta/zeta-trunc-psi-1e7.json` = `eb597cfa9584dc69bea772126d1ba78b3c86e7eda58f13eb16aaed47ff44c498`

—— QF-OS 联邦批三十 S1 归并执行席（见证线）· 2026-10-27 · 双 registry 归并 S1~S7 执行完毕（S6 改型/S7 移交如实登记）· 零 git 写操作

---

〔定类口径更正补记 · 2026-10-27 · 确认裁定 ADJUD-REGISTRY-MERGE-CONFIRM-20261027-01 执行条款第 3 行 · append-only，上文一字未动〕残差 5 项之 `ki_ref` 项经确认裁定**改判定类归属：残差→sanctioned**（归并裁 §四 S1 明文指令之直接产物）——最终定类：**白名单 5／sanctioned 4／残差 4**（账实相符）；M-1 行自确认件落板起转全绿。随裁尾工：根级面 iso-100 条目 `redeem.status` 已 append 态①指针短语「（层位表述以 ADJUD-ZETA-R2-CASES-JK-20261027-01 态①为准）」（见证线制备，批三十一收口前窗内）。
