"""AD-21 独立验收器。

不导入求解器或分析模块；从原始 JSON/JSONL 的角度、边序与目标参数重建。
所有电路残差均为 max(abs(U-target))；优化器 status 不作成功判据。
"""
import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2

RUN = Path(__file__).resolve().parent
ALPHA = np.pi / 8
I2 = np.eye(2, dtype=complex)
PAULI = {
    'I': I2,
    'X': np.array([[0, 1], [1, 0]], complex),
    'Y': np.array([[0, -1j], [1j, 0]], complex),
    'Z': np.diag([1, -1]).astype(complex),
}
PATH = [(0, 1), (1, 2)]
SEQS = {k: list(itertools.product(PATH, repeat=k)) for k in [7]}


def load(name):
    return json.loads((RUN / name).read_text())


def loadl(name):
    return [json.loads(s) for s in (RUN / name).read_text().splitlines() if s.strip()]


def pm(s):
    return np.kron(np.kron(PAULI[s[0]], PAULI[s[1]]), PAULI[s[2]])


def rz(a):
    return np.diag([np.exp(-0.5j * a), np.exp(0.5j * a)])


def ry(a):
    return np.array([[np.cos(a / 2), -np.sin(a / 2)],
                     [np.sin(a / 2), np.cos(a / 2)]], complex)


def su2(t):
    return rz(t[0]) @ ry(t[1]) @ rz(t[2])


def local_layer(t):
    return np.kron(np.kron(su2(t[0]), su2(t[1])), su2(t[2]))


def cz(edge):
    a, b = edge
    d = np.ones(8, complex)
    for x in range(8):
        if ((x >> (2 - a)) & 1) and ((x >> (2 - b)) & 1):
            d[x] = -1
    return np.diag(d)


def layers_of(p, edges):
    k = len(edges)
    assert len(p) == 1 + 9 * (k + 1)
    return np.asarray(p[1:], float).reshape(k + 1, 3, 3)


def circuit(p, edges):
    """U=e^{i phase} L_k CZ_{k-1} L_{k-1} ... CZ_0 L_0."""
    p = np.asarray(p, float)
    edges = [tuple(e) for e in edges]
    th = layers_of(p, edges)
    U = np.exp(1j * p[0]) * local_layer(th[-1])
    for j in range(len(edges) - 1, -1, -1):
        U = U @ cz(edges[j]) @ local_layer(th[j])
    return U


def toffoli(controls, target):
    T = np.zeros((8, 8), complex)
    for x in range(8):
        b = [(x >> 2) & 1, (x >> 1) & 1, x & 1]
        if all(b[q] for q in controls):
            b[target] ^= 1
        y = (b[0] << 2) | (b[1] << 1) | b[2]
        T[y, x] = 1
    return T


TARGETS = {'G1': toffoli({0, 1}, 2), 'G2': toffoli({0, 2}, 1)}


def sname(a, b, c, sa, sb):
    s = ['I'] * 3
    s[a], s[b], s[c] = sa, sb, 'Z'
    return ''.join(s)


def basis_names(perm):
    a, b, c = perm
    return [sname(a, b, c, 'Z', 'X'), sname(a, b, c, 'Z', 'I'),
            sname(a, b, c, 'Y', 'I'), sname(a, b, c, 'X', 'I'),
            sname(a, b, c, 'Y', 'X'), sname(a, b, c, 'X', 'X')]


def sphere(perm, sigma, theta, phi):
    n = basis_names(perm)
    u = (sigma + np.cos(theta)) / 2
    v = (np.cos(theta) - sigma) / 2
    w = np.sin(theta) * np.cos(phi) / 2
    t = np.sin(theta) * np.sin(phi) / 2
    return (u * pm(n[0]) + v * pm(n[1]) + w * (pm(n[2]) + pm(n[4]))
            + t * (pm(n[3]) + pm(n[5])))


def target_of(H, T, alpha=ALPHA):
    return (np.cos(alpha) * np.eye(8) + 1j * np.sin(alpha) * H) @ T


def realvec(M):
    z = np.asarray(M).reshape(-1)
    return np.concatenate([z.real, z.imag])


def outside_fraction(perm, dH):
    B = np.column_stack([realvec(pm(s)) for s in basis_names(perm)])
    d = realvec(dH)
    coef, *_ = np.linalg.lstsq(B, d, rcond=None)
    out = d - B @ coef
    return float(np.linalg.norm(out) / np.linalg.norm(d)), float(np.linalg.norm(out))


