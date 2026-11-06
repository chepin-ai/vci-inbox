import os, sys, json, time, itertools, argparse
import numpy as np
from scipy.optimize import least_squares
from concurrent.futures import ProcessPoolExecutor, as_completed

BASE = os.environ.get('QLV_AD20_BASE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)
import toffoli_solver as ts
SEQS = list(itertools.product(ts.PATH, repeat=7))
TARGETS = {'G1': ts.toffoli({0, 1}, 2), 'G2': ts.toffoli({0, 2}, 1)}


def solve(task):
    geometry, idx, r = task
    seq = [tuple(e) for e in SEQS[idx]]
    seed = 700000 + idx * 64 + r
    rng = np.random.default_rng(seed)
    p0 = rng.normal(scale=1.5, size=73)
    ts._cache.clear()
    t0 = time.time()
    sol = least_squares(ts.f_resid, p0, jac=ts.j_resid,
                        args=(seq, TARGETS[geometry].reshape(-1)), method='lm',
                        max_nfev=2500, ftol=1e-15, xtol=1e-15, gtol=1e-15)
    e = float(np.max(np.abs(sol.fun[:64] + 1j * sol.fun[64:])))
    return {'geometry': geometry, 'idx': idx, 'restart': r, 'seed': seed,
            'e': e, 'nfev': int(sol.nfev), 'status': int(sol.status),
            'optimality': float(sol.optimality), 'seconds': time.time() - t0,
            'x': sol.x.tolist()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=BASE + '/run/ad20_targeted.jsonl')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--restarts', type=int, default=40)
    args = ap.parse_args()
    tasks = [('G2', idx, r) for idx in [91, 34, 38, 52]
             for r in range(args.restarts)]
    tasks += [('G1', 85, r) for r in range(args.restarts)]
    t0 = time.time()
    print(json.dumps({'event': 'start', 'tasks': len(tasks),
                      'restarts': args.restarts, 'workers': args.workers}), flush=True)
    with open(args.out, 'w', buffering=1) as f:
        with ProcessPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(solve, t): t for t in tasks}
            n = 0
            for fut in as_completed(futs):
                task = futs[fut]
                try:
                    row = fut.result()
                except Exception as exc:
                    row = {'geometry': task[0], 'idx': task[1], 'restart': task[2],
                           'error': type(exc).__name__ + ': ' + str(exc)}
                f.write(json.dumps(row, separators=(',', ':')) + '\n')
                n += 1
                if 'error' in row:
                    print(json.dumps({'event': 'error', **row}), flush=True)
                elif n % 20 == 0 or n == len(tasks):
                    print(json.dumps({'event': 'progress', 'done': n,
                                      'elapsed': time.time() - t0}), flush=True)
    print(json.dumps({'event': 'done', 'seconds': time.time() - t0}), flush=True)

if __name__ == '__main__':
    main()
