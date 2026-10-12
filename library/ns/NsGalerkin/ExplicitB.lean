-- CLASSIFY: L1
/-
WS-42 · Explicit three-mode nonlinearity on `ModeSpace 1 = EuclideanSpace ℝ (Fin 3)`.

A fully explicit, machine-checked sample of the "abstract → explicit" seam:
instead of assuming the energy cancellation `⟪B u u, u⟫ = 0` as a hypothesis,
we define a concrete bilinear map

  (B₃ u v)₀ =  u₁v₂ + u₂v₁
  (B₃ u v)₁ = -(u₀v₂ + u₂v₀)
  (B₃ u v)₂ =  0

(the three-mode Euler/Eady-style truncation) and *prove* the cancellation
`⟪B₃ u u, u⟫ = 0` by explicit finite computation (`fin_cases` + `ring`), and
prove continuity with the explicit bound `‖B₃ u v‖ ≤ 4‖u‖‖v‖`.

This yields `explicitData3 : GalerkinNS (ModeSpace 1)` with no hypotheses left
unproven, and hence fully explicit existence/energy/uniqueness corollaries.
-/
import NsGalerkin.Concrete

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

/-- The explicit three-mode bilinear form on `ModeSpace 1` (coordinate view). -/
def B3fun (u v : ModeSpace 1) : ModeSpace 1 :=
  ![u 1 * v 2 + u 2 * v 1, -(u 0 * v 2 + u 2 * v 0), 0]

/-- `B3fun` as a bilinear map. -/
def B3lin : ModeSpace 1 →ₗ[ℝ] ModeSpace 1 →ₗ[ℝ] ModeSpace 1 :=
  LinearMap.mk₂ ℝ B3fun
    (fun u₁ u₂ v => by
      funext i
      fin_cases i <;>
        simp [B3fun, PiLp.add_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
          Matrix.cons_val_two, Matrix.head_cons, Pi.add_apply] <;> ring)
    (fun c u v => by
      funext i
      fin_cases i <;>
        simp [B3fun, PiLp.smul_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
          Matrix.cons_val_two, Matrix.head_cons, smul_eq_mul] <;> ring)
    (fun u v₁ v₂ => by
      funext i
      fin_cases i <;>
        simp [B3fun, PiLp.add_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
          Matrix.cons_val_two, Matrix.head_cons, Pi.add_apply] <;> ring)
    (fun c u v => by
      funext i
      fin_cases i <;>
        simp [B3fun, PiLp.smul_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
          Matrix.cons_val_two, Matrix.head_cons, smul_eq_mul] <;> ring)

/-- Every coordinate of a Euclidean vector is bounded by its norm. -/
theorem abs_coord_le_norm (w : ModeSpace 1) (i : Fin 3) : |w i| ≤ ‖w‖ := by
  have h := Finset.single_le_sum (f := fun j : Fin 3 => ‖w j‖ ^ 2)
    (fun j _ => sq_nonneg _) (Finset.mem_univ i)
  rw [← PiLp.norm_sq_eq_of_L2] at h
  have h2 := abs_le_of_sq_le_sq h (norm_nonneg w)
  rwa [abs_of_nonneg (norm_nonneg _), Real.norm_eq_abs] at h2

/-- The explicit three-mode continuous bilinear nonlinearity `B₃`,
with bound `‖B₃ u v‖ ≤ 4‖u‖‖v‖`. -/
def B3 : ModeSpace 1 →L[ℝ] ModeSpace 1 →L[ℝ] ModeSpace 1 :=
  LinearMap.mkContinuous₂ B3lin 4 (fun u v => by
    have h0 : |B3fun u v 0| ≤ 2 * (‖u‖ * ‖v‖) := by
      have e : B3fun u v 0 = u 1 * v 2 + u 2 * v 1 := by
        simp [B3fun, Matrix.cons_val_zero]
      rw [e]
      calc |u 1 * v 2 + u 2 * v 1| ≤ |u 1 * v 2| + |u 2 * v 1| := abs_add _ _
        _ = |u 1| * |v 2| + |u 2| * |v 1| := by rw [abs_mul, abs_mul]
        _ ≤ ‖u‖ * ‖v‖ + ‖u‖ * ‖v‖ := by
            gcongr <;> exact abs_coord_le_norm _ _
        _ = 2 * (‖u‖ * ‖v‖) := by ring
    have h1 : |B3fun u v 1| ≤ 2 * (‖u‖ * ‖v‖) := by
      have e : B3fun u v 1 = -(u 0 * v 2 + u 2 * v 0) := by
        simp [B3fun, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_zero]
      rw [e, abs_neg]
      calc |u 0 * v 2 + u 2 * v 0| ≤ |u 0 * v 2| + |u 2 * v 0| := abs_add _ _
        _ = |u 0| * |v 2| + |u 2| * |v 0| := by rw [abs_mul, abs_mul]
        _ ≤ ‖u‖ * ‖v‖ + ‖u‖ * ‖v‖ := by
            gcongr <;> exact abs_coord_le_norm _ _
        _ = 2 * (‖u‖ * ‖v‖) := by ring
    have h2 : |B3fun u v 2| ≤ 2 * (‖u‖ * ‖v‖) := by
      have e : B3fun u v 2 = 0 := by
        simp [B3fun, Matrix.cons_val_two, Matrix.head_cons, Matrix.cons_val_one,
          Matrix.cons_val_zero]
      rw [e, abs_zero]
      positivity
    have hcoord : ∀ i : Fin 3, ‖B3fun u v i‖ ^ 2 ≤ (2 * (‖u‖ * ‖v‖)) ^ 2 := by
      intro i
      have hb : |B3fun u v i| ≤ 2 * (‖u‖ * ‖v‖) := by
        fin_cases i
        · simpa using h0
        · simpa using h1
        · simpa using h2
      have hnn : (0:ℝ) ≤ 2 * (‖u‖ * ‖v‖) := by positivity
      have hb2 : |(|B3fun u v i|)| ≤ |2 * (‖u‖ * ‖v‖)| := by
        rwa [abs_abs, abs_of_nonneg hnn]
      rw [Real.norm_eq_abs]
      exact sq_le_sq.mpr hb2
    have hsq : ‖B3fun u v‖ ^ 2 ≤ (4 * ‖u‖ * ‖v‖) ^ 2 := by
      rw [PiLp.norm_sq_eq_of_L2]
      calc ∑ i : Fin 3, ‖B3fun u v i‖ ^ 2
          ≤ ∑ _i : Fin 3, (2 * (‖u‖ * ‖v‖)) ^ 2 :=
            Finset.sum_le_sum fun i _ => hcoord i
        _ = 3 * (2 * (‖u‖ * ‖v‖)) ^ 2 := by
            rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
            ring
        _ ≤ (4 * ‖u‖ * ‖v‖) ^ 2 := by
            nlinarith [mul_nonneg (norm_nonneg u) (norm_nonneg v)]
    have hfin := abs_le_of_sq_le_sq hsq (by positivity : (0:ℝ) ≤ 4 * ‖u‖ * ‖v‖)
    rwa [abs_of_nonneg (norm_nonneg _)] at hfin)

