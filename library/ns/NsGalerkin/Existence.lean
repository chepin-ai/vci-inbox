-- CLASSIFY: L1
/-
WS-42 · Global existence for the Galerkin-truncated 2D Navier–Stokes ODE.

Uniform-step Picard–Lindelöf continuation driven by the Grönwall energy
a priori bound `‖x t‖² ≤ max ‖x a‖² (‖f‖²/ν²)`. Carried over from WS-41.
-/
import NsGalerkin.Basic
import Mathlib.Analysis.ODE.ExistUnique
open scoped InnerProductSpace

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

namespace GalerkinNS

variable (D : GalerkinNS E)

/-- Uniform Picard–Lindelöf step size: `δ = 1 / max C 1` with
`C = ν‖A‖(RB+1) + ‖B‖(RB+1)² + ‖f‖` bounding `‖F‖` on any unit ball whose
center has norm `≤ RB`. -/
def δC (D : GalerkinNS E) (RB : ℝ) : ℝ :=
  1 / max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1

theorem δC_pos (D : GalerkinNS E) (RB : ℝ) : 0 < D.δC RB := by
  have h : (0:ℝ) < max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=
    lt_of_lt_of_le zero_lt_one (le_max_right _ _)
  unfold δC
  positivity

/-- One uniform Picard–Lindelöf step: from any initial state `x₁` with
`‖x₁‖ ≤ RB`, a solution exists on `[t₀, t₀ + δC RB]`. -/
theorem solution_step (D : GalerkinNS E) [FiniteDimensional ℝ E] {RB : ℝ} (_hRB : 0 ≤ RB)
    {t₀ : ℝ} {x₁ : E} (hx₁ : ‖x₁‖ ≤ RB) :
    ∃ x : ℝ → E, x t₀ = x₁ ∧
      ∀ t ∈ Icc t₀ (t₀ + D.δC RB), HasDerivWithinAt x (D.vf (x t)) (Icc t₀ (t₀ + D.δC RB)) t := by
  haveI := FiniteDimensional.complete ℝ E
  have hδ : 0 < D.δC RB := D.δC_pos RB
  have hC1 : (0:ℝ) <
      max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=
    lt_of_lt_of_le zero_lt_one (le_max_right _ _)
  have hpl : IsPicardLindelof (fun _ => D.vf) (tmin := t₀) (tmax := t₀ + D.δC RB)
      ⟨t₀, mem_Icc.mpr ⟨le_refl _, le_add_of_nonneg_right hδ.le⟩⟩ x₁
      1 0 ⟨D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖, by
        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg
        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg
        have hRB1 : (0:ℝ) ≤ RB + 1 := add_nonneg (le_trans (norm_nonneg _) hx₁) zero_le_one
        exact add_nonneg (add_nonneg (mul_nonneg (mul_nonneg D.hν.le h1) hRB1)
          (mul_nonneg h2 (pow_nonneg hRB1 2))) (norm_nonneg _)⟩
      ⟨D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + 1), by
        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg
        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg
        have h3 : (0:ℝ) ≤ ‖x₁‖ + 1 := add_nonneg (norm_nonneg _) zero_le_one
        nlinarith [mul_nonneg D.hν.le h1, mul_nonneg h2 h3]⟩ :=
    { lipschitzOnWith := fun t _ => D.lipschitzOnWith_vf x₁ zero_le_one
      continuousOn := fun x _ => continuousOn_const
      norm_le := by
        intro t _ x hx
        have hxb : ‖x‖ ≤ RB + 1 := by
          have h : ‖x - x₁‖ ≤ (1:ℝ) := by
            rw [Metric.mem_closedBall, dist_eq_norm] at hx
            simpa using hx
          have hx' : ‖x‖ ≤ ‖x₁‖ + 1 := by
            calc ‖x‖ = ‖x - x₁ + x₁‖ := by simp
              _ ≤ ‖x - x₁‖ + ‖x₁‖ := norm_add_le _ _
              _ ≤ 1 + ‖x₁‖ := by linarith
              _ = ‖x₁‖ + 1 := by ring
          linarith
        have e := D.norm_vf_le x
        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg
        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg
        have hsq : ‖x‖ ^ 2 ≤ (RB + 1) ^ 2 := by gcongr
        show ‖D.vf x‖ ≤ D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖
        nlinarith [e, mul_le_mul_of_nonneg_left hxb (mul_nonneg D.hν.le h1),
          mul_le_mul_of_nonneg_left hsq h2]
      mul_max_le := by
        show (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) *
            max (t₀ + D.δC RB - t₀) (t₀ - t₀) ≤ (1:ℝ) - 0
        rw [sub_zero]
        have hmax : max (t₀ + D.δC RB - t₀) (t₀ - t₀) = D.δC RB := by
          rw [add_sub_cancel_left, sub_self, max_eq_left hδ.le]
        rw [hmax, δC, mul_one_div, div_le_iff₀ hC1]
        calc D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖
            ≤ max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 := le_max_left _ _
          _ = 1 * max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=
              (one_mul _).symm }
  obtain ⟨x, hx0, hx⟩ := hpl.exists_eq_forall_mem_Icc_hasDerivWithinAt₀
  exact ⟨x, hx0, hx⟩

