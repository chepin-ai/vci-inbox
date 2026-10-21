-- CLASSIFY: L1
/-
M1-1 / L1-1 · Skew-symmetry packaging upgrade
(EXT-WAVE-15「构」 · WS-44 部件 L1-1 · EXT18 放行件 · 候选件, spike 验证后转正)

The physical Galerkin nonlinearity is skew in the last two arguments,
`⟪B u v, w⟫ = -⟪B u w, v⟫` (integration by parts against a divergence-free
basis). The kernel structure field (`GalerkinNS.hskew`, migrated from
`hB` in M1-4/L1-1, EXT-WAVE-18) carries only the diagonal cancellation
`⟪B u u, u⟫ = 0`, which is strictly weaker: polarization of the cubic
diagonal kills only the full symmetrization, not the (2,3)-skew part needed
at the PDE seam (cf. FluidGalerkinLean's `⟨B(u,v),w⟩ = -⟨B(u,w),v⟩`).

This module provides the seam-facing strengthened diagonal hypothesis
`hskew_full : ∀ u v, ⟪B u v, v⟫ = 0` and proves
  (1) it implies the kernel diagonal `GalerkinNS.hskew`;
  (2) it polarization-yields full (2,3)-skew-symmetry.
Downstream seam work (FGL port / 2D uniqueness) should consume the
strengthened interface where the physical skew law is available.

M1-4 status (code-fact decision, registered deviation): the strengthened
form is *not* satisfied by the machine-checked instances `skewB`
(`Concrete.lean`) and `B₃` (`ExplicitB.lean`) — e.g.
`⟪skewB a u v, v⟫ = ⟪a,u⟫⟪v,v⟫ - ⟪a,v⟫⟪u,v⟫ ≠ 0` in general — so the
`GalerkinNS` field `hskew` retains exactly the consumed diagonal content
`∀ u, ⟪B u u, u⟫ = 0`, and this module remains the opt-in strengthened
interface for instances that do enjoy the physical skew law.

Toolchain target: leanprover/lean4:v4.35.0 + mathlib v4.35.0.
-/
import NsGalerkin.Basic
open scoped InnerProductSpace

open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The strengthened (physical) skew-diagonal hypothesis implies the
kernel diagonal cancellation `GalerkinNS.hskew`, `⟪B u u, u⟫ = 0`. -/
theorem diag_of_hskew_full (B : E →L[ℝ] E →L[ℝ] E)
    (hskew_full : ∀ u v : E, ⟪B u v, v⟫_ℝ = 0) (u : E) :
    ⟪B u u, u⟫_ℝ = 0 :=
  hskew_full u u

/-- **Polarization lemma**: from the strengthened diagonal cancellation
`⟪B u v, v⟫ = 0` (for all `u v`), recover the full skew-symmetry in the
last two arguments, `⟪B u v, w⟫ = -⟪B u w, v⟫`.

Proof: expand `⟪B u (v + w), v + w⟫ = 0` by bilinearity; the diagonal terms
vanish by hypothesis, leaving the two cross terms summing to zero. -/
theorem inner_B_antisymm (B : E →L[ℝ] E →L[ℝ] E)
    (hskew_full : ∀ u v : E, ⟪B u v, v⟫_ℝ = 0) (u v w : E) :
    ⟪B u v, w⟫_ℝ = -⟪B u w, v⟫_ℝ := by
  have hvw := hskew_full u (v + w)
  have hv : ⟪B u v, v⟫_ℝ = 0 := hskew_full u v
  have hw : ⟪B u w, w⟫_ℝ = 0 := hskew_full u w
  simp only [map_add, inner_add_left, inner_add_right, hv, hw] at hvw
  linarith [hvw]

/-- Packaging note: any `GalerkinNS` instance whose nonlinearity satisfies
the physical skew-diagonal form can be re-anchored at the seam with the
full skew law. This records the intended usage as a typed constructor.
The field is named `hskew_full` to distinguish it from the kernel
diagonal field `GalerkinNS.hskew` (strictly weaker). -/
structure SkewNonlinearity (E : Type*) [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] where
  B : E →L[ℝ] E →L[ℝ] E
  hskew_full : ∀ u v : E, ⟪B u v, v⟫_ℝ = 0

namespace SkewNonlinearity

variable (S : SkewNonlinearity E)

/-- Full skew-symmetry of a `SkewNonlinearity`, via polarization. -/
theorem antisymm (u v w : E) : ⟪S.B u v, w⟫_ℝ = -⟪S.B u w, v⟫_ℝ :=
  inner_B_antisymm S.B S.hskew_full u v w

/-- The strengthened skew form specializes to the kernel diagonal
cancellation `GalerkinNS.hskew`. -/
theorem diag (u : E) : ⟪S.B u u, u⟫_ℝ = 0 :=
  diag_of_hskew_full S.B S.hskew_full u

/-- The trilinear form `b(u,v,w) = ⟪B u v, w⟫` of a `SkewNonlinearity`
satisfies full (2,3)-skew-symmetry `b(u,v,w) = -b(u,w,v)` — the abstract
form of the fluid identity consumed at the PDE seam (FGL-SEAM-SPEC-01
单元① 1.1「斜对称强于抵消」口径;本有限维 ODE 截断层的对齐件)。 -/
theorem trilinear_antisymm (u v w : E) :
    ⟪S.B u v, w⟫_ℝ = -⟪S.B u w, v⟫_ℝ :=
  S.antisymm u v w

end SkewNonlinearity

/-- **skew⇒cancel 桥的消费端**（WS-B 降级档 D-A，E9 逐项同构改写）：
由强化斜对称接口 `SkewNonlinearity` 直接组装 `GalerkinNS` 数据——
`hskew` 字段证据由桥定理 `SkewNonlinearity.diag` 供给。
同构对齐：与 `GalerkinNS.mk` 语义全等，非新证；
凡具物理斜对称律的实例（下游接缝）均可经此构造进入本有限维 ODE
截断层的既有存在/唯一/先验界机制。 -/
def GalerkinNS.ofSkewNonlinearity (ν : ℝ) (hν : 0 < ν) (A : E →L[ℝ] E)
    (hA : ∀ x : E, ‖x‖ ^ 2 ≤ ⟪A x, x⟫_ℝ) (S : SkewNonlinearity E) (f : E) :
    GalerkinNS E where
  ν := ν
  hν := hν
  A := A
  hA := hA
  B := S.B
  hskew := S.diag
  f := f

/-- 桥消费端的非线性项对齐：组装后的 `B` 即接口携带的 `S.B`（定义性相等）。 -/
theorem GalerkinNS.ofSkewNonlinearity_B (ν : ℝ) (hν : 0 < ν) (A : E →L[ℝ] E)
    (hA : ∀ x : E, ‖x‖ ^ 2 ≤ ⟪A x, x⟫_ℝ) (S : SkewNonlinearity E) (f : E) :
    (GalerkinNS.ofSkewNonlinearity ν hν A hA S f).B = S.B := rfl

-- D-A 桥件公理审计（构建期打印）。
#print axioms SkewNonlinearity.trilinear_antisymm
#print axioms GalerkinNS.ofSkewNonlinearity

end NSGalerkin

end
