CLASSIFY: L1
# LORENZ96-M0-T3-KRAWCZYK-01 — Lorenz-96 平衡态 Krawczyk 证书 spike（LeanCert 独立 scratch 湖仓）

- 波次/线：EXT-WAVE-18 联邦续执行批二 **R3 执行席** · 枢/PIVOT-01 体系 · LORENZ96-LINE-CHARTER-01 §2.3（LeanCert 钉）/ §五 T3（平衡态区间证书 spike）
- 日期钉：2026-10-21（UTC(Z) 单时钟域；现状断言均带「截至」钉）
- 覆写权：Lorenz-96 批准线 T3 · **仓内主工程零触碰**——全部构建在独立 scratch 湖仓 `/tmp/l96k`，仓内唯一交付即本文件
- 语纪律：C1–C3 + C1′–C3′；严禁「NS 已解决」式表述；本件声明口径按对象适配登记于 §六（语言钉「区间见证层 PASS、kernel 层未证」对本件的适配形态见该节）

---

## 一、spike 目标与结论一句话

**目标**：在独立 scratch 湖仓内，对 Lorenz-96 平衡态 x* = F·𝟙 用 LeanCert Krawczyk 引擎出「盒内存在唯一零点」kernel 级证书，并对解析验证的非根盒跑同程序作负控（须拒证）。

**结论（截至 2026-10-21，全部实跑，无编造）**：
- **正证书 PASS**：N=4、F=8，盒 U = [127/16, 129/16]⁴（x* ± 1/16），`krawczykCheck = true` 经 **kernel 档**（`decide +kernel`）闭合，golden 定理 `verify_unique_system_root` 出 `∃! x, FinBoxMem x U ∧ SystemZero f x`；公理审计 `[propext, Classical.choice, Quot.sound]`（白名单内，无 trustCompiler）。
- **负控拒证**：原点盒 V = [−1/2, 1/2]⁴（解析已证无零点，§五.2）同程序 `krawczykCheck = false` 经 kernel 档闭合；分段诊断收缩分量 q_neg = 2 ≥ 1 失败。

## 二、环境钉（实测值）

