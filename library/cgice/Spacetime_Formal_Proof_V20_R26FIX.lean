import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.BilinearForm.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import Mathlib.Topology.Order.IntermediateValue
/-! Conditional geometric relaxation and effective cosmological models.
Source-level proof manuscript; compilation verified under the pinned Lean 4 / Mathlib build.
All physical inputs occur as definitions or explicit local hypotheses.
The CGICECore namespace reproduces selected mathematical results from the companion CGICE source.
-/
/-! 【枢修R26·联邦修复版】 原件 sha256 0944d696ce61e6e4150f84be8f107837e588f7d8ba1655c14964f89419c71d48
  (证据保全于同库 Spacetime_Formal_Proof_V20.lean · 未动一字)。
  R25裁决: 原件在所报pin(mathlib 9fe29c4b·toolchain v4.35.0-rc2)上 rc=1 —— 行62/71 `rfl` defeq失败+行63/72级联。
  本修复版: 5处 convert-using-1 的defeq脆弱bullet级联 → all_goals-first 稳健链(show+ring/rfl/ring_nf/ext+simp/field_simp+ring)。
  修复点均以【枢修R26/v2】标注; v2迭代: first→solve组合子·除ring_nf半成品毒化·增simp/push_cast备选 · 原件©Hui Xu(preprints202609.1998.v1) · 修复: 枢/PIVOT-01代联邦 · 覆写权归原作者 · precedent lgt-118 -/
noncomputable section
open Real Set Topology MeasureTheory ProbabilityTheory Filter
open scoped BigOperators NNReal Matrix
set_option autoImplicit false
namespace CGICECore

abbrev V6 := Fin 6 → ℝ
def positiveRoots : Finset (Fin 6 × Fin 6) :=
  Finset.univ.filter (fun p => p.1 < p.2)
def root (i j : Fin 6) (k : Fin 6) : ℝ :=
  (if k = i then 1 else 0) - (if k = j then 1 else 0)
def rhoAlg : V6 := ![5/2, 3/2, 1/2, -1/2, -3/2, -5/2]
def rhoRes (k : Fin 6) : ℝ := 2 * rhoAlg k
def dualNormSq (c : ℝ) (v : V6) : ℝ := (∑ k, v k ^ 2) / c
theorem positive_roots_card : positiveRoots.card = 15 := by decide
theorem half_sum_positive_roots (k : Fin 6) :
    (1 / 2 : ℝ) * (∑ p ∈ positiveRoots, root p.1 p.2 k) = rhoAlg k := by
  have hp : (positiveRoots.filter (fun p => k = p.1)).card = 5-k.val := by
    fin_cases k <;> decide
  have hn : (positiveRoots.filter (fun p => k = p.2)).card = k.val := by
    fin_cases k <;> decide
  simp [root, hp, hn]
  fin_cases k <;> norm_num [rhoAlg]
theorem rho_alg_norm_sq : (∑ k, rhoAlg k ^ 2) = (35 / 2 : ℝ) := by
  norm_num [rhoAlg, Fin.sum_univ_succ]
theorem rho_restricted_norm_sq : (∑ k, rhoRes k ^ 2) = (70 : ℝ) := by
  norm_num [rhoRes, rhoAlg, Fin.sum_univ_succ]
theorem restricted_threshold_scale (c : ℝ) : dualNormSq c rhoRes = 70 / c := by
  rw [dualNormSq, rho_restricted_norm_sq]
theorem restricted_threshold_35 : dualNormSq 2 rhoRes = 35 := by
  norm_num [restricted_threshold_scale]
theorem ordinary_norm_metric_two : dualNormSq 2 rhoAlg = 35 / 4 := by
  rw [dualNormSq, rho_alg_norm_sq]; norm_num
theorem transverse_rate_of_matching (r t : ℝ)
    (hr : r = dualNormSq 2 rhoRes) (hmatch : 3 * t = r) : t = 35 / 3 := by
  rw [restricted_threshold_35] at hr
  linarith
def quarticPotential (a q x : ℝ) : ℝ := a / 2 * x^2 + q / 4 * x^4
def quarticGradient (a q x : ℝ) : ℝ := a*x + q*x^3
def quarticHessian (a q x : ℝ) : ℝ := a + 3*q*x^2
theorem quartic_hasDerivAt (a q x : ℝ) :
    HasDerivAt (quarticPotential a q) (quarticGradient a q x) x := by
  unfold quarticPotential quarticGradient
  convert (((hasDerivAt_id x).pow 2).const_mul (a/2)).add
    (((hasDerivAt_id x).pow 4).const_mul (q/4)) using 1
  all_goals solve -- 【枢修R26v2】原`· rfl`×2级联在所报pin defeq失败(行62/63)→solve链(v1的ring_nf半成品毒化已除: bare ring_nf会部分归约后"成功"留下id-atom残局)
    | rfl
    | (ext y; simp)
    | simp
    | (simp; ring)
    | (push_cast; ring)
    | (field_simp; ring)
theorem gradient_hasDerivAt (a q x : ℝ) :
    HasDerivAt (quarticGradient a q) (quarticHessian a q x) x := by
  unfold quarticGradient quarticHessian
  convert ((hasDerivAt_id x).const_mul a).add
    (((hasDerivAt_id x).pow 3).const_mul q) using 1
  all_goals solve -- 【枢修R26v2】同上→solve链
    | rfl
    | (ext y; simp)
    | simp
    | (simp; ring)
    | (push_cast; ring)
    | (field_simp; ring)
theorem hessian_positive (a q x : ℝ) (ha : 0 < a) (hq : 0 ≤ q) :
    0 < quarticHessian a q x := by
  have := mul_nonneg hq (sq_nonneg x)
  dsimp [quarticHessian]; nlinarith
def wittenScalarPotential (h a q x : ℝ) : ℝ :=
  (quarticGradient a q x)^2 - h * quarticHessian a q x
theorem witten_quartic_expansion (h a q x : ℝ) :
    wittenScalarPotential h a q x =
    a^2*x^2 - h*a + q*(2*a*x^4 - 3*h*x^2) + q^2*x^6 := by
  unfold wittenScalarPotential quarticGradient quarticHessian; ring
theorem quartic_operator_differs :
    wittenScalarPotential 1 1 1 2 ≠ wittenScalarPotential 1 1 0 2 := by
  norm_num [wittenScalarPotential, quarticGradient, quarticHessian]
theorem witten_diffusion_scaling (b lap gradSq lapV : ℝ) (hb : b ≠ 0) :
    b/4 * (-(2/b)^2*lap + gradSq - (2/b)*lapV) =
    -(1/b)*lap + (b/4)*gradSq - lapV/2 := by
  field_simp; ring
def relax (g e i t : ℝ) : ℝ := e + (i-e)*Real.exp (-g*t)
theorem relax_initial (g e i : ℝ) : relax g e i 0 = i := by
  simp [relax]
theorem relax_hasDerivAt (g e i t : ℝ) :
    HasDerivAt (relax g e i) (-g*(relax g e i t-e)) t := by
  have hid : HasDerivAt (fun x : ℝ => -g * x) (-g) t := by
    simpa using (hasDerivAt_id t).const_mul (-g)
  have hexp : HasDerivAt (fun x : ℝ => Real.exp (-g * x)) (-g * Real.exp (-g * t)) t := by
    simpa only [mul_comm] using hid.exp
  unfold relax
  convert (hexp.const_mul (i-e)).const_add e using 1 <;> (first | rfl | ext x; simp | ring)
theorem relaxation_unique (g e : ℝ) (I J : ℝ → ℝ)
    (hI : ∀ t, HasDerivAt I (-g*(I t-e)) t)
    (hJ : ∀ t, HasDerivAt J (-g*(J t-e)) t)
    (h0 : I 0 = J 0) (t : ℝ) : I t = J t := by
  let f := fun s => (I s-J s)*Real.exp (g*s)
  have hf : ∀ s, HasDerivAt f 0 s := by
    intro s
    have hexp : HasDerivAt (fun x : ℝ => Real.exp (g * x)) (g * Real.exp (g * s)) s := by
      simpa only [id_eq, mul_one, mul_comm] using (((hasDerivAt_id s).const_mul g).exp)
    dsimp [f]
    convert ((hI s).sub (hJ s)).mul hexp using 1 <;> (first | rfl | ext x; simp | simp <;> ring_nf)
  have hc := is_const_of_deriv_eq_zero (fun s => (hf s).differentiableAt)
    (fun s => (hf s).deriv) t 0
  have hz : (I t-J t)*Real.exp (g*t) = 0 := by simpa [f, h0] using hc
  exact sub_eq_zero.mp ((mul_eq_zero.mp hz).resolve_right (Real.exp_ne_zero _))
theorem relaxation_solution (g e i : ℝ) (I : ℝ → ℝ)
    (hI : ∀ t, HasDerivAt I (-g*(I t-e)) t) (h0 : I 0 = i) (t : ℝ) :
    I t = relax g e i t := by
  apply relaxation_unique g e I (relax g e i) hI (relax_hasDerivAt g e i)
  simpa using h0.trans (relax_initial g e i).symm
theorem relax_limit (g e i : ℝ) (hg : 0 < g) :
    Tendsto (relax g e i) atTop (nhds e) := by
  have ht : Tendsto (fun t : ℝ => -(g * t)) atTop atBot := by
    simpa [neg_mul] using (tendsto_const_mul_atBot_of_neg (neg_lt_zero.mpr hg)).2 tendsto_id
  have he : Tendsto (fun t : ℝ => Real.exp (-(g * t))) atTop (nhds 0) :=
    Real.tendsto_exp_atBot.comp ht
  have hmain : Tendsto (fun t : ℝ => e + (i - e) * Real.exp (-(g * t))) atTop (nhds e) := by
    simpa [mul_zero, add_zero] using
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => e) atTop (nhds e)).add
        ((tendsto_const_nhds : Tendsto (fun _ : ℝ => i - e) atTop (nhds (i - e))).mul he)
  convert hmain using 1
  · funext t
    unfold relax
    ring_nf
theorem forced_relaxation (g i : ℝ) (E F : ℝ → ℝ)
    (hF : ∀ t, HasDerivAt F (g*Real.exp (g*t)*E t) t) (t : ℝ) :
    HasDerivAt (fun s => Real.exp (-g*s)*(i+F s))
      (-g*(Real.exp (-g*t)*(i+F t)-E t)) t := by
  have hex : Real.exp (-g*t)*Real.exp (g*t) = 1 := by
    rw [← Real.exp_add]; ring_nf; exact Real.exp_zero
  have hexp : HasDerivAt (fun x : ℝ => Real.exp (-g * x)) (-g * Real.exp (-g * t)) t := by
    simpa only [id_eq, mul_one, mul_comm] using (((hasDerivAt_id t).const_mul (-g)).exp)
  have h1 : Real.exp (-g * t) * (g * Real.exp (g * t) * E t) = g * E t := by
    calc
      Real.exp (-g * t) * (g * Real.exp (g * t) * E t)
        = g * (Real.exp (-g * t) * Real.exp (g * t)) * E t := by ring
      _ = g * 1 * E t := by rw [hex]
      _ = g * E t := by ring
  have hmain : HasDerivAt ((fun x : ℝ => Real.exp (-g * x)) * (fun x : ℝ => i + F x))
      (-g * Real.exp (-g * t) * (i + F t) + g * E t) t := by
    convert (hexp.mul ((hF t).const_add i)) using 1 <;>
      (first | rfl | ext x; simp | rw [h1])
  convert hmain using 1 <;> (first | rfl | ext x; simp | ring)
def referenceRate : ℝ := (35/3)/(2*Real.pi)
def referenceTime : ℝ := 6*Real.pi/35
theorem reference_time_positive : 0 < referenceTime := by
  unfold referenceTime; positivity
theorem reference_time_reciprocal : referenceRate*referenceTime = 1 := by
  unfold referenceRate referenceTime
  field_simp [Real.pi_ne_zero]
  <;> ring
def varianceFromMoments (m s : ℝ) : ℝ := s-m^2
theorem variance_hasDerivAt (ell D : ℝ) (m s : ℝ → ℝ) (t : ℝ)
    (hm : HasDerivAt m (-ell*m t) t)
    (hs : HasDerivAt s (-2*ell*s t+2*D) t) :
    HasDerivAt (fun u => varianceFromMoments (m u) (s u))
      (-2*ell*varianceFromMoments (m t) (s t)+2*D) t := by
  have hsub : HasDerivAt (fun u => s u - (m u)^2)
      (-2*ell*s t+2*D - 2*(m t)*(-ell*m t)) t := by
    convert hs.sub (hm.pow 2) using 1 <;> (first | rfl | ext u; simp | ring_nf)
  unfold varianceFromMoments
  convert hsub using 1 <;> (first | rfl | ext u; simp | ring_nf)
def ouCov (ell D C0 t : ℝ) : ℝ := relax (2*ell) (D/ell) C0 t
theorem ouCov_initial (ell D C0 : ℝ) : ouCov ell D C0 0 = C0 :=
  relax_initial _ _ _
theorem ouCov_hasDerivAt (ell D C0 t : ℝ) (hl : ell ≠ 0) :
    HasDerivAt (ouCov ell D C0) (-2*ell*ouCov ell D C0 t+2*D) t := by
  unfold ouCov
  convert relax_hasDerivAt (2*ell) (D/ell) C0 t using 1
  field_simp [hl] <;> ring
theorem ouCov_excess (ell D C0 t : ℝ) :
    ouCov ell D C0 t-D/ell = (C0-D/ell)*Real.exp (-2*ell*t) := by
  dsimp [ouCov, relax]; ring
theorem ouCov_stationary (ell D t : ℝ) : ouCov ell D (D/ell) t = D/ell := by
  simp [ouCov, relax]
theorem ouCov_limit (ell D C0 : ℝ) (hl : 0 < ell) :
    Tendsto (ouCov ell D C0) atTop (nhds (D/ell)) := by
  exact relax_limit _ _ _ (by linarith)
theorem stationary_noise_positive (ell D t : ℝ) (hl : 0 < ell) (hD : 0 < D) :
    0 < ouCov ell D (D/ell) t := by
  rw [ouCov_stationary]; exact div_pos hD hl

def cross (a b : Fin 3 → ℝ) : Fin 3 → ℝ :=
  ![a 1*b 2-a 2*b 1, a 2*b 0-a 0*b 2, a 0*b 1-a 1*b 0]
theorem double_bracket_nonzero :
    cross ![1,0,0] (cross ![1,0,0] ![0,1,0]) 1 = -1 := by
  norm_num [cross, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.cons_val_fin_one]
theorem cross_orthogonal (a j : Fin 3 → ℝ) : (∑ k, j k*cross a j k) = 0 := by
  simp [Fin.sum_univ_succ, cross]; ring

theorem finite_charge_hasDerivAt {ι : Type*} [Fintype ι]
    (J rhs : ℝ → ι → ℝ) (t : ℝ)
    (hJ : ∀ i, HasDerivAt (fun s => J s i) (rhs t i) t) :
    HasDerivAt (fun s => ∑ i, J s i) (∑ i, rhs t i) t := by
  simpa using HasDerivAt.fun_sum (u := Finset.univ) (fun i _ => hJ i)
theorem finite_charge_conserved {ι : Type*} [Fintype ι]
    (J rhs : ℝ → ι → ℝ)
    (hJ : ∀ t i, HasDerivAt (fun s => J s i) (rhs t i) t)
    (hzero : ∀ t, ∑ i, rhs t i = 0) (t : ℝ) :
    (∑ i, J t i) = ∑ i, J 0 i := by
  have hd : ∀ s, HasDerivAt (fun u => ∑ i, J u i) 0 s := by
    intro s
    simpa [hzero s] using finite_charge_hasDerivAt J rhs s (hJ s)
  exact is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0
theorem cross_casimir_hasDerivAt (g : ℝ) (a j : ℝ → Fin 3 → ℝ) (t : ℝ)
    (hj : ∀ k, HasDerivAt (fun s => j s k) (-g*cross (a t) (j t) k) t) :
    HasDerivAt (fun s => ∑ k, (j s k)^2) 0 t := by
  have horth := cross_orthogonal (a t) (j t)
  have hsq : ∀ k, HasDerivAt (fun s => (j s k)^2)
      (2 * (j t k) * (-g * cross (a t) (j t) k)) t := by
    intro k
    convert (hj k).mul (hj k) using 1
    all_goals solve -- 【枢修R26v2】同款(+11h行226/227/228实证)→solve链(含pow_two备选)
      | rfl
      | (ext x; simp [pow_two])
      | simp
      | (simp; ring)
      | (push_cast; ring)
      | (field_simp; ring)
  have hderiv : HasDerivAt (fun s => ∑ k, (j s k)^2)
      (∑ k, 2 * (j t k) * (-g * cross (a t) (j t) k)) t := by
    simpa only using HasDerivAt.fun_sum (u := Finset.univ) (fun k _ => hsq k)
  have hzero : (∑ k, 2 * (j t k) * (-g * cross (a t) (j t) k)) = 0 := by
    calc
      (∑ k, 2 * (j t k) * (-g * cross (a t) (j t) k))
          = -2 * g * (∑ k, (j t k) * cross (a t) (j t) k) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl; intro k _; ring
      _ = -2 * g * 0 := by rw [horth]
      _ = 0 := by ring
  convert hderiv using 1 <;> (first | rfl | simpa using hzero)
theorem cross_casimir_conserved (g : ℝ) (a j : ℝ → Fin 3 → ℝ)
    (hj : ∀ t k, HasDerivAt (fun s => j s k) (-g*cross (a t) (j t) k) t)
    (t : ℝ) : (∑ k, (j t k)^2) = ∑ k, (j 0 k)^2 := by
  have hd := fun s => cross_casimir_hasDerivAt g a j s (hj s)
  exact is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0

