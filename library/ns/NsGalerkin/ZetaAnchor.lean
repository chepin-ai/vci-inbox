-- CLASSIFY: L1
/-
WS-64 · ZetaAnchor — Prop-level honest anchor for external interval certificates
of ζ-zero isolation on the critical line. Discipline identical to
NsGalerkin/CapAnchor.lean: Prop-valued defs only, no proof asserted; kernel-layer
proof is BLOCKED(B1). Names verified against mathlib4 tag v4.10.0 (commit a719ba5).

Deviation disclosure from the WS-64 draft: none (draft compiled verbatim).
-/
import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.Dirichlet

open Set Complex
open scoped Topology

noncomputable section

namespace ZetaAnchor

/-- Critical-line parametrization `t ↦ 1/2 + I·t`. -/
def critLine (t : ℝ) : ℂ := 1 / 2 + I * (t : ℂ)

/-- ANCHOR A: on `t ∈ Icc 0 T`, every zero of `ζ(1/2 + I·t)` is at a registered
witness point `w i`. Statement-level only. -/
def zetaIsolationAnchor (T : ℝ) {n : ℕ} (w : Fin n → ℝ) : Prop :=
  ∀ t ∈ Icc (0 : ℝ) T, riemannZeta (critLine t) = 0 → ∃ i : Fin n, t = w i

/-- ANCHOR B (box ∃! form, mirrors capAnchorStatement): in `Icc a b` on the
critical line there is a unique zero, lying in `Icc lo hi`. -/
def zetaUniqueZeroAnchor (a b lo hi : ℝ) : Prop :=
  ∃! t : ℝ, t ∈ Icc a b ∧ riemannZeta (critLine t) = 0 ∧ t ∈ Icc lo hi

/-- Weld to mathlib's own Prop precedent `RiemannHypothesis` (RiemannZeta.lean:157):
the critical-line half of RH at global scale. No proof asserted. -/
def zetaAnchorImpliesRHCriticalLine : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → (0 : ℝ) ≤ s.re → s.re ≤ 1 →
    ¬∃ n : ℕ, s = -2 * (n + 1) → s ≠ 1 → s.re = 1 / 2

end ZetaAnchor
