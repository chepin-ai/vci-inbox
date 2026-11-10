"""AD-22 全候选 ansatz 外方向二阶障碍扫描。
预注册：先过 theta/phi 已知答案门；外方向须 outside_ratio>.99 且一阶投影比<1e-8。
每个方向以零点和确定独立种子优化零空间二次方程；只报局部数值证书，不报全局不存在。
"""
import itertools, json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from scipy.linalg import qr

AD21 = Path('/mnt/agents/output/.stash/ad21/run')
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(AD21))
from ad21_tangent import (ts, TARGETS, ALPHA, form_from_sphere, sphere_derivatives,
                          form_terms, target_of, realvec, pm3)
TAN = json.loads((AD21/'ad21_tangent.json').read_text())
SEEDS = [0, 2201, 2202, 2203, 2204, 2205]


def setup_case(case):
    form = case['form']; p0 = np.asarray(case['x_polished'], float)
    seq = list(itertools.product(ts.PATH, repeat=7))[case['idx']]
    th, ph = case['theta'], case['phi']
    H0 = form_from_sphere(form, th, ph); T = TARGETS[form]; V0 = target_of(H0, T)
    _, J = ts.f_j(p0, seq, V0.reshape(-1))
    U, s, Vh = np.linalg.svd(J, full_matrices=True)
    rank = int(np.sum(s > s[0]*1e-10)); Q = U[:, rank:]; N = Vh[rank:].T
    return dict(case=case, form=form, p0=p0, seq=seq, th=th, ph=ph, H0=H0, T=T,
                V0=V0, J=J, Q=Q, N=N, rank=rank)


def direction(st, kind, pauli=None):
    th, ph, form, H0, T = st['th'], st['ph'], st['form'], st['H0'], st['T']
    if kind in ('theta', 'phi'):
        dth, dph = sphere_derivatives(form, th, ph)
        dH = dth if kind == 'theta' else dph
        if kind == 'theta':
            H2 = form_terms(form, -np.cos(th)/2, -np.cos(th)/2,
                            -np.sin(th)*np.cos(ph)/2, -np.sin(th)*np.sin(ph)/2)
        else:
            w = np.sin(th)*np.cos(ph)/2; t = np.sin(th)*np.sin(ph)/2
            H2 = form_terms(form, 0, 0, -w, -t)
    else:
        P = pm3(pauli); dH = 1j*(P@H0-H0@P); H2 = 2*(P@H0@P-H0)
    d = realvec(1j*np.sin(ALPHA)*dH@T)
    v2 = realvec(1j*np.sin(ALPHA)*H2@T)
    p10, *_ = np.linalg.lstsq(st['J'], d, rcond=1e-11)
    return d, v2, p10