def extract_H(x, idx, T):
    U = circuit(x, SEQS[7][idx])
    vals, vecs = np.linalg.eig(U @ T)
    angles = np.angle(vals)
    K = vecs @ np.diag(angles) @ np.linalg.inv(vecs)
    H = K / ALPHA
    H = (H + H.conj().T) / 2
    return H, angles, float(np.max(np.abs(U - T)))


def fit_one(H, perm, sigma):
    names = basis_names(perm)
    co = np.array([float((np.trace(pm(s) @ H) / 8).real) for s in names])
    u, v, w, t = co[:4]
    theta = float(np.arccos(np.clip(u + v, -1, 1)))
    phi = float(np.arctan2(t, w))
    H0 = sphere(perm, sigma, theta, phi)
    return {'perm': list(perm), 'sigma': int(sigma), 'theta': theta, 'phi': phi,
            'delta': float(np.max(np.abs(H - H0))),
            'H0_involution': float(np.max(np.abs(H0 @ H0 - np.eye(8))))}


def fits(H):
    ans = [fit_one(H, p, s) for p in itertools.permutations(range(3)) for s in [1, -1]]
    return sorted(ans, key=lambda r: r['delta'])


def classify(x, idx, T):
    H, angles, direct = extract_H(x, idx, T)
    ff = fits(H)
    best = ff[0]
    c = {'direct_e_rebuilt': direct,
         'angle_max_dev_rad': float(np.max(np.abs(np.abs(angles) - ALPHA))),
         'H_involution_max': float(np.max(np.abs(H @ H - np.eye(8)))),
         'best_perm': best['perm'], 'best_sigma': best['sigma'],
         'best_ansatz_max_delta': best['delta'],
         'runner_up_ansatz_max_delta': ff[1]['delta']}
    return c


def basin_hit(e, c):
    return bool(e < .205 and c['angle_max_dev_rad'] < 1e-5 and c['H_involution_max'] < 1e-4
                and c['best_perm'] == [2, 1, 0] and c['best_sigma'] == -1
                and c['best_ansatz_max_delta'] < 1e-4)


def close(a, b, tol=2e-10):
    return bool(np.isfinite(a) and np.isfinite(b) and abs(a - b) <= tol * max(1., abs(a), abs(b)))


def known_answer_gate():
    rng = np.random.default_rng(210021)
    max_u = 0.
    max_id = 0.
    for k in [0, 1, 2, 7]:
        edges = list(next(itertools.product(PATH, repeat=k))) if k else []
        # 对 k=7 使用确定但非平凡的边序。
        if k == 7:
            edges = [PATH[(3 * j + 1) % 2] for j in range(k)]
        p = rng.normal(size=1 + 9 * (k + 1))
        U = circuit(p, edges)
        max_u = max(max_u, float(np.max(np.abs(U @ U.conj().T - np.eye(8)))))
        max_id = max(max_id, float(np.max(np.abs(circuit(p, edges) - U))))
    assert max_u < 3e-14 and max_id == 0
    max_sphere = 0.
    for perm in itertools.permutations(range(3)):
        for sigma in [-1, 1]:
            for th in np.linspace(0.02, np.pi - .02, 7):
                for ph in np.linspace(-np.pi, np.pi, 8, endpoint=False):
                    H = sphere(perm, sigma, th, ph)
                    max_sphere = max(max_sphere, float(np.max(np.abs(H @ H - np.eye(8)))))
                    assert np.array_equal(target_of(H, TARGETS['G1'], 0), TARGETS['G1'])
    assert max_sphere < 3e-14
    return {'random_circuit_unitary_max': max_u,
            'random_circuit_rebuild_max': max_id,
            'sphere_involution_max': max_sphere,
            'random_circuit_cases': 4, 'sphere_cases': 6 * 2 * 7 * 8}