/-- Energy identity (differential form) along a solution. -/
theorem energy_identity (D : GalerkinNS E) {a b : ℝ} {x : ℝ → E}
    (hx : ∀ t ∈ Icc a b, HasDerivWithinAt x (D.vf (x t)) (Icc a b) t) {t : ℝ}
    (ht : t ∈ Icc a b) :
    HasDerivWithinAt (fun s => ‖x s‖ ^ 2) (2 * ⟪x t, D.vf (x t)⟫_ℝ) (Icc a b) t :=
  (hx t ht).norm_sq

/-- Energy bound via Grönwall: along any solution on `[a,b]`,
`‖x t‖² ≤ max ‖x a‖² (‖f‖²/ν²)` — the a priori estimate that prevents blow-up. -/
theorem norm_sq_le_of_solution (D : GalerkinNS E) {a b : ℝ} (hab : a ≤ b) {x : ℝ → E}
    (hx : ∀ t ∈ Icc a b, HasDerivWithinAt x (D.vf (x t)) (Icc a b) t) :
    ∀ t ∈ Icc a b, ‖x t‖ ^ 2 ≤ max (‖x a‖ ^ 2) (‖D.f‖ ^ 2 / D.ν ^ 2) := by
  set g : ℝ → ℝ := fun t => ‖x t‖ ^ 2 with hg
  set g' : ℝ → ℝ := fun t => 2 * ⟪x t, D.vf (x t)⟫_ℝ with hg'
  set m := ‖D.f‖ ^ 2 / D.ν ^ 2 with hm
  have hm0 : 0 ≤ m := div_nonneg (sq_nonneg _) (sq_nonneg _)
  have hcx : ContinuousOn x (Icc a b) := fun t ht => (hx t ht).continuousWithinAt
  have hcont : ContinuousOn g (Icc a b) := by
    have h1 : ContinuousOn (fun t => ‖x t‖) (Icc a b) := continuous_norm.comp_continuousOn hcx
    have h2 : ContinuousOn (fun t => ‖x t‖ * ‖x t‖) (Icc a b) := h1.mul h1
    rw [hg]
    simpa [pow_two] using h2
  have hdg : ∀ t ∈ Ico a b, HasDerivWithinAt g (g' t) (Ici t) t := by
    intro t ht
    have h1 : HasDerivWithinAt x (D.vf (x t)) (Icc a b) t := hx t (Ico_subset_Icc_self ht)
    have hmem : Icc a b ∈ 𝓝[Ici t] t := mem_nhdsWithin.mpr
      ⟨Iio b, isOpen_Iio, ht.2, fun s hs => ⟨ht.1.trans hs.2, le_of_lt hs.1⟩⟩
    have h2 := (h1.mono_of_mem_nhdsWithin hmem).norm_sq
    rw [hg, hg']
    exact h2
  have hlim : ∀ t ∈ Ico a b, ∀ r, g' t < r →
      ∃ᶠ z in 𝓝[>] t, (z - t)⁻¹ * (g z - g t) < r := by
    intro t ht r hr
    have h := (hdg t ht).liminf_right_slope_le hr
    simpa only [slope, smul_eq_mul, vsub_eq_sub] using h
  have hbound : ∀ t ∈ Ico a b, g' t ≤ -D.ν * g t + ‖D.f‖ ^ 2 / D.ν := by
    intro t ht
    have h := D.inner_vf_le (x t)
    rw [real_inner_comm] at h
    have hν := D.hν
    have hν0 : D.ν ≠ 0 := ne_of_gt hν
    have h1 : D.ν * (‖D.f‖ ^ 2 / D.ν) = ‖D.f‖ ^ 2 := by field_simp
    have hamg : 2 * (‖D.f‖ * ‖x t‖) ≤ D.ν * (‖x t‖ ^ 2) + ‖D.f‖ ^ 2 / D.ν := by
      have h0 := mul_self_nonneg (D.ν * ‖x t‖ - ‖D.f‖)
      nlinarith [h0, h1, hν]
    rw [hg', hg]
    show 2 * ⟪x t, D.vf (x t)⟫_ℝ ≤ -D.ν * ‖x t‖ ^ 2 + ‖D.f‖ ^ 2 / D.ν
    nlinarith [h, hamg]
  intro t ht
  have hG := le_gronwallBound_of_liminf_deriv_right_le hcont hlim (le_refl (g a)) hbound t ht
  rw [gronwallBound_of_K_ne_0 (neg_ne_zero.mpr (ne_of_gt D.hν))] at hG
  simp only [] at hG
  have hs : 0 ≤ t - a := sub_nonneg.mpr ht.1
  set e := Real.exp (-D.ν * (t - a)) with he
  have he0 : 0 < e := he ▸ Real.exp_pos _
  have he1 : e ≤ 1 := by
    rw [he, Real.exp_le_one_iff]
    exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr D.hν.le) hs
  have hεm : ‖D.f‖ ^ 2 / D.ν / -D.ν = -m := by
    rw [hm, div_neg, div_div, ← pow_two]
  rw [hεm] at hG
  have hG' : g t ≤ g a * e + m * (1 - e) := by
    have hrw : g a * e + -m * (e - 1) = g a * e + m * (1 - e) := by ring
    rw [hrw] at hG
    exact hG
  rcases le_total (g a) m with hgm | hgm
  · rw [max_eq_right hgm]
    have p1 : g a * e ≤ m * e := mul_le_mul_of_nonneg_right hgm he0.le
    have p2 : 0 ≤ m * (1 - e) := mul_nonneg hm0 (sub_nonneg.mpr he1)
    have hsum : g a * e + m * (1 - e) ≤ m := by nlinarith [p1, p2]
    exact hG'.trans hsum
  · rw [max_eq_left hgm]
    have p1 : m * e ≤ g a * e := mul_le_mul_of_nonneg_right hgm he0.le
    have p2 : m * (1 - e) ≤ g a * (1 - e) :=
      mul_le_mul_of_nonneg_right hgm (sub_nonneg.mpr he1)
    have hsum : g a * e + m * (1 - e) ≤ g a := by nlinarith [p1, p2]
    exact hG'.trans hsum

/-- **Global existence for the Galerkin-truncated 2D Navier–Stokes ODE**:
for every `T ≥ 0` there is a solution on `[0, T]`. Proof: uniform-step
Picard–Lindelöf continuation, with the Grönwall energy bound keeping every
restart inside the ball of radius `max ‖x₀‖² (‖f‖²/ν²) + 1`. -/
theorem exists_solution_upto (D : GalerkinNS E) [FiniteDimensional ℝ E] (x₀ : E) {T : ℝ}
    (hT : 0 ≤ T) :
    ∃ x : ℝ → E, x 0 = x₀ ∧
      ∀ t ∈ Icc 0 T, HasDerivWithinAt x (D.vf (x t)) (Icc 0 T) t := by
  set m := ‖D.f‖ ^ 2 / D.ν ^ 2 with hm
  have hm0 : 0 ≤ m := div_nonneg (sq_nonneg _) (sq_nonneg _)
  set M := max (‖x₀‖ ^ 2) m with hM
  have hM0 : 0 ≤ M := le_max_of_le_left (sq_nonneg _)
  set RB := M + 1 with hRB
  have hRB0 : 0 ≤ RB := by rw [hRB]; linarith
  set δ := D.δC RB with hδ
  have hδ0 : 0 < δ := hδ ▸ D.δC_pos RB
  have hnorm_of_sq : ∀ y : E, ‖y‖ ^ 2 ≤ M → ‖y‖ ≤ RB := by
    intro y hy
    by_cases h1 : ‖y‖ ≤ 1
    · rw [hRB]; linarith
    · have h2 : ‖y‖ * 1 ≤ ‖y‖ * ‖y‖ :=
        mul_le_mul_of_nonneg_left ((not_le.mp h1).le) (norm_nonneg y)
      rw [hRB]
      nlinarith [h2, hy, hM0]
  have key : ∀ n : ℕ, ∃ x : ℝ → E, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 (((n : ℝ) + 1) * δ), HasDerivWithinAt x (D.vf (x t))
        (Icc 0 (((n : ℝ) + 1) * δ)) t) ∧
      (∀ t ∈ Icc 0 (((n : ℝ) + 1) * δ), ‖x t‖ ^ 2 ≤ M) := by
    intro n
    induction n with
    | zero =>
      have e0 : ((↑(0 : ℕ) + 1) * δ) = 0 + δ := by push_cast; ring
      rw [e0]
      obtain ⟨x, hx0, hx⟩ := D.solution_step hRB0 (t₀ := 0) (x₁ := x₀)
        (hnorm_of_sq x₀ (hM ▸ le_max_left _ _))
      rw [← hδ] at hx
      refine ⟨x, hx0, hx, fun t ht => ?_⟩
      have hB := D.norm_sq_le_of_solution (show (0:ℝ) ≤ 0 + δ from by linarith [hδ0.le])
        hx t ht
      rw [hx0] at hB
      calc ‖x t‖ ^ 2 ≤ max (‖x₀‖ ^ 2) (‖D.f‖ ^ 2 / D.ν ^ 2) := hB
        _ = M := by rw [← hm, ← hM]
    | succ n ih =>
      push_cast
      obtain ⟨xn, h0, hd, hb⟩ := ih
      set j := ((n : ℝ) + 1) * δ with hj
      have hj0 : 0 ≤ j := hj ▸ mul_nonneg
        (add_nonneg (Nat.cast_nonneg _) zero_le_one) hδ0.le
      have hje : j + δ = ((n : ℝ) + 1 + 1) * δ := by rw [hj]; ring
      rw [← hje]
      obtain ⟨y, hy0, hy⟩ := D.solution_step hRB0 (t₀ := j) (x₁ := xn j)
        (hnorm_of_sq (xn j) (hb j ⟨hj0, le_refl _⟩))
      rw [← hδ] at hy
      set z : ℝ → E := fun t => if t ≤ j then xn t else y t with hz
      have hzxn : ∀ s ∈ Icc 0 j, z s = xn s := fun s hs => by
        rw [hz]; exact if_pos hs.2
      have hzy : ∀ s ∈ Icc j (j + δ), z s = y s := fun s hs => by
        by_cases h : s ≤ j
        · have hsj : s = j := le_antisymm h hs.1
          have e1 : z s = xn s := by rw [hz]; exact if_pos h
          rw [e1, hsj, hy0]
        · rw [hz]; exact if_neg h
      have hz0 : z 0 = x₀ := by
        have : z 0 = xn 0 := by rw [hz]; exact if_pos hj0
        rw [this, h0]
      have hzj : z j = xn j := by rw [hz]; exact if_pos (le_refl j)
      have hzjy : z j = y j := by rw [hzj, hy0]
      have hzsol : ∀ t ∈ Icc 0 (j + δ),
          HasDerivWithinAt z (D.vf (z t)) (Icc 0 (j + δ)) t := by
        intro t ht
        by_cases htj : t ≤ j
        · rcases lt_or_eq_of_le htj with hlt | rfl
          · have hL : HasDerivWithinAt z (D.vf (xn t)) (Icc 0 j) t :=
              (hd t ⟨ht.1, htj⟩).congr (fun s hs => hzxn s hs) (hzxn t ⟨ht.1, htj⟩)
            rw [← hzxn t ⟨ht.1, htj⟩] at hL
            have hmem : Icc 0 j ∈ 𝓝[Icc 0 (j + δ)] t := mem_nhdsWithin.mpr
              ⟨Iio j, isOpen_Iio, hlt, fun s hs => ⟨hs.2.1, le_of_lt hs.1⟩⟩
            exact hL.mono_of_mem_nhdsWithin hmem
          · have hL : HasDerivWithinAt z (D.vf (xn j)) (Icc 0 j) j :=
              (hd j ⟨hj0, le_refl _⟩).congr (fun s hs => hzxn s hs) hzj
            rw [← hzj] at hL
            have hR : HasDerivWithinAt z (D.vf (y j)) (Icc j (j + δ)) j :=
              (hy j ⟨le_refl _, le_add_of_nonneg_right hδ0.le⟩).congr
                (fun s hs => hzy s hs) hzjy
            rw [← hzjy] at hR
            have := hL.union hR
            rwa [Icc_union_Icc_eq_Icc hj0 (le_add_of_nonneg_right hδ0.le)] at this
        · have hgt : j < t := lt_of_not_ge htj
          have hR : HasDerivWithinAt z (D.vf (y t)) (Icc j (j + δ)) t :=
            (hy t ⟨hgt.le, ht.2⟩).congr (fun s hs => hzy s hs)
              (hzy t ⟨hgt.le, ht.2⟩)
          rw [← hzy t ⟨hgt.le, ht.2⟩] at hR
          have hmem : Icc j (j + δ) ∈ 𝓝[Icc 0 (j + δ)] t := mem_nhdsWithin.mpr
            ⟨Ioi j, isOpen_Ioi, hgt, fun s hs => ⟨le_of_lt hs.1, hs.2.2⟩⟩
          exact hR.mono_of_mem_nhdsWithin hmem
      refine ⟨z, hz0, hzsol, fun t ht => ?_⟩
      have hB := D.norm_sq_le_of_solution (by linarith [hj0, hδ0.le]) hzsol t ht
      rw [hz0] at hB
      calc ‖z t‖ ^ 2 ≤ max (‖x₀‖ ^ 2) (‖D.f‖ ^ 2 / D.ν ^ 2) := hB
        _ = M := by rw [← hm, ← hM]
  -- final assembly: pick n with T ≤ (n+1)δ and restrict
  obtain ⟨n, hn⟩ := exists_nat_ge (T / δ)
  obtain ⟨x, hx0, hxd, _⟩ := key n
  have hδ0' : δ ≠ 0 := ne_of_gt hδ0
  have heq : T / δ * δ = T := by field_simp
  have hTle : T ≤ ((n : ℝ) + 1) * δ := by
    have h1 : T ≤ (n : ℝ) * δ := by
      nlinarith [mul_le_mul_of_nonneg_right hn hδ0.le, heq]
    nlinarith [h1, hδ0.le]
  refine ⟨x, hx0, fun t ht => ?_⟩
  exact (hxd t ⟨ht.1, ht.2.trans hTle⟩).mono (Icc_subset_Icc_right hTle)

end GalerkinNS

end NSGalerkin