/-- Applying the continuous `B₃` is applying `B3fun`. -/
theorem B3_apply (u v : ModeSpace 1) : B3 u v = B3fun u v := rfl

/-- **Machine-checked energy cancellation for the explicit three-mode `B₃`**:
`⟪B₃ u u, u⟫ = 0` by explicit finite computation over the three coordinates.
This is the "abstract → explicit" seam: the hypothesis `hB` of `GalerkinNS`
is a theorem here, not an assumption. -/
theorem B3_inner_self (u : ModeSpace 1) : ⟪B3 u u, u⟫_ℝ = 0 := by
  rw [PiLp.inner_apply]
  simp_rw [RCLike.inner_apply, conj_trivial, B3_apply]
  simp only [Fin.sum_univ_succ, Fin.sum_univ_one, Finset.univ_eq_empty, Finset.sum_empty,
    Fin.succ_zero_eq_one', Fin.succ_one_eq_two', add_zero,
    B3fun, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
    Matrix.cons_val_two, Matrix.tail_cons]
  rw [Fin.succ_zero_eq_one', Fin.succ_zero_eq_one', Fin.succ_one_eq_two']
  ring

/-- Explicit Galerkin NS data on `ModeSpace 1`: viscosity 1, `A = id`,
the explicit three-mode nonlinearity `B₃`, forcing `f`. Every hypothesis of
`GalerkinNS` is discharged by a proof — nothing is assumed. -/
def explicitData3 (f : ModeSpace 1) : GalerkinNS (ModeSpace 1) where
  ν := 1
  hν := one_pos
  A := .id ℝ _
  hA := fun x => by
    rw [ContinuousLinearMap.id_apply]
    exact (real_inner_self_eq_norm_sq x).symm.le
  B := B3
  hB := B3_inner_self
  f := f

/-- Global existence for the explicit three-mode truncation. -/
theorem explicit3_exists_solution_upto (f x₀ : ModeSpace 1) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → ModeSpace 1, x 0 = x₀ ∧
      ∀ t ∈ Icc 0 T, HasDerivWithinAt x ((explicitData3 f).vf (x t)) (Icc 0 T) t :=
  (explicitData3 f).exists_solution_upto x₀ hT

/-- Existence and uniqueness for the explicit three-mode truncation. -/
theorem explicit3_exists_unique_solution_upto (f x₀ : ModeSpace 1) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → ModeSpace 1, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 T, HasDerivWithinAt x ((explicitData3 f).vf (x t)) (Icc 0 T) t) ∧
      ∀ y : ℝ → ModeSpace 1, y 0 = x₀ →
        (∀ t ∈ Icc 0 T, HasDerivWithinAt y ((explicitData3 f).vf (y t)) (Icc 0 T) t) →
          ∀ t ∈ Icc 0 T, y t = x t :=
  (explicitData3 f).exists_unique_solution_upto x₀ hT

/-- Energy bound for the explicit three-mode truncation. -/
theorem explicit3_energy_bound (f x₀ : ModeSpace 1) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → ModeSpace 1, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 T, HasDerivWithinAt x ((explicitData3 f).vf (x t)) (Icc 0 T) t) ∧
      ∀ t ∈ Icc 0 T, ‖x t‖ ^ 2 ≤ max (‖x₀‖ ^ 2) (‖f‖ ^ 2 / (1 : ℝ) ^ 2) := by
  obtain ⟨x, hx0, hx⟩ := explicit3_exists_solution_upto f x₀ hT
  refine ⟨x, hx0, hx, fun t ht => ?_⟩
  have hB := (explicitData3 f).norm_sq_le_of_solution hT hx t ht
  rw [hx0] at hB
  exact hB

-- Axiom audit (printed at build time).
#print axioms B3_inner_self
#print axioms explicit3_exists_unique_solution_upto
#print axioms explicit3_energy_bound

end NSGalerkin
