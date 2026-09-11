# cisvr-80 · D-157 班次革命落成判词: 钟面遗物废除, QF-OS事件驱动贯通
ts: 2026-08-29T01:23Z ｜ by: cisvr司法 ｜ law: D-157/D-140/D-139 ｜ 锚: LEGISL-19 @ stream-ledger seq103 (hash cc76f065fa65)

## 〇、总判
root问「为什么还在用4h/13h schedule这种CI-OS遗物」——判： 遗物属实, 根源在GitHub schedule注册滞后+低优降级, 钟面只能当死手(dead-man), 不能当心跳。D-157全面升级为QF-OS事件驱动模型, 工程落成+三弹实测全PASS, 即刻生效。

## 一、四器改造清单(全push 200, py_compile全过)
- kernel-loop.yml: on块+repository_dispatch[qf-beat]+inputs.cause; P9 BEAT-FORWARD(evolution deltas非空或overdue>0→叩fleet-judge)
- fleet-judge.yml: 同on块升级; 判词变更或协同旗非空→叩kernel-loop(FLEET-STATE覆写前先读prev比对)
- intake-agent.yml: 同on块升级; new>0或escalations→叩kernel-loop+fleet-judge
- circle-refresh.yml: 同on块升级; knock带cause='beat-forward'
- 统一铁律: CAUSE='beat-forward'受叩方不转叩 → 级联有界, 环死锁结构免疫; cron全降级为死手兜底

## 二、级联三弹实测(轮询回测律亲验)
- 弹1: kernel-loop手动dispatch 01:06:59Z → fleet-judge 32s后自动被叩 success, 无第三班(器对器级联深度1成立)
- 弹2: qf-beat POST 204 → 01:08:23Z 一应四器(repository_dispatch)全success → gen2三叩(01:08:46/51/52) → 全终止, 无gen3
- 弹3: qf-beat POST 204 → 01:17:49Z 一应四器全success → gen2三叩 → 01:18:37Z全终止
- 事件响应延迟: POST→四器同班 ≈15-20s。对照旧钟面班距: fleet 5.5h/intake 4h/circle 13h → 秒级, 三个数量级
- pub-guard哨兵全程陪跑(弹2四班/弹3六班push触发)全success, 公私边界无恙
- 注: 弹2初报"3/4"系逐器查询per_page窗口截断之误, 全时间线复核确认4/4; 司法误报更正, 实证以全量runs时间线为准

## 三、健康指标切换(即日)
旧: 班距(4h/13h达标论) → 新: 事件响应延迟(目标<60s)+死手未触发率(目标100%)。kernel-loop P1-P9每班自测自报, 链上KERNEL_LOOP条目即健康账。

## 四、发现与后续
- FINDING(优化项): repository_dispatch触发班CAUSE=event_name非'beat-forward', gen1四器会各自再叩一代(gen2)。冗余但可终止, 不违环免疫。优化径: CAUSE解析加client_payload.cause → qf-beat带'beat-forward'即可抑制gen2。列入EXP-038范围(usrm对照组可验)。
- EXP-038: cisvr侧(四器beat-forward化+级联实测)落成, 证据锚seq103; usrm侧(circle-refresh重建对照组+T154方案)候09-06。
- EXP-017尾账OVERDUE: kernel-loop P1已自动盯账, 追复哨在岗。
- FD01回执潮死线今日19:30Z: kernel-loop死手+事件双轨盯办, 逾期自动escalate提案。

## 五、与递归引擎多进程/OTP模式匹配(root令后半)
四器=四进程, qf-beat=一发多收的事件总线, beat-forward=进程间OTP叩门, 会话端dispatch/qf-beat POST=OTP介入点。OS端引擎自主跑(P0-P9全拍), 会话端随时POST qf-beat即并入同一条事件流——双流共锚(stream-ledger单链), 过程不并, 状态必并(DUAL-DRIVE-01)。
