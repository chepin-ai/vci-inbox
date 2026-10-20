CLASSIFY: L1
> 入仓注记：2026-10-21 自 research/leancert_integration_01.md 入仓，仓外原件留存，以仓内本为登记正本。
# EXT-WAVE-18「攻」WS-I · LeanCert 接入设计 01 —— L2-2 轨 A 设计 + S1 spike 前置

- 执行席：枢/PIVOT-01 体系 WS-I 攻坚线执行席（资深 Lean 4 工程）；成文日期钉：2026-10-21（UTC(Z) 单时钟域，现状断言均带「截至」钉，EXT18 卡6）
- 上游：WS-44《NS-SOLUTION-v2 设计书》L2-2 行；WS-D 预研 capanchor_preresearch_01.md（轨 A 先行结论、S1 spike 钉 2–3 pd / 截止 2026-11-04）；TRUSTBOUNDARY-REGISTRY-01（§二 12 条边界，本文只提建议不改该文件）
- 对象文件：CapAnchor.lean（只读，零漂移维持，本文未改任何 library/ns 文件）；S1 spike 草稿骨架见仓内 specs/LEANCERT-SPIKE-DRAFT-01.lean.txt（.txt 存放＝未接线不入库构建）
- 语纪律：OpenAI 相关成果口径固定「自评已核、外部复现中、未颁奖」；HWY 全程「报告了/提出」；Clay NS 未解决、未颁奖；严禁「NS 已解决」式表述；本接入不改变我方「有限维 ODE 截断层」档位

---

## 〇、上游核实（本席 2026-10-21 经 api.github.com 实测复核，与 WS-D 钉一致）

| 钉 | 值 |
|---|---|
| 仓库 | https://github.com/alerad/leancert （Apache-2.0；创建 2026-01-02；search API `q=LeanCert` 首名命中） |
| 最新 release | **v4.35.0**，published **2026-10-15T15:32:11Z**（releases API 实测；次新 v4.34.0 2026-09-18） |
| tag→commit 全钉 | annotated tag object `91a56a72629ce5f274712e594683bbd4fd8e9958` → commit **`d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e`** |
| LeanCert 自身工具链 | `lean-toolchain` = `leanprover/lean4:v4.35.0`；`lakefile.toml` require mathlib @ `v4.35.0`（与我方 library/ns 现状同链：lean-toolchain v4.35.0、mathlib @56a005855ea17e0b0958f73ec801ae140b0a1679，TB-01/TB-03 在册） |
| 版本漂移警示 | 三钉两漂移维持 WS-D 登记：arXiv:2610.02335 钉 LeanCert 4.33.0 系 commit 501b2c09；Mori Weil-log5 钉 v4.34.0 = commit 6320a15be41a；现行 v4.35.0 = d3e7f686eb6b。接入一律以 v4.35.0 commit 全钉为准，**禁引旧钉充当现行接口依据** |

能力面 README 级核实（截至 2026-10-21）：`leancert` 策略覆盖点不等式/盒上量化界/根存在唯一/积分/尾部界；信任三档 `native`（native_decide 默认）/ `kernel`（decide+kernel，绝不回退）/ `auto`（kernel 优先、受限回退并报告）；官方 Limitations 明示「not a complete decision procedure」「Downstream enclosure execution currently targets unary interval bounds」「kernel-only verification may be substantially more expensive」。Krawczyk 引擎源码级核实见 §二。

---

## 一、依赖引入方式（确切写法；本波纪律＝不改 lakefile，此为接线时指令）

### 1.1 lakefile require（我方为 lakefile.lean Lean DSL）

```lean
-- library/ns/lakefile.lean 追加（接线时执行，本波不动）
require leancert from git
  "https://github.com/alerad/leancert" @ "d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e"
  -- = tag v4.35.0（2026-10-15 释出）。commit 40-hex 全钉为纪律首选
  --（Palomar/L4-4 40-hex commit pin 先例；tag 可移动、commit 不可移动）。
```

- 版本钉三件齐：commit 全钉 `d3e7f686…e8f43e` + tag 别名注释 `v4.35.0` + 接线后 `lake-manifest.json` 全文件 sha256 入册仓 ledger（随 WS44 L0-2 依赖钉定簿扩展）。
- 兼容性零摩擦点：LeanCert v4.35.0 自身 require mathlib @ v4.35.0，与我方 mathlib @56a00585（v4.35.0 发布点）同钉，无依赖解析冲突预期；接线首日以 `lake update leancert && lake build` 实测为准。
- LeanCert 默认 target 为 `leancert` lib（precompileModules = false）；其 Examples/Showcase/Benchmarks 等非默认 target 不随下游构建，算力影响面可控。

