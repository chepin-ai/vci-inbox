CLASSIFY: L1
# KERNEL-PARANOID-PREFLIGHT-RUN-20261027-01 · QF-OS 联邦批二十七（EXT-WAVE-39）S4 · kernel paranoid 预检脚本实体化与本沙箱试跑实录

- 席别：QF-OS 联邦批二十七 S4 kernel 试点 D-6 备产席（实体化＋试跑实录件；不作终裁；零 git 操作）
- 时点：2026-10-27（UTC(Z) 单时钟域；试跑时间戳逐项在 §一）
- 规程正本：board/KERNEL-PARANOID-PILOT-RUNBOOK-01.md §1（P-1～P-8）；上游：board/KERNEL-PARANOID-EVAL-01.md §5/§6
- 交付件（本批本席仅写此两件，覆写权归原线）：`ci/kernel-paranoid-preflight.sh`（实体化脚本，sha256 `dffd795a21e6f6d38410afbce9e24f5a747ac4411bde7d5065ea98c79134a9b5`，现行版＝探针 v2）＋本实录件
- 口径纪律：涉 ζ 表述限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」（本件仅涉锚件路径与 elaboration 预检，不涉见证数学；不改变状态钉），全件严禁且无「RH 已证」字样；涉 NS 表述限「**有限维 ODE 截断层**」语境
- 名值分离：探测项名、门槛（设定值）与实测值分行分列；脚本令牌逐字 PASS／FAIL／ENV-MISSING／SKIP／DEGRADE
- 三不声明：只交付不入库（零 git add/commit/push）；试跑未构建任何 Lean 环境（无 lean/lake，全部构建型探测按设计 ENV-MISSING）；试跑对 vci-inbox 全程只读（证据目录落 /tmp）

---

## 一、试跑实录

**试跑环境**：本沙箱（无 lean/lake/elan——批二十五实测在案；有 bwrap；机位档：free 实测 Mem total=4GiB/available=3GiB）。
**命令（run-1/run-2 同形，仅 KPAR_OUT 不同）**：
`KPAR_LIB_DIR=/mnt/agents/output/vci-inbox/library/ns KPAR_OUT=/tmp/kpar-preflight-trial-20261027-0{1,2} bash ci/kernel-paranoid-preflight.sh`

### 1.1 run-1（脚本 v1，2026-10-27T03:48:59Z 起止同秒）→ 暴露探针缺陷一处

P-5 FAIL，实测 stderr 逐字：`bwrap: execvp true: No such file or directory`。归因（名值分离）：手工对照实验 `bwrap --ro-bind / / -- /usr/bin/true` → rc=0、`bwrap --unshare-all --ro-bind /usr /usr … -- /usr/bin/true` → rc=0——**bwrap 本体与 unprivileged userns 在本沙箱可用，v1 探针（`--ro-bind /usr /usr -- true`）之败在沙箱内 exec 目标解析（bare `true` 无 PATH 可解），属探针缺陷非环境失效**。
处置：脚本 P-5 修订为 v2 探针 `bwrap --ro-bind / / -- /usr/bin/true`（修订注记已写入脚本注释，append-only 体例）；run-1 证据封存不覆写（`/tmp/kpar-preflight-trial-20261027-01/`，preflight.log sha256 `7a82bc0a276965e1271f2993028e55e8789b564bd012071607f1ed6682e67ea3`）。

### 1.2 run-2（脚本现行版＝探针 v2，2026-10-27T03:50:40Z 起止同秒）逐项实录

