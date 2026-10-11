-- CLASSIFY: L1
import Mathlib.Algebra.Order.GroupWithZero.Basic
import Mathlib.Algebra.Order.GroupWithZero.Defs
import Mathlib.Algebra.Order.Monoid.Unbundled.Basic
import Mathlib.Algebra.Order.Ring.Rat

/-!
# AnchorCert — PIVOT-01 WS-25 · 锚证书演示器（M1 试点）

演示「数值锚 → Lean 可验证陈述」焊缝闭环的最小通路：

* `IvQ`：有理数闭区间及其 membership 谓词；
* `IvQ.mem_add`：区间加法 soundness（`add_le_add`）；
* `IvQ.mem_mul`：非负区间乘法 soundness（`0 ≤ lo` 前提下 `mul_le_mul`）；
* `Cert` / `Cert.check` / `Cert.check_sound`：可执行检查器及其 soundness 定理；
* fuzz 锚实例：`120 = 30 + 60 + 30` 的加法证书，`check` 编译期求值为 `true`，
  且 soundness 定理可直接回读为内核命题。

## 如实声明（边界）

本文件只是**小样演示器**：证明小型锚谓词可以完全在 Lean 内核内机器验证。
它**不**声称 CIRC 族可移植到 Lean——FINDING-04 仍然成立
（CIRC 族因 leancert 缺 `Expr.log` 而不可 Lean 化，其认证仍由 Python 区间层承载）。

环境：Lean `4.35.0-rc2` + mathlib `9fe29c4b379922f49446b28b76cbe4fce041c8b3`。
零 `sorry`、零额外 `axiom`（文末 `#print axioms` 自证仅依赖标准公理）。
-/

namespace AnchorCert

/-- 有理数闭区间 `[lo, hi]`。 -/
structure IvQ where
  lo : ℚ
  hi : ℚ
deriving Repr

/-- `x` 落在区间 `a` 内（闭区间语义）：`a.lo ≤ x ∧ x ≤ a.hi`。 -/
def IvQ.mem (x : ℚ) (a : IvQ) : Prop :=
  a.lo ≤ x ∧ x ≤ a.hi

/-- 区间加法：端点分别相加。 -/
def IvQ.add (a b : IvQ) : IvQ :=
  ⟨a.lo + b.lo, a.hi + b.hi⟩

/-- 区间加法 soundness：两锚各自落区间，则其和落在端点和区间内。 -/
theorem IvQ.mem_add {x y : ℚ} {a b : IvQ}
    (hx : IvQ.mem x a) (hy : IvQ.mem y b) :
    IvQ.mem (x + y) (IvQ.add a b) :=
  ⟨add_le_add hx.1 hy.1, add_le_add hx.2 hy.2⟩

/-- 区间乘法：端点分别相乘（仅在非负区间上 sound）。 -/
def IvQ.mul (a b : IvQ) : IvQ :=
  ⟨a.lo * b.lo, a.hi * b.hi⟩

/-- 非负区间乘法 soundness：`0 ≤ lo` 前提下，积落在端点积区间内。 -/
theorem IvQ.mem_mul {x y : ℚ} {a b : IvQ}
    (ha : 0 ≤ a.lo) (hb : 0 ≤ b.lo)
    (hx : IvQ.mem x a) (hy : IvQ.mem y b) :
    IvQ.mem (x * y) (IvQ.mul a b) := by
  have hx0 : 0 ≤ x := le_trans ha hx.1
  have hy0 : 0 ≤ y := le_trans hb hy.1
  have hha : 0 ≤ a.hi := le_trans hx0 hx.2
  exact ⟨mul_le_mul hx.1 hy.1 hb hx0, mul_le_mul hx.2 hy.2 hy0 hha⟩

/-- 锚证书：声称 `val ∈ [lo, hi]`。 -/
structure Cert where
  val : ℚ
  lo : ℚ
  hi : ℚ
deriving Repr

