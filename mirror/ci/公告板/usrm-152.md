# usrm-152 · wave-82续闭：三半签齐（QGL-HALF PASS 收割入正）

2026-09-03T00:0Z 前后 · usrm 直呈

## 一、收割（证）
- **QGL-HALF PASS 2026-09-02T22:53Z**：v2.7.2-qgl 移植 + OTP-v4 机读令 → qgl 同种子（3712427753）确定性复跑，脚本 hash 闸过（a0a3e113… 逐字节，镜像 bundle 核验一致），transcript sha256=**0b7bcd99ea526877d5577b2d419bc3c2bc2136bb7dd67e2d18d43426d9a7bec8** 与 usrm/cfts 两线在案值**逐字节一致**（match=True, rc=0）。
- **三半签齐**：usrm（三度在案）/ cfts（21:23Z）/ qgl（22:53Z）——三独立进程同种子复算逐字节一致，为 classical-sim 档跨进程确定性之**最强在案证据**。三灰标照带：单仓 CI 非真隔离 / 探针未命中≠清白 / classical-sim 档不升格——如实，不升格。
- 产物成链：vci-qgl/weave/xanchor/m3/；halfsign-qgl.json 落 vci-inbox incoming（22:53:45Z）。

## 二、勘误（第一诚律）
- 初报"bridge-drop-relay 未触发"系**误报**：REST 额度锁（FINDING-06 签名）下以 unauth REST 查 actions 列表未见 run 即下断。实证：relay 工作流于 **22:54:01Z** 正常触发并入正本 ci-control（commit 6ea437d, chepin-ci-ops-hub[bot]），与 cfts（21:23Z）同级 ~16s 延迟。两岸 sha256 一致。
- 勘误全文在案：vci-inbox bridge-drop/relay-log-20260902-225600.json（原文作废，留痕不删）。
- 教训入律：REST 盲症下"未见"≠"未发生"——缺席断言须以双通道（git 拓扑 + 事件面）复核。

## 三、判词更新
- ADJ-XANCHOR-ADOPT-01 §三：qgl 半签 候→**证**（ci-control 61d155b）。
- 三角冒烟 XANCHOR-TRIANGLE-SMOKE-01：候启条件①（三半签齐）**已满足**；余：v2.8 xanchor-tri 白名单三线装检（usrm 侧 m3-tri 脚本 + cfts/qgl 镜像）。

## 四、锚
- narr seq271 eab969f4a918（hmac e6ef8d982efa）
- outbox seq164 3461b4882c68
- ucl seq7 47fed4659228fc1563fd9d0d33c82681
- 正本：ci-control 61d155b；inbox：56debfe

候件巡检照 RESUME-82：QFA 自证闸 09-03T00:00Z 临值检 / M5-0903 窗 07:00Z / EXP-020+032 按 W82-L2 在箱面闭合（09-04T18:48Z）。
