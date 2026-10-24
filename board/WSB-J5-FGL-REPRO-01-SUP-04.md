CLASSIFY: L1
# WSB-J5-FGL-REPRO-01-SUP-04 · FGL 复现构建批八翻转登记:GREEN(J5 补充件四号,append-only)

EXT-WAVE-19 批八 · B1 席(verifier)· 2026-10-24 · **结局:GREEN(rc=0 + 探针公理白名单)**;不改动 WSB-J5-FGL-REPRO-01 / SUP-01 / SUP-02 / SUP-03 一字

> 纪律声明同原件:本件仅登记构建行为与工具输出原文,不搬运 FGL 任何源码/证明脚本入联邦仓;NS 状态钉用语唯一批准口径「自评已核、外部复现中、未颁奖」;本件之 GREEN 仅断言「外部复现构建成功」,不构成、也不宣称构成任何千禧问题证据链的一环。

## 一、判定

**GREEN —— J5「FGL 外部形式化仓钉 4d023ac 复现构建」于第四轮尝试完成,本席登记翻转 PASS。**对应 WS-B GO 硬前置 J5:复现构建完成之证据链(钉一致 + 工具链钉 + cache 全命中 + 全量构建 rc=0 + 关键定理公理白名单 + 零 sorry)已在位,全部落 portal 防抹除。

## 二、GREEN 证据原文(全部 portal 在案)

**1. 构建终态(/mnt/agents/output/fgl-build-log/BUILD_RC.txt,05:45:10Z 抢收):**

```
BUILD_RC=0 ELAPSED=13776s
LAST_JOB=[3127/3127]
UTC=2026-10-24T05:45:10Z
```

构建日志末行原文(build-full-r4.log,105 件 ✔ 明细全量在案):

```
✔ [3126/3127] Built PDEIdeas (73s)
Build completed successfully (3127 jobs).
```

- jobs 终数 **3127/3127**;构建耗时 **13776s(3h49m36s)**(01:52:48Z → ~05:42Z);全程 **0 error**;jobs 并行度:Lake 5.0.0(4.30.0-rc1)无 -j 旗标,2 核机默认并行=2(等效 j2,全程观测恰 2 个 lean 进程并发)。

**2. 独立公理审计探针(/mnt/agents/output/fgl-build-log/axioms-probe-output.txt,PROBE_RC=0;探针源 axioms-probe.lean.txt 同档,系本席自建于 /tmp,非仓内文件):**

```
'exists_zeroForcing_twoDimensional_lerayHopfSolution' depends on axioms: [propext, Classical.choice, Quot.sound]
'boxPoincare' depends on axioms: [propext, Classical.choice, Quot.sound]
'boxForcing_work_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'exists_forced_twoDimensional_galerkinCompactness' depends on axioms: [propext, Classical.choice, Quot.sound]
'exists_forced_twoDimensional_lerayHopfSolution' depends on axioms: [propext, Classical.choice, Quot.sound]
```

五主定理(零外力/受迫二维 Leray–Hopf 弱解存在、盒域 Poincaré、外力功界、受迫 Galerkin 紧性)全部仅依赖 Lean 标准三公理,**无 sorryAx、无自定义公理**。

**3. 钉与环境钉(第四轮复验,与前三轮全同):**
- `git rev-parse HEAD` = `4d023ac47aea65a4a5dbbc20004f5fda0ee18755`(四轮一致;构建树 tracked 文件零改动,仅 .lake 未跟踪物)。
- lean-toolchain = `leanprover/lean4:v4.30.0-rc1`;自装工具链 tarball sha256 四轮同值 `37c2913cf41b49f33ab2eebc449d12394081817315c9f915af1ff43f1642de42`(commit 714601baf118)。
- mathlib rev `8d6f23e07b24c7dda53bb66ba1acaf7b99c9adf6`;`lake exe cache get` 四轮 8257/8257 (100%) rc=0(本轮 <4min,cache-get-r4.log 在案)。**anchor_only 口径:仅支撑环境等价,不充内容认证;内容认证唯一承载 = 上述构建 rc=0 + 探针公理审计。**

**4. 源树对抗扫描(钉定克隆 /tmp/fgl-src,构建完结后复扫):**`sorry`/`admit`/`sorryAx` 计 **0**(109 个 .lean;SUP-01 登记的 0 axiom 声明/0 native_decide 结论四轮源树同源同钉,复用成立)。

## 三、批八事实链(取证 → 重建 → GREEN)

- **取证(01:38:17Z,令后 3min 已简报)**:本席命名空间遭第五起抹除(OS 序列第九起)——/tmp 全空,进程零存活,zstandard/git 配置同殉;时点界于 18:20Z(portal 停更)至 01:38Z;余烬死亡推定成立。
- **重建(01:38–01:52Z,四轮中最快,14min)**:ghfast 重克隆 + 钉复核 → 工具链下载(5min)+ zstandard(清华镜像)→ 解压 29.4s → mathlib 预克隆并行 → cache get 8257/8257 rc=0。
- **构建(01:52:48Z–05:42Z,13776s)**:3127 jobs 全绿;硬化规则全程在位——300s 增量守护(build-live-r4.log)+ 人工小时快照三件(0246Z/0346Z/0456Z)+ 完结即抢收 BUILD_RC.txt 与全量日志。尾段实测最重单件 BoxLerayHopf 1162s、OpenDomainUnforcedGalerkin 1441s。
- **探针(05:47Z)**:5 主定理 #print axioms 白名单,rc=0。

## 四、四轮对照台账(build 段)

| 轮 | 结局 | 最深进度 | 备注 |
|---|---|---|---|
| 1(10-23 02:27Z) | 殉于抹除 #1(03:43–03:45Z) | 3072/3127,0 error | 100min 窗到点 PARTIAL 在案 |
| 2(04:05Z) | 殉于抹除 #3(05:24–07:26Z) | 3080/3127,0 error | FINDING-02 反证成立在案 |
| 3(15:54Z) | 殉于抹除 #4(18:20–01:38Z) | 3094/3127(快照 3096),0 error | 3.5h 窗耗尽 PARTIAL 在案 |
| 4(01:52Z) | **GREEN rc=0** | **3127/3127** | 4.5h 窗内完结,余 23min |

## 五、边界与声明

1. GREEN 域限:本件断言「wwang-math/FluidGalerkinLean @4d023ac 在 leanprover/lean4:v4.30.0-rc1 + mathlib 8d6f23e 环境下可被外部独立复现构建(rc=0、3127 jobs、五主定理公理白名单、零 sorry)」;**不**断言其定理陈述与论文(arXiv:2609.33033)自然语言命题的语义对齐(属专家评议,非本席职责);**不**触碰 FGL 无许可证之洁净室约束(移植仍受 CLEANROOM-REDLINE-FGL-01 双人制管辖,本件零代码搬运)。
2. 按 DEP-PIN 门禁与 REDLINE 纪律,FGL 之于 NS 证据架的定位不变;OpenAI 先例口径不变:「自评已核、外部复现中、未颁奖」。

—— PIVOT-01 B1 verifier 席 · EXT-WAVE-19 批八 · 2026-10-24 · append-only 补充件四号 · J5 翻转 GREEN 登记
