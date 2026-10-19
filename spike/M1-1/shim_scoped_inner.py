# CLASSIFY: L1
"""M1-1 spike helper: insert `open scoped InnerProductSpace` after the last top-level
import line of every file that uses the inner-product notation and lacks the open.
(mathlib v4.10.0 -> v4.35.0 made inner notation scoped[InnerProductSpace].)"""
import pathlib, sys

def shim(path):
    p = pathlib.Path(path)
    t = p.read_text()
    if '⟪' not in t or 'open scoped InnerProductSpace' in t:
        return False
    lines = t.split('\n')
    imp = [i for i, l in enumerate(lines) if l.startswith('import ')]
    if not imp:
        return False
    lines.insert(imp[-1] + 1, 'open scoped InnerProductSpace')
    p.write_text('\n'.join(lines))
    return True

if __name__ == '__main__':
    for a in sys.argv[1:]:
        print(('shimmed  ' if shim(a) else 'skipped  ') + a)
