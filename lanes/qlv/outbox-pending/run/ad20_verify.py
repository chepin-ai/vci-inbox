import sys, json, itertools, hashlib
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent.parent
RUN = BASE / 'run'
sys.path.insert(0, str(BASE))
import toffoli_solver as ts

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
P = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
THETA = np.pi / 8
T1 = ts.toffoli({0, 1}, 2)
T2 = ts.toffoli({0, 2}, 1)


def pm2(s):
    return np.kron(P[s[0]], P[s[1]])


def pm3(s):
    return np.kron(np.kron(P[s[0]], P[s[1]]), P[s[2]])


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def generator(x, idx, k, target):
    seq = list(itertools.product(ts.PATH, repeat=k))[idx]
    U = ts.U_of(np.asarray(x), seq)
    A = U @ target
    vals, vecs = np.linalg.eig(A)
    angles = np.angle(vals)
    K = vecs @ np.diag(angles) @ np.linalg.inv(vecs)
    return U, K, angles


def spectral_metrics(K, angles):
    H = K / THETA
    return {
        'angle_max_dev_rad': float(np.max(np.abs(np.abs(angles) - THETA))),
        'involution_max': float(np.max(np.abs(H @ H - np.eye(8)))),
        'hermitian_max': float(np.max(np.abs(K - K.conj().T)))
    }


# 已知答案自证：S² 参数化必须逐点给出严格对合。
selftest_max = {'G1_form': 0.0, 'G2_form': 0.0}
for theta in np.linspace(0, np.pi, 9):
    for phi in np.linspace(-np.pi, np.pi, 12, endpoint=False):
        u = (1 + np.cos(theta)) / 2
        v = (np.cos(theta) - 1) / 2
        w = np.sin(theta) * np.cos(phi) / 2
        t = np.sin(theta) * np.sin(phi) / 2
        B1 = u * pm2('ZX') + v * pm2('ZI') + w * (pm2('YI') + pm2('YX')) + t * (pm2('XI') + pm2('XX'))
        B2 = w * (pm2('IX') + pm2('XX')) + t * (pm2('IY') + pm2('XY')) + u * pm2('IZ') + v * pm2('XZ')
        selftest_max['G1_form'] = max(selftest_max['G1_form'], float(np.max(np.abs(B1 @ B1 - np.eye(4)))))
        selftest_max['G2_form'] = max(selftest_max['G2_form'], float(np.max(np.abs(B2 @ B2 - np.eye(4)))))
assert selftest_max['G1_form'] < 2e-15, selftest_max
assert selftest_max['G2_form'] < 2e-15, selftest_max

scan = load_jsonl(RUN / 'ad20_g2k7_scan.jsonl')
targeted = load_jsonl(RUN / 'ad20_targeted.jsonl')
assert len(scan) == 128 and len({r['idx'] for r in scan}) == 128
assert all('error' not in r and len(r['restart_e']) == 5 for r in scan)
assert len(targeted) == 200 and all('error' not in r for r in targeted)
for geometry, idx in [('G2', 91), ('G2', 34), ('G2', 38), ('G2', 52), ('G1', 85)]:
    assert sum(r['geometry'] == geometry and r['idx'] == idx for r in targeted) == 40

# 从原始记录独立选最优，不沿用分析过程的中间变量。
g2_candidates = []
for r in scan:
    b = r['best']
    g2_candidates.append({'geometry': 'G2', 'idx': r['idx'], 'source': 'scan', 'e': b['e'], 'x': b['x']})
for r in targeted:
    if r['geometry'] == 'G2':
        g2_candidates.append({'geometry': 'G2', 'idx': r['idx'], 'source': 'targeted', 'e': r['e'], 'x': r['x']})
best_g2 = min(g2_candidates, key=lambda r: r['e'])
U, K, angles = generator(best_g2['x'], best_g2['idx'], 7, T2)
best_g2_direct_e = float(np.max(np.abs(U - T2)))
assert abs(best_g2_direct_e - best_g2['e']) < 1e-12
best_g2_metrics = spectral_metrics(K, angles)
assert best_g2_metrics['angle_max_dev_rad'] < 2e-8
assert best_g2_metrics['involution_max'] < 6e-8

polish = json.loads((RUN / 'ad20_g1k7_polish.json').read_text())
U1, K1, angles1 = generator(polish['x'], 85, 7, T1)
best_g1_direct_e = float(np.max(np.abs(U1 - T1)))
assert abs(best_g1_direct_e - polish['e']) < 1e-12
best_g1_metrics = spectral_metrics(K1, angles1)
assert best_g1_metrics['angle_max_dev_rad'] < 4e-7
assert best_g1_metrics['involution_max'] < 1e-6

