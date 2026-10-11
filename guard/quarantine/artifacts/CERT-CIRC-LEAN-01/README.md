# artifacts/CERT-CIRC-LEAN-01 — rev 段（[EXT-WAVE-05 drift-repair]）

## rev v4341（2026-10-11，PIVOT-01 工程线）
环境：leanprover/lean4:v4.34.1 + mathlib v4.34.1 @d13f23b7 + leancert @7f91b6eb3567437f6cfac03ed279706603ee22f4（tag v4.34.1 原指向；远端 tag 已漂移至 a5777840，本构建按工件注释钉死 7f91b6eb35）。leancert 库本体源码编译全绿。

v4341 修复内容：矩阵字面量去掉行外括号（`!![[…];[…]]` → `!![…;…]`），消除 v4.34.1 下的
类型漂移（Matrix (Fin n) (Fin 1) (List ?m)）与 19×19 心跳超时——阐释层全部转绿。

**残余结构性阻塞（如实记录）**：native_decide 判 `krawczykCheck … = true` 为 false。
根因诊断（逐合取项探针）：centerInside=true，但 checkADSupported 对全部方程=false——
leancert 的 ADSupported 片段（const/var/add/mul/neg/sin/cos/exp，自功能引入提交 4bf84ea91 起）
不含 Expr.log，而 circSystem 方程含 log；且 Matrix.det 为 Leibniz 定义，n=11/19 组合数爆炸不可机算。
结论：该证书族在其自身钉定的 leancert 版本下按现写法结构性不可验证；需证书内容级重构
（如 log 消除编码 + 证书重算），超出 drift-repair 范畴，建议另开义务。

| 文件 | verdict | sha256 | fp16 |
|---|---|---|---|
| CertCircLean01_v4341.lean | ELAB_OK / CHECK_FALSE(structural) | db27dac12758413c08630972e5b8a2d908201aa85638bb3be6f69d3a5169404e | db27dac12758413c |
| family/CertCircK6E1_2_v4341.lean | ELAB_OK / CHECK_FALSE(structural) | 6f5cd4c7cc403f37944bcdf13f82bc4ec9585aeb5f59a43cf0f17dc3e5755fb7 | 6f5cd4c7cc403f37 |
| family/CertCircK6E1_5_v4341.lean | ELAB_OK / CHECK_FALSE(structural) | 42673c9de1cbd7e4700805ca123a836c41f6ca2e960b2adb8a9897b283e6fc2d | 42673c9de1cbd7e4 |
| family/CertCircK10E1_v4341.lean | ELAB_OK / CHECK_FALSE(structural) | 4361f33d578b7bab5981f7f47bf2bd555de17cabe01cdf0a200bf31025174e30 | 4361f33d578b7bab |
| family/CertCircK10E1_2_v4341.lean | ELAB_OK / CHECK_FALSE(structural) | 248ddcfdda944c447ff03793150c1013cde5c79b256f3ef13c71c9fba8f3e4d0 | 248ddcfdda944c44 |
| CertCircK10E1_5_v4341.lean | ELAB_OK / CHECK_FALSE(structural) | 7714cf0b89946daf051e7adc1f7fde53d736e86a943c6762bdb91557a8607ff9 | 7714cf0b89946daf |

fp16 = sha256 前 16 hex。上游缺陷记录：lakefile.toml `defaultTargets=["certCirc"]` 与 `[[lean_lib]] name="CertCirc"` 大小写不符。
