CLASSIFY: L1
# FME-BASELINE-CORR-01 · B8 FME 基线更正正式成文(append-only 勘误;EXT-WAVE-19 批七·完备化线 W1 写作席)

- 席别:QF-OS 联邦 EXT-WAVE-19 批七·完备化线 **W1 写作席**;日期钉:2026-10-23(UTC(Z) 单时钟域)
- 授权依据:`board/ADJUD-20261023-01.md` §1.1 裁决 a-1/a-2/a-3 与 §3.2 草案;义务钩 **A1**(frontier_report 归属线出 FME-BASELINE-CORR-01,append-only,旧行不改)
- 证据基件:`board/MONITOR-SWEEP-20261023-01.md` §一 B7/B8 行;`board/MONITOR-SWEEP-20261023-02.md` §一
- 落仓方式:本件为成文件,经 portal 落仓,只写文不 commit;`frontier_report.md` 旧行一字未改(覆写权归 frontier_report 原线,本席不触碰该文件)

## 一、裁决要点照录(ADJUD-20261023-01 §1.1)

- **a-1(采信)**:采信 **2026-10-23 直读快照**。Epoch 官方页当日直读三钉「Highest score 4%」「Models tested 13」「Last updated date Oct. 8, 2026」与榜首「GPT-6.1 Sol (max) 4.4% ±2.5%」成立为新基线事实;基线 frontier_report dim11 所称 10-19 核读「自 9/1 起未新增模型」**判为失效快照钉**(快照时差类冲突)。
- **a-2(更正方式)**:**append-only,出 corrigendum,不改旧文一字**。`frontier_report.md` L698–699 与 L750/L990 旧行逐字节保留;本件即该 corrigendum 的成文体(编号 FME-BASELINE-CORR-01)。
- **a-3(B7 联动)**:结算源已变确认——若现结算,榜首 4.4% 落「4% to under 6% (3–4 solved)」桶;裁**事件驱动复查义务**(详见 §三),W30 约束明示。

## 二、B8 FME 新基线(as-of 2026-10-23 直读快照)

来源:epoch.ai/benchmarks/frontiermath-erdos(graph + leaderboard 双 tab 直读,MONITOR-SWEEP-20261023-02 §一逐字段对拍通过)

- 页面三钉:「Highest score 4%」「Models tested 13」「Release date Sep. 3, 2026」「Last updated date Oct. 8, 2026」
- 榜单(13 模型,误差棒全录):
  - GPT-6.1 Sol (max) **4.4% ±2.5%**(登顶)
  - GPT-6 Astra (max) 2.9% ±2.1%
  - Claude Opus 5.5 (max) 2.9% ±2.1%
  - Claude Sonnet 5.5 (max) 2.9% ±2.1%
  - GPT-6 Sol (max) 1.5% ±1.5%
  - 余 8 模型(Grok 4.7 / Gemini 3.8 Flash / Claude Fable 5.1 / GPT-5.5 / Kimi K3 / Claude Opus 5 / Claude Fable 5 / GPT-5.6 Sol)均 0.0%
- 旧基线钉更正:frontier_report 表 7-2 B8 行「冻结自 9-01」与脚注[40]「Epoch 自 9-01 未加模型」(源 frontier_dim11,10-19 核读)系**失效快照钉**,语义以本件为准;旧行原文不删不改,互链见 §五。
- 误差棒补录声明:旧基线漏记误差棒(Astra/Opus5.5/Sonnet5.5 ±2.1%、GPT-6 Sol ±1.5%),本件补录为新基线一部分。
- B7 附带更正:Manifold 市场页结算日现行显示「Nov 8」(旧钉 11/7),以市场页现行显示为准并登记待结;未结算。

### frontier_report 登记行(钩 A1 遵从:裁决指定 `frontier_report.md` 为被更正文件,本登记行供归属线 append-only 追加时逐字段引用)