# 四个 G2 深谷候选均须保持 ±π/8 谱与对合。
candidate_metrics = []
for idx in [34, 91, 38, 52]:
    r = min((z for z in g2_candidates if z['idx'] == idx), key=lambda z: z['e'])
    _, Kc, ac = generator(r['x'], idx, 7, T2)
    m = spectral_metrics(Kc, ac)
    assert m['angle_max_dev_rad'] < 2e-8 and m['involution_max'] < 6e-8
    candidate_metrics.append({'idx': idx, 'e': r['e'], 'source': r['source'], **m})

# G2k6 旧账勘误：d=XZ<0，约束是 c-d=1 而非 c+d=1。
x43 = np.load(RUN / 'g2k6_seq43.npy')
_, K43, a43ang = generator(x43, 43, 6, T2)
H43 = K43 / THETA
B43 = H43[:4, :4]
coef = lambda s: float((np.trace(pm2(s) @ B43) / 4).real)
a, b, c, d = coef('IX'), coef('IY'), coef('IZ'), coef('XZ')
g2k6_constraints = {'c-d-1': c - d - 1, 'a2+b2+cd': a*a + b*b + c*d, 'c+d-1': c + d - 1}
assert abs(g2k6_constraints['c-d-1']) < 2e-8
assert abs(g2k6_constraints['a2+b2+cd']) < 2e-8
assert abs(g2k6_constraints['c+d-1']) > 1.0

# G1k7 与 G2k7 最优解的同一 M⊗Z 嵌入及 S² 约束。
def coef3(K, s):
    return float((np.trace(pm3(s) @ (K / THETA)) / 8).real)

u1, v1 = coef3(K1, 'ZZX'), coef3(K1, 'ZZI')
w1, t1 = coef3(K1, 'ZYI'), coef3(K1, 'ZXI')
g1_constraints = {'u-v-1': u1 - v1 - 1, 'w2+t2+uv': w1*w1 + t1*t1 + u1*v1}
assert abs(g1_constraints['u-v-1']) < 1e-7
assert abs(g1_constraints['w2+t2+uv']) < 1e-7

u2, v2 = coef3(K, 'ZXZ'), coef3(K, 'ZIZ')
w2, t2 = coef3(K, 'YIZ'), coef3(K, 'XIZ')
g2_constraints = {'u-v-1': u2 - v2 - 1, 'w2+t2+uv': w2*w2 + t2*t2 + u2*v2,
                  'pair_w': coef3(K, 'YIZ') - coef3(K, 'YXZ'),
                  'pair_t': coef3(K, 'XIZ') - coef3(K, 'XXZ')}
assert abs(g2_constraints['u-v-1']) < 1e-7
assert abs(g2_constraints['w2+t2+uv']) < 2e-7
assert abs(g2_constraints['pair_w']) < 2e-7 and abs(g2_constraints['pair_t']) < 2e-7

# 可复算角度包。
angles_out = {
    'G1k7_seq85': {'e': best_g1_direct_e, 'edges': list(itertools.product(ts.PATH, repeat=7))[85], 'x': polish['x']},
    'G2k7_seq34': {'e': best_g2_direct_e, 'edges': list(itertools.product(ts.PATH, repeat=7))[best_g2['idx']], 'x': best_g2['x']},
    'G2k6_seq43': {'e': float(np.max(np.abs(ts.U_of(x43, list(itertools.product(ts.PATH, repeat=6))[43]) - T2))),
                    'edges': list(itertools.product(ts.PATH, repeat=6))[43], 'x': x43.tolist()}
}
(RUN / 'ad20_best_angles.json').write_text(json.dumps(angles_out, separators=(',', ':')) + '\n')

inputs = ['ad20_g2k7_scan.jsonl', 'ad20_targeted.jsonl', 'ad20_g1k7_polish.json', 'g2k6_seq43.npy']
out = {
    'beat': 'AD-20', 'verdict': 'ALL_PASS', 'selftest_max': selftest_max,
    'scan': {'sequences': len(scan), 'restarts_per_sequence': 5, 'errors': 0},
    'targeted': {'runs': len(targeted), 'errors': 0},
    'best_G2k7': {'idx': best_g2['idx'], 'source': best_g2['source'], 'e': best_g2_direct_e, **best_g2_metrics},
    'best_G1k7': {'idx': 85, 'e': best_g1_direct_e, **best_g1_metrics},
    'G2k7_candidates': candidate_metrics,
    'G2k6_erratum': g2k6_constraints,
    'G1k7_constraints': g1_constraints, 'G2k7_constraints': g2_constraints,
    'input_sha256': {fn: hashlib.sha256((RUN / fn).read_bytes()).hexdigest() for fn in inputs},
    'best_angles_sha256': hashlib.sha256((RUN / 'ad20_best_angles.json').read_bytes()).hexdigest()
}
(RUN / 'ad20_verify.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
