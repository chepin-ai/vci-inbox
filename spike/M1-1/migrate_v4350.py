# CLASSIFY: L1
"""M1-1 spike migration-candidate patcher v10: Lean/mathlib v4.10.0 -> v4.35.0.
v1: BC-1 scoped inner notation / BC-2 sub_apply / BC-3 add_le_add flip / BC-4 LipschitzOnWith alias.
v4 reorder: BC-5 block FIRST (BC-10 substring sits inside BC-5 old block, v3 ordering shadowed it); v3 added BC-5b (ExistUnique import — decls moved file) + BC-10 (div_le_iff → div_le_iff₀); v2 added Existence.lean layer (surfaced after Basic cleared):
  BC-5  IsPicardLindelof API redesign (t0 : Icc subtype; (a r L K : R>=0);
        fields lipschitzOnWith/continuousOn/norm_le/mul_max_le;
        exists_forall_hasDerivWithinAt_Icc_eq -> exists_eq_forall_mem_Icc_hasDerivWithinAt0)
  BC-7  HasFDerivWithinAt.mono_of_mem -> mono_of_mem_nhdsWithin (x3)
  BC-8  slope simp set needs vsub_eq_sub
  BC-9  le_of_not_le removed -> (not_le.mp h1).le
v8 adds ExplicitB layer (surfaced iter-9): WithLp became a structure in v4.35.0
  BC-12a PiLp construction: ![...] literal needs WithLp.toLp 2 wrapper
  BC-12b funext i fails on structure equality -> ext i (PiLp.ext)
  BC-12c simp sets need PiLp.toLp_apply to reduce (toLp p f) i (CoeFun via ofLp)
  BC-12d B3_inner_self simp only set likewise +PiLp.toLp_apply
  BC-13  abs_add removed -> abs_add_le (x2)
v9 pre-staged CapAnchor layer (same WithLp-structure family; pushed only after iter-10 confirms):
  BC-14a capLin def literal -> WithLp.toLp 2 wrap
  BC-14b capF_apply stmt literal -> wrap; funext->ext; simp +PiLp.toLp_apply
  BC-14c capParamsP1.f / capCenterP1 literals -> wrap
  BC-14d capF_p1_eq_vf funext->ext + simp +PiLp.toLp_apply
v9b (iter-10 harvest): ExplicitB fully clean except B3_inner_self tail —
  BC-15  simp only now fully normalizes Fin indices; trailing
         rw [Fin.succ_zero_eq_one', ...] finds no pattern -> delete the rw, ring closes
v10 (iter-12 harvest): idempotency hardening for post-转正 re-application —
  BC-5b anchored to 'import NsGalerkin.Basic\n\nopen Set Filter' (no double insert)
  BC-11b newline-terminated (was prefix-matching its own output 'simpa using e\'')
Each applied edit is printed for the breaking-change ledger."""
import pathlib, sys

