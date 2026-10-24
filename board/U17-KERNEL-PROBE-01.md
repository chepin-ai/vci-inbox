CLASSIFY: L1

# U17-KERNEL-PROBE-01 · EXT-WAVE-23 批十一 · NS 包线 kernel 探针复验

席位：QF-OS 联邦 L3 探针席（verifier，独立复验，非原作者）
日期：2026-10-25 · 作业面：全新 /tmp 命名空间自建
措辞基线：自评已核、外部复现中、未颁奖。本探针仅涉声明的 kernel 可解析性与公理集，**不构成任何 RH 主张**（禁「RH 已证」）。

## 1. 环境重建台账

| 项 | 实测值 |
|---|---|
| toolchain 包 | lean-4.35.0-linux.tar.zst，594,481,375 B（与任务书一致） |
| toolchain sha256（自算登记） | `7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d` |
| 解压方式 | python zstandard 0.25.0 + tarfile 流式解至 /tmp/lean-4.35.0-linux（符号链接 /tmp/lean-4.35.0），耗时 ~22s |
| lean --version | Lean 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release |
| lean-toolchain 钉 | `leanprover/lean4:v4.35.0`（与主库 lean-toolchain 一致） |
| 作业面 | `cp -r` 主库 `/mnt/agents/output/vci-inbox/library/ns/` → `/tmp/ns-work`（11,887 文件，230M，含预置 .lake/packages 与 .lake/build olean；文件清单 diff 全等） |
| mathlib cache | `lake exe cache get` RC=0；**9031/9031 项**下载+解压；时长 **110s**（未触发失速预案，无需 xargs prefetch） |
| lakefile 钉 | mathlib4 @ `v4.35.0`（git require） |

备注：`lake env` 首次运行打印 9 条 "remote URL changed" info（清单内 ghfast 镜像 URL ↔ github.com 规范化），纯提示性，无 refetch，不影响结果。

## 2. 静态引证（源码行号钉）

- `NsGalerkin/ZetaAnchor.lean:18` `namespace ZetaAnchor`
- `NsGalerkin/ZetaAnchor.lean:25` `def zetaIsolationAnchor (T : ℝ) {n : ℕ} (w : Fin n → ℝ) : Prop`
- `NsGalerkin/ZetaAnchor.lean:30` `def zetaUniqueZeroAnchor (a b lo hi : ℝ) : Prop`
- `NsGalerkin/ZetaAnchor.lean:35` `def zetaAnchorImpliesRHCriticalLine : Prop`
- `NsGalerkin/CapAnchor.lean:61` `namespace NSGalerkin`；`:131` `def capAnchorP1 : Prop := capAnchorStatement capParamsP1 capCenterP1 capRadiusP1`
- 根模块 `NsGalerkin.lean` 确认 import 含 CapAnchor 与 ZetaAnchor（全 13 子模块）

## 3. 探针输出原文

探针文件 `/tmp/ns-work/Probe.lean`（写 /tmp，非仓内；未 commit 任何改动）：

```lean
-- CLASSIFY: L1
-- U17-KERNEL-PROBE-01 · EXT-WAVE-23 批十一 verifier probe
import NsGalerkin

#check @ZetaAnchor.zetaAnchorImpliesRHCriticalLine
#check @ZetaAnchor.zetaIsolationAnchor
#check @ZetaAnchor.zetaUniqueZeroAnchor
#check @NSGalerkin.capAnchorP1
#print axioms ZetaAnchor.zetaAnchorImpliesRHCriticalLine
```

执行：`PATH=/tmp/lean-4.35.0/bin:$PATH lake env lean Probe.lean` → **RC=0**，全输出（过滤上述 9 条 URL info 后）：

```
ZetaAnchor.zetaAnchorImpliesRHCriticalLine : Prop
ZetaAnchor.zetaIsolationAnchor : ℝ → {n : ℕ} → (Fin n → ℝ) → Prop
ZetaAnchor.zetaUniqueZeroAnchor : ℝ → ℝ → ℝ → ℝ → Prop
NSGalerkin.capAnchorP1 : Prop
'ZetaAnchor.zetaAnchorImpliesRHCriticalLine' depends on axioms: [propext, Classical.choice, Quot.sound]
```

原始落盘：`/tmp/probe-out.txt`、`/tmp/probe-rc.txt`（RC=0）、`/tmp/cacheget.log`。

## 4. 对抗性附加检查（防陈旧 olean 误判）

不复信预置 .lake/build olean：对锚文件做源码级重编译
`lake env lean NsGalerkin/ZetaAnchor.lean` → **RC=0，72s，零诊断输出**（mathlib 依赖全走 cache olean）。证明 ZetaAnchor.lean 源文本在本环境可独立 elaboration，探针所读声明非陈旧产物。

## 5. 结论

1. **锚位 decl kernel 可解析性：PASS**。ZetaAnchor 三锚（zetaIsolationAnchor / zetaUniqueZeroAnchor / zetaAnchorImpliesRHCriticalLine）与 CapAnchor 侧 `NSGalerkin.capAnchorP1`（实际命名空间为 `NSGalerkin`，非 CapAnchor，任务书备选写法已按实修正）全部被 kernel 解析，类型签名与源码行钉逐字一致。
2. **公理集：白名单内**。`zetaAnchorImpliesRHCriticalLine` 依赖公理恰为 `[propext, Classical.choice, Quot.sound]`，**无 sorryAx、无其他公理**，与 Prop 级 def 预期一致。
3. 性质界定（逐字钉）：以上四锚均为 **Prop 级陈述定义**（statement-only，无证明断言）。NS 侧属**有限维 ODE 截断层**（Galerkin 截断包线，非 PDE 全局长存断言）；RH 侧属**有限高度 T=100/1000 截断**的外部区间见证锚定——**区间见证层 PASS、kernel 层未证、非 RH 证据**。`zetaAnchorImpliesRHCriticalLine` 仅为对 mathlib `RiemannHypothesis` 命题形式的临界线半边陈述焊接，kernel 层证明 BLOCKED(B1) 状态未被本探针改变。
4. 批准措辞维持：**自评已核、外部复现中、未颁奖**。

## 6. 异常登记

- 无。无 sorryAx、无意外公理、无 RC 非零、无 cache 缺失项（9031/9031）。
- 观察项（非异常）：lake 清单内远端 URL 含 ghfast 镜像前缀（前序会话 insteadOf 配置残留），lake 自检打印规范化 info；对构建与探针结果无影响，名值未混。

—— EXT-WAVE-23 批十一 · verifier 席 · 不 commit
