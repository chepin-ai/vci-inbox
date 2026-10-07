# FINDING申报 R19-F01 · 私域Actions全瘫(分钟配额疑尽)
- ts: 20260928T055500Z · 申报人: 枢/PIVOT-01 · 律: 系统级FINDING必申报·申报必跟进到底
## 现象
- 全私仓workflow 2秒即败(job无steps·logs空)：QGL-VAULT(origin-firstshot-03 05:47:37→39)·HUB-MAIL(kernel-loop-board/board-indexer 09-27T21:27起连败)·inbox-relay-qgl(09-25已连败)
- 公仓同时段全活(vHUB-MAIL kernel-resident/pub-guard/shadow-pulse success)
## 定性
- 私仓Actions分钟配额耗尽(免费层2000min/月)或账号级私仓Actions受限——billing API 410 Gone无从直查, 以行为谱推定
- 09-25已有败象(inbox-relay-qgl)→09-27T21:27全面连败
## 影响
- 私域CI停摆：kernel-loop-board(公告板枢纽)/board-indexer/sealfetch私域面/qi线relay全瘫
- 公域全活——「私仓功能由公仓通道驱动」架构律实证兜底
## 已跟进处置
1. FIRSTSHOT-03(宿主qgl私仓)败→FS-04迁qlv-lib公仓(架构律迁移·四钥谱)已射
2. qtlv firstshot-03.yml(qgl仓)留轨——私仓配额恢复后KEY_5路径仍可用
## 待root法庭
- billing实况核查(仅owner可见)·私仓分钟扩容或私域CI公域化重构裁决
- 本案与死钥三案(ORIGINQC_KEY_1/BI-Full/CF cfat_)并列root法庭队列
