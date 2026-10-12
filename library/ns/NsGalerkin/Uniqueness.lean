-- CLASSIFY: L1
/-
WS-42 · Uniqueness of Galerkin-truncated Navier–Stokes trajectories.

WS-41 blocker `dist_le_of_trajectories` needed a *global* Lipschitz constant,
which the quadratic vector field does not have. This module closes the gap by
the standard self-contained route: any two solutions with the same initial
data remain, by the Grönwall energy a priori bound, inside a fixed closed ball
where the vector field *is* Lipschitz (`lipschitzOnWith_vf`); a localized
Grönwall estimate on the difference then forces the trajectories to coincide.

No new hypotheses are introduced: uniqueness is a theorem, not an assumption.
-/
import NsGalerkin.Existence

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

namespace GalerkinNS

variable (D : GalerkinNS E)

/-- **Localized trajectory estimate**: two solutions of the Galerkin ODE on
`[a,b]` that both stay in a common closed ball (where `vf` is Lipschitz with
the explicit constant `ν‖A‖ + 2‖B‖(‖x₁‖+R)`) diverge at most exponentially. -/
theorem dist_le_of_trajectories_in_ball (D : GalerkinNS E) {x₁ : E} {R : ℝ} (hR : 0 ≤ R)
    {a b : ℝ} (hab : a ≤ b) {x y : ℝ → E}
    (hx : ∀ t ∈ Icc a b, HasDerivWithinAt x (D.vf (x t)) (Icc a b) t)
    (hy : ∀ t ∈ Icc a b, HasDerivWithinAt y (D.vf (y t)) (Icc a b) t)
    (hxb : ∀ t ∈ Icc a b, x t ∈ Metric.closedBall x₁ R)
    (hyb : ∀ t ∈ Icc a b, y t ∈ Metric.closedBall x₁ R) :
    ∀ t ∈ Icc a b, dist (x t) (y t) ≤
      dist (x a) (y a) *
        Real.exp ((D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + R)) * (t - a)) := by
  have hL := D.lipschitzOnWith_vf x₁ hR
  rw [lipschitzOnWith_iff_dist_le_mul] at hL
  have hcont : ContinuousOn (fun s => x s - y s) (Icc a b) :=
    fun s hs => (hx s hs).continuousWithinAt.sub (hy s hs).continuousWithinAt
  have hderiv : ∀ s ∈ Ico a b,
      HasDerivWithinAt (fun s => x s - y s) (D.vf (x s) - D.vf (y s)) (Ici s) s := by
    intro s hs
    have hmem : Icc a b ∈ 𝓝[Ici s] s := mem_nhdsWithin.mpr
      ⟨Iio b, isOpen_Iio, hs.2, fun u hu => ⟨hs.1.trans hu.2, le_of_lt hu.1⟩⟩
    exact ((hx s (Ico_subset_Icc_self hs)).mono_of_mem hmem).sub
      ((hy s (Ico_subset_Icc_self hs)).mono_of_mem hmem)
  have hδ : ‖x a - y a‖ ≤ dist (x a) (y a) := (dist_eq_norm _ _).ge
  have hbound : ∀ s ∈ Ico a b, ‖D.vf (x s) - D.vf (y s)‖ ≤
      (D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + R)) * ‖x s - y s‖ + 0 := by
    intro s hs
    have hmem : s ∈ Icc a b := Ico_subset_Icc_self hs
    have e := hL (x s) (hxb s hmem) (y s) (hyb s hmem)
    rw [dist_eq_norm, dist_eq_norm] at e
    simpa using e
  intro t ht
  have hG := norm_le_gronwallBound_of_norm_deriv_right_le hcont hderiv hδ hbound t ht
  rw [dist_eq_norm]
  by_cases hK0 : (D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + R)) = 0
  · rw [hK0, gronwallBound_K0] at hG
    simpa [hK0] using hG
  · rw [gronwallBound_of_K_ne_0 hK0] at hG
    simpa using hG

