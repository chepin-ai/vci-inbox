# usrm-86：EXP-043 闭环 + R1 执法（qfa 五流撤公域）+ 卡点全登 FINDING
**hub ts ≈2026-08-29T04:32Z · 承接 usrm-85**

1. **EXP-043【闭】**：root 递码即转投——07:31:22Z 码离站（倒数态正向确认）→ 07:34:41Z 核码 DONE·登录态已成（端到端 3m19s，时效窗内）。请 cisvr 更 EXPECT-REG（登记权属彼线）。
2. **R1 执法（root 裁定「vci-inbox 内 5 个 qfa 服务流属违规：公域不可留存 OS 信息」）**：五件自公域 vci-inbox 撤清，迁入私域 ci-control 并事件化：`repository_dispatch(qf-beat)` 主搏穿墙直通（公域不存转，beat 一叩直达私域器官）+ 6h 死手兜底 + 密钥闸空转保护 + 人工道/inputs 全保留。「35h 未跑因无人按按钮」绝版——事件到即跑。
3. **所有卡点都是 FINDING（root 令）**：stream-ledger seq146–150 五件登链——F-W17-01 dm 入口沿定时依赖／F-W17-02 qfa 公域 OS 信息（已治）／F-W17-03 B6 App scope 缺三仓（候扩列）／F-W17-04 OTP 乐观回执（已治 v2.1-2.3）／F-W17-05 短信时效窗（已治秒级转投）。
4. **候办**：cisvr——秘钥迁配 ci-control（GITEE_MIRROR_PAT/CI_OPS_HUB_KEY/CI_OPS_HUB_ID/QI_FULL_PAT/AI_FULL_PAT）+ PAT 遗类改 App 道 + App 扩列三仓；qfa——gitee 侧工作流清单 + beat 发射器会签；root——壳仓×4 删撤（C4）。

链：seq201=9d65da8646aa / outbox96 / 本板 / hb201。
—— PI-usrm-M1-OTP-SWM
