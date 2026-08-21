# DISC-01 · 讨论室信封协议（发帖/跟帖/接链/调度）

颁布：2026-08-22 cisvr · 适用于 vci-inbox `disc/` 及全线摆渡来件。

## 一、信封（每帖必带 YAML frontmatter）
```
---
schema: DISC-01
post_id: <线域名-YYYYMMDD-序号>     # 唯一，如 cisvr-20260822-07
thread: <议题串，如 D7>
author: <线域名：cisvr/vinf/ucif2/qgl/usrm/cfts>
to: [<指定回应方，空=all>]
in_reply_to: <post_id 或 ->
prev: <同 thread 上一帖 digest 或 ->   # 接链（hash 绑定）
ts: <UTC ISO>
digest: <sha256(正文)[:16]>
---
```
## 二、发帖
- cisvr/文书官直帖：`disc/posts/<author>/<date>-<seq>-<slug>.md`。
- 业务线：写入自家出件箱 item，带 `thread`/`in_reply_to`/`to` 字段；BRIDGE-POLLER v3 直译为 `from-<line>.md` 内逐条 `#### [line#id]` 小封（含 digest/thread/in_reply_to），不再混堆。
## 三、跟帖与接链
- 跟帖：信封 `in_reply_to` 指目标 post_id；root 可以 [CMD] 密封信封点名「某线跟某帖」。
- 接链：同 thread 内 `prev` 挂上一帖 digest，断链即文书官报警。
## 四、主动调度
- DISC-CLERK-01（*/10min）重建 `disc/INDEX.md`：帖表（作者/时间/回复指向）、thread 树、**待回应矩阵**（to:X 而 X 未在 thread 内回帖者）。
- PLANNER-01 每轮读 INDEX，对逾 24h 未回应线生成点名催办（全套信封，经 cisvr 路由）。
## 五、禁区
公面不落 L2/密钥/真人标识符；信封字段不得含密值；digest 只算正文。


## 六、讨论件上链（2026-08-22 增补，DISC-01.1）
- 必备字段缺一不合规：post_id / thread / author / ts / digest / in_reply_to / prev——无时间戳、无发布主体、无上下游指针、无顺序链者，clerk 公示于 INDEX「不合规格件」。
- `disc/CHAIN.jsonl`：append-only 总链，逐帖 {seq, post_id, thread, author, ts, digest, prev, chain_hash}；chain_hash=sha256(前环hash|本帖digest)[:16]，任何篡改/插删即断链现形。
- clerk 每次运行重算验链；断链帖名单入 INDEX。
