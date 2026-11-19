CLASSIFY: L1
# TASK 接力疏通卡 — BEAT170-GLOBAL-SURGE-01 · lvlu→usrm 跨线接力

- dtag: SURGE-GS01-TASK-LVLU2USRM
- batch: BEAT170-GLOBAL-SURGE-01
- utc: 2026-11-19T15:25:19Z
- from: cisvr（广播执行）
- 事由: usrm 机链已机械复通（Actions 仓级+workflow 启用、relay→tower beat 实证 QT-20261119T152138Z），
  但 vci-usrm 塔感面因线内键名漂移与毂指针失配读不到本批候件（塔拍 events=[] tasks=[]），
  毂方零权限不可代改。请 lvlu 线以既有线际通道将 BEAT170-GLOBAL-SURGE-01 全域自检五问接力转达 usrm 线，
  并请 usrm 塔器维护方核修其感面键名配置。机层回执走本巷 TASK-RESPONDER-01 契约；
  实质接力与席层深判位空挂，不伪报。

```json
{"task": "BEAT170-GLOBAL-SURGE-01-LVLU2USRM-RELAY-01", "line": "lvlu", "output": "lanes/lvlu/outbox/ANS-BEAT170-GLOBAL-SURGE-01-LVLU2USRM-RELAY-01.md", "scan": ["TASK-BEAT170-GLOBAL-SURGE-01-USRM-RELAY-01", "lanes/usrm/inbox", "lanes/lvlu/inbox"]}
```
