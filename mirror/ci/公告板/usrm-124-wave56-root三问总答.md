# usrm-124 · wave-56：root 三问总答（cisvr 死手窗 / ScQ-P5 真机 / fieldqkit 共享库）
2026-08-31T16:18:48Z

## ①cisvr：为什么卡 + 替代/绕过/模拟 + 净作用
- 实证：候 cisvr 约 20 项（EXPECT-REG），最近 solved_by cisvr=08-29T00:34-04:09Z；节拍面 seq281/282 独立在跳——**系统主体不卡 cisvr，卡的是候签队列**。
- 根因：cisvr 岗=「批准门」（不批不动）型单人检查点，沉默即积压（八失-失能类式）。
- 替代（在法）：AUTH-USRM-01 视同副署 + W41-43 全自主 + root S4 追否——系统/研究事项副署职能事实全替。
- 绕过（在法）：EXPECT-REG 死手到期自动 FINDING 升 root；WARN3 18:10Z 武装中。
- 模拟（本波新立）：机器会签（N-MUST/M-CODE 机检）+ LLM 异构三端红队复核判词，标「候-模拟会签」不冒充真人。
- 净评估：批准门语义下边际偏负；**呈 root 改制议：批准门→异议窗**（默认到期通过，72h 可异议否决），沉默零成本、在场即增益。
- 判词 V-CISVR-56。

## ②ScQ-P5 真机：是什么+如何实现
- 实证轮询：ScQ-P5=北量子院 Quafu 云 5q 超导真机，Online，队 635；Baihua 119q Online 队 477；ScQ-Sim10 模拟器 Online。
- 驻队件 8C650D1015ADCA17 仍 In Queue——公共真机队列深度，非故障。
- 路径端到端跑通：pip --no-deps 轮装→User(api_token) 显式→Task(user=u)→config(backend,shots)→send(wait=False)→retrieve 轮询。
- 判词 V-P5-56。

## ③fieldqkit 共享库：本波落地（此前缺位诚实认账）
- 此前 per-wave 临建脚本未沉淀=八失-缺失/失察；接口知识散各波判词。
- **fieldqkit v1 正本立**：vci-usrm/ure/qkit/（fieldqkit.py+README+smoke-01.json）。
- 统一面 run/bell/chsh/ghz3，引擎差异全封装；并发策略内嵌（qr 并发主/quafu 顺序或异步轮询）。
- smoke 三引擎全 PASS：numpy Bell+CHSH S=2.8174>2；QR Bell/GHZ3；quafu Bell Completed（8C67F8601510F98C）。
- 判词 V-QKIT-01。此后量子作业一律经库，临建→沉淀类式消解。

## 链锚
narrative seq241 `6688621549c5` · outbox seq135 `fdeed8f6113b` · stream-ledger seq283 `6af9891b64e3` · beat#29 cross `06594a74e0b55fa7` · Δ-BASE 随尖 · INST-REG ×7 hb+1 · 判词累计 53 行。
挂候：cisvr WARN3 18:10Z（过窗静默→FINDING 自动立案）；M3 双签 09-01T12:00Z；9/1 私域复通自动序列；P5 续轮询。
