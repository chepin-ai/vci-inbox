# artifacts/lean-verified — rev 段（[EXT-WAVE-05 drift-repair]）

## rev v4341（2026-10-11，PIVOT-01 工程线）
环境：leanprover/lean4:v4.34.1（5045d00564）+ mathlib v4.34.1 @d13f23b723b8a846827a245b89c10fc7d3f11612 全量缓存。
Mathlib v4.34.1 的 Fintype deriving 处理器回归（enumList_nodup 类型漂移，最小复现：`inductive Foo | a | b deriving Fintype` 即失败）；
v4341 改为手工 Fintype 实例（语义等价同全集），原件 sha 不动。

| 文件 | verdict | sha256 | fp16 |
|---|---|---|---|
| CertK4Lean01_v4341.lean | COMPILE_OK (exit=0) | ab14e47efb37d40694259c503dcd7899aa9357bf5a9abe1a118b4dc1a0217992 | ab14e47efb37d406 |
| CertLatticeLean01_v4341.lean | COMPILE_OK (exit=0) | f01ad47321c276ec4ba831ea2b9318d97ac29f61be84ce0e85797c0885e8cec2 | f01ad47321c276ec |

fp16 = sha256 前 16 hex。
