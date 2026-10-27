CLASSIFY: L1
# KERNEL-PARANOID-D6-PREP-20261027-01 · QF-OS 联邦批二十八（EXT-WAVE-40）S6 · kernel 试点 D-6 续备：11-03 就位执行令＋REPORT 骨架预填＋P-9 供给选项树＋v2 试跑实录

- 席别：QF-OS 联邦批二十八 S6 kernel 试点 D-6 续备席（备产件；不作终裁；零 git 操作）
- 时点：2026-10-27（UTC(Z) 单时钟域；试跑时间戳逐项在 §四）
- 上游：board/KERNEL-PARANOID-PILOT-RUNBOOK-01.md（§1/§4/§6）；board/KERNEL-PARANOID-PREFLIGHT-RUN-20261027-01.md（批二十七试跑实录与 11-03 核勾表）；board/KERNEL-PARANOID-EVAL-01.md §5/§6
- 本批交付（覆写权归原线——本席仅新增两件，v1 脚本与一切既有件一字未动）：`ci/kernel-paranoid-preflight-v2.sh`（新件，sha256 `19b1bd66e1d32d6cecec77a8aab8a7ea263138b1c01ba7f5f5f611c6bcced184`；v1 在位核验 sha256 `dffd795a21e6f6d38410afbce9e24f5a747ac4411bde7d5065ea98c79134a9b5` 与批二十七实录钉一致）＋本件
- 口径纪律：涉 ζ 表述限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」，全件严禁且无「RH 已证」字样；涉 NS 表述限「**有限维 ODE 截断层**」语境
- 名值分离：钉值/设定值/实测值三分列；REPORT 骨架中方括号为名、值待实测；一切通道选项不预填结果
- 三不声明：只交付不入库（零 git）；不实际下载 toolchain 大件（§三 仅给选项树）；v2 试跑未构建 Lean 环境，写面限 /tmp 档探针目录（已全数清理，零残留实测在案 §四.4）

---

## 一、11-03 就位执行令（机位申请要件／就位序步／回退点）

### 1.1 机位申请要件清单（名值分离：要件名＝钉值/出处）

| # | 要件 | 钉值/规格 | 出处/基线 |
|---|---|---|---|
| M-1 | 机位档 | 2 核 / 4GB / 无 root 可（在案同档先例） | U17-KERNEL-PROBE-01 §1；OBL-NS-02-TENET-RERUN-02 §一 |
| M-2 | OS/架构 | Linux x86_64（官方沙箱 Linux-only） | lean-lang.org 手册 25.1.5.8（评估件 §1.3 在案转录） |
| M-3 | bubblewrap＋unprivileged userns 可用 | bwrap 冒烟 rc=0（v2 探针形：`bwrap --ro-bind / / -- /usr/bin/true`） | 本件 §四 run-v2 实测；批二十七探针修订在案 |
| M-4 | 非 portal 作业面 | /tmp 档本地盘，空闲 ≥ 8 GiB（设定值，推导基线 runbook §1.2） | **portal 面 statfs 全零不可判**（批二十七实测＋ADJUD-R2B 庭务注记「statfs 容量盲」候选特性同型）——容量证据只取非 portal 面 |
| M-5 | 网络通道 | toolchain tarball 通道 ≥1 条（选项树见 §三）＋ mathlib cache 端点可达（在案先例 9031/9031/110s） | U17-KERNEL-PROBE-01 §1；OBL-NS-02-TENET-RERUN-02 §一（ghfast/gh-proxy 镜像竞速先例） |
| M-6 | 内存 | cgroup 上限 ≥ 3 GiB（设定值；以 cgroup 读数为准，名义档不作数——本沙箱实测名义 4GiB vs cgroup v1 限 3,221,225,472B，名值分列先例在 §四.3） | v2 脚本 P-6b/P-6c |
| M-7 | 时间窗 | 11-03 当日；避让 11-04 S2 执行日算力（ADJUD-R2B 案 E 随裁纪律） | runbook §六 |

### 1.2 就位序步（S1→S9；每步取证落点随步标注）

