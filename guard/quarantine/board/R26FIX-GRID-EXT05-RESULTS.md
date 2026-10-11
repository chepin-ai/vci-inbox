# R26FIX-GRID EXT05 四格结果汇总（WS-15 / B段）

执行：PIVOT-01 工程线沙箱（2 核 / 4GB）；日期 2026-10-11。
编译对象：`library/cgice/Spacetime_Formal_Proof_V20_R26FIX.lean`（manifest v1.1.1 锚定）。
**artifact_hash 验算一致**：取件自 vci-inbox/library/cgice，sha256 实测 = `790283cd718052881559a58195e7c3ba96a33ab5ce8bba9b58b20673d1e695b9`，与 manifest 钉定逐字符一致（fail-closed 通过）。

## 八字段表

| 格 | rev_hash | run_mode | toolchain_version | env_hash | build_exit_code | artifact_hash(fp16) | verdict | paired_run_id |
|---|---|---|---|---|---|---|---|---|
| G2 | 2f3d8f63…24ceb | cold | leanprover/lean4:v4.35.0-rc2 | 0c1f991e16a26383… | 0 | 790283cd…95b9 | PASS | R26FIX-GRID-G2-EXT05-20261011 |
| G3 | 815bbf13…f14a | cold | leanprover/lean4:v4.35.0-rc2 | 2a7884121d11fae3… | 0 | 790283cd…95b9 | PASS | R26FIX-GRID-G3-EXT05-20261011 |
| G5 | 815bbf13…f14a | hot | leanprover/lean4:v4.35.0-rc2 | 2a7884121d11fae3… | 0 | 790283cd…95b9 | PASS | R26FIX-GRID-G5-EXT05-20261011 |
| G6 | 9fe29c4b…c8b3 | hot | leanprover/lean4:v4.35.0-rc2 | d292d372b598c511… | — | 790283cd…95b9 | COLD_FALLTHROUGH_BLOCKED | R26FIX-GRID-G6-EXT05-20261011 |

完整八字段 JSON：vci-qtlv/outbox/R26FIX-GRID-G2/G3/G5/G6-RESULT.json。
env_hash 构造：sha256("leanprover/lean4:v4.35.0-rc2@11acb17ec6b07a8f9e9173e6845197929540936|mathlib4:<rev>|lake-manifest-sha256:<各格工程 manifest sha256>")，全量值见各 JSON。

## 备注
- compile_wall：G2=144s，G3=155s，G5(hot)=146s（本沙箱 `lake env lean` 独立调用为全量重编译，hot/cold 墙时近似；三格 rc=0）。
- 三个 mathlib pin 均实证为 v4.35.0-rc2 时代 commit（各 rev 的 lean-toolchain 文件逐一核对 = leanprover/lean4:v4.35.0-rc2）。
- **G6 fallthrough 说明**：mathlib@9fe29c4b 官方 cache 缺 4157/8936（4779 可得、4157 个 ltar 于 cache.mathlib.org 404，与 manifest 预言「0/4157」互证）；mathlib 源码构建在本沙箱（2c/4G）不可行。按 manifest fallthrough_rule：格保持 hot 标 + cold-fallthrough 备注，裁决按 cold 等价计，未执行编译。本体价值（实证该 pin 无完整 cache）达成。
- 本沙箱 egress 对 cache.mathlib.org 限流约 11KB/s：G2/G3 两 rev 的 8936/8655 个 ltar 经一次性中继仓 chepin-ai/vci-cache-relay（Actions 拉取 → Release → 代理回拉 + 离线解包）取得；建议善后删除该中继仓。
- **leancert 结构性发现**（A段副产品；详见 artifacts/CERT-CIRC-LEAN-01/README.md rev 段与 lean-build-report.md）：leancert 的 checkADSupported 自功能引入提交起不含 Expr.log，CERT-CIRC 证书族在其钉定依赖下结构性不可验证；drift-repair 后阐释层已全绿，残余阻塞为 checker 语义层面。