### 1.2 使用面白名单（防 LeanCert 内部非全证面渗入）

允许 import 面（已逐文件源码核实）：

| 模块 | 角色 |
|---|---|
| `LeanCert.Validity.Krawczyk` | golden 层：`verify_unique_system_root` / `verify_system_root_exists` / `verify_system_root_unique`（均为 `krawczykCheck_sound` 的稳定更名，kernel 已证） |
| `LeanCert.Engine.RootFinding.Krawczyk` | 检查器与证书：`KrawczykCert`、`krawczykCheck`、`intervalJacobian`、`preconditionedJacobian`、`intervalMatrixBound`、`newtonImageEnclosure`、`intervalStrictInside`、`FinBoxMem`、`SystemZero` |
| `LeanCert.Core.Expr` / `LeanCert.Core.IntervalRat`（经 Core 伞） | 表达式文法与有理区间结构 |
| `LeanCert.Tactic`（可选） | `system_unique_root using cert (trust := kernel)` 前门 + `inspectKrawczyk` 分段诊断 |

禁入面（登记理由）：`LeanCert.CertifiedBounds.Li2` 轻量接口（其 lakefile.toml 自述两条界陈述故意以占位符存放、机证在 CI 的 Li2Verified target——非全证面，禁入我方 kernel 链）；一切 `native` 默认档隐式调用（必须显式 `(trust := kernel)` 或裸 `decide`）。

---

## 二、Krawczyk 引擎源码级核实（v4.35.0 @ d3e7f686 实测读取）

- `KrawczykCert (n : Nat)` 结构：`center : Fin n → ℚ`、`preconditioner : Matrix (Fin n) (Fin n) ℚ`——中心与预条件子均为**不可信证书数据**（与我方「z/Y 由 float64 产出、证书可靠性不仰赖候选质量」纪律同构）。
- `krawczykCheck F X cert cfg : Bool` 五分量合取：① 每分量 `checkADSupported`；② `centerInside X cert.center`；③ `cert.preconditioner.det ≠ 0`（ℚ 上精确行列式）；④ **收缩判据** `intervalMatrixBound (preconditionedJacobian Y (intervalJacobian F X cfg)) < 1`（ℚ 精确）；⑤ **严格自映射** 每分量 `intervalStrictInside (newtonImageEnclosure …) (X i)`。
- golden 定理：`krawczykCheck_sound : krawczykCheck F X cert cfg = true → ∃! x, FinBoxMem x X ∧ SystemZero F x`（收缩路线，`ContractingWith.exists_fixedPoint'`，免 Brouwer——与我方证书 schema 的 Krawczyk–Moore–Rump 收缩路线同型）。
- **关键数学差异登记**：LeanCert 的区间雅可比 `intervalJacobian` 由其**受检 AD**（`derivIntervalCoreN`）导出，非手编 `□DF(U)` 公式求值；其自映射包络 `newtonImageEnclosure` 结构为「Newton 中心点包络 ± q·r 对称区间」，与 mpmath 验证器直接求值 K(U) 的区间形状**不同构**——两引擎均数学严谨但包络过度估计不同，一致性门（§四）据此分「硬判定字段」与「对拍参考字段」两级。
- 多元能力面：Krawczyk 引擎本身 n 维通用——上游 FunctionalTests 含 3×3 循环耦合系统（`cyclicSystem`，有理 3×3 逆）与 4 维 identity 系统的 `(trust := kernel)` 通过例（LeanCert/Test/KrawczykTactic.lean）。WS-D 所引官方「unary interval bounds」Limitation 限定的是**下游自定义算子 enclosure** 面，不覆盖 Krawczyk 引擎内核；我方 B₃ 系统（3 维、纯多项式、ADSupported 片段 const/var/add/mul/neg 子集）落在已示范覆盖内。第三方「log 缺失/高维行列式不可行」报告（hexagonmath 条目）所述阻塞为其适应症（log + 高维 det），与本适应症无关，仍标**未核**。
- 表达式文法（Expr 归纳类型，v4.35.0 实读）：const/var/add/mul/neg/inv/exp/sin/cos/log/atan/arsinh/atanh/sinc/erf/sinh/cosh/tanh/sqrt/namedConst；**ADSupported 受检片段＝const/var/add/mul/neg/sin/cos/exp**（`evalFin_differentiable` 归纳支为限）——我方系统只用前五支，处于片段核心。

---

## 三、API 映射表（LeanCert 区间/验证原语 → CapAnchor 证书字段，逐字段）

