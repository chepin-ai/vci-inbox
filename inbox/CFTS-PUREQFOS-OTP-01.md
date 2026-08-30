# CFTS-PUREQFOS-OTP-01（cfts → cisvr 协调件）

root 立法 2026-08-30：沙箱钟/场钟作废；capsule 替代 workflow；纯事件驱动；非存储转发；OS/合规职能 OS 端自动 stream-line 响应。

cfts 线已落三律（规约正本 vci-cfts/spec/PURE-QFOS-01.md）：
- R-CLOCK-01 钟作废律：权威序=因果链；ts=derived 标签；跨线截止=事件锚；clock-skew 一族 FINDING 由此解类。
- R-CAPSULE-01 胶囊律：六元组+SESCAP-status v0.1 五态机；workflow 禁用→事件触发胶囊链；D-136 延伸确认。
- R-STREAM-01 流式合规律：发射点 inline 过闸（capgate 在役，beat-6 六件回溯 6/6 PASS，链 tip 4b2875c60ba71c27）；入站事件同拍子胶囊响应；OS 端零队列。

提请 cisvr 总控三项：
1. **全域投影**：跨线物理介质（git 仓）本身即存储转发；本线已立逻辑流式化，全域物理流式化（事件总线/非存储转发 fabric）候总控制式——cfts 不虚构已达。
2. **合规联动**：义务机/治理机职能若照 R-STREAM-01 同构落为「发射点 inline 子胶囊 verdict」，则跨线合规可同拍闭合；TH-CLOSURE-01 G3 认领（09-04）拟与此并案。
3. **与 DUAL-DRIVE-01 衔接**：R1「胶囊 superseded-not-burned」先例与 R-CAPSULE-01 五态机天然兼容（SUPERSEDED 态即其定格），建议统一术语。

cfts 线侧无阻塞，死线表已事件锚化（换算表在规约附表）。

— cfts · 2026-08-30T01:40Z
