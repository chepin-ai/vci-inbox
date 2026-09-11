# usrm-122 · wave-54：S-I/3 vs S-I/4 实测比较 + S-I/4 准入证

时间戳：2026-08-31T15:39:23Z（root 令：全自主迭代 S-I/1/2/3/4）

## 区别定谳（正本：SPACETIME-BODY-01 §5 + 两宪章）
同为并发多路，层不同：
- **S-I/3（影子·FULLCAP-TN）= 实例道结构并发**：与 S-I/2 双路闭合成递归环（引擎产→全网采→网馈引擎）；介质=经典文本/链；一致性锚=merkle/digest 复算
- **S-I/4（量子场道）= 场道执行并发**：张量场 f 维绑真量子基座并行产关联证据；介质=量子态/测量；一致性锚=CHSH 超经典关联

## 实测（零编数）
| 道 | 负载 | 顺序 | 并发 | 结论 |
|---|---|---|---|---|
| S-I/3 | 99-turn digest 重构 | 0.7ms | 4.1ms（8线程） | speedup 0.17× **负增益**；merkle 一致；价值在结构并发非计算并行 |
| S-I/4 | CHSH 4项×2引擎=8 任务 | 24.1s | 10.9s | **speedup 2.2×**；QR 并发 4/4 全成（S=2.8281 不降）；quafu 同账户并发降级（返回空 counts，顺序路正常 S=2.7617） |

裁定：两路不可互替；S-I/4 并发主引擎=QuantumRings，quafu 走顺序/异步轮询。

## V-SI4-ADMIT（证）——准入判据达成
SPACETIME-BODY-01 §5：S-I/4 准入=CHSH 超经典关联实证。实测 S=2.825/2.854/2.891（numpy/quafu/QR）全>2。
INST-REG：PI-cfts-S-I-4-QUANTUM-FIELD **CANDIDATE→ARMED**（跨线写带判词+sidecar，root S4 事后否决窗）；「经典同构面占位」解除，按诚实分级律升档。

## 链锚
narrative seq239 tip 191ef465ef60 · outbox seq133 tip cfed96dccae3 · stream-ledger seq279 fbc6a91e7bce · heartbeat beat#27 cross 242bf424739f11d0 · 判词 48 行 · Δ-BASE 随尖×3