以 `cap-b3-p1-mild.cap.json`（run ws55-cap-20261012T201100Z，sha256 a54b6ea1d140cffd…）schema v1.0 字段为行：

| 证书字段（值实例） | LeanCert 原语 | 映射规则与注意 |
|---|---|---|
| `params.nu/a/f`（1；[1,1,1]；[1,0.5,-0.25]） | `Expr.const (q : ℚ)` | decimal 字符串精确 parse 为 ℚ（"0.5"→1/2）；进入系统编码的常数叶 |
| `system.components`（F0=2u₁u₂−νa₀u₀+f₀ 等三式） | `Expr.add/mul/neg/var` 树 × 3 | 手编码一次、双写对拍：与 `capF_apply` 坐标展开（CapAnchor.lean 行 85–93）逐项同形；只用 ADSupported 片段 |
| `system.jacobian`（□DF 公式） | `intervalJacobian F X cfg`（checked AD 导出） | **不需要**手编区间雅可比——由受检 AD 生成，与证书 DF 公式的语义一致性由 golden 定理链承载；此为相对 mpmath 路线的信任基收缩点 |
| `candidate.z` = `box.center`（[0.6,0.8,-0.25]） | `KrawczykCert.center : Fin 3 → ℚ` | 证书自标「registered as exact decimal rationals」：0.6→3/5、0.8→4/5、-0.25→-1/4 |
| `preconditioner.Y`（3×3 decimal 字符串） | `KrawczykCert.preconditioner : Matrix (Fin 3) (Fin 3) ℚ` | 逐字符串 parse 为 ℚ；注意 `0.31999999999999995` 为 float64 尾迹（精确值 8/25 的 float64 最近邻）——主对拍用证书原值，备选探针用 8/25 替换并记录在案（见 §六 R5） |
| `box.radius`（0.0474531328121258） | `IntervalRat` 端点 `{lo := zᵢ−r, hi := zᵢ+r, le}` | r 为精确 decimal ℚ；盒子由规范字段 center±radius 构造 |
| `krawczyk.U`（派生端点显示） | `finBoxEnv`/`FinBoxMem` 语义对应 | **派生显示字段**：第 3 坐标 -0.29745313281212576 为 float64 显示尾迹（z−r 精确 decimal 为 -0.2974531328121258），门按 1e-12 容差对拍（§四 G2） |
| `krawczyk.F_z` / `y0_hi` | `pointEvalIntervals`/`newtonCenterInterval` 内部量 | LeanCert 不暴露同名字段；经包络对拍间接覆盖（G4 参考级） |
| `krawczyk.rho_hi`（0.22777503749820385） | `intervalMatrixBound (preconditionedJacobian Y (intervalJacobian F X {})) : ℚ` + `decide (· < 1)` | **硬判定字段**：q_lean 为 ℚ 精确值；门 G3 双条件（q<1 且 \|q−ρ_hi\|≤5e-2） |
| `krawczyk.K` / `margins` / `min_margin`（0.0366…） | `newtonImageEnclosure` + `intervalStrictInside` | **结构不同构**（LeanCert＝Newton 中心 ± q·r 对称包络）：布尔判定为硬字段（G1 内含），端点对拍仅参考级（G4，不判 FAIL） |
| `verdict.existence/uniqueness/status` | `krawczykCheck = true` | **硬判定字段**（G1）：PASS ⟺ check=true，布尔精确一致 |
| `capAnchorStatement`（Lean 侧命题） | `verify_unique_system_root` 产出 `∃! x, FinBoxMem x X ∧ SystemZero F x` + 适配桥 | 桥接义务三件（B1 WithLp 双射 ∃! 转移 / B2 SystemZero↔capF=0 经 `capF_apply` 与 `evalFin` 归纳 / B3 FinBoxMem↔capBox 端点展开）；S1 一期只到 fin 版 ∃!，桥接为二期（§五 TBD-B1） |

覆盖率一句话：证书 schema 14 个字段域全部有 LeanCert 原语承接（10 硬映射 + 2 派生显示容差映射 + 2 内部量参考映射），无悬空字段。

---

## 四、复算一致性门定义（「复算一致」判定算法）

输入：Lean 侧 spike 产物（`krawczykCheck` 五分量真值、`capB3P1_contractionBound : ℚ`、包络端点、资源实测）× 证书 JSON（verify.py 独立复算输出为准）。

