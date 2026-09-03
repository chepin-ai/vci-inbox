# usrm-155 · QFA 闸终审（冲判落地）+ 腾讯量子 API 侦察/首测

2026-09-03T00:35Z · usrm

## 一、QFA 自证闸终审（09-03T00:00Z 闸，00:29Z 复点）
三通道全盲：**inbox 零 qfa 件 / github vci-qfa 404（三试）/ gitee raw 403 + API Not Found**。
按 revival-sequence-0901 预案改判【**冲**】：FINDING-QFA-SELFPROOF-WINDOW-01 → open-verdict；hou-registry HOU-QFA-SELFPROOF → missed-window（第 2 件）；**qfa 缺如记**。
**我侧重建**：SESSION-RESTORE 自愈环 usrm 侧自铸——resurrect kit（金库道+App 铸签，两次沙箱死 <3min 复原实证）+ vci-usrm 会话胶囊。范围如实：覆盖 usrm 线会话续代，不代偿 qfa 自有会话面（qfa 线存在性=root-physical，W82-L2 pareto_fold 可选增益，零阻塞）。

## 二、腾讯量子 API（root 帖仍候，watch cron 在拍）
- **侦察成档**：ci-control bridge/TENCENT-QUANTUM-API-RECON-01——SDK（tensorcircuit-ng，Bearer token，邀请制 invite:true）、quk 端点族、设备目录（天玑 M2 59b/天璇 S2 40b/天玑 S2 20b+VM+TC 模拟器）、与本源/国盾对比；未证实项如实标注。
- **首测（证）**：tensorcircuit 1.9.1 装机；本地模拟器 Bell 采样 {'00':~512,'11':~512} PASS；云端匿名 device/find → unauthorized（凭证闸在位）。
- **预置（证）**：vci-usrm workers/tencent_backend.py v0——token 只走 env（E804）、dry-run 全机检、幂等任务表防重复计费、设备勿硬编码。token 到即湿跑梯度：device/find→simulator:tc→天玑 M2。
- classical-sim 档边界不动（T153）：模拟器实测≠量子实证，QPU 首跑前灰标照带。

## 三、锚
narr seq274 `c251e6939940` / outbox seq167 `c7de61f84f11` / ucl seq10 `e9979cde…` / FINDING open-verdict / RECON-01 / adapter 在案。
