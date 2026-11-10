"""统一 M(a,b)⊗Z(c) 双分支 S² 几何。"""
import numpy as np
I=np.eye(2,dtype=complex)
PAULI={'I':I,'X':np.array([[0,1],[1,0]],complex),'Y':np.array([[0,-1j],[1j,0]],complex),'Z':np.diag([1,-1]).astype(complex)}
def pm(s):return np.kron(np.kron(PAULI[s[0]],PAULI[s[1]]),PAULI[s[2]])
def sname(a,b,c,sa,sb):
    s=['I']*3;s[a]=sa;s[b]=sb;s[c]='Z';return ''.join(s)
def basis_names(perm):
    a,b,c=perm
    return [sname(a,b,c,'Z','X'),sname(a,b,c,'Z','I'),sname(a,b,c,'Y','I'),
            sname(a,b,c,'X','I'),sname(a,b,c,'Y','X'),sname(a,b,c,'X','X')]
def sphere(perm,sigma,theta,phi):
    n=basis_names(perm)
    u=(sigma+np.cos(theta))/2;v=(np.cos(theta)-sigma)/2
    w=np.sin(theta)*np.cos(phi)/2;t=np.sin(theta)*np.sin(phi)/2
    return u*pm(n[0])+v*pm(n[1])+w*(pm(n[2])+pm(n[4]))+t*(pm(n[3])+pm(n[5]))
def derivatives(perm,sigma,theta,phi):
    n=basis_names(perm)
    du,dv=-np.sin(theta)/2,-np.sin(theta)/2
    dw,dt=np.cos(theta)*np.cos(phi)/2,np.cos(theta)*np.sin(phi)/2
    dtheta=du*pm(n[0])+dv*pm(n[1])+dw*(pm(n[2])+pm(n[4]))+dt*(pm(n[3])+pm(n[5]))
    dphi=(-np.sin(theta)*np.sin(phi)/2)*(pm(n[2])+pm(n[4]))+(np.sin(theta)*np.cos(phi)/2)*(pm(n[3])+pm(n[5]))
    return dtheta,dphi
def realvec(M):
    z=np.asarray(M).reshape(-1);return np.concatenate([z.real,z.imag])
def outside_fraction(perm,dH):
    B=np.column_stack([realvec(pm(s)) for s in basis_names(perm)])
    d=realvec(dH);c,*_=np.linalg.lstsq(B,d,rcond=None);out=d-B@c
    return float(np.linalg.norm(out)/np.linalg.norm(d)),float(np.linalg.norm(out))
def target_of(H,T,alpha):return (np.cos(alpha)*np.eye(8)+1j*np.sin(alpha)*H)@T
