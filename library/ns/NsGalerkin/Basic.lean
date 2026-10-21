-- CLASSIFY: L1
/-
WS-42 · 2D Navier–Stokes Galerkin truncation: proof kernel (abstract layer).

Finite-dimensional ODE layer:
`F(x) = -ν • A x + B x x + f` on a real inner product space `E`, with
`A` coercive (Stokes operator, `‖x‖² ≤ ⟪A x, x⟫`) and `B` the projected
bilinear nonlinearity carrying the skew-symmetric energy cancellation
field `hskew : ⟪B u u, u⟫ = 0` (M1-4/L1-1 migration: the former field
`hB` is repackaged as `hskew`, same diagonal content — see
`NsGalerkin/SkewB.lean` for the seam-facing strengthened interface).

Proven kernel carried over from WS-41 (feasibility skeleton, GO verdict);
module split and proof extensions (uniqueness, explicit three-mode `B`)
are WS-42 work; the `hB → hskew` field migration is WS-A M1-4 work.

Toolchain: Lean 4.10.0 + mathlib v4.10.0.
-/
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.Dual
open scoped InnerProductSpace

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Data of a Galerkin-truncated 2D Navier–Stokes system on the energy space `E`:
viscosity `ν > 0`, coercive Stokes operator `A` (`‖x‖² ≤ ⟪A x, x⟫`),
projected bilinear nonlinearity `B` with the skew-symmetric energy
cancellation field `hskew : ∀ u, ⟪B u u, u⟫ = 0` (the diagonal of the
skew-symmetry of the trilinear form `b(u,u,u) = 0`, a standard identity
for any divergence-free Galerkin basis), and forcing `f`.

M1-4/L1-1 (EXT-WAVE-18): the field is named `hskew` to expose the
skew-symmetric cancellation interface at downstream seams; its content is
exactly the diagonal cancellation that the kernel consumes (`inner_vf`).
The strengthened uniform diagonal `∀ u v, ⟪B u v, v⟫ = 0` (polarizing to
full `(2,3)`-skew-symmetry) lives in `NsGalerkin/SkewB.lean` as
`SkewNonlinearity.hskew_full`; it is strictly stronger and is *not*
satisfied by the machine-checked instances `skewB`/`B₃`, hence is not the
field semantics (code-fact decision, registered deviation). -/
structure GalerkinNS (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] where
  ν : ℝ
  hν : 0 < ν
  A : E →L[ℝ] E
  hA : ∀ x : E, ‖x‖ ^ 2 ≤ ⟪A x, x⟫_ℝ
  B : E →L[ℝ] E →L[ℝ] E
  hskew : ∀ u : E, ⟪B u u, u⟫_ℝ = 0
  f : E

namespace GalerkinNS

variable (D : GalerkinNS E)

/-- The Galerkin ODE vector field `F(x) = -ν • A x + B x x + f`. -/
def vf (D : GalerkinNS E) (x : E) : E := -(D.ν • D.A x) + D.B x x + D.f

/-- Energy form of the vector field: `⟪F x, x⟫ = -ν ⟪A x, x⟫ + ⟪f, x⟫`
(the nonlinear term drops out by the skew-cancellation field `hskew`). -/
theorem inner_vf (x : E) : ⟪D.vf x, x⟫_ℝ = -D.ν * ⟪D.A x, x⟫_ℝ + ⟪D.f, x⟫_ℝ := by
  unfold vf
  rw [inner_add_left, inner_add_left, inner_neg_left, real_inner_smul_left, D.hskew x]
  ring

/-- Dissipativity: `⟪F x, x⟫ ≤ -ν ‖x‖² + ‖f‖ ‖x‖`. -/
theorem inner_vf_le (x : E) : ⟪D.vf x, x⟫_ℝ ≤ -D.ν * ‖x‖ ^ 2 + ‖D.f‖ * ‖x‖ := by
  rw [inner_vf]
  have h1 : -D.ν * ⟪D.A x, x⟫_ℝ ≤ -D.ν * ‖x‖ ^ 2 := by
    have := D.hA x
    have hν := D.hν
    nlinarith [mul_le_mul_of_nonpos_left this (neg_nonpos.mpr hν.le)]
  have h2 : ⟪D.f, x⟫_ℝ ≤ ‖D.f‖ * ‖x‖ :=
    (le_abs_self _).trans (abs_real_inner_le_norm _ _)
  linarith

/-- `B (x-y) x + B y (x-y) = B x x - B y y` (bilinearity splitting). -/
theorem B_split (x y : E) : D.B (x - y) x + D.B y (x - y) = D.B x x - D.B y y := by
  have h1 : D.B (x - y) x = D.B x x - D.B y x := by
    rw [map_sub, sub_apply]
  have h2 : D.B y (x - y) = D.B y x - D.B y y := map_sub _ _ _
  rw [h1, h2]
  abel