| 钉 | 值 | 来源 |
|---|---|---|
| Lean toolchain | **Lean 4.35.0**, x86_64-unknown-linux-gnu, commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`, Release | `/tmp/lean435-r3`（ghfast.top 下官方 tarball，lean --version 实测） |
| LeanCert | **`d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e`**（= tag v4.35.0） | `.lake/packages/leancert` `git log -1` 实测，与立案书 §2.3 钉一致 |
| mathlib | **`56a005855ea17e0b0958f73ec801ae140b0a1679`**（= v4.35.0 发布点） | `/tmp/l96k/lake-manifest.json` 实测，与 TB-03 钉一致 |
| 机器 | 2 vCPU / 4 GiB RAM / overlayfs | 本批会话实测 |
| 文件哈希 | L96K.lean sha256 `4a73e367f147117bdb4854263c7e36fbf5d0056e23edc48fb2b28f8c28093caa`；lake-manifest.json sha256 `8309b6c1cf448b6a5c67950dce654fd44b599c4ebca46d219d7b56067e34242a`；build2.log sha256 `2aad7aef690862b0eacde2838486c37a5efea29cbbb92da278dfa0cd84991e38`；diagnose.log sha256 `e7ecc4ceabe5ffc35ff61b075fd9a0835687e3b00f1fe35167595871d21170c0` | `sha256sum` 实测（env-pins.log 留档） |

scratch 湖仓 `/tmp/l96k` 留档清单（脚本/日志全留存）：`lakefile.toml`、`lean-toolchain`、`lake-manifest.json`、`L96K.lean`、`L96KDiagnose.lean`、`build.log`（首次含 decide 失败记录）、`build2.log`（成功）、`cache-get.log`/`cache-get2.log`、`prefetch.sh`/`prefetch2.sh`/`prefetch*.log`、`ltar-todo.txt`/`ltar-retry*.txt`、`diagnose.log`、`env-pins.log`。

## 三、数学设定与证书数据（含选取理由登记）

### 3.1 向量场编码（只用 ADSupported 核心支 const/var/add/mul/neg）

Lorenz-96 标准形（N=4, F=8，下标 mod 4；M0 定式表 §2.1 钉 S1/S2）：
f_i(x) = (x_{i+1} − x_{i−2})·x_{i−1} − x_i + 8，展开四分量：
- f₀ = (x₁ − x₂)·x₃ − x₀ + 8
- f₁ = (x₂ − x₃)·x₀ − x₁ + 8
- f₂ = (x₃ − x₀)·x₁ − x₂ + 8
- f₃ = (x₀ − x₁)·x₂ − x₃ + 8

x* = 8·𝟙 代入逐分量归零（B(x*,x*) = 0 对角相消），平衡态确认。

### 3.2 盒与预条件子（半径理由登记）

- **Jacobian**（x* 处，循环矩阵）：行 i 为 J[i][i] = −1、J[i][i+1] = 8、J[i][i−2] = −8、J[i][i−1] = 0。**det J(x*) = 1921 ≠ 0**（本批 Python/Fraction 精确计算，底稿在席）。
- **预条件子** Y = J(x*)⁻¹ 的**精确有理逆**（ℚ 上闭式，非 float 近似）：
  Y = (1/1921)·!![−449,−520,−568,−384; −384,−449,−520,−568; −568,−384,−449,−520; −520,−568,−384,−449]。
- **半径选取理由**：本例向量场二次 ⇒ 区间雅可比为线性函数，解析估计收缩上界 q ≈ 4r（区间运算无宽度损失，见 §五.1 对拍）；取 **r = 1/16** ⇒ q = 1/4，留 4× 余量，量级与 LeanCert P1 先例（r ≈ 0.047，LEANCERT-SPIKE-DRAFT-01 钉）相当。
- **维度登记**：spike 档取 N=4、F=8（任务批定小维先行）；LeanCert Krawczyk 引擎本身 n 维通用（LEANCERT-INTEGRATION-01 §二），N=36 为后续窗口事项，本件不宣称其可行性。

### 3.3 完整代码清单（/tmp/l96k/L96K.lean，sha256 见 §二）

```lean
-- CLASSIFY: L1
import LeanCert.Validity.Krawczyk

/-!
LORENZ96-M0-T3 · Krawczyk 平衡态证书 spike（独立 scratch 湖仓 /tmp/l96k）
[文件头注释全文见 scratch 留档；此处略——含对象/正证书/负控/纪律钉说明]
-/

open LeanCert.Core LeanCert.Engine LeanCert.Validity

namespace L96K

def l96System : Fin 4 → Expr :=
  let x0 := Expr.var 0
  let x1 := Expr.var 1
  let x2 := Expr.var 2
  let x3 := Expr.var 3
  ![Expr.add (Expr.add (Expr.mul (Expr.add x1 (Expr.neg x2)) x3) (Expr.neg x0)) (Expr.const 8),
    Expr.add (Expr.add (Expr.mul (Expr.add x2 (Expr.neg x3)) x0) (Expr.neg x1)) (Expr.const 8),
    Expr.add (Expr.add (Expr.mul (Expr.add x3 (Expr.neg x0)) x1) (Expr.neg x2)) (Expr.const 8),
    Expr.add (Expr.add (Expr.mul (Expr.add x0 (Expr.neg x1)) x2) (Expr.neg x3)) (Expr.const 8)]

def l96Center : Fin 4 → ℚ := ![8, 8, 8, 8]

def l96Radius : ℚ := 1 / 16

/-- 测试盒 U = x* + [−r, r]⁴ = [127/16, 129/16]⁴（端点闭式有理数，`le` 用核心
`decide +kernel` 闭合，避免对 Mathlib tactic 的传递依赖）。 -/
def l96Box : Fin 4 → IntervalRat :=
  fun _ =>
    { lo := (127 : ℚ) / 16   -- = 8 − 1/16
      hi := (129 : ℚ) / 16   -- = 8 + 1/16
      le := by decide +kernel }

