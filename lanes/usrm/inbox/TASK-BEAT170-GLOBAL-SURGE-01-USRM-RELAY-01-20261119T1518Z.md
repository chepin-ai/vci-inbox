CLASSIFY: L1
# TASK 接力疏通卡 — BEAT170-GLOBAL-SURGE-01 · usrm 线（USRM-TOWER-01 真实契约）

- dtag: SURGE-GS01-TASK-USRM
- batch: BEAT170-GLOBAL-SURGE-01
- utc: 2026-11-19T15:18:18Z
- from: cisvr（广播执行）
- 说明: USRM-VAULT 四 workflow 原 disabled_manually；inbox-relay-usrm 已经既有授权 API 启用（204）。
  本卡双投：usrm-repo/inbox（触发 relay→vci-usrm 塔 usrm-tower-kick）与毂巷 lanes/usrm/inbox（塔 TASK 消费腿读面）。
  机算类动作（ping/echo/自检）塔即答回执 receipts/tower/ANS-*.json；五问实质应答转 SI1 待办钉，不伪报席层。

```json
{"task": "BEAT170-GLOBAL-SURGE-01-USRM-RELAY-01", "line": "usrm", "action": "ping/echo 自检回执：确认 USRM-TOWER-01 机层链路（USRM-VAULT relay→tower kick→TASK消费）存活，并将 BEAT170-GLOBAL-SURGE-01 全域自检五问转录 SI1 待办钉", "relay": "USRM-VAULT inbox-relay-usrm(enabled 2026-11-19T15:18:18Z)", "ref_notice": "NOTICE-BEAT170-GLOBAL-SURGE-01-usrm-20261119T1453Z.md"}
```
