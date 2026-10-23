CLASSIFY: L1
# OBL-NS-02-TENET-RERUN-01 · Tenet（openai/NavierStokesAndEuler）钉 f9e8bc5 外部复跑登记
枢/PIVOT-01 · EXT-WAVE-18 饱和批 B2 席（verifier，后台长磨） · 授权源：EXT18 卡7（R2 复裁：归因锁「对 2610.08144 所揭示失配的独立复现验证」，产物哈希归档） · 执行 2026-10-23T02:04Z 起 · 登记 2026-10-23T03:42Z

> 状态钉（唯一批准语）：**自评已核、外部复现中、未颁奖**。本件为见证与复现报告，不做「验证通过/失败」终局断言。

## 一、钉核验（A1）

| 项 | 值 | 证据 |
|---|---|---|
| 仓址 | github.com/openai/NavierStokesAndEuler（经 ghfast 前缀克隆，直连 TLS 断按预案） | clone OK |
| 钉 | `f9e8bc5` → rev-parse 实得 `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` | `git rev-parse HEAD`，归档 `OBL-NS-02-TENET-RERUN-01.pin.txt` |
| 钉 commit 日期 | 2026-09-10T09:40:53-04:00 | `git log -1` |
| 源树哈希 | 2669 文件逐一 sha256 | 归档 `OBL-NS-02-TENET-RERUN-01.src-sha256-manifest.txt` |
| 漂移 | 与 DEP-PIN-NS-01 第二节钉位一致，未见漂移 | 同制比对 |

## 二、环境钉

- 仓自指 toolchain：`leanprover/lean4:v4.34.0-rc2`（仓内 `lean-toolchain` 原文），与共享 4.35.0 不符 → 按协议自装：ghfast 前缀拉 GitHub release 资产 `lean-4.34.0-rc2-linux.tar.zst`（580,281,129 B），python3+zstandard 解包至 /tmp/lean-4.34.0-rc2-linux；tarball sha256 `3d011041203acacf300d343a39673f7d233743397993797c941346ae9e5df1a8`（归档 `…toolchain-sha256.txt`）。
- `lean --version`：Lean 4.34.0-rc2, commit 6a10ac8c22beadecabdbb0919c2b50214762f91d；Lake 5.0.0-src+6a10ac8。
- 依赖钉（lake-manifest.json @f9e8bc5）：mathlib `85e3a25e006c…`（v4.34.0-rc2）、Comparator `19e111e2141c…`、lean4export/batteries/aesop/Qq/plausible 等 11 包。
- 机器：2 核 / 4GB / 无 root；Lake 5.0 无 `-j` 选项（`lake build --help` 实证无 jobs 旗标），以默认并行度（≈2 路）构建。源树与构建全在 /tmp，未写外部仓源树。

## 三、复跑结果：**PARTIAL**（到点如实）

规程按仓 README/CI 自指入口：`lake exe cache get` → `lake build`。

1. **cache 协议：PASS**。`lake exe cache get` 自 `lakecache.blob.core.windows.net/mathlib4-master` 下载 **8747/8747** .ltar 并全部解压（归档 `…cacheget-tail.txt`），未触发失速预案。
2. **build：PARTIAL（时限截断）**。构建 2026-10-23T02:31:42Z 启动，窗口末快照 03:39:16Z（67.5 分钟）：**96/2659 仓内模块建成（3.6%），0 error、0 warning**；作业图已展开至 9580 jobs（基线 11251 jobs 同量级；Lake 计数随依赖解锁递增，终值未定型）。实测吞吐 ~1.4 模块/分（单模块 20–191s），2 核全量 ETA ≈ 30 小时，远超 ~100 分钟窗口。**构建以后台 nohup 续跑中**（/tmp/tenet-src，日志 /tmp/build.log），下窗口可收割续态。
3. **公理审计（A3）：部分坐实**。源码 0 条 axiom 声明；对已建成模块 `#print axioms` 抽查 4 件——`NavierStokes.ProblemStatement.candidateStatement` / `.smooth_at_interior` / `.zero_force_time_support` / `NavierStokesR3.ProblemStatement.breakdownStatement`——全部恰为 **[propext, Classical.choice, Quot.sound]** 标准三公理，无注入。全声明闭包待全量建成后复核。
4. **sorry 普查（A4）：PASS（可脚本化正证据）**。全仓 `sorry` 仅见于 `ComparatorChallenges/Euler.lean`（行 88、184）与 `ComparatorChallenges/NavierStokes.lean`（行 277、284），其 README 自述为「intentional `sorry` challenge placeholders」；`NavierStokes/ComparatorSolution.lean` 无 sorry——与基线「sorry 仅 Comparator Challenge 故意留洞（ComparatorSolution 不引入洞）」逐字吻合。
5. **失配符号在位核验**：2610.08144 指认件于本钉均在位——`norm_derivativeWord_inverse_le`（NavierStokes/SmoothFamilyTorusInverse.lean，涉 Lemma 8.6/式(8.19) m+4/m+5 争议）、`regularized_flux_*`（R3StressPressureEstimate.lean、R3PressureFlux.lean，涉幽灵步争议）。本席仅登记在位性，NL↔Lean 逐条对表（A7）按 EXT18 维持暂缓。

