import sys, json, time, itertools, os
import numpy as np
from scipy.optimize import least_squares
BASE = os.environ.get('QLV_AD20_BASE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)
import toffoli_solver as ts
rows = [json.loads(l) for l in open(BASE + '/run/ad20_targeted.jsonl') if l.strip()]
rows = [r for r in rows if r.get('geometry') == 'G1' and r['idx'] == 85]
best = min(rows, key=lambda r: r['e'])
p0 = np.array(best['x'])
seq = list(itertools.product(ts.PATH, repeat=7))[85]
T = ts.toffoli({0, 1}, 2)
ts._cache.clear()
t0 = time.time()
sol = least_squares(ts.f_resid, p0, jac=ts.j_resid, args=(seq, T.reshape(-1)),
                    method='lm', max_nfev=10000,
                    ftol=1e-15, xtol=1e-15, gtol=1e-15)
e = float(np.max(np.abs(sol.fun[:64] + 1j * sol.fun[64:])))
out = {'geometry': 'G1', 'idx': 85, 'e': e, 'nfev': int(sol.nfev),
       'status': int(sol.status), 'optimality': float(sol.optimality),
       'seconds': time.time() - t0, 'initial_e': best['e'], 'x': sol.x.tolist()}
with open(BASE + '/run/ad20_g1k7_polish.json', 'w') as f:
    json.dump(out, f, separators=(',', ':'))
np.save(BASE + '/run/ad20_g1k7_polish.npy', sol.x)
print(json.dumps({k: v for k, v in out.items() if k != 'x'}), flush=True)
