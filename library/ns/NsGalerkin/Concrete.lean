-- CLASSIFY: L1
/-
WS-42 · Concrete instantiation of the abstract Galerkin layer.

`skewB a u v = ⟪a,u⟫ • v - ⟪a,v⟫ • u` is a genuine continuous bilinear map
satisfying the energy cancellation (indeed `skewB a u u = 0`), showing the
abstract `GalerkinNS` hypotheses are inhabited. `ModeSpace N` is the mode
space of the `N`-th order truncation. Carried over from WS-41; WS-42 adds the
instantiated uniqueness corollaries.
-/
import NsGalerkin.Uniqueness
open scoped InnerProductSpace

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

namespace GalerkinNS

/-- A concrete skew bilinear nonlinearity on any real inner product space:
`skewB a u v = ⟪a,u⟫ • v - ⟪a,v⟫ • u`. It satisfies `skewB a u u = 0`,
hence the Galerkin skew-cancellation field `hskew`. (This is the finite-model
analogue of `b(u,u,u) = 0`; the explicit Fourier-mode `B` is `NsGalerkin/ExplicitB.lean`.) -/
def skewB (a : E) : E →L[ℝ] E →L[ℝ] E :=
  LinearMap.mkContinuous₂
    (LinearMap.mk₂ ℝ (fun u v => ⟪a, u⟫_ℝ • v - ⟪a, v⟫_ℝ • u)
      (fun u₁ u₂ v => by
        show (⟪a, u₁ + u₂⟫_ℝ • v - ⟪a, v⟫_ℝ • (u₁ + u₂)) =
          (⟪a, u₁⟫_ℝ • v - ⟪a, v⟫_ℝ • u₁) + (⟪a, u₂⟫_ℝ • v - ⟪a, v⟫_ℝ • u₂)
        rw [inner_add_right, add_smul, smul_add]
        abel)
      (fun c u v => by
        show (⟪a, c • u⟫_ℝ • v - ⟪a, v⟫_ℝ • (c • u)) =
          c • (⟪a, u⟫_ℝ • v - ⟪a, v⟫_ℝ • u)
        have e1 : ⟪a, c • u⟫_ℝ • v = c • (⟪a, u⟫_ℝ • v) := by
          rw [real_inner_smul_right, mul_smul]
        have e2 : (⟪a, v⟫_ℝ : ℝ) • (c • u) = c • (⟪a, v⟫_ℝ • u) := smul_comm _ _ _
        rw [e1, e2, smul_sub])
      (fun u v₁ v₂ => by
        show (⟪a, u⟫_ℝ • (v₁ + v₂) - ⟪a, v₁ + v₂⟫_ℝ • u) =
          (⟪a, u⟫_ℝ • v₁ - ⟪a, v₁⟫_ℝ • u) + (⟪a, u⟫_ℝ • v₂ - ⟪a, v₂⟫_ℝ • u)
        rw [smul_add, inner_add_right, add_smul]
        abel)
      (fun c u v => by
        show (⟪a, u⟫_ℝ • (c • v) - ⟪a, c • v⟫_ℝ • u) =
          c • (⟪a, u⟫_ℝ • v - ⟪a, v⟫_ℝ • u)
        have e1 : (⟪a, u⟫_ℝ : ℝ) • (c • v) = c • (⟪a, u⟫_ℝ • v) := smul_comm _ _ _
        have e2 : ⟪a, c • v⟫_ℝ • u = c • (⟪a, v⟫_ℝ • u) := by
          rw [real_inner_smul_right, mul_smul]
        rw [e1, e2, smul_sub]))
    (2 * ‖a‖)
    (fun u v => by
      have h1 : ‖(⟪a, u⟫_ℝ : ℝ)‖ * ‖v‖ ≤ ‖a‖ * ‖u‖ * ‖v‖ := by
        rw [Real.norm_eq_abs]
        exact mul_le_mul_of_nonneg_right (abs_real_inner_le_norm _ _) (norm_nonneg _)
      have h2 : ‖(⟪a, v⟫_ℝ : ℝ)‖ * ‖u‖ ≤ ‖a‖ * ‖u‖ * ‖v‖ := by
        rw [Real.norm_eq_abs]
        calc |⟪a, v⟫_ℝ| * ‖u‖ ≤ (‖a‖ * ‖v‖) * ‖u‖ :=
              mul_le_mul_of_nonneg_right (abs_real_inner_le_norm _ _) (norm_nonneg _)
          _ = ‖a‖ * ‖u‖ * ‖v‖ := by ring
      calc ‖⟪a, u⟫_ℝ • v - ⟪a, v⟫_ℝ • u‖
          ≤ ‖⟪a, u⟫_ℝ • v‖ + ‖⟪a, v⟫_ℝ • u‖ := norm_sub_le _ _
        _ = ‖(⟪a, u⟫_ℝ : ℝ)‖ * ‖v‖ + ‖(⟪a, v⟫_ℝ : ℝ)‖ * ‖u‖ := by
            rw [norm_smul, norm_smul]
        _ ≤ ‖a‖ * ‖u‖ * ‖v‖ + ‖a‖ * ‖u‖ * ‖v‖ := add_le_add h1 h2
        _ = 2 * ‖a‖ * ‖u‖ * ‖v‖ := by ring)

