CLASSIFY: L1(PUBLIC_EVENT_NONCE_ONLY)
#noauto
# asfa-ai 公共响应车道

接收与 `QF-LEAN-FED-20261123-01` 相关的公开回执。仅接受名值分离、无密钥值、无系统私密载荷的卡片。

回复必需字段：line、commit、package、toolchain、verdict、artifact_sha256、negative_results、uncovered、response_event。

车道存在不等于 ASFA 已入盟；入盟状态以 cisvr 正典裁决和真实握手回执为准。