/-- Norm bound on the vector field: `‖F x‖ ≤ ν‖A‖‖x‖ + ‖B‖‖x‖² + ‖f‖`. -/
theorem norm_vf_le (x : E) :
    ‖D.vf x‖ ≤ D.ν * ‖D.A‖ * ‖x‖ + ‖D.B‖ * ‖x‖ ^ 2 + ‖D.f‖ := by
  have e1 : ‖-(D.ν • D.A x)‖ ≤ D.ν * ‖D.A‖ * ‖x‖ := by
    rw [norm_neg, norm_smul, Real.norm_of_nonneg D.hν.le, mul_assoc]
    exact mul_le_mul_of_nonneg_left (D.A.le_opNorm x) D.hν.le
  have e2 : ‖D.B x x‖ ≤ ‖D.B‖ * ‖x‖ ^ 2 := by
    calc ‖D.B x x‖ ≤ ‖D.B x‖ * ‖x‖ := (D.B x).le_opNorm x
      _ ≤ ‖D.B‖ * ‖x‖ * ‖x‖ :=
          mul_le_mul_of_nonneg_right (D.B.le_opNorm x) (norm_nonneg _)
      _ = ‖D.B‖ * ‖x‖ ^ 2 := by ring
  have h1 := norm_add_le (-(D.ν • D.A x) + D.B x x) D.f
  have h2 := norm_add_le (-(D.ν • D.A x)) (D.B x x)
  have : ‖D.vf x‖ ≤ ‖-(D.ν • D.A x)‖ + ‖D.B x x‖ + ‖D.f‖ := by
    calc ‖D.vf x‖ ≤ ‖-(D.ν • D.A x) + D.B x x‖ + ‖D.f‖ := h1
      _ ≤ (‖-(D.ν • D.A x)‖ + ‖D.B x x‖) + ‖D.f‖ := add_le_add_left h2 _
  linarith

/-- The vector field is Lipschitz on any closed ball, with explicit constant
`ν‖A‖ + 2‖B‖(‖x₁‖ + R)`. -/
theorem lipschitzOnWith_vf (x₁ : E) {R : ℝ} (hR : 0 ≤ R) :
    LipschitzOnWith (⟨D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + R), by
        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg
        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg
        have h3 : (0:ℝ) ≤ ‖x₁‖ + R := add_nonneg (norm_nonneg _) hR
        nlinarith [mul_nonneg D.hν.le h1, mul_nonneg h2 h3]⟩ : ℝ≥0)
      D.vf (Metric.closedBall x₁ R) := by
  refine LipschitzOnWith.of_dist_le_mul ?_
  intro x hx y hy
  have hxb : ‖x‖ ≤ ‖x₁‖ + R := by
    have h : ‖x - x₁‖ ≤ R := by rwa [Metric.mem_closedBall, dist_eq_norm] at hx
    calc ‖x‖ = ‖x - x₁ + x₁‖ := by simp
      _ ≤ ‖x - x₁‖ + ‖x₁‖ := norm_add_le _ _
      _ = ‖x₁‖ + ‖x - x₁‖ := by ring
      _ ≤ ‖x₁‖ + R := by linarith
  have hyb : ‖y‖ ≤ ‖x₁‖ + R := by
    have h : ‖y - x₁‖ ≤ R := by rwa [Metric.mem_closedBall, dist_eq_norm] at hy
    calc ‖y‖ = ‖y - x₁ + x₁‖ := by simp
      _ ≤ ‖y - x₁‖ + ‖x₁‖ := norm_add_le _ _
      _ = ‖x₁‖ + ‖y - x₁‖ := by ring
      _ ≤ ‖x₁‖ + R := by linarith
  have hsub : D.vf x - D.vf y = -(D.ν • D.A (x - y)) + (D.B (x - y) x + D.B y (x - y)) := by
    unfold vf
    rw [B_split, map_sub D.A x y, smul_sub]
    abel
  have e1 : ‖-(D.ν • D.A (x - y))‖ ≤ D.ν * ‖D.A‖ * ‖x - y‖ := by
    rw [norm_neg, norm_smul, Real.norm_of_nonneg D.hν.le, mul_assoc]
    exact mul_le_mul_of_nonneg_left (D.A.le_opNorm _) D.hν.le
  have e2 : ‖D.B (x - y) x‖ ≤ ‖D.B‖ * ‖x - y‖ * ‖x‖ :=
    ((D.B (x - y)).le_opNorm x).trans
      (mul_le_mul_of_nonneg_right (D.B.le_opNorm _) (norm_nonneg _))
  have e3 : ‖D.B y (x - y)‖ ≤ ‖D.B‖ * ‖y‖ * ‖x - y‖ :=
    ((D.B y).le_opNorm (x - y)).trans
      (mul_le_mul_of_nonneg_right (D.B.le_opNorm _) (norm_nonneg _))
  have h4 := norm_add_le (-(D.ν • D.A (x - y))) (D.B (x - y) x + D.B y (x - y))
  have h5 := norm_add_le (D.B (x - y) x) (D.B y (x - y))
  rw [dist_eq_norm, hsub, dist_eq_norm]
  have key : ‖-(D.ν • D.A (x - y)) + (D.B (x - y) x + D.B y (x - y))‖
      ≤ (D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + R)) * ‖x - y‖ := by
    have h6 : ‖-(D.ν • D.A (x - y)) + (D.B (x - y) x + D.B y (x - y))‖
        ≤ ‖-(D.ν • D.A (x - y))‖ + ‖D.B (x - y) x‖ + ‖D.B y (x - y)‖ := by
      calc _ ≤ ‖-(D.ν • D.A (x - y))‖ + ‖D.B (x - y) x + D.B y (x - y)‖ := h4
        _ = ‖D.B (x - y) x + D.B y (x - y)‖ + ‖-(D.ν • D.A (x - y))‖ := by ring
        _ ≤ (‖D.B (x - y) x‖ + ‖D.B y (x - y)‖) + ‖-(D.ν • D.A (x - y))‖ :=
            add_le_add_left h5 _
        _ = ‖-(D.ν • D.A (x - y))‖ + ‖D.B (x - y) x‖ + ‖D.B y (x - y)‖ := by ring
    have hB0 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg
    have hxy := norm_nonneg (x - y)
    nlinarith [h6, e1, e2, e3, hxb, hyb,
      mul_le_mul_of_nonneg_left hxb (mul_nonneg hB0 hxy),
      mul_le_mul_of_nonneg_left hyb (mul_nonneg hB0 hxy)]
  exact key