def verify_continuation(tan, base91):
    cases = {c['name']: c for c in tan['cases']}
    specs = {}
    for c in cases.values():
        specs[c['name']] = {'perm': (1, 2, 0) if c['form'] == 'G1' else (0, 1, 2),
                            'sigma': 1, 'theta': c['theta'], 'phi': c['phi']}
    specs['G2k7_seq91'] = {'perm': tuple(base91['perm']), 'sigma': base91['sigma'],
                           'theta': base91['theta'], 'phi': base91['phi']}
    groups = {}
    max_de = max_du = max_dh = max_dr = 0.
    total = 0
    success = 0
    for filename in ['ad21_continuation.jsonl', 'ad21_seq91_continuation.jsonl']:
        for r in loadl(filename):
            sp = specs[r['case']]
            H0 = sphere(sp['perm'], sp['sigma'], sp['theta'], sp['phi'])
            if r['kind'] in ['outside', 'outside_fine']:
                P = pm(r['pauli'])
                eps = r['epsilon']
                C = np.cos(eps) * np.eye(8) + 1j * np.sin(eps) * P
                H = C @ H0 @ C.conj().T
                dH = 1j * (P @ H - H @ P)
                ratio, _ = outside_fraction(sp['perm'], dH)
                max_dr = max(max_dr, abs(ratio - r['outside_ratio']))
            else:
                H = sphere(sp['perm'], sp['sigma'], r['theta'], r['phi'])
            V = target_of(H, TARGETS[r['form']], r['alpha'])
            U = circuit(r['x'], SEQS[7][r['idx']])
            e = float(np.max(np.abs(U - V)))
            hi = float(np.max(np.abs(H @ H - np.eye(8))))
            du = float(np.max(np.abs(U @ U.conj().T - np.eye(8))))
            assert close(e, r['e'], 3e-11), (filename, r['case'], r['kind'], e, r['e'])
            assert close(hi, r['H_involution_max'], 3e-11)
            assert du < 3e-13
            max_de, max_du, max_dh = max(max_de, abs(e-r['e'])), max(max_du, du), max(max_dh, abs(hi-r['H_involution_max']))
            key = r['case'] + '/' + r['kind']
            g = groups.setdefault(key, {'n': 0, 'success': 0, 'e_min': np.inf, 'e_max': 0.})
            g['n'] += 1
            g['success'] += int(e < 1e-8)
            g['e_min'], g['e_max'] = min(g['e_min'], e), max(g['e_max'], e)
            total += 1
            success += int(e < 1e-8)
    assert total == 450 and max_dr < 2e-10
    return {'records': total, 'success_e_lt_1e-8': success,
            'max_abs_e_record_minus_rebuild': max_de,
            'max_circuit_unitarity_error': max_du,
            'max_abs_H_involution_record_minus_rebuild': max_dh,
            'max_abs_outside_ratio_record_minus_rebuild': max_dr,
            'groups': groups}


def verify_highorder(tan):
    cases = {c['name']: c for c in tan['cases']}
    max_de = max_du = 0.
    groups = {}
    rows = loadl('ad21_highorder.jsonl')
    assert len(rows) == 56
    for r in rows:
        c = cases[r['case']]
        perm = (1, 2, 0) if c['form'] == 'G1' else (0, 1, 2)
        H0 = sphere(perm, 1, c['theta'], c['phi'])
        if r['kind'] == 'alpha_fine':
            H, alpha = H0, r['alpha']
        else:
            P, eps = pm(r['pauli']), r['delta']
            C = np.cos(eps) * np.eye(8) + 1j * np.sin(eps) * P
            H, alpha = C @ H0 @ C.conj().T, ALPHA
        U = circuit(r['x'], SEQS[7][r['idx']])
        e = float(np.max(np.abs(U - target_of(H, TARGETS[r['form']], alpha))))
        assert close(e, r['e'], 3e-11), (r['case'], r['kind'], r['delta'], e, r['e'])
        du = float(np.max(np.abs(U @ U.conj().T - np.eye(8))))
        assert du < 3e-13
        max_de, max_du = max(max_de, abs(e-r['e'])), max(max_du, du)
        key = f"{r['case']}/{r['kind']}/sign{int(np.sign(r['delta']))}"
        groups.setdefault(key, []).append((abs(r['delta']), max(e, 1e-300)))
    slopes = {}
    for key, vals in groups.items():
        vals.sort()
        x, y = np.array([v[0] for v in vals]), np.array([v[1] for v in vals])
        slopes[key] = float(np.polyfit(np.log(x), np.log(y), 1)[0])
    return {'records': len(rows), 'max_abs_e_record_minus_rebuild': max_de,
            'max_circuit_unitarity_error': max_du, 'loglog_slopes': slopes}


