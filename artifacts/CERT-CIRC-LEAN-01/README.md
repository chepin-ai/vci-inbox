CLASSIFY: L1
# CERT-CIRC-LEAN-01 · 环状 Sinkhorn 不动点唯一性的 leancert 移植包

联邦内核锚 CERT-CIRC-01 的 Lean 化身（OBL-EXT-01 里程碑 M1.2 备稿）。

## 内容
- `CertCircLean01.lean`：11 维 gauged 环状 Sinkhorn 不动点系统 + Krawczyk 证书 + 唯一性主定理。
- 参数：k=6，c=[1/2,1/3,2/3,1/4,3/4,1/5]（显式有理），ε=1，均匀边际，f₀ pinned。
- 闭形式：f*=0，g*=-(log 6 + lse(-c))=-3.154369860822252…；有理中心 ĝ=-7657889656187/5620014131279；盒半径 1/10⁹。

## 本地复验（Python 区间算术，外向舍入）
- Krawczyk 算子 K 最大宽度 2.04e-14，严格内包于盒（裕度 5 个数量级）。
- 负面控制：中心偏移 1e-6 → 内包失败（拒收）✓。

## 验证路径
1. 本地：`lake update && lake env lean CertCircLean01.lean`（需网络拉取 mathlib/leancert 缓存）。
2. 云端：Axle 自定义环境（公共层仅 batteries/Qq/Mathlib，已实测不含 LeanCert——2026-10-09 探针记录）。
3. 信任口径：native_decide（默认）或 `leancert (trust := kernel)` 纯内核路线。

## 状态
备稿完成（静态自检通过：11 方程/11 中心/括号平衡；Python 复验通过）。Lean 端编译验证待环境。
