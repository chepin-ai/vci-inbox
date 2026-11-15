"""AD-23 MAJ 规范压缩：35维边界规范显式消元，不改变电路矩阵。

对边界 L_{i+1} C_i L_i：
- C_i 的两个边量子比特：L_i,q -> Rz(-a_q)L_i,q，L_{i+1},q -> L_{i+1},q Rz(a_q)，
  使 L_i,q 的首 Euler 角为零；
- C_i 的空闲量子比特 q：L_i,q -> G†L_i,q=I，L_{i+1},q -> L_{i+1},q G，G=L_i,q。
依次 i=0..k-1 后，前 k 层各仅余4个角，末层9个角，加全局相位共4k+10个坐标；
k=7 时73->38。整个过程只做SU(2)矩阵乘法，无目标拟合或近似。
"""
import hashlib
import json
from pathlib import Path
import numpy as np

R23=Path(__file__).resolve().parent
R22=R23.parent.parent/'ad22/run'
R21=R23.parent.parent/'ad21/run'
I2=np.eye(2,dtype=complex)

def rz(a): return np.diag([np.exp(-.5j*a),np.exp(.5j*a)])
def ry(b): return np.array([[np.cos(b/2),-np.sin(b/2)],[np.sin(b/2),np.cos(b/2)]],complex)
def su2(t): return rz(t[0])@ry(t[1])@rz(t[2])
def cz(edge):
    d=np.ones(8,complex);a,b=edge
    for x in range(8):
        if ((x>>(2-a))&1) and ((x>>(2-b))&1): d[x]=-1
    return np.diag(d)
def circuit_layers(layers,edges,phase=0.):
    U=np.exp(1j*phase)*np.eye(8,dtype=complex)
    for i in range(len(edges)-1,-1,-1):
        L=np.kron(np.kron(layers[i+1][0],layers[i+1][1]),layers[i+1][2])
        U=U@L@cz(edges[i])
    return U@np.kron(np.kron(layers[0][0],layers[0][1]),layers[0][2])
def unpack(p):
    p=np.asarray(p,float);k=(len(p)-10)//9
    assert len(p)==1+9*(k+1)
    th=p[1:].reshape(k+1,3,3)
    return p[0],[[su2(th[i,q]) for q in range(3)] for i in range(k+1)]
def pack(phase,layers):
    ts=[]
    for L in layers:
        ts.append([zxz(L[q]) for q in range(3)])
    return np.concatenate([[phase],np.asarray(ts).reshape(-1)])
def zxz(U):
    """SU(2)->Rz(a)Ry(b)Rz(c)，b∈[0,π]；奇异处固定c=0。"""
    U=np.asarray(U,complex)
    assert np.max(np.abs(U@U.conj().T-I2))<1e-8
    assert abs(np.linalg.det(U)-1)<1e-8
    b=2*np.arctan2(abs(U[1,0]),abs(U[0,0]));s=np.sin(b/2);c=np.cos(b/2)
    if s<1e-12:
        alpha=-2*np.angle(U[0,0]);a,c=alpha,0.
    elif c<1e-12:
        beta=2*np.angle(U[1,0]);a,c=beta,0.
    else:
        alpha=-2*np.angle(U[0,0]);beta=2*np.angle(U[1,0]);a,c=(alpha+beta)/2,(alpha-beta)/2
    out=np.array([a,b,c],float)
    # 只在重构误差需要时绕2π选择等价代表，不改变门。
    V=su2(out)
    if np.max(np.abs(V-U))>1e-8:
        raise AssertionError(('zxz reconstruction',np.max(np.abs(V-U)),out,U))
    return out