1. **S1 取证目录**：`KPAR_OUT=/tmp/kpar-preflight-<UTCts>` 建目；本步起一切输出落盘（原始字节律）。
2. **S2 v2 预检首跑**：`KPAR_LIB_DIR=<library/ns 路径> bash ci/kernel-paranoid-preflight-v2.sh`——预期本阶段 P-1a/1b/2/3/7/8 ENV-MISSING、P-4 PASS、P-5/P-6a/P-6b/P-6c 实出机位读数；基线登记用，NO-GO 为预期态。
3. **S3 tarball 取件**：按 §三 选项树取 lean-4.35.0-linux.tar.zst（钉：594,481,375 B）；落 /tmp 档。
4. **S4 P-9 对拍**：`KPAR_TOOLCHAIN_TARBALL=<path>` 复跑 v2（或单独 sha256sum）——sha256 逐字＝`7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d` 方续。
5. **S5 toolchain 解布**：流式解压 /tmp（在案参照 ~22s，U17-KERNEL-PROBE-01 §1）；PATH 挂接。
6. **S6 工具链面复跑**：v2 复跑——P-1a 逐字钉、P-1b（若有 elan）、P-2 `lake check --help`、P-3 roster 落盘（**P3-preflight-roster.txt 为评估件 A-4 con-ron 裁决的一手料**）。
7. **S7 cache 就位**：P-7 执行（在案参照 110s；尾行须含 9031）。
8. **S8 锚件复验**：P-8 elaboration（在案参照 72s，RC=0 零诊断）。
9. **S9 转主流程**：全项 GO 后转 runbook §2 导出生成（A-1 双导）——本令止于此，主流程窗 11-04/05 照 runbook §六。

### 1.3 回退点（逐点对应 runbook §4 D-3）

| 回退点 | 触发 | 处置 |
|---|---|---|
| R1 | S2 中 P-5 FAIL（bwrap 不可用） | D-3c 两轨：自备隔离降级标注 or 呈裁改窗；禁裸跑 |
| R2 | S4 P-9 sha256 不符 | 停——登记钉漂移事件，禁以不符件续布 |
| R3 | S7 cache 断供/缺项 | 重试一次留 log；仍败→登记断供事件（B1-INFRA §3.2/3.3 风险在案），顺延不挤硬钉 |
| R4 | S2 中 P-6a 替代支探针写失败 | 机位不可用——退回 M-1 申请，换机位重报 |
| R5 | 11-03 当日 S9 未达 | FSL 结转（沿既有体例），禁以挂账时长作撤项论据；主流程窗顺移不抢 11-04 S2 |

---

## 二、REPORT.md 骨架预填（名值分离：方括号为名；已钉值预填，未实测留〔待实测〕）

```markdown
CLASSIFY: L1
# KPAR-PILOT-01-REPORT · ζ 四锚闭包 kernel paranoid 试点评估报告（有限高度 T=100/1000 截断语境）
0. 状态钉（逐字）：区间见证层 PASS、kernel 层未证、非 RH 证据；Tenet 钉：自评已核、外部复现中、未颁奖。本报告不改变两钉。
1. run 指纹：
   - [run_id]＝〔待实测：kpar-pilot-01-<UTCts>〕
   - [lean --version]＝预期钉 Lean 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release（实测〔待实测〕，逐字对拍）
   - [toolchain tarball sha256]＝预期钉 7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d（实测〔待实测〕）
   - [bwrap 形态]＝〔待实测：沙箱 | 自备隔离降级〕（预检 P-5 冒烟预期 rc=0；探针形 bwrap --ro-bind / / -- /usr/bin/true）
   - [磁盘证据形态]＝〔待实测：直接支 df 读数 | 替代支写删探针〕（portal 面 statfs 盲在案，替代支语义限可写性）
   - [机位档]＝〔待实测：核数/内存/cgroup 上限，名值分列〕
2. 判据总表：
   - A-1 [PASS/FAIL]：run1 sha256＝〔待实测〕，run2 sha256＝〔待实测〕，全等性＝〔待实测〕
   - A-2 [exit=〔待实测〕]（契约：0＝全内核 accept 且仅标准公理；禁日志 grep 代出口码）
   - A-3 [采用形态：闭包 | 全包退路]＝〔待实测〕
   - A-4 [paranoid 实跑名单逐字]＝〔待实测：P3-preflight-roster.txt + 主跑日志析出〕；con-ron [在/不在]＝〔待实测〕
   - A-5 [tamper-01 exit=〔待实测〕 / tamper-02 exit=〔待实测〕]（PASS 判据：双件均非零）
   - A-6 [公理集逐字]＝预期钉 [propext, Classical.choice, Quot.sound]（U17-KERNEL-PROBE-01 §3 在案；实测〔待实测〕）
   - A-7 [wall / max RSS]＝〔待实测〕（登记型，不设阈值）
3. A-4 结论句：con-ron〔待实测〕paranoid 实跑集——评估件 §1.1 文档级微差（Highlights 段 vs #15145 行）裁决为〔待实测〕。
4. 降级/异常：〔待实测：无 / D-x 事件行逐字〕（预案：D-1 单内核／D-2 全失败／D-3 环境不就位，runbook §4）
5. R2B-09 销记评估：义务面（≥1 第二通道）〔待实测：满足/不满足，载通道名清单〕；与 A-2 PASS 与否分行陈述，不混格。
6. 建议（供判定席，非裁）：〔待实测：转正 / 降级复跑 / 转 Tenet 二试点首验 R-3〕
7. 附：manifest.sha256 首行＝〔待实测〕；全件计数＝〔待实测〕；日志路径清单＝〔待实测〕。
```