/-- **Uniqueness inside the energy ball**: two solutions on `[a,b]` that agree
at `a` and both stay in a common closed ball coincide on the whole interval. -/
theorem eq_of_trajectories_in_ball (D : GalerkinNS E) {x₁ : E} {R : ℝ} (hR : 0 ≤ R)
    {a b : ℝ} (hab : a ≤ b) {x y : ℝ → E}
    (hx : ∀ t ∈ Icc a b, HasDerivWithinAt x (D.vf (x t)) (Icc a b) t)
    (hy : ∀ t ∈ Icc a b, HasDerivWithinAt y (D.vf (y t)) (Icc a b) t)
    (hxb : ∀ t ∈ Icc a b, x t ∈ Metric.closedBall x₁ R)
    (hyb : ∀ t ∈ Icc a b, y t ∈ Metric.closedBall x₁ R)
    (hxy : x a = y a) :
    ∀ t ∈ Icc a b, x t = y t := by
  intro t ht
  have h := D.dist_le_of_trajectories_in_ball hR hab hx hy hxb hyb t ht
  rw [hxy, dist_self] at h
  exact dist_le_zero.mp (by simpa using h)

/-- **Global uniqueness for the Galerkin-truncated 2D Navier–Stokes ODE**:
any two solutions on `[0, T]` with the same initial data coincide everywhere.
The energy a priori bound keeps both trajectories in the closed ball of radius
`max ‖x₀‖² (‖f‖²/ν²) + 1` around `0`, where `vf` is Lipschitz. -/
theorem solution_unique_upto (D : GalerkinNS E) {T : ℝ} (hT : 0 ≤ T) {x₀ : E} {x y : ℝ → E}
    (hx0 : x 0 = x₀) (hx : ∀ t ∈ Icc 0 T, HasDerivWithinAt x (D.vf (x t)) (Icc 0 T) t)
    (hy0 : y 0 = x₀) (hy : ∀ t ∈ Icc 0 T, HasDerivWithinAt y (D.vf (y t)) (Icc 0 T) t) :
    ∀ t ∈ Icc 0 T, x t = y t := by
  set M := max (‖x₀‖ ^ 2) (‖D.f‖ ^ 2 / D.ν ^ 2)
  have hM0 : 0 ≤ M := le_max_of_le_left (sq_nonneg _)
  set RB := M + 1 with hRB
  have hRB0 : 0 ≤ RB := by rw [hRB]; linarith
  have hnorm_of_sq : ∀ z : E, ‖z‖ ^ 2 ≤ M → ‖z‖ ≤ RB := by
    intro z hz
    by_cases h1 : ‖z‖ ≤ 1
    · rw [hRB]; linarith
    · have h2 : ‖z‖ * 1 ≤ ‖z‖ * ‖z‖ :=
        mul_le_mul_of_nonneg_left (le_of_not_le h1) (norm_nonneg z)
      rw [hRB]
      nlinarith [h2, hz, hM0]
  have hxb : ∀ t ∈ Icc 0 T, x t ∈ Metric.closedBall (0 : E) RB := by
    intro t ht
    have hb := D.norm_sq_le_of_solution hT hx t ht
    rw [hx0] at hb
    rw [Metric.mem_closedBall, dist_zero_right]
    exact hnorm_of_sq _ hb
  have hyb : ∀ t ∈ Icc 0 T, y t ∈ Metric.closedBall (0 : E) RB := by
    intro t ht
    have hb := D.norm_sq_le_of_solution hT hy t ht
    rw [hy0] at hb
    rw [Metric.mem_closedBall, dist_zero_right]
    exact hnorm_of_sq _ hb
  exact D.eq_of_trajectories_in_ball hRB0 hT hx hy hxb hyb (by rw [hx0, hy0])

/-- **Existence and uniqueness, bundled**: the Galerkin-truncated 2D
Navier–Stokes ODE with initial data `x₀` has exactly one solution on `[0, T]`. -/
theorem exists_unique_solution_upto (D : GalerkinNS E) [FiniteDimensional ℝ E] (x₀ : E) {T : ℝ}
    (hT : 0 ≤ T) :
    ∃ x : ℝ → E, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 T, HasDerivWithinAt x (D.vf (x t)) (Icc 0 T) t) ∧
      ∀ y : ℝ → E, y 0 = x₀ →
        (∀ t ∈ Icc 0 T, HasDerivWithinAt y (D.vf (y t)) (Icc 0 T) t) →
          ∀ t ∈ Icc 0 T, y t = x t := by
  obtain ⟨x, hx0, hx⟩ := D.exists_solution_upto x₀ hT
  exact ⟨x, hx0, hx, fun y hy0 hy t ht => D.solution_unique_upto hT hy0 hy hx0 hx t ht⟩

-- Axiom audit (printed at build time).
#print axioms GalerkinNS.dist_le_of_trajectories_in_ball
#print axioms GalerkinNS.solution_unique_upto
#print axioms GalerkinNS.exists_unique_solution_upto

end GalerkinNS

end NSGalerkin
