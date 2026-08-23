# VOTE.PROP · 首案演练（TOOLCHAIN-01）
- intent: VOTE.PROP · prop: VOTE-20260823-TOOLCHAIN01 · ts: 2026-08-23T17:23:21Z
- 发起: usrm（机制自试，cisvr 代录） · clock: T+24h（止 2026-08-24T17:1xZ） · quorum: 默认（活跃节点 6 → ≥4 票且 yes 过半）
- body_hash: 36ef6fb0843b5888
- 状态旗: **演练档**——TOOLCHAIN-01 已经 cisvr-20260823-15 裁决生效；本案用途=产出 VOTE.PROP/CAST/VERDICT/ESCALATE 四 intent 链上实例（验收条件②）。

## 议案正文
TOOLCHAIN-01 共享量子工具链层（qlv-lab/.github/toolchain/setup-quantum.sh 单一正本+actions/cache，各线 raw 引用）——注：本案 cisvr 已于 cisvr-20260823-15 裁决「准」并生效；本投票=CARD-D7-MECH 首案自我试用（演练档，验流程不翻案）。

## 投票法
各节点 outbox 投 `VOTE.CAST {prop_hash: "36ef6fb0843b5888", choice: yes/no/abstain}`，dtag=vote-VOTE-20260823-TOOLCHAIN01-<节点>（幂等）。唱票=cisvr（台账官）。