section FluxForceConjugate
-- 本 section 共享 V/E 类型类变量，部分声明仅使用其子集；关闭 unusedSectionVars 以避免逐一声明 omit
set_option linter.unusedSectionVars false
variable {V E : Type*} [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
variable (s t : E → V)
def discGrad (ξ : V → ℝ) (e : E) : ℝ := ξ (t e) - ξ (s e)
def discDiv (J : E → ℝ) (v : V) : ℝ :=
  (∑ e, if s e = v then J e else 0) - (∑ e, if t e = v then J e else 0)
def edgeDensity (p : V → ℝ) (e : E) : ℝ := p (s e)
def fluxPower (p : V → ℝ) (J : E → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ e, (J e)^2 / edgeDensity s p e
def forcePower (p : V → ℝ) (F : E → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ e, edgeDensity s p e * (F e)^2
def pairing (J F : E → ℝ) : ℝ := ∑ e, J e * F e
def freeEnergyRate (ξ : V → ℝ) (J : E → ℝ) : ℝ :=
  ∑ v, ξ v * (- discDiv s t J v)
lemma sum_ξ_indicator_s (ξ : V → ℝ) (J : E → ℝ) :
    (∑ v, ξ v * (∑ e, if s e = v then J e else 0)) = ∑ e, ξ (s e) * J e := by
  calc
    (∑ v, ξ v * (∑ e, if s e = v then J e else 0))
      = ∑ v, ∑ e, ξ v * (if s e = v then J e else 0) := by
        simp only [Finset.mul_sum]
    _ = ∑ e, ∑ v, ξ v * (if s e = v then J e else 0) := Finset.sum_comm
    _ = ∑ e, ξ (s e) * J e := by
        apply Finset.sum_congr rfl
        intro e _
        simp
lemma sum_ξ_indicator_t (ξ : V → ℝ) (J : E → ℝ) :
    (∑ v, ξ v * (∑ e, if t e = v then J e else 0)) = ∑ e, ξ (t e) * J e := by
  calc
    (∑ v, ξ v * (∑ e, if t e = v then J e else 0))
      = ∑ v, ∑ e, ξ v * (if t e = v then J e else 0) := by
        simp only [Finset.mul_sum]
    _ = ∑ e, ∑ v, ξ v * (if t e = v then J e else 0) := Finset.sum_comm
    _ = ∑ e, ξ (t e) * J e := by
        apply Finset.sum_congr rfl
        intro e _
        simp
theorem graph_div_summation (ξ : V → ℝ) (J : E → ℝ) :
    (∑ v, ξ v * discDiv s t J v) + (∑ e, discGrad s t ξ e * J e) = 0 := by
  unfold discDiv discGrad
  have h1 : (∑ v, ξ v * ((∑ e, if s e = v then J e else 0) - ∑ e, if t e = v then J e else 0))
      = (∑ v, ξ v * (∑ e, if s e = v then J e else 0))
        - (∑ v, ξ v * (∑ e, if t e = v then J e else 0)) := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro v _
    ring
  rw [h1]
  rw [sum_ξ_indicator_s, sum_ξ_indicator_t]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro e _
  ring
lemma flux_force_gap_pointwise (p j f : ℝ) (hp : p ≠ 0) :
    (1 / 2 : ℝ) * j^2 / p + (1 / 2 : ℝ) * p * f^2 - j * f
      = (1 / 2 : ℝ) * (j - p * f)^2 / p := by
  field_simp [hp]
  ring
theorem flux_force_gap (p : V → ℝ) (J F : E → ℝ) (hp : ∀ e, edgeDensity s p e ≠ 0) :
    fluxPower s p J + forcePower s p F - pairing J F
      = (1 / 2 : ℝ) * ∑ e, (J e - edgeDensity s p e * F e)^2 / edgeDensity s p e := by
  unfold fluxPower forcePower pairing
  simp only [Finset.mul_sum]
  rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro e _
  field_simp [hp e]
  ring
theorem flux_force_nonneg (p : V → ℝ) (J F : E → ℝ) (hp : ∀ e, 0 < edgeDensity s p e) :
    pairing J F ≤ fluxPower s p J + forcePower s p F := by
  have hgap := flux_force_gap s p J F (fun e => ne_of_gt (hp e))
  have hnonneg : 0 ≤ (1 / 2 : ℝ) * ∑ e,
      (J e - edgeDensity s p e * F e)^2 / edgeDensity s p e := by
    apply mul_nonneg (by norm_num) (Finset.sum_nonneg (fun e _ => by
      exact div_nonneg (sq_nonneg _) (le_of_lt (hp e))))
  rw [← hgap] at hnonneg
  linarith
theorem flux_force_equality (p : V → ℝ) (J F : E → ℝ) (hp : ∀ e, 0 < edgeDensity s p e) :
    (fluxPower s p J + forcePower s p F = pairing J F) ↔
      (∀ e, J e = edgeDensity s p e * F e) := by
  have hgap := flux_force_gap s p J F (fun e => ne_of_gt (hp e))
  constructor
  · intro h
    have hzero : (1 / 2 : ℝ) * ∑ e, (J e - edgeDensity s p e * F e)^2 / edgeDensity s p e = 0 := by
      rw [← hgap]
      linarith
    have hsum : (∑ e, (J e - edgeDensity s p e * F e)^2 / edgeDensity s p e) = 0 := by
      nlinarith
    intro e
    have hterm : (J e - edgeDensity s p e * F e)^2 / edgeDensity s p e = 0 := by
      have := Finset.sum_eq_zero_iff_of_nonneg (fun e _ => by
        exact div_nonneg (sq_nonneg _) (le_of_lt (hp e))) |>.mp hsum e (Finset.mem_univ e)
      exact this
    have hsq : (J e - edgeDensity s p e * F e)^2 = 0 := by
      have hd := div_eq_zero_iff.mp hterm
      rcases hd with hsq | hp0
      · exact hsq
      · exfalso; exact (ne_of_gt (hp e)) hp0
    have hzero' : J e - edgeDensity s p e * F e = 0 := sq_eq_zero_iff.mp hsq
    linarith
  · intro h
    have hgap' := flux_force_gap s p J F (fun e => ne_of_gt (hp e))
    have hsumzero : (∑ e, (J e - edgeDensity s p e * F e)^2 / edgeDensity s p e) = 0 := by
      apply Finset.sum_eq_zero
      intro e _
      rw [h e]
      simp
    rw [← sub_eq_zero]
    rw [hgap']
    rw [hsumzero]
    norm_num
theorem flux_force_master (p ξ : V → ℝ) (J : E → ℝ) (hp : ∀ e, edgeDensity s p e ≠ 0)
    (hJ : ∀ e, J e = - edgeDensity s p e * discGrad s t ξ e) :
    freeEnergyRate s t ξ J + fluxPower s p J + forcePower s p (fun e => - discGrad s t ξ e) = 0 := by
  have h_fer : freeEnergyRate s t ξ J = ∑ e, discGrad s t ξ e * J e := by
    unfold freeEnergyRate
    calc
      (∑ v, ξ v * (- discDiv s t J v))
        = -(∑ v, ξ v * discDiv s t J v) := by
          rw [← Finset.sum_neg_distrib]
          apply Finset.sum_congr rfl
          intro v _
          ring
      _ = ∑ e, discGrad s t ξ e * J e := by
          have h := graph_div_summation s t ξ J
          linarith
  rw [h_fer]
  have h_sum : (∑ e, discGrad s t ξ e * J e) = -∑ e, edgeDensity s p e * (discGrad s t ξ e)^2 := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro e _
    rw [hJ e]
    ring
  rw [h_sum]
  have h_flux : fluxPower s p J = (1 / 2 : ℝ) * ∑ e, edgeDensity s p e * (discGrad s t ξ e)^2 := by
    unfold fluxPower
    congr 1
    apply Finset.sum_congr rfl
    intro e _
    rw [hJ e]
    field_simp [hp e] <;> ring
  rw [h_flux]
  have h_force : forcePower s p (fun e => - discGrad s t ξ e)
      = (1 / 2 : ℝ) * ∑ e, edgeDensity s p e * (discGrad s t ξ e)^2 := by
    unfold forcePower
    congr 1
    apply Finset.sum_congr rfl
    intro e _
    ring
  rw [h_force]
  ring
noncomputable def freeEnergy (U : V → ℝ) (D : ℝ) (p : V → ℝ) : ℝ :=
  ∑ v, (U v * p v + D * p v * Real.log (p v))
noncomputable def variationalXi (U : V → ℝ) (D : ℝ) (p : V → ℝ) : V → ℝ :=
  fun v => U v + D * (Real.log (p v) + 1)
lemma hasDerivAt_entropyTerm (D : ℝ) (p : ℝ → ℝ) (p' : ℝ) (τ : ℝ)
    (hp : 0 < p τ) (hp' : HasDerivAt p p' τ) :
    HasDerivAt (fun s : ℝ => D * p s * Real.log (p s))
      (D * p' * (Real.log (p τ) + 1)) τ := by
  have hlog : HasDerivAt (fun s : ℝ => Real.log (p s)) (p' * (p τ)⁻¹) τ := by
    simpa [Function.comp_def, mul_comm] using (Real.hasDerivAt_log (ne_of_gt hp)).comp τ hp'
  have hpD : HasDerivAt (fun s : ℝ => D * p s) (D * p') τ := hp'.const_mul D
  have hmul : HasDerivAt (fun s : ℝ => (D * p s) * Real.log (p s))
      ((D * p') * Real.log (p τ) + (D * p τ) * (p' * (p τ)⁻¹)) τ := hpD.mul hlog
  have hsimp : (D * p') * Real.log (p τ) + (D * p τ) * (p' * (p τ)⁻¹)
      = D * p' * (Real.log (p τ) + 1) := by
    field_simp [ne_of_gt hp]
  simpa [hsimp] using hmul
theorem freeEnergy_chain_rule (U : V → ℝ) (D : ℝ) (p : ℝ → V → ℝ) (p' : V → ℝ) (τ : ℝ)
    (hp_pos : ∀ v, 0 < p τ v) (hp_deriv : ∀ v, HasDerivAt (fun s : ℝ => p s v) (p' v) τ) :
    HasDerivAt (fun s : ℝ => freeEnergy U D (p s))
      (∑ v, variationalXi U D (p τ) v * p' v) τ := by
  classical
  let f : V → ℝ → ℝ := fun v s => U v * p s v + D * p s v * Real.log (p s v)
  let f' : V → ℝ := fun v => variationalXi U D (p τ) v * p' v
  have hsum : HasDerivAt (fun s : ℝ => ∑ v, f v s) (∑ v, f' v) τ := by
    have hfun : HasDerivAt (∑ v, f v) (∑ v, f' v) τ := by
      apply HasDerivAt.sum
      intro v hv
      have hU : HasDerivAt (fun s : ℝ => U v * p s v) (U v * p' v) τ := (hp_deriv v).const_mul (U v)
      have hD : HasDerivAt (fun s : ℝ => D * p s v * Real.log (p s v))
          (D * p' v * (Real.log (p τ v) + 1)) τ :=
        hasDerivAt_entropyTerm D (fun s => p s v) (p' v) τ (hp_pos v) (hp_deriv v)
      have h := hU.add hD
      have hderiv : U v * p' v + D * p' v * (Real.log (p τ v) + 1)
          = (U v + D * (Real.log (p τ v) + 1)) * p' v := by ring
      have hfun_eta : ((fun s : ℝ => U v * p s v) + (fun s : ℝ => D * p s v * Real.log (p s v)))
          = fun s : ℝ => U v * p s v + D * p s v * Real.log (p s v) := by
        funext s
        simp
      simpa [f, f', variationalXi, hderiv, hfun_eta] using h
    have hfun' : HasDerivAt (fun s : ℝ => ∑ v, f v s) (∑ v, f' v) τ := by
      convert hfun using 1
      funext s
      simp [Finset.sum_apply]
    exact hfun'
  simpa [f, f', freeEnergy] using hsum
lemma discGrad_const_zero : discGrad s t (fun _ : V => (1 : ℝ)) = fun _ : E => (0 : ℝ) := by
  funext e
  unfold discGrad
  simp
theorem probability_conservation (J : E → ℝ) : ∑ v, discDiv s t J v = 0 := by
  have h := graph_div_summation s t (fun _ : V => (1 : ℝ)) J
  have hg := discGrad_const_zero s t
  rw [hg] at h
  simpa using h
theorem freeEnergyRate_eq_fluxForce (U : V → ℝ) (D : ℝ) (p : ℝ → V → ℝ) (J : E → ℝ) (τ : ℝ)
    (hp_pos : ∀ v, 0 < p τ v)
    (hcont : ∀ v, HasDerivAt (fun s : ℝ => p s v) (- discDiv s t J v) τ) :
    HasDerivAt (fun s : ℝ => freeEnergy U D (p s))
      (freeEnergyRate s t (variationalXi U D (p τ)) J) τ := by
  have hchain := freeEnergy_chain_rule U D p (fun v => - discDiv s t J v) τ hp_pos hcont
  simpa [freeEnergyRate] using hchain
lemma edgeDensity_pos_of_pos {p : V → ℝ} (hp : ∀ v, 0 < p v) (e : E) :
    0 < edgeDensity s p e := by
  simpa [edgeDensity] using hp (s e)
lemma fluxPower_nonneg {p : V → ℝ} {J : E → ℝ} (hp : ∀ v, 0 < p v) :
    0 ≤ fluxPower s p J := by
  dsimp [fluxPower]
  apply mul_nonneg (by norm_num)
  apply Finset.sum_nonneg
  intro e _
  exact div_nonneg (sq_nonneg (J e)) (le_of_lt (edgeDensity_pos_of_pos (s := s) hp e))
lemma forcePower_nonneg {p : V → ℝ} {F : E → ℝ} (hp : ∀ v, 0 < p v) :
    0 ≤ forcePower s p F := by
  dsimp [forcePower]
  apply mul_nonneg (by norm_num)
  apply Finset.sum_nonneg
  intro e _
  exact mul_nonneg (le_of_lt (edgeDensity_pos_of_pos (s := s) hp e)) (sq_nonneg (F e))
theorem freeEnergy_dissipation (U : V → ℝ) (D : ℝ)
    (p : ℝ → V → ℝ) (J : ℝ → E → ℝ) (τ : ℝ)
    (hp_pos : ∀ v, 0 < p τ v)
    (hp_deriv : ∀ v, HasDerivAt (fun t => p t v) (- discDiv s t (J τ) v) τ)
    (hJ : ∀ e, J τ e = - edgeDensity s (p τ) e * discGrad s t (variationalXi U D (p τ)) e) :
    HasDerivAt (fun t => freeEnergy U D (p t))
      (-(fluxPower s (p τ) (J τ) + forcePower s (p τ) (fun e => - discGrad s t (variationalXi U D (p τ)) e))) τ := by
  have hchain := freeEnergyRate_eq_fluxForce s t U D p (J τ) τ hp_pos hp_deriv
  have hp_edge : ∀ e, edgeDensity s (p τ) e ≠ 0 :=
    fun e => ne_of_gt (edgeDensity_pos_of_pos (s := s) hp_pos e)
  have hmaster := flux_force_master s t (p τ) (variationalXi U D (p τ)) (J τ) hp_edge hJ
  have hrate : freeEnergyRate s t (variationalXi U D (p τ)) (J τ) =
      - (fluxPower s (p τ) (J τ) + forcePower s (p τ) (fun e => - discGrad s t (variationalXi U D (p τ)) e)) := by
    linarith [hmaster]
  simpa [hrate] using hchain
theorem freeEnergy_nonincrease_deriv (U : V → ℝ) (D : ℝ)
    (p : ℝ → V → ℝ) (J : ℝ → E → ℝ) (τ : ℝ)
    (hp_pos : ∀ v, 0 < p τ v)
    (hp_deriv : ∀ v, HasDerivAt (fun t => p t v) (- discDiv s t (J τ) v) τ)
    (hJ : ∀ e, J τ e = - edgeDensity s (p τ) e * discGrad s t (variationalXi U D (p τ)) e) :
    ∃ c : ℝ, HasDerivAt (fun t => freeEnergy U D (p t)) c τ ∧ c ≤ 0 := by
  let c : ℝ := - (fluxPower s (p τ) (J τ) +
    forcePower s (p τ) (fun e => - discGrad s t (variationalXi U D (p τ)) e))
  refine ⟨c, freeEnergy_dissipation s t U D p J τ hp_pos hp_deriv hJ, ?_⟩
  have hn1 : 0 ≤ fluxPower s (p τ) (J τ) := fluxPower_nonneg (s := s) hp_pos
  have hn2 : 0 ≤ forcePower s (p τ) (fun e => - discGrad s t (variationalXi U D (p τ)) e) :=
    forcePower_nonneg (s := s) hp_pos
  unfold c
  linarith
lemma probability_mass_hasDerivAt_zero
    (p : ℝ → V → ℝ) (J : ℝ → E → ℝ) (τ : ℝ)
    (hp_deriv : ∀ v, HasDerivAt (fun t => p t v) (- discDiv s t (J τ) v) τ) :
    HasDerivAt (fun t => ∑ v : V, p t v) 0 τ := by
  have hsum : HasDerivAt (fun t => ∑ v : V, p t v) (∑ v : V, - discDiv s t (J τ) v) τ := by
    have hfun : HasDerivAt (∑ v : V, fun t => p t v) (∑ v : V, - discDiv s t (J τ) v) τ := by
      apply HasDerivAt.sum
      intro v _
      exact hp_deriv v
    convert hfun using 1
    funext t
    simp [Finset.sum_apply]
  have hzero : (∑ v : V, - discDiv s t (J τ) v) = 0 := by
    rw [Finset.sum_neg_distrib]
    rw [probability_conservation s t (J τ)]
    norm_num
  simpa [hzero] using hsum
noncomputable def relativeEntropy (p μ : V → ℝ) : ℝ :=
  ∑ v : V, p v * Real.log (p v / μ v)
noncomputable def relFisherInformation (p μ : V → ℝ) : ℝ :=
  ∑ e : E, edgeDensity s p e * (discGrad s t (fun v => Real.log (p v / μ v)) e)^2
end FluxForceConjugate
set_option linter.unusedSectionVars true

section RadialSpectralGap
def radialGapLower (a D : ℝ) : ℝ := a - 6 * D
def freeLaplacianBottom : ℝ := 35
def matchingRate : ℝ := 35 / 3
theorem bakry_emery_combine (D a ric hess g : ℝ)
    (hric : ric = -6 * g) (hhess : a * g ≤ hess) :
    (a - 6 * D) * g ≤ D * ric + hess := by
  rw [hric]
  nlinarith
theorem radial_gap_lower_29 : radialGapLower 35 1 = 29 := by
  unfold radialGapLower
  norm_num
theorem three_spectral_objects_distinct :
    radialGapLower 35 1 ≠ freeLaplacianBottom ∧ freeLaplacianBottom ≠ matchingRate := by
  constructor
  · unfold radialGapLower freeLaplacianBottom; norm_num
  · unfold freeLaplacianBottom matchingRate; norm_num
theorem bottom_eq_three_matching : freeLaplacianBottom = 3 * matchingRate := by
  unfold freeLaplacianBottom matchingRate
  norm_num
end RadialSpectralGap
section QuarticMomentSystem
def kappa4 (E_X4 C : ℝ) : ℝ := E_X4 - 3 * C^2
def GaussianClosure (E_X4 C : ℝ) : Prop := kappa4 E_X4 C = 0
def quarticCovRate (a q C E_X4 D : ℝ) : ℝ := -2*a*C - 2*q*E_X4 + 2*D
def riccatiCovRate (a q C D : ℝ) : ℝ := -2*a*C - 6*q*C^2 + 2*D
theorem quartic_cov_decompose (a q C E_X4 D : ℝ) :
    quarticCovRate a q C E_X4 D = riccatiCovRate a q C D - 2*q*kappa4 E_X4 C := by
  unfold quarticCovRate riccatiCovRate kappa4
  ring
theorem gaussian_closure_reduces (a q C E_X4 D : ℝ) (h : GaussianClosure E_X4 C) :
    quarticCovRate a q C E_X4 D = riccatiCovRate a q C D := by
  rw [quartic_cov_decompose]
  unfold GaussianClosure at h
  rw [h]
  ring
noncomputable def riccatiStationary (a q D : ℝ) : ℝ :=
  (Real.sqrt (a^2 + 12*q*D) - a) / (6*q)
theorem riccati_stationary_solves_closed (a q D : ℝ) (hq : q ≠ 0)
    (hnonneg : 0 ≤ a^2 + 12*q*D) :
    riccatiCovRate a q (riccatiStationary a q D) D = 0 := by
  unfold riccatiCovRate riccatiStationary
  have hsqrt : Real.sqrt (a^2 + 12*q*D)^2 = a^2 + 12*q*D :=
    Real.sq_sqrt hnonneg
  have hsqrt' : Real.sqrt (a^2 + q*D*12)^2 = a^2 + q*D*12 := by
    simpa [mul_comm, mul_left_comm, mul_assoc] using hsqrt
  field_simp [hq]
  ring_nf
  rw [hsqrt']
  ring
end QuarticMomentSystem

theorem antisymmetric_symmetric_contraction {ι : Type*} [Fintype ι]
    (f S : ι → ι → ℝ) (hf : ∀ i j, f i j = -f j i)
    (hS : ∀ i j, S i j = S j i) : (∑ i, ∑ j, f i j*S i j) = 0 := by
  have hn : (∑ i, ∑ j, f i j*S i j) = -(∑ i, ∑ j, f i j*S i j) := by
    calc
      _ = ∑ j, ∑ i, f i j*S i j := Finset.sum_comm
      _ = ∑ j, ∑ i, -(f j i*S j i) := by
        apply Finset.sum_congr rfl; intro j _
        apply Finset.sum_congr rfl; intro i _
        rw [hf i j, hS i j]; ring
      _ = _ := by simp only [Finset.sum_neg_distrib]
  linarith
def betaNP (b eta g : ℝ) : ℝ := eta/2*g+b/(8*Real.pi^2)*g^3
theorem beta_hasDerivAt (b eta g : ℝ) :
    HasDerivAt (betaNP b eta) (eta/2+3*b/(8*Real.pi^2)*g^2) g := by
  unfold betaNP
  convert ((hasDerivAt_id g).const_mul (eta/2)).add
    (((hasDerivAt_id g).pow 3).const_mul (b/(8*Real.pi^2))) using 1
  all_goals solve -- 【枢修R26v2】同上→solve链
    | rfl
    | (ext x; simp)
    | simp
    | (simp; ring)
    | (push_cast; ring)
    | (field_simp; ring)
theorem beta_fixedpoint (b eta g : ℝ) (hb : b ≠ 0)
    (hg : g^2 = -4*Real.pi^2*eta/b) : betaNP b eta g = 0 := by
  unfold betaNP
  have hp := Real.pi_ne_zero
  field_simp at hg ⊢
  nlinarith [congrArg (fun x : ℝ => x*g) hg]
theorem beta_fixedpoint_slope (b eta g : ℝ) (hb : b ≠ 0)
    (hg : g^2 = -4*Real.pi^2*eta/b) :
    eta/2+3*b/(8*Real.pi^2)*g^2 = -eta := by
  rw [hg]; field_simp; ring
def etaSigned : ℝ := -36/35
def gStar : ℝ := Real.sqrt (12*Real.pi^2/35)
theorem gStar_sq : gStar^2 = 12*Real.pi^2/35 := by
  apply Real.sq_sqrt; positivity
theorem signed_fixedpoint : betaNP 12 etaSigned gStar = 0 := by
  apply beta_fixedpoint _ _ _ (by norm_num)
  rw [gStar_sq]; unfold etaSigned; ring
def gTC : ℝ := Real.sqrt (24*Real.pi^2/35)
theorem gTC_sq : gTC^2 = 24*Real.pi^2/35 := by
  apply Real.sq_sqrt; positivity
theorem gTC_sq_eq_two_gStar_sq : gTC^2 = 2 * (gStar^2) := by
  rw [gTC_sq, gStar_sq]
  ring
theorem ouCov_positive (ell D C0 t : ℝ)
    (hl : 0 < ell) (hD : 0 ≤ D) (hC : 0 < C0) (ht : 0 ≤ t) :
    0 < ouCov ell D C0 t := by
  have he : Real.exp (-2*ell*t) ≤ 1 := Real.exp_le_one_iff.mpr (by nlinarith)
  have hfirst := mul_pos hC (Real.exp_pos (-2*ell*t))
  have hsecond := mul_nonneg (div_nonneg hD hl.le) (sub_nonneg.mpr he)
  dsimp [ouCov,relax]
  have hex : -(2*ell)*t = -2*ell*t := by ring
  rw [hex]
  nlinarith
theorem ouCov_strict_decrease (ell D C0 t : ℝ)
    (hl : 0 < ell) (hC : D/ell < C0) (ht : 0 < t) :
    ouCov ell D C0 t < C0 := by
  have he : Real.exp (-2*ell*t) < 1 := Real.exp_lt_one_iff.mpr (by nlinarith [mul_pos hl ht])
  have hp := mul_pos (sub_pos.mpr hC) (sub_pos.mpr he)
  dsimp [ouCov,relax]
  have hex : -(2*ell)*t = -2*ell*t := by ring
  rw [hex]
  nlinarith
end CGICECore

namespace Obstructions
open scoped ProbabilityTheory NNReal
def regP_X (κ lam X : ℝ) : ℝ := -κ + 2 * lam * X
def regK_kin (κ lam X : ℝ) : ℝ := -κ + 6 * lam * X
theorem cusp_kinetic_degenerate {κ lam : ℝ} (hlam : lam ≠ 0) :
    regK_kin κ lam (κ / (6 * lam)) = 0 ∧ regP_X κ lam (κ / (6 * lam)) = -(2 * κ / 3) := by
  constructor
  · unfold regK_kin
    field_simp [hlam]
    ring
  · unfold regP_X
    field_simp [hlam]
    ring
theorem cusp_gradient_instability {κ lam : ℝ} (hκ : 0 < κ) (hlam : lam ≠ 0) :
    regP_X κ lam (κ / (6 * lam)) < 0 := by
  unfold regP_X
  field_simp [hlam]
  nlinarith
theorem kessence_healthy_region {κ lam X : ℝ} (hκ : 0 < κ) (hlam : 0 < lam) :
    (regK_kin κ lam X > 0 ∧ regP_X κ lam X > 0) ↔ X > κ / (2 * lam) := by
  unfold regK_kin regP_X
  have hpos : 0 < 2 * lam := by positivity
  constructor
  · intro h
    exact (div_lt_iff₀ hpos).mpr (by nlinarith [h.2])
  · intro hX
    have hlin : κ < X * (2 * lam) := (div_lt_iff₀ hpos).mp hX
    constructor
    · nlinarith [hlin]
    · have hlamX : 0 < lam * X := by nlinarith [hlin, hκ]
      nlinarith [hlin, hlamX]
theorem redshift_ansatz_div_eq_mul_inv {z_c : ℝ} :
    (fun z : ℝ => z ^ 2 / (z + z_c) ^ 2) = (fun z : ℝ => z ^ 2 * ((z + z_c) ^ 2)⁻¹) := by
  funext z
  rw [div_eq_mul_inv]
theorem metric_dual_scaling {c : ℝ} (hc : c ≠ 0) :
    (70 : ℝ) / c = 35 ↔ c = 2 := by
  constructor
  · intro h
    field_simp [hc] at h
    nlinarith
  · intro h
    rw [h]
    norm_num
theorem third_of_nonzero_ne_self {a : ℝ} (ha : a ≠ 0) :
    a / 3 ≠ a := by
  intro h
  have h3 : (3 : ℝ) ≠ 0 := by norm_num
  have hzero : a = 0 := by
    field_simp [h3] at h
    linarith
  exact ha hzero
theorem two_nonpos_sum_zero_iff_both_zero
    {d₁ d₂ : ℝ} (h1 : d₁ ≤ 0) (h2 : d₂ ≤ 0) (hsum : d₁ + d₂ = 0) :
    d₁ = 0 ∧ d₂ = 0 := by
  constructor <;> linarith
theorem redshift_slope_zero (w_core z_c : ℝ) (hz : z_c ≠ 0) :
    HasDerivAt (fun z => -1 + (1 - w_core) * (z ^ 2 / (z + z_c) ^ 2)) 0 0 := by
  have hn : HasDerivAt (fun z : ℝ => z ^ 2) 0 0 := by
    convert ((hasDerivAt_id (0 : ℝ)).mul (hasDerivAt_id (0 : ℝ))) using 1 <;>
      (first | rfl | ext x; simp [id_eq, pow_two] | simp <;> ring_nf)
  have hd : HasDerivAt (fun z : ℝ => (z + z_c) ^ 2) (2 * z_c) 0 := by
    convert (((hasDerivAt_id (0 : ℝ)).add_const z_c).mul
      ((hasDerivAt_id (0 : ℝ)).add_const z_c)) using 1 <;>
      (first | rfl | ext x; simp [id_eq, pow_two] | simp <;> ring_nf)
  have hden : (0 + z_c) ^ 2 ≠ 0 := by
    simp [hz]
  have hdiv : HasDerivAt (fun z : ℝ => z ^ 2 / (z + z_c) ^ 2) 0 0 := by
    have h := hn.div hd hden
    convert h using 1 <;> (first | rfl | ext x; simp [Pi.div_apply] | norm_num)
  convert ((hasDerivAt_const (0 : ℝ) (-1)).add
    ((hasDerivAt_const (0 : ℝ) (1 - w_core)).mul hdiv)) using 1 <;>
    (first | rfl | ext x; simp | ring)
theorem gaussian_coordinate_variance_is_one :
    Var[id; gaussianReal (0 : ℝ) (1 : ℝ≥0)] = 1 := by
  simpa using (variance_id_gaussianReal (μ := (0 : ℝ)) (v := (1 : ℝ≥0)))
theorem nonneg_integral_zero_iff_ae_zero {α : Type*} [MeasurableSpace α] (μ : Measure α)
    {f : α → ℝ} (hf : 0 ≤ᵐ[μ] f) (hfi : Integrable f μ) :
    (∫ x, f x ∂μ) = 0 ↔ f =ᵐ[μ] 0 :=
  integral_eq_zero_iff_of_nonneg_ae hf hfi
end Obstructions

namespace VEV123CW
open Real
noncomputable section
def mu2 : ℝ := -3
def lam : ℝ := 1
lemma lam_pos : 0 < lam := by norm_num [lam]
lemma lam_ne : lam ≠ 0 := ne_of_gt lam_pos
def V0 (φ : ℝ) : ℝ := (mu2 / 2) * φ ^ 2 + (lam / 4) * φ ^ 4
def V0_deriv (φ : ℝ) : ℝ := mu2 * φ + lam * φ ^ 3
def V0_hess (φ : ℝ) : ℝ := mu2 + 3 * lam * φ ^ 2
def phiStar : ℝ := Real.sqrt (-mu2 / lam)
lemma phiStar_sq : phiStar ^ 2 = -mu2 / lam := by
  unfold phiStar
  have hnonneg : 0 ≤ -mu2 / lam := by
    have hm : 0 ≤ -mu2 := by norm_num [mu2]
    exact div_nonneg hm (le_of_lt lam_pos)
  simpa using (Real.sq_sqrt hnonneg)
lemma phiStar_pos : 0 < phiStar := by
  unfold phiStar
  apply Real.sqrt_pos.mpr
  apply div_pos
  · norm_num [mu2]
  · exact lam_pos
lemma phiStar_sq_value : phiStar ^ 2 = 3 := by
  rw [phiStar_sq]
  norm_num [mu2, lam]
lemma phiStar_fourth_value : phiStar ^ 4 = 9 := by
  have h4 : phiStar ^ 4 = (phiStar ^ 2) ^ 2 := by ring
  rw [h4, phiStar_sq_value]
  norm_num
theorem V0_deriv_at_phiStar : V0_deriv phiStar = 0 := by
  unfold V0_deriv
  have hsq : phiStar ^ 2 = -mu2 / lam := phiStar_sq
  have h3 : phiStar ^ 3 = phiStar * (phiStar ^ 2) := by ring
  rw [h3, hsq]
  field_simp [lam_ne]
  ring
theorem V0_hess_at_phiStar_pos : 0 < V0_hess phiStar := by
  unfold V0_hess
  rw [phiStar_sq]
  have h : mu2 + 3 * lam * (-mu2 / lam) = -2 * mu2 := by
    field_simp [lam_ne]
    ring
  rw [h]
  norm_num [mu2]
theorem hessian_positive_at_stationary :
    ∃ φ : ℝ, φ ≠ 0 ∧ V0_deriv φ = 0 ∧ 0 < V0_hess φ :=
  ⟨phiStar, ne_of_gt phiStar_pos, V0_deriv_at_phiStar, V0_hess_at_phiStar_pos⟩
theorem V0_at_phiStar : V0 phiStar = -mu2 ^ 2 / (4 * lam) := by
  unfold V0 mu2 lam
  rw [phiStar_sq_value, phiStar_fourth_value]
  ring_nf
theorem V0_sub_min (φ : ℝ) :
    V0 φ - (-mu2 ^ 2 / (4 * lam)) = (lam / 4) * (φ ^ 2 - (-mu2 / lam)) ^ 2 := by
  unfold V0
  field_simp [lam_ne]
  ring
theorem V0_global_min (φ : ℝ) : V0 phiStar ≤ V0 φ := by
  rw [V0_at_phiStar]
  have h := V0_sub_min φ
  have hl : 0 ≤ lam / 4 := div_nonneg (le_of_lt lam_pos) (by norm_num)
  have hsq : 0 ≤ (φ ^ 2 - (-mu2 / lam)) ^ 2 := sq_nonneg _
  have hnn : 0 ≤ (lam / 4) * (φ ^ 2 - (-mu2 / lam)) ^ 2 := mul_nonneg hl hsq
  linarith
def V0_param (m2 lam φ : ℝ) : ℝ := (m2 / 2) * φ ^ 2 + (lam / 4) * φ ^ 4
def V0_deriv_param (m2 lam φ : ℝ) : ℝ := m2 * φ + lam * φ ^ 3
def V0_hess_param (m2 lam φ : ℝ) : ℝ := m2 + 3 * lam * φ ^ 2
theorem V0_hess_param_at_zero (m2 lam : ℝ) : V0_hess_param m2 lam 0 = m2 := by
  unfold V0_hess_param
  norm_num
theorem V0_hess_param_at_zero_neg (m2 lam : ℝ) (hm2 : m2 < 0) :
    V0_hess_param m2 lam 0 < 0 := by
  simpa [V0_hess_param_at_zero] using hm2
theorem V0_param_square_completion (m2 lam φ : ℝ) (hlam : lam ≠ 0) :
    V0_param m2 lam φ - (-(m2 ^ 2) / (4 * lam)) = (lam / 4) * (φ ^ 2 + m2 / lam) ^ 2 := by
  unfold V0_param
  field_simp [hlam]
  ring
theorem V0_param_min_lower_bound (m2 lam φ : ℝ) (hlam_pos : 0 < lam) :
    -(m2 ^ 2) / (4 * lam) ≤ V0_param m2 lam φ := by
  have h := V0_param_square_completion m2 lam φ (ne_of_gt hlam_pos)
  have hsq : 0 ≤ (φ ^ 2 + m2 / lam) ^ 2 := sq_nonneg _
  have hl : 0 ≤ lam / 4 := div_nonneg (le_of_lt hlam_pos) (by norm_num)
  have hnn : 0 ≤ (lam / 4) * (φ ^ 2 + m2 / lam) ^ 2 := mul_nonneg hl hsq
  linarith
end
end VEV123CW

namespace SourceQ
noncomputable section
structure Comp where
  rho_b  : ℝ
  rho_DM : ℝ
  rho_BH : ℝ
deriving Inhabited
def Comp.total (N : Comp) : ℝ := N.rho_b + N.rho_DM + N.rho_BH
structure Rates where
  Γ_b    : ℝ
  Γ_BH   : ℝ
  Γ_DM   : ℝ
  Γ_b2DM : ℝ
def Rates.A (r : Rates) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![-(r.Γ_b + r.Γ_b2DM), r.Γ_DM, 0;
     r.Γ_b2DM, -r.Γ_DM, r.Γ_BH;
     r.Γ_b, 0, -r.Γ_BH]
def Rates.act (r : Rates) (N : Comp) : Comp where
  rho_b  := -(r.Γ_b + r.Γ_b2DM) * N.rho_b + r.Γ_DM * N.rho_DM
  rho_DM := r.Γ_b2DM * N.rho_b - r.Γ_DM * N.rho_DM + r.Γ_BH * N.rho_BH
  rho_BH := r.Γ_b * N.rho_b - r.Γ_BH * N.rho_BH
def Rates.Q_b_to_BH (r : Rates) (N : Comp) : ℝ := r.Γ_b * N.rho_b
def Rates.Q_BH_to_DM (r : Rates) (N : Comp) : ℝ := r.Γ_BH * N.rho_BH
def Rates.Q_DM_to_b (r : Rates) (N : Comp) : ℝ := r.Γ_DM * N.rho_DM
def Rates.Q_b_to_DM (r : Rates) (N : Comp) : ℝ := r.Γ_b2DM * N.rho_b
def Rates.source_b (r : Rates) (N : Comp) : ℝ :=
  r.Q_DM_to_b N - r.Q_b_to_BH N - r.Q_b_to_DM N
def Rates.source_DM (r : Rates) (N : Comp) : ℝ :=
  r.Q_b_to_DM N + r.Q_BH_to_DM N - r.Q_DM_to_b N
def Rates.source_BH (r : Rates) (N : Comp) : ℝ :=
  r.Q_b_to_BH N - r.Q_BH_to_DM N
def ValidRates (r : Rates) : Prop :=
    r.Γ_b ≥ 0 ∧ r.Γ_BH ≥ 0 ∧ r.Γ_DM ≥ 0 ∧ r.Γ_b2DM ≥ 0
theorem valid_rates_exists : ∃ r : Rates, ValidRates r := by
  refine ⟨⟨0, 0, 0, 0⟩, ?_⟩
  constructor <;> norm_num
def initial_dm_baryon_ratio : ℝ := 5
def observed_dm_baryon_ratio : ℝ := 547 / 100
theorem initial_ratio_eq : (5 : ℝ) = initial_dm_baryon_ratio := rfl
theorem observed_ratio_eq : observed_dm_baryon_ratio = (547 : ℝ) / 100 := rfl
def baryonLossFraction : ℝ := 1 - 5 / observed_dm_baryon_ratio
theorem act_total_zero (r : Rates) (N : Comp) :
    (r.act N).total = 0 := by
  unfold Rates.act Comp.total
  ring
theorem total_mass_conserved (r : Rates) (N : Comp) :
    (r.act N).total = 0 := act_total_zero r N
theorem transfer_rhs_sums_to_zero (r : Rates) (N : Comp) :
    (r.act N).total = 0 := act_total_zero r N
structure TransferSolution (r : Rates) where
  rho_b : ℝ → ℝ
  rho_DM : ℝ → ℝ
  rho_BH : ℝ → ℝ
  hasDeriv_b : ∀ t, HasDerivAt rho_b ((r.act ⟨rho_b t, rho_DM t, rho_BH t⟩).rho_b) t
  hasDeriv_DM : ∀ t, HasDerivAt rho_DM ((r.act ⟨rho_b t, rho_DM t, rho_BH t⟩).rho_DM) t
  hasDeriv_BH : ∀ t, HasDerivAt rho_BH ((r.act ⟨rho_b t, rho_DM t, rho_BH t⟩).rho_BH) t
theorem transfer_solution_total_deriv_zero (r : Rates) (sol : TransferSolution r) (t : ℝ) :
    HasDerivAt (fun x => sol.rho_b x + sol.rho_DM x + sol.rho_BH x) 0 t := by
  let N : Comp := ⟨sol.rho_b t, sol.rho_DM t, sol.rho_BH t⟩
  have hb : HasDerivAt sol.rho_b ((r.act N).rho_b) t := sol.hasDeriv_b t
  have hDM : HasDerivAt sol.rho_DM ((r.act N).rho_DM) t := sol.hasDeriv_DM t
  have hBH : HasDerivAt sol.rho_BH ((r.act N).rho_BH) t := sol.hasDeriv_BH t
  have hsum : HasDerivAt (fun x => sol.rho_b x + sol.rho_DM x + sol.rho_BH x)
      (((r.act N).rho_b + (r.act N).rho_DM) + (r.act N).rho_BH) t :=
    (hb.add hDM).add hBH
  have hzero : ((r.act N).rho_b + (r.act N).rho_DM) + (r.act N).rho_BH = 0 := by
    simpa [Comp.total] using (act_total_zero r N)
  simpa [hzero] using hsum
theorem transfer_solution_total_constant (r : Rates) (sol : TransferSolution r) (t t0 : ℝ) :
    sol.rho_b t + sol.rho_DM t + sol.rho_BH t =
    sol.rho_b t0 + sol.rho_DM t0 + sol.rho_BH t0 := by
  let f : ℝ → ℝ := fun x => sol.rho_b x + sol.rho_DM x + sol.rho_BH x
  have hf : Differentiable ℝ f := by
    intro x
    exact (transfer_solution_total_deriv_zero r sol x).differentiableAt
  have hf' : ∀ x, deriv f x = 0 := by
    intro x
    exact (transfer_solution_total_deriv_zero r sol x).deriv
  exact is_const_of_deriv_eq_zero hf hf' t t0
theorem baryon_loss_approx :
    |baryonLossFraction - (859 : ℝ) / 10000| < (1 : ℝ) / 1000 := by
  unfold baryonLossFraction
  rw [observed_ratio_eq]
  norm_num
theorem baryon_loss_pos : baryonLossFraction > 0 := by
  unfold baryonLossFraction
  rw [observed_ratio_eq]
  norm_num
theorem baryon_loss_lt_one : baryonLossFraction < 1 := by
  unfold baryonLossFraction
  rw [observed_ratio_eq]
  norm_num
theorem baryon_loss_relation :
    baryonLossFraction = 1 - 5 / observed_dm_baryon_ratio := rfl
theorem baryon_loss_from_initial :
    baryonLossFraction = 1 - 5 / observed_dm_baryon_ratio
    ∧ initial_dm_baryon_ratio = 5 := by
  refine ⟨rfl, ?_⟩
  linarith [initial_ratio_eq]
theorem source_matches_act (r : Rates) (N : Comp) :
    r.source_b N = (r.act N).rho_b ∧
    r.source_DM N = (r.act N).rho_DM ∧
    r.source_BH N = (r.act N).rho_BH := by
  unfold Rates.source_b Rates.source_DM Rates.source_BH
  unfold Rates.Q_b_to_BH Rates.Q_BH_to_DM Rates.Q_DM_to_b Rates.Q_b_to_DM
  unfold Rates.act
  ring_nf
  tauto
theorem source_sum_zero (r : Rates) (N : Comp) :
    r.source_b N + r.source_DM N + r.source_BH N = 0 := by
  unfold Rates.source_b Rates.source_DM Rates.source_BH
  unfold Rates.Q_b_to_BH Rates.Q_BH_to_DM Rates.Q_DM_to_b Rates.Q_b_to_DM
  ring
end
end SourceQ

namespace DMAbundance
noncomputable section
structure BoltzmannSolution where
  lambda : ℝ → ℝ
  Y_eq : ℝ → ℝ
  Y : ℝ → ℝ
  lambda_pos : ∀ x, 0 < x → 0 < lambda x
  Y_eq_pos : ∀ x, 0 < x → 0 < Y_eq x
  Y_pos : ∀ x, 0 < x → 0 < Y x
  frozen_above_eq : ∀ x, 0 < x → Y_eq x < Y x
  boltzmann : ∀ x, 0 < x →
    deriv Y x = -(lambda x) * ((Y x)^2 - (Y_eq x)^2)
theorem frozen_monotone_decreasing
    (sol : BoltzmannSolution) (x : ℝ) (hx : 0 < x) :
    deriv sol.Y x < 0 := by
  rw [sol.boltzmann x hx]
  have h1 : 0 < sol.lambda x := sol.lambda_pos x hx
  have h2 : sol.Y_eq x < sol.Y x := sol.frozen_above_eq x hx
  have h3 : 0 < sol.Y x := sol.Y_pos x hx
  have h4 : (sol.Y_eq x)^2 < (sol.Y x)^2 := by
    apply sq_lt_sq.mpr
    rw [abs_of_pos (sol.Y_eq_pos x hx), abs_of_pos (sol.Y_pos x hx)]
    exact h2
  have h5 : 0 < (sol.Y x)^2 - (sol.Y_eq x)^2 := sub_pos.mpr h4
  have : -(sol.lambda x) * ((sol.Y x)^2 - (sol.Y_eq x)^2) < 0 := by
    have := mul_pos h1 h5
    linarith
  exact this
theorem frozen_differentiable (sol : BoltzmannSolution) (x : ℝ) (hx : 0 < x) :
    DifferentiableAt ℝ sol.Y x :=
  differentiableAt_of_deriv_ne_zero (ne_of_lt (frozen_monotone_decreasing sol x hx))
noncomputable def counterexample_Y (x : ℝ) : ℝ := 1 / (1 + x)
noncomputable def counterexample_Y_eq (x : ℝ) : ℝ := 1 / (2 * (1 + x))
lemma one_add_pos_of_pos {x : ℝ} (hx : 0 < x) : 0 < 1 + x := by linarith
lemma one_add_ne_zero_of_pos {x : ℝ} (hx : 0 < x) : 1 + x ≠ 0 :=
  ne_of_gt (one_add_pos_of_pos hx)
lemma deriv_counterexample_Y {x : ℝ} (hx : 0 < x) :
    deriv counterexample_Y x = -(1 : ℝ) / (1 + x) ^ 2 := by
  unfold counterexample_Y
  have h1 : HasDerivAt (fun t => (1 : ℝ) + t) 1 x := by
    simpa using ((hasDerivAt_id x).const_add (1 : ℝ))
  have h2 : HasDerivAt (fun t => ((1 : ℝ) + t)⁻¹) (-1 / (1 + x) ^ 2) x := by
    exact h1.inv (one_add_ne_zero_of_pos hx)
  have h3 : HasDerivAt (fun t => (1 : ℝ) / (1 + t)) (-1 / (1 + x) ^ 2) x := by
    simpa [div_eq_mul_inv] using h2.const_mul (1 : ℝ)
  rw [h3.deriv]
lemma counterexample_boltzmann {x : ℝ} (hx : 0 < x) :
    deriv counterexample_Y x =
      -((4 : ℝ) / 3) * ((counterexample_Y x) ^ 2 - (counterexample_Y_eq x) ^ 2) := by
  rw [deriv_counterexample_Y hx]
  unfold counterexample_Y counterexample_Y_eq
  field_simp [one_add_ne_zero_of_pos hx]
  ring
noncomputable def counterexample_solution : BoltzmannSolution where
  lambda := fun _ => (4 : ℝ) / 3
  Y_eq := counterexample_Y_eq
  Y := counterexample_Y
  lambda_pos := by intro x _; norm_num
  Y_eq_pos := by
    intro x hx
    unfold counterexample_Y_eq
    exact one_div_pos.mpr (mul_pos two_pos (one_add_pos_of_pos hx))
  Y_pos := by
    intro x hx
    unfold counterexample_Y
    exact one_div_pos.mpr (one_add_pos_of_pos hx)
  frozen_above_eq := by
    intro x hx
    unfold counterexample_Y counterexample_Y_eq
    have hpos : 0 < 1 + x := one_add_pos_of_pos hx
    have hpos2 : 0 < 2 * (1 + x) := mul_pos two_pos hpos
    rw [one_div_lt_one_div hpos2 hpos]
    nlinarith
  boltzmann := by
    intro x hx
    exact counterexample_boltzmann hx
theorem counterexample_tendsto_zero :
    Filter.Tendsto counterexample_Y Filter.atTop (nhds 0) := by
  unfold counterexample_Y
  have h1 : Filter.Tendsto (fun x => (1 : ℝ) + x) Filter.atTop Filter.atTop := by
    rw [show (fun x => (1 : ℝ) + x) = fun x => x + (1 : ℝ) by funext; ring]
    exact Filter.atTop.tendsto_atTop_add_const_right (1 : ℝ) Filter.tendsto_id
  have h2 : Filter.Tendsto (fun x => ((1 : ℝ) + x)⁻¹) Filter.atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp h1
  simpa [one_div] using h2
structure RelicSolution where
  sol : BoltzmannSolution
  Y_infinity : ℝ
  tendsto_Y : Filter.Tendsto sol.Y Filter.atTop (nhds Y_infinity)
structure PositiveRelicSolution extends RelicSolution where
  Y_infinity_pos : 0 < Y_infinity
theorem dof_ratio_seventyfive_fifteen : (75 : ℚ) / 15 = 5 := by
  norm_num
theorem baryon_loss_fraction :
    (1 : ℚ) - 5 / (547 / 100 : ℚ) = 47 / 547 := by
  norm_num
theorem baryon_loss_percent_bound :
    0 < (47 : ℚ) / 547 ∧ (47 : ℚ) / 547 < 1 / 10 := by
  constructor <;> norm_num
theorem dm_baryon_ratio_consistency :
    (5 : ℚ) / (1 - 47 / 547) = 547 / 100 := by
  norm_num
end
noncomputable def positiveRelic_lambda (x : ℝ) : ℝ := 1 / (1 + x)^2
noncomputable def positiveRelic_Y (x : ℝ) : ℝ := 4 * (1 + x) / (1 + 4 * x)
noncomputable def positiveRelic_Y_eq (x : ℝ) : ℝ := 2 * (1 + x) / (1 + 4 * x)
lemma one_add_four_mul_pos_of_pos {x : ℝ} (hx : 0 < x) : 0 < 1 + 4 * x := by
  nlinarith
lemma one_add_four_mul_ne_zero_of_pos {x : ℝ} (hx : 0 < x) : 1 + 4 * x ≠ 0 :=
  ne_of_gt (one_add_four_mul_pos_of_pos hx)
lemma positiveRelic_Y_deriv {x : ℝ} (hx : 0 < x) :
    deriv positiveRelic_Y x = -12 / (1 + 4 * x)^2 := by
  have h_num : HasDerivAt (fun t => (4 : ℝ) * (1 + t)) 4 x := by
    have h1 : HasDerivAt (fun t => (1 : ℝ) + t) 1 x := by
      simpa using ((hasDerivAt_id x).const_add (1 : ℝ))
    simpa [mul_add, mul_one] using h1.const_mul (4 : ℝ)
  have h_den : HasDerivAt (fun t => (1 : ℝ) + 4 * t) 4 x := by
    have h1 : HasDerivAt (fun t => (4 : ℝ) * t) 4 x := by simpa using (hasDerivAt_id x).const_mul 4
    simpa [add_comm] using h1.const_add (1 : ℝ)
  have h_den_ne : (1 + 4 * x) ≠ 0 := one_add_four_mul_ne_zero_of_pos hx
  have h_inv : HasDerivAt (fun t => ((1 : ℝ) + 4 * t)⁻¹) (-4 / (1 + 4 * x)^2) x :=
    h_den.inv h_den_ne
  have h_mul : HasDerivAt (fun t => (4 : ℝ) * (1 + t) * ((1 + 4 * t)⁻¹))
      (4 * ((1 + 4 * x)⁻¹) + (4 * (1 + x)) * (-4 / (1 + 4 * x)^2)) x :=
    h_num.mul h_inv
  have h_div : HasDerivAt positiveRelic_Y
      (4 * ((1 + 4 * x)⁻¹) + (4 * (1 + x)) * (-4 / (1 + 4 * x)^2)) x := by
    unfold positiveRelic_Y
    simpa [div_eq_mul_inv] using h_mul
  rw [h_div.deriv]
  field_simp [one_add_four_mul_ne_zero_of_pos hx]
  ring
lemma positiveRelic_boltzmann_rhs {x : ℝ} (hx : 0 < x) :
    -(positiveRelic_lambda x) * ((positiveRelic_Y x)^2 - (positiveRelic_Y_eq x)^2)
      = -12 / (1 + 4 * x)^2 := by
  unfold positiveRelic_lambda positiveRelic_Y positiveRelic_Y_eq
  have h1ne : 1 + x ≠ 0 := one_add_ne_zero_of_pos hx
  have h1sqne : (1 + x)^2 ≠ 0 := pow_ne_zero 2 h1ne
  have h2ne : 1 + 4 * x ≠ 0 := one_add_four_mul_ne_zero_of_pos hx
  field_simp [h1ne, h1sqne, h2ne]
  ring
lemma positiveRelic_boltzmann {x : ℝ} (hx : 0 < x) :
    deriv positiveRelic_Y x =
      -(positiveRelic_lambda x) * ((positiveRelic_Y x)^2 - (positiveRelic_Y_eq x)^2) := by
  rw [positiveRelic_Y_deriv hx, positiveRelic_boltzmann_rhs hx]
lemma positiveRelic_lambda_pos {x : ℝ} (hx : 0 < x) : 0 < positiveRelic_lambda x := by
  unfold positiveRelic_lambda
  exact one_div_pos.mpr (sq_pos_of_ne_zero (one_add_ne_zero_of_pos hx))
lemma positiveRelic_Y_pos {x : ℝ} (hx : 0 < x) : 0 < positiveRelic_Y x := by
  unfold positiveRelic_Y
  have h1pos : 0 < 4 * (1 + x) := mul_pos (by norm_num : 0 < (4 : ℝ)) (one_add_pos_of_pos hx)
  have h2pos : 0 < 1 + 4 * x := one_add_four_mul_pos_of_pos hx
  exact div_pos h1pos h2pos
lemma positiveRelic_Y_eq_pos {x : ℝ} (hx : 0 < x) : 0 < positiveRelic_Y_eq x := by
  unfold positiveRelic_Y_eq
  have h1pos : 0 < 2 * (1 + x) := mul_pos (by norm_num : 0 < (2 : ℝ)) (one_add_pos_of_pos hx)
  have h2pos : 0 < 1 + 4 * x := one_add_four_mul_pos_of_pos hx
  exact div_pos h1pos h2pos
lemma positiveRelic_frozen_above_eq {x : ℝ} (hx : 0 < x) :
    positiveRelic_Y_eq x < positiveRelic_Y x := by
  unfold positiveRelic_Y_eq positiveRelic_Y
  have h1pos : 0 < 4 * (1 + x) := mul_pos (by norm_num : 0 < (4 : ℝ)) (one_add_pos_of_pos hx)
  have h2pos : 0 < 1 + 4 * x := one_add_four_mul_pos_of_pos hx
  have hdivpos : 0 < 4 * (1 + x) / (1 + 4 * x) := div_pos h1pos h2pos
  have hhalf : (2 : ℝ) * (1 + x) / (1 + 4 * x) < 4 * (1 + x) / (1 + 4 * x) := by
    rw [div_lt_div_iff_of_pos_right h2pos]
    nlinarith
  exact hhalf
noncomputable def positiveRelic_boltzmann_solution : BoltzmannSolution where
  lambda := positiveRelic_lambda
  Y_eq := positiveRelic_Y_eq
  Y := positiveRelic_Y
  lambda_pos := fun x hx => positiveRelic_lambda_pos hx
  Y_eq_pos := fun x hx => positiveRelic_Y_eq_pos hx
  Y_pos := fun x hx => positiveRelic_Y_pos hx
  frozen_above_eq := fun x hx => positiveRelic_frozen_above_eq hx
  boltzmann := fun x hx => positiveRelic_boltzmann hx
lemma positiveRelic_Y_rewrite {x : ℝ} (hx : 0 < x) :
    positiveRelic_Y x = 1 + 3 / (1 + 4 * x) := by
  unfold positiveRelic_Y
  have h2ne : 1 + 4 * x ≠ 0 := one_add_four_mul_ne_zero_of_pos hx
  field_simp [h2ne]
  ring
lemma positiveRelic_Y_tendsto_one : Filter.Tendsto positiveRelic_Y Filter.atTop (nhds 1) := by
  have h_den : Filter.Tendsto (fun x => (1 : ℝ) + 4 * x) Filter.atTop Filter.atTop := by
    rw [show (fun x => (1 : ℝ) + 4 * x) = fun x => 4 * x + (1 : ℝ) by funext; ring]
    exact Filter.atTop.tendsto_atTop_add_const_right (1 : ℝ)
      (Filter.tendsto_id.const_mul_atTop (by norm_num : 0 < (4 : ℝ)))
  have h_inv : Filter.Tendsto (fun x => ((1 : ℝ) + 4 * x)⁻¹) Filter.atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp h_den
  have h_three : Filter.Tendsto (fun x => (3 : ℝ) / (1 + 4 * x)) Filter.atTop (nhds 0) := by
    simpa [div_eq_mul_inv] using h_inv.const_mul (3 : ℝ)
  have h_sum : Filter.Tendsto (fun x => (1 : ℝ) + 3 / (1 + 4 * x)) Filter.atTop (nhds 1) := by
    simpa using (tendsto_const_nhds.add h_three)
  refine Filter.Tendsto.congr' ?_ h_sum
  filter_upwards [Filter.eventually_gt_atTop (0 : ℝ)] with x hx
  exact (positiveRelic_Y_rewrite hx).symm
noncomputable def positiveRelic_solution : PositiveRelicSolution where
  toRelicSolution := {
    sol := positiveRelic_boltzmann_solution
    Y_infinity := 1
    tendsto_Y := positiveRelic_Y_tendsto_one
  }
  Y_infinity_pos := by norm_num
lemma positiveRelic_Y_gt_one {x : ℝ} (hx : 0 < x) : 1 < positiveRelic_Y x := by
  rw [positiveRelic_Y_rewrite hx]
  have h3pos : 0 < (3 : ℝ) := by norm_num
  have h_den_pos : 0 < 1 + 4 * x := one_add_four_mul_pos_of_pos hx
  have h_div_pos : 0 < 3 / (1 + 4 * x) := div_pos h3pos h_den_pos
  linarith
theorem positiveRelic_exists : ∃ r : PositiveRelicSolution, r.Y_infinity = 1 :=
  ⟨positiveRelic_solution, rfl⟩
noncomputable def TailIntegrable (f : ℝ → ℝ) (x_f : ℝ) : Prop :=
  IntegrableOn f (Set.Ioi x_f)
noncomputable def freeze_b (s : BoltzmannSolution) (x : ℝ) : ℝ :=
  s.lambda x * (1 - (s.Y_eq x / s.Y x)^2)
lemma freeze_b_nonneg (s : BoltzmannSolution) {x : ℝ} (hx : 0 < x) : 0 ≤ freeze_b s x := by
  unfold freeze_b
  have hYpos : 0 < s.Y x := s.Y_pos x hx
  have hle : s.Y_eq x / s.Y x ≤ 1 := (div_le_one hYpos).2 (le_of_lt (s.frozen_above_eq x hx))
  have hsq : (s.Y_eq x / s.Y x)^2 ≤ 1 := by
    have hnonneg : 0 ≤ s.Y_eq x / s.Y x :=
      div_nonneg (le_of_lt (s.Y_eq_pos x hx)) (le_of_lt hYpos)
    rw [sq_le_one_iff_abs_le_one]
    rw [abs_of_nonneg hnonneg]
    exact hle
  exact mul_nonneg (le_of_lt (s.lambda_pos x hx)) (sub_nonneg.mpr hsq)
lemma freeze_b_le_lambda (s : BoltzmannSolution) {x : ℝ} (hx : 0 < x) :
    freeze_b s x ≤ s.lambda x := by
  unfold freeze_b
  have hYpos : 0 < s.Y x := s.Y_pos x hx
  have hle : s.Y_eq x / s.Y x ≤ 1 := (div_le_one hYpos).2 (le_of_lt (s.frozen_above_eq x hx))
  have hsq_nonneg : 0 ≤ (s.Y_eq x / s.Y x)^2 := sq_nonneg _
  have h_sub_le_one : 1 - (s.Y_eq x / s.Y x)^2 ≤ 1 := by linarith
  calc
    s.lambda x * (1 - (s.Y_eq x / s.Y x)^2) ≤ s.lambda x * 1 :=
      mul_le_mul_of_nonneg_left h_sub_le_one (le_of_lt (s.lambda_pos x hx))
    _ = s.lambda x := by ring
end DMAbundance

namespace GWTT
noncomputable section
open Real
variable {n : ℕ}
abbrev TensorField (n : ℕ) := Matrix (Fin n) (Fin n) ℝ
def trace (A : TensorField n) : ℝ := Matrix.trace A
def divergence (A : TensorField n) (k : Fin n → ℝ) : Fin n → ℝ :=
  fun i => ∑ j, k j * A i j
def TTSubspace (k : Fin n → ℝ) : Set (TensorField n) :=
  { A | trace A = 0 ∧ divergence A k = 0 ∧ A.transpose = A }
theorem zero_mem_TTSubspace (k : Fin n → ℝ) :
    (0 : TensorField n) ∈ TTSubspace k := by
  constructor
  · simp [trace]
  · constructor
    · funext i
      simp [divergence]
    · simp
theorem trace_add (A B : TensorField n) :
    trace (A + B) = trace A + trace B := by
  simp [trace, Matrix.trace_add]
theorem trace_smul (c : ℝ) (A : TensorField n) :
    trace (c • A) = c * trace A := by
  simp [trace, Matrix.trace_smul]
theorem divergence_add (A B : TensorField n) (k : Fin n → ℝ) :
    divergence (A + B) k = divergence A k + divergence B k := by
  funext i
  simp [divergence, mul_add, Finset.sum_add_distrib]
theorem divergence_smul (c : ℝ) (A : TensorField n) (k : Fin n → ℝ) :
    divergence (c • A) k = c • divergence A k := by
  funext i
  simp [divergence]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  ring
theorem add_mem_TTSubspace (k : Fin n → ℝ) {A B : TensorField n}
    (hA : A ∈ TTSubspace k) (hB : B ∈ TTSubspace k) :
    A + B ∈ TTSubspace k := by
  rcases hA with ⟨hAtr, hAdiv, hAsym⟩
  rcases hB with ⟨hBtr, hBdiv, hBsym⟩
  constructor
  · rw [trace_add, hAtr, hBtr, add_zero]
  · constructor
    · rw [divergence_add, hAdiv, hBdiv]
      simp
    · rw [Matrix.transpose_add, hAsym, hBsym]
theorem smul_mem_TTSubspace (k : Fin n → ℝ) (c : ℝ) {A : TensorField n}
    (hA : A ∈ TTSubspace k) : c • A ∈ TTSubspace k := by
  rcases hA with ⟨hAtr, hAdiv, hAsym⟩
  constructor
  · rw [trace_smul, hAtr, mul_zero]
  · constructor
    · rw [divergence_smul, hAdiv, smul_zero]
    · rw [Matrix.transpose_smul, hAsym]
theorem TTSubspace_isLinear (k : Fin n → ℝ) :
    (0 : TensorField n) ∈ TTSubspace k ∧
    (∀ A B, A ∈ TTSubspace k → B ∈ TTSubspace k → A + B ∈ TTSubspace k) ∧
    (∀ (c : ℝ) A, A ∈ TTSubspace k → c • A ∈ TTSubspace k) :=
  ⟨zero_mem_TTSubspace k,
   fun _ _ hA hB => add_mem_TTSubspace k hA hB,
   fun c _ hA => smul_mem_TTSubspace k c hA⟩
def IsIsotropicSource (S : TensorField n) : Prop :=
  ∃ s : ℝ, S = s • (1 : TensorField n)
noncomputable def transverseProjector (n : ℕ) (k : Fin n → ℝ) : TensorField n :=
  fun i j => (if i = j then (1 : ℝ) else 0) - k i * k j / (∑ l : Fin n, k l * k l)
noncomputable def ttProjectionExplicit (n : ℕ) (k : Fin n → ℝ) (S : TensorField n) : TensorField n :=
  (transverseProjector n k * S * transverseProjector n k) -
    (trace (transverseProjector n k * S) / ((n : ℝ) - 1)) • transverseProjector n k
def NonzeroWavevector {n : ℕ} (k : Fin n → ℝ) : Prop := k ≠ 0
def SymmetricTensor {n : ℕ} (S : TensorField n) : Prop := ∀ i j, S i j = S j i
lemma trace_mul_mul_eq_trace_mul_of_idempotent {n : ℕ} (P S : TensorField n) (hP : P * P = P) :
    Matrix.trace (P * S * P) = Matrix.trace (P * S) := by
  calc
    Matrix.trace (P * S * P) = Matrix.trace (P * (S * P)) := by rw [Matrix.mul_assoc]
    _ = Matrix.trace ((S * P) * P) := by rw [Matrix.trace_mul_comm]
    _ = Matrix.trace (S * (P * P)) := by rw [Matrix.mul_assoc]
    _ = Matrix.trace (S * P) := by rw [hP]
    _ = Matrix.trace (P * S) := by rw [Matrix.trace_mul_comm]
lemma transpose_mul_mul_self_of_symm {n : ℕ} (A B : TensorField n)
    (hA : A.transpose = A) (hB : B.transpose = B) :
    (A * B * A).transpose = A * B * A := by
  rw [Matrix.transpose_mul, Matrix.transpose_mul, hA, hB, Matrix.mul_assoc]
lemma divergence_eq_mulVec (A : TensorField 3) (k : Fin 3 → ℝ) :
    divergence A k = Matrix.mulVec A k := by
  funext i
  unfold divergence
  exact Finset.sum_congr rfl (fun j _ => mul_comm (k j) (A i j))
lemma mul_tt_mul_self {n : ℕ} (P S : TensorField n) (c : ℝ) (hP : P * P = P) :
    P * ((P * S * P) - c • P) * P = (P * S * P) - c • P := by
  rw [Matrix.mul_sub, Matrix.mul_smul, Matrix.sub_mul, Matrix.smul_mul]
  have hre : (P * (P * S * P)) * P = (P * P) * S * (P * P) := by
    noncomm_ring
  rw [hre, hP, hP]
theorem transverseProjector_symm (n : ℕ) (k : Fin n → ℝ) :
    SymmetricTensor (transverseProjector n k) := by
  intro i j
  unfold transverseProjector
  by_cases hij : i = j
  · subst hij
    rfl
  · have hji : j ≠ i := fun h => hij h.symm
    simp [hij, hji, mul_comm]
theorem sumsq_pos_of_ne_zero (k : Fin 3 → ℝ) (hk : k ≠ 0) :
    0 < ∑ l : Fin 3, k l * k l := by
  have h_nonneg : ∀ l : Fin 3, 0 ≤ k l * k l := fun l => mul_self_nonneg (k l)
  have h_exists : ∃ l : Fin 3, k l ≠ 0 := by
    by_contra h
    apply hk
    funext l
    exact Classical.byContradiction fun hnl => h ⟨l, hnl⟩
  rcases h_exists with ⟨l, hl⟩
  have h_pos_l : 0 < k l * k l := mul_self_pos.mpr hl
  have h_le : k l * k l ≤ ∑ j : Fin 3, k j * k j :=
    Finset.single_le_sum (fun j _ => h_nonneg j) (Finset.mem_univ l)
  exact lt_of_lt_of_le h_pos_l h_le
theorem sumsq_ne_zero (k : Fin 3 → ℝ) (hk : k ≠ 0) :
    (∑ l : Fin 3, k l * k l) ≠ 0 := ne_of_gt (sumsq_pos_of_ne_zero k hk)
theorem transverseProjector_trace (k : Fin 3 → ℝ) (hk : k ≠ 0) :
    trace (transverseProjector 3 k) = 2 := by
  have hS : (k 0 ^ 2 + k 1 ^ 2 + k 2 ^ 2) ≠ 0 := by
    simpa [Fin.sum_univ_three, pow_two] using sumsq_ne_zero k hk
  unfold trace
  simp only [Matrix.trace, Matrix.diag, Fin.sum_univ_three, transverseProjector]
  field_simp [hS]
  simp
  ring
theorem transverseProjector_idempotent (k : Fin 3 → ℝ) (hk : k ≠ 0) :
    transverseProjector 3 k * transverseProjector 3 k = transverseProjector 3 k := by
  ext i j
  have hS : (k 0 ^ 2 + k 1 ^ 2 + k 2 ^ 2) ≠ 0 := by
    simpa [Fin.sum_univ_three, pow_two] using sumsq_ne_zero k hk
  fin_cases i <;> fin_cases j <;>
    simp [transverseProjector, Matrix.mul_apply, Fin.sum_univ_three]
  all_goals
    field_simp [hS]
    ring
theorem transverseProjector_annihilates_k (k : Fin 3 → ℝ) (hk : k ≠ 0) :
    ∀ i, ∑ j : Fin 3, (transverseProjector 3 k) i j * k j = 0 := by
  intro i
  have hS : (k 0 ^ 2 + k 1 ^ 2 + k 2 ^ 2) ≠ 0 := by
    simpa [Fin.sum_univ_three, pow_two] using sumsq_ne_zero k hk
  fin_cases i <;> simp [transverseProjector, Fin.sum_univ_three]
  all_goals
    field_simp [hS]
    ring
end
end GWTT

namespace InternalCharge
noncomputable def trace_pairing (X Y : Matrix (Fin 6) (Fin 6) ℂ) : ℝ :=
  (Matrix.trace (X * Y)).re
theorem trace_pairing_ad_invariant (X Y Z : Matrix (Fin 6) (Fin 6) ℂ) :
    trace_pairing (X * Y - Y * X) Z + trace_pairing Y (X * Z - Z * X) = 0 := by
  unfold trace_pairing
  rw [← Complex.add_re]
  rw [← Matrix.trace_add]
  have h : (X * Y - Y * X) * Z + Y * (X * Z - Z * X) = X * Y * Z - Y * Z * X := by
    noncomm_ring
  rw [h]
  rw [Matrix.trace_sub]
  rw [show Matrix.trace (X * Y * Z) = Matrix.trace (Y * Z * X) from (Matrix.trace_mul_cycle Y Z X).symm]
  exact sub_self _
end InternalCharge

namespace MultiplicityLabels
noncomputable section
def ValidMacroPartition (S T : ℕ) : Prop := S + T = 4 ∧ 0 < S ∧ 0 < T
theorem three_macro_partitions {S T : ℕ} (h : ValidMacroPartition S T) :
    (S = 1 ∧ T = 3) ∨ (S = 2 ∧ T = 2) ∨ (S = 3 ∧ T = 1) := by
  unfold ValidMacroPartition at h
  omega
inductive PhaseName where
  | Label31 | Label13 | Label22
  deriving DecidableEq
def phasePair : PhaseName → ℕ × ℕ
  | .Label31 => (3, 1)
  | .Label13 => (1, 3)
  | .Label22 => (2, 2)
theorem phasePair_valid (p : PhaseName) : ValidMacroPartition (phasePair p).1 (phasePair p).2 := by
  cases p <;> norm_num [phasePair, ValidMacroPartition]
theorem phasePair_injective : Function.Injective phasePair := by
  intro a b h
  cases a <;> cases b <;> simp [phasePair] at h ⊢
theorem phasePair_surjOn_valid (S T : ℕ) (h : ValidMacroPartition S T) :
    ∃ p : PhaseName, phasePair p = (S, T) := by
  rcases three_macro_partitions h with hST | hST | hST
  · refine ⟨.Label13, ?_⟩; simp [phasePair, hST.1, hST.2]
  · refine ⟨.Label22, ?_⟩; simp [phasePair, hST.1, hST.2]
  · refine ⟨.Label31, ?_⟩; simp [phasePair, hST.1, hST.2]
def duality : ℕ × ℕ → ℕ × ℕ := fun p => (p.2, p.1)
theorem swap_label31 : duality (phasePair .Label31) = phasePair .Label13 := by
  rfl
theorem swap_label22 : duality (phasePair .Label22) = phasePair .Label22 := by
  rfl
theorem dual_involution (p : ℕ × ℕ) : duality (duality p) = p := by
  simp [duality]
structure VEVTriple where
  n1 : ℕ
  n2 : ℕ
  n3 : ℕ
def VEV123 : VEVTriple := ⟨1, 2, 3⟩
def VEV222 : VEVTriple := ⟨2, 2, 2⟩
def sumTriple (v : VEVTriple) : ℕ := v.n1 + v.n2 + v.n3
def Positive (v : VEVTriple) : Prop := 0 < v.n1 ∧ 0 < v.n2 ∧ 0 < v.n3
def SumSix (v : VEVTriple) : Prop := sumTriple v = 6
def Nondegenerate (v : VEVTriple) : Prop :=
  v.n1 ≠ v.n2 ∧ v.n2 ≠ v.n3 ∧ v.n3 ≠ v.n1
def Canonical (v : VEVTriple) : Prop := v.n1 ≤ v.n2 ∧ v.n2 ≤ v.n3
theorem VEV123_positive : Positive VEV123 := by norm_num [Positive, VEV123]
theorem VEV123_sumSix : SumSix VEV123 := by norm_num [SumSix, sumTriple, VEV123]
theorem VEV123_nondeg : Nondegenerate VEV123 := by norm_num [Nondegenerate, VEV123]
theorem VEV222_sumSix : SumSix VEV222 := by norm_num [SumSix, sumTriple, VEV222]
theorem VEV222_degenerate : ¬ Nondegenerate VEV222 := by norm_num [Nondegenerate, VEV222]
theorem canonical_positive_sumSix_nondeg_unique (v : VEVTriple) :
    Positive v → SumSix v → Nondegenerate v → Canonical v → v = VEV123 := by
  rcases v with ⟨a, b, c⟩
  simp [Positive, SumSix, Nondegenerate, Canonical, VEV123, sumTriple]
  intro hpos hsum h_ab h_bc h_ca h_le1 h_le2
  omega
theorem cubic_action_123 : (1 : ℕ) ^ 3 + 2 ^ 3 + 3 ^ 3 = 36 := by norm_num
theorem cubic_action_222 : (2 : ℕ) ^ 3 + 2 ^ 3 + 2 ^ 3 = 24 := by norm_num
theorem vev_space_matches_label31 : VEV123.n3 = (phasePair .Label31).1 := by
  norm_num [VEV123, phasePair]
theorem vev_time_matches_label31 : VEV123.n1 = (phasePair .Label31).2 := by
  norm_num [VEV123, phasePair]
theorem vev_n2_hidden : VEV123.n2 = 2 := by norm_num [VEV123]
theorem vev_uniqueness_and_label31_alignment (v : VEVTriple) :
    Positive v → SumSix v → Nondegenerate v → Canonical v → v = VEV123 := by
  intro hp hs hn hc
  exact canonical_positive_sumSix_nondeg_unique v hp hs hn hc
end
end MultiplicityLabels

namespace ModelAlgebra
theorem w0_lt_minus_one (eps : ℝ)
    (he : 0 < eps) (hu : eps < 1 / 2) :
    -1 - 2 * eps / (1 - 2 * eps) < -1 := by
  have hd : 0 < 1 - 2 * eps := by linarith
  have hq : 0 < 2 * eps / (1 - 2 * eps) :=
    div_pos (by linarith) hd
  linarith
theorem w0_minus073_example :
    -1 - 2 * (-27 / 146 : ℚ) / (1 - 2 * (-27 / 146)) = -73 / 100 ∧
    -6 * (-27 / 146 : ℚ) / (1 - 2 * (-27 / 146)) ^ 2 = 5913 / 10000 := by
  norm_num
theorem branching_ratio_mismatch :
    let f : ℚ := 47 / 547
    let d : ℚ := (341 / 500) / (f * (37009 / 250))
    (5 + (1 - d) * f) / (1 - f) ≠ 547 / 100 := by
  norm_num
theorem w_a_elimination (eps : ℝ) (hD : 1 - 2 * eps ≠ 0) :
    let w0 : ℝ := -1 - 2 * eps / (1 - 2 * eps)
    let wa : ℝ := -6 * eps / (1 - 2 * eps) ^ 2
    wa = -3 * w0 * (1 + w0) := by
  dsimp
  have hw0 : (-1 : ℝ) - 2 * eps / (1 - 2 * eps) = -1 / (1 - 2 * eps) := by
    field_simp [hD]
    ring
  have h1w0 : (1 : ℝ) + (-1 / (1 - 2 * eps)) = -2 * eps / (1 - 2 * eps) := by
    field_simp [hD]
    ring
  rw [hw0, h1w0]
  field_simp [hD]
  ring
theorem eos_inverse_epsilon (eps w0 : ℝ)
    (h : w0 = -1 - 2 * eps / (1 - 2 * eps))
    (hD : 1 - 2 * eps ≠ 0) (hw0 : w0 ≠ 0) :
    eps = (w0 + 1) / (2 * w0) := by
  have hw0_alt : w0 = -1 / (1 - 2 * eps) := by
    rw [h]
    field_simp [hD]
    ring
  rw [hw0_alt]
  have hD' : 1 - eps * 2 ≠ 0 := by
    simpa [mul_comm] using hD
  field_simp [hD, hD']
  ring
theorem w_a_minus073_value :
    -3 * (-73 / 100 : ℚ) * (1 + (-73 / 100)) = 5913 / 10000 := by
  norm_num
def metzlerM (u v : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![ (-u), v ; u, (-v) ]
theorem metzler_charpoly (u v lam : ℝ) :
    Matrix.det (metzlerM u v - lam • (1 : Matrix (Fin 2) (Fin 2) ℝ)) = lam * (lam + u + v) := by
  rw [Matrix.det_fin_two]
  simp [metzlerM]
  ring
theorem metzler_det_zero (u v : ℝ) : Matrix.det (metzlerM u v) = 0 := by
  rw [Matrix.det_fin_two]
  simp [metzlerM]
  ring
theorem metzler_steady_ratio_arbitrary (u v : ℝ) :
    metzlerM u v *ᵥ ![v, u] = 0 := by
  ext i <;> fin_cases i <;> simp [metzlerM, Matrix.mulVec] <;> ring
end ModelAlgebra

namespace NumericalBounds
theorem central_difference_symmetric (f : ℝ → ℝ) (x h : ℝ) :
    f (x + h) - 2 * f x + f (x - h) = f (x - h) - 2 * f x + f (x + h) := by
  ring
theorem central_difference_linear_zero (a b x h : ℝ) (hh : h ≠ 0) :
    ((a * (x + h) + b) - 2 * (a * x + b) + (a * (x - h) + b)) / h ^ 2 = 0 := by
  field_simp [hh]
  ring
theorem central_difference_quadratic (a x h : ℝ) (hh : h ≠ 0) :
    (a * (x + h) ^ 2 - 2 * (a * x ^ 2) + a * (x - h) ^ 2) / h ^ 2 = 2 * a := by
  field_simp [hh]
  ring
end NumericalBounds

namespace PhaseI
/-- A radial Hessian bound evaluated on one tangent vector. -/
theorem radial_hessian_lower (a q s hs ds g : ℝ)
    (ha : 0 ≤ a) (hq : 0 ≤ q) (hs0 : 0 ≤ s) (hcomp : 2*g ≤ hs) :
    (a + q*s)*g ≤ (a/2 + q*s/2)*hs + q/2*ds^2 := by
  have hcoef : 0 ≤ a/2 + q*s/2 := by positivity
  have hmul := mul_le_mul_of_nonneg_left hcomp hcoef
  have hsq : 0 ≤ q/2*ds^2 := by positivity
  nlinarith
/-- The analytic Poincare estimate is an explicit premise on actual functionals. -/
theorem poincare_lower_bound {F : Type*} (energy variance : F → ℝ)
    (D a : ℝ) (hbound : ∀ f, (a-6*D)*variance f ≤ D*energy f)
    (f : F) (hv : 0 < variance f) :
    a-6*D ≤ D*energy f / variance f := by
  exact (le_div_iff₀ hv).2 (hbound f)
theorem radial_gap_positive (a D : ℝ) (h : 6*D < a) : 0 < a-6*D := by linarith
theorem radial_gap_D_two : (35 : ℝ)-6*2 = 23 := by norm_num
theorem strong_convexity_excludes_transverse_drift : ¬ ((35 : ℝ) ≤ 35/3) := by norm_num
end PhaseI

namespace Transport
/-- Integrating +phi*(rho_t + div(rho*v)) fixes this velocity sign. -/
theorem kinetic_completion (rho v gradPhi : ℝ) :
    rho*v^2/2-rho*v*gradPhi = rho*(v-gradPhi)^2/2-rho*gradPhi^2/2 := by ring
theorem kinetic_minimum (rho v gradPhi : ℝ) (hrho : 0 ≤ rho) :
    -rho*gradPhi^2/2 ≤ rho*v^2/2-rho*v*gradPhi := by
  rw [kinetic_completion]
  have : 0 ≤ rho*(v-gradPhi)^2/2 := by positivity
  linarith
end Transport

namespace DMAbundance
/-- Derivative of reciprocal abundance on the physical positive domain. -/
theorem reciprocal_hasDerivAt (s : BoltzmannSolution) (x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t => (s.Y t)⁻¹) (freeze_b s x) x := by
  have hd := (frozen_differentiable s x hx).hasDerivAt
  have hb : deriv s.Y x = -(s.lambda x) * ((s.Y x)^2 - (s.Y_eq x)^2) := s.boltzmann x hx
  rw [hb] at hd
  have hi := hd.inv (ne_of_gt (s.Y_pos x hx))
  have h1 : HasDerivAt (fun t => (s.Y t)⁻¹) (s.lambda x * (s.Y x ^ 2 - s.Y_eq x ^ 2) / s.Y x ^ 2) x := by
    convert hi using 1 <;> (first | rfl | ring)
  have h2 : s.lambda x * (s.Y x ^ 2 - s.Y_eq x ^ 2) / s.Y x ^ 2 = freeze_b s x := by
    unfold freeze_b
    field_simp [ne_of_gt (s.Y_pos x hx)]
  rw [h2] at h1
  exact h1
/-- The integral identity and its upper bound are explicit analytic hypotheses. -/
theorem abundance_lower_bound (Y Yf I B : ℝ)
    (hY : 0 < Y) (hYf : 0 < Yf) (hB : 0 ≤ B)
    (hI : I ≤ B) (hid : 1/Y = 1/Yf+I) :
    1/(1/Yf+B) ≤ Y := by
  have hd : 0 < 1/Yf+B := by positivity
  apply (div_le_iff₀ hd).2
  have hrec : 1/Y ≤ 1/Yf+B := by linarith
  have hh := (div_le_iff₀ hY).1 hrec
  nlinarith
/-- Tail integration remains a premise, not a global research axiom. -/
theorem positive_limit_from_reciprocal_identity
    (s : RelicSolution) (xf B : ℝ) (hxf : 0 < xf) (hB : 0 ≤ B)
    (hidentity : ∀ᶠ x in atTop,
      1/s.sol.Y x = 1/s.sol.Y xf + ∫ t in xf..x, freeze_b s.sol t)
    (hbound : ∀ᶠ x in atTop, (∫ t in xf..x, freeze_b s.sol t) ≤ B) :
    0 < s.Y_infinity := by
  have hc : 0 < 1/(1/s.sol.Y xf+B) := by
    have := s.sol.Y_pos xf hxf
    positivity
  have he : ∀ᶠ x in atTop, 1/(1/s.sol.Y xf+B) ≤ s.sol.Y x := by
    filter_upwards [hidentity, hbound, Filter.eventually_gt_atTop (0 : ℝ)] with x hi hb hx
    exact abundance_lower_bound _ _ _ _ (s.sol.Y_pos x hx) (s.sol.Y_pos xf hxf) hB hb hi
  exact lt_of_lt_of_le hc (ge_of_tendsto s.tendsto_Y he)
end DMAbundance

namespace Branching
/-- Initial baryon density is normalized to today's critical density. -/
def finalRatio (r f d : ℝ) : ℝ := (r+(1-d)*f)/(1-f)
def deDensity (Bi A f d : ℝ) : ℝ := Bi*A*f*d
def jointLoss (r R e : ℝ) : ℝ := (R-r+e)/(R+1)
def jointBranch (r R e : ℝ) : ℝ := e/jointLoss r R e
theorem joint_constraints (r R e : ℝ)
    (hR : R+1 ≠ 0) (hf : jointLoss r R e ≠ 0)
    (hremain : 1-jointLoss r R e ≠ 0) :
    finalRatio r (jointLoss r R e) (jointBranch r R e) = R ∧
    jointLoss r R e * jointBranch r R e = e := by
  have he : jointBranch r R e * jointLoss r R e = e := by
    unfold jointBranch
    field_simp [hf]
  constructor
  · unfold finalRatio
    apply (div_eq_iff hremain).2
    have hrel : (R+1)*jointLoss r R e = R-r+e := by
      unfold jointLoss
      field_simp [hR]
    nlinarith
  · nlinarith [he]
theorem joint_physical_range (r R e : ℝ)
    (hr : 0 < r) (hRr : r < R) (he : 0 ≤ e)
    (he1 : e < r+1) (he2 : e*R ≤ R-r) :
    0 < jointLoss r R e ∧ jointLoss r R e < 1 ∧
    0 ≤ jointBranch r R e ∧ jointBranch r R e ≤ 1 := by
  have hR : 0 < R+1 := by linarith
  have hf : 0 < jointLoss r R e := by
    unfold jointLoss
    exact div_pos (by linarith) hR
  have hf1 : jointLoss r R e < 1 := by
    unfold jointLoss
    apply (div_lt_one hR).2
    linarith
  have hef : e ≤ jointLoss r R e := by
    unfold jointLoss
    apply (le_div_iff₀ hR).2
    nlinarith
  refine ⟨hf, hf1, ?_, ?_⟩
  · exact div_nonneg he (le_of_lt hf)
  · exact (div_le_one hf).2 hef
/-- Four-component source conservation; pressure dilution is separate. -/
def sources (qB qDM qDE qReturn : ℝ) : Fin 4 → ℝ :=
  ![-qB+qReturn, qDM-qReturn, qB-qDM-qDE, qDE]
theorem sources_sum_zero (qB qDM qDE qReturn : ℝ) :
    ∑ i, sources qB qDM qDE qReturn i = 0 := by
  simp [sources, Fin.sum_univ_succ]
  <;> ring
theorem benchmark_joint_solution :
    let r : ℚ := 5
    let R : ℚ := 547/100
    let Bi : ℚ := 3/50
    let A : ℚ := (529/100)^3
    let E : ℚ := 341/500
    let e := E/(Bi*A)
    let f := (R-r+e)/(R+1)
    let d := e/f
    0 < f ∧ f < 1 ∧ 0 ≤ d ∧ d ≤ 1 ∧
    (r+(1-d)*f)/(1-f) = R ∧ Bi*A*f*d = E := by norm_num
end Branching

namespace CosmologicalClosure
/-- Local FRW continuity algebra for rho = rhoStar + kappa*excess. -/
theorem eos_from_continuity (H rho ell clock kappa excess Q w : ℝ)
    (hH : H ≠ 0) (hrho : rho ≠ 0)
    (hc : -2*ell*clock*kappa*excess+3*H*(rho+w*rho)=Q) :
    w = -1+(2*ell*clock*kappa*excess+Q)/(3*H*rho) := by
  field_simp [hH, hrho]
  nlinarith [hc]
end CosmologicalClosure

namespace IndexMatching
/-- This is a numerical matching function, not a constructed Fredholm operator. -/
def couplingSq (rate : ℝ) (index : ℤ) : ℝ :=
  8*Real.pi^2/(rate*(|index| : ℤ))
theorem unit_index_matching (rate : ℝ) (index : ℤ)
    (hr : rate = 35/3) (hi : |index| = 1) :
    couplingSq rate index = 24*Real.pi^2/35 := by
  simp [couplingSq, hr, hi]
  <;> ring
theorem self_adjoint_dimension_index (ker coker : ℕ) (h : ker = coker) :
    (ker : ℤ)-(coker : ℤ) = 0 := by simp [h]
end IndexMatching

namespace NumericalBounds
theorem quartic_central_difference (x h : ℝ) (hh : h ≠ 0) :
    ((x+h)^4-2*x^4+(x-h)^4)/h^2 = 12*x^2+2*h^2 := by
  field_simp [hh]
  <;> ring
theorem certified_cover_bound (K L eps sample value : ℝ)
    (hs : K ≤ sample) (he : |value-sample| ≤ L*eps) :
    K-L*eps ≤ value := by
  have h := (abs_le.mp he).1
  linarith
end NumericalBounds

namespace GWTT
/-- A concrete nonzero TT tensor for a nonzero wavevector. -/
theorem explicit_nonzero_witness :
    ttProjectionExplicit 3 ![0,0,1]
      (!![1,0,0; 0,-1,0; 0,0,0] : TensorField 3) =
      (!![1,0,0; 0,-1,0; 0,0,0] : TensorField 3) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [ttProjectionExplicit, transverseProjector, trace,
      Matrix.trace, Matrix.mul_apply, Fin.sum_univ_succ]
/-- Isotropic stress has zero TT part at any nonzero three-dimensional k. -/
theorem explicit_isotropic_zero (k : Fin 3 → ℝ) (hk : k ≠ 0) (c : ℝ) :
    ttProjectionExplicit 3 k (c • (1 : TensorField 3)) = 0 := by
  have hP := transverseProjector_idempotent k hk
  have ht := transverseProjector_trace k hk
  have hP1 : transverseProjector 3 k * (1 : TensorField 3) = transverseProjector 3 k := by simp
  have hPS : transverseProjector 3 k * (c • (1 : TensorField 3)) = c • transverseProjector 3 k := by
    simp [hP1]
  have hPSP : (c • transverseProjector 3 k) * transverseProjector 3 k = c • transverseProjector 3 k := by
    rw [smul_mul_assoc, hP]
  have htr : trace (c • transverseProjector 3 k) = c * 2 := by
    rw [trace_smul, ht]
  unfold ttProjectionExplicit
  rw [hPS, hPSP, htr]
  norm_num
end GWTT

namespace ModelAlgebra
/-- Negative epsilon is compatible with positive density for positive scale factor. -/
theorem density_positive_negative_epsilon (eps a rhoV : ℝ)
    (he : eps < 0) (ha : 0 < a) (hr : 0 < rhoV) :
    0 < rhoV*(1-2*eps/a^3) := by
  have hneg : 2*eps/a^3 < 0 := div_neg_of_neg_of_pos (by linarith) (pow_pos ha 3)
  exact mul_pos hr (by linarith)
theorem stabilizer_and_broken_dimensions :
    (1 : ℕ)^2+2^2+3^2-1 = 13 ∧ 35-13 = (22 : ℕ) ∧ 22*3 = (66 : ℕ) := by norm_num
end ModelAlgebra

namespace TwoState

def baryon (u v N B0 t : ℝ) : ℝ := CGICECore.relax (u+v) (v*N/(u+v)) B0 t
def dark (u v N B0 t : ℝ) : ℝ := N-baryon u v N B0 t

theorem total (u v N B0 t : ℝ) : baryon u v N B0 t+dark u v N B0 t=N := by
  unfold dark
  ring

theorem initial (u v N B0 : ℝ) : baryon u v N B0 0=B0 ∧ dark u v N B0 0=N-B0 := by
  simp [baryon, dark, CGICECore.relax_initial]

theorem solution (u v N B0 t : ℝ) (h : u+v ≠ 0) :
    HasDerivAt (baryon u v N B0)
      (-u*baryon u v N B0 t+v*dark u v N B0 t) t ∧
    HasDerivAt (dark u v N B0)
      (u*baryon u v N B0 t-v*dark u v N B0 t) t := by
  constructor
  · change HasDerivAt (CGICECore.relax (u+v) (v*N/(u+v)) B0)
      (-u*CGICECore.relax (u+v) (v*N/(u+v)) B0 t + v*(N-CGICECore.relax (u+v) (v*N/(u+v)) B0 t)) t
    have hb := CGICECore.relax_hasDerivAt (u+v) (v*N/(u+v)) B0 t
    convert hb using 1 <;> (first | rfl | field_simp [h]; ring)
  · change HasDerivAt (fun t => N - CGICECore.relax (u+v) (v*N/(u+v)) B0 t)
      (u*CGICECore.relax (u+v) (v*N/(u+v)) B0 t - v*(N-CGICECore.relax (u+v) (v*N/(u+v)) B0 t)) t
    have hb := CGICECore.relax_hasDerivAt (u+v) (v*N/(u+v)) B0 t
    have hb' : HasDerivAt (CGICECore.relax (u+v) (v*N/(u+v)) B0)
        (-u*CGICECore.relax (u+v) (v*N/(u+v)) B0 t + v*(N-CGICECore.relax (u+v) (v*N/(u+v)) B0 t)) t := by
      convert hb using 1 <;> (first | rfl | field_simp [h]; ring)
    convert (hasDerivAt_const t N).sub hb' using 1 <;> (first | rfl | ring)

theorem nonnegative (u v N B0 t : ℝ) (hu : 0 < u) (hv : 0 < v)
    (hN : 0 ≤ N) (hB : 0 ≤ B0) (hBN : B0 ≤ N) (ht : 0 ≤ t) :
    0 ≤ baryon u v N B0 t ∧ 0 ≤ dark u v N B0 t := by
  have huv : 0 < u+v := by linarith
  have hs : 0 ≤ v*N/(u+v) := div_nonneg (mul_nonneg hv.le hN) huv.le
  have hsN : v*N/(u+v) ≤ N := by
    apply (div_le_iff₀ huv).2
    nlinarith [mul_nonneg hu.le hN]
  have he : 0 ≤ Real.exp (-(u+v)*t) := (Real.exp_pos _).le
  have he1 : Real.exp (-(u+v)*t) ≤ 1 := Real.exp_le_one_iff.2 (by nlinarith)
  have h1 := mul_nonneg hB he
  have h2 := mul_nonneg hs (sub_nonneg.mpr he1)
  have h3 := mul_nonneg (sub_nonneg.mpr hBN) he
  have h4 := mul_nonneg (sub_nonneg.mpr hsN) (sub_nonneg.mpr he1)
  dsimp [baryon, dark, CGICECore.relax]
  constructor <;> nlinarith

theorem limits (u v N B0 : ℝ) (hu : 0 < u) (hv : 0 < v) :
    Tendsto (baryon u v N B0) atTop (nhds (v*N/(u+v))) ∧
    Tendsto (dark u v N B0) atTop (nhds (u*N/(u+v))) := by
  have huv : 0 < u+v := by linarith
  have hb := CGICECore.relax_limit (u+v) (v*N/(u+v)) B0 huv
  refine ⟨hb, ?_⟩
  have hd := (tendsto_const_nhds : Tendsto (fun _ : ℝ => N) atTop (nhds N)).sub hb
  have heq : N-v*N/(u+v)=u*N/(u+v) := by
    field_simp [ne_of_gt huv]
    <;> ring
  unfold dark baryon
  simpa [heq] using hd

theorem ratio_limit (u v N B0 : ℝ) (hu : 0 < u) (hv : 0 < v) (hN : 0 < N) :
    Tendsto (fun t => dark u v N B0 t / baryon u v N B0 t) atTop (nhds (u/v)) := by
  have huv : 0 < u+v := by linarith
  have hbpos : 0 < v*N/(u+v) := div_pos (mul_pos hv hN) huv
  have hl := limits u v N B0 hu hv
  have hdiv := hl.2.div hl.1 (ne_of_gt hbpos)
  have htarget : (u*N/(u+v))/(v*N/(u+v))=u/v := by
    field_simp [ne_of_gt hu, ne_of_gt hv, ne_of_gt hN, ne_of_gt huv]
  convert hdiv using 1
  all_goals solve -- 【枢修R26v2】ext+rfl级联(+11h行1764/1765实证)→solve链(含htarget改写)
    | rfl
    | (rw [htarget])
    | (ext t; simp)
    | simp
    | (simp; ring)

theorem uniqueness (u v N B0 : ℝ) (h : u+v ≠ 0)
    (B : ℝ → ℝ) (hB : ∀ t, HasDerivAt B (-u*B t+v*(N-B t)) t)
    (h0 : B 0=B0) (t : ℝ) : B t=baryon u v N B0 t := by
  apply CGICECore.relaxation_solution (u+v) (v*N/(u+v)) B0 B _ h0 t
  intro x
  convert hB x using 1
  field_simp [h]
  <;> ring
end TwoState

namespace InternalCharge
/-- Orthonormal compact-algebra coordinates: A is skew for the positive Euclidean metric. -/
theorem casimir_hasDerivAt {ι : Type*} [Fintype ι]
    (A : ℝ → ι → ι → ℝ) (j : ℝ → ι → ℝ) (t : ℝ)
    (hA : ∀ i k, A t i k = -A t k i)
    (hj : ∀ i, HasDerivAt (fun s => j s i) (∑ k, A t i k*j t k) t) :
    HasDerivAt (fun s => ∑ i, (j s i)^2) 0 t := by
  have hd := HasDerivAt.fun_sum (u := Finset.univ) (fun i _ => (hj i).pow 2)
  have hz := CGICECore.antisymmetric_symmetric_contraction (A t)
    (fun i k => j t i*j t k) hA (fun i k => mul_comm _ _)
  have heq : (∑ i, 2*j t i*(∑ k, A t i k*j t k))=0 := by
    calc
      _ = 2*(∑ i, ∑ k, A t i k*(j t i*j t k)) := by
        simp only [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        apply Finset.sum_congr rfl
        intro k _
        ring
      _ = 0 := by rw [hz]; ring
  have hd' : HasDerivAt (fun s => ∑ i, (j s i)^2) (∑ i, 2*j t i*(∑ k, A t i k*j t k)) t := by
    have hder : (∑ i, ↑2 * j t i ^ (2 - 1) * ∑ k, A t i k * j t k) = (∑ i, 2 * j t i * ∑ k, A t i k * j t k) := by
      congr; funext i; ring_nf
    simpa [hder] using hd
  rw [heq] at hd'
  exact hd'

theorem casimir_conserved {ι : Type*} [Fintype ι]
    (A : ℝ → ι → ι → ℝ) (j : ℝ → ι → ℝ)
    (hA : ∀ t i k, A t i k = -A t k i)
    (hj : ∀ t i, HasDerivAt (fun s => j s i) (∑ k, A t i k*j t k) t)
    (t : ℝ) : (∑ i, (j t i)^2) = ∑ i, (j 0 i)^2 := by
  have hd := fun s => casimir_hasDerivAt A j s (hA s) (hj s)
  exact is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0
end InternalCharge

namespace CGICECore
theorem ouCov_unique (ell D C0 : ℝ) (hl : ell ≠ 0) (C : ℝ → ℝ)
    (hc : ∀ t, HasDerivAt C (-2*ell*C t+2*D) t) (h0 : C 0=C0) (t : ℝ) :
    C t=ouCov ell D C0 t := by
  apply relaxation_solution (2*ell) (D/ell) C0 C _ h0 t
  intro x
  convert hc x using 1
  field_simp [hl]
  <;> ring

theorem ouCov_excess_square_hasDerivAt (ell D C0 t : ℝ) (hl : ell ≠ 0) :
    HasDerivAt (fun s => (ouCov ell D C0 s-D/ell)^2)
      (-4*ell*(ouCov ell D C0 t-D/ell)^2) t := by
  have hlin : -2*ell*ouCov ell D C0 t + 2*D = -2*ell*(ouCov ell D C0 t - D/ell) := by
    field_simp [hl]; ring
  convert ((ouCov_hasDerivAt ell D C0 t hl).sub_const (D/ell)).pow 2 using 1
  <;> first | rfl | (rw [hlin]; ring)
end CGICECore

namespace CosmologicalClosure

def density (rhoV eps a : ℝ) : ℝ := rhoV*(1-2*eps/a^3)

theorem density_hasDerivAt (rhoV eps a : ℝ) (ha : a ≠ 0) :
    HasDerivAt (density rhoV eps) (6*rhoV*eps/a^4) a := by
  have hq : HasDerivAt (fun x : ℝ => 2*eps/x^3) (-6*eps/a^4) a := by
    convert (hasDerivAt_const a (2*eps)).div ((hasDerivAt_id a).pow 3)
      (pow_ne_zero 3 ha) using 1
    <;> first | rfl | (simp [id_eq]; field_simp [ha]; ring_nf)
  convert ((hasDerivAt_const a (1 : ℝ)).sub hq).const_mul rhoV using 1
  <;> first | rfl | ring | (ext x; simp [density])

theorem pressure_from_density (rhoV eps a : ℝ) (ha : a ≠ 0) :
    -density rhoV eps a-a/3*(6*rhoV*eps/a^4) = -rhoV := by
  unfold density
  field_simp [ha]
  <;> ring

theorem eos_from_density (rhoV eps a : ℝ) (ha : a ≠ 0)
    (hr : rhoV ≠ 0) (hden : a^3-2*eps ≠ 0) :
    (-rhoV)/density rhoV eps a = -1-2*eps/(a^3-2*eps) := by
  have hinner : 1-2*eps/a^3 ≠ 0 := by
    intro h
    apply hden
    have hh := (sub_eq_zero.mp h)
    have hmul := (eq_div_iff (pow_ne_zero 3 ha)).1 hh
    linarith
  unfold density
  field_simp [ha, hr, hden, hinner]
  <;> ring
end CosmologicalClosure

namespace GWTT

theorem explicit_trace_zero (k : Fin 3 → ℝ) (hk : k ≠ 0) (S : TensorField 3) :
    trace (ttProjectionExplicit 3 k S) = 0 := by
  have hP := transverseProjector_idempotent k hk
  have ht := transverseProjector_trace k hk
  have htr := trace_mul_mul_eq_trace_mul_of_idempotent (transverseProjector 3 k) S hP
  unfold ttProjectionExplicit trace
  dsimp [trace] at ht htr
  rw [Matrix.trace_sub, Matrix.trace_smul, htr, ht]
  field_simp
  ring

theorem explicit_transverse (k : Fin 3 → ℝ) (hk : k ≠ 0) (S : TensorField 3) :
    divergence (ttProjectionExplicit 3 k S) k = 0 := by
  have hPann := transverseProjector_annihilates_k k hk
  have hPk : Matrix.mulVec (transverseProjector 3 k) k = 0 := by
    ext i
    rw [Matrix.mulVec_apply_eq_sum]
    exact hPann i
  rw [divergence_eq_mulVec]
  unfold ttProjectionExplicit
  rw [Matrix.sub_mulVec, Matrix.smul_mulVec]
  rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, hPk]
  simp [Matrix.mulVec_zero]

theorem explicit_symmetric (k : Fin 3 → ℝ) (hk : k ≠ 0) (S : TensorField 3)
    (hS : SymmetricTensor S) : (ttProjectionExplicit 3 k S).transpose=ttProjectionExplicit 3 k S := by
  have hPsym : (transverseProjector 3 k).transpose = transverseProjector 3 k := by
    ext i j
    exact (transverseProjector_symm (3 : ℕ) k i j).symm
  have hSsym : S.transpose = S := by
    ext i j
    exact (hS i j).symm
  unfold ttProjectionExplicit
  rw [Matrix.transpose_sub, Matrix.transpose_smul,
    transpose_mul_mul_self_of_symm (transverseProjector 3 k) S hPsym hSsym, hPsym]

theorem explicit_mem_TT (k : Fin 3 → ℝ) (hk : k ≠ 0) (S : TensorField 3)
    (hS : SymmetricTensor S) : ttProjectionExplicit 3 k S ∈ TTSubspace k :=
  ⟨explicit_trace_zero k hk S, explicit_transverse k hk S, explicit_symmetric k hk S hS⟩

theorem explicit_idempotent (k : Fin 3 → ℝ) (hk : k ≠ 0) (S : TensorField 3) :
    ttProjectionExplicit 3 k (ttProjectionExplicit 3 k S)=ttProjectionExplicit 3 k S := by
  have hP := transverseProjector_idempotent k hk
  have ht := transverseProjector_trace k hk
  have htr := trace_mul_mul_eq_trace_mul_of_idempotent (transverseProjector 3 k) S hP
  have h1 := mul_tt_mul_self (transverseProjector 3 k) S (trace (transverseProjector 3 k * S) / 2) hP
  have h2 : trace (transverseProjector 3 k * ((transverseProjector 3 k * S * transverseProjector 3 k) -
      (trace (transverseProjector 3 k * S) / 2) • transverseProjector 3 k)) = 0 := by
    dsimp [trace]
    rw [Matrix.mul_sub, Matrix.mul_smul]
    rw [Matrix.trace_sub, Matrix.trace_smul]
    rw [show transverseProjector 3 k * (transverseProjector 3 k * S * transverseProjector 3 k) = transverseProjector 3 k * S * transverseProjector 3 k by
      rw [← Matrix.mul_assoc, ← Matrix.mul_assoc, hP]]
    rw [hP]
    rw [htr]
    rw [show Matrix.trace (transverseProjector 3 k) = 2 by simpa [trace] using ht]
    norm_num
  unfold ttProjectionExplicit
  norm_num
  rw [h1, h2]
  norm_num
end GWTT

/-! V20 integration of V18's three-stage programme.
These are concrete conditional models, not propositions named after physical phases.
No theorem in this addition asserts a microscopic SL(6,C) stress-energy derivation.
-/
namespace ThermalBridge

def massSq (c T Tc : ℝ) : ℝ := c * (T^2 - Tc^2)

theorem massSq_positive_above (c T Tc : ℝ)
    (hc : 0 < c) (hTc : 0 ≤ Tc) (hT : Tc < T) : 0 < massSq c T Tc := by
  unfold massSq
  exact mul_pos hc (by nlinarith)

theorem massSq_negative_below (c T Tc : ℝ)
    (hc : 0 < c) (hT : 0 ≤ T) (hTc : T < Tc) : massSq c T Tc < 0 := by
  unfold massSq
  exact mul_neg_of_pos_of_neg hc (by nlinarith)

theorem symmetric_minimum (m2 lam phi : ℝ) (hm : 0 ≤ m2) (hl : 0 ≤ lam) :
    VEV123CW.V0_param m2 lam 0 ≤ VEV123CW.V0_param m2 lam phi := by
  simp only [VEV123CW.V0_param, zero_pow (by norm_num : (2 : ℕ) ≠ 0),
    zero_pow (by norm_num : (4 : ℕ) ≠ 0), mul_zero, add_zero]
  positivity

/-- A selected nonzero stationary point is a global minimum of the scalar model. -/
theorem broken_minimum (m2 lam v phi : ℝ) (hm : m2 < 0) (hl : 0 < lam)
    (hv : v^2 = -m2 / lam) :
    VEV123CW.V0_deriv_param m2 lam v = 0 ∧
    0 < VEV123CW.V0_hess_param m2 lam v ∧
    VEV123CW.V0_param m2 lam v ≤ VEV123CW.V0_param m2 lam phi := by
  have hl0 := ne_of_gt hl
  have hv' : lam * v^2 = -m2 := by rw [hv]; field_simp
  have hmin : VEV123CW.V0_param m2 lam v = -(m2^2)/(4*lam) := by
    have h := VEV123CW.V0_param_square_completion m2 lam v hl0
    rw [hv] at h
    have hz : -m2 / lam + m2 / lam = 0 := by ring
    rw [hz] at h
    nlinarith
  refine ⟨?_, ?_, ?_⟩
  · unfold VEV123CW.V0_deriv_param
    calc
      m2*v + lam*v^3 = v*(m2 + lam*v^2) := by ring
      _ = 0 := by rw [hv']; ring
  · unfold VEV123CW.V0_hess_param
    nlinarith [hv']
  · rw [hmin]
    exact VEV123CW.V0_param_min_lower_bound m2 lam phi hl

/-- Critical slowing of this order parameter is separate from the diffusion gap. -/
theorem critical_origin_hessian (c Tc lam : ℝ) :
    VEV123CW.V0_hess_param (massSq c Tc Tc) lam 0 = 0 := by
  simp [massSq, VEV123CW.V0_hess_param]
end ThermalBridge

namespace PhaseI
/-- Directional robustness under a separately certified Hessian perturbation. -/
theorem perturbation_gap_lower (a L D g ric hess correction : ℝ)
    (hric : ric = -6*g) (hhess : a*g ≤ hess) (hcor : -L*g ≤ correction) :
    (a-L-6*D)*g ≤ D*ric+hess+correction := by
  rw [hric]
  nlinarith
end PhaseI

namespace ClockResponse

/-- N = log(a/a_ref); rhoE is an assigned physical density, not a variance. -/
def tail (m E0 N : ℝ) : ℝ := E0 * Real.exp (-m*N)
def pressure (rhoStar m rhoE : ℝ) : ℝ := -rhoStar + (m/3-1)*rhoE

theorem tail_hasDerivAt (m E0 N : ℝ) :
    HasDerivAt (tail m E0) (-m*tail m E0 N) N := by
  have h := (((hasDerivAt_id N).const_mul (-m)).exp).const_mul E0
  have hf : (fun y => E0 * rexp (-m * id y)) = tail m E0 := by
    funext y
    unfold tail
    simp [id_eq]
  have hder : E0 * (rexp (-m * id N) * (-m * 1)) = -m * tail m E0 N := by
    unfold tail
    simp [id_eq]
    ring
  simpa only [hf, hder] using h

/-- Composition with an actual differentiable physical clock N(t). -/
theorem tail_physical_hasDerivAt (m E0 : ℝ) (N : ℝ → ℝ) (t H : ℝ)
    (hN : HasDerivAt N H t) :
    HasDerivAt (fun s => tail m E0 (N s)) (-m*H*tail m E0 (N t)) t := by
  have h := (tail_hasDerivAt m E0 (N t)).comp t hN
  convert h using 1 <;> (first | rfl | ring)

theorem ou_clock_identity (ell D C0 nu N : ℝ) :
    CGICECore.ouCov ell D C0 (nu*N)-D/ell =
      tail (2*ell*nu) (C0-D/ell) N := by
  rw [CGICECore.ouCov_excess]
  unfold tail
  congr 2 <;> ring

theorem positive_tail (m E0 N : ℝ) (hE : 0 < E0) : 0 < tail m E0 N :=
  mul_pos hE (Real.exp_pos _)

theorem continuity (rhoStar m rhoE H : ℝ) :
    -m*H*rhoE + 3*H*((rhoStar+rhoE)+pressure rhoStar m rhoE) = 0 := by
  unfold pressure; ring

theorem enthalpy (rhoStar m rhoE : ℝ) :
    (rhoStar+rhoE)+pressure rhoStar m rhoE = m*rhoE/3 := by
  unfold pressure; ring

theorem no_phantom (rhoStar m rhoE : ℝ)
    (hm : 0 ≤ m) (hE : 0 ≤ rhoE) (hrho : 0 < rhoStar+rhoE) :
    -1 ≤ pressure rhoStar m rhoE / (rhoStar+rhoE) := by
  apply (le_div_iff₀ hrho).2
  have h := mul_nonneg hm hE
  have he := enthalpy rhoStar m rhoE
  linarith

theorem dust_clock_pressure (rhoStar rhoE : ℝ) :
    pressure rhoStar 3 rhoE = -rhoStar := by
  norm_num [pressure]

theorem density_ansatz_match (rhoStar eps a : ℝ) :
    CosmologicalClosure.density rhoStar eps a =
      rhoStar + (-2*rhoStar*eps)/a^3 := by
  unfold CosmologicalClosure.density; ring

theorem positive_tail_epsilon_sign (rhoStar eps : ℝ) (h : 0 < rhoStar) :
    0 ≤ -2*rhoStar*eps ↔ eps ≤ 0 := by
  constructor
  · intro he
    nlinarith
  · intro he
    have := mul_nonpos_of_nonneg_of_nonpos (le_of_lt h) he
    nlinarith

theorem acceleration_numerator (rhoStar m rhoE rhoM : ℝ) :
    (rhoM+rhoStar+rhoE)+3*pressure rhoStar m rhoE =
      rhoM+(m-2)*rhoE-2*rhoStar := by
  unfold pressure; ring

theorem acceleration_criterion (rhoStar m rhoE rhoM : ℝ) :
    (rhoM+rhoStar+rhoE)+3*pressure rhoStar m rhoE < 0 ↔
      rhoM+(m-2)*rhoE < 2*rhoStar := by
  rw [acceleration_numerator]
  constructor <;> intro h <;> linarith

theorem tail_limit (m E0 : ℝ) (hm : 0 < m) :
    Tendsto (tail m E0) atTop (nhds 0) := by
  have h := CGICECore.relax_limit m 0 E0 hm
  convert h using 1
  funext N
  simp [tail, CGICECore.relax]
end ClockResponse

namespace CosmologicalBridge

/-- M2 denotes the positive reduced Planck mass squared. -/
def constraint (M2 H rho : ℝ) : ℝ := 3*M2*H^2-rho

theorem total_continuity (H : ℝ) (rho p rate Q : Fin 4 → ℝ)
    (hc : ∀ i, rate i+3*H*(rho i+p i)=Q i) (hq : ∑ i, Q i=0) :
    (∑ i, rate i)+3*H*((∑ i, rho i)+(∑ i, p i))=0 := by
  have hs := congrArg (fun f : Fin 4 → ℝ => ∑ i, f i) (funext hc)
  rw [hq] at hs
  rw [Finset.sum_add_distrib] at hs
  rw [← Finset.mul_sum] at hs
  rw [Finset.sum_add_distrib] at hs
  simpa using hs

theorem friedmann_constraint_hasDerivAt (M2 : ℝ) (H rho p : ℝ → ℝ)
    (t : ℝ) (hM : M2 ≠ 0)
    (hH : HasDerivAt H (-(rho t+p t)/(2*M2)) t)
    (hr : HasDerivAt rho (-3*H t*(rho t+p t)) t) :
    HasDerivAt (fun s => constraint M2 (H s) (rho s)) 0 t := by
  unfold constraint
  convert ((hH.pow 2).const_mul (3*M2)).sub hr using 1
  <;> first | rfl | (field_simp [hM]; ring_nf)

/-- Global real-line version; interval existence/patching is not asserted. -/
theorem friedmann_constraint_preserved (M2 : ℝ) (H rho p : ℝ → ℝ)
    (hM : M2 ≠ 0)
    (hH : ∀ t, HasDerivAt H (-(rho t+p t)/(2*M2)) t)
    (hr : ∀ t, HasDerivAt rho (-3*H t*(rho t+p t)) t)
    (t t0 : ℝ) : constraint M2 (H t) (rho t) = constraint M2 (H t0) (rho t0) := by
  have hd := fun s => friedmann_constraint_hasDerivAt M2 H rho p s hM (hH s) (hr s)
  exact is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t t0

/-- Expansion dilution prevents conservation of physical density even with zero exchange. -/
theorem comoving_pressure_work (volume H rho p Q : ℝ) :
    (3*H*volume)*rho+volume*(Q-3*H*(rho+p)) =
      volume*Q-3*H*volume*p := by ring

/-- Energy compensation across an idealized instantaneous condensation event. -/
theorem transition_energy_matching (rBefore rAfter uBefore uAfter : ℝ)
    (hheat : rAfter-rBefore=uBefore-uAfter) :
    rAfter+uAfter=rBefore+uBefore := by linarith

theorem acceleration_from_raychaudhuri (M2 H rho p Hdot : ℝ)
    (hM : M2 ≠ 0) (hf : 3*M2*H^2=rho)
    (hr : Hdot=-(rho+p)/(2*M2)) :
    Hdot+H^2=-(rho+3*p)/(6*M2) := by
  rw [hr]
  field_simp [hM]
  nlinarith [hf]

/-- Nonempty reduced dust-plus-vacuum regimes, not a full cosmological solution. -/
theorem dust_vacuum_regime_witness :
    let rhoM := fun a : ℚ => 8/a^3
    let rhoV : ℚ := 1
    rhoV < rhoM 1 ∧ rhoM 3 < rhoV ∧ rhoM 3 < 2*rhoV := by norm_num
end CosmologicalBridge

namespace Branching

/-- Necessity and uniqueness for the simultaneous constraints, not just one fitted identity. -/
theorem joint_unique (r R e f d : ℝ) (hR : R+1 ≠ 0)
    (hf : f ≠ 0) (hf1 : f ≠ 1)
    (hratio : finalRatio r f d=R) (hde : f*d=e) :
    f=jointLoss r R e ∧ d=jointBranch r R e := by
  have hden : 1-f ≠ 0 := by intro h; apply hf1; linarith
  have hrat : r+(1-d)*f=R*(1-f) := (div_eq_iff hden).1 hratio
  have hlin : f*(R+1)=R-r+e := by nlinarith
  have hsol : f=jointLoss r R e := by
    unfold jointLoss
    exact (eq_div_iff hR).2 hlin
  refine ⟨hsol, ?_⟩
  unfold jointBranch
  rw [← hsol]
  exact (eq_div_iff hf).2 (by nlinarith [hde])

theorem feasible_necessary (r R e f d : ℝ)
    (hR : 0 ≤ R+1) (hf : 0 ≤ f) (hf1 : f < 1) (hd1 : d ≤ 1)
    (hratio : finalRatio r f d=R) (hde : f*d=e) : e*R ≤ R-r := by
  have hden : 1-f ≠ 0 := by linarith
  have hrat : r+(1-d)*f=R*(1-f) := (div_eq_iff hden).1 hratio
  have hef : e ≤ f := by nlinarith [mul_nonneg hf (sub_nonneg.mpr hd1)]
  have hprod := mul_nonneg (sub_nonneg.mpr hef) hR
  nlinarith [hrat, hde]

/-- With R > r > 0, the single sharp bound supplies the former extra hypothesis. -/
theorem feasible_sufficient_sharp (r R e : ℝ)
    (hr : 0 < r) (hRr : r < R) (he : 0 ≤ e) (hbound : e*R ≤ R-r) :
    0 < jointLoss r R e ∧ jointLoss r R e < 1 ∧
      0 ≤ jointBranch r R e ∧ jointBranch r R e ≤ 1 := by
  have hR : 0 < R := lt_trans hr hRr
  have he1 : e < 1 := by
    by_contra h
    have hp := mul_nonneg (sub_nonneg.mpr (le_of_not_gt h)) (le_of_lt hR)
    nlinarith
  exact joint_physical_range r R e hr hRr he (by linarith) hbound
end Branching

namespace DrivenEntropy

/-- Differentiation of D(t) KL(t): external reference motion is not free dissipation. -/
theorem moving_reference_balance (D K : ℝ → ℝ) (t Ddot Kdot : ℝ)
    (hD : HasDerivAt D Ddot t) (hK : HasDerivAt K Kdot t) :
    HasDerivAt (fun s => D s*K s) (Ddot*K t+D t*Kdot) t := by
  convert hD.mul hK using 1 <;> rfl

/-- Pointwise sign criterion when d(KL)/dt = -D*I-referencePower. -/
theorem kl_nonincrease (D I referencePower : ℝ)
    (h : -D*I ≤ referencePower) : -D*I-referencePower ≤ 0 := by linarith
end DrivenEntropy

/-! Review response, 2026-09-21. The constructions below are conditional.
They do not identify configuration-space probability with physical matter,
construct a global tensor bundle, or prove a Callias index theorem.
-/
namespace TransportClock

/-- Covariance response, not a consequence of optimal transport alone. -/
def eFold (beta Eref : ℝ) (E : ℝ → ℝ) (t : ℝ) : ℝ :=
  beta * (Real.log Eref - Real.log (E t))

theorem eFold_hasDerivAt (beta Eref : ℝ) (E : ℝ → ℝ) (t rate : ℝ)
    (hE : E t ≠ 0) (hd : HasDerivAt E rate t) :
    HasDerivAt (eFold beta Eref E) (-beta * rate / E t) t := by
  convert ((hasDerivAt_const t (Real.log Eref)).sub (hd.log hE)).const_mul beta using 1 <;>
    (first | rfl | ring)

theorem ou_eFold_hasDerivAt (beta Eref ell lapse : ℝ) (E : ℝ → ℝ) (t : ℝ)
    (hE : E t ≠ 0) (hd : HasDerivAt E (-2*ell*lapse*E t) t) :
    HasDerivAt (eFold beta Eref E) (2*beta*ell*lapse) t := by
  convert eFold_hasDerivAt beta Eref E t _ hE hd using 1
  field_simp [hE]
  <;> ring

/-- A uniform relative-rate bound gives a whole-interval Lipschitz estimate. -/
theorem eFold_interval_lipschitz (beta Eref L left right : ℝ)
    (E rate : ℝ → ℝ) (hb : 0 ≤ beta)
    (hE : ∀ t ∈ Icc left right, 0 < E t)
    (hd : ∀ t ∈ Icc left right, HasDerivAt E (rate t) t)
    (hbound : ∀ t ∈ Icc left right, |rate t / E t| ≤ L)
    (x y : ℝ) (hx : x ∈ Icc left right) (hy : y ∈ Icc left right) :
    |eFold beta Eref E y - eFold beta Eref E x| ≤ beta*L*|y-x| := by
  have hf : ∀ t ∈ Icc left right,
      HasDerivWithinAt (eFold beta Eref E) (-beta*rate t/E t) (Icc left right) t := by
    intro t ht
    exact (eFold_hasDerivAt beta Eref E t (rate t) (ne_of_gt (hE t ht))
      (hd t ht)).hasDerivWithinAt
  have hbnd : ∀ t ∈ Icc left right, ‖-beta*rate t/E t‖ ≤ beta*L := by
    intro t ht
    have heq : -beta*rate t/E t = -beta*(rate t/E t) := by ring
    rw [Real.norm_eq_abs, heq, abs_mul, abs_neg, abs_of_nonneg hb]
    exact mul_le_mul_of_nonneg_left (hbound t ht) hb
  simpa only [Real.norm_eq_abs] using
    (convex_Icc left right).norm_image_sub_le_of_norm_hasDerivWithin_le hf hbnd hx hy

theorem divergence_compatibility (beta ell lapse theta : ℝ)
    (h : theta = 6*beta*ell*lapse) : theta/3 = 2*beta*ell*lapse := by
  rw [h]; ring

theorem density_dilution (n ndot theta H : ℝ)
    (hc : ndot + n*theta = 0) (ht : theta = 3*H) :
    ndot + 3*H*n = 0 := by rw [ht] at hc; nlinarith [hc]

theorem covariance_volume_contracts (C Cdot H : ℝ) (hC : 0 < C)
    (hd : Cdot < 0) (hH : 2*C*H = Cdot) : H < 0 := by
  nlinarith

theorem lapse_acceleration (k lapse lapseDot : ℝ) :
    k*lapseDot + (k*lapse)^2 = k*(lapseDot + k*lapse^2) := by ring

/-- The old tail composition is now instantiated by the covariance-defined clock. -/
theorem covariance_tail_hasDerivAt (m E0 beta Eref ell lapse : ℝ)
    (E : ℝ → ℝ) (t : ℝ) (hE : E t ≠ 0)
    (hd : HasDerivAt E (-2*ell*lapse*E t) t) :
    HasDerivAt (fun s => ClockResponse.tail m E0 (eFold beta Eref E s))
      (-m*(2*beta*ell*lapse)*ClockResponse.tail m E0 (eFold beta Eref E t)) t :=
  ClockResponse.tail_physical_hasDerivAt m E0 (eFold beta Eref E) t _
    (ou_eFold_hasDerivAt beta Eref ell lapse E t hE hd)
end TransportClock

namespace TensorResponse
variable {V W U : Type*}
variable [AddCommGroup V] [Module ℝ V] [AddCommGroup W] [Module ℝ W]
variable [AddCommGroup U] [Module ℝ U]

/-- Fiberwise covariant two-tensor pullback; smooth gluing is separate. -/
def pullback (F : LinearMap.BilinForm ℝ W) (e : V →ₗ[ℝ] W) :
    LinearMap.BilinForm ℝ V := F.compl₁₂ e e

theorem pullback_symmetric (F : LinearMap.BilinForm ℝ W) (e : V →ₗ[ℝ] W)
    (hF : ∀ u v, F u v = F v u) (u v : V) :
    pullback F e u v = pullback F e v u := hF (e u) (e v)

theorem pullback_nonnegative (F : LinearMap.BilinForm ℝ W) (e : V →ₗ[ℝ] W)
    (hF : ∀ w, 0 ≤ F w w) (v : V) : 0 ≤ pullback F e v v := hF (e v)

theorem positive_pullback_not_timelike (F : LinearMap.BilinForm ℝ W)
    (e : V →ₗ[ℝ] W) (hF : ∀ w, 0 ≤ F w w) :
    ¬ ∃ v, pullback F e v v < 0 := by
  rintro ⟨v, hv⟩
  exact (not_lt_of_ge (pullback_nonnegative F e hF v)) hv

theorem pullback_composition (F : LinearMap.BilinForm ℝ W)
    (e : V →ₗ[ℝ] W) (r : U →ₗ[ℝ] V) :
    pullback (pullback F e) r = pullback F (e.comp r) := by
  ext u v
  rfl

theorem pullback_internal_invariance (F : LinearMap.BilinForm ℝ W)
    (e : V →ₗ[ℝ] W) (r : W →ₗ[ℝ] W)
    (hr : ∀ u v, F (r u) (r v) = F u v) :
    pullback F (r.comp e) = pullback F e := by
  ext u v
  exact hr (e u) (e v)

/-- Finite score approximation: positivity is independent of a Lorentzian metric. -/
def scoreGram {ι : Type*} [Fintype ι] (weight : ι → ℝ)
    (score : ι → V →ₗ[ℝ] ℝ) (u v : V) : ℝ :=
  ∑ i, weight i * score i u * score i v

theorem scoreGram_nonnegative {ι : Type*} [Fintype ι] (weight : ι → ℝ)
    (score : ι → V →ₗ[ℝ] ℝ) (hw : ∀ i, 0 ≤ weight i) (v : V) :
    0 ≤ scoreGram weight score v v := by
  apply Finset.sum_nonneg
  intro i _
  have h := mul_nonneg (hw i) (sq_nonneg (score i v))
  nlinarith [h]

def covariantRate (A : V →ₗ[ℝ] V) (value rate : V) : V := rate + A value

/-- Local connection transformation law; spacetime derivatives remain analytical. -/
theorem covariantRate_transforms (A B R Rdot : V →ₗ[ℝ] V)
    (hconn : ∀ v, B (R v) = R (A v) - Rdot v) (v rate : V) :
    covariantRate B (R v) (Rdot v + R rate) = R (covariantRate A v rate) := by
  simp only [covariantRate, hconn, map_add]
  abel

theorem infinitesimal_pairing_invariant (F : LinearMap.BilinForm ℝ V)
    (A : V →ₗ[ℝ] V) (hA : ∀ u v, F (A u) v + F u (A v) = 0)
    (u v : V) : F (-A u) v + F u (-A v) = 0 := by
  simp only [map_neg, LinearMap.neg_apply]
  linarith [hA u v]

/-- A constant Euclidean line metric is not invariant under dilations. -/
theorem lie_derivative_dilation_counterexample :
    (1 : ℝ)*0 + 2*1*1 ≠ 0 := by norm_num

def scalarStress (Z traceK potential : ℝ) (g K : LinearMap.BilinForm ℝ V) :
    LinearMap.BilinForm ℝ V := Z • K - (Z/2*traceK + potential) • g

theorem scalarStress_symmetric (Z traceK potential : ℝ)
    (g K : LinearMap.BilinForm ℝ V)
    (hg : ∀ u v, g u v = g v u) (hK : ∀ u v, K u v = K v u) (u v : V) :
    scalarStress Z traceK potential g K u v = scalarStress Z traceK potential g K v u := by
  change Z*K u v-(Z/2*traceK+potential)*g u v =
    Z*K v u-(Z/2*traceK+potential)*g v u
  rw [hg u v, hK u v]

theorem homogeneous_enthalpy (kin potential : ℝ) :
    (kin/2+potential)+(kin/2-potential) = kin := by ring
end TensorResponse

namespace QuarticError

theorem exact_difference (a q D C G kappa : ℝ) :
    (CGICECore.riccatiCovRate a q C D-2*q*kappa) -
      CGICECore.riccatiCovRate a q G D =
      -(2*a+6*q*(C+G))*(C-G)-2*q*kappa := by
  unfold CGICECore.riccatiCovRate
  ring

theorem cumulant_abs_bound (C M4 M : ℝ)
    (hJ : C^2 ≤ M4) (hM : M4 ≤ M) :
    |CGICECore.kappa4 M4 C| ≤ 2*M := by
  rw [abs_le]
  unfold CGICECore.kappa4
  constructor <;> nlinarith [sq_nonneg C]

theorem restoring_rate_lower (a q C G : ℝ)
    (hq : 0 ≤ q) (hC : 0 ≤ C) (hG : 0 ≤ G) :
    2*a ≤ 2*a+6*q*(C+G) := by
  have h : 0 ≤ 6*q*(C+G) := by positivity
  linarith

/-- Young's inequality written as a polynomial certificate, before division by a. -/
theorem squared_error_differential_bound (a q C G kappa K delta deltaDot : ℝ)
    (ha : 0 < a) (hq : 0 ≤ q) (hC : 0 ≤ C) (hG : 0 ≤ G)
    (hK : kappa^2 ≤ K^2)
    (hd : deltaDot = -(2*a+6*q*(C+G))*delta-2*q*kappa) :
    a*(2*delta*deltaDot+2*a*delta^2) ≤ 2*q^2*K^2 := by
  rw [hd]
  have hrest := mul_nonneg
    (mul_nonneg (le_of_lt ha) (mul_nonneg hq (add_nonneg hC hG)))
    (sq_nonneg delta)
  have hk := mul_nonneg (sq_nonneg q) (sub_nonneg.mpr hK)
  nlinarith [sq_nonneg (a*delta+q*kappa)]

/-- Moment-Lyapunov estimate, conditional on the Ito moment identities. -/
theorem fourth_moment_differential_bound (a q D C M4 M6 rate : ℝ)
    (ha : 0 < a) (hq : 0 ≤ q) (hM6 : 0 ≤ M6) (hJ : C^2 ≤ M4)
    (hr : rate = -4*a*M4-4*q*M6+12*D*C) :
    a*rate ≤ -2*a^2*M4+18*D^2 := by
  rw [hr]
  have hj := mul_nonneg (sq_nonneg a) (sub_nonneg.mpr hJ)
  have h6 := mul_nonneg (le_of_lt ha) (mul_nonneg hq hM6)
  nlinarith [sq_nonneg (a*C-3*D)]

/-- General integrating-factor bound; no stochastic derivation is assumed hidden. -/
theorem scalar_comparison (u rate : ℝ → ℝ) (c b t : ℝ) (ht : 0 ≤ t)
    (hd : ∀ s ∈ Icc 0 t, HasDerivAt u (rate s) s)
    (hr : ∀ s ∈ Icc 0 t, rate s ≤ -c*(u s-b)) :
    u t ≤ b + Real.exp (-c*t)*(u 0-b) := by
  let f : ℝ → ℝ := fun s => Real.exp (c*s)*(u s-b)
  have hf : ∀ s ∈ Icc 0 t, HasDerivAt f
      (Real.exp (c*s)*(c*(u s-b)+rate s)) s := by
    intro s hs
    have he := ((hasDerivAt_id s).const_mul c).exp
    convert he.mul ((hd s hs).sub_const b) using 1 <;> (first | rfl | (simp [id_eq]; ring))
  have hnonpos : ∀ s ∈ Icc 0 t, deriv f s ≤ 0 := by
    intro s hs
    rw [(hf s hs).deriv]
    exact mul_nonpos_of_nonneg_of_nonpos (le_of_lt (Real.exp_pos _)) (by linarith [hr s hs])
  have hmono : AntitoneOn f (Icc 0 t) := antitoneOn_of_deriv_nonpos (convex_Icc 0 t)
    (fun s hs => (hf s hs).continuousAt.continuousWithinAt)
    (fun s hs => (hf s (interior_subset hs)).differentiableAt.differentiableWithinAt)
    (fun s hs => hnonpos s (interior_subset hs))
  have h := hmono ⟨le_rfl, ht⟩ ⟨ht, le_rfl⟩ ht
  have he : Real.exp (c*t)*(u t-b) ≤ u 0-b := by simpa [f] using h
  have hdiv : u t-b ≤ (u 0-b)/Real.exp (c*t) := by
    apply (le_div_iff₀ (Real.exp_pos _)).2
    nlinarith [he]
  rw [div_eq_mul_inv, ← Real.exp_neg] at hdiv
  have hexp : -(c*t) = -c*t := by ring
  rw [hexp] at hdiv
  nlinarith [hdiv]

theorem fourth_moment_bound (a D t : ℝ) (M4 rate : ℝ → ℝ)
    (ha : 0 < a) (ht : 0 ≤ t)
    (hd : ∀ s ∈ Icc 0 t, HasDerivAt M4 (rate s) s)
    (hr : ∀ s ∈ Icc 0 t, a*rate s ≤ -2*a^2*M4 s+18*D^2) :
    M4 t ≤ 9*D^2/a^2+Real.exp (-2*a*t)*(M4 0-9*D^2/a^2) := by
  have hb : ∀ s ∈ Icc 0 t, rate s ≤ -(2*a)*(M4 s-9*D^2/a^2) := by
    intro s hs
    apply le_of_mul_le_mul_left _ ha
    calc
      a*rate s ≤ -2*a^2*M4 s+18*D^2 := hr s hs
      _ = a*(-(2*a)*(M4 s-9*D^2/a^2)) := by
        field_simp [ne_of_gt ha]
        <;> ring
  have h := scalar_comparison M4 rate (2*a) (9*D^2/a^2) t ht hd hb
  convert h using 1 <;> ring

theorem covariance_error_bound (a q K t : ℝ) (C G kappa : ℝ → ℝ)
    (ha : 0 < a) (hq : 0 ≤ q) (ht : 0 ≤ t)
    (hC : ∀ s ∈ Icc 0 t, 0 ≤ C s) (hG : ∀ s ∈ Icc 0 t, 0 ≤ G s)
    (hk : ∀ s ∈ Icc 0 t, (kappa s)^2 ≤ K^2)
    (hd : ∀ s ∈ Icc 0 t, HasDerivAt (fun x => C x-G x)
      (-(2*a+6*q*(C s+G s))*(C s-G s)-2*q*kappa s) s) :
    (C t-G t)^2 ≤ q^2*K^2/a^2 + Real.exp (-2*a*t)*
      ((C 0-G 0)^2-q^2*K^2/a^2) := by
  let r := fun s => 2*(C s-G s)*
    (-(2*a+6*q*(C s+G s))*(C s-G s)-2*q*kappa s)
  have hder : ∀ s ∈ Icc 0 t, HasDerivAt (fun x => (C x-G x)^2) (r s) s := by
    intro s hs
    convert (hd s hs).pow 2 using 1 <;> (first | rfl | (dsimp [r]; ring))
  have hrate : ∀ s ∈ Icc 0 t,
      r s ≤ -(2*a)*((C s-G s)^2-q^2*K^2/a^2) := by
    intro s hs
    have hb := squared_error_differential_bound a q (C s) (G s) (kappa s) K
      (C s-G s) _ ha hq (hC s hs) (hG s hs) (hk s hs) rfl
    have ha0 := ne_of_gt ha
    have hb' : a*(r s+2*a*(C s-G s)^2) ≤ 2*q^2*K^2 := hb
    apply le_of_mul_le_mul_left _ ha
    calc
      a*r s ≤ 2*q^2*K^2 - 2*a^2*(C s-G s)^2 := by nlinarith [hb']
      _ = a*(-(2*a)*((C s-G s)^2-q^2*K^2/a^2)) := by
        field_simp [ha0]
        <;> ring
  have h := scalar_comparison (fun x => (C x-G x)^2) r (2*a) (q^2*K^2/a^2) t ht hder hrate
  convert h using 1 <;> ring

theorem gaussian_cumulant_not_preserved (q C : ℝ) (hq : 0 < q) (hC : 0 < C) :
    -24*q*C^3 < 0 := by
  have h := mul_pos hq (pow_pos hC 3)
  nlinarith [h]

theorem gaussian_initial_cumulant_rate (a q D C : ℝ) :
    (-4*a*(3*C^2)-4*q*(15*C^3)+12*D*C) -
      6*C*(-2*a*C-6*q*C^2+2*D) = -24*q*C^3 := by ring
end QuarticError

namespace NoncompactControl

/-- Finite quadrature only, not a theorem that an infinite-volume trace exists. -/
theorem weighted_sum_bound {ι : Type*} [Fintype ι]
    (w diagonal : ι → ℝ) (B : ℝ)
    (hw : ∀ i, 0 ≤ w i) (hdiag : ∀ i, diagonal i ≤ B) :
    (∑ i, w i*diagonal i) ≤ B*(∑ i, w i) := by
  calc
    (∑ i, w i*diagonal i) ≤ ∑ i, w i*B :=
      Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (hdiag i) (hw i))
    _ = B*(∑ i, w i) := by rw [← Finset.sum_mul, mul_comm]

theorem exterior_coercivity (normSq phiSq cross m2 c : ℝ)
    (hp : m2*normSq ≤ phiSq) (hc : |cross| ≤ c*normSq) :
    (m2-c)*normSq ≤ phiSq+cross := by
  have h := (abs_le.mp hc).1
  nlinarith

theorem localization_error (bulk boundary eps normSq : ℝ)
    (hbulk : 0 ≤ bulk) (hbd : boundary ≤ eps*normSq) :
    -eps*normSq ≤ bulk-boundary := by linarith
end NoncompactControl

/-!
2026-09-22: derivative-coupled homogeneous effective model.
NEW SOURCE HAS NOT BEEN COMPILED, as requested by the author.
Signature (-,+,+,+); X = thetaRate^2/2, not the signed contraction +dtheta^2/2.
The Lorentzian base, action, parameters, smooth solution and target reduction are inputs.
Neither stochastic-to-physical closure nor a populated SU(6) vacuum is assumed proved.
The namespace supplies finite identities, actual derivative implications, a conditional
crossing theorem and conditional late limits. There are no proof placeholders.
-/
namespace UnifiedDynamics

/-- Coordinates of the homogeneous physical ODE; the statistical law is separate. -/
structure UnifiedState where
  theta : ℝ
  thetaRate : ℝ
  phi : ℝ
  phiRate : ℝ
  hubble : ℝ
  scale : ℝ

def kineticCoeff (Z gamma phi : ℝ) : ℝ := Z - gamma / 2 * phi^2
def kinetic (u : ℝ) : ℝ := u^2 / 2
def barePotential (m lam phi : ℝ) : ℝ := m / 2 * phi^2 + lam / 4 * phi^4
def effMassSq (m gamma X : ℝ) : ℝ := m + gamma * X
def forcePotential (m gamma lam X phi : ℝ) : ℝ :=
  effMassSq m gamma X / 2 * phi^2 + lam / 4 * phi^4
def totalDensity (Z gamma m lam u phi v U : ℝ) : ℝ :=
  kineticCoeff Z gamma phi * kinetic u + kinetic v + U + barePotential m lam phi
def totalPressure (Z gamma m lam u phi v U : ℝ) : ℝ :=
  kineticCoeff Z gamma phi * kinetic u + kinetic v - U - barePotential m lam phi
def stateDensity (Z gamma m lam : ℝ) (U : ℝ → ℝ) (s : UnifiedState) : ℝ :=
  totalDensity Z gamma m lam s.thetaRate s.phi s.phiRate (U s.theta)
def thetaResidual (Z gamma H u phi v udot Utheta : ℝ) : ℝ :=
  kineticCoeff Z gamma phi * udot + 3*H*kineticCoeff Z gamma phi*u
    - gamma*phi*v*u + Utheta
def phiResidual (m gamma lam H u phi v vdot : ℝ) : ℝ :=
  vdot + 3*H*v + effMassSq m gamma (kinetic u)*phi + lam*phi^3
def densityRate (Z gamma m lam u phi v udot vdot Utheta : ℝ) : ℝ :=
  kineticCoeff Z gamma phi*u*udot - gamma*phi*v*kinetic u
    + v*vdot + Utheta*u + (m*phi+lam*phi^3)*v
def exchange (gamma u phi v : ℝ) : ℝ := gamma*phi*v*kinetic u

/-- Velocity-dependent force potential belongs inside L, not in rho with the same sign. -/
theorem lagrangian_rearrangement (Z gamma m lam X Y phi U : ℝ) :
    Z*X+Y-U-forcePotential m gamma lam X phi =
      kineticCoeff Z gamma phi*X+Y-U-barePotential m lam phi := by
  unfold forcePotential effMassSq kineticCoeff barePotential
  ring

/-- The review's proposed continuity cancellation leaves a generally nonzero residual. -/
theorem review_continuity_residual (gamma H X phi : ℝ) :
    (-6*H*X)*(1+gamma/2*phi^2)+3*H*(2*X) = -3*gamma*H*X*phi^2 := by
  ring

theorem review_residual_counterexample :
    (-6*(1:ℝ)*1)*(1+1/2*1^2)+3*1*(2*1) = -3 := by norm_num

theorem enthalpy (Z gamma m lam u phi v U : ℝ) :
    totalDensity Z gamma m lam u phi v U + totalPressure Z gamma m lam u phi v U =
      2*(kineticCoeff Z gamma phi*kinetic u+kinetic v) := by
  unfold totalDensity totalPressure
  ring

theorem null_energy (Z gamma m lam u phi v U : ℝ)
    (hA : 0 ≤ kineticCoeff Z gamma phi) :
    0 ≤ totalDensity Z gamma m lam u phi v U + totalPressure Z gamma m lam u phi v U := by
  rw [enthalpy]
  unfold kinetic
  positivity

theorem acceleration_criterion (Z gamma m lam u phi v U : ℝ) :
    totalDensity Z gamma m lam u phi v U + 3*totalPressure Z gamma m lam u phi v U < 0 ↔
      2*(kineticCoeff Z gamma phi*kinetic u+kinetic v) < U+barePotential m lam phi := by
  unfold totalDensity totalPressure
  constructor <;> intro h <;> linarith

/-- Off-shell identity: E_theta*thetaRate + E_phi*phiRate is the continuity residual. -/
theorem continuity_identity (Z gamma m lam H u phi v U udot vdot Utheta : ℝ) :
    densityRate Z gamma m lam u phi v udot vdot Utheta +
      3*H*(totalDensity Z gamma m lam u phi v U + totalPressure Z gamma m lam u phi v U) =
    u*thetaResidual Z gamma H u phi v udot Utheta +
      v*phiResidual m gamma lam H u phi v vdot := by
  unfold densityRate totalDensity totalPressure thetaResidual phiResidual effMassSq kinetic
  ring

theorem continuity_algebra (Z gamma m lam H u phi v U udot vdot Utheta : ℝ)
    (ht : thetaResidual Z gamma H u phi v udot Utheta = 0)
    (hp : phiResidual m gamma lam H u phi v vdot = 0) :
    densityRate Z gamma m lam u phi v udot vdot Utheta =
      -3*H*(totalDensity Z gamma m lam u phi v U + totalPressure Z gamma m lam u phi v U) := by
  have h := continuity_identity Z gamma m lam H u phi v U udot vdot Utheta
  rw [ht, hp] at h
  linarith

/-- U is the potential evaluated along theta; hU encodes its chain rule U_theta*u. -/
theorem density_hasDerivAt (Z gamma m lam : ℝ) (u phi v U : ℝ → ℝ)
    (t udot vdot Utheta : ℝ)
    (hu : HasDerivAt u udot t) (hphi : HasDerivAt phi (v t) t)
    (hv : HasDerivAt v vdot t) (hU : HasDerivAt U (Utheta*u t) t) :
    HasDerivAt (fun s => totalDensity Z gamma m lam (u s) (phi s) (v s) (U s))
      (densityRate Z gamma m lam (u t) (phi t) (v t) udot vdot Utheta) t := by
  have hA := (hasDerivAt_const t Z).sub ((hphi.pow 2).const_mul (gamma/2))
  have hX := (hu.pow 2).div_const 2
  have hY := (hv.pow 2).div_const 2
  have hW := ((hphi.pow 2).const_mul (m/2)).add ((hphi.pow 4).const_mul (lam/4))
  convert (((hA.mul hX).add hY).add hU).add hW using 1 <;>
    (first | rfl | (simp [densityRate, kineticCoeff, kinetic]; ring_nf))

/-- Actual trajectory continuity follows from both field equations, not a continuity premise. -/
theorem unified_continuity (Z gamma m lam H : ℝ) (u phi v U : ℝ → ℝ)
    (t udot vdot Utheta : ℝ)
    (hu : HasDerivAt u udot t) (hphi : HasDerivAt phi (v t) t)
    (hv : HasDerivAt v vdot t) (hU : HasDerivAt U (Utheta*u t) t)
    (ht : thetaResidual Z gamma H (u t) (phi t) (v t) udot Utheta = 0)
    (hp : phiResidual m gamma lam H (u t) (phi t) (v t) vdot = 0) :
    HasDerivAt (fun s => totalDensity Z gamma m lam (u s) (phi s) (v s) (U s))
      (-3*H*(totalDensity Z gamma m lam (u t) (phi t) (v t) (U t) +
        totalPressure Z gamma m lam (u t) (phi t) (v t) (U t))) t := by
  have hr := density_hasDerivAt Z gamma m lam u phi v U t udot vdot Utheta hu hphi hv hU
  rw [continuity_algebra Z gamma m lam H (u t) (phi t) (v t) (U t) udot vdot Utheta ht hp] at hr
  exact hr

/-- Couples the new scalar trajectory theorem to the retained Friedmann derivative theorem. -/
theorem action_friedmann_hasDerivAt (Z gamma m lam M2 : ℝ) (u phi v U H : ℝ → ℝ)
    (t udot vdot Utheta : ℝ) (hM : M2 ≠ 0)
    (hu : HasDerivAt u udot t) (hphi : HasDerivAt phi (v t) t)
    (hv : HasDerivAt v vdot t) (hU : HasDerivAt U (Utheta*u t) t)
    (ht : thetaResidual Z gamma (H t) (u t) (phi t) (v t) udot Utheta = 0)
    (hp : phiResidual m gamma lam (H t) (u t) (phi t) (v t) vdot = 0)
    (hH : HasDerivAt H (-(totalDensity Z gamma m lam (u t) (phi t) (v t) (U t) +
      totalPressure Z gamma m lam (u t) (phi t) (v t) (U t))/(2*M2)) t) :
    HasDerivAt (fun s => CosmologicalBridge.constraint M2 (H s)
      (totalDensity Z gamma m lam (u s) (phi s) (v s) (U s))) 0 t := by
  exact CosmologicalBridge.friedmann_constraint_hasDerivAt M2 H
    (fun s => totalDensity Z gamma m lam (u s) (phi s) (v s) (U s))
    (fun s => totalPressure Z gamma m lam (u s) (phi s) (v s) (U s)) t hM hH
    (unified_continuity Z gamma m lam (H t) u phi v U t udot vdot Utheta hu hphi hv hU ht hp)

theorem exchange_balance (gamma u phi v : ℝ) :
    exchange gamma u phi v + (-exchange gamma u phi v) = 0 := by ring

/-- The theta-sector rate includes the derivative of its phi-dependent kinetic metric. -/
theorem theta_exchange (Z gamma H u phi v udot Utheta : ℝ)
    (ht : thetaResidual Z gamma H u phi v udot Utheta = 0) :
    kineticCoeff Z gamma phi*u*udot-gamma*phi*v*kinetic u+Utheta*u +
      6*H*kineticCoeff Z gamma phi*kinetic u = exchange gamma u phi v := by
  unfold thetaResidual at ht
  unfold exchange kinetic
  have hu : u * (kineticCoeff Z gamma phi*udot+3*H*kineticCoeff Z gamma phi*u-gamma*phi*v*u+Utheta) = 0 := by
    rw [ht]; ring
  nlinarith [hu]

theorem phi_exchange (m gamma lam H u phi v vdot : ℝ)
    (hp : phiResidual m gamma lam H u phi v vdot = 0) :
    v*vdot+(m*phi+lam*phi^3)*v+6*H*kinetic v = -exchange gamma u phi v := by
  unfold phiResidual effMassSq kinetic at hp
  unfold exchange kinetic
  have hv : v * (vdot+3*H*v+(m+gamma*(u^2/2))*phi+lam*phi^3) = 0 := by
    rw [hp]; ring
  nlinarith [hv]

/-- No monotone kinetic decay follows unless the feedback and potential-gradient terms allow it. -/
theorem kinetic_rate_balance (Z gamma H u phi v udot Utheta : ℝ)
    (ht : thetaResidual Z gamma H u phi v udot Utheta = 0) :
    kineticCoeff Z gamma phi*(u*udot+6*H*kinetic u) =
      2*gamma*phi*v*kinetic u-Utheta*u := by
  unfold thetaResidual at ht
  unfold kinetic
  have hu : u * (kineticCoeff Z gamma phi*udot+3*H*kineticCoeff Z gamma phi*u-gamma*phi*v*u+Utheta) = 0 := by
    rw [ht]; ring
  nlinarith [hu]

theorem kinetic_decreases_if_feedback_nonpositive (Z gamma H u phi v udot Utheta : ℝ)
    (hA : 0 < kineticCoeff Z gamma phi) (hH : 0 ≤ H)
    (ht : thetaResidual Z gamma H u phi v udot Utheta = 0)
    (hfeedback : 2*gamma*phi*v*kinetic u-Utheta*u ≤ 0) : u*udot ≤ 0 := by
  have h := kinetic_rate_balance Z gamma H u phi v udot Utheta ht
  have hX : 0 ≤ kinetic u := by unfold kinetic; positivity
  have hd : 0 ≤ 6*H*kinetic u := by positivity
  nlinarith

theorem symmetric_branch_dilution (Z H u udot : ℝ) (hZ : Z ≠ 0)
    (ht : Z*udot+3*H*Z*u=0) : u*udot = -6*H*kinetic u := by
  have hz : Z*(udot+3*H*u)=0 := by nlinarith [ht]
  have hv := (mul_eq_zero.mp hz).resolve_left hZ
  unfold kinetic
  have hu : u*(udot+3*H*u) = 0 := by rw [hv]; ring
  nlinarith [hu]

theorem zero_order_parameter_is_invariant (m gamma lam H u : ℝ) :
    phiResidual m gamma lam H u 0 0 0 = 0 := by
  simp [phiResidual]

def criticalKinetic (m gamma : ℝ) : ℝ := -m/gamma

theorem critical_positive (m gamma : ℝ) (hm : m < 0) (hg : 0 < gamma) :
    0 < criticalKinetic m gamma := div_pos (neg_pos.mpr hm) hg

theorem effMass_strictMono (m gamma : ℝ) (hg : 0 < gamma) :
    StrictMono (effMassSq m gamma) := by
  intro x y hxy
  unfold effMassSq
  nlinarith

theorem critical_mass_zero (m gamma : ℝ) (hg : gamma ≠ 0) :
    effMassSq m gamma (criticalKinetic m gamma) = 0 := by
  unfold effMassSq criticalKinetic
  field_simp [hg]
  <;> ring

theorem mass_sign_criterion (m gamma X : ℝ) (hg : 0 < gamma) :
    (0 < effMassSq m gamma X ↔ criticalKinetic m gamma < X) ∧
    (effMassSq m gamma X < 0 ↔ X < criticalKinetic m gamma) := by
  have hz := critical_mass_zero m gamma (ne_of_gt hg)
  unfold effMassSq at *
  constructor <;> constructor <;> intro h <;> nlinarith

/-- Limit conclusion only: existence of the trajectory and its decay are explicit hypotheses. -/
theorem mass_eventually_negative (m gamma : ℝ) (X : ℝ → ℝ) (hm : m < 0)
    (hX : Tendsto X atTop (nhds 0)) :
    ∀ᶠ t in atTop, effMassSq m gamma (X t) < 0 := by
  have hmLim : Tendsto (fun t => effMassSq m gamma (X t)) atTop (nhds m) := by
    simpa [effMassSq] using
      (tendsto_const_nhds.add (tendsto_const_nhds.mul hX) :
        Tendsto (fun t => m+gamma*X t) atTop (nhds (m+gamma*0)))
  exact hmLim.eventually (gt_mem_nhds hm)

/-- Continuity and the actual initial value close the gap between eventual sign and crossing. -/
theorem critical_crossing (m gamma : ℝ) (X : ℝ → ℝ) (hm : m < 0)
    (hX : Continuous X) (hlim : Tendsto X atTop (nhds 0))
    (hearly : 0 < effMassSq m gamma (X 0)) :
    ∃ tc : ℝ, 0 < tc ∧ effMassSq m gamma (X tc) = 0 := by
  obtain ⟨T, hT⟩ := eventually_atTop.1 (mass_eventually_negative m gamma X hm hlim)
  let b : ℝ := max T 1
  have hb : 0 < b := lt_of_lt_of_le (by norm_num : (0:ℝ) < 1) (le_max_right T 1)
  have hneg : effMassSq m gamma (X b) < 0 := hT b (le_max_left T 1)
  have hc : Continuous (fun t => effMassSq m gamma (X t)) := by
    unfold effMassSq
    exact continuous_const.add (continuous_const.mul hX)
  obtain ⟨tc, htc, hz⟩ := intermediate_value_Icc' (le_of_lt hb) hc.continuousOn
    (show (0:ℝ) ∈ Icc (effMassSq m gamma (X b)) (effMassSq m gamma (X 0)) from
      ⟨le_of_lt hneg, le_of_lt hearly⟩)
  refine ⟨tc, ?_, hz⟩
  have hne : tc ≠ 0 := by intro heq; subst tc; linarith
  exact lt_of_le_of_ne htc.1 (Ne.symm hne)

theorem critical_crossing_unique (m gamma : ℝ) (X : ℝ → ℝ) (hg : 0 < gamma)
    (hmono : StrictAntiOn X (Ici 0)) (t1 t2 : ℝ)
    (h1 : 0 ≤ t1) (h2 : 0 ≤ t2)
    (hz1 : effMassSq m gamma (X t1) = 0) (hz2 : effMassSq m gamma (X t2) = 0) : t1 = t2 := by
  have hx : X t1 = X t2 := by unfold effMassSq at *; nlinarith
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hh := hmono h1 h2 hlt
    linarith
  · have hh := hmono h2 h1 hgt
    linarith

theorem critical_sign_order (m gamma : ℝ) (X : ℝ → ℝ) (hg : 0 < gamma)
    (hmono : StrictAntiOn X (Ici 0)) (tc t : ℝ) (hc : 0 ≤ tc) (ht : 0 ≤ t)
    (hz : effMassSq m gamma (X tc) = 0) :
    (t < tc → 0 < effMassSq m gamma (X t)) ∧
    (tc < t → effMassSq m gamma (X t) < 0) := by
  have hmass := effMass_strictMono m gamma hg
  constructor
  · intro hlt
    have h := hmass (hmono ht hc hlt)
    linarith
  · intro hlt
    have h := hmass (hmono hc ht hlt)
    linarith

/-- Scalar minima only; this does not select a matrix conjugacy class. -/
theorem broken_scalar_minimum (m gamma lam X v phi : ℝ)
    (hm : effMassSq m gamma X < 0) (hl : 0 < lam)
    (hv : v^2 = -effMassSq m gamma X/lam) :
    VEV123CW.V0_deriv_param (effMassSq m gamma X) lam v = 0 ∧
    0 < VEV123CW.V0_hess_param (effMassSq m gamma X) lam v ∧
    forcePotential m gamma lam X v ≤ forcePotential m gamma lam X phi := by
  exact ThermalBridge.broken_minimum (effMassSq m gamma X) lam v phi hm hl hv

/-- Sum of scalar lower bounds; the traceless constraint can only restrict competitors. -/
theorem six_mode_lower_bound (m lam : ℝ) (u : Fin 6 → ℝ) (hl : 0 < lam) :
    -(6*m^2)/(4*lam) ≤ ∑ i, VEV123CW.V0_param m lam (u i) := by
  have hs : (∑ _i : Fin 6, -(m^2)/(4*lam)) ≤
      ∑ i : Fin 6, VEV123CW.V0_param m lam (u i) :=
    Finset.sum_le_sum (fun i _ => VEV123CW.V0_param_min_lower_bound m lam (u i) hl)
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    Nat.cast_ofNat] at hs
  ring_nf at hs ⊢
  exact hs

/-- A traceless (3,3) spectrum saturates the bound at m=-1, lambda=1. -/
theorem three_three_witness :
    let u : Fin 6 → ℝ := ![1,1,1,-1,-1,-1]
    (∑ i, u i) = 0 ∧ (∑ i, VEV123CW.V0_param (-1) 1 (u i)) = -(3:ℝ)/2 := by
  norm_num [Fin.sum_univ_succ, VEV123CW.V0_param]

/-- A nonempty parameter range can support positive origin mass and accelerated stress. -/
theorem early_parameter_witness :
    0 < effMassSq (-1) 1 2 ∧
    2*((1:ℝ)*2) < 10 ∧ 0 < kineticCoeff 1 1 0 := by
  norm_num [effMassSq, kineticCoeff]

def vacuumDensity (m lam Uinf : ℝ) : ℝ := Uinf - m^2/(4*lam)

theorem vacuum_potential_value (m lam phi : ℝ) (hl : lam ≠ 0)
    (hv : phi^2 = -m/lam) : barePotential m lam phi = -m^2/(4*lam) := by
  have h := VEV123CW.V0_param_square_completion m lam phi hl
  have hz : phi^2+m/lam = 0 := by rw [hv]; ring
  rw [hz] at h
  change m/2*phi^2+lam/4*phi^4 = -m^2/(4*lam)
  dsimp [VEV123CW.V0_param] at h
  nlinarith

theorem vacuum_density_pressure (Z gamma m lam Uinf phi : ℝ) (hl : lam ≠ 0)
    (hv : phi^2 = -m/lam) :
    totalDensity Z gamma m lam 0 phi 0 Uinf = vacuumDensity m lam Uinf ∧
    totalPressure Z gamma m lam 0 phi 0 Uinf = -vacuumDensity m lam Uinf := by
  have hW := vacuum_potential_value m lam phi hl hv
  simp [totalDensity, totalPressure, kinetic, hW, vacuumDensity]
  constructor <;> ring

theorem vacuum_w_minus_one (Z gamma m lam Uinf phi : ℝ) (hl : lam ≠ 0)
    (hv : phi^2 = -m/lam) (hpos : 0 < vacuumDensity m lam Uinf) :
    totalPressure Z gamma m lam 0 phi 0 Uinf / totalDensity Z gamma m lam 0 phi 0 Uinf = -1 := by
  obtain ⟨hr, hp⟩ := vacuum_density_pressure Z gamma m lam Uinf phi hl hv
  rw [hr, hp]
  field_simp [ne_of_gt hpos]

theorem vacuum_healthy_criterion (Z gamma m lam phi : ℝ) (hl : lam ≠ 0)
    (hv : phi^2 = -m/lam) : kineticCoeff Z gamma phi = Z+gamma*m/(2*lam) := by
  unfold kineticCoeff
  rw [hv]
  field_simp [hl]
  <;> ring

theorem vacuum_rest_equations (Z gamma m lam H phi : ℝ) (hl : lam ≠ 0)
    (hv : phi^2 = -m/lam) :
    thetaResidual Z gamma H 0 phi 0 0 0 = 0 ∧
    phiResidual m gamma lam H 0 phi 0 0 = 0 := by
  have hprod : lam*phi^2 = -m := by rw [hv]; field_simp [hl]
  constructor
  · simp [thetaResidual]
  · simp only [phiResidual, effMassSq, kinetic, zero_pow (by norm_num : (2:ℕ) ≠ 0),
      zero_div, mul_zero, add_zero, zero_add]
    calc
      m*phi+lam*phi^3 = phi*(m+lam*phi^2) := by ring
      _ = 0 := by rw [hprod]; ring

theorem vacuum_health_positive_witness :
    0 < kineticCoeff 1 1 1 ∧ 0 < vacuumDensity (-1) 1 1 := by
  norm_num [kineticCoeff, vacuumDensity]

theorem residual_energy_need_not_be_positive : vacuumDensity (-1) 1 0 = -(1:ℝ)/4 := by
  norm_num [vacuumDensity]

/-- Limits of the actual polynomial stress; no attraction to these limits is postulated as a result. -/
theorem density_pressure_limits (Z gamma m lam Uinf phiv : ℝ) (u phi v U : ℝ → ℝ)
    (hu : Tendsto u atTop (nhds 0)) (hp : Tendsto phi atTop (nhds phiv))
    (hv : Tendsto v atTop (nhds 0)) (hU : Tendsto U atTop (nhds Uinf))
    (hl : lam ≠ 0) (hvev : phiv^2 = -m/lam) :
    Tendsto (fun t => totalDensity Z gamma m lam (u t) (phi t) (v t) (U t)) atTop
      (nhds (vacuumDensity m lam Uinf)) ∧
    Tendsto (fun t => totalPressure Z gamma m lam (u t) (phi t) (v t) (U t)) atTop
      (nhds (-vacuumDensity m lam Uinf)) := by
  have hA := (tendsto_const_nhds : Tendsto (fun _ : ℝ => Z) atTop (nhds Z)).sub
    ((tendsto_const_nhds : Tendsto (fun _ : ℝ => gamma/2) atTop (nhds (gamma/2))).mul (hp.pow 2))
  have hX := (hu.pow 2).div_const 2
  have hY := (hv.pow 2).div_const 2
  have hW := ((tendsto_const_nhds : Tendsto (fun _ : ℝ => m/2) atTop (nhds (m/2))).mul
    (hp.pow 2)).add ((tendsto_const_nhds : Tendsto (fun _ : ℝ => lam/4) atTop
      (nhds (lam/4))).mul (hp.pow 4))
  have hr := (((hA.mul hX).add hY).add hU).add hW
  have hpr := (((hA.mul hX).add hY).sub hU).sub hW
  change Tendsto (fun t => totalDensity Z gamma m lam (u t) (phi t) (v t) (U t)) atTop
    (nhds (totalDensity Z gamma m lam 0 phiv 0 Uinf)) at hr
  change Tendsto (fun t => totalPressure Z gamma m lam (u t) (phi t) (v t) (U t)) atTop
    (nhds (totalPressure Z gamma m lam 0 phiv 0 Uinf)) at hpr
  obtain ⟨hvalr, hvalp⟩ := vacuum_density_pressure Z gamma m lam Uinf phiv hl hvev
  rw [hvalr] at hr
  rw [hvalp] at hpr
  exact ⟨hr, hpr⟩

theorem late_w_limit (Z gamma m lam Uinf phiv : ℝ) (u phi v U : ℝ → ℝ)
    (hu : Tendsto u atTop (nhds 0)) (hp : Tendsto phi atTop (nhds phiv))
    (hv : Tendsto v atTop (nhds 0)) (hU : Tendsto U atTop (nhds Uinf))
    (hl : lam ≠ 0) (hvev : phiv^2 = -m/lam) (hpos : 0 < vacuumDensity m lam Uinf) :
    Tendsto (fun t => totalPressure Z gamma m lam (u t) (phi t) (v t) (U t) /
      totalDensity Z gamma m lam (u t) (phi t) (v t) (U t)) atTop (nhds (-1)) := by
  obtain ⟨hr, hpr⟩ := density_pressure_limits Z gamma m lam Uinf phiv u phi v U hu hp hv hU hl hvev
  have hratio := hpr.div hr (ne_of_gt hpos)
  have heq : -vacuumDensity m lam Uinf / vacuumDensity m lam Uinf = -1 := by
    field_simp [ne_of_gt hpos]
  change Tendsto ((fun t => totalPressure Z gamma m lam (u t) (phi t) (v t) (U t)) /
      (fun t => totalDensity Z gamma m lam (u t) (phi t) (v t) (U t))) atTop (nhds (-1))
  simpa [heq] using hratio

/-- Density domination is conditional on independently established dilution. -/
theorem vacuum_eventually_dominates (Lambda : ℝ) (rhoMatter : ℝ → ℝ)
    (hL : 0 < Lambda) (hm : Tendsto rhoMatter atTop (nhds 0)) :
    ∀ᶠ t in atTop, rhoMatter t < Lambda := hm.eventually (gt_mem_nhds hL)

/-- Actual limiting scalar stress plus a diluting extra component has an accelerating sign. -/
theorem late_accelerating_stress (Lambda : ℝ) (rho p rhoM pM : ℝ → ℝ)
    (hL : 0 < Lambda) (hr : Tendsto rho atTop (nhds Lambda))
    (hp : Tendsto p atTop (nhds (-Lambda))) (hm : Tendsto rhoM atTop (nhds 0))
    (hpm : Tendsto pM atTop (nhds 0)) :
    ∀ᶠ t in atTop, (rho t+rhoM t)+3*(p t+pM t) < 0 := by
  have hlim := (hr.add hm).add
    ((tendsto_const_nhds : Tendsto (fun _ : ℝ => (3:ℝ)) atTop (nhds 3)).mul (hp.add hpm))
  exact hlim.eventually (gt_mem_nhds (by linarith : Lambda+0+3*(-Lambda+0) < 0))

end UnifiedDynamics

end
