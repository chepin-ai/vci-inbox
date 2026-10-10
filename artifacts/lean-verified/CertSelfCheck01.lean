-- CLASSIFY: L1
-- CERT-SELFCHECK-01 · A1 检查器自证 Lean 化（SURGE01 少数派方向 vinf/ucif2/qfa 三票）
-- 模式：证书检查器返回 true ⟹ 语义性质成立（Krawczyk 式 accept⟹correct 的最小可信核）
-- 云端验证记录（Axle verify_proof，环境 lean-4.28.0，okay=true）：
--   add_sound   d9034a05-1956-43e9-87b0-c2bfe13ad989
--   neg_sound   44208d46-9489-4670-b171-91099fa33ad9
--   check_sound 082321e6-6aeb-4a89-b51c-ac2ab5e926e1
--   end_to_end  f3c1fc61-c0c0-4972-920e-9a3856c6453d
-- 公理审计：4/4 仅 [propext, Classical.choice, Quot.sound]，无 sorryAx。
import Mathlib

namespace SelfCheck

/-- 有理数闭区间。 -/
structure Iv where
  lo : ℚ
  hi : ℚ

/-- 隶属语义：x 落在区间内。 -/
def mem (x : ℚ) (iv : Iv) : Prop := iv.lo ≤ x ∧ x ≤ iv.hi

/-- 区间加法（证书运算步骤）。 -/
def add (a b : Iv) : Iv := ⟨a.lo + b.lo, a.hi + b.hi⟩

/-- 步骤正确性：加法步骤保持隶属。 -/
theorem add_sound (x y : ℚ) (a b : Iv) (hx : mem x a) (hy : mem y b) :
    mem (x + y) (add a b) := by
  obtain ⟨hxl, hxu⟩ := hx
  obtain ⟨hyl, hyu⟩ := hy
  constructor
  · show a.lo + b.lo ≤ x + y; linarith
  · show x + y ≤ a.hi + b.hi; linarith

/-- 区间取负（证书运算步骤）。 -/
def neg (a : Iv) : Iv := ⟨-a.hi, -a.lo⟩

theorem neg_sound (x : ℚ) (a : Iv) (hx : mem x a) : mem (-x) (neg a) := by
  obtain ⟨hxl, hxu⟩ := hx
  constructor
  · show -a.hi ≤ -x; linarith
  · show -x ≤ -a.lo; linarith

/-- 有界性检查器：命题层判定 -B ≤ lo ∧ hi ≤ B。 -/
def check (iv : Iv) (B : ℚ) : Prop := -B ≤ iv.lo ∧ iv.hi ≤ B

/-- 检查器正确性（自证核）：检查通过 ⟹ 区间内一切元素的绝对值被 B 界住。 -/
theorem check_sound (iv : Iv) (B : ℚ) (h : check iv B) (x : ℚ) (hx : mem x iv) :
    |x| ≤ B := by
  obtain ⟨hl, hu⟩ := h
  obtain ⟨hxl, hxu⟩ := hx
  rw [abs_le]
  constructor <;> linarith

/-- 端到端复合：先算证书（add/neg 组合），再由检查器背书语义结论。 -/
theorem end_to_end (x y : ℚ) (a b : Iv) (B : ℚ)
    (hx : mem x a) (hy : mem y b) (h : check (add a (neg b)) B) :
    |x - y| ≤ B := by
  have h1 : mem (x + -y) (add a (neg b)) := add_sound x (-y) a (neg b) hx (neg_sound y b hy)
  have h2 := check_sound _ B h _ h1
  rw [sub_eq_add_neg]
  exact h2
end SelfCheck
