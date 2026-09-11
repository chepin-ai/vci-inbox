# usrm-116 · wave-48：F7/Pages 两候件锐化闭环

时间戳：2026-08-31T13:32:22Z

## F7 relay-keymig（root 唯一动作，一次访问两个 toggle，约 3 分钟）
入口（chepin-ai=User 账号实证）：https://github.com/settings/installations
1. chepin-ci-ops-hub（4621702）→ Configure → Repository access → 加 relay-keymig → Save
2. chepin-ci-root（4621743）→ Configure → 加 relay-keymig → Save
为何两个：ops-hub 实测 secrets:write 在权→未归档即由我即刻直删；若已归档，删密需先解归档（administration:write 唯 ci-root 有，wave-38 实证）→9/1 自动兜底。两个 toggle 免除二次打扰。
授权后我全闭环：删密→复核→判词回填，零追加 root 动作。
穷举四径皆断（两 App 选区不含/PEM 9/1 前不可触/PAT 永废立法/App 不能自加选区）。精确件：ci-control/bridge/findings/f7-relay-keymig-root-action.md

## Pages 三裁：收窄 + 默认飞行
422 BLOCKED-PLAN=计费档（usrm-106 实证），非权限。②转公破 R1 不可选 → 三裁实质二选一：①升 Pro / ③弃 Pages。
按 W41 实飞令**默认飞 ③弃**（展示职已由 9 公仓极简锚承载）；root 保留事后否决——若选①升级后我一键开（ci-root pages RW 在权）。
撤回 wave-46 报中「待 ci-root token 9/1 自跑」表述：真阻塞是 plan，不是 token。
精确件：ci-control/bridge/findings/pages-trichotomy-adjudication.md

## 链锚
narrative seq232 tip dd28ca7f9bbf · outbox seq126 tip 7fa8c9244406 · stream-ledger seq272 688dadbe4850 · heartbeat beat#20 cross 561c023238cc6217 · 判词×2（V-F7-SHARP / V-PAGES-ADJ）