- **G0 分段门（诊断）**：以 `inspectKrawczyk`（或五分量逐项 `#guard`/`decide` 分解）记录每分量真值；`stage ≠ accepted` 即 FAIL 并按 `KrawczykCheckStage`（unsupportedAD/centerOutside/singularPreconditioner/contractionNotStrict/imageNotStrictlyInside）定位。
- **G1 判定门（硬）**：`krawczykCheck capB3SystemP1 capB3BoxP1 capB3CertP1 = true` 经 **kernel 档**（`decide`，非 native_decide）闭合 ⟺ 证书 `verdict.status = "PASS"`（existence∧uniqueness=true）。布尔精确一致，不容差。
- **G2 盒子门（硬，小容差）**：Lean 盒子由规范字段 center±radius 精确构造；与证书 `krawczyk.U` 六端点逐一比对，`|端点差| ≤ 1e-12`（float64 显示尾迹容差）；超差即 FAIL（schema 规范字段与显示字段自相矛盾，须回证书生成器问责）。
- **G3 收缩门（硬，双条件）**：`q_lean : ℚ`（LeanCert 精确收缩上界）须满足 ① `q_lean < 1`（数学判据本身）；② `|q_lean − ρ_hi_cert| ≤ 5×10⁻²`（跨引擎包络过度估计差容差；两引擎均包络同一真值 ‖I₃−Y·□DF(U)‖∞，ρ_hi≈0.22778，余量约 4 倍，容差取余量 1/8 量级）。参考级（记录不判定）：`q_lean ≤ ρ_hi + 1e-9` 是否成立（mpmath dps=50 包络理论上更紧，若反向超差 >1e-9 记异常但不 FAIL）。
- **G4 包络门（参考级）**：`intervalStrictInside` 每分量 = true 已由 G1 内含（硬）；`newtonImageEnclosure` 端点与证书 `krawczyk.K` 六端点对拍仅记录（结构不同构，见 §二），不判 FAIL。
- **G5 资源门（测量，不判数学 FAIL）**：kernel 档 wall-time / max RSS 实测入册（补 dim08 Gaps 2 量化空白）；阈值钉：wall-time > 30 min 或 max RSS > 16 GB 记「能力面负发现」——激活 WS-D 未决项 1/2 的降级路径（auto 档重试 + 证据目录明示信任基 + 轨 B 评估触发），**负结果亦为交付**。
- **FAIL 总结**：G0–G3 任一失败，或 kernel 档 decide 不可终止（超时/爆内存，此时按 G5 降级并登记），判「复算不一致」；S1 验收钉（WS-D 原钉重申）：逐字段一致（G1–G3 全过）+ 耗时/内存实测入册 + LeanCert v4.35.0 tag/commit 钉 + lake-manifest 哈希。截止钉 2026-11-04 维持；工具链 v4.35.0 已并轨在册（TB-01/TB-03），L0-1 前置已满足，S1 不再受卡2 顺延条件约束。

---

## 五、与 TRUSTBOUNDARY-REGISTRY-01 的边界更新建议（只建议，不改该文件；按「裁决先行、登记同步、行文随后」走判定席）

1. **新增 TB-13「LeanCert 依赖真身与 golden 定理链」**（建议）：
   - 信任对象：alerad/leancert v4.35.0 @ d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e（源码供应链）+ `verify_unique_system_root` golden 定理链（语义面）。
   - 信任性质：**TCB 内经 kernel 复核**（golden 定理经我方 kernel 复编即受检；`trust := kernel` 档 decide+kernel 无 native_decide 攻击面，dim08 C2 纪律满足）+ 源码供应链 TCB 组件（同 TB-03 mathlib 格）。
   - 建议 T 级：接入前 **T0**（设计自述），S1 通过后升 **T1**（实测记录在册）。
   - 缺口与关闭：① LeanCert 内含非全证面（Li2 轻量接口占位符面）——以 §1.2 使用面白名单关闭；② LeanCert 上游 CI soundness tier 的审计结论属转述证据——关闭路径＝我方自跑 `#print axioms` 对 spike 终定理（预期不越 propext/Classical.choice/Quot.sound 白名单）+ Comparator 声明级比对随件。
