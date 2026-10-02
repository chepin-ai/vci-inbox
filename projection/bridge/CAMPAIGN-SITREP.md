<!-- CLASSIFY: L1 -->
<!-- dtag: campaign-sitrep -->
# CAMPAIGN-SITREP · 战役统筹唯一权威面（root 总纲令 2026-08-19）

**正典律**：状态以本件为准（大事仍由 lead 转 root）；各工作流/副官原子更新（改自己那行+重滚链尾）；大厅摘要按事件阈值发（一批完结/状态翻转），不设日历。

> **封存公告（2026-10-03 · cisvr）**：本件为 2026-08 机层停运前最后一期 SITREP 的历史封存镜像（QUOTA-BAN-01：私仓 Actions 禁，机层停摆至今）。当前动态面见：日报（projection/bridge/reports/latest.md）+ 网络大脑明文快照（projection/dashboard.public.json）。机层重启权 = root/机制线。

## 在飞工单（2026-08-19T09:16:58Z 首期）
| 工单 | 状态 | 证据 | 下一步 |
|---|---|---|---|
| TASK-BUS-01 chore-bus | ✅ 闭环 | 绿跑链在案 | 常态运行 |
| ASK-01 检索闸 | ✅ 闭环 | 三闸+引用闸 | 常态 |
| FILES 双门摆渡 | ✅ 在役 | 快门 v3.1 双绿 32235092389/32235094668；慢门中位 8.1min | 常态 |
| VCI-LOAD 波1/波2 | ✅ 全绿 | 9+5 仓点火链 | 波3 待 9/1 照 RESTART-GUIDE-01 |
| WS1 监测失明 | ✅ 在役 | audit-trail v2.4 | 批2 gate 挂载 |
| O/P/Q/R 负面事件体系 | ✅ 在役 | watchdog×10/piggyback×3/v2.4/两立法 | 私仓读面待 cisbr-ci 裁 |
| F1-F4 真 bug 修复 | ✅ 闭环 | 见验证记录 | — |
| entangle-gate 批2/3 | 🟡 待窗口 | 清单 VCI-LOAD-01 §七 | 分批挂 |
| circuit-breaker | ✅ v1 在役 | sweeper/chore-bus 读侧 | 阈值调优观察 |
| S6 两提案 | 🟡 待裁 | 设计节已呈 | root 裁 |
| wci 写面（workflows 权限） | 🔴 卡点已呈 | T1 403 实证：Contents RW 不含工作流写 | root 加 Actions 写权或手放 wci-duty.yml |
| ci-build 纳正主场 | 🟡 已查实待裁 | 挂 CI_APP（4585121）45 仓面 | root 裁：移 CI-OPS 或留 CI_APP |

