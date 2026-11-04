"""拍AD-16/17 Toffoli梯浅化析 — 解析雅可比模板求解器(内核重置韧性版)
律: 判读器先以已知答案自证(全连通k=6↔Shende-Markov)再判未知"""
import numpy as np, itertools, time, json, sys
from numpy import kron, eye
from scipy.optimize import least_squares

def mRz(a): return np.array([[np.exp(-0.5j*a),0],[0,np.exp(0.5j*a)]])
def mRy(b): return np.array([[np.cos(b/2),-np.sin(b/2)],[np.sin(b/2),np.cos(b/2)]])
def dRz(a): return np.array([[-0.5j*np.exp(-0.5j*a),0],[0,0.5j*np.exp(0.5j*a)]])
def dRy(b): return np.array([[-0.5*np.sin(b/2),-0.5*np.cos(b/2)],[0.5*np.cos(b/2),-0.5*np.sin(b/2)]])
def su2(t):  return mRz(t[0]) @ mRy(t[1]) @ mRz(t[2])
def dsu2(t):
    a,b,c = t
    return [dRz(a)@mRy(b)@mRz(c), mRz(a)@dRy(b)@mRz(c), mRz(a)@mRy(b)@dRz(c)]
def cz3(p,q):
    D = np.ones(8,complex)
    for x in range(8):
        if ((x>>(2-p))&1) and ((x>>(2-q))&1): D[x] = -1
    return np.diag(D)
def build_factors(p, edges):
    k = len(edges); th = np.asarray(p)[1:].reshape(k+1,3,3)
    mats = []
    for i in range(k+1):
        mats.append(kron(kron(su2(th[i,0]), su2(th[i,1])), su2(th[i,2])))
        if i < k: mats.append(cz3(*edges[i]))
    return mats, th
def U_of(p, edges):
    mats,_ = build_factors(p, edges)
    U = np.exp(1j*p[0])*eye(8)
    for M in reversed(mats): U = U @ M
    return U
def f_j(p, edges, Tvec):
    mats, th = build_factors(p, edges)
    k = len(edges); n = len(mats); ph = np.exp(1j*p[0])
    pre = [None]*(n+1); pre[0] = eye(8)
    for j in range(n): pre[j+1] = mats[j] @ pre[j]
    post = [None]*(n+1); post[n-1] = eye(8)
    for j in range(n-2,-1,-1): post[j] = post[j+1] @ mats[j+1]
    U = ph * pre[n]
    F = U.reshape(-1) - Tvec
    f = np.concatenate([F.real, F.imag])
    npar = len(p); J = np.zeros((128, npar))
    dU = 1j*U
    J[:,0] = np.concatenate([dU.reshape(-1).real, dU.reshape(-1).imag])
    col = 1
    for i in range(k+1):
        base = [su2(th[i,0]), su2(th[i,1]), su2(th[i,2])]
        for q in range(3):
            for dd in dsu2(th[i,q]):
                parts = list(base); parts[q] = dd
                dL = kron(kron(parts[0], parts[1]), parts[2])
                dUi = ph * (post[2*i] @ dL @ pre[2*i])
                J[:,col] = np.concatenate([dUi.reshape(-1).real, dUi.reshape(-1).imag]); col += 1
    return f, J
_cache = {}
def f_resid(p, ek, tv):
    key = (p.tobytes(), id(ek))
    if key not in _cache: _cache[key] = f_j(p, ek, tv)
    return _cache[key][0]
def j_resid(p, ek, tv):
    key = (p.tobytes(), id(ek))
    if key not in _cache: _cache[key] = f_j(p, ek, tv)
    return _cache[key][1]

def toffoli(controls, target):
    M = np.zeros((8,8),complex)
    for x in range(8):
        b=[(x>>2)&1,(x>>1)&1,x&1]
        if all(b[c] for c in controls): b[target]^=1
        M[(b[0]<<2)|(b[1]<<1)|b[2], x]=1
    return M

PATH = [(0,1),(1,2)]; FULL = [(0,1),(1,2),(0,2)]

def solve_k(T, edges_avail, k, n_seq=24, restarts=5, seed=0, exhaustive=False, cb=None):
    rng = np.random.default_rng(seed)
    seqs = list(itertools.product(edges_avail, repeat=k))
    if not exhaustive and len(seqs) > n_seq:
        seqs = [seqs[i] for i in rng.choice(len(seqs), n_seq, replace=False)]
    best = (np.inf, None); tv = T.reshape(-1)
    for si, seq in enumerate(seqs):
        seq = [tuple(e) for e in seq]
        for r in range(restarts):
            p0 = rng.normal(scale=1.5, size=1+9*(k+1))
            try:
                sol = least_squares(f_resid, p0, jac=j_resid, args=(seq, tv),
                                    method='lm', max_nfev=2500, ftol=1e-15, xtol=1e-15, gtol=1e-15)
            except Exception:
                continue
            e = np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:]))
            if e < best[0]: best = (e, seq)
            if e < 1e-10: return best
        if cb: cb(si, len(seqs), best)
    return best
