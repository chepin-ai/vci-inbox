# CLASSIFY: L1
"""M1-1 spike migration-candidate patcher v6: Lean/mathlib v4.10.0 -> v4.35.0.
v1: BC-1 scoped inner notation / BC-2 sub_apply / BC-3 add_le_add flip / BC-4 LipschitzOnWith alias.
v4 reorder: BC-5 block FIRST (BC-10 substring sits inside BC-5 old block, v3 ordering shadowed it); v3 added BC-5b (ExistUnique import — decls moved file) + BC-10 (div_le_iff → div_le_iff₀); v2 added Existence.lean layer (surfaced after Basic cleared):
  BC-5  IsPicardLindelof API redesign (t0 : Icc subtype; (a r L K : R>=0);
        fields lipschitzOnWith/continuousOn/norm_le/mul_max_le;
        exists_forall_hasDerivWithinAt_Icc_eq -> exists_eq_forall_mem_Icc_hasDerivWithinAt0)
  BC-7  HasFDerivWithinAt.mono_of_mem -> mono_of_mem_nhdsWithin (x3)
  BC-8  slope simp set needs vsub_eq_sub
  BC-9  le_of_not_le removed -> (not_le.mp h1).le
Each applied edit is printed for the breaking-change ledger."""
import pathlib, sys

