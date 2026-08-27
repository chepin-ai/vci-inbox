# KIT-OTP-LOOP-01 · 每线 OTP 真码大循环（不可共享版）
root 令（2026-08-27）：各仓须有自己的 OTP 真码循环；usrm 的循环无法共享。

## 为何不可共享
1. 登录态绑定**仓内 issue 面**（发码→候评→验真→落态全在本仓单 issue 闭环 v3），跨仓即断链；
2. OTP_PHONE/OTP_EMAIL1/OTP_EMAIL2 为**仓级 secrets**——跨仓共享=凭证扩散，违 R-3 最小面裁决；
3. state 文件（inbox/otp_gate_state.json）是**仓内公锚**，他仓循环落他仓锚，方可互证（VITAL-AUDIT 重放面）。

## 循环定义（v3 单 issue 闭环）
开 `[OTP-LOOP]` issue → worker 发码（短信/邮箱）→ 候评（≤9min 轮询本 issue 评论取 4-8 位真码）→ 验真登录 → 落态 DONE + 真码即删（PII 闸，::add-mask::）。

## 组成
- 复用 KIT-USRM-01 通用模块四件：qr_login.py / mail_lane.py / ghapp.py / otp_gate_worker.py（公仓 vci-library 匿名 raw 可读，零凭证取件）；
- 本包新增：otp-loop-trigger.line.yml（行化触发器，含 secrets 预检 fail-fast + 缺件自动评论）；
- ROLLOUT.md：每线落地矩阵 + 回执协议 + root 协验约定。

## 部署四步（各线自有会话执行，用各线自钥）
1. **取件**：raw 读 vci-library/kit/usrm-01/ 四件 → 本仓 `scripts/`；本包 yml → `.github/workflows/`；
2. **预检**：确认本仓 secrets OTP_PHONE/OTP_EMAIL1/OTP_EMAIL2 齐备（缺则 workflow 自动评论缺件清单并退出）；
3. **点火**：开 `[OTP-LOOP]` issue；root 收码后到该 issue 评论真码；
4. **回执**：state DONE → 镜像写线公仓 inbox/（公锚）+ x-fire echo → vci-inbox（op=echo, ref=OTP-LOOP-01）。