def verify_embeddings_and_basin(base91):
    # 五个深谷：从原始最佳解而非汇总分类重放。
    scan = loadl('ad20_g2k7_scan.jsonl')
    targeted = loadl('ad20_targeted.jsonl')
    source = []
    for idx in [34, 38, 52, 91]:
        cand = [({'x': r['best']['x'], 'e': r['best']['e']}, 'scan') for r in scan if r['idx'] == idx]
        cand += [({'x': r['x'], 'e': r['e']}, 'targeted') for r in targeted if r['idx'] == idx]
        best, src = min(cand, key=lambda z: z[0]['e'])
        source.append(('G2', idx, best['x'], src))
    p1 = load('ad20_g1k7_polish.json')
    source.append(('G1', 85, p1['x'], 'polish'))
    emb = []
    for form, idx, x, src in source:
        c = classify(x, idx, TARGETS[form])
        emb.append({'form': form, 'idx': idx, 'source': src, **c})
        # 深谷嵌入分类允许原始近似解；精确电路另由切空间抛光账验收。
        assert c['direct_e_rebuilt'] < .25
        assert c['best_ansatz_max_delta'] < 2e-5
    expected = {(85): ([1, 2, 0], 1), 34: ([0, 1, 2], 1), 38: ([0, 1, 2], 1),
                52: ([0, 1, 2], -1), 91: ([2, 1, 0], -1)}
    for r in emb:
        assert (r['best_perm'], r['best_sigma']) == expected[r['idx']]
    # 序91精确基准。
    U = circuit(base91['x'], SEQS[7][91])
    H = sphere(tuple(base91['perm']), base91['sigma'], base91['theta'], base91['phi'])
    e91 = float(np.max(np.abs(U - target_of(H, TARGETS['G2']))))
    assert e91 < 1e-10
    # 256次窄盆：每条独立重判命中。
    rows = loadl('ad21_seq91_basin.jsonl')
    assert len(rows) == 256
    max_de = 0.
    glob, loc = [], []
    for r in rows:
        assert 'error' not in r
        c = classify(r['x'], 91, TARGETS['G2'])
        e = c['direct_e_rebuilt']
        assert close(e, r['e'], 3e-10), (r['kind'], r['seed'], e, r['e'])
        # 分类数值允许本征分解的微小差异，但命中布尔必须一致。
        for key in ['angle_max_dev_rad', 'H_involution_max', 'best_ansatz_max_delta']:
            assert close(c[key], r['classification'][key], 2e-7), (key, c[key], r['classification'][key])
        assert c['best_perm'] == r['classification']['best_perm']
        assert c['best_sigma'] == r['classification']['best_sigma']
        assert basin_hit(e, c) == r['hit']
        r['_rebuilt_e'] = e
        max_de = max(max_de, abs(e-r['e']))
        (glob if r['kind'] == 'global' else loc).append(r)
    radii = sorted({r['radius'] for r in loc})
    by_radius = {str(rad): {'n': sum(r['radius'] == rad for r in loc),
                            'hits': sum(r['radius'] == rad and basin_hit(r['_rebuilt_e'], classify(r['x'], 91, TARGETS['G2'])) for r in loc)}
                 for rad in radii}
    ghits = sum(r['hit'] for r in glob)
    assert len(glob) == 64 and ghits == 0
    assert sum(r['hit'] for r in loc) == 130
    return {'embeddings': emb, 'seq91_base_rebuilt_e': e91,
            'basin': {'records': len(rows), 'max_abs_e_record_minus_rebuild': max_de,
                      'global': {'n': len(glob), 'hits': ghits, 'e_min': min(r['_rebuilt_e'] for r in glob)},
                      'local': {'n': len(loc), 'hits': sum(r['hit'] for r in loc), 'by_radius': by_radius},
                      'width_coordinate': '73维原始求解器坐标；非规范不变几何宽度'}}


def maj_target():
    M = np.zeros((8, 8), complex)
    table = []
    for x in range(8):
        a, b, c = (x >> 2) & 1, (x >> 1) & 1, x & 1
        y = [a ^ b, int(a + b + c >= 2), b ^ c]
        yi = (y[0] << 2) | (y[1] << 1) | y[2]
        M[yi, x] = 1
        table.append((x, yi))
    return M, table


def one3(q, U):
    ops = [np.eye(2, dtype=complex)] * 3
    ops[q] = U
    return np.kron(np.kron(ops[0], ops[1]), ops[2])