section DAWaveB
/-! ### WS-B 降级档 · D-A（E9 逐项同构改写，EXT-WAVE-18 续执行批）

以下 decl 是本有限维 ODE 截断层（E9，联邦口径）对 FGL-SEAM-SPEC-01
单元① 1.1 的**同构对齐改写**（改写非新证，不引入任何新假设）：

1. **显式对流界 `C_b` 数据化**：`Cb := ‖B‖` 以显式常数携带对流界
   `‖B u v‖ ≤ Cb·‖u‖·‖v‖`（规格「配显式常数 `C_b`，
   `‖c(u,v,·)‖ ≤ C_b‖u‖‖v‖`」口径；既有算子范数两步界的逐项数据化）。
2. **时间依赖对偶外力变体（Riesz 组装模式）**：`vfT`/`rieszRhs`——
   对偶外力 `F : ℝ → E →L[ℝ] ℝ` 经 Riesz 表示元组装右端
   （规格「`r(t,u)` 为泛函 `v ↦ -d(u,v)-c(u,u,v)+F(t)v` 的 Riesz 表示元」
   口径；本层 `d(u,v) = ν⟪A u, v⟫`、`c(u,u,v) = ⟪B u u, v⟫`）。
   常值外力 `F t = toDual D.f` 逐项退化回既有 `vf`
   （`rieszRhs_const`/`vfT_const`），故既有存在/唯一/先验界定理
   经此同构逐字迁移，常值向量外力是对偶外力的数学特例。 -/

/-- 显式对流界常数（数据化）：`Cb := ‖B‖`。 -/
def Cb (D : GalerkinNS E) : ℝ := ‖D.B‖

/-- 显式对流界常数非负。 -/
theorem Cb_nonneg (D : GalerkinNS E) : 0 ≤ D.Cb := D.B.opNorm_nonneg

/-- 显式对流界：`‖B u v‖ ≤ Cb·‖u‖·‖v‖`
（既有 `norm_vf_le` 内部两步算子范数界的逐项数据化形式）。 -/
theorem norm_B_apply_le (D : GalerkinNS E) (u v : E) :
    ‖D.B u v‖ ≤ D.Cb * ‖u‖ * ‖v‖ := by
  calc ‖D.B u v‖ ≤ ‖D.B u‖ * ‖v‖ := (D.B u).le_opNorm v
    _ ≤ ‖D.B‖ * ‖u‖ * ‖v‖ :=
        mul_le_mul_of_nonneg_right (D.B.le_opNorm u) (norm_nonneg _)
    _ = D.Cb * ‖u‖ * ‖v‖ := rfl

/-- 时间依赖外力（向量形式）的右端变体：
`vfT F t x = -(ν • A x) + B x x + F t`。 -/
def vfT (D : GalerkinNS E) (F : ℝ → E) (t : ℝ) (x : E) : E :=
  -(D.ν • D.A x) + D.B x x + F t

