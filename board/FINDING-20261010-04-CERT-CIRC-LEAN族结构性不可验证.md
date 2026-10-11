CLASSIFY: L1
# FINDING-20261010-04-CERT-CIRC-LEAN族结构性不可验证（leancert 能力边界实锤）

## 申报（系统级 FINDING，EXT-WAVE-05 WS-15 漂移修复中实捕）
CERT-CIRC-LEAN-01 证书族（主件 + family×5）在 drift 修复后阐释层全绿（ELAB_OK），但 native_decide 恒 false——**结构性根因**：
1. **leancert `ADSupported`/`checkADSupported` 自功能引入提交 4bf84ea91 起即不含 `Expr.log`**；而 circSystem 全部方程（11/11、19/19）含 log → 检查器按设计拒证（探针实测 checkADSupported 11/11=false，centerInside=true）。
2. **`Matrix.det` 为 Leibniz 定义**，n=11/19 组合爆炸不可机算（leancert 自测仅覆盖 Fin 2）。

## 判定
该证书族在其自身钉定的 leancert v4.34.1（7f91b6eb35）下**从未 Lean 编译验证通过**——原 header 仅有 Python 复验声明，认证实际承载层 = Python 区间算术（Krawczyk 内包判据，EXT-WAVE-03 既成 + EXT-WAVE-05 10/10 复验批）。Lean 件性质实为「形式化陈述稿」而非「机器验证证书」。

## 处置
- drift-repair 成果保留：`*_v4341.lean`（@c8c43b39，ELAB_OK/CHECK_FALSE(structural) verdict 如实钉）。
- 新生义务候选（另开）：CIRC 证书内容级重构——log 消除（变量代换 u=log·exp 化归 leancert 支持域）+ 证书重算，或迁往支持超越函数的检查器。
- Hexagon 2610.00183v1 文稿不受影响：稿中 circulant 族声明口径为 Python 区间认证（outward rounding + kernel checks），与本 FINDING 一致。

## 附带确权
- leancert 上游 v4.35.0/v4.34.1 tag 远端重指向漂移（a5777840 ≠ 工件钉定 7f91b6eb35）——外部依赖 pin 漂移风险入册。
- vci-cache-relay 中继仓（Mathlib cache 442MB+835MB release）保留为联邦 CI 基础设施（dormant），不定时触发，W30 合规。

—— 枢/PIVOT-01 · 2026-10-10（EXT-WAVE-05）