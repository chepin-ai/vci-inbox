import json, sys, itertools
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

BASE = Path(__file__).resolve().parent.parent
RUN = BASE / 'run'
sys.path.insert(0, str(BASE))
import toffoli_solver as ts

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
ALPHA = np.pi / 8
TARGETS = {'G1': ts.toffoli({0, 1}, 2), 'G2': ts.toffoli({0, 2}, 1)}
PAULI_STRINGS = [''.join(s) for s in itertools.product('IXYZ', repeat=3) if s != 'III']


def pm3(s):
    return np.kron(np.kron(PAULI[s[0]], PAULI[s[1]]), PAULI[s[2]])


def realvec(M):
    z = np.asarray(M).reshape(-1)
    return np.concatenate([z.real, z.imag])


def form_terms(form, u, v, w, t):
    if form == 'G1':
        return (u*pm3('ZZX') + v*pm3('ZZI') + w*(pm3('ZYI')+pm3('ZYX'))
                + t*(pm3('ZXI')+pm3('ZXX')))
    if form == 'G2':
        return (u*pm3('ZXZ') + v*pm3('ZIZ') + w*(pm3('YIZ')+pm3('YXZ'))
                + t*(pm3('XIZ')+pm3('XXZ')))
    raise ValueError(form)


def form_coefficients(form, H):
    names = {'G1': ['ZZX', 'ZZI', 'ZYI', 'ZXI'],
             'G2': ['ZXZ', 'ZIZ', 'YIZ', 'XIZ']}[form]
    return [float((np.trace(pm3(s) @ H) / 8).real) for s in names]


def form_from_sphere(form, theta, phi):
    u = (1 + np.cos(theta)) / 2
    v = (np.cos(theta) - 1) / 2
    w = np.sin(theta) * np.cos(phi) / 2
    t = np.sin(theta) * np.sin(phi) / 2
    return form_terms(form, u, v, w, t)


def sphere_derivatives(form, theta, phi):
    du, dv = -np.sin(theta)/2, -np.sin(theta)/2
    dw, dt = np.cos(theta)*np.cos(phi)/2, np.cos(theta)*np.sin(phi)/2
    dtheta = form_terms(form, du, dv, dw, dt)
    dphi = form_terms(form, 0.0, 0.0, -np.sin(theta)*np.sin(phi)/2,
                      np.sin(theta)*np.cos(phi)/2)
    return dtheta, dphi


def fit_sphere(form, H):
    u, v, w, t = form_coefficients(form, H)
    theta = float(np.arccos(np.clip(u+v, -1, 1)))
    phi = float(np.arctan2(t, w))
    return theta, phi


def ansatz_basis(form):
    names = {'G1': ['ZZX', 'ZZI', 'ZYI', 'ZYX', 'ZXI', 'ZXX'],
             'G2': ['ZXZ', 'ZIZ', 'YIZ', 'YXZ', 'XIZ', 'XXZ']}[form]
    return [pm3(s) for s in names]


def extract_generator(p, seq, target):
    U = ts.U_of(np.asarray(p), seq)
    A = U @ target
    vals, vecs = np.linalg.eig(A)
    angles = np.angle(vals)
    K = vecs @ np.diag(angles) @ np.linalg.inv(vecs)
    H = K / ALPHA
    return U, (H + H.conj().T) / 2, angles


def target_of(H, target, alpha=ALPHA):
    return (np.cos(alpha)*np.eye(8) + 1j*np.sin(alpha)*H) @ target


def polish(p, seq, target_matrix, max_nfev=4000):
    ts._cache.clear()
    sol = least_squares(ts.f_resid, np.asarray(p), jac=ts.j_resid,
                        args=(seq, target_matrix.reshape(-1)), method='lm',
                        max_nfev=max_nfev, ftol=1e-15, xtol=1e-15, gtol=1e-15)
    e = float(np.max(np.abs(sol.fun[:64] + 1j*sol.fun[64:])))
    return sol.x, e, int(sol.nfev), int(sol.status)


def project_tangent(J, derivative):
    d = realvec(derivative)
    delta, *_ = np.linalg.lstsq(J, d, rcond=1e-11)
    residual = J @ delta - d
    return float(np.linalg.norm(residual) / np.linalg.norm(d)), float(np.linalg.norm(delta))


