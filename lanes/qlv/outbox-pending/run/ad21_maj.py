"""AD-21 完整可逆 MAJ 细胞：10 CZ 构造上界与 9/8 CZ 删门压缩。"""
import itertools, json, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

BASE=Path(__file__).resolve().parent.parent
RUN=BASE/'run'
sys.path.insert(0,str(BASE))
import toffoli_solver as ts

I2=np.eye(2)
H2=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)

def one(q,U):
    ops=[np.eye(2)]*3;ops[q]=U
    return np.kron(np.kron(ops[0],ops[1]),ops[2])
def cnot(c,t): return one(t,H2)@ts.cz3(c,t)@one(t,H2)
def maj_target():
    T=np.zeros((8,8),complex)
    table=[]
    for x in range(8):
        a,b,c=(x>>2)&1,(x>>1)&1,x&1
        y=[a^b, int((a+b+c)>=2), b^c]
        yi=(y[0]<<2)|(y[1]<<1)|y[2]
        T[yi,x]=1;table.append({'input':[a,b,c],'output':y})
    return T,table
MAJ,MAJ_TABLE=maj_target()

def locals_of(p,k):
    th=np.asarray(p[1:]).reshape(k+1,3,3)
    return [[ts.su2(th[i,q]) for q in range(3)] for i in range(k+1)]
def euler_su2(U):
    cb,sb=abs(U[0,0]),abs(U[1,0]); b=2*np.arctan2(sb,cb)
    if sb>1e-10 and cb>1e-10:
        sm=-2*np.angle(U[0,0]); df=-2*np.angle(-U[0,1])
        a,c=(sm+df)/2,(sm-df)/2
    elif sb<=1e-10:
        a,c=-2*np.angle(U[0,0]),0.;b=0.
    else:
        a,c=-2*np.angle(-U[0,1]),0.;b=np.pi
    err=float(np.max(np.abs(ts.su2([a,b,c])-U)))
    assert err<2e-12,('euler',err,U)
    return [float(a),float(b),float(c)]
def pack(phase,layers):
    return [float(phase)]+[a for layer in layers for U in layer for a in euler_su2(U)]
def concat_params(pA,edgesA,pB,edgesB):
    """返回 B@A；边序=A后B，边界局部层作 SU2 精确合并。"""
    ka,kb=len(edgesA),len(edgesB);LA,LB=locals_of(pA,ka),locals_of(pB,kb)
    layers=LA[:-1]+[[LB[0][q]@LA[-1][q] for q in range(3)]]+LB[1:]
    assert len(layers)==ka+kb+1
    return pack(pA[0]+pB[0],layers),list(edgesA)+list(edgesB)
def delete_one(p,edges,j):
    k=len(edges);L=locals_of(p,k)
    newL=L[:j]+[[L[j+1][q]@L[j][q] for q in range(3)]]+L[j+2:]
    newe=edges[:j]+edges[j+1:]
    return pack(p[0],newL),newe

def cnot_param(c,t):
    # H = i Rz(0) Ry(pi/2) Rz(pi)；两个H与全局相位pi合成CNOT。
    z=[0.,0.,0.];h=[0.,np.pi/2,np.pi]
    th=[]
    for layer in range(2):
        for q in range(3): th += h if q==t else z
    return [np.pi]+th

def optimize(task):
    kind,deleted,p,edges=task
    ts._cache.clear();t0=time.time()
    sol=least_squares(ts.f_resid,np.asarray(p),jac=ts.j_resid,args=(edges,MAJ.reshape(-1)),
                      method='lm',max_nfev=3000,ftol=1e-15,xtol=1e-15,gtol=1e-15)
    e=float(np.max(np.abs(sol.fun[:64]+1j*sol.fun[64:])))
    return {'kind':kind,'deleted':list(deleted),'k':len(edges),'edges':edges,
            'e':e,'nfev':int(sol.nfev),'status':int(sol.status),'optimality':float(sol.optimality),
            'seconds':time.time()-t0,'x':sol.x.tolist()}

def main():
    # 已知答案门：MAJ真值表、双CNOT+Toffoli恒等式、CNOT参数化均须先通过。
    T2=ts.toffoli({0,2},1)
    composition_identity_max=float(np.max(np.abs(T2@cnot(1,2)@cnot(1,0)-MAJ)))
    assert composition_identity_max<1e-15,composition_identity_max
    assert np.array_equal(np.sum(MAJ,axis=0),np.ones(8)) and np.array_equal(np.sum(MAJ,axis=1),np.ones(8))
    assert len({tuple(r['output']) for r in MAJ_TABLE})==8  # 可逆；该门并非对合，禁止误加MAJ²=I。
    c1=cnot_param(1,0);c2=cnot_param(1,2)
    assert np.max(np.abs(ts.U_of(c1,[(0,1)])-cnot(1,0)))<1e-12
    assert np.max(np.abs(ts.U_of(c2,[(1,2)])-cnot(1,2)))<1e-12
    t8=json.loads((BASE/'toffoli_path_8cz.json').read_text())['G2_路径Toffoli_控02靶1']
    p8,e8=t8['params'],[tuple(z) for z in t8['edges']]
    p12,e12=concat_params(c1,[(0,1)],c2,[(1,2)])
    p10,e10=concat_params(p12,e12,p8,e8)
    constructed_e=float(np.max(np.abs(ts.U_of(p10,e10)-MAJ)))
    assert constructed_e<1e-11,constructed_e
    # 自检删门参数化：不优化时，删门初值必须等于手工删去同一CZ的矩阵。
    p9,e9=delete_one(p10,e10,0)
    assert len(p9)==91 and len(e9)==9
    tasks=[]
    for j in range(10):
        p,e=delete_one(p10,e10,j);tasks.append(('delete_from_10',[j],p,e))
    for i,j in itertools.combinations(range(10),2):
        p,e=delete_one(p10,e10,j);p,e=delete_one(p,e,i)
        tasks.append(('delete_pair_from_10',[i,j],p,e))
    t0=time.time();rows=[]
    with (RUN/'ad21_maj.jsonl').open('w',buffering=1) as f:
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs={ex.submit(optimize,t):t for t in tasks}
            for n,fut in enumerate(as_completed(futs),1):
                t=futs[fut]
                try:r=fut.result()
                except Exception as exc:r={'kind':t[0],'deleted':list(t[1]),'k':len(t[3]),'edges':t[3],
                                            'error':type(exc).__name__+': '+str(exc)}
                rows.append(r);f.write(json.dumps(r,separators=(',',':'))+'\n');f.flush()
                if n%10==0 or n==len(tasks):print(json.dumps({'event':'progress','done':n,'total':len(tasks),'elapsed':time.time()-t0}),flush=True)
    valid=[r for r in rows if 'error' not in r]
    summary={'beat':'AD-21','target':'(a,b,c)->(a xor b,maj(a,b,c),b xor c)',
             'truth_table':MAJ_TABLE,'construction_10cz':{'edges':e10,'params':p10,'e':constructed_e},
             'runs':len(rows),'errors':len(rows)-len(valid),'seconds':time.time()-t0,
             'best_by_k':{str(k):min(({'e':r['e'],'deleted':r['deleted'],'nfev':r['nfev'],'status':r['status']}
                                      for r in valid if r['k']==k),key=lambda z:z['e'],default=None) for k in [9,8]},
             'exact_by_k':{str(k):sum(r['e']<1e-9 for r in valid if r['k']==k) for k in [9,8]}}
    (RUN/'ad21_maj_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
