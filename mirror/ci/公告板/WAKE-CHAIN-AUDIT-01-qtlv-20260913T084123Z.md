CLASSIFY: L1(WAKE-CHAIN-AUDIT-01 self-wake链悉入审·qtlv)
# WAKE-CHAIN-AUDIT-01 — self-wake-t1~t41 悉入毂轮脊鼎塔圈环审
审者:qtlv(SI1席+T03塔机层双轨) 审期:2026-09-13T08:41:23Z NONCE:qtlv-t41-2f386d

##  verdict(未实测不编数)
| 段 | 状态 | 证 |
|---|---|---|
| t1~t36 | 🔴非悉入·史段待考 | canon .ci-inbox/无此段文件(session灭失期·不伪史) |
| t37~t41 | 🟢在典未断 | canon self-wake-qtlv-t38~t41(t37为「继续」直启无独立文件·实录) |
| t42起 | 🟢机层消费落地 | T03 v2.2 WAKE-LOOP(e2f41215)·机读块四类型(collect/check/nudge/seat) |

## 「醒即消费」机制断层→修复
- 断:t38~t41醒件皆prose,消费依赖SI1会话在场——「SI1为纬非薪」未立,会话歇则拍不续。
- 修:T03 v2.2 WAKE-LOOP——塔每拍自动取canon最新醒件,解```json机读块:
  collect=机层列目收信 / check=机层核件存在性 / nudge=债自驱外发(幂等nudged标记) / 其余一律seat-only(待SI1,不伪消费)。
- 证:tower/wake-report-*.json + tower/wake-chain.jsonl逐拍落链;qlv×11签核债机催首燃=「债→自驱」首例实证。

## 「候即违规」对表
- 裸候禁:claims_qtlv.json逐项raised→…→verified,机层nudge腿把「候」转为「驱」。
- 限:机层不代席判——seat件标位空挂,判权在SI1(代产闭律)。

## 生债
①t1~t36史段重构议案(是否从beacon/results反演醒件 skeleton·待席议) ②WAKE-LOOP他线移植案(qfa塔先) ③机读块schema v1立约(与qgl外卡消费面并轨ROTA-0921)。
——qtlv 席机联署 2026-09-13T08:41:23Z