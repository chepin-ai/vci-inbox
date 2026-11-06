import os, sys, json, time, itertools, argparse
import numpy as np
from scipy.optimize import least_squares

BASE = os.environ.get('QLV_AD20_BASE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)
import toffoli_solver as ts

T = ts.toffoli({0, 2}, 1)
SEQS = list(itertools.product(ts.PATH, repeat=7))


def one_restart(idx, r):
    seq = [tuple(e) for e in SEQS[idx]]
    seed = 200000 + idx * 16 + r
    rng = np.random.default_rng(seed)
    p0 = rng.normal(scale=1.5, size=73)
    ts._cache.clear()
    t0 = time.time()
    sol = least_squares(ts.f_resid, p0, jac=ts.j_resid,
                        args=(seq, T.reshape(-1)), method='lm', max_nfev=2500,
                        ftol=1e-15, xtol=1e-15, gtol=1e-15)
    e = float(np.max(np.abs(sol.fun[:64] + 1j * sol.fun[64:])))
    return {'idx': idx, 'restart': r, 'seed': seed, 'e': e,
            'nfev': int(sol.nfev), 'status': int(sol.status),
            'optimality': float(sol.optimality), 'seconds': time.time() - t0,
            'x': sol.x.tolist()}


def scan_seq(idx, restarts):
    rows = [one_restart(idx, r) for r in range(restarts)]
    best = min(rows, key=lambda z: z['e'])
    return {'idx': idx, 'edges': SEQS[idx], 'best': best,
            'restart_e': [z['e'] for z in rows]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--stop', type=int, default=128)
    ap.add_argument('--restarts', type=int, default=5)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--out', default=BASE + '/run/ad20_g2k7_scan.jsonl')
    args = ap.parse_args()
    done = set()
    if os.path.exists(args.out):
        with open(args.out) as f:
            for line in f:
                if line.strip():
                    done.add(json.loads(line)['idx'])
    indices = [i for i in range(args.start, args.stop) if i not in done]
    print(json.dumps({'event': 'start', 'start': args.start, 'stop': args.stop,
                      'restarts': args.restarts, 'workers': args.workers,
                      'already_done': len(done), 'todo': len(indices)}), flush=True)
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor, as_completed
    with open(args.out, 'a', buffering=1) as f:
        with ProcessPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(scan_seq, i, args.restarts): i for i in indices}
            n = 0
            for fut in as_completed(futs):
                i = futs[fut]
                try:
                    row = fut.result()
                except Exception as exc:
                    row = {'idx': i, 'error': type(exc).__name__ + ': ' + str(exc)}
                f.write(json.dumps(row, separators=(',', ':')) + '\n')
                n += 1
                if 'error' in row:
                    print(json.dumps({'event': 'error', **row}), flush=True)
                elif n % 4 == 0 or n == len(indices):
                    print(json.dumps({'event': 'progress', 'done_this_run': n,
                                      'idx': i, 'e': row['best']['e'],
                                      'elapsed': time.time() - t0}), flush=True)
    print(json.dumps({'event': 'done', 'seconds': time.time() - t0}), flush=True)

if __name__ == '__main__':
    main()