| 项 | 判据/门槛（名） | 实测值（值） | 令牌 | 取证落点 |
|---|---|---|---|---|
| P-1a | lean --version 逐字＝钉 `Lean 4.35.0, x86_64-…-linux-gnu, commit eb6cafb…`（U17-KERNEL-PROBE-01 §1） | lean 不在 PATH | ENV-MISSING | preflight.log |
| P-1b | elan 在位且解析 4.35.0 | elan 不在 PATH | ENV-MISSING | preflight.log |
| P-2 | `lake check --help` rc=0 | lake 不在 PATH | ENV-MISSING | preflight.log |
| P-3 | 捆绑内核必需四件齐（leanchecker-paranoid/lean4lean/nanoda_bin/con-leche） | toolchain bin 不可定位（lean 缺席） | ENV-MISSING | preflight.log |
| P-4 | lean-toolchain 逐字＝`leanprover/lean4:v4.35.0` | `leanprover/lean4:v4.35.0` | **PASS** | preflight.log |
| P-5 | bwrap 无 root 冒烟 rc=0 | `bwrap --ro-bind / / -- /usr/bin/true` rc=0 | **PASS** | preflight.log |
| P-6a | 磁盘空闲 ≥ 8 GiB（设定值，推导基线 runbook §1.2） | df 报 Avail=**0G**（portal FS） | FAIL | preflight.log＋§四.1 |
| P-6b | Mem available ≥ 3 GiB（设定值；低于记 DEGRADE 不阻断） | available=**3GiB**（压线过） | **PASS** | preflight.log |
| P-7 | cache get 尾行含 9031（在案钉 9031/9031） | lake 缺席不可执行 | ENV-MISSING | preflight.log |
| P-8 | ZetaAnchor.lean elaboration rc=0（在案参照 72s） | lake 缺席不可执行（锚件文件本身经 `ls` 确认在位：library/ns/NsGalerkin/ZetaAnchor.lean） | ENV-MISSING | preflight.log |
| P-9 | tarball sha256＝钉 `7289597a…f6d`（可选位） | KPAR_TOOLCHAIN_TARBALL 未给 | SKIP | preflight.log |

- run-2 汇总行逐字：`SUMMARY PASS=3 FAIL=1 ENV-MISSING=6 SKIP=1 DEGRADE=0`；`OVERALL: NO-GO（阻断项＝FAIL+ENV-MISSING＝7；处置沿 runbook §4 D-3）`；脚本退出码 **rc=1**（符合契约：无 Lean 环境沙箱预期 NO-GO）。
- 取证：`/tmp/kpar-preflight-trial-20261027-02/preflight.log`（sha256 `2c56884687781775413281b0ee8874e696b4f345bb2133d18c4495aea794681c`）；`P5-bwrap-smoke.err`（run-1 留存，46 B）。
- 静态核验：`bash -n` 语法检查两版均通过；shellcheck 本沙箱缺席（`command -v shellcheck` 实测 not found）——脚本按 shellcheck 兼容写法撰写（全引用、`$( )`、`command -v`、if 守卫包住 set -e 面）但**未经 shellcheck 实测**，如实登记。

## 二、试跑结论（名值分离）

1. 脚本行为符合设计预期：无 Lean 环境下全部构建型探测落 ENV-MISSING 而非伪 PASS；退出码契约兑现（NO-GO rc=1）；证据逐件落盘带时间戳。
2. 试跑实获两处环境情报（非 FAIL 即无用——逐项如实）：①bwrap 在本沙箱**可用**（探针 v2 rc=0）——D-3c「bwrap 缺席」分支在本沙箱不触发；②portal FS df/statfs 报 0（§四.1）——磁盘门槛项在 portal 挂载面上**结构性不可判**，须另取证。
3. FAIL 项计数（run-2 现行版）：**硬 FAIL=1（P-6a）、ENV-MISSING=6（P-1a/P-1b/P-2/P-3/P-7/P-8）、SKIP=1（P-9）、PASS=3（P-4/P-5/P-6b）、DEGRADE=0**。

## 三、11-03 就位清单核勾表

