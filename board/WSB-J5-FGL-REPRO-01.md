CLASSIFY: L1
# WSB-J5-FGL-REPRO-01 · FGL 外部形式化仓钉定复现构建登记(WS-B GO 硬前置 J5)

EXT-WAVE-18 饱和批 B1 席(verifier,后台长磨)· 2026-10-23 · 执行席:PIVOT-01 B1 verifier

> 纪律声明:本件为**复现构建登记**(事实 + 原文证据 + 判定)。FGL(wwang-math/FluidGalerkinLean)无许可证,其代码受 CLEANROOM-REDLINE-FGL-01 约束;本登记不搬运其任何源码/证明脚本/文件结构入联邦仓,仅登记构建行为与工具输出原文。NS 状态钉用语唯一批准口径:**「自评已核、外部复现中、未颁奖」**;本件不构成、也不宣称构成任何千禧问题证据链的一环。源树与构建全在 /tmp;/tmp/fgl-src 钉定核验克隆保持只读洁净(git status 零改动),构建在副本 /tmp/fgl-build 进行。

## 一、环境钉

| 项 | 值 | 证据 |
|---|---|---|
| 机器 | 2 核 / 4.0GiB 内存 / 无 root | `nproc`=2;`free -h` total 4.0Gi |
| OS | Linux 5.10.134-18.0.12.lifsea8.x86_64 | `uname -a` |
| FGL 仓 | wwang-math/FluidGalerkinLean | DEP-PIN-NS-01 §二 |
| 钉定 commit | `4d023ac47aea65a4a5dbbc20004f5fda0ee18755` | 见 §二核验原文 |
| FGL lean-toolchain | `leanprover/lean4:v4.30.0-rc1`(**≠共享 4.35.0,按协议自装**) | `/tmp/fgl-src/lean-toolchain` 原文 |
| 自装工具链 | /tmp/lean-4.30.0-rc1-linux;`Lean (version 4.30.0-rc1, x86_64-unknown-linux-gnu, commit 714601baf118066cbf3f282361339c6d06665b2a, Release)`;Lake 5.0.0-src+714601b | `lean --version` / `lake --version` 输出原文 |
| 工具链 tarball | lean-4.30.0-rc1-linux.tar.zst,529531960 字节(与响应 content-length 一致),sha256 `37c2913cf41b49f33ab2eebc449d12394081817315c9f915af1ff43f1642de42` | 本机 sha256sum |
| mathlib 依赖钉 | rev `8d6f23e07b24c7dda53bb66ba1acaf7b99c9adf6`(lake-manifest.json,连同 plausible/LeanSearchClient/importGraph/ProofWidgets 等继承依赖) | manifest 原文 |
| 网络 | github.com 直连 TLS 断;git/curl 走 ghfast.top 镜像;api.github.com 直连可用 | 环境硬事实,本次复验属实 |

## 二、钉核验原文

api.github.com 直连核验(2026-10-23T02:03Z):

```
sha:      4d023ac47aea65a4a5dbbc20004f5fda0ee18755
date:     2026-09-29T04:10:03Z
message:  Add bounded-domain global Leray-Hopf formalization
```

克隆(checkout 后原文记录):

```
$ git rev-parse HEAD
4d023ac47aea65a4a5dbbc20004f5fda0ee18755
$ cat lean-toolchain
leanprover/lean4:v4.30.0-rc1
```

判定:克隆 HEAD 与 DEP-PIN-NS-01 钉**逐字符一致**;lean-toolchain 为 v4.30.0-rc1,与共享 /tmp/lean-4.35.0-linux **不一致**,已按「以 FGL 自身 lean-toolchain 为准」协议自装 4.30.0-rc1,全程未混用 4.35.0。

## 三、复现流程与耗时台账(全部 UTC,机器时钟 2026-10-23)

| 时刻 | 阶段 | 结果 |
|---|---|---|
| 02:03:26Z | 开工;api.github.com 直连核验 commit | 钉一致(§二) |
| 02:05Z | ghfast 克隆 + `git checkout 4d023ac…` + `git rev-parse HEAD` | 逐字符一致 |
| 02:09–02:13Z | 工具链 tarball 经 ghfast `curl -C -` 断点续传 | 529531960/529531960 字节 |
| 02:14Z | zstandard+tarfile 解压 19.8s;`lean --version` 核验 | 4.30.0-rc1 @714601b 就绪 |
| 02:19–02:26Z | `lake exe cache get`(mathlib4 克隆 + 缓存) | **8257/8257 (100%) 尝试全成功,rc=0**;未触发失速预案。原文:`Attempting to download 8257 file(s) from leanprover-community/mathlib4 cache` / `Downloaded: 8257 file(s) [attempted 8257/8257 = 100%, 56 KB/s], Decompressed: 8253` / `CACHE_RC=0` |
| 02:27Z | `lake build` 启动(本版 Lake 5.0.0 无 `-j` 选项——首试 `-j2` 报 `error: unknown short option '-j'` 已弃;并行度=机器核数 2,等效 j2,全程观测恰 2 个 lean 进程并发) | 进行中 |
| 03:40:39Z | **~100 分钟墙钟纪律到点快照** | 进度 `[3072/3127]`,已完成 PDEIdeas 模块 51 个,**日志零 error**;构建仍在推进(尾段重模块单件 200–373s) |