# entries: (substr, repl, tag) global, or (file_substr, substr, repl, tag) file-scoped
TEXT_EDITS = [
    ("  have hpl : IsPicardLindelof (fun _ => D.vf) t₀ t₀ (t₀ + D.δC RB) x₁\n      ⟨D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + 1), by\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have h3 : (0:ℝ) ≤ ‖x₁‖ + 1 := add_nonneg (norm_nonneg _) zero_le_one\n        nlinarith [mul_nonneg D.hν.le h1, mul_nonneg h2 h3]⟩\n      1 (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) :=\n  { ht₀ := mem_Icc.mpr ⟨le_refl _, le_add_of_nonneg_right hδ.le⟩\n    hR := zero_le_one\n    lipschitz := fun t _ => D.lipschitzOnWith_vf x₁ zero_le_one\n    cont := fun x _ => continuousOn_const\n    norm_le := by\n      intro t _ x hx\n      have hxb : ‖x‖ ≤ RB + 1 := by\n        have h : ‖x - x₁‖ ≤ (1:ℝ) := by rwa [Metric.mem_closedBall, dist_eq_norm] at hx\n        have hx' : ‖x‖ ≤ ‖x₁‖ + 1 := by\n          calc ‖x‖ = ‖x - x₁ + x₁‖ := by simp\n            _ ≤ ‖x - x₁‖ + ‖x₁‖ := norm_add_le _ _\n            _ ≤ 1 + ‖x₁‖ := by linarith\n            _ = ‖x₁‖ + 1 := by ring\n        linarith\n      have e := D.norm_vf_le x\n      have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n      have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n      have hsq : ‖x‖ ^ 2 ≤ (RB + 1) ^ 2 := by gcongr\n      nlinarith [e, mul_le_mul_of_nonneg_left hxb (mul_nonneg D.hν.le h1),\n        mul_le_mul_of_nonneg_left hsq h2]\n    C_mul_le_R := by\n      have hmax : max (t₀ + D.δC RB - t₀) (t₀ - t₀) = D.δC RB := by\n        rw [add_sub_cancel_left, sub_self, max_eq_left hδ.le]\n      rw [hmax, δC, mul_one_div]\n      rw [div_le_iff hC1]\n      calc D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖\n          ≤ max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 := le_max_left _ _\n        _ = 1 * max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=\n            (one_mul _).symm }\n  obtain ⟨x, hx0, hx⟩ := hpl.exists_forall_hasDerivWithinAt_Icc_eq x₁", "  have hpl : IsPicardLindelof (fun _ => D.vf) (tmin := t₀) (tmax := t₀ + D.δC RB)\n      ⟨t₀, mem_Icc.mpr ⟨le_refl _, le_add_of_nonneg_right hδ.le⟩⟩ x₁\n      1 0 ⟨D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖, by\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have hRB1 : (0:ℝ) ≤ RB + 1 := add_nonneg (le_trans (norm_nonneg _) hx₁) zero_le_one\n        exact add_nonneg (add_nonneg (mul_nonneg (mul_nonneg D.hν.le h1) hRB1)\n          (mul_nonneg h2 (pow_nonneg hRB1 2))) (norm_nonneg _)⟩\n      ⟨D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + 1), by\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have h3 : (0:ℝ) ≤ ‖x₁‖ + 1 := add_nonneg (norm_nonneg _) zero_le_one\n        nlinarith [mul_nonneg D.hν.le h1, mul_nonneg h2 h3]⟩ :=\n    { lipschitzOnWith := fun t _ => D.lipschitzOnWith_vf x₁ zero_le_one\n      continuousOn := fun x _ => continuousOn_const\n      norm_le := by\n        intro t _ x hx\n        have hxb : ‖x‖ ≤ RB + 1 := by\n          have h : ‖x - x₁‖ ≤ (1:ℝ) := by\n            rw [Metric.mem_closedBall, dist_eq_norm] at hx\n            simpa using hx\n          have hx' : ‖x‖ ≤ ‖x₁‖ + 1 := by\n            calc ‖x‖ = ‖x - x₁ + x₁‖ := by simp\n              _ ≤ ‖x - x₁‖ + ‖x₁‖ := norm_add_le _ _\n              _ ≤ 1 + ‖x₁‖ := by linarith\n              _ = ‖x₁‖ + 1 := by ring\n          linarith\n        have e := D.norm_vf_le x\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have hsq : ‖x‖ ^ 2 ≤ (RB + 1) ^ 2 := by gcongr\n        show ‖D.vf x‖ ≤ D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖\n        nlinarith [e, mul_le_mul_of_nonneg_left hxb (mul_nonneg D.hν.le h1),\n          mul_le_mul_of_nonneg_left hsq h2]\n      mul_max_le := by\n        show (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) *\n            max (t₀ + D.δC RB - t₀) (t₀ - t₀) ≤ (1:ℝ) - 0\n        rw [sub_zero]\n        have hmax : max (t₀ + D.δC RB - t₀) (t₀ - t₀) = D.δC RB := by\n          rw [add_sub_cancel_left, sub_self, max_eq_left hδ.le]\n        rw [hmax, δC, mul_one_div, div_le_iff hC1]\n        calc D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖\n            ≤ max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 := le_max_left _ _\n          _ = 1 * max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=\n              (one_mul _).symm }\n  obtain ⟨x, hx0, hx⟩ := hpl.exists_eq_forall_mem_Icc_hasDerivWithinAt₀", 'BC-5'),
    ("Existence", "import NsGalerkin.Basic",
     "import NsGalerkin.Basic\nimport Mathlib.Analysis.ODE.ExistUnique", "BC-5b"),
    ("Existence", "div_le_iff hC1", "div_le_iff₀ hC1", "BC-10"),
    ("ContinuousLinearMap.sub_apply", "sub_apply", 'BC-2'),
    ("add_le_add_right h2 _", "add_le_add_left h2 _", 'BC-3'),
    ("add_le_add_right h5 _", "add_le_add_left h5 _", 'BC-3'),
    ("  rw [lipschitzOnWith_iff_dist_le_mul]\n  intro x hx y hy", "  refine LipschitzOnWith.of_dist_le_mul ?_\n  intro x hx y hy", 'BC-4'),
    ("  have hL := D.lipschitzOnWith_vf x₁ hR\n  rw [lipschitzOnWith_iff_dist_le_mul] at hL", "  have hL := (D.lipschitzOnWith_vf x₁ hR).dist_le_mul", 'BC-4'
    ("Uniqueness", "    simpa using e", "    simpa only [NNReal.coe_mk, add_zero] using e", "BC-11"),),
    (".mono_of_mem ", ".mono_of_mem_nhdsWithin ", 'BC-7'),
    ("simpa only [slope, smul_eq_mul] using h", "simpa only [slope, smul_eq_mul, vsub_eq_sub] using h", 'BC-8'),
    ("le_of_not_le h1", "(not_le.mp h1).le", 'BC-9')
]

def patch(path):
    p = pathlib.Path(path)
    t = p.read_text()
    orig = t
    for ent in TEXT_EDITS:
        if len(ent) == 4:
            fscope, old, new, tag = ent
            if fscope not in str(p) or old not in t:
                continue
        else:
            old, new, tag = ent
            if old not in t:
                continue
        t = t.replace(old, new)
        print(f'{tag} applied  {p}')
    if '⟪' in t and 'open scoped InnerProductSpace' not in t:
        lines = t.split('\n')
        imp = [i for i, l in enumerate(lines) if l.startswith('import ')]
        if imp:
            lines.insert(imp[-1] + 1, 'open scoped InnerProductSpace')
            t = '\n'.join(lines)
            print(f'BC-1 applied  {p}')
    if t != orig:
        p.write_text(t)

if __name__ == '__main__':
    for a in sys.argv[1:]:
        patch(a)