def verify_maj(summary):
    M, table = maj_target()
    assert len({y for _, y in table}) == 8
    assert np.array_equal(M.sum(axis=0), np.ones(8)) and np.array_equal(M.sum(axis=1), np.ones(8))
    non_involution = float(np.max(np.abs(M @ M - np.eye(8))))
    assert non_involution == 1.
    H2 = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
    def cnot(c, t):
        return one3(t, H2) @ cz((c, t)) @ one3(t, H2)
    identity = float(np.max(np.abs(TARGETS['G2'] @ cnot(1, 2) @ cnot(1, 0) - M)))
    assert identity < 1e-15
    con = summary['construction_10cz']
    e10 = float(np.max(np.abs(circuit(con['params'], con['edges']) - M)))
    assert e10 < 1e-11
    out = {'known_answer': {'truth_table_unique_outputs': 8, 'composition_identity_max': identity,
                            'MAJ_non_involution_max': non_involution, 'construction_10cz_e': e10}}
    all_groups = {}
    exact8 = []
    for filename in ['ad21_maj.jsonl', 'ad21_maj_lower.jsonl']:
        rows = loadl(filename)
        max_de = max_du = 0.
        groups = {}
        for r in rows:
            assert 'error' not in r
            U = circuit(r['x'], r['edges'])
            e = float(np.max(np.abs(U - M)))
            assert close(e, r['e'], 3e-10), (filename, r.get('seed'), r.get('deleted'), e, r['e'])
            du = float(np.max(np.abs(U @ U.conj().T - np.eye(8))))
            assert du < 3e-13
            max_de, max_du = max(max_de, abs(e-r['e'])), max(max_du, du)
            key = r.get('source', r.get('kind', 'unknown')) + f"/k{r['k']}"
            g = groups.setdefault(key, {'n': 0, 'exact': 0, 'best_e': np.inf})
            g['n'] += 1
            g['exact'] += int(e < 1e-9)
            g['best_e'] = min(g['best_e'], e)
            if filename == 'ad21_maj.jsonl' and r['k'] == 8 and e < 1e-9:
                exact8.append({'deleted': r['deleted'], 'edges': r['edges'], 'x': r['x'],
                               'source_record_e': r['e'], 'independent_rebuilt_e': e,
                               'nfev': r['nfev'], 'status': r['status']})
        out[filename] = {'records': len(rows), 'max_abs_e_record_minus_rebuild': max_de,
                         'max_circuit_unitarity_error': max_du, 'groups': groups}
    exact8.sort(key=lambda r: (r['independent_rebuilt_e'], r['deleted']))
    assert len(exact8) == 18
    assert all(g['exact'] == 0 for name, g in out['ad21_maj_lower.jsonl']['groups'].items())
    out['exact8_count'] = len(exact8)
    out['best8'] = {k: exact8[0][k] for k in ['deleted', 'edges', 'independent_rebuilt_e', 'nfev', 'status']}
    out['lower_boundary'] = 'k≤7零精确仅为本批144删门+128个k7边序+64个k6边序的L2数值否证，非解析下界。'
    return out, exact8


def analytic_residual_jacobian(p, edges, T):
    """独立解析导数，仅供二阶复核；与circuit使用同一数学定义但不调用分析模块。"""
    p = np.asarray(p, float)
    k = len(edges)
    th = layers_of(p, edges)
    mats = []
    for i in range(k + 1):
        mats.append(local_layer(th[i]))
        if i < k:
            mats.append(cz(edges[i]))
    n = len(mats)
    pre = [None] * (n + 1)
    pre[0] = np.eye(8, dtype=complex)
    for j in range(n):
        pre[j + 1] = mats[j] @ pre[j]
    post = [None] * (n + 1)
    post[n - 1] = np.eye(8, dtype=complex)
    for j in range(n - 2, -1, -1):
        post[j] = post[j + 1] @ mats[j + 1]
    phase = np.exp(1j * p[0])
    U = phase * pre[n]
    F = U.reshape(-1) - T.reshape(-1)
    f = np.concatenate([F.real, F.imag])
    J = np.zeros((128, len(p)))
    dU = 1j * U
    J[:, 0] = np.concatenate([dU.reshape(-1).real, dU.reshape(-1).imag])
    col = 1
    for i in range(k + 1):
        base = [su2(th[i, q]) for q in range(3)]
        for q in range(3):
            a, b, c = th[i, q]
            drz_a = np.diag([-.5j * np.exp(-.5j*a), .5j * np.exp(.5j*a)])
            dry_b = np.array([[-.5*np.sin(b/2), -.5*np.cos(b/2)],
                              [.5*np.cos(b/2), -.5*np.sin(b/2)]])
            drz_c = np.diag([-.5j * np.exp(-.5j*c), .5j * np.exp(.5j*c)])
            derivs = [drz_a @ ry(b) @ rz(c), rz(a) @ dry_b @ rz(c), rz(a) @ ry(b) @ drz_c]
            for dlocal in derivs:
                parts = list(base)
                parts[q] = dlocal
                dL = np.kron(np.kron(parts[0], parts[1]), parts[2])
                dU = phase * (post[2*i] @ dL @ pre[2*i])
                J[:, col] = np.concatenate([dU.reshape(-1).real, dU.reshape(-1).imag])
                col += 1
    return f, J