构建日志快照原文(03:40:39Z,`/tmp/build.log` 尾):

```
✔ [3068/3127] Built PDEIdeas.AbstractSpectralDynamics (203s)
✔ [3069/3127] Built PDEIdeas.CountableCompactSubsequence (203s)
✔ [3070/3127] Built PDEIdeas.QuadraticWeakFormLimit (210s)
✔ [3071/3127] Built PDEIdeas.LerayTimeTest (243s)
✔ [3072/3127] Built PDEIdeas.BoxSpectralGalerkinTower (373s)
```

## 四、对抗性预扫描(源树,构建无关)

- `grep -rnE "^\s*axiom " --include="*.lean" /tmp/fgl-src` → **0**(无自定义公理声明)。
- `grep -rnE "\bsorry\b|\badmit\b|sorryAx"` → **0**;`grep -c native_decide` → **0**。
- .lean 文件数:109(与 EXT-WAVE-15 登记口径一致)。

## 五、结果判定与 GO 前置对应

**判定:PARTIAL(时限纪律到点如实登记)。**

已证成(正证据):
1. **钉核验 PASS**:克隆 HEAD 与 DEP-PIN-NS-01 钉 `4d023ac47aea65a4a5dbbc20004f5fda0ee18755` 逐字符一致;api.github.com 独立复核同 sha、提交 message `Add bounded-domain global Leray-Hopf formalization`(2026-09-29T04:10:03Z)。
2. **工具链钉 PASS**:FGL 自身 lean-toolchain = `leanprover/lean4:v4.30.0-rc1`,与共享 4.35.0 不一致;已按协议自装 /tmp/lean-4.30.0-rc1-linux(commit 714601baf118066cbf3f282361339c6d06665b2a),全程未混用。
3. **环境等价(anchor_only)PASS**:mathlib 官方 cache 8257/8257 全命中 rc=0。
4. **对抗性源树扫描 PASS**:0 自定义 `axiom` 声明、0 `sorry`/`admit`/`sorryAx`、0 `native_decide`(109 个 .lean 文件)。
5. **构建进行中无失败**:至 03:40:39Z,3072/3127 jobs,51/109 源模块编讫,日志 0 error;全部已完成模块均内核验讫(✔)。

未证成(受阻于时限,非受阻于失败):
- `lake build` 全程 rc=0 终态未达——尾段约 55 jobs(重模块为主,单件 200–373s,2 并发)估计仍需 40–60 分钟。
- 仓内自带构建期公理审计(PaperAxiomAudit/OpenDomainGlobalAxiomAudit 之 `#guard_msgs` + `#print axioms`)尚未执行到;本席自建的独立探针 `/tmp/axioms-probe.lean`(5 主定理 `#print axioms`)亦未运行。
- 故 J5 硬前置之「复现构建完成」**尚不可登记为 PASS**;WS-B GO 不得援引本件为构建完成证据。

**与 GO 前置条件对应声明**:本件当前仅支撑「钉一致 + 环境等价 + 构建中段无失败」;按默认拒绝律,GO 前置 J5 维持**未满足**,待构建完结后补登记翻转。构建进程保留续跑(日志 /tmp/build.log,完成标记 `BUILD_RC=` 行);唤醒本席复核即可在 ~10 分钟内补完终态登记与公理审计原文。

## 六、受阻项与建议

1. **受阻项(唯一)**:100 分钟墙钟上限 vs 2 核 4GB 机器构建体量(3127 jobs,尾段重模块)。非网络、非工具链、非源树问题——每一阶段均一次通过,零重试。
2. **建议(供枢裁决)**:(a) 直接唤醒本席复核续跑结果——构建无需重启,增量接续,预计 04:20–04:40Z 自然完结;(b) 后续波次若需限时内完成全量复现,建议将时限预算提至 ~150 分钟或预置 mathlib cache/工具链预热(本次工具链下载+解压+cache 共耗 ~23 分钟,为一次性成本,后续复用 /tmp/lean-4.30.0-rc1-linux 可省);(c) `lake build` 的 jobs 语义注记:Lean 4.30.0-rc1 之 Lake 5.0.0 已移除 `-j` 旗标,并行度由核数决定,「-j1~j2」纪律在 2 核机上由默认行为自然满足,登记时如实注明。

—— PIVOT-01 B1 verifier 席 · EXT-WAVE-18 饱和批 · 2026-10-23
