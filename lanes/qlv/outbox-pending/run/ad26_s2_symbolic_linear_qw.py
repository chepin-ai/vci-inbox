"""AD-26 S^2：线性角k-CZ候选的通用Q(w)全矩阵精确证明器。

用法：python3 ad26_s2_symbolic_linear_qw.py ad26_s2_analytic6_89d2d6d2
候选模块必须提供K/TOPOLOGY/PHASE_W/EDGES/FROZEN_N/FREE_SPEC/core/matrix。
"""
import hashlib,importlib,json,sys,time
from fractions import Fraction
from pathlib import Path
import ad26_s2_symbolic9_89_qw as sym
from ad26_s2_prune import raw_indices

R=Path(__file__).resolve().parent


def build(numeric):
    k=numeric.K;sym.EDGES=numeric.EDGES;sym.FROZEN_N=numeric.FROZEN_N;sym.FREE_SPEC=numeric.FREE_SPEC
    sym.raw_to_core={raw:j for j,raw in enumerate(raw_indices(numeric.EDGES))};sym.numeric89=numeric
    U=sym.mscale(sym.ground(sym.ex.wpow(numeric.PHASE_W)),
                 sym.kron3(sym.symbolic_su2(k,0),sym.symbolic_su2(k,1),sym.symbolic_su2(k,2)))
    U=sym.reduce_matrix(U)
    for j in range(k-1,-1,-1):
        L=sym.kron3(sym.symbolic_su2(j,0),sym.symbolic_su2(j,1),sym.symbolic_su2(j,2))
        U=sym.reduce_matrix(sym.matmul(sym.matmul(U,sym.sym_cz(numeric.EDGES[j])),L))
        print(json.dumps({"built_layer":j}),flush=True)
    C,S,F,G=sym.C,sym.S,sym.F,sym.G
    co=(C*C-S*S)*(C*C-S*S)-(2*C*S)*(2*C*S);si=4*C*S*(C*C-S*S)
    cp,spf=F*F-G*G,2*F*G;half=sym.ground(sym.ex.ONE.scale(Fraction(1,2)))
    u,v=(sym.ONE+co)*half,(co-sym.ONE)*half;w,z=si*cp*half,si*spf*half
    H=sym.zeros(8)
    for coeff,names in [(u,"ZXZ"),(v,"ZIZ"),(w,"YIZ"),(w,"YXZ"),(z,"XIZ"),(z,"XXZ")]:
        H=sym.madd(H,sym.mscale(coeff,sym.pm(names)))
    ca,sa=sym.const_ground_cs(1)
    target=sym.matmul(sym.madd(sym.mscale(ca,sym.eye(8)),sym.mscale(sym.IP*sa,H)),sym.toffoli_sym())
    return U,target,sym.msub(U,target)


def main():
    start=time.time();module=sys.argv[1] if len(sys.argv)>1 else "ad26_s2_analytic6_89d2d6d2"
    numeric=importlib.import_module(module);k,stem=numeric.K,numeric.TOPOLOGY
    field_gate=sym.ex.known_answer_gate();U,target,residual=build(numeric)
    gate=sym.numeric_known_answer_gate(U,residual);certificates=[]
    for row in range(8):
        for col in range(8):
            expr=residual[row][col]
            if not expr.d: continue
            reduced=sym.reduce_poly(expr)
            cert={"entry":[row,col],"raw_polynomial_sha256":hashlib.sha256(expr.signature().encode()).hexdigest(),
                  "reduced_term_count":len(reduced.d),"pass":not reduced.d};certificates.append(cert)
            print(json.dumps({"entry":[row,col],"pass":cert["pass"],"terms":cert["reduced_term_count"],
                              "elapsed":time.time()-start}),flush=True)
    assert certificates and all(x["pass"] for x in certificates)
    prefix=f"ad26_s2_symbolic{k}_{stem}_qw"
    cert_out={"beat":"AD-26","status":f"S2_{k}CZ_{stem.upper()}_QW_ALL_ENTRIES_EXACT_PASS",
              "coefficient_field":"Q(w),w=exp(i*pi/8),w^8+1=0,Fraction coefficients",
              "relations":["c^2+s^2=1","f^2+g^2=1"],"entries":certificates}
    cert_raw=json.dumps(cert_out,ensure_ascii=False,indent=2).encode()+b"\n";(R/f"{prefix}_entries.json").write_bytes(cert_raw)
    companion=R/f"ad26_s2_analytic{k}_{stem}_summary.json"
    out={"beat":"AD-26","status":f"S2_{k}CZ_{stem.upper()}_FULL_SPHERE_DIRECT_L1_EXACT_PASS",
         "evidence_level":"L1 exact Q(w)-coefficient polynomial full-matrix identity on the whole S^2",
         "topology":stem,"cz_count":k,"edges":[list(e) for e in numeric.EDGES],
         "field_known_answer_gate":field_gate,"numeric_known_answer_gate":gate,
         "proof":{"method":"sparse polynomial matrices with exact Q(w) coefficients; reduce all residuals modulo two circle relations",
                  "nonzero_residual_entries":len(certificates),"passed_entries":sum(x["pass"] for x in certificates),
                  "entries_file":f"{prefix}_entries.json","entries_sha256":hashlib.sha256(cert_raw).hexdigest(),
                  "numerics_in_identity_decision":False,"candidate_module":module},
         "numeric_companion":{"path":companion.name,"sha256":hashlib.sha256(companion.read_bytes()).hexdigest(),"points":241},
         "strict_conclusion":f"整个S^2目标族存在边序{numeric.EDGES}的{k}-CZ精确线性角构造，全局相位为{numeric.PHASE_W}*pi/8。",
         "boundary":f"不冒报{k}-CZ最优；{k-1}-CZ、其他{k}-CZ拓扑及块级同族性仍开放。",
         "first_honesty_anomaly_note":"候选先经删门、有限网格和规范吸附发现；L1资格仅来自本精确域恒等式。",
         "private_ci_consumption":0,"quantum_machine_actual_consumption_seconds":0,
         "quantum_machine_launched":False,"quantum_account_quota_verified":False}
    raw=json.dumps(out,ensure_ascii=False,indent=2).encode()+b"\n";(R/f"{prefix}_summary.json").write_bytes(raw)
    print(json.dumps({"status":out["status"],"entries":len(certificates),"seconds":time.time()-start,
                      "entries_sha256":hashlib.sha256(cert_raw).hexdigest(),
                      "summary_sha256":hashlib.sha256(raw).hexdigest()},ensure_ascii=False,indent=2))


if __name__=="__main__": main()