def form_terms(form, u, v, w, t):
    perm = (1, 2, 0) if form == 'G1' else (0, 1, 2)
    n = basis_names(perm)
    return u*pm(n[0]) + v*pm(n[1]) + w*(pm(n[2])+pm(n[4])) + t*(pm(n[3])+pm(n[5]))


def second_order_case(case, kind):
    form = case['form']
    p0 = np.asarray(case['x_polished'])
    seq = SEQS[7][case['idx']]
    th, ph = case['theta'], case['phi']
    H0 = form_terms(form, (1+np.cos(th))/2, (np.cos(th)-1)/2,
                    np.sin(th)*np.cos(ph)/2, np.sin(th)*np.sin(ph)/2)
    T = TARGETS[form]
    V0 = target_of(H0, T)
    _, J = analytic_residual_jacobian(p0, seq, V0)
    U, sv, Vh = np.linalg.svd(J, full_matrices=True)
    rank = int(np.sum(sv > sv[0]*1e-10))
    assert rank == case['jacobian_rank']
    Q, N = U[:, rank:], Vh[rank:].T
    if kind in ['theta', 'phi']:
        du = dv = -np.sin(th)/2
        dw, dt = np.cos(th)*np.cos(ph)/2, np.cos(th)*np.sin(ph)/2
        dth = form_terms(form, du, dv, dw, dt)
        dph = form_terms(form, 0, 0, -np.sin(th)*np.sin(ph)/2, np.sin(th)*np.cos(ph)/2)
        if kind == 'theta':
            dH = dth
            H2 = form_terms(form, -np.cos(th)/2, -np.cos(th)/2,
                            -np.sin(th)*np.cos(ph)/2, -np.sin(th)*np.sin(ph)/2)
        else:
            dH = dph
            w, t = np.sin(th)*np.cos(ph)/2, np.sin(th)*np.sin(ph)/2
            H2 = form_terms(form, 0, 0, -w, -t)
    else:
        chosen = [r for r in case['outside_candidates']
                  if r['outside_ratio'] > .99 and r['projection_residual_ratio'] < 1e-8][0]
        P = pm(chosen['pauli'])
        dH = 1j * (P @ H0 - H0 @ P)
        H2 = 2 * (P @ H0 @ P - H0)
    d = realvec(1j*np.sin(ALPHA)*dH@T)
    p10, *_ = np.linalg.lstsq(J, d, rcond=1e-11)
    v2 = realvec(1j*np.sin(ALPHA)*H2@T)
    def rhs(z, h=1e-4):
        p1 = p10 + N @ z
        jp = analytic_residual_jacobian(p0+h*p1, seq, V0)[1] @ p1
        jm = analytic_residual_jacobian(p0-h*p1, seq, V0)[1] @ p1
        return (jp-jm)/(2*h) - v2
    sol = least_squares(lambda z: Q.T @ rhs(z), np.zeros(N.shape[1]), max_nfev=180,
                        ftol=1e-12, xtol=1e-12, gtol=1e-12)
    vals = []
    for h in [1e-3, 3e-4, 1e-4, 3e-5, 1e-5]:
        vals.append(float(np.linalg.norm(Q.T @ rhs(sol.x, h))))
    return {'case': case['name'], 'kind': kind, 'rank': rank,
            'cokernel_norm_optimized': float(np.linalg.norm(Q.T @ rhs(sol.x))),
            'stability_max_minus_min': max(vals)-min(vals), 'nfev': int(sol.nfev)}


