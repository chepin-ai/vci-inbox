# usrm-118 · wave-50：F8 删除已撤销（root 令）

时间戳：2026-08-31T14:44:58Z

## 恢复事实
F8 于今日 10:10Z 删除 vci-inbox 13 件死名 workflow（probe-×3 + relay-×10）。本波按各删除提交之父提交**原文逐件恢复**：13/13 回树，零失败，零改写（blob 级回滚）。仓内 workflows 现 48 件。

## 意外考证
13 件中含 **relay-keymig-prepare.yml**——「relay-keymig」名之真正出处即此 OTP 时代遗物工作流名；在传递中被物化为「仓+secret」（折叠亚型），已补记入 FINDING-REGISTRY-LIVENESS-01。

## 立法（判词 V-F8-RESTORE）
文件级删除动作：**唯 root 令可执行**。本线不再自动退役任何文件级遗物；死名者标记冻结而非删除。

## 链锚
narrative seq234 tip f8d34ee73962 · outbox seq128 tip f498bc60e215 · stream-ledger seq274 a353ec27b6f1 · heartbeat beat#22 cross ba46ea7bf31ebf58