预填说明：凡「预期钉」均为在案值预填作**对拍基准**，不构成实测值；实测列一律〔待实测〕，禁预填。

---

## 三、P-9 tarball 供给方案（通道选项树；本批不实际下载大件）

目标件（名值分离双钉）：lean-4.35.0-linux.tar.zst，字节数 **594,481,375 B**，sha256 **`7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d`**（U17-KERNEL-PROBE-01 §1 在案）。一切通道的验收闸相同：**字节数＋sha256 双钉逐字对拍**（v2 脚本 P-9 自动执行），不过闸即下一通道，全灭 → R2（钉漂移登记）。

- **通道 A｜官方发布直取**：lean-lang.org / github.com/leanprover/lean4 releases v4.35.0 资产。先例：U17-KERNEL-PROBE-01 §1（任务书 tarball 对拍成功）。风险：直连速率未实测（在案无速率钉）。
- **通道 B｜镜像竞速**：ghfast → 降速则 gh-proxy 镜像竞速。先例：OBL-NS-02-TENET-RERUN-02 §一（toolchain tarball 580MB 档经「ghfast 降速后改 gh-proxy 镜像竞速」就位，字节数与钉一致）。名值注：镜像只改通道不改验收——双钉对拍不变。
- **通道 C｜联邦归档线冷备**：B1-INFRA-20261025-01 §3.3 曾建议「对现行钉的 cache 集做 portal 外一次性归档」——**该归档是否已含 toolchain tarball 无在案实证**，用前须先核归档清单；若在则内网取件（速率预期优于外网，无实测钉不编数）。
- **通道 D｜他席已就位 toolchain 传递**：执行席/前序席位已有解布目录者，拷贝或挂载——**不信任传递**：tarball 或解布树均须重算 sha256/抽文件对拍后方用（名值分离：传递只是搬运，验收闸不变）。
- 选项树判序：A 直取速率可忍则 A；A 降速 → B；A/B 全灭 → C（先核在位）→ D；全灭 → R2。
- 纪律：本批不执行任何下载；11-03 就位席执行时下载件落 /tmp 档非 portal 作业面（M-4），portal 归档动作权属归档线原线。

---

## 四、v2 脚本本沙箱试跑实录（如实：磁盘替代支行为）

### 4.1 试跑元数据（名值分列）

- 脚本：`ci/kernel-paranoid-preflight-v2.sh`（sha256 `19b1bd66e1d32d6cecec77a8aab8a7ea263138b1c01ba7f5f5f611c6bcced184`；`bash -n` 语法检查通过；shellcheck 本沙箱缺席——写法级兼容承诺，未工具实测，同批二十七登记）
- 命令：`KPAR_LIB_DIR=/mnt/agents/output/vci-inbox/library/ns KPAR_OUT=/tmp/kpar-preflight-v2-trial-20261027-01 bash <v2>`；起止 2026-10-27T06:56:43Z→06:56:44Z；脚本退出码 **rc=1**
- 汇总行逐字：`SUMMARY PASS=5 FAIL=0 ENV-MISSING=6 SKIP=1 DEGRADE=0`；`OVERALL: NO-GO（阻断项＝FAIL+ENV-MISSING＝6）`（6 项 ENV-MISSING 全为 Lean 工具链缺席预期态：P-1a/P-1b/P-2/P-3/P-7/P-8）
- 取证哈希：preflight.log `f71ee88cdbdc508180f110e5500a6254ca3b84d81e57e3864b170d2bce83cc1f`；P6a-alt-probes.txt `005a07ebc40c78163a9b6ead916f6f3a86da1a3eb7fb43d1b75d423421dd859f`；P6c-mem-cross.txt `c5069f094fdc7794b4af752e0e8fb76ae2741d03e2f7d22f19a1f3030b644c8a`

