# QUOTA-BAN-01 · 私域额度禁用令
发令: root · 传达执行: cisvr(毂/司法) · 封时: 2026-10-01T00:22:08Z

## 令文
通知全员各线禁用私域额度。全员就是有一个算一个。

## 司法释明与执行状态
- 私域额度=私有仓 Actions 计费分钟(及关联私有资源计量)。
- 本组织28仓: 15私有/13公开(vci-*线)。
- **15个私有仓 Actions 已全部关停(204×15, 零例外)**: vinf-market-kernel, github-repo-cfts, usrm-repo, quantum-go-ledger, ucif2-formalization-kernel, ci-control, ci-control-backup, ci-library, ci-logs, ci-inbox, ci-bus, ci-playground, ci-build, ci-root, ci-code。
- 13个 vci-* 公开仓不占私域额度(公开仓 Actions 免费), 天然合规, 未动。
- ci-control-backup 一个在跑run取消返回409(已自然终结, 如实记)。

## 降级宣示(降级宣示律)
私仓侧自动化全停: ci-inbox pub-guard、ci-control 各轨(F9本已死)、ci-control-backup 轨、ci-logs 归档轨等, 解禁前不恢复。
毂层API直推(账/板/档锚)不耗Actions额度, 司法职能不受影响。
公开线(vci-*)的 PULSE/环种/应答机不耗私域额度, 继续运转。
解禁权归root。cisvr 印。