def canonicalize(p,edges):
    phase,layers=unpack(p);edges=[tuple(e) for e in edges];k=len(edges)
    assert len(layers)==k+1
    moves=[]
    for i,(a,b) in enumerate(edges):
        idle=({0,1,2}-{a,b}).pop();old=[q.copy() for q in layers[i]]
        aa=[]
        for q in (a,b):
            t=zxz(layers[i][q]);aa.append(float(t[0]))
            layers[i][q]=rz(-t[0])@layers[i][q]
            layers[i+1][q]=layers[i+1][q]@rz(t[0])
        G=layers[i][idle].copy()
        layers[i][idle]=G.conj().T@layers[i][idle]
        layers[i+1][idle]=layers[i+1][idle]@G
        moves.append({'boundary':i,'edge':[a,b],'idle':idle,'edge_absorbed_a':aa,
                      'idle_absorption_frobenius':float(np.linalg.norm(G-old[idle]))})
    # 数值消元闸：首角、空闲门、全程酉性。
    max_a=max_i=0.
    for i in range(k):
        a,b=edges[i];idle=({0,1,2}-{a,b}).pop()
        for q in (a,b): max_a=max(max_a,abs(zxz(layers[i][q])[0]))
        max_i=max(max_i,float(np.max(np.abs(layers[i][idle]-I2))))
    assert max_a<1e-8 and max_i<1e-12,(max_a,max_i)
    return phase,layers,{'boundaries':moves,'max_absorbed_first_angle':max_a,'max_idle_identity_error':max_i}

def known_answer_gate():
    rng=np.random.default_rng(230023);worst=0.
    cases=[]
    for k in (1,2,7):
        for rep in range(4):
            edges=[(0,1) if (j+rep)%2==0 else (1,2) for j in range(k)]
            p=rng.normal(size=1+9*(k+1));_,L0=unpack(p)
            U0=circuit_layers(L0,edges,p[0]);ph,L,moves=canonicalize(p,edges)
            U1=circuit_layers(L,edges,ph);e=float(np.max(np.abs(U1-U0)));worst=max(worst,e)
            assert e<2e-12,e
            pc=pack(ph,L);_,Lc=unpack(pc)
            ec=float(np.max(np.abs(circuit_layers(Lc,edges,pc[0])-U0)));worst=max(worst,ec)
            assert ec<2e-12,ec
            cases.append({'k':k,'rep':rep,'matrix_preserved':e,'repack_preserved':ec})
    return {'random_cases':cases,'max_matrix_error':worst}

def main():
    gate=known_answer_gate()
    src=json.loads((R22/'ad22_maj_7cz.json').read_text())
    out={'beat':'AD-23','kind':'exact_gauge_compression_not_exact_target_certificate',
         'coordinate_formula':'4*k+10; k=7 gives 38','known_answer_gate':gate,'hits':[]}
    for h in src['hits']:
        p=np.asarray(h['x'],float);edges=h['edges'];_,L0=unpack(p)
        U0=circuit_layers(L0,edges,p[0]);ph,L,meta=canonicalize(p,edges)
        U1=circuit_layers(L,edges,ph);pc=pack(ph,L);_,Lc=unpack(pc)
        e=float(np.max(np.abs(U1-U0)));er=float(np.max(np.abs(circuit_layers(Lc,edges,pc[0])-U0)))
        assert e<2e-12 and er<2e-12,(h['idx'],h['restart'],e,er)
        th=pc[1:].reshape(8,3,3)
        out['hits'].append({'idx':h['idx'],'restart':h['restart'],'edges':edges,
                            'source_independent_e':h.get('independent_e'),
                            'x_canonical':pc.tolist(),'canonical_angles':th.tolist(),
                            'matrix_preservation':e,'repack_preservation':er,'gauge_meta':meta})
    raw=json.dumps(out,indent=2).encode()+b'\n';(R23/'ad23_gauge.json').write_bytes(raw)
    print(json.dumps({'status':'GAUGE_PASS','known_random_cases':len(gate['random_cases']),
                      'known_max_matrix_error':gate['max_matrix_error'],'hits':len(out['hits']),
                      'sha256':hashlib.sha256(raw).hexdigest()},indent=2))
if __name__=='__main__':main()