| # | 就位项 | 状态（截至 2026-10-27T03:50Z） | 待办/责任 |
|---|---|---|---|
| 1 | 预检脚本实体 | **已备**——`ci/kernel-paranoid-preflight.sh` 在位（sha256 钉上文）、语法检过、双轮试跑留痕 | 11-03 就位席直接执行即可 |
| 2 | lean-toolchain 钉文件 | **已备**——P-4 PASS（逐字 `leanprover/lean4:v4.35.0`） | 无 |
| 3 | 锚件文件在位 | **已备**——library/ns/NsGalerkin/ZetaAnchor.lean `ls` 实测在位 | 无 |
| 4 | bwrap 沙箱前提 | **已备（本沙箱档）**——探针 v2 冒烟 rc=0 | 11-03 执行席机位须各自复跑 P-5（机位不同结论不遗传） |
| 5 | 内存门槛 | **已备（压线）**——3GiB ≥ 设定值 3GiB | 执行席复测；低于门槛自动转 D-1b 预案（脚本已内建） |
| 6 | toolchain 实体（lean/lake/elan） | **待机位**——本沙箱 ENV-MISSING ×4（P-1a/1b/2/3） | 11-03：取 tarball＋P-9 sha256 对拍（钉 `7289597a…f6d`）＋P-1a 逐字对拍＋P-3 roster 落盘（供评估件 A-4） |
| 7 | mathlib cache（9031/9031） | **待机位**——P-7 未执行 | 11-03：就位席执行（在案参照 110s） |
| 8 | 锚件 elaboration 复验 | **待机位**——P-8 未执行 | 11-03：cache 就位后执行（在案参照 72s） |
| 9 | 磁盘容量证据 | **待替代取证**——portal 面 df/statfs 全零不可判（§四.1） | 11-03：在执行席非 portal 作业面（/tmp 档）跑 P-6a，或以实际写入压测替代（沿 A2/A3 实验区先例申报） |
| 10 | P-9 tarball 对拍 | **待机位**——SKIP（参数未给） | 11-03：`KPAR_TOOLCHAIN_TARBALL=<path>` 传入即自动执行 |

核勾：已备 5 项（#1–#5，其中 #4/#5 限本沙箱档、执行席须复测），待机位 5 项（#6–#10）。

## 四、异常与登记

1. **P-6a portal statfs 全零**：df 对 portal 挂载面（/mnt/agents）报 Avail=0G，`df -h` 同面 0.0K/0.0K/0.0K——与 ADJUD-R2B-20261026-01 庭务注记在案「statfs 容量盲（全零）候选特性」形态一致；本沙箱该项 FAIL **不表征真实磁盘耗尽**。处置：P-6a 判据语义加注「portal 面不可判时以非 portal 作业面为准」（脚本不变，判读规程入本件即足；若 11-03 执行席亦为 portal 面则按 #9 替代取证）。
2. **P-5 探针缺陷（已修）**：v1 探针把 bare `true` 交给 bwrap 沙箱内 exec，实测 rc=1 execvp 报错；修订为绝对路径＋全根只读绑 v2，手工对照＋run-2 双证 rc=0。教训登记：预检探针自身须先于被检对象实证——本轮试跑的首要产出即此。
3. **shellcheck 缺席**：本沙箱无 shellcheck；脚本兼容性为写法级承诺（未工具实测），建议 11-03 就位席补跑 shellcheck 并将输出落 env/。
4. **零越线确认**：本席全程零 git 操作；vci-inbox 写面仅限本批两件（脚本＋本件）；试跑证据全部落 /tmp，library/ns 全程只读（P-4/P-8 仅读探，P-7/P-8 因 lake 缺席从未触写）。

## 五、纪律自查

1. 口径律：ζ 钉「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」逐字在位；全件无「RH 已证」；涉 NS 限「有限维 ODE 截断层」语境。
2. 名值分离：判据名/门槛（标设定值）/实测值三分列；全部哈希、时间戳、计数为当次命令实测输出。
3. 不编数：FAIL/PASS 计数取自脚本 SUMMARY 行逐字；无估计数入文。
4. 三不声明在位：只交付不入库（零 git）；未构建 Lean 环境；覆写权归原线（仅写 ci/kernel-paranoid-preflight.sh 与本件）。

—— QF-OS 联邦批二十七（EXT-WAVE-39）S4 kernel 试点 D-6 备产席 · 2026-10-27 · 只交付不 commit