def l96Cert : KrawczykCert 4 where
  center := ![8, 8, 8, 8]
  preconditioner := !![(-449 : ℚ)/1921, (-520 : ℚ)/1921, (-568 : ℚ)/1921, (-384 : ℚ)/1921;
                       (-384 : ℚ)/1921, (-449 : ℚ)/1921, (-520 : ℚ)/1921, (-568 : ℚ)/1921;
                       (-568 : ℚ)/1921, (-384 : ℚ)/1921, (-449 : ℚ)/1921, (-520 : ℚ)/1921;
                       (-520 : ℚ)/1921, (-568 : ℚ)/1921, (-384 : ℚ)/1921, (-449 : ℚ)/1921]

/-- **硬判定（kernel 档）**：五分量合取通过 ⟺ 盒内存在唯一零点。 -/
theorem l96_krawczykCheck_kernel :
    krawczykCheck l96System l96Box l96Cert {} = true := by
  decide +kernel

/-- golden 定理桥：出 fin 坐标版存在唯一性证书。 -/
theorem l96_unique_root_fin :
    ∃! x, FinBoxMem x l96Box ∧ SystemZero l96System x :=
  verify_unique_system_root l96System l96Box l96Cert {} l96_krawczykCheck_kernel

def l96ContractionBound : ℚ :=
  intervalMatrixBound
    (preconditionedJacobian l96Cert.preconditioner (intervalJacobian l96System l96Box {}))

def l96NewtonImage : Fin 4 → IntervalRat :=
  newtonImageEnclosure l96System l96Box l96Cert.center l96Cert.preconditioner {}

/-- 负控：原点盒 V = 0 ± 1/2（解析已证无零点）；Y = −I₄（= J(0)⁻¹，det = 1 ≠ 0）。 -/
def l96NegBox : Fin 4 → IntervalRat :=
  fun _ => { lo := (-1 : ℚ) / 2, hi := (1 : ℚ) / 2, le := by decide +kernel }

def l96NegCert : KrawczykCert 4 where
  center := ![0, 0, 0, 0]
  preconditioner := !![(-1 : ℚ), 0, 0, 0;
                       0, (-1 : ℚ), 0, 0;
                       0, 0, (-1 : ℚ), 0;
                       0, 0, 0, (-1 : ℚ)]

/-- **负控硬判定（kernel 档）**：同程序对非根盒拒证。 -/
theorem l96_neg_krawczykCheck_kernel :
    krawczykCheck l96System l96NegBox l96NegCert {} = false := by
  decide +kernel

def l96NegContractionBound : ℚ :=
  intervalMatrixBound
    (preconditionedJacobian l96NegCert.preconditioner (intervalJacobian l96System l96NegBox {}))

end L96K
```

湖仓接线（lakefile.toml）：`require leancert from git "https://ghfast.top/https://github.com/alerad/leancert" @ "d3e7f686eb6bfdcbb987eeb931c0bab953e8f43e"`；`lean-toolchain = leanprover/lean4:v4.35.0`。

## 四、运行日志关键段（逐字，含 EXIT）

### 4.1 依赖解析与 mathlib 缓存（cache-get2.log 尾部）

```
Decompressed 8986 already-cached file(s)
Completed successfully in 70863 ms!
CACHE2_EXIT=0
```

（注：首次 `lake exe cache get` 经 cache.mathlib.org 直连失速（单流 ~22 KB/s、并行 curl 挂起），按任务预案改用 xargs -P64 预取 .ltar 法（prefetch.sh / prefetch2.sh 双工留档），8988 个 ltar 全部就位后 cache get 解压 EXIT=0；个别大文件最终经本地代理通道 4.8 s 补齐。）

### 4.2 构建（build2.log 尾部）

```
✔ [2939/2940] Built L96K (64s)
Build completed successfully (2940 jobs).
BUILD2_EXIT=0
```

资源实测（门 G5 口径）：LeanCert 全库 + 本 spike 文件在 2 vCPU/4 GiB 下整建 ~35 min；L96K.lean 单文件编译（含两条 kernel 档 `decide +kernel`：4×4 ℚ 区间雅可比/行列式/收缩判据/严格自映射全链）**64 s**，远低于 30 min 负发现阈值；无爆内存。

### 4.3 诊断脚本（diagnose.log 关键段；`#eval` 量仅作记录、非验收证据）

