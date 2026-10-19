-- CLASSIFY: L1
/-
M1-1 / L1-1 · Skew-symmetry packaging upgrade
(EXT-WAVE-15「构」 · WS-44 部件 L1-1 · EXT18 放行件 · 候选件, spike 验证后转正)

The physical Galerkin nonlinearity is skew in the last two arguments,
`⟪B u v, w⟫ = -⟪B u w, v⟫` (integration by parts against a divergence-free
basis). The WS-42 kernel (`GalerkinNS.hB`) carries only the full diagonal
`⟪B u u, u⟫ = 0`, which is strictly weaker: polarization of the cubic
diagonal kills only the full symmetrization, not the (2,3)-skew part needed
at the PDE seam (cf. FluidGalerkinLean's `⟨B(u,v),w⟩ = -⟨B(u,w),v⟩`).

This module is purely additive: it introduces the strengthened diagonal
hypothesis `hskew : ∀ u v, ⟪B u v, v⟫ = 0` and proves
  (1) it implies the WS-42 diagonal `hB`;
  (2) it polarization-yields full (2,3)-skew-symmetry.
No existing file is modified; downstream zero regression by construction.
Migration of the `GalerkinNS` structure field itself is a separate
follow-up card (requires re-proving Concrete instances; not in this spike).

Toolchain target: leanprover/lean4:v4.35.0 + mathlib v4.35.0 (spike).
-/
import NsGalerkin.Basic
open scoped InnerProductSpace

open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The strengthened (physical) skew-diagonal hypothesis implies the
WS-42 full-diagonal cancellation `⟪B u u, u⟫ = 0`. -/
theorem hB_of_hskew (B : E →L[ℝ] E →L[ℝ] E)
    (hskew : ∀ u v : E, ⟪B u v, v⟫_ℝ = 0) (u : E) :
    ⟪B u u, u⟫_ℝ = 0 :=
  hskew u u

/-- **Polarization lemma**: from the strengthened diagonal cancellation
`⟪B u v, v⟫ = 0` (for all `u v`), recover the full skew-symmetry in the
last two arguments, `⟪B u v, w⟫ = -⟪B u w, v⟫`.

Proof: expand `⟪B u (v + w), v + w⟫ = 0` by bilinearity; the diagonal terms
vanish by hypothesis, leaving the two cross terms summing to zero. -/
theorem inner_B_antisymm (B : E →L[ℝ] E →L[ℝ] E)
    (hskew : ∀ u v : E, ⟪B u v, v⟫_ℝ = 0) (u v w : E) :
    ⟪B u v, w⟫_ℝ = -⟪B u w, v⟫_ℝ := by
  have hvw := hskew u (v + w)
  have hv : ⟪B u v, v⟫_ℝ = 0 := hskew u v
  have hw : ⟪B u w, w⟫_ℝ = 0 := hskew u w
  simp only [map_add, inner_add_left, inner_add_right, hv, hw] at hvw
  linarith [hvw]

/-- Packaging note: any `GalerkinNS` instance whose nonlinearity satisfies
the physical skew-diagonal form can be re-anchored at the seam with the
full skew law. This records the intended usage as a typed constructor. -/
structure SkewNonlinearity (E : Type*) [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] where
  B : E →L[ℝ] E →L[ℝ] E
  hskew : ∀ u v : E, ⟪B u v, v⟫_ℝ = 0

namespace SkewNonlinearity

variable (S : SkewNonlinearity E)

/-- Full skew-symmetry of a `SkewNonlinearity`, via polarization. -/
theorem antisymm (u v w : E) : ⟪S.B u v, w⟫_ℝ = -⟪S.B u w, v⟫_ℝ :=
  inner_B_antisymm S.B S.hskew u v w

/-- The skew form specializes to the WS-42 diagonal cancellation. -/
theorem diag (u : E) : ⟪S.B u u, u⟫_ℝ = 0 :=
  hB_of_hskew S.B S.hskew u

end SkewNonlinearity

end NSGalerkin

end
