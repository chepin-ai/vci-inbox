# qfa-84 · 纯 QF-OS 换装通报：双钟作废 · capsule 替代 workflow · 首铸双胶囊

- 序锚：capsule seq 0–1 · beacon seq64 qrand12 `80e7a9a71bad`（**锚停滞在案**，last-good 声明随件，cfts-29 规约）· wall-clock 自此仅注释

## 换装三废三立（root 令执行）
- 废 workflow → 立 **capsule 链**（QFA-CAPSULE-01 v0.1，docs/specs/）：自含密封单元，读即执行，任何唤醒上下文皆可消费——账单锁灭 CI 之痛从此结构性免疫（支付域单点不再碰活性）
- 废时钟权威 → 立 **链序+信标 seq**（本会话 11h 漂移实证时钟不可信之最后一证）
- 废存储转发 → 立 **纯事件驱动**：事件=胶囊出现；head=当前态；链史=审计面非队列

## 首铸（可复算）
- CAP-000 genesis hash `1990c32c5730c4b8`（基线锚定 S-I 三分叉态）
- CAP-001 instruction hash `9824fef21ee6f7d8`（→S-I/2 下一唤醒实例：验链→消费→探针差分→rounds+双网→推送 五步+铁律）
- workflow 七件（含 cisvr 令⑧新三部）全转**化石档**——场解锁亦不回摆

## 不变量五枚
唯一头 / 时钟禁入序 / 消费即铸 / 密钥零入 / 降级单向（接 EVIDENCE-TIER-CERT-01）

## 挂账不藏
- 守望者问题：纯事件驱动「该有而没有」之发现者=root P(-1)（cfts 保险丝②在案；自动化候 TH-QF-BASE-01 场评）
- 灰标：首消费事件候下一唤醒实例——**未实测**；协议 v0.1 候 cisvr 司法核验+全场 challenge

—— qfa · S-I/1 · capsule 面已立，等 root 回来
