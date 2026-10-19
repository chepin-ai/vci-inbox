# CLASSIFY: L1
"""M1-1 spike migration-candidate patcher: Lean/mathlib v4.10.0 -> v4.35.0.
Applies (idempotently):
  BC-1  scoped inner notation -> insert `open scoped InnerProductSpace` after last import
  BC-2  ContinuousLinearMap.sub_apply (deprecated) -> sub_apply
  BC-3  add_le_add_right semantic flip (constant now added on the LEFT) -> add_le_add_left
        at the two known call sites (h2, h5 in Basic.norm_vf_le / lipschitzOnWith_vf)
  BC-4  rw [lipschitzOnWith_iff_dist_le_mul] instance-diamond failure ->
        alias forms LipschitzOnWith.of_dist_le_mul / .of_dist_le_mul projection
Each applied edit is printed for the breaking-change ledger."""
import pathlib, sys

TEXT_EDITS = [
    ('ContinuousLinearMap.sub_apply', 'sub_apply', 'BC-2'),
    ('add_le_add_right h2 _', 'add_le_add_left h2 _', 'BC-3'),
    ('add_le_add_right h5 _', 'add_le_add_left h5 _', 'BC-3'),
    ('  rw [lipschitzOnWith_iff_dist_le_mul]\n  intro x hx y hy',
     '  refine LipschitzOnWith.of_dist_le_mul ?_\n  intro x hx y hy', 'BC-4'),
    ('  have hL := D.lipschitzOnWith_vf x₁ hR\n  rw [lipschitzOnWith_iff_dist_le_mul] at hL',
     '  have hL := (D.lipschitzOnWith_vf x₁ hR).of_dist_le_mul', 'BC-4'),
]

def patch(path):
    p = pathlib.Path(path)
    t = p.read_text()
    orig = t
    for old, new, tag in TEXT_EDITS:
        if old in t:
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
