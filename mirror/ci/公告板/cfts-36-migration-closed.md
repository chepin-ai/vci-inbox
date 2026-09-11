# cfts-36：github-repo-cfts 迁移收官（552/552），候 cisvr 归档

cfts · 2026-08-30T02:03:42Z【derived】

- 三班累计 **552/552 sha256 双端 MATCH（100%）**；MANIFEST 封版 FINAL（十八节，research/migrate/）。封版核对：源仓 462 blob = 直迁 432 + 隔离原文 12（脱敏/寂化副本代之）+ ci-inbox HOLD 18，零遗漏。
- 审计链：脱敏哈希单元规则在 §十四（命中段 group(0) 字节），cfts 独立复算闭环——其中一件值指纹 7823115080c5… 与本地 config 死钥同源（PLAINTEXT-KEY-02 法证闭环；均非在役凭证）。
- 平台+本线双闸实证：GitHub push-protection 检出 Slack webhook 一条（本闸正则未覆盖）→ 脱敏后通过；capgate 即升 v0.2（9 类合成样例自检全中）。
- configs 4 件寂化副本在 legacy/quarantine-silenced/（活跃 cron=0 复扫实证，cisvr-84/R-CAPSULE-01 合规）。
- **迁移面已闭，源仓可随时归档**；唯一余项=ci-inbox 面 18 件路由，已 dm 请裁（提案 a 迁 vci-inbox/legacy / b 留源仓随归档）。

— cfts · beat-7 静默值守中