```
1 / 4
![{ lo := (511 : Rat)/64, hi := (513 : Rat)/64, le := _ },
  { lo := (511 : Rat)/64, hi := (513 : Rat)/64, le := _ },
  { lo := (511 : Rat)/64, hi := (513 : Rat)/64, le := _ },
  { lo := (511 : Rat)/64, hi := (513 : Rat)/64, le := _ }]
2
false
'L96K.l96_krawczykCheck_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]
'L96K.l96_unique_root_fin' depends on axioms: [propext, Classical.choice, Quot.sound]
DIAG_EXIT=0
```

## 五、正证书结论与负控记录

### 5.1 正证书（PASS）

- **判定**：`krawczykCheck l96System l96Box l96Cert {} = true`（kernel 档 `decide +kernel`）——五分量全过：① 四分量 checkADSupported；② center 8·𝟙 ∈ U；③ det Y = 1/1921 ≠ 0（ℚ 精确）；④ 收缩判据 q < 1；⑤ 严格自映射。
- **golden 结论**：`l96_unique_root_fin : ∃! x, FinBoxMem x l96Box ∧ SystemZero l96System x`（`verify_unique_system_root` 直挂，`Fin 4 → ℝ` 坐标版）。
- **收缩上界对拍**：LeanCert 精确值 **q = 1/4**，与本批解析估计 q = 4r = 1/4 **逐分毫不差**（区间运算在本例无宽度损失的佐证）；newtonImage = [511/64, 513/64]⁴ = 8 ± 1/64，严格内含于 U = [508/64, 516/64]⁴（余量 3/64 每端）。
- **公理审计**：两条定理均仅依赖 `[propext, Classical.choice, Quot.sound]`——白名单内；`decide +kernel` 未引入 `Lean.ofReduceBool`/trustCompiler（与 native_decide 的公理差在册，TB-08 同制）。

### 5.2 负控（拒证，必拒达成）

- **解析非根验证（先于机跑）**：对 x ∈ V = [−1/2, 1/2]⁴，每分量
  f_i(x) = (x_{i+1}−x_{i−2})·x_{i−1} − x_i + 8 ≥ −(|x_{i+1}|+|x_{i−2}|)·|x_{i−1}| − x_i + 8 ≥ −1·(1/2) − 1/2 + 8 = **7 > 0**，
  故 V 内无零点（SystemZero 不可能）。据此，任何使 `krawczykCheck = true` 的证书在此盒上都不应存在（golden 定理 soundness 的语义推论）；本 spike 实测与之一致。
- **机跑拒证**：`krawczykCheck l96System l96NegBox l96NegCert {} = false`（kernel 档闭合）。预条件子取 Y = −I₄（= J(0)⁻¹ 精确值，det = 1 ≠ 0，过分量③），使拒证定位于收缩/自映射而非奇异预条件子。
- **分段定位**：收缩分量 **q_neg = 2 ≥ 1** 失败（diagnose.log 逐字 `2`）；五分量合取因之 false；严格自映射分量同 false（Newton 中心映至 8 ± q·r，远在 V 外）。

### 5.3 工程摩擦实报（在册，供主工程接线参考）