2. **TB-07（见证层采样代码）更新建议**：S1 通过后，缺口行「LeanCert 接入复算」标记关闭；`krawczyk_ns_gen.py`/`krawczyk_ns_verify.py` 角色由「唯一证据来源」改写为「不可信候选生成器 + 跨引擎对拍器」（T 级维持 T1，证据角色迁移登记）。
3. **TB-08（自有声明）更新建议**：spike 产物若接线入库，新增 decl 走 S1 白名单审计（公理不越界；kernel 档 `decide` 不引入 trustCompiler——与 native_decide 的公理差在册对比说明）。
4. **TB-09（alignment 缝）更新建议**：`ModeSpace 1 ↔ Fin 3 → ℝ` 适配桥（§三 B1–B3）登记为 **Adapter 环**新条目候选（30 行级，环间契约 Gap→Adapter 已定条目路径），与 kernel 化一期 C3 构件同槽排期。
5. **TB-06（Comparator）随件建议**：spike 入库件作为 Comparator 基线报告首件「非 mathlib 外部依赖」比对对象，随 L3-1 基线一并产出。
6. **TB-12（册仓治理）随件建议**：leancert 三钉（commit 全钉 + tag 别名 + lake-manifest 哈希）入册仓 ledger，随 L0-2 扩展；lean4checker/NanoDa 对 kernel-only 产物的双核重放属 OBL-NS-02 窗口随件候选（NanoDa 对含 trustCompiler 证明 decline——kernel 档产出恰好满足其约束，dim08 C2）。

---

## 六、风险登记（诚实条目；WS-D 未决项逐条引）

| id | 风险 | 等级 | 缓解/出处 |
|---|---|---|---|
| R1 | **版本漂移**：三钉两漂移（4.33.0 系 501b2c09 / 4.34.0 6320a15 / v4.35.0 d3e7f68）；本文 API 形态全部按 v4.35.0 源码实读，旧钉文献仅作历史参照 | 中 | commit 40-hex 全钉 + manifest 哈希（§1.1）；漂移检出即开新条目（append-only，TRUSTBOUNDARY R4 同制） |
| R2 | **kernel 档算力未量化**（WS-D 未决项 1）：官方仅定性「substantially more expensive」；唯一工程参照 Mori 32GB/25GB | 高 | S1 内置实测（G5）；超阈降级 auto 档并明示信任基，轨 B（ℚ-证书化）评估触发——负结果亦为交付 |
| R3 | **多元 enclosure 覆盖度**（WS-D 未决项 2 修订）：官方「unary」Limitation 经源码核实**不覆盖 Krawczyk 引擎**（n 维通用，3×3/4 维 kernel 档通过例在上游 FunctionalTests）；但上游 kernel 档多元样例均 ≤4 维小盒子，B₃ 3 维 + 非平凡 Y 的 kernel 档耗时仍无先例 | 中 | S1 即实测；G0 分段定位能力缺口；第三方「log/高维行列式不可行」报告与本适应症无关，标未核 |
| R4 | **det 计算规模**：`krawczykCheck` 内 `decide (Y.det ≠ 0)` 为 3×3 ℚ 精确行列式，平凡；高维风险（R3 引报告）不适用本例 | 低 | 登记即可 |
| R5 | **float64 尾迹字段**：Y[1][2]=0.31999999999999995、U 第 3 端点 −0.29745313281212576 为 float64 显示尾迹，非精确 decimal | 低 | 规范字段（center/radius）为构造基准（G2）；备选探针以 8/25 替换 Y 尾迹值重跑对拍，两轨结果均入册 |
| R6 | **LeanCert 默认档陷阱**：`native` 为默认信任档，隐式使用即引入 trustCompiler 攻击面（dim08 C2：native_decide 证明 lean4checker/SafeVerify 不可重放） | 中 | 白名单纪律：一切复算显式 `decide` 或 `(trust := kernel)`；spike 文件头写死；入库 CI 加 `leancert.trust` 选项审计钩 |
| R7 | **桥接缝（B1–B3）未证**：fin 版 ∃! 到 `capAnchorStatement` 的 ModeSpace 适配为二期工作，S1 一期不闭合 | 低 | TB-09 Adapter 环登记（§五.4）；一期交付物明示「kernel 级 ∃! 限于 Fin 3 → ℝ 坐标版」不越界表述 |
| R8 | **spike 回退闸**：S1 估 2–3 pd（WS-D 钉），散布小但 kernel 档耗时为零先例 | 低 | ≤2 人周回退闸（卡2 先例）；超闸回判定席，禁静默扩项 |

---

## 七、合规自检（本文行文）

本文不含新数学断言；未改 library/ns、lakefile、lean-toolchain、registry 任何文件；OpenAI 成果口径「自评已核、外部复现中、未颁奖」；Clay NS 未解决、未颁奖；HWY 未涉引述；全部时间戳 UTC(Z) 带「截至」钉；官源复核记录＝api.github.com 实测（search/releases/tags/contents 六接口，2026-10-21）。接入完成后我方档位仍＝有限维 ODE 截断层 + kernel 级证书锚（如 S1 通过），不构成任何 PDE 层主张。

—— WS-I 攻坚线执行席 · 枢/PIVOT-01 体系 · EXT-WAVE-18「攻」· 2026-10-21
