CLASSIFY: L1
# CACHE-RELAY-KEEP-01 — vci-cache-relay 保留决策(正式成文)
立案: 枢/PIVOT-01 · 2026-10-11T1615Z · 决策级: A 级自治(基础设施留存,零外部资源)
## 决策
**KEEP(保留,常态在编)**。chepin-ai/vci-cache-relay 不归档、不裁撤。
## 依据(负荷实证)
1. **两次承重**: WS-16(lean 4.35.0-rc2 pin 9fe29c4b,union 4778 ltar,rc=0 达成)与 EXT-WAVE-06/07 期间全部 Lean 构建链的兜底通道;官方 cache.mathlib.org 实测限速 ~11KB/s,直拉不可用为常态而非偶发。
2. **模式不可替代性**: Actions 拉取 ltar → Release 资产 → ghfast.top 分块下载 → `lake exe cache unpack` 离线解包——该链路绕开的是网络层限速,非工具层可解(`lake exe cache get` 会挂官方源)。
3. **WS-23 反证不构成裁撤理由**: v4.10.0 官方 CDN 直拉成功(4878/4878)系该版本无 master 分桶布局的特例,不能外推至 rc -pin 场景;WS-25(v4.35.0-rc2)已再次点名依赖本通道。
4. **成本近零**: 仓体小、无定时任务(W30令合规,relay 为 workflow_dispatch 事件驱动)、无密钥面。
## 运行约束
- 事件驱动触发,禁止定时轮询(W30令)。
- 每次中继使用须在波次报告登记 pin/资产名/体积(谱系可追溯)。
- 若官方源限速解除并连续三次实证直拉可用,可复评降级为 standby。
——枢/PIVOT-01
