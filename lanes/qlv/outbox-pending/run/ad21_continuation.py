import json, sys, itertools, math, time
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent.parent
RUN = BASE/'run'
sys.path.insert(0, str(RUN))
from ad21_tangent import (ts, TARGETS, ALPHA, form_from_sphere, target_of, polish,
                          outside_fraction, pm3)

TANGENT = json.loads((RUN/'ad21_tangent.json').read_text())
OUT = RUN/'ad21_continuation.jsonl'


def emit(f, case, kind, p, e, nfev, status, H, **spec):
    rec = {'case': case['name'], 'form': case['form'], 'idx': case['idx'], 'kind': kind,
           'e': float(e), 'nfev': int(nfev), 'status': int(status),
           'H_involution_max': float(np.max(np.abs(H@H-np.eye(8)))),
           'x': np.asarray(p).tolist(), **spec}
    if kind == 'outside':
        rec['outside_ratio'], rec['outside_norm'] = outside_fraction(case['form'], spec['delta_H'])
        del rec['delta_H']
    f.write(json.dumps(rec, separators=(',', ':'))+'\n')
    f.flush()
    return rec


def solve_step(f, case, kind, p, H, **spec):
    seq = list(itertools.product(ts.PATH, repeat=7))[case['idx']]
    target = TARGETS[case['form']]
    p2, e, nfev, status = polish(p, seq, target_of(H, target, spec.get('alpha', ALPHA)),
                                 max_nfev=spec.pop('max_nfev', 1800))
    return p2, emit(f, case, kind, p2, e, nfev, status, H, **spec)


def theta_navigation(f, case, p0, theta0, phi0, theta1):
    p = p0
    n = max(1, int(math.ceil(abs(theta1-theta0)/(np.pi/24))))
    records = []
    for j in range(1, n+1):
        th = theta0 + (theta1-theta0)*j/n
        H = form_from_sphere(case['form'], th, phi0)
        p, rec = solve_step(f, case, 'theta_navigation', p, H, theta=th, phi=phi0, alpha=ALPHA)
        records.append(rec)
        if rec['e'] >= 1e-8:
            break
    return p, records


def run_case(f, case):
    form = case['form']
    p0 = np.asarray(case['x_polished'])
    th0, ph0 = case['theta'], case['phi']
    H0 = form_from_sphere(form, th0, ph0)
    seq = list(itertools.product(ts.PATH, repeat=7))[case['idx']]
    # 角度单独变化：与S²方向及Pauli共轭严格隔离。
    for sign in [-1, 1]:
        for delta in [0.001, 0.005, 0.01, 0.05, 0.1, 0.2]:
            alpha = ALPHA + sign*delta
            solve_step(f, case, 'alpha_scan', p0, H0, theta=th0, phi=ph0,
                       alpha=alpha, delta_alpha=sign*delta, max_nfev=2200)
    # 六个纬圈，每圈12步闭回；另逼近并直达两个极点。
    theta_values = [th0, 0.05, np.pi/4, np.pi/2, 3*np.pi/4, np.pi-0.05]
    for th in theta_values:
        p, nav = theta_navigation(f, case, p0, th0, ph0, th)
        if nav and nav[-1]['e'] >= 1e-8:
            continue
        p_loop = p
        for j in range(1, 13):
            ph = ph0 + 2*np.pi*j/12
            H = form_from_sphere(form, th, ph)
            p_loop, rec = solve_step(f, case, 'phi_loop', p_loop, H,
                                     theta=th, phi=ph, alpha=ALPHA,
                                     latitude_origin=th0, loop_steps=12)
            if rec['e'] >= 1e-8:
                break
    for pole in [0.0, np.pi]:
        p, nav = theta_navigation(f, case, p0, th0, ph0, pole)
    # 选一切向可动且完全离开ansatz的Pauli共轭，向两侧各走24步至±π/2。
    candidates = [r for r in case['outside_candidates']
                  if r['outside_ratio'] > 0.99 and r['projection_residual_ratio'] < 1e-8]
    if candidates:
        chosen = candidates[0]
        P = pm3(chosen['pauli'])
        for sign in [-1, 1]:
            p = p0
            for j in range(1, 25):
                eps = sign*(np.pi/2)*j/24
                C = np.cos(eps)*np.eye(8) + 1j*np.sin(eps)*P
                H = C @ H0 @ C.conj().T
                delta_H = 1j*(P@H-H@P)
                p, rec = solve_step(f, case, 'outside', p, H, theta=th0, phi=ph0,
                                    alpha=ALPHA, pauli=chosen['pauli'], epsilon=eps,
                                    delta_H=delta_H)
                if rec['e'] >= 1e-8:
                    break


def main():
    t0 = time.time()
    with OUT.open('w', buffering=1) as f:
        for case in TANGENT['cases']:
            run_case(f, case)
            print(json.dumps({'event': 'case_done', 'case': case['name'], 'elapsed': time.time()-t0}), flush=True)
    rows = [json.loads(s) for s in OUT.read_text().splitlines() if s.strip()]
    summary = {'beat': 'AD-21', 'records': len(rows), 'seconds': time.time()-t0, 'groups': {}}
    for case in TANGENT['cases']:
        for kind in sorted({r['kind'] for r in rows if r['case'] == case['name']}):
            rr = [r for r in rows if r['case'] == case['name'] and r['kind'] == kind]
            summary['groups'][case['name']+'/'+kind] = {
                'count': len(rr), 'success_e_lt_1e-8': sum(r['e'] < 1e-8 for r in rr),
                'e_min': min(r['e'] for r in rr), 'e_max': max(r['e'] for r in rr),
                'outside_ratio_max': max([r.get('outside_ratio', 0) for r in rr]),
            }
    (RUN/'ad21_continuation_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