def verify_second_order(tan):
    rows = [second_order_case(c, kind) for c in tan['cases'] for kind in ['theta', 'phi', 'outside']]
    gate = [r['cokernel_norm_optimized'] for r in rows if r['kind'] != 'outside']
    outside = [r['cokernel_norm_optimized'] for r in rows if r['kind'] == 'outside']
    assert max(gate) < 1e-6 and min(outside) > 1e-3
    return {'rows': rows, 'known_answer_gate_max': max(gate), 'outside_min': min(outside),
            'boundary': '固定秩与有限差分的局部二阶数值证书，非全局不可达定理。'}


H4 = np.array([[1, 1], [1, -1]], complex)/np.sqrt(2)
X4 = np.array([[0, 1], [1, 0]], complex)
Z4 = np.diag([1, -1]).astype(complex)
S4 = np.diag([1, 1j]).astype(complex)
PHYS = [0, 6, 7, 12]
IX4 = {q: i for i, q in enumerate(PHYS)}


def parse_qcis(txt):
    ops = []
    for line in txt.splitlines():
        z = line.split()
        op = z[0]
        qs = [int(q[1:]) for q in z[1:] if q.startswith('Q')]
        val = float(z[-1]) if op == 'RZ' else None
        ops.append((op, qs, val))
    return ops


def tensor_distribution(ops):
    st = np.zeros((2, 2, 2, 2), complex)
    st[0, 0, 0, 0] = 1
    for op, qs, val in ops:
        if op == 'M':
            continue
        if op in ['H', 'X', 'Z', 'S', 'RZ']:
            q = IX4[qs[0]]
            mat = {'H': H4, 'X': X4, 'Z': Z4, 'S': S4}.get(op)
            if op == 'RZ':
                mat = np.diag([np.exp(-1j*val/2), np.exp(1j*val/2)])
            st = np.moveaxis(np.tensordot(mat, st, axes=([1], [q])), 0, q)
        elif op == 'CZ':
            a, b = IX4[qs[0]], IX4[qs[1]]
            for s in range(16):
                if ((s >> (3-a)) & 1) and ((s >> (3-b)) & 1):
                    idx = tuple((s >> (3-i)) & 1 for i in range(4))
                    st[idx] *= -1
        else:
            raise ValueError(op)
    return np.abs(st.reshape(-1))**2


def bits4(s):
    return [(s >> (3-i)) & 1 for i in range(4)]


def decode4(arr, meta):
    ans = 0.
    for s, value in enumerate(arr):
        b = bits4(s)
        iA = b[IX4[0]] + 2*b[IX4[7]]
        iB = b[IX4[6]] + 2*b[IX4[12]]
        if ((meta['y'] == 1 and (iA-iB) % 4 == meta['x1'])
                or (meta['y'] == 2 and (iA+iB) % 4 == meta['x2'])):
            ans += value
    return float(ans)