/-- 常值外力特例：`vfT (fun _ => D.f)` 与既有 `vf` 定义性相等（同构对齐）。 -/
theorem vfT_const (D : GalerkinNS E) (t : ℝ) (x : E) :
    D.vfT (fun _ => D.f) t x = D.vf x := rfl

/-- `vfT` 的能量形式：`⟪vfT F t x, x⟫ = -ν⟪A x, x⟫ + ⟪F t, x⟫`
（与 `inner_vf` 逐项同构；对流项仍由 `hskew` 严格抵消）。 -/
theorem inner_vfT (D : GalerkinNS E) (F : ℝ → E) (t : ℝ) (x : E) :
    ⟪D.vfT F t x, x⟫_ℝ = -D.ν * ⟪D.A x, x⟫_ℝ + ⟪F t, x⟫_ℝ := by
  unfold vfT
  rw [inner_add_left, inner_add_left, inner_neg_left, real_inner_smul_left, D.hskew x]
  ring

-- Riesz 表示（`InnerProductSpace.toDual`）需底空间完备；
-- 本截断层的应用场景均为有限维（自动完备），此处按需局部引入。
variable [CompleteSpace E]

/-- Riesz 组装的右端：时间依赖**对偶**外力 `F : ℝ → E →L[ℝ] ℝ` 下，
`r(t, x)` 定义为泛函 `v ↦ -ν⟪A x, v⟫ + ⟪B x x, v⟫ + F t v` 的 Riesz 表示元
（规格单元① 1.1 的组装模式：全程只需弱型，无需把 Stokes 算子当作
能量空间上的有界算子）。 -/
def rieszRhs (D : GalerkinNS E) (F : ℝ → E →L[ℝ] ℝ) (t : ℝ) (x : E) : E :=
  (InnerProductSpace.toDual ℝ E).symm
    ((-D.ν) • InnerProductSpace.toDual ℝ E (D.A x) +
      InnerProductSpace.toDual ℝ E (D.B x x) + F t)

/-- Riesz 组装的向量形式展开：Riesz 表示元逐项回到算子值。 -/
theorem rieszRhs_eq (D : GalerkinNS E) (F : ℝ → E →L[ℝ] ℝ) (t : ℝ) (x : E) :
    D.rieszRhs F t x =
      -(D.ν • D.A x) + D.B x x + (InnerProductSpace.toDual ℝ E).symm (F t) := by
  unfold rieszRhs
  rw [map_add, map_add, map_smulₛₗ, LinearIsometryEquiv.symm_apply_apply,
    LinearIsometryEquiv.symm_apply_apply, starRingEnd_apply, star_trivial, neg_smul]

/-- Riesz 组装与向量形式一致：对偶外力取 `F t = toDual (fvec t)` 时
`rieszRhs` 逐项回到 `vfT`（同构对齐，非新证）。 -/
theorem rieszRhs_eq_vfT (D : GalerkinNS E) (fvec : ℝ → E) (t : ℝ) (x : E) :
    D.rieszRhs (fun t => InnerProductSpace.toDual ℝ E (fvec t)) t x =
      D.vfT fvec t x := by
  rw [rieszRhs_eq, LinearIsometryEquiv.symm_apply_apply]
  rfl

/-- 常值对偶外力特例：`rieszRhs (fun _ => toDual D.f)` 逐项回到既有 `vf`。 -/
theorem rieszRhs_const (D : GalerkinNS E) (t : ℝ) (x : E) :
    D.rieszRhs (fun _ => InnerProductSpace.toDual ℝ E D.f) t x = D.vf x := by
  rw [rieszRhs_eq_vfT, vfT_const]

/-- Riesz 组装右端的能量形式：
`⟪r(t, x), x⟫ = -ν⟪A x, x⟫ + F t x`（对流项由 `hskew` 严格抵消；
与 `inner_vf` 逐项同构，对偶外力经 `toDual_symm_apply` 展开）。 -/
theorem inner_rieszRhs (D : GalerkinNS E) (F : ℝ → E →L[ℝ] ℝ) (t : ℝ) (x : E) :
    ⟪D.rieszRhs F t x, x⟫_ℝ = -D.ν * ⟪D.A x, x⟫_ℝ + F t x := by
  rw [rieszRhs_eq, inner_add_left, inner_add_left, inner_neg_left,
    real_inner_smul_left, D.hskew x, InnerProductSpace.toDual_symm_apply]
  ring

-- D-A 件公理审计（构建期打印）。
#print axioms GalerkinNS.norm_B_apply_le
#print axioms GalerkinNS.inner_vfT
#print axioms GalerkinNS.rieszRhs_eq_vfT
#print axioms GalerkinNS.inner_rieszRhs

end DAWaveB

end GalerkinNS

end NSGalerkin
