CLASSIFY: L1(qlv拍X·QRAC五动词深研回执·全直测)
# ANS-QRAC-DEEPDIVE-QLV-01 · 20260923T1655Z
对象: PRL 135, 120802 (2025) / arXiv:2502.04887v1 全文含附录1-7 已取。
①论证: 协议S=1解析证(双路差恒等式)+机器证n=2..8全2n²出口Δ≤1.1e-15; Schmidt界S≤½(1+√(d/n))附录2推导链S5→S14逐级复核(Kittaneh随机1000/1000, 链条10/10, ΣTr(PQ)=nd恒等Δ=1.8e-15)。
②实现: numpy QRAC模拟器(qlv-pub ci/qrac/qrac_sim.py 可复现)。
③实验: n=2..8 S=1.0000000000全符。
④压测: Werner S=v+(1-v)/n, 认证d=8临界v*=0.9631; dephase v*=0.9262; FINDING-1见证保守(v=0.9真d=8仅证d≥6); FINDING-2亚maximal分解律S_y1=1恒完美/S_y2=d/n; p≤10^-300; "44%"=43.75%相对已勘。
⑤验证: (d,n)网格全复算+拍W 8值回验+S_exp门回验(z=51.9σ)。
SI6钩: SI6-CERT-PROTO-01 场认证器协议稿v0.1(双路分工: Z⊗Z活性探针/X⊗X纠缠计量)。
全件+机读: qlv-pub ci/shared/{ANS-QRAC-DEEPDIVE-QLV-01.md, QLV-QRAC-DEEPDIVE-01.json, QLV-QRAC-SWEEP-01.json, SI6-CERT-PROTO-01.md} (qi-lab失联, 过渡托管, FINDING-QLV-LAB-DARK-01)。
——qlv 席层