def outside_fraction(form, delta_H):
    B = np.column_stack([realvec(M) for M in ansatz_basis(form)])
    d = realvec(delta_H)
    coef, *_ = np.linalg.lstsq(B, d, rcond=None)
    outside = d - B @ coef
    return float(np.linalg.norm(outside) / np.linalg.norm(d)), float(np.linalg.norm(outside))


def load_cases():
    best = json.loads((RUN/'ad20_best_angles.json').read_text())
    # 序91不预设为序34的同一嵌入；其Pauli分类另行判定，避免把错嵌入投影伪作远目标。
    return [
        {'name': 'G1k7_seq85', 'form': 'G1', 'idx': 85, 'x': best['G1k7_seq85']['x']},
        {'name': 'G2k7_seq34', 'form': 'G2', 'idx': 34, 'x': best['G2k7_seq34']['x']},
    ]


def analyze_case(case):
    form = case['form']
    seq = list(itertools.product(ts.PATH, repeat=7))[case['idx']]
    target = TARGETS[form]
    U, Hraw, angles = extract_generator(case['x'], seq, target)
    theta, phi = fit_sphere(form, Hraw)
    H0 = form_from_sphere(form, theta, phi)
    ansatz_delta = float(np.max(np.abs(Hraw-H0)))
    p, polish_e, nfev, status = polish(case['x'], seq, target_of(H0, target))
    assert polish_e < 1e-8, (case['name'], polish_e)
    U0 = ts.U_of(p, seq)
    V0 = target_of(H0, target)
    _, J = ts.f_j(p, seq, V0.reshape(-1))
    singular = np.linalg.svd(J, compute_uv=False)
    rank = int(np.sum(singular > singular[0]*1e-10))
    dtheta, dphi = sphere_derivatives(form, theta, phi)
    dalpha = (-np.sin(ALPHA)*np.eye(8) + 1j*np.cos(ALPHA)*H0) @ target
    directions = {}
    for name, deriv in [('alpha', dalpha), ('theta', 1j*np.sin(ALPHA)*dtheta@target),
                        ('phi', 1j*np.sin(ALPHA)*dphi@target)]:
        ratio, step = project_tangent(J, deriv)
        directions[name] = {'projection_residual_ratio': ratio, 'least_squares_parameter_step': step}
    outside = []
    for s in PAULI_STRINGS:
        P = pm3(s)
        delta_H = 1j * (P@H0 - H0@P)
        if np.linalg.norm(delta_H) < 1e-10:
            continue
        out_ratio, out_norm = outside_fraction(form, delta_H)
        deriv = 1j*np.sin(ALPHA)*delta_H@target
        proj_ratio, step = project_tangent(J, deriv)
        outside.append({'pauli': s, 'outside_ratio': out_ratio, 'outside_norm': out_norm,
                        'projection_residual_ratio': proj_ratio, 'least_squares_parameter_step': step})
    outside.sort(key=lambda r: (r['projection_residual_ratio'], -r['outside_ratio']))
    return {**case, 'theta': theta, 'phi': phi, 'ansatz_max_delta_before_polish': ansatz_delta,
            'polish_e': polish_e, 'polish_nfev': nfev, 'polish_status': status,
            'jacobian_rank': rank, 'jacobian_singular_max': float(singular[0]),
            'jacobian_singular_min_nonzero': float(singular[rank-1]),
            'directions': directions, 'outside_candidates': outside,
            'H0_max_involution_error': float(np.max(np.abs(H0@H0-np.eye(8)))),
            'x_polished': p.tolist()}


def main():
    # Known-answer gate: every sphere sample is an involution, and the zero-angle target is T.
    gate_max = 0.0
    for form in ['G1', 'G2']:
        for theta in np.linspace(0.03, np.pi-0.03, 7):
            for phi in np.linspace(-np.pi, np.pi, 8, endpoint=False):
                H = form_from_sphere(form, theta, phi)
                gate_max = max(gate_max, float(np.max(np.abs(H@H-np.eye(8)))))
                assert np.max(np.abs(target_of(H, TARGETS[form], 0)-TARGETS[form])) == 0
    assert gate_max < 3e-15, gate_max
    cases = [analyze_case(c) for c in load_cases()]
    out = {'beat': 'AD-21', 'selftest_involution_max': gate_max, 'cases': cases}
    (RUN/'ad21_tangent.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'selftest_involution_max': gate_max, 'cases': [
        {k: c[k] for k in ['name','polish_e','jacobian_rank','theta','phi','directions']}
        | {'best_outside': c['outside_candidates'][:3]} for c in cases]}, indent=2))


if __name__ == '__main__':
    main()