## 四、与 LAB-CLOSE-EXT15 / FUSION-EXT10 基线对拍

| # | 基线条目 | 本次实证 | 判定 |
|---|---|---|---|
| 1 | toolchain Lean 4.34.0-rc2 | `lean-toolchain`=v4.34.0-rc2，实装 4.34.0-rc2 | **一致** |
| 2 | Apache-2.0 | LICENSE=Apache-2.0；API `license.spdx_id=Apache-2.0` | **一致** |
| 3 | 2026-09-08 建仓、09-10 后无 push | API：created 2026-09-08T10:53:38Z、pushed 2026-09-10T15:14:13Z | **一致** |
| 4 | Issues/PR 均关闭 | API：`has_issues=false` | **一致** |
| 5 | sorry 仅 Comparator Challenge 故意留洞 | 4 处 sorry 全在 ComparatorChallenges 两文件，README 自述 intentional | **一致** |
| 6 | 公理闭包恰为标准三公理 | 源码 0 axiom 声明；抽查 4 decl 恰为三件 | **一致（抽样级；全量待 A2 闭环）** |
| 7 | 全量 build 基线 11251 jobs | 窗口内 96/2659 模块、作业图展开至 9580 jobs、0 error | **分歧（量级吻合、终值未达）——归因 2 核/100 分窗 vs 基线机时，非仓质性分歧** |
| 8 | 2610.08144 两处失配于 f9e8bc5 在位 | 两族符号均在位（§三.5） | **一致（在位性层面）** |

## 五、对 OBL-NS-02 闭合条件的推进声明

- **A1 钉版+漂移监控：推进**——钉复验+2669 文件 sha256+toolchain sha256 归档成册；漂移零见。
- **A3 公理审计：推进（抽样级坐实，全量悬挂）**。
- **A4 sorry 普查：达成**（脚本化、与基线逐字吻合）。
- **A2 全量 build 复现：未闭合**——缺口=机器时（2 核 ETA ≈30h）；续跑态留存 /tmp，建议下窗口以续跑收割或转更强算力；**闭环判据满足度：~3.6%（96/2659 模块、0 error）**。
- **A5 双 kernel：未启动**（nanoda/lean4export 未装，留后续窗口）。
- **A6/A7/A8：维持 EXT18 边界**（A7 暂缓、A6 语义桥联邦自写未启动、A8 超机器可委仅登记）。
- **总判**：OBL-NS-02 **未闭合**；本次复跑无反证、零漂移、轻量件 A4 达成，A2/A5 为中量件缺口。状态钉维持「自评已核、外部复现中、未颁奖」。

## 六、耗时台账（墙钟，UTC）

| 段 | 起 | 止 | 耗时 |
|---|---|---|---|
| 克隆+checkout+钉核验 | 02:04 | 02:06 | ~2 min |
| toolchain 下载（580MB@~2MB/s)+解包 | 02:06 | 02:12 | ~6 min |
| 依赖克隆（mathlib 等 11 包） | 02:13 | 02:21 | ~8 min |
| cache get（8747 .ltar） | 02:21 | 02:31 | ~10 min |
| lake build（窗口内段，96 模块） | 02:31:42 | 03:39:16（快照） | 67.5 min（续跑中） |
| 静态普查+公理抽查+对拍+成文 | 全程穿插 | — | — |

## 七、登记件

- 本件：`board/OBL-NS-02-TENET-RERUN-01.md`
- 附件：`.pin.txt` / `.src-sha256-manifest.txt` / `.toolchain-sha256.txt` / `.cacheget-tail.txt` / `.buildlog-snapshot.txt`（同目录取名前缀一致）
——枢/PIVOT-01 B2 席
