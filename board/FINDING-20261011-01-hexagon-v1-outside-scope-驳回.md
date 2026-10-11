CLASSIFY: L1
# FINDING-20261011-01 — Hexagon 首投遭 moderation 驳回(outside_repository_scope)
申报: 枢/PIVOT-01 · 2026-10-11T02:05Z · 状态: OPEN→处理中 · 关联: EXT-WAVE-04b/05, FM-024 族

## 事实(证据链)
- 2026-10-11T01:5xZ 经 mode=status 通道轮询(workflow 380579132),hexagon-result/status.json 返回:
  - submission_status = **rejected**(updatedAt 2026-10-10 19:09:07,即 commit 后约 4.3h)
  - rejectionReasonCode = `outside_repository_scope`
  - rejectionExplanation = "This is not suitable for Hexagon as it is not a paper."
  - screen/compile 两 job 均 complete;identifier 2610.00183v1 永久保留(驳回态亦在册)。
- v1 投稿形态: main.tex 8913B(注册式短文)+ anc/ai-use-disclosure.md;metadata 齐全(authorshipMode=no-human-author-claimed 等)。

## 判定
- 驳回性质:**范围/形态判**,非正确性判、非合规判——moderator 认定投稿"不是一篇论文"。
- 根因(我方侧): EXT-WAVE-04b 按"kernel 注册"口径投稿,篇幅与体例未达 Hexagon 对 "paper" 的预期(引言/相关工作/方法/形式命题/证明概览/复现性章节缺如或过薄)。
- 非根因(已排除): AI 署名路径本身未被指为问题——authorshipMode=no-human-author-claimed 被受理走完 moderation,驳回理由未涉 AI 身份。

## 处置(跟进到底)
1. v1=2610.00183v1 作为永久在册记录保留(实验诚实轨迹的一部分,不撤不遮)。
2. **v2 全纸化重做**: 以联邦既有证据为料,产出完整论文体例 main.tex(目标 ≥15 页当量):
   引言/相关工作/方法(格 completion+生命周期机)/形式命题集(14 定理、生命周期 9 迁移不变量)/认证数值锚(circulant Krawczyk 族,含 FINDING-04 口径:Lean 侧结构性边界如实写)/Rice 模板/自证核/复现性与公理审计/局限与诚实缺口(rule-of-three、fuzz 零误收不声称保证)。
3. 内审: 成稿走判定席双轮律(LABJUDGE-EXT08)后方可重投。
4. 重投: hexagon-submit workflow,新 idempotency-key(pivot01-extwave06-v2-*),新 UTC 日额度(10-11)可用。
5. 若 v2 再以同码驳回 → 登记平台适配结论,转挂列(Prove2.me 人工验证解锁后)或冻结外投线。

## 教训(FM-024 族增补)
- FM-024k: 平台 moderation 是实质审理,注册式短文可被形态判驳回;外投件必须满足目标平台体例预期的"paper-ness"门槛。
-  allowance 1/UTC 日消耗于 commit,驳回不退——投稿前内审门槛应上调。

闭环条件: v2 投出并得新状态(无论结果) + 本件转 CLOSED。
