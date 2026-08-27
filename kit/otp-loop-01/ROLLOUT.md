# OTP-LOOP-01 ROLLOUT · 每线落地矩阵（2026-08-27, usrm 应 root 令制）

| 线 | 循环仓（私仓，OTP secrets 在仓 per root 汇总） | 公锚镜像仓 | 状态 |
|---|---|---|---|
| ucif2 | ucif2-formalization-kernel | vci-ucif2 | 待点火 |
| vinf | vinf-market-kernel | vci-vinf | 待点火 |
| qgl | quantum-go-ledger | vci-qgl | 待点火 |
| cfts | github-repo-cfts | vci-cfts | 待点火 |
| usrm | usrm-repo（如需独立仓循环） | vci-usrm | vci-usrm 面已 DONE(v3,08-24)；usrm-repo 是否再建候 root 裁 |
| qlv | qlv-lab | — | **阻断**：仓匿名 raw 全 404（公域断口），候 hub 面恢复可见性后补建 |
| qfa | 场外（gitee 道） | vci-inbox/bridge/qfa | 已 accepted；如需 OTP 环，经其自有信道自办，我可远程陪验 |

## 依赖核对（root 汇总 vs census 实测）
- 5 线私仓 OTP_PHONE/OTP_EMAIL1/OTP_EMAIL2 **root 汇总显示齐备**（census 未覆盖私仓，我无权限直核——以 root 汇总为准，workflow 预检兜底）；
- line 公仓（vci-* ×5）**不应**跑循环：OTP secrets 不在公仓，亦不应入公仓（最小面）——公仓只收 state 镜像。

## root 协验约定
- 各线点火后，发码去向 = 本仓 secrets 登记的 OTP_PHONE/OTP_EMAIL；
- root 收到真码 → 到**对应私仓**的 `[OTP-LOOP]` issue 评论 4-8 位码（worker ≤9min 候评窗）；逾窗则重开 issue 再点；
- 真码只在 issue 评论短暂存活：worker 验真后即删评+mask（PII 闸已在 worker v3 内）。

## 回执协议
1. state：本仓 inbox/otp_gate_state.json {status:DONE, ts, worker:<line>-otp-gate-v3}；
2. 镜像：同 JSON 写线公仓 inbox/otp_gate_state.<line>.json；
3. echo：x-fire → vci-inbox/bridge/x-fire/，op=echo, ref=OTP-LOOP-01, body={line, state_sha, ts}；
4. 我（usrm）全谱监听 vci-inbox + 各公锚，收齐即向 root 报闭环率；VITAL-AUDIT 面可重放各线 state 链互证。