/-- The cancellation identity for `skewB`: `skewB a u u = 0`. -/
theorem skewB_self (a u : E) : skewB a u u = 0 := by
  show (⟪a, u⟫_ℝ • u : E) - ⟪a, u⟫_ℝ • u = 0
  exact sub_self _

/-- Concrete Galerkin NS data on `E` with viscosity 1, Stokes operator `A = id`
(coercive with constant 1), nonlinearity `skewB a`, forcing `f`.
The `hskew` evidence (M1-4 re-proof): on the diagonal, `skewB a u u = 0`
(`skewB_self`), so `⟪skewB a u u, u⟫ = 0` by `inner_zero_left`. -/
def concreteData (a f : E) : GalerkinNS E where
  ν := 1
  hν := one_pos
  A := .id ℝ E
  hA := fun x => by
    rw [ContinuousLinearMap.id_apply]
    exact (real_inner_self_eq_norm_sq x).symm.le
  B := skewB a
  hskew := fun u => by rw [skewB_self]; exact inner_zero_left _
  f := f

end GalerkinNS

/-- The mode space of the `N`-th order Galerkin truncation: `2N+1` real
coefficients, standing in for the Fourier modes `|k| ≤ N` of a scalar field
on the 2-torus (vorticity formulation). Any `GalerkinNS (ModeSpace N)` data
on it is an `N`-th order Galerkin-truncated 2D Navier–Stokes ODE system. -/
abbrev ModeSpace (N : ℕ) := EuclideanSpace ℝ (Fin (2 * N + 1))

/-- The type of `N`-th order Galerkin-truncated 2D Navier–Stokes ODE systems. -/
abbrev galerkinNS (N : ℕ) := GalerkinNS (ModeSpace N)

/-- Global existence for the concrete `N`-th order truncation. -/
theorem galerkinNS_exists_solution_upto (N : ℕ) (a f x₀ : ModeSpace N) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → ModeSpace N, x 0 = x₀ ∧
      ∀ t ∈ Icc 0 T, HasDerivWithinAt x ((GalerkinNS.concreteData a f).vf (x t))
        (Icc 0 T) t :=
  (GalerkinNS.concreteData a f).exists_solution_upto x₀ hT

/-- The concrete truncation enjoys the uniform energy bound. -/
theorem galerkinNS_energy_bound (N : ℕ) (a f x₀ : ModeSpace N) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → ModeSpace N, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 T, HasDerivWithinAt x ((GalerkinNS.concreteData a f).vf (x t))
        (Icc 0 T) t) ∧
      ∀ t ∈ Icc 0 T, ‖x t‖ ^ 2 ≤ max (‖x₀‖ ^ 2) (‖f‖ ^ 2 / (1 : ℝ) ^ 2) := by
  obtain ⟨x, hx0, hx⟩ := galerkinNS_exists_solution_upto N a f x₀ hT
  refine ⟨x, hx0, hx, fun t ht => ?_⟩
  have hEn := (GalerkinNS.concreteData a f).norm_sq_le_of_solution hT hx t ht
  rw [hx0] at hEn
  exact hEn

/-- Global uniqueness for the concrete `N`-th order truncation (WS-42). -/
theorem galerkinNS_solution_unique (N : ℕ) (a f x₀ : ModeSpace N) {T : ℝ} (hT : 0 ≤ T)
    {x y : ℝ → ModeSpace N}
    (hx0 : x 0 = x₀)
    (hx : ∀ t ∈ Icc 0 T, HasDerivWithinAt x ((GalerkinNS.concreteData a f).vf (x t))
      (Icc 0 T) t)
    (hy0 : y 0 = x₀)
    (hy : ∀ t ∈ Icc 0 T, HasDerivWithinAt y ((GalerkinNS.concreteData a f).vf (y t))
      (Icc 0 T) t) :
    ∀ t ∈ Icc 0 T, x t = y t :=
  (GalerkinNS.concreteData a f).solution_unique_upto hT hx0 hx hy0 hy

/-- Existence and uniqueness, bundled, for the concrete `N`-th order truncation. -/
theorem galerkinNS_exists_unique_solution_upto (N : ℕ) (a f x₀ : ModeSpace N) {T : ℝ}
    (hT : 0 ≤ T) :
    ∃ x : ℝ → ModeSpace N, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 T, HasDerivWithinAt x ((GalerkinNS.concreteData a f).vf (x t))
        (Icc 0 T) t) ∧
      ∀ y : ℝ → ModeSpace N, y 0 = x₀ →
        (∀ t ∈ Icc 0 T, HasDerivWithinAt y ((GalerkinNS.concreteData a f).vf (y t))
          (Icc 0 T) t) →
          ∀ t ∈ Icc 0 T, y t = x t :=
  (GalerkinNS.concreteData a f).exists_unique_solution_upto x₀ hT

-- Axiom audit (printed at build time).
#print axioms GalerkinNS.exists_solution_upto
#print axioms GalerkinNS.norm_sq_le_of_solution
#print axioms GalerkinNS.solution_unique_upto
#print axioms GalerkinNS.exists_unique_solution_upto
#print axioms GalerkinNS.skewB_self
#print axioms galerkinNS_exists_solution_upto
#print axioms galerkinNS_energy_bound
#print axioms galerkinNS_solution_unique

end NSGalerkin
