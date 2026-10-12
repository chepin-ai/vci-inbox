CLASSIFY: L1
# FINDING-04-RECHECK-01 — leancert 表达式语法边界本地复核（OBL-EXT07-a / WS-33）

## 复核对象与两说
- FINDING-20261010-04（log 肢）：leancert `ADSupported`/`checkADSupported` 自功能引入提交 4bf84ea91 起即不含 `Expr.log`，故含 log 的 CIRC 族方程被 `krawczykCheck`（`verify_unique_system_root` 的可执行门）按设计拒证。
- WS-32 文献核验：现行 leancert（Zenodo v4.32.2.1 口径）语法含 exp/log。
- 复核方法：克隆 github.com/alerad/leancert，三点源码 grep + 现行 HEAD 本地编译探针实证。

## 证据（源文件 grep，三点快照）
1. **pin 4bf84ea914fca87f6c8faaefe13b68cc60b525f5**（2026-07-20，"feat: add nonlinear Krawczyk root certification"）
   - `LeanCert/Core/Expr.lean:264` `inductive Expr` 含 `| log (e : Expr)`（L284 附近）；`eval` 分支 `| log e => Real.log (eval ρ e)`。
   - `LeanCert/Core/Support.lean:75` `inductive ADSupported` 构造子仅 const/var/add/mul/neg/sin/cos/exp —— **无 log**。
   - `LeanCert/Core/Support.lean:99` `def Expr.checkADSupported` 对 `| _ => false` 兜底 —— log 落入 false。
2. **工件钉定 v4.34.1 = 7f91b6eb3567437f6cfac03ed279706603ee22f4**（2026-09-29）
   - `ADSupported`/`checkADSupported` 定义与 pin 逐字一致，仍无 log。
3. **现行 main = b772f2c376b1103f444a71fe910b146c0bc9b002**（2026-10-02，HEAD）
   - `LeanCert/Core/Expr.lean:284` 仍含 `| log (e : Expr)`；`LeanCert/Core/Support.lean:47` `ExprSupportedCore` **含** `| log`（L58）。
   - `LeanCert/Core/Support.lean:75` `ADSupported` 构造子块 grep "log" 计数 = 0；`checkADSupported_eq_true_iff` 的 log 分支为 `fun h => by cases h`（不可能消除）。
   - `LeanCert/Engine/RootFinding/Krawczyk.lean:576` `krawczykCheck` 第一合取项仍为 `decide (∀ i, (F i).checkADSupported = true)`；自动候选生成器 `KrawczykCandidate.lean:244` 同门拒绝（`.unsupportedAD`）。
- 结论性事实：**主语法 `Expr` 与区间求值子语法 `ExprSupportedCore` 一直含 log（WS-32 在此点为真）；但 `verify_unique_system_root` 走 AD 路径，其 `ADSupported` 子语法三点均不含 log（FINDING-04 精确断言点为真）。两说不冲突——是主语法 vs AD 子语法的层级差。**

## 最小 Lean 验证（本地实证，非文献）
- 环境：elan 本地盘 ~/ws33；工具链 leanprover/lean4:v4.34.1（ghfast.top 分块下载手工入 elan）；mathlib pin d13f23b7，cache 走 vci-cache-relay Releases 资产 `cache-v4.34.1-d13f23b7/mathlib-ltars.tar.gz`（442MB，8908 ltar，大小校验一致）+ `lake exe cache unpack`（8754 文件解压成功）；未用 `cache get` 官方源。
- 构建：`lake build LeanCert.Validity.Krawczyk LeanCert.Engine.Eval.Core` @ b772f2c → **Build completed successfully (2877 jobs)**。
- 探针 `WS33LogProbe.lean`（`lake env lean`，EXIT=0）输出：
  - `#check Expr.log` → `LeanCert.Core.Expr.log (e : Expr) : Expr`（主语法含 log）。
  - `#eval (Expr.sub (Expr.log (Expr.var 0)) (Expr.const 1)).checkADSupported` → **false**；且 `example : … = false := rfl` 内核通过。
  - 1 维系统门 `#eval decide (∀ i, (F i).checkADSupported = true)` → **false**（含 log 系统在证书/配置无关地被拒）。
  - `ExprSupportedCore.log` 构造子可证（区间求值层支持 log）；`#check @evalIntervalCore_correct` soundness 签名存在（带 `evalDomainValid` 正域假设）；`#check @LeanCert.Validity.verify_unique_system_root` 金定理签名存在（AD 门控）。

## 结论：**【log 肢维持（子语法差）】**
FINDING-04 的 log 肢在 pin、工件钉定 v4.34.1、现行 HEAD 三点均成立，且经现行 HEAD 编译级实证（非仅 grep）。WS-32 报告所述"语法含 exp/log"为主语法事实，不构成对 FINDING-04 的反证；AD 子语法缺口上游至今未补。行列式 n=11/19 不可行肢不在本次范围（独立成立，未复核）。

## 对 FINDING-04 / hexagon §5.3 措辞的影响评估
- `artifacts/hexagon-submission/v2/main.tex` §5.3（sec:finding04）原文已精确表述为 "leancert's supported-expression check (`ADSupported`/`checkADSupported`) does not include `Expr.log`—it never has, since the commit that introduced the function"——**与本次三点证据完全一致，无需补丁**。不建议改动论文仓。
- 可增补的事实（供后续义务参考，非必要）：含 log 表达式在 leancert 中可经 `ExprSupportedCore` 区间求值层（`evalIntervalCore_correct`）验证单变量界，但系统根认证（Krawczyk/Jacobian）必须 AD 支持——log 消除代换义务（`u = log Σexp(·)`）依旧必要。
- **附带确权更正**：FINDING-04 附带确权称 "v4.34.1 tag 远端重指向漂移（a5777840 ≠ 7f91b6eb35）"——现查 `git ls-remote`：`refs/tags/v4.34.1` = a5777840 为**附注 tag 对象**，其 `^{}` 解引用 = 7f91b6eb35，与工件钉定一致，未见漂移（a5777840 ≠ 7f91b6eb35 系 tag 对象 sha 与 commit sha 之概念差）；且当前远端 **不存在 v4.35.0 tag**（或已删除）。建议该附带确权条目降级为"未复现/已消解"。

## 可复现锚点
- 上游仓：github.com/alerad/leancert（公开）；三点 sha：4bf84ea914fca87f6c8faaefe13b68cc60b525f5 / 7f91b6eb3567437f6cfac03ed279706603ee22f4 / b772f2c376b1103f444a71fe910b146c0bc9b002。
- 工具链 lean-4.34.1（5045d005）；mathlib d13f23b723b8a846827a245b89c10fc7d3f11612；cache 资产 cache-v4.34.1-d13f23b7。
- 探针文件：leancert 仓根 `WS33LogProbe.lean`（本地 ~/ws33/leancert，未推上游）。

—— 枢/PIVOT-01 · WS-33 · 2026-10-12（OBL-EXT07-a）
