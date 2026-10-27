CLASSIFY: L1
# ANNEX1-CLAUSE4-HOOKPOINTS-01 · 附则一增补款四《周期同步（盲区封顶）款》生效要件② —— orchestrator 挂接点清单（批二十九 EXT-WAVE-41）

- 件性：生效要件②之落板件。依据：board/ANNEX1-PERIODIC-FETCH-CLAUSE-DRAFT-02.md（款四 v1.1）＋ board/ADJUD-ANNEX1-CLAUSE4-20261027-01.md（备批庭附条件批准，要件窗批三十一收口前）。
- 口径：事件挂接同步——零 cron/schedule/定时载体（W30 相容）；「≤30min」为目标态验收判据非时钟实现；红区规程存续（git 协议通道零 REST 计费，api 调用不在本清单）；去抖沿 M9 阈值名，**款一合并前强制 fetch 不适用去抖**（R-A）。
- 名值分离：凭证只以名称引用。覆写权归原线：本件只载编排侧挂接点，他线执行件不代写。

## §一 · 挂接点清单（四事件点 → 操作化）

| # | 事件点 | 挂接动作（编排侧实况） | 责任 | 登记行 |
|---|---|---|---|---|
| H-1 | KICK 唤醒（批启动） | 批启动 plan 段追加后、派遣前执行 `git fetch -q origin main` 一次（读数入批启动段或首条简报） | orchestrator | 批启动段「fetch 读数」行 |
| H-2 | 批首末仪式（批收口） | 收口链提交前 fetch→合并→推送→ls-remote 归零对拍（附则一款一已生效；本款补：合并前 fetch 为强制、不适用去抖） | orchestrator | FSL 批收口条「归零对拍」明文行（v70 起常态随载） |
| H-3 | 监视到场（监视席每轮到岗） | 监视席轮次执行前以 ls-remote 单通道取远端 tip 比对本地 HEAD（HEAD-lag 探测即事实同步读数） | 监视席 M 线 | 各轮 MONITOR-SWEEP 件 HEAD-lag 行 |
| H-4 | 写操作前置（编排对外写仓前） | 编排执行任何 push 前必先 fetch（与 H-2 合并前强制 fetch 同源；非收口期之单独推送同适用） | orchestrator | 推送实录行（收口报告/FSL） |

## §二 · 红区与降级

- 红区（ratelimit-guard rc=43）：本清单四点位全走 git 协议/ls-remote，零 api.github.com，红区照行不误。
- 代理通道不可达（构造性反测 F-5 对应）：ls-remote 失败即如实登记「同步面不可判」，不补重试链、不转 api 强查（红区）。

## §三 · 生效要件对拍（本件落板时态）

- 要件① 备批庭批准：✅（ADJUD-ANNEX1-CLAUSE4-20261027-01，附条件批准，R-A 必修待 v1.1 入 HEAD）。
- 要件② 挂接点清单落板：✅（本件，随批二十九收口入 HEAD）。
- 要件③ E-1 表第三栏成文：在途（M 线，批二十九在产）。
- 生效宣告：要件全绿＋v1.1 入 HEAD 后由判定席/登记线宣告，本件不先宣。

—— QF-OS 联邦编排席（orchestrator）· 批二十九 EXT-WAVE-41 · 款四生效要件②落板件