def chi2_two(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    mask = a+b > 0
    stat = float(np.sum((a[mask]-b[mask])**2/(a[mask]+b[mask])))
    df = int(mask.sum()-1)
    return {'statistic': stat, 'df': df, 'p_value': float(chi2.sf(stat, df)) if df else 1.}


def parity4(counts):
    return [int(sum(c for s, c in enumerate(counts) if sum(bits4(s)) % 2 == p)) for p in [0, 1]]


def holm4(rows, key):
    m = len(rows)
    order = sorted(range(m), key=lambda i: rows[i][key]['p_value'])
    adj, running = [0.]*m, 0.
    for rank, i in enumerate(order):
        running = max(running, (m-rank)*rows[i][key]['p_value'])
        adj[i] = min(1., running)
    return adj


def verify_rac(rac):
    rows = []
    max_dist = 0.
    for old in rac['circuits']:
        txt = old['qcis']
        assert hashlib.sha256(txt.encode()).hexdigest() == old['qcis_sha256']
        dist = tensor_distribution(parse_qcis(txt))
        i = old['index']
        ca = np.bincount(np.random.default_rng(20261110+i).choice(16, size=240, p=dist), minlength=16)
        cb = np.bincount(np.random.default_rng(20261210+i).choice(16, size=240, p=dist), minlength=16)
        assert np.array_equal(ca, old['counts_matrix']) and np.array_equal(cb, old['counts_tensor'])
        meta = {k: old[k] for k in ['x1', 'x2', 'y']}
        sa = decode4(dist, meta)
        assert sa > 1-1e-12
        assert round(decode4(ca, meta)) == 240 and round(decode4(cb, meta)) == 240
        r = {'index': i, 'S': sa, 'chi2_16outcome': chi2_two(ca, cb),
             'chi2_hamming_parity': chi2_two(parity4(ca), parity4(cb))}
        for key in ['chi2_16outcome', 'chi2_hamming_parity']:
            assert close(r[key]['statistic'], old[key]['statistic'], 1e-10)
            assert close(r[key]['p_value'], old[key]['p_value'], 1e-10)
        rows.append(r)
        max_dist = max(max_dist, float(np.max(np.abs(dist-dist))))
    a16, ap = holm4(rows, 'chi2_16outcome'), holm4(rows, 'chi2_hamming_parity')
    assert min(a16) >= .01 and min(ap) >= .01
    # 独立已知答案：逻辑0,2 Bell态只应占据索引0和12。
    bell_txt = 'H Q0\nH Q6\nCZ Q0 Q6\nH Q6\nM Q0\nM Q6'
    bd = tensor_distribution(parse_qcis(bell_txt))
    assert abs(bd[0]-.5) < 1e-14 and abs(bd[12]-.5) < 1e-14
    return {'circuits': len(rows), 'shots_per_independent_stream': 240,
            'S_min': min(r['S'] for r in rows), 'min_holm_p_16outcome': min(a16),
            'min_holm_p_hamming_parity': min(ap),
            'bell_known_answer': [float(bd[0]), float(bd[12])],
            'scope': 'QLV侧零机时独立张量重建与采样重放；非跨线S_sim对拍，非真机。'}


def main():
    t0 = time.time()
    tan = load('ad21_tangent.json')
    base91 = load('ad21_seq91_base.json')
    majsum = load('ad21_maj_summary.json')
    rac = load('ad21_rac22_xval.json')
    checks = {'known_answer_gate': known_answer_gate()}
    checks['continuation'] = verify_continuation(tan, base91)
    checks['highorder'] = verify_highorder(tan)
    checks['embeddings_and_basin'] = verify_embeddings_and_basin(base91)
    checks['maj'], exact8 = verify_maj(majsum)
    checks['second_order'] = verify_second_order(tan)
    checks['rac22'] = verify_rac(rac)
    pack = {'beat': 'AD-21', 'target': '(a,b,c)->(a xor b,maj(a,b,c),b xor c)',
            'count': len(exact8), 'residual_definition': 'max(abs(U-MAJ))',
            'solutions': exact8,
            'boundary': '18个精确8 CZ数值电路；不声称8为解析最小值。'}
    (RUN / 'ad21_maj_8cz.json').write_text(json.dumps(pack, indent=2)+'\n')
    input_names = ['ad21_tangent.json', 'ad21_seq91_base.json', 'ad21_continuation.jsonl',
                   'ad21_seq91_continuation.jsonl', 'ad21_highorder.jsonl', 'ad21_seq91_basin.jsonl',
                   'ad20_g2k7_scan.jsonl', 'ad20_targeted.jsonl', 'ad20_g1k7_polish.json',
                   'ad21_maj_summary.json', 'ad21_maj.jsonl', 'ad21_maj_lower.jsonl',
                   'ad21_rac22_xval.json']
    hashes = {n: hashlib.sha256((RUN/n).read_bytes()).hexdigest() for n in input_names}
    out = {'beat': 'AD-21', 'verified_at': time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()),
           'evidence_scope': 'independent rebuild from raw parameters; no solver/analysis-module import',
           'residual': '逐元最大模 max(abs(U-target))', 'input_sha256': hashes,
           'checks': checks, 'seconds': time.time()-t0, 'verdict': 'ALL_PASS'}
    (RUN / 'ad21_verify.json').write_text(json.dumps(out, indent=2)+'\n')
    brief = {'verdict': out['verdict'], 'seconds': out['seconds'],
             'continuation': {k: checks['continuation'][k] for k in ['records', 'success_e_lt_1e-8', 'max_abs_e_record_minus_rebuild']},
             'highorder_records': checks['highorder']['records'],
             'basin': checks['embeddings_and_basin']['basin'],
             'maj': {'exact8': checks['maj']['exact8_count'], 'best8': checks['maj']['best8'],
                     'lower_groups': checks['maj']['ad21_maj_lower.jsonl']['groups']},
             'second_order': checks['second_order'], 'rac22': checks['rac22']}
    print(json.dumps(brief, indent=2))


if __name__ == '__main__':
    main()
