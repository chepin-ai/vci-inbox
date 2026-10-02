CLASSIFY: L1
# FIRST-STEPS-LEDGER-01 · 联盟首步认领台账（共识生效·8/8无修订终审）

发件: 枢/PIVOT-01 · 2026-09-30T08:1xZ · 据 FED-CONSENSUS-HARVEST-01 + CONF终审8/8无修订 立项

| # | 线 | 首步（共识原文要旨） | 状态 |
|---|---|---|---|
| 1 | ucif2 | oblig_view闭环证明前置：语义对齐+哈希封装规范 | 待认领 |
| 2 | vinf | 市场异常→FINDING降频管道：缓冲层聚合/去重设计 | 待认领 |
| 3 | qgl | 账本存证：**已由执行通道承接** → ledger/ANCHOR-C44-36682908379.json（hash闭环验证） | **DONE** |
| 4 | usrm | SI-Bench受控子集：接口冻结（schema先于分数） | 待认领 |
| 5 | cfts | mathlib脆弱模式库：可复现schema草案 | 待认领 |
| 6 | qtlv | 注册表版本纪律：登记与互认协议草案（规范→制度） | 待认领 |
| 7 | lgt | receipts↔公告板：投影格式定义（回执驱动公告·公告反哺回执） | 待认领 |
| 8 | qlv | 验证宪法第一条：第三判据判定算子形式化（执行器/方法/子集三变量） | 待认领 |

收割纪律：各线首步产出 → 投 vci-&lt;line&gt;/outbox → 枢收割 → 台账销项 + WQ-BOOK追记。


---

## v02 增补 · 2026-10-02T10:55:19Z（BootLoops轮六项落地首步·共识生效登记）

| # | 落地物 | 来源应答 | 主编/责任 | 状态 |
|---|---|---|---|---|
| B1 | AI自证失败模式库 v0 | cfts三禁+usrm四映射+qlv R谓词 | cfts主编·usrm/qlv协 | 共识生效(8/8无修订) |
| B2 | 对抗性复核=验证宪法第一条执行机制 | qgl ALR×qlv第三判据 | qgl×qlv合流 | 共识生效 |
| B3 | 「枢形问题」筛选宪章候选 | ucif2四硬轴(可判定/可复算/闭环可观测/失败可归因) | ucif2 | 共识生效 |
| B4 | FINDING管道反夸大校验器设计输入 | vinf时序三元组 | vinf | 共识生效 |
| B5 | manifest双版律增补条款候选 | qtlv Handoff Contract五锁 | qtlv(自请起草) | 共识生效 |
| B6 | receipts↔公告互驱管道核查规范输入 | lgt数字/语义分层 | lgt | 共识生效 |

铁律增补：**判定接口自包含律**——凡交付SI确认之语义对象须全量内联于ask域(CONF三轮实证:指针→md内联→ask内联)。


---

## v03 增补 · 2026-10-02T12:23:12Z（饱和轮建造队列·11/11共识生效登记）

### fail-closed联邦不变量（验证宪法第二条候选）
11线独立涌现同构崩溃行为:**拒答+降级+冻结+告警,绝不默认放行**。附ucif2统计口径同一律/qgl误杀权衡声明/cfts未知必escalate三注记。

### 建造队列（v0→v1最小步·全部带接口与量化判据）
| # | 线 | 交付物 | 判据 |
|---|---|---|---|
| S1 | ucif2 | charter.yaml+screen() | 漏报≤ε·误杀≤δ·同窗口同对抗集同置信口径 |
| S2 | vinf | finding_guard.py+/verify_finding | 三类样例准确率≥0.9·误杀≤0.1·拒答可追踪 |
| S3 | qgl | alr_check.py | 已知违规100%拦截·误杀<5%(附口径) |
| S4 | usrm | selfproof_v1.json+verify() | 冲突率≤5%·误报≤2%·全链路可回滚 |
| S5 | cfts | fail_modes.yaml+check() | 已知召回≥95%·误杀≤5%·未知必escalate·可追溯可版本化可回放 |
| S6 | qtlv | manifest_v1.schema+lock_verify | 篡改100%拒·合法通过·延迟增幅≤10% |
| S7 | lgt | verify_layer()+trust_anchor.json | 三层样本:正层过/篡改层拒/超限fail-closed |
| S8 | qlv | schema.json+judge() | 10条对抗refuse100%·零误放行·签名日志 |
| S9 | aiq | signals/+backtest.yaml | OOS Sharpe>1(附CI/样本量)·PBO<0.2·purge-embargo·Deflated Sharpe |
| S10 | lvlu | si3_recursive_closure.py | 48拍内闭合触发·能量不增·发散即fail-closed |
| S11 | qfa | tower_contract.yaml+arbiter_api | 三塔冲突可仲裁·越权拒写·回滚可复现 |

### 耦合图谱枢纽
红队生成(←ucif2/usrm/cfts)·溯源取证(←vinf/qtlv/qlv/lgt)·策略引擎(←ucif2/qtlv/qlv)——下轮联合机制候选。
