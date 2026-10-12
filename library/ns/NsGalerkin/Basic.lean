-- CLASSIFY: L1
/-
WS-42 · 2D Navier–Stokes Galerkin truncation: proof kernel (abstract layer).

Finite-dimensional ODE layer:
`F(x) = -ν • A x + B x x + f` on a real inner product space `E`, with
`A` coercive (Stokes operator, `‖x‖² ≤ ⟪A x, x⟫`) and `B` the projected
bilinear nonlinearity satisfying the Galerkin energy cancellation
`⟪B u u, u⟫ = 0`.

Proven kernel carried over from WS-41 (feasibility skeleton, GO verdict);
module split and proof extensions (uniqueness, explicit three-mode `B`)
are WS-42 work.

Toolchain: Lean 4.10.0 + mathlib v4.10.0.
-/
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Data of a Galerkin-truncated 2D Navier–Stokes system on the energy space `E`:
viscosity `ν > 0`, coercive Stokes operator `A` (`‖x‖² ≤ ⟪A x, x⟫`),
projected bilinear nonlinearity `B` with the energy cancellation
`⟪B u u, u⟫ = 0` (skew-symmetry of the trilinear form `b(u,u,u) = 0`,
a standard identity for any divergence-free Galerkin basis), and forcing `f`. -/
structure GalerkinNS (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] where
  ν : ℝ
  hν : 0 < ν
  A : E →L[ℝ] E
  hA : ∀ x : E, ‖x‖ ^ 2 ≤ ⟪A x, x⟫_ℝ
  B : E →L[ℝ] E →L[ℝ] E
  hB : ∀ u : E, ⟪B u u, u⟫_ℝ = 0
  f : E

namespace GalerkinNS

variable (D : GalerkinNS E)

/-- The Galerkin ODE vector field `F(x) = -ν • A x + B x x + f`. -/
def vf (D : GalerkinNS E) (x : E) : E := -(D.ν • D.A x) + D.B x x + D.f

/-- Energy form of the vector field: `⟪F x, x⟫ = -ν ⟪A x, x⟫ + ⟪f, x⟫`
(the nonlinear term drops out by the cancellation hypothesis). -/
theorem inner_vf (x : E) : ⟪D.vf x, x⟫_ℝ = -D.ν * ⟪D.A x, x⟫_ℝ + ⟪D.f, x⟫_ℝ := by
  unfold vf
  rw [inner_add_left, inner_add_left, inner_neg_left, real_inner_smul_left, D.hB]
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
    rw [map_sub, ContinuousLinearMap.sub_apply]
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
      _ ≤ (‖-(D.ν • D.A x)‖ + ‖D.B x x‖) + ‖D.f‖ := add_le_add_right h2 _
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
  rw [lipschitzOnWith_iff_dist_le_mul]
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
            add_le_add_right h5 _
        _ = ‖-(D.ν • D.A (x - y))‖ + ‖D.B (x - y) x‖ + ‖D.B y (x - y)‖ := by ring
    have hB0 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg
    have hxy := norm_nonneg (x - y)
    nlinarith [h6, e1, e2, e3, hxb, hyb,
      mul_le_mul_of_nonneg_left hxb (mul_nonneg hB0 hxy),
      mul_le_mul_of_nonneg_left hyb (mul_nonneg hB0 hxy)]
  exact key

end GalerkinNS

end NSGalerkin
