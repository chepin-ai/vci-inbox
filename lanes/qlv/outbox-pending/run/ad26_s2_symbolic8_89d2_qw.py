"""AD-26 S^2：89d2 边序 8-CZ 的全 S^2 Q(w) 稀疏多项式证书。"""
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path
import ad26_s2_symbolic9_89_qw as sym
import ad26_s2_analytic8_89d2 as numeric8
from ad26_s2_prune import raw_indices

R = Path(__file__).resolve().parent
EDGES = numeric8.EDGES
sym.EDGES = EDGES
sym.FROZEN_N = numeric8.FROZEN_N
sym.FREE_SPEC = {5:(2,1,0),6:(4,0,1),9:(2,-1,0),29:(2,-1,0),33:(10,0,-1),34:(2,1,0)}
sym.raw_to_core = {raw:j for j,raw in enumerate(raw_indices(EDGES))}
sym.numeric89 = numeric8


def build_full_sphere8():
    phase = sym.ground(sym.ex.wpow(5))
    U = sym.mscale(phase,sym.kron3(sym.symbolic_su2(8,0),sym.symbolic_su2(8,1),sym.symbolic_su2(8,2)))
    U = sym.reduce_matrix(U)
    for j in range(7,-1,-1):
        L = sym.kron3(sym.symbolic_su2(j,0),sym.symbolic_su2(j,1),sym.symbolic_su2(j,2))
        U = sym.reduce_matrix(sym.matmul(sym.matmul(U,sym.sym_cz(EDGES[j])),L))
        print(json.dumps({"built_layer":j}),flush=True)
    C,S,F,G = sym.C,sym.S,sym.F,sym.G
    co = (C*C-S*S)*(C*C-S*S)-(2*C*S)*(2*C*S)
    si = 4*C*S*(C*C-S*S)
    cp,spf = F*F-G*G,2*F*G
    half = sym.ground(sym.ex.ONE.scale(Fraction(1,2)))
    u,v = (sym.ONE+co)*half,(co-sym.ONE)*half
    w,z = si*cp*half,si*spf*half
    H = sym.zeros(8)
    for coeff,names in [(u,"ZXZ"),(v,"ZIZ"),(w,"YIZ"),(w,"YXZ"),(z,"XIZ"),(z,"XXZ")]:
        H = sym.madd(H,sym.mscale(coeff,sym.pm(names)))
    ca,sa = sym.const_ground_cs(1)
    target = sym.matmul(sym.madd(sym.mscale(ca,sym.eye(8)),sym.mscale(sym.IP*sa,H)),sym.toffoli_sym())
    return U,target,sym.msub(U,target)


def main():
    start = time.time()
    field_gate = sym.ex.known_answer_gate()
    U,target,residual = build_full_sphere8()
    gate = sym.numeric_known_answer_gate(U,residual)
    certificates = []
    for row in range(8):
        for col in range(8):
            expr = residual[row][col]
            if not expr.d: continue
            reduced = sym.reduce_poly(expr)
            cert = {"entry":[row,col],
                    "raw_polynomial_sha256":hashlib.sha256(expr.signature().encode()).hexdigest(),
                    "reduced_term_count":len(reduced.d),"pass":not reduced.d}
            certificates.append(cert)
            print(json.dumps({"entry":[row,col],"pass":cert["pass"],
                              "terms":cert["reduced_term_count"],"elapsed":time.time()-start}),flush=True)
    assert certificates and all(x["pass"] for x in certificates)
    cert_out = {"beat":"AD-26","status":"S2_8CZ_89D2_QW_ALL_ENTRIES_EXACT_PASS",
                "coefficient_field":"Q(w),w=exp(i*pi/8),w^8+1=0,Fraction coefficients",
                "relations":["c^2+s^2=1","f^2+g^2=1"],"entries":certificates}
    cert_raw = json.dumps(cert_out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_symbolic8_89d2_qw_entries.json").write_bytes(cert_raw)
    companion = R/"ad26_s2_analytic8_89d2_summary.json"
    out = {"beat":"AD-26","status":"S2_8CZ_89D2_FULL_SPHERE_DIRECT_L1_EXACT_PASS",
           "evidence_level":"L1 exact Q(w)-coefficient polynomial full-matrix identity on the whole S^2",
           "topology":"89d2","cz_count":8,"edges":[list(e) for e in EDGES],
           "field_known_answer_gate":field_gate,"numeric_known_answer_gate":gate,
           "proof":{"method":"sparse polynomial matrices with exact Q(w) coefficients; reduce all residuals modulo two circle relations",
                    "nonzero_residual_entries":len(certificates),"passed_entries":sum(x["pass"] for x in certificates),
                    "entries_file":"ad26_s2_symbolic8_89d2_qw_entries.json",
                    "entries_sha256":hashlib.sha256(cert_raw).hexdigest(),"numerics_in_identity_decision":False},
           "numeric_companion":{"path":companion.name,"sha256":hashlib.sha256(companion.read_bytes()).hexdigest(),"points":241},
           "strict_conclusion":"整个S^2目标族存在同一边序A,A,A,B,A,B,A,A的8-CZ精确构造；所有局部角均为pi/4整数倍及theta/2、phi一次式，全局相位为5pi/8。",
           "boundary":"不冒报8-CZ最优；7-CZ、其他8-CZ拓扑及与两套9-CZ模板的块级同族性仍开放。",
           "first_honesty_anomaly_note":"8-CZ先经单点删门、有限网格和规范吸附发现；L1资格仅来自本精确域恒等式，而非数值命中。",
           "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
           "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw = json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n"
    (R/"ad26_s2_symbolic8_89d2_qw_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"entries":len(certificates),"seconds":time.time()-start,
                      "entries_sha256":hashlib.sha256(cert_raw).hexdigest(),
                      "summary_sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