# entries: (substr, repl, tag) global, or (file_substr, substr, repl, tag) file-scoped
TEXT_EDITS = [
    ("  have hpl : IsPicardLindelof (fun _ => D.vf) t₀ t₀ (t₀ + D.δC RB) x₁\n      ⟨D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + 1), by\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have h3 : (0:ℝ) ≤ ‖x₁‖ + 1 := add_nonneg (norm_nonneg _) zero_le_one\n        nlinarith [mul_nonneg D.hν.le h1, mul_nonneg h2 h3]⟩\n      1 (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) :=\n  { ht₀ := mem_Icc.mpr ⟨le_refl _, le_add_of_nonneg_right hδ.le⟩\n    hR := zero_le_one\n    lipschitz := fun t _ => D.lipschitzOnWith_vf x₁ zero_le_one\n    cont := fun x _ => continuousOn_const\n    norm_le := by\n      intro t _ x hx\n      have hxb : ‖x‖ ≤ RB + 1 := by\n        have h : ‖x - x₁‖ ≤ (1:ℝ) := by rwa [Metric.mem_closedBall, dist_eq_norm] at hx\n        have hx' : ‖x‖ ≤ ‖x₁‖ + 1 := by\n          calc ‖x‖ = ‖x - x₁ + x₁‖ := by simp\n            _ ≤ ‖x - x₁‖ + ‖x₁‖ := norm_add_le _ _\n            _ ≤ 1 + ‖x₁‖ := by linarith\n            _ = ‖x₁‖ + 1 := by ring\n        linarith\n      have e := D.norm_vf_le x\n      have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n      have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n      have hsq : ‖x‖ ^ 2 ≤ (RB + 1) ^ 2 := by gcongr\n      nlinarith [e, mul_le_mul_of_nonneg_left hxb (mul_nonneg D.hν.le h1),\n        mul_le_mul_of_nonneg_left hsq h2]\n    C_mul_le_R := by\n      have hmax : max (t₀ + D.δC RB - t₀) (t₀ - t₀) = D.δC RB := by\n        rw [add_sub_cancel_left, sub_self, max_eq_left hδ.le]\n      rw [hmax, δC, mul_one_div]\n      rw [div_le_iff hC1]\n      calc D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖\n          ≤ max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 := le_max_left _ _\n        _ = 1 * max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=\n            (one_mul _).symm }\n  obtain ⟨x, hx0, hx⟩ := hpl.exists_forall_hasDerivWithinAt_Icc_eq x₁", "  have hpl : IsPicardLindelof (fun _ => D.vf) (tmin := t₀) (tmax := t₀ + D.δC RB)\n      ⟨t₀, mem_Icc.mpr ⟨le_refl _, le_add_of_nonneg_right hδ.le⟩⟩ x₁\n      1 0 ⟨D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖, by\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have hRB1 : (0:ℝ) ≤ RB + 1 := add_nonneg (le_trans (norm_nonneg _) hx₁) zero_le_one\n        exact add_nonneg (add_nonneg (mul_nonneg (mul_nonneg D.hν.le h1) hRB1)\n          (mul_nonneg h2 (pow_nonneg hRB1 2))) (norm_nonneg _)⟩\n      ⟨D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + 1), by\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have h3 : (0:ℝ) ≤ ‖x₁‖ + 1 := add_nonneg (norm_nonneg _) zero_le_one\n        nlinarith [mul_nonneg D.hν.le h1, mul_nonneg h2 h3]⟩ :=\n    { lipschitzOnWith := fun t _ => D.lipschitzOnWith_vf x₁ zero_le_one\n      continuousOn := fun x _ => continuousOn_const\n      norm_le := by\n        intro t _ x hx\n        have hxb : ‖x‖ ≤ RB + 1 := by\n          have h : ‖x - x₁‖ ≤ (1:ℝ) := by\n            rw [Metric.mem_closedBall, dist_eq_norm] at hx\n            simpa using hx\n          have hx' : ‖x‖ ≤ ‖x₁‖ + 1 := by\n            calc ‖x‖ = ‖x - x₁ + x₁‖ := by simp\n              _ ≤ ‖x - x₁‖ + ‖x₁‖ := norm_add_le _ _\n              _ ≤ 1 + ‖x₁‖ := by linarith\n              _ = ‖x₁‖ + 1 := by ring\n          linarith\n        have e := D.norm_vf_le x\n        have h1 : (0:ℝ) ≤ ‖D.A‖ := D.A.opNorm_nonneg\n        have h2 : (0:ℝ) ≤ ‖D.B‖ := D.B.opNorm_nonneg\n        have hsq : ‖x‖ ^ 2 ≤ (RB + 1) ^ 2 := by gcongr\n        show ‖D.vf x‖ ≤ D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖\n        nlinarith [e, mul_le_mul_of_nonneg_left hxb (mul_nonneg D.hν.le h1),\n          mul_le_mul_of_nonneg_left hsq h2]\n      mul_max_le := by\n        show (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) *\n            max (t₀ + D.δC RB - t₀) (t₀ - t₀) ≤ (1:ℝ) - 0\n        rw [sub_zero]\n        have hmax : max (t₀ + D.δC RB - t₀) (t₀ - t₀) = D.δC RB := by\n          rw [add_sub_cancel_left, sub_self, max_eq_left hδ.le]\n        rw [hmax, δC, mul_one_div, div_le_iff hC1]\n        calc D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖\n            ≤ max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 := le_max_left _ _\n          _ = 1 * max (D.ν * ‖D.A‖ * (RB + 1) + ‖D.B‖ * (RB + 1) ^ 2 + ‖D.f‖) 1 :=\n              (one_mul _).symm }\n  obtain ⟨x, hx0, hx⟩ := hpl.exists_eq_forall_mem_Icc_hasDerivWithinAt₀", 'BC-5'),
    ("Existence", "import NsGalerkin.Basic\n\nopen Set Filter",
     "import NsGalerkin.Basic\nimport Mathlib.Analysis.ODE.ExistUnique\n\nopen Set Filter", "BC-5b"),
    ("Existence", "div_le_iff hC1", "div_le_iff₀ hC1", "BC-10"),
    ("ContinuousLinearMap.sub_apply", "sub_apply", 'BC-2'),
    ("add_le_add_right h2 _", "add_le_add_left h2 _", 'BC-3'),
    ("add_le_add_right h5 _", "add_le_add_left h5 _", 'BC-3'),
    ("  rw [lipschitzOnWith_iff_dist_le_mul]\n  intro x hx y hy", "  refine LipschitzOnWith.of_dist_le_mul ?_\n  intro x hx y hy", 'BC-4'),
    ("  have hL := D.lipschitzOnWith_vf x₁ hR\n  rw [lipschitzOnWith_iff_dist_le_mul] at hL", "  have hL := (D.lipschitzOnWith_vf x₁ hR).dist_le_mul", 'BC-4'),
    ("Uniqueness", "    simpa using e\n", "    have e' : ‖D.vf (x s) - D.vf (y s)‖ ≤\n        (D.ν * ‖D.A‖ + 2 * ‖D.B‖ * (‖x₁‖ + R)) * ‖x s - y s‖ := e\n    simpa using e'\n", "BC-11b"),
    (".mono_of_mem ", ".mono_of_mem_nhdsWithin ", 'BC-7'),
    ("simpa only [slope, smul_eq_mul] using h", "simpa only [slope, smul_eq_mul, vsub_eq_sub] using h", 'BC-8'),
    ("le_of_not_le h1", "(not_le.mp h1).le", 'BC-9'),
    ("ExplicitB", "def B3fun (u v : ModeSpace 1) : ModeSpace 1 :=\n  ![u 1 * v 2 + u 2 * v 1, -(u 0 * v 2 + u 2 * v 0), 0]",
     "def B3fun (u v : ModeSpace 1) : ModeSpace 1 :=\n  WithLp.toLp 2 ![u 1 * v 2 + u 2 * v 1, -(u 0 * v 2 + u 2 * v 0), 0]", "BC-12a"),
    ("ExplicitB", "funext i", "ext i", "BC-12b"),
    ("ExplicitB", "simp [B3fun, PiLp.add_apply,", "simp [B3fun, PiLp.toLp_apply, PiLp.add_apply,", "BC-12c"),
    ("ExplicitB", "simp [B3fun, PiLp.smul_apply,", "simp [B3fun, PiLp.toLp_apply, PiLp.smul_apply,", "BC-12c"),
    ("ExplicitB", "simp [B3fun, Matrix.cons_val_zero]", "simp [B3fun, PiLp.toLp_apply, Matrix.cons_val_zero]", "BC-12c"),
    ("ExplicitB", "simp [B3fun, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_zero]",
     "simp [B3fun, PiLp.toLp_apply, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_zero]", "BC-12c"),
    ("ExplicitB", "simp [B3fun, Matrix.cons_val_two, Matrix.head_cons, Matrix.cons_val_one,",
     "simp [B3fun, PiLp.toLp_apply, Matrix.cons_val_two, Matrix.head_cons, Matrix.cons_val_one,", "BC-12c"),
    ("ExplicitB", ":= abs_add _ _", ":= abs_add_le _ _", "BC-13"),
    ("ExplicitB", "    B3fun, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,\n    Matrix.cons_val_two, Matrix.tail_cons]",
     "    PiLp.toLp_apply, B3fun, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,\n    Matrix.cons_val_two, Matrix.tail_cons]", "BC-12d"),
    ("CapAnchor", "def capLin (P : CapParams) (u : ModeSpace 1) : ModeSpace 1 :=\n  ![P.ν * (P.a 0 * u 0), P.ν * (P.a 1 * u 1), P.ν * (P.a 2 * u 2)]",
     "def capLin (P : CapParams) (u : ModeSpace 1) : ModeSpace 1 :=\n  WithLp.toLp 2 ![P.ν * (P.a 0 * u 0), P.ν * (P.a 1 * u 1), P.ν * (P.a 2 * u 2)]", "BC-14a"),
    ("CapAnchor", "    capF P u = ![u 1 * u 2 + u 2 * u 1 - P.ν * (P.a 0 * u 0) + P.f 0,\n                -(u 0 * u 2 + u 2 * u 0) - P.ν * (P.a 1 * u 1) + P.f 1,\n                -P.ν * (P.a 2 * u 2) + P.f 2] := by\n  funext i",
     "    capF P u = WithLp.toLp 2 ![u 1 * u 2 + u 2 * u 1 - P.ν * (P.a 0 * u 0) + P.f 0,\n                -(u 0 * u 2 + u 2 * u 0) - P.ν * (P.a 1 * u 1) + P.f 1,\n                -P.ν * (P.a 2 * u 2) + P.f 2] := by\n  ext i", "BC-14b"),
    ("CapAnchor", "simp [capF, capLin, B3fun, PiLp.sub_apply, PiLp.add_apply,",
     "simp [capF, capLin, B3fun, PiLp.toLp_apply, PiLp.sub_apply, PiLp.add_apply,", "BC-14b"),
    ("CapAnchor", "  f := ![1, 0.5, -0.25]", "  f := WithLp.toLp 2 ![1, 0.5, -0.25]", "BC-14c"),
    ("CapAnchor", "def capCenterP1 : ModeSpace 1 := ![0.6, 0.8, -0.25]",
     "def capCenterP1 : ModeSpace 1 := WithLp.toLp 2 ![0.6, 0.8, -0.25]", "BC-14c"),
    ("CapAnchor", "  funext i\n  fin_cases i <;>\n    simp [capF, capLin, GalerkinNS.vf, explicitData3, capParamsP1, B3fun, B3_apply,",
     "  ext i\n  fin_cases i <;>\n    simp [capF, capLin, GalerkinNS.vf, explicitData3, capParamsP1, B3fun, B3_apply,\n      PiLp.toLp_apply,", "BC-14d"),
    ("ExplicitB", "\n  rw [Fin.succ_zero_eq_one', Fin.succ_zero_eq_one', Fin.succ_one_eq_two']\n  ring",
     "\n  ring", "BC-15")
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
