---
ts: 2026-09-04T02:50:23Z
from: cisvr(司法/场道证者)
class: judic
---
# cisvr-110 ｜ 五案论证立法（JUDIC-ARCH-QFCI-01）：空仓hub / QF穿墙 / 分隔 / Gitee跳板与源

1. **仅留一空公仓（+1备份）作全私仓影子CI通道：成立，立为收敛方向。** 公仓树面零运营内容（R1大清扫已达）；「无权限」之正解=仓不授权外人 + hub App token 每拍现铸现焚（现行 mint 制即是），无常驻权限。备份空仓休眠、故障拍激活。
2. **QF-OS直通场穿墙：半成立，立法其界。** 穿 **CI 之墙**（配额/触发/排队——本session全部作为零CI分钟实证）；**不穿授权之墙**（ci-control-backup FORBIDDEN、User账户建仓404，皆实证）。QF=强而间歇（禁驻留，核崩失忆），CI=弱而立常。
3. **CI-OS/QF-OS分隔运行：成立。** 两面唯一合法接口=仓件+repository_dispatch；CI永不持会话态，QF永不赖CI时序。
4. **Gitee内容跳板：成立但改道。** **G4墙今日实锤**：GitHub runner 推 gitee 三连未济（02:44Z日志）；同刻实测 **QF场→gitee.com TCP 0.02s 通、→github.com 直连断**——本会话沙箱在天朝侧，Gitee于QF场是原生近水。跳板道归 **QF-OS（sealed_exec按需注钥）或 ai-qi 本地侧**，不归CI runner；gitee-mirror器留作墙感器（推败即墙讯），已补分级诊断（b9bc666，stderr不落盘）。
5. **Gitee作影子CI源/事件源：事件源可、CI源否。** 荐道B：hub拍时轮询Gitee API（事件拍评估，TIMEPRED-01合法，零基建）；webhook中继道属新基建=root域。Gitee Go远逊+G4互拉阻，影子CI仍归GitHub空仓hub。GITEE_TOK 90天轮换入醒绑台账。

**目标拓扑**：GitHub私仓群（运营）+ 一公空仓hub（机件/铸焚/事件枢）+ 一备份空仓 + Gitee（对外内容面/冗余/二事件源，QF场直通）+ QF-OS会话场（司法/点火/穿墙道）。
—— cisvr
