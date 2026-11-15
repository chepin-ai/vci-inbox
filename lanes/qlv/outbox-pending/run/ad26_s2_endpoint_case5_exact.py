"""AD-26 theta=0 对角恒等式与 Shende--Markov case 5b 的 Q(w) 精确证书。"""
import hashlib,importlib.util,json,time
from pathlib import Path

R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("ad26_endpoint_exact_field",R.parent.parent/"ad23/run/ad23_exact.py")
ex=importlib.util.module_from_spec(spec);spec.loader.exec_module(ex)
F=ex.F;Z=ex.Z;ONE=ex.ONE


def op(q,A):
    ms=[ex.eye(2),ex.eye(2),ex.eye(2)];ms[q]=A
    return ex.kron(ex.kron(ms[0],ms[1]),ms[2])


def delta(q,n):return op(q,ex.diag2(ONE,ex.wpow(n)))
def diagonal(entries):return [[entries[i] if i==j else Z for j in range(8)] for i in range(8)]
def phase_n(x):
    hits=[n for n in range(16) if x.a==ex.wpow(n).a]
    assert len(hits)==1,repr(x)
    return hits[0]


def main():
    start=time.time();gate=ex.known_answer_gate()
    X=[[Z,ONE],[ONE,Z]];Zz=ex.diag2(ONE,-ONE);I2=ex.eye(2)
    invsqrt2=(ex.wpow(2)+ex.wpow(-2)).scale(F(1,2))
    H=[[invsqrt2,invsqrt2],[invsqrt2,-invsqrt2]]
    H1=op(1,H);ZXZ=ex.mm(ex.mm(op(0,Zz),op(1,X)),op(2,Zz))
    ZZZ=ex.mm(ex.mm(op(0,Zz),op(1,Zz)),op(2,Zz));T=ex.toffoli({0,2},1)
    w,wm=ex.wpow(1),ex.wpow(-1);co,isi=(w+wm).scale(F(1,2)),(w-wm).scale(F(1,2))
    def phase_pauli(P):return [[co*a+isi*p for a,p in zip(ri,rp)] for ri,rp in zip(ex.eye(8),P)]
    V=ex.mm(phase_pauli(ZXZ),T);D=ex.mm(ex.mm(H1,V),H1)
    CCZ=ex.mm(ex.mm(H1,T),H1);Rdiag=ex.mm(phase_pauli(ZZZ),CCZ)
    diagonal_identity_nz=ex.nonzero_entries(ex.md(D,Rdiag));assert diagonal_identity_nz==0
    # H_t CX(c,t) H_t = CZ(c,t)，用于把论文的五个 CX 逐个换成五个 CZ。
    cx_cz_nz=0
    for c,t in [(1,2),(0,1),(1,2),(0,1),(0,2)]:
        Ht=op(t,H);converted=ex.mm(ex.mm(Ht,ex.cz((c,t))),Ht)
        cx_cz_nz+=ex.nonzero_entries(ex.md(converted,ex.cnot(c,t)))
    assert cx_cz_nz==0
    # case 5b：alpha=beta=gamma=w^2；初始 Delta(i)，逆根 Delta(w^-2)。
    C=delta(0,4)
    C=ex.mm(C,delta(1,4));C=ex.mm(C,delta(2,4))
    schedule=[]
    def apply(name,M):
        nonlocal C
        C=ex.mm(M,C);schedule.append(name)
    apply("CX(1,2)",ex.cnot(1,2))
    apply("CX(0,1)",ex.cnot(0,1))
    apply("Delta(q2,w^-2)",delta(2,14))
    apply("CX(1,2)",ex.cnot(1,2))
    apply("Delta(q1,w^-2)",delta(1,14));apply("Delta(q2,w^-2)",delta(2,14))
    apply("CX(0,1)",ex.cnot(0,1));apply("CX(0,2)",ex.cnot(0,2))
    canonical=diagonal([ONE,ONE,ONE,ex.wpow(4),ONE,ex.wpow(4),ex.wpow(4),ex.wpow(12)])
    case5_canonical_nz=ex.nonzero_entries(ex.md(C,canonical));assert case5_canonical_nz==0
    outer=delta(0,14)
    outer=ex.mm(outer,delta(1,14));outer=ex.mm(outer,delta(2,14))
    Dcase=ex.mm(outer,C);Dcase=[[w*x for x in row] for row in Dcase]
    case5_full_nz=ex.nonzero_entries(ex.md(Dcase,D));assert case5_full_nz==0
    # 负控制：CX(0,2) 自逆，左乘可消去 case 核心最左的 02 门。
    C_without02=ex.mm(ex.cnot(0,2),C)
    negative_nz=ex.nonzero_entries(ex.md(C_without02,canonical));assert negative_nz>0
    phases=[phase_n(D[i][i]) for i in range(8)]
    lam1=(phases[3]+phases[0]-phases[1]-phases[2])%16
    lam2=(phases[5]+phases[0]-phases[4]-phases[1])%16
    lam3=(phases[6]+phases[0]-phases[4]-phases[2])%16
    xi=(phases[7]+2*phases[0]-phases[4]-phases[2]-phases[1])%16
    assert (lam1,lam2,lam3,xi)==(4,4,4,12)
    ratios=[(lam1+lam2-lam3)%16,(lam1+lam3-lam2)%16,(lam2+lam3-lam1)%16]
    assert ratios==[4,4,4] and (lam1+lam2+lam3)%16==xi
    out={"beat":"AD-26","status":"S2_THETA0_DIAGONAL_AND_UNRESTRICTED_5CZ_EXACT_PASS",
         "field":"Q(w), w=exp(i*pi/8), w^8+1=0, Fraction coefficients",
         "known_answer_gate":gate,
         "diagonal_identity":{"formula":"H_1 target(0,0) H_1 = (cos(pi/8) I + i sin(pi/8) ZZZ) CCZ",
                              "nonzero_residual_entries":diagonal_identity_nz,"cx_to_cz_nonzero_residual_entries":cx_cz_nz},
         "diagonal_phase_pi_over_8":phases,
         "shende_markov_invariants_pi_over_8":{"lambda1":lam1,"lambda2":lam2,"lambda3":lam3,"xi":xi,
             "ab_over_c":ratios[0],"ac_over_b":ratios[1],"bc_over_a":ratios[2],"abc":(lam1+lam2+lam3)%16},
         "case5b":{"source":"Shende--Markov, On the CNOT-cost of TOFFOLI gates (2009), Theorem 14 case 5b, printed p.481",
             "square_roots":"alpha=beta=gamma=w^2","schedule_left_to_right":schedule,
             "cx_edges_in_time_order":[[1,2],[0,1],[1,2],[0,1],[0,2]],
             "cz_count_after_H_conjugation":5,"canonical_nonzero_residual_entries":case5_canonical_nz,
             "full_target_including_global_phase_nonzero_residual_entries":case5_full_nz,
             "delete_02_negative_control_nonzero_entries":negative_nz},
         "minimum_unrestricted_three_qubit_cz":5,
         "minimum_reason":"s(D)=(i,i,i;-i)=abc 类；三个 ab/c 型比值均为 i，不等于 xi=-i，且不属于定理14的0至4门特殊类；case 5b 给出5门构造。",
         "evidence_level":"L1 exact arithmetic for theta=0 plus cited external classification; not a full-S^2 result",
         "boundary":"构造使用一条02边，故只证明 unrestricted 三比特图、无辅助比特的 theta=0 端点最小5-CZ；不证明 PATH=A,B 最小5，也不给出全 S^2 5-CZ 或6-CZ最优。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_endpoint_case5_exact_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"diagonal_identity_nz":diagonal_identity_nz,
         "case5_full_nz":case5_full_nz,"phases":phases,"invariants":[lam1,lam2,lam3,xi],
         "minimum_unrestricted_three_qubit_cz":5,"negative_control_nz":negative_nz,
         "seconds":time.time()-start,"sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