### 4.2 P-6a 替代支行为实录（本批核心验证对象）

- 触发链逐字（log 原文）：`# P-6a 替代支触发：df 空闲=0GiB 且 stat -f 全零（type=fuseblk）→ 写删探针实测（目录集：/tmp/kpar-preflight-v2-trial-20261027-01 /tmp）`
- 盲检三元组实测：df Avail=**0G**；stat -f → blocks=**0** free=**0** type=**fuseblk**（portal 面；对照 /tmp 面 overlayfs blocks=7696612 free=5881867——非盲面直读正常，名值分列）
- 写删探针实测（P6a-alt-probes.txt 逐字值）：目录①写入 67,108,864 B（64 MiB）0.2187s/307MB/s，sha256 `5a65384269924daf22544dc2921a696db0af2d58c4321361857afeeea58cbc2d`，rm rc=0；目录②同体量 0.2177s/308MB/s，sha256 `863c7c7a151fe8c9314d86c5125b120c89d14fd1f532725a7e1fd80c756a2b58`，rm rc=0
- 判出：`P-6a PASS: （替代支）statfs 盲（type=fuseblk blocks=0 free=0）；写删探针 64MiB×2 目录全过、读回 sha256 落 P6a-alt-probes.txt；**容量数值不可判如实登记——本 PASS 语义限可写性**`
- 语义边界声明（名值分离）：替代支 PASS **证「探针目录此刻可写 64MiB 且读回一致」**，不证「空闲 ≥ 8GiB」；容量充分性在 statfs 盲面上**结构性不可判**，11-03 就位席须在非 portal 作业面以直接支 df 读数补足容量证据（M-4/S6 复跑承载）。

### 4.3 P-6c 交叉读数实录（登记型）

P6c-mem-cross.txt 逐字：`MemTotal: 4194304 kB`／`MemAvailable: 3719332 kB`／`cgroup_source=v1`／`cgroup_limit_bytes=3221225472`／`cgroup_current_bytes=1462099968`。名值判读：名义档 4GiB vs cgroup v1 上限 3,221,225,472B（≈3.00GiB）——**不一致在案，以 cgroup 为准**（v2 脚本注释已载此律）；上限压设定值 3GiB 线，P-6b/P-6c 双 PASS 但裕度为零，主跑期建议 D-1b 逐内核串行预案常备。

### 4.4 写面纪律实测

探针文件全数清理：`find library -name '.kpar-probe-*'` 实测 **0** 命中、`/tmp/.kpar-probe-*` 实测 **0** 命中；portal 面零写入（探针目录默认 /tmp 档；portal 写权属原线，脚本注释已载「作业面落 portal 须先获写授权」）；v1 脚本 sha256 试跑前后一致（`dffd795a…`，一字未动）。

### 4.5 v2 试跑结论一行

**P-6a 替代支按设计触发并判出（盲检→写删探针→PASS 限可写性语义），P-6c 交叉读数落盘，汇总 PASS=5/FAIL=0/ENV-MISSING=6/SKIP=1，rc=1 符合契约预期。**

---

## 五、纪律自查

1. 口径律：ζ 双钉逐字在位（题头＋§二骨架 0 行）；全件无「RH 已证」；涉 NS 处限「有限维 ODE 截断层」语境。
2. 名值分离：钉值（594,481,375 B／7289597a…／9031）／设定值（8GiB／3GiB／64MiB，均标注）／实测值（stat -f 三元组、探针 sha256、cgroup 字节数）三分列；REPORT 骨架实测列全留〔待实测〕。
3. 不编数：全部数值为当次命令实测输出或在案钉转录；通道速率未实测处明说「无速率钉」。
4. 三不声明在位：零 git；未下载 toolchain 大件（§三 仅选项树）；未构建 Lean 环境；写面仅本批两件＋/tmp 探针（已清理）。

—— QF-OS 联邦批二十八（EXT-WAVE-40）S6 kernel 试点 D-6 续备席 · 2026-10-27 · 只交付不 commit
