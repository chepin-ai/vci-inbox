"""AD-21: G1/G2 深谷的六个有向 M(a,b)⊗Z(c) 嵌入分类。
只从 AD-20 原始 JSONL 重选解；不以优化器停止码代替电路/谱判据。
"""
import itertools, json, sys
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent.parent
RUN = BASE/'run'
sys.path.insert(0, str(BASE))
import toffoli_solver as ts

I = np.eye(2, dtype=complex)
PAULI = {'I':I, 'X':np.array([[0,1],[1,0]],complex),
         'Y':np.array([[0,-1j],[1j,0]],complex), 'Z':np.diag([1,-1]).astype(complex)}
ALPHA = np.pi/8
TARGETS = {'G1':ts.toffoli({0,1},2), 'G2':ts.toffoli({0,2},1)}

def pm(s):
    return np.kron(np.kron(PAULI[s[0]],PAULI[s[1]]),PAULI[s[2]])

def string_for(a,b,c,sa,sb,sc='Z'):
    s=['I']*3; s[a]=sa; s[b]=sb; s[c]=sc
    return ''.join(s)

def basis_names(perm):
    a,b,c=perm
    return [string_for(a,b,c,'Z','X'), string_for(a,b,c,'Z','I'),
            string_for(a,b,c,'Y','I'), string_for(a,b,c,'X','I'),
            string_for(a,b,c,'Y','X'), string_for(a,b,c,'X','X')]

def H_of(x,idx,target):
    seq=list(itertools.product(ts.PATH,repeat=7))[idx]
    U=ts.U_of(np.asarray(x),seq)
    vals,vecs=np.linalg.eig(U@target)
    ang=np.angle(vals)
    K=vecs@np.diag(ang)@np.linalg.inv(vecs)
    H=(K/ALPHA+(K/ALPHA).conj().T)/2
    return H,ang,float(np.max(np.abs(U-target)))

def fit(H,perm):
    names=basis_names(perm)
    co=np.array([float((np.trace(pm(s)@H)/8).real) for s in names])
    u,v,w,t=co[:4]
    theta=float(np.arccos(np.clip(u+v,-1,1)))
    phi=float(np.arctan2(t,w))
    branches=[]
    for sigma in [1,-1]:
        us=(sigma+np.cos(theta))/2; vs=(np.cos(theta)-sigma)/2
        ws=np.sin(theta)*np.cos(phi)/2; ts_=np.sin(theta)*np.sin(phi)/2
        H0=us*pm(names[0])+vs*pm(names[1])+ws*(pm(names[2])+pm(names[4]))+ts_*(pm(names[3])+pm(names[5]))
        branches.append({'perm':list(perm),'sigma_u_minus_v':sigma,'basis':names,'coefficients_uvwt':[u,v,w,t],
                'pair_w_delta':float(w-co[4]),'pair_t_delta':float(t-co[5]),
                'theta':theta,'phi':phi,'ansatz_max_delta':float(np.max(np.abs(H-H0))),
                'H0_involution_max':float(np.max(np.abs(H0@H0-np.eye(8))))})
    return min(branches,key=lambda r:r['ansatz_max_delta'])

def best_records():
    scan=[json.loads(s) for s in (RUN/'ad20_g2k7_scan.jsonl').read_text().splitlines() if s.strip()]
    targeted=[json.loads(s) for s in (RUN/'ad20_targeted.jsonl').read_text().splitlines() if s.strip()]
    out=[]
    for idx in [34,38,52,91]:
        cand=[{'x':r['best']['x'],'e':r['best']['e'],'source':'scan'} for r in scan if r['idx']==idx]
        cand += [{'x':r['x'],'e':r['e'],'source':'targeted'} for r in targeted if r['idx']==idx]
        r=min(cand,key=lambda z:z['e'])
        out.append(('G2',idx,r['x'],r['source']))
    p=json.loads((RUN/'ad20_g1k7_polish.json').read_text())
    out.append(('G1',85,p['x'],'polish'))
    return out

def main():
    rows=[]
    for geometry,idx,x,source in best_records():
        H,angles,e=H_of(x,idx,TARGETS[geometry])
        fits=sorted((fit(H,p) for p in itertools.permutations(range(3))),key=lambda r:r['ansatz_max_delta'])
        rows.append({'geometry':geometry,'idx':idx,'source':source,'direct_e':e,
                     'angle_max_dev_rad':float(np.max(np.abs(np.abs(angles)-ALPHA))),
                     'H_involution_max':float(np.max(np.abs(H@H-np.eye(8)))),
                     'fits':fits,'best_perm':fits[0]['perm'],'best_sigma':fits[0]['sigma_u_minus_v'],'best_ansatz_max_delta':fits[0]['ansatz_max_delta']})
    out={'beat':'AD-21','cases':rows}
    (RUN/'ad21_embeddings.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'cases':[{**{k:r[k] for k in ['geometry','idx','direct_e','angle_max_dev_rad','H_involution_max','best_perm','best_sigma','best_ansatz_max_delta']},
                               'runner_up_delta':r['fits'][1]['ansatz_max_delta']} for r in rows]},indent=2))

if __name__=='__main__': main()
