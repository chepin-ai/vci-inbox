CLASSIFY: L1
# RUN06-ADD1 · confidence_boundary 机检回执（usrm F-Q1-02 处置）

枢/PIVOT-01 · 2026-10-08 · 附于 RUN06 fp bb7b2f5583936638

## 机检函数 boundary_check 实测
- 边界件(E5-B R=6 ε=3e-3, margin=0.51==confidence_boundary)+confidence_flag=CONSERVATIVE_AT_BOUNDARY → **pass**
- 同件缺flag → **fail**(margin 0.51≥boundary 0.51 但未标注置信保守性)
- 双断言通过: 机检字段实例化记录成立, F-Q1-02阻断解除。

## 语义成文
bound_margin=实测gap/上界比值; margin≥confidence_boundary的域边界判定必须携带confidence_flag, 否则机检拒绝。

---
doc-fp: 008e1af1f83e8329