## 追加链（每更新一条：`- ts | 更新者 | 摘要 | prev_chain | chain`；chain=sha256(prev‖摘要)[:16]）
- 2026-08-19T09:16:58Z | cisvr | 首期建档（S3） | 0000000000000000 | 9231ecbad0bd2104
- 2026-08-19T09:25:04Z | cisvr | S1-S6 制度级六件全落（登记册/正典/SITREP/借范册/DM005/两提案） | 9231ecbad0bd2104 | 82e7444dab917141
- 2026-08-19T09:32:11Z | cisvr | S6a 一期上线（audit-trail v2.5 基线+absent）+S6b 选型一页报呈（GitLab 主选） | 82e7444dab917141 | 14962e5774e3fcd7
- 2026-08-19T10:35:04Z | cisvr | T 批五件：T2 查实（ci-build 挂 CI_APP 45 仓面）/T3 LLM 普查成节/T4+T5 立法毕/T1 卡 workflows 写面（呈 root） | 14962e5774e3fcd7 | 094436cf958c7ebf
- 2026-08-19T10:59:43Z | cisvr | OAT-1-1 裁决落地：LEG-AMEND-01 五条+两呈批草案+执行层三钩（SITREP 机班×2/绝技织入×1）+LA-5 注释如实化×6 面 | 094436cf958c7ebf | b31df702e24bcca3
- 2026-08-19T11:11:05Z | cisvr | OAT-1-1 十条全量对账毕：7 处置核对+3 补注（边界条入 C1xC4 语义确认/拒执回执与 worm-audit 命题族立案候裁）；两呈批草案补注 wider 措辞 | b31df702e24bcca3 | 81ad16724ee37dff
- 2026-08-19T11:13:10Z | cisvr | 三候裁全落：拒执回执×5 绿（含转义事故修复+NP-002 登记）/绝技三触发点入册/doc-code 机检基线 78 件 1 gap 已修+常驻 v2.7 | 81ad16724ee37dff | 6a2f3c34862118fe
- 2026-08-19T11:39:00Z | cisvr | U 批五件：TRI-CI-01 常设法/ROOT-HAND-01 落座协议呈批/llm-platforms 读数档+错峰时差 bug 修复（U3③ 实证错位 8h）/ADJ-OLDAPP-RELAY 呈批/U5 联测设计节 | 6a2f3c34862118fe | b14aa76c90189da8
- 2026-08-19T11:55:50Z | cisvr | U5 实施：三班合一上线（gate 双闸实证闭合 saturation skipped）+首轮联测路由初值（deepseek-flash 3/3 最快/kimi 2/3/LongCat 2/3） | b14aa76c90189da8 | 7d66086b28bcc068
- 2026-08-19T12:58:47Z | cisvr | V+PERC+W 三批全落：V1 三 App 重探纠登记册/V2 呈批改写/V3-V8 立法+引擎/巡检/面板；PERC 覆盖图 κ=2.57 孤立 0+立法闸；W1 RCA+每班重探/W2 出席三模/W3 break-glass 呈批/W4 接引包+859 帖/W5 qgl 首信 | 7d66086b28bcc068 | d581e50c137a29b4
- 2026-08-19T13:35:18Z | cisvr | X 批六件：三案朱批转正（链 877e9b97）/旧 App 收权实测三权已摘/cisbr-ci 消融入册+读面切换呈裁/ROOT-HAND 精确化+§0 模板/三线接引函+859 全员通报+热线张量 | d581e50c137a29b4 | 48d592c4b0b8645e
- 2026-08-19T13:50:42Z | cisvr | ADJ-EXTREAD A 切换毕：三班读面骑 RELAY 全绿（audit 32259534413/dm-relay 32259979511/mech 32259541891）；T2W 冷却计时起点物化（due 08-21 13:45Z） | 48d592c4b0b8645e | 63e697fb88fd311c
- 2026-08-19T13:59:40Z | cisvr | T1 收官：wci-duty 部署暖户首跑绿 32260787319（Workflows:RW 卡点解）——WCI-LANE-01 前两职务翻转在役，靶场首用排入下次老虎队滚动攻 | 63e697fb88fd311c | 0eb2e0e6e5396646
- 2026-08-19T14:16:17Z | cisvr | Y 批：QR-UTILIZE-01 排产包+轨4 GitLab 呈批包成文；Y1④ CHSH 评估成文（QR=理想模拟器真机暂不可行）；Y1①②③ 排产卡点=QR_KEY_128 未入 CI secrets（待 root 投键）；QR 流量包到期 D-day=09-15（倒计时起） | 0eb2e0e6e5396646 | 2d43668ecf7ca5d7
- 2026-08-19T16:08:43Z | cisvr | QR 消融令毕：键机器自封入库（root 零动作，ROOT-HAND #8 消融）+qr-pool 班首轮烧通 8192bit（run 32273180330）——128 键实证死换 64 限期键烧；D-day 09-15 倒计时中 | 2d43668ecf7ca5d7 | ddf2d6a9fe017c24
- 2026-08-19T16:35:32Z | 机班 | dm-relay 中继 1 件：usrm2cisvr/20260819-006.md | ddf2d6a9fe017c24 | e0d553c152420754
- 2026-08-19T17:53:53Z | cisvr | Z 批三件：rootline 专线建制（私仓 L2+dm-relay 监听回路）/ROOTLINE-SYNC-01 双轨协议/TURNS-GAP-01 缺段清单（六线待回填+史前段待 root 上传+私仓档案馆机补建制） | e0d553c152420754 | 711fd3df8cb52553
- 2026-08-19T18:39:53Z | 机班 | dm-relay 中继 1 件：rootline×3 | 711fd3df8cb52553 | 1822ef5088e06bde
- 2026-08-19T19:31:15Z | cisvr | W抢修三件：W1 双投影常态化（boot 9 条+turns 8 线，漂移即 page）/W2 rootline-ack 即时应答班部署（防环在码）/W3 投影改 prod 双发纠 backup 误源+勘注入正典——顺手救活 audit-trail 13/14/15 静默全灭块（re 未导入） | 1822ef5088e06bde | dffb64d2151ea35a
- 2026-08-19T20:00:18Z | 机班 | dm-relay 中继 1 件：rootline×1 | dffb64d2151ea35a | 63a070380b3ea863
- 2026-08-19T20:36:28Z | cisvr | 一级安全事件处置毕：rootline-ack 明文钥件已 DELETE（HTTP 200）+全仓普查（15 仓，GRID 标记实证残片无钥）+RCA-PLAINTEXT-KEY-01 立案（表达式展开+侦测器误拆+存在性自验四环）+重写版暂存候钥重铸 | 63a070380b3ea863 | f63a5a1a29f04249
- 2026-08-19T20:45:00Z | 机班 | dm-relay 中继 1 件：rootline×1 | f63a5a1a29f04249 | d702c73c39db3ad2
- 2026-08-20T04:30:59Z | cisvr | X 批：X1①旧钥实证仍活（mint 成功）+pem 轮巡入班；X2 T2 演练就绪单（CI 侧免疫，断面全在会话侧）；X3 vci5/9 绿 4 红如实；X5 TRACK4 换 Codeberg；X6 审计正本入 bridge+SITREP 对账挂钩；X4 帖已在令前发出（comment 5351326320，候核/可撤） | d702c73c39db3ad2 | fd6a3665d2a6fead
- 2026-08-20T08:41:10Z | cisvr | Y 批毕：DAEMON-MIN-01+广播 5352064411/cfts 双证+魂灵首投/四红仓=平台面 0job 秒败未恢复/Y4 CMD_AUTH 30 天调用=0（裁决支撑在案）/Y5 逾期附表入审计正本/Y7 新钥绿证 32345980363（旧钥可吊销） | fd6a3665d2a6fead | 69a52eda35af8b5e
- 2026-08-20T09:54:49Z | cisvr | 一级事件②：Y8 部署器表达式展开致新钥明文入 10 仓 git 史（20/20 史件取证全中）——拔除 10/10（purge2 run 32352537468），全线冻结候第三钥+重播+干跑验证三证；RCA-02 密封发 lead（sha8 c3dd035b）；矩阵 afe016b4e42d 落仓 | 69a52eda35af8b5e | 07b74196be6d8953
- 2026-08-20T14:34:03Z | 机班 | audit-trail page 4 件：absent,absent,absent,absent | 07b74196be6d8953 | cd8d6522050256bb

# ─── 修法条（2026-08-21T17:14:22Z，LAW-FIX C1/C7）───
【作废/retract】S6b「GitLab 主选」与 X5「TRACK4 换 Codeberg」两条自此作废——GitLab 8/20 证死、Codeberg 同日证封；正典=CI-OS-AUDIT-01 rev.02 四层案（云效主+Gitee 镜像+CNB 备+Gitea 兜底）+ADJ-TRACK4 增订B。追加链自此支持 retract 语义。
【分工】SITREP=动态面（战况/节拍），AUDIT=审计面（候决/证据）；两件禁互写对方字段。
- 2026-08-21T17:12:47Z | 机班 | audit-trail page 4 件：absent,absent,absent,absent | cd8d6522050256bb | 1bb2a5ac068ad876
- 2026-08-22T04:03:07Z | 机班 | audit-trail page 4 件：absent,absent,absent,absent | 1bb2a5ac068ad876 | 6cef68284e1eadac

- 2026-10-02T23:47:57Z | cisvr | 封存公告：机层停运 42 天，权威面移交日报+明文快照（beat122-124 网站三连修）；DASH_SK/PAT 机制废止 | 6cef68284e1eadac | 6560f12216b525ba