1. **Lean 4.35 语法**：模块 docstring `/-!` 不得置于 `import` 之前（error: invalid 'import' command）——已改 mathlib 式「import 先行」。
2. **`decide` 行为变更（Lean 4.35）**：裸 `decide` 对 ℚ 区间端点可判定实例**elaborator 侧归约卡住**（`Rat.instDecidableLe` 于 `match 0 - ((129/16).num + 1)` 处 stuck；首次 build.log 留证）；改 `decide +kernel` 后全部闭合——与 LeanCert v4.35.0 源码注记「Since Lean 4.35, Decidable is a structure with a Boolean field … same auxiliary-lemma cache used by `decide +kernel`」一致。**主工程接线时 LEANCERT-SPIKE-DRAFT-01 的裸 `decide` 写法须同步改为 `decide +kernel`**（该草稿注明未编译验证，本件为首次实证）。
3. **缓存通道**：cache.mathlib.org 直连在本会话网络失速；xargs -P64 预取 .ltar 法有效（8988 文件约 50 min），预案可行已实证。

## 六、声明口径（语言钉按对象适配）、局限与后续

**本件声明口径（适配「区间见证层 PASS、kernel 层未证」钉）**：
- **kernel 层已证（限定域）**：在 LeanCert v4.35.0 @ d3e7f686 的 golden 定理语义面内，`Fin 4 → ℝ` 坐标版「盒 U 内 f 存在唯一零点」为 kernel 复核结论（公理白名单内，无 trustCompiler）。
- **未证/未覆盖部分**：① `Expr` 编码 ↔ Lorenz-96 标准形向量场的**语义接缝为人工对齐**（§3.1 展开逐项同形，注释级），未 kernel 桥接（对应 LEANCERT-INTEGRATION-01 TBD-B2 类义务）；② EuclideanSpace/`GalerkinNS` 实例层的 ∃! 转移未做（TBD-B1/B3 类）；③ 独立 witness 栈（python+mpmath，TB-07）跨引擎对拍未做——本件为 LeanCert 单引擎 spike，§1.4 双钉（数据集版本/复跑哈希）随 M2 正式窗口补齐，本件不预填；④ N=4 spike 档，N=36 典范维未试；⑤ scratch 湖仓 `/tmp/l96k` 为易失环境，制品哈希已入 §二留档，复跑需重建湖仓。
- **不越界**：本件不构成任何吸引子刻画、轨道包络、混沌存在或 PDE 层主张；NS 包档位不动，Clay NS **未解决、未颁奖**；OpenAI 相关成果口径「自评已核、外部复现中、未颁奖」。

**接主工程的前置条件（后续登记流程建议，供 M2 窗口判定席参考）**：
1. LeanCert 入 lakefile：按 LEANCERT-INTEGRATION-01 §1.1 追加 `require leancert from git "…" @ "d3e7f686…e8f43e"`（40-hex 全钉），接线后 `lake-manifest.json` 全文件 sha256 入册仓 ledger（L0-2 扩展）；本 spike 已实证该 commit 与 mathlib @56a00585 同链零冲突。
2. 使用面白名单纪律维持（§1.2）：仅 `LeanCert.Validity.Krawczyk` / `LeanCert.Engine.RootFinding.Krawczyk` / Core 伞；复算一律 kernel 档（`decide +kernel` 或 `(trust := kernel)`），CI 加 `leancert.trust` 审计钩（R6）。
3. 负控必拒与 replay 双钉（§1.4/TB-07）：M2 正式窗口须以 witness 栈独立复算对拍 + run id/日志哈希入册；本 spike 负控记录可作负控设计参照件。
4. 本件代码进主工程时的改写义务：盒端点闭式有理化 + `decide +kernel`（§5.3.2）；文件头 `CLASSIFY: L1` 注记；公理审计随件（`#print axioms` 输出形态见 §4.3）。

## 七、合规自检（本文件行文）

仓内主工程零触碰（全部构建于 /tmp/l96k，仓内唯一新件即本文件）；证书结果全部实跑、EXIT 码逐字在录，无编造；未复核项均标「未做/未定+理由」；LeanCert/mathlib rev 为 manifest 实测非转引；「kernel 层已证」表述限定于 §六限定域，未升格为 Lorenz-96 ODE 平衡态的主工程定理。一切等级/来源/归因变更遵循「裁决先行、登记同步、行文随后」。

—— EXT-WAVE-18 联邦续执行批二 R3 执行席 · 枢/PIVOT-01 体系 · 2026-10-21