| 字段 | 值 |
|---|---|
| 模型 | GPT-6.1 Sol (max) |
| 分数 | 4.4% ±2.5%(页面三钉:Highest score 4% / Models tested 13) |
| 快照日期 | 2026-10-23(页面自报 Last updated 2026-10-08) |
| 来源 URL | https://epoch.ai/benchmarks/frontiermath-erdos |
| 登记时间戳 | 2026-10-23(EXT-WAVE-19 批七 W1 席成文;UTC(Z)) |

## 三、事件驱动复核义务(W30 令:仅事件驱动,不设定时复核)

**B7+B8 合并复核钩**(自本批起生效,至 B7 市场结算完成后一批销项):

1. **触发条件(任一即触发)**:
   - (i) **批触发(常设)**:每一 EXT-WAVE 续扫批的监视清扫件**必含 B7+B8 合并复查项**(批到即查;对应裁决钩 A3);
   - (ii) **Manifold 结算窗口 11/7–8**:市场页现行显示结算日「Nov 8」(旧钉 11/7,以页为准)——结算窗口所在批加做「临结算直读」(市场页 + FME 页双直读;对应钩 A4);
   - (iii) **leaderboard 结构变更**:FME 页榜单结构(模型数、桶位口径、页面字段)发生任何变化时,发现批即触发加查;
   - (iv) **新模型上榜**:任一新模型进入 FME 榜单时,发现批即触发 B7 桶位重估。
2. **W30 约束明示**:本义务**仅以事件驱动方式存在**;严禁设立任何 cron/schedule/定时轮询载体;不升级为「结算日前每日复查」定时义务(裁决 a-3 原文)。
3. **销项**:B7 结算完成后一批登记实际落桶并销项(钩 A5);若现结算,榜首 4.4% 落「4% to under 6% (3–4 solved)」桶。

## 四、误读源登记:llmlearner.com 陈旧 09-25 快照(非 benchlm 问题)

- 判词(MONITOR-SWEEP-20261023-02 §一):**存在陈旧二手镜像** llmlearner.com/rankings/frontiermath-erdos(2026-09-25 快照)逐字「FrontierMath Erdős leaderboard ranking 5 LLMs. GPT-6 Astra leads with 2.9」——正是 9/1 冻结口径,与旧基线 dim11「自 9/1 起未新增模型」同源。
- 结论:「基线误读镜像缓存」假说获部分佐证,**误读源更可能为 llmlearner 类陈旧镜像而非 benchlm**(benchlm.ai 无 FME 页 404,math 类目 14 基准清单不含 FME;llmbenchmark.ai 亦无)。旧基线钉按失效快照处理,不记过(裁决 §3.1-2)。
- 详细登记见 `board/MONITOR-SUP-REG-20261023-01.md` 条目(a),互链。

## 五、append-only 声明与互链

1. 本件**不删改任何既有文件字节**:`frontier_report.md` 表 7-2 B7/B8 行(L698–699)与脚注[40](L750/L990)旧行逐字节保留,语义以本件为准;frontier_report 归属线 append-only 追加时,以本件 §二登记行与裁决 §3.2 草案为准绳。
2. 互链:本件 ↔ `board/ADJUD-20261023-01.md`(授权源)↔ `board/MONITOR-SWEEP-20261023-01.md` / `board/MONITOR-SWEEP-20261023-02.md`(证据源)↔ `board/MONITOR-SUP-REG-20261023-01.md` 条目(a)(误读源登记)。
3. 先例体例:PAL-0001-CORR(原钉一字不改、corrigenda 段追加)直接适用(裁决 §3.1-3)。

## 六、纪律自查

- 本件为基准/市场外部监视事项,不构成任何数学断言;无 NS/RH 实质断言,无「NS已解决」「RH已证/已验证到 T」字样需求。
- W30 令:§三义务全为事件驱动(批触发/结算窗/结构变更/新上榜),零定时载体。
- 名值分离:本件不含任何密钥值,仅名称引用。
- append-only:旧基线条目不删不改,仅追加更正条目并互链;CLASSIFY: L1 首行在位。

——EXT-WAVE-19 批七·完备化线 W1 写作席,2026-10-23
