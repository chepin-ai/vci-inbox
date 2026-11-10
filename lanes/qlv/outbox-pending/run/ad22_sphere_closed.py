"""AD-22 S² 闭式几何与7-CZ解析纬圈。
定理层：H=R_z(-phi) W_theta H_00 W_theta† R_z(-phi)†；A与Toffoli对易。
电路层：phi共轭是控制位局域Z旋转，吸收进首末SU(2)层，CZ序列/数量不变。
theta只证目标闭式，不宣称同模板经线解析提升。
"""
import itertools,json,sys
from pathlib import Path
import numpy as np
AD21=Path('/mnt/agents/output/.stash/ad21/run');RUN=Path('/mnt/agents/output/.stash/ad22/run')
sys.path.insert(0,str(AD21.parent));sys.path.insert(0,str(AD21))
import toffoli_solver as ts
import ad21_geometry as g
from ad21_tangent import target_of,ALPHA
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)


def op(q,A):
    m=[I,I,I];m[q]=A;return np.kron(np.kron(m[0],m[1]),m[2])
def Rx(t):return np.cos(t/2)*I-1j*np.sin(t/2)*X
def local_R(a,delta):return op(a,ts.mRz(-delta))
def controlled_W(a,b,delta):
    pp=(I+X)/2;pm=(I-X)/2
    return op(b,pm)+op(b,pp)@op(a,Rx(-delta))
def angles_of_su2(U):
    U=np.asarray(U,complex)/np.sqrt(np.linalg.det(U));c=float(np.clip(abs(U[0,0]),0,1));b=2*np.arccos(c);s=np.sin(b/2)
    if s<1e-10:
        if c>.5:a,c=np.angle(U[1,1])-np.angle(U[0,0]),0.
        else:a,c=np.angle(U[1,0])-np.angle(-U[0,1]),0.
    else:a=np.angle(U[1,0])-np.angle(U[0,0]);c=np.angle(-U[0,1])-np.angle(U[0,0])
    return np.array([a,b,c])
def phi_circuit(x,perm,delta):
    k=(len(x)-1)//9-1;th=np.asarray(x[1:]).reshape(k+1,3,3).copy();a=perm[0]
    R=ts.mRz(-delta)
    th[k,a]=angles_of_su2(R@ts.su2(th[k,a]));th[0,a]=angles_of_su2(ts.su2(th[0,a])@R.conj().T)
    return np.concatenate([[x[0]],th.reshape(-1)])


def geometry_gate():
    rng=np.random.default_rng(227000);maxh=maxv=maxcomm=maxblock=0.;count=0
    for perm in itertools.permutations(range(3)):
        a,b,c=perm;T=ts.toffoli({a,c},b)
        for sigma in [-1,1]:
            for _ in range(24):
                th0,ph0=rng.uniform(.03,np.pi-.03),rng.uniform(-np.pi,np.pi)
                th,ph=rng.uniform(0,np.pi),rng.uniform(-np.pi,np.pi)
                H0=g.sphere(perm,sigma,th0,ph0);H=g.sphere(perm,sigma,th,ph)
                R0=local_R(a,ph0);W0=controlled_W(a,b,th0)
                R=local_R(a,ph);W=controlled_W(a,b,th)
                pole=g.sphere(perm,sigma,0.,0.)
                H00=R0@W0@pole@W0.conj().T@R0.conj().T
                # 从(th0,ph0)到(th,ph)：A=R(ph) W(th-th0) R(ph0)†。
                A=R@controlled_W(a,b,th-th0)@R0.conj().T
                V0=target_of(H0,T,ALPHA);V=target_of(H,T,ALPHA)
                maxh=max(maxh,float(np.max(np.abs(H-A@H0@A.conj().T))))
                maxv=max(maxv,float(np.max(np.abs(V-A@V0@A.conj().T))))
                maxcomm=max(maxcomm,float(np.max(np.abs(A@T-T@A))))
                maxblock=max(maxblock,float(np.max(np.abs(H0-H00))))
                count+=1
    assert max(maxh,maxv,maxcomm,maxblock)<2e-12,(maxh,maxv,maxcomm,maxblock)
    return {'cases':count,'sphere_identity_max':maxh,'target_identity_max':maxv,
            'toffoli_commutation_max':maxcomm,'pole_identity_max':maxblock}


def circuit_cases():
    tan=json.loads((AD21/'ad21_tangent.json').read_text());out=[]
    for case in tan['cases']:
        out.append({'name':case['name'],'form':case['form'],'idx':case['idx'],'perm':{'G1':[1,2,0],'G2':[0,1,2]}[case['form']],
                    'sigma':1,'theta':case['theta'],'phi':case['phi'],'x':case['x_polished']})
    b=json.loads((AD21/'ad21_seq91_base.json').read_text())
    out.append({'name':'G2k7_seq91','form':'G2','idx':91,'perm':b['perm'],'sigma':b['sigma'],
                'theta':b['theta'],'phi':b['phi'],'x':b['x']})
    return out


def main():
    gate=geometry_gate();records=[];base_gates=[]
    for case in circuit_cases():
        perm=tuple(case['perm']);a,b,c=perm;T=ts.toffoli({a,c},b);edges=list(itertools.product(ts.PATH,repeat=7))[case['idx']]
        x=np.asarray(case['x']);H0=g.sphere(perm,case['sigma'],case['theta'],case['phi']);V0=target_of(H0,T,ALPHA)
        e0=float(np.max(np.abs(ts.U_of(x,edges)-V0)));assert e0<1e-8,(case['name'],e0)
        base_gates.append({'case':case['name'],'base_e':e0})
        for j in range(25):
            delta=2*np.pi*j/24;ph=case['phi']+delta;H=g.sphere(perm,case['sigma'],case['theta'],ph);V=target_of(H,T,ALPHA)
            xp=phi_circuit(x,perm,delta);e=float(np.max(np.abs(ts.U_of(xp,edges)-V)))
            records.append({'case':case['name'],'idx':case['idx'],'perm':case['perm'],'sigma':case['sigma'],
                            'theta':case['theta'],'phi':ph,'delta_phi':delta,'e':e,'x':xp.tolist()})
    emax=max(r['e'] for r in records);assert emax<1e-8,emax
    out={'beat':'AD-22','geometry_known_answer_gate':gate,'base_gates':base_gates,'records':len(records),
         'cases':len(base_gates),'phi_circuits':records,'max_circuit_e':emax,
         'theorem':'每条既有解纬度上的全部phi由首末SU(2)层解析生成；边序与7 CZ不变；delta=2pi闭合。',
         'boundary':'全S²目标矩阵有闭式共轭；theta经线的同7-CZ模板解析提升仍未证，不宣称全S²同模板电路覆盖。'}
    (RUN/'ad22_sphere_closed.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['phi_circuits','base_gates']},indent=2))
if __name__=='__main__':main()
