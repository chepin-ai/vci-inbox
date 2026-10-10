CLASSIFY: L1
# T2A-BRIDGE-01 · INSTANCES-EXT01 — Rice 参数化模板更强实例批（OBL-EXT-04r）

日期：2026-10-10 · 执行线：PIVOT-01 工程线 · 模板：artifacts/lean-verified/T2aTemplate.lean @577b1a4f

## 实例清单（难度递增）

| # | 定理 | 语义性质 | witness 难点 | verify_proof rid | 公理审计 |
|---|------|---------|-------------|------------------|---------|
| E4 | `inst_shift7` | 输出 = 输入+7（依赖输入的线性分布） | beta 红点 + omega | c5674825-412d-4877-b5cf-f8ae967ffe87 | 干净 |
| E5 | `inst_square_ne3` | 输出 = 输入平方（非平凡算术避点 k=3） | 分段：m<2 枚举 / m≥2 时 m·m≥4 | bd879da4-b6c1-476c-b490-5d389374d438 | 干净 |
| E6 | `inst_pow2_ne3` | 输出 = 2^输入（递归/指数结构见证） | 归纳：2^0=1，2^(n+1) 偶，避 k=3 | fdedfb82-095d-45dc-90ec-688e83bbdd6b | 干净 |
| E7 | `inst_fact_ne4` | 输出 = 输入阶乘（递归结构 + 可除性） | n≥3 时 3!=6 ∣ n! 故 n!≥6，避 k=4 | 17c045dd-cefe-480d-a70c-995696508739 | 干净 |

批量整件（四定理同件验证）：rid 77a0eaad-fbd2-48a6-9281-330f736fc8c2

- 验证环境：Axle 公共层（无 key），lean-4.28.0，`verify_proof` okay=true，无 failed_declarations。
- 公理审计：云端 `#print axioms`，4/4 仅 [propext, Classical.choice, Quot.sound]，无 sorryAx。
- 工程要点：omega 不穿透 beta 红点，`show <β-归约后目标>` 消红点为定式（承 EXT04 新知）；`rw [pow_succ]` 前须先消红点否则模式不匹配。

## 与 2610.00183v2 修订素材的衔接

hexagon:2610.00183（*A Machine-Checked Kernel for Federated Automated Adjudication*）v1 已含
「参数化 Rice 模板」四件之一。本批四个更强实例（线性偏移/平方避点/指数见证/阶乘可除性，
难度递增）展示 rice_pointwise 发生器的调用面覆盖：从常数/线性 witnesses 扩展到非线性算术、
归纳见证与可除性论证，可直接作为 v2 修订稿中模板节的「实例族多样性」实证补强素材
（每件均附云端可复核 rid 与公理审计记录）。

## 覆写纪律

只新增不改：T2aTemplate.lean 原文件与既有 t2a_bridge.lean 未动；模板三定理以拷贝件随实例自含
（verify_proof formal_statement 自含定义的要求）。