def solve_second_order(st, kind, pauli=None, h=1e-4):
    d, v2, p10 = direction(st, kind, pauli)
    J, Q, N, p0, seq, V0 = st['J'], st['Q'], st['N'], st['p0'], st['seq'], st['V0']
    tv = V0.reshape(-1)
    cache = {}
    def parts(zv, hh=h):
        key = (zv.tobytes(), hh)
        if key in cache: return cache[key]
        p1 = p10 + N@zv
        Jp = ts.f_j(p0+hh*p1, seq, tv)[1]
        Jm = ts.f_j(p0-hh*p1, seq, tv)[1]
        D2 = (Jp@p1-Jm@p1)/(2*hh)
        # d[Q^T(B(p1,p1)-v2)]/dz = 2 Q^T B(p1,N)
        BN = (Jp@N-Jm@N)/(2*hh)
        rr = D2-v2
        fun = Q.T@rr
        jac = 2*(Q.T@BN)
        cache[key] = (fun, jac, rr, p1)
        return cache[key]
    starts = [np.zeros(N.shape[1])]
    for seed in SEEDS[1:]:
        rng = np.random.default_rng(seed)
        starts.append(rng.normal(scale=0.7, size=N.shape[1]))
    runs = []
    for si, z0 in enumerate(starts):
        t0 = time.time()
        sol = least_squares(lambda z: parts(z)[0], z0, jac=lambda z: parts(z)[1],
                            max_nfev=500, ftol=1e-13, xtol=1e-13, gtol=1e-13)
        fun, jac, rr, p1 = parts(sol.x)
        runs.append({'start_index': si, 'seed': SEEDS[si], 'cokernel_norm': float(np.linalg.norm(fun)),
                     'rhs_norm': float(np.linalg.norm(rr)), 'nfev': int(sol.nfev),
                     'status': int(sol.status), 'optimality': float(sol.optimality),
                     'seconds': time.time()-t0, 'z': sol.x.tolist()})
    best = min(runs, key=lambda r: r['cokernel_norm'])
    # 差分稳定性只复算最优零空间点，避免把停止码当证书。
    zbest = np.asarray(best['z']); stability = []
    for hh in [1e-3, 3e-4, 1e-4, 3e-5, 1e-5]:
        stability.append({'h': hh, 'cokernel_norm': float(np.linalg.norm(parts(zbest, hh)[0]))})
    return {'kind': kind, 'pauli': pauli, 'rank': st['rank'], 'nullity': N.shape[1],
            'first_order_residual_ratio': float(np.linalg.norm(J@p10-d)/np.linalg.norm(d)),
            'best_cokernel_norm': best['cokernel_norm'], 'best_rhs_norm': best['rhs_norm'],
            'best_start_index': best['start_index'], 'all_starts_min': min(r['cokernel_norm'] for r in runs),
            'all_starts_max': max(r['cokernel_norm'] for r in runs), 'runs': runs,
            'finite_difference_stability': stability}


def main():
    rows = []; independent = {}
    for case in TAN['cases']:
        st = setup_case(case)
        for kind in ('theta', 'phi'):
            r = solve_second_order(st, kind); r['case'] = case['name']; rows.append(r)
            print(json.dumps({'case': r['case'], 'kind': kind, 'best': r['best_cokernel_norm']}), flush=True)
        cand = [x for x in case['outside_candidates']
                if x['outside_ratio'] > .99 and x['projection_residual_ratio'] < 1e-8]
        B = np.column_stack([direction(st, 'outside', x['pauli'])[0] for x in cand])
        ss = np.linalg.svd(B, compute_uv=False)
        _, _, piv = qr(B, pivoting=True, mode='economic')
        drank = int(np.sum(ss > ss[0]*1e-10))
        independent[case['name']] = {'candidate_count': len(cand), 'direction_rank': drank,
                                     'singular_values': ss.tolist(),
                                     'independent_pauli': [cand[i]['pauli'] for i in piv[:drank]]}
        for x in cand:
            r = solve_second_order(st, 'outside', x['pauli']); r['case'] = case['name']; rows.append(r)
            print(json.dumps({'case': r['case'], 'pauli': x['pauli'], 'best': r['best_cokernel_norm'],
                              'start': r['best_start_index']}), flush=True)
    gates = {r['case']+'/'+r['kind']: r['best_cokernel_norm'] for r in rows if r['kind'] in ('theta','phi')}
    outside = [r for r in rows if r['kind'] == 'outside']
    assert all(v < 1e-6 for v in gates.values()), gates
    assert all(r['first_order_residual_ratio'] < 1e-8 for r in outside)
    out = {'beat': 'AD-22', 'protocol': 'all eligible Pauli directions; six deterministic nullspace starts',
           'known_answer_gate': gates, 'independent_directions': independent, 'rows': rows,
           'outside_summary': [{'case': r['case'], 'pauli': r['pauli'],
                                'best_cokernel_norm': r['best_cokernel_norm'],
                                'best_start_index': r['best_start_index']} for r in outside],
           'boundary': '固定秩阈值、中心差分及六个起点的局部数值证书；不是零空间二次方程的全局不存在证明。'}
    (RUN/'ad22_outside_all.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'gate_max': max(gates.values()), 'outside_min': min(r['best_cokernel_norm'] for r in outside),
                      'outside_count': len(outside), 'independent': independent}, indent=2))

if __name__ == '__main__': main()