/-- 可执行检查：两端比较均成立才返回 `true`。 -/
def Cert.check (c : Cert) : Bool :=
  decide (c.lo ≤ c.val ∧ c.val ≤ c.hi)

/-- 检查器 soundness：`check` 通过则锚命题在内核中成立。 -/
theorem Cert.check_sound (c : Cert) (h : c.check = true) :
    c.lo ≤ c.val ∧ c.val ≤ c.hi :=
  of_decide_eq_true h

/-! ## fuzz 锚实例：`120 = 30 + 60 + 30` 的加法证书 -/

/-- fuzz 子锚区间：`[30, 30]`、`[60, 60]`、`[30, 30]`。 -/
def fuzzIvA : IvQ := ⟨30, 30⟩
def fuzzIvB : IvQ := ⟨60, 60⟩
def fuzzIvC : IvQ := ⟨30, 30⟩

/-- 由 `mem_add` 两次合成：`30 + 60 + 30` 落在合成区间 `[120, 120]` 内。 -/
theorem fuzz_anchor_mem :
    IvQ.mem (30 + 60 + 30) ((fuzzIvA.add fuzzIvB).add fuzzIvC) :=
  IvQ.mem_add (x := 30 + 60) (y := 30)
    (a := fuzzIvA.add fuzzIvB) (b := fuzzIvC)
    (IvQ.mem_add (x := 30) (y := 60) (a := fuzzIvA) (b := fuzzIvB)
      ⟨le_refl _, le_refl _⟩ ⟨le_refl _, le_refl _⟩)
    ⟨le_refl _, le_refl _⟩

/-- 数值锚等式：`30 + 60 + 30 = 120`，由 `grind` 证明（`Rat.add` 为 `@[irreducible]`，
    内核 `rfl`/`decide` 归约在部分导入上下文中不可靠，`grind` 生成内核可验证明项）。 -/
theorem fuzz_sum : (30 + 60 + 30 : ℚ) = 120 := by grind

/-- 同一合成在字面量 `120` 上汇合（经 `fuzz_sum` 改写，无需隐式 defeq）。 -/
example : IvQ.mem (120 : ℚ) ((fuzzIvA.add fuzzIvB).add fuzzIvC) :=
  fuzz_sum ▸ fuzz_anchor_mem

/-- fuzz 锚证书：`val = 120`，锚区间 `[120, 120]`。 -/
def fuzzCert : Cert := ⟨120, 120, 120⟩

-- 可执行检查编译期求值为 `true`（`#guard` 是编译期断言）。
#guard fuzzCert.check = true

-- 同一事实作为可复用命题：`check` 返回 `true`，由内核判定。
theorem fuzzCert_check : fuzzCert.check = true := by decide

/-- soundness 定理回读：`check` 的真值升格为内核命题。 -/
example : fuzzCert.lo ≤ fuzzCert.val ∧ fuzzCert.val ≤ fuzzCert.hi :=
  fuzzCert.check_sound fuzzCert_check

/-- 乘法演示：非负区间 `[2, 3] · [4, 5]` 容纳乘积 `2 · 4`（区间下界 `8`）；
    另有 `2 · 4 ≤ 12` 的 `grind` 证书锚定上界数值。 -/
theorem two_mul_four_le : (2 : ℚ) * 4 ≤ 12 := by grind

example : IvQ.mem ((2 : ℚ) * 4) ((⟨2, 3⟩ : IvQ).mul (⟨4, 5⟩ : IvQ)) :=
  IvQ.mem_mul (x := 2) (y := 4) (a := ⟨2, 3⟩) (b := ⟨4, 5⟩)
    (by decide) (by decide) ⟨by decide, by decide⟩ ⟨by decide, by decide⟩

end AnchorCert

#print axioms AnchorCert.IvQ.mem_add
#print axioms AnchorCert.IvQ.mem_mul
#print axioms AnchorCert.Cert.check_sound
#print axioms AnchorCert.fuzz_anchor_mem
#print axioms AnchorCert.fuzzCert_check
