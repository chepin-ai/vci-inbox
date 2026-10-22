CLASSIFY: L1
# TRUSTBOUNDARY-SPIKE-A-01 — kernel 化一期 spike 子件 A「Comparator 并轨实测」受理探测实录

- 波次/线：EXT-WAVE-18「攻」续执行批三 · WS-H 攻坚线 R4 受理席 · 枢/PIVOT-01 体系
- 受理钉：2026-11-04 前瞻探测（spike 验估报告硬钉之一，TRUSTBOUNDARY-REGISTRY-01 §4.7）
- 探测时点：2026-10-22（UTC(Z) 单时钟域；全部「可得/实测」断言均以本次实跑为据）
- 上游：`registry/TRUSTBOUNDARY-REGISTRY-01.md` §4.2/§4.6（子件 A 2–3pd 口径）§二 TB-06 行；`board/LAB-CLOSE-EXT18-20261020T2304Z.md` §一 WS-H 行
- 语纪律：全部运行结果均为本席实跑记录；受阻项一律「未定+理由」，无编造
- 探测机规格（时间测量假设之机器钉）：x86_64 Linux 5.10 / 2 核 / 4GB RAM / overlay 30G（余 21G）/ 无 root / git 2.39.5 / curl 7.88.1 / python 3.12.12

---

## 一、探测实录（每条命令 + 结果一句话）

### 1.0 通道基线

| # | 命令/动作 | 结果一句话 |
|---|---|---|
| 1 | `curl -sI https://github.com` / `https://api.github.com` / `https://raw.githubusercontent.com` | github 主域 HEAD 200、api.github.com 200 可通；raw 域 000 不通（与任务书口径一致） |
| 2 | `git config --global url."https://ghfast.top/…".insteadOf …` 后克隆 | ghfast 通道可克隆公开仓（本席三仓均经此道成功） |
| 3 | `curl -sI https://sh.rustup.rs` / `https://static.rust-lang.org/…/rustup-init` | 两站 HEAD 均 200，但 static.rust-lang.org 实际数据流停滞（见 1.2 阻塞） |
| 4 | `curl -sI https://index.crates.io/config.json` | sparse 索引 200 可通；crates.io 主站 403 不影响 sparse 协议 |

### 1.1 Lean 本体 /tmp 安装（复用三席 tarball 法，本席第四次成功）

| # | 命令/动作 | 结果一句话 |
|---|---|---|
| 5 | `curl api.github.com/repos/leanprover/lean4/releases/tags/v4.35.0` | 查得 `lean-4.35.0-linux.tar.zst` 官方大小 594,481,375 字节（完整性对照基准） |
| 6 | ghfast 下载该 tarball（首跑前台超时截断至 537,656,459 → `curl -C -` 断点续传补全） | 续传后实测 594,481,375 字节，与官方 API 口径逐字节相符 ✓ |
| 7 | 解压：本机**无 zstd 二进制**、tar 不能 `--zstd`；`pip install --user zstandard` 成功，python `ZstdDecompressor().copy_stream` 解出 tar 再 `tar -x` | 解压链通；`lean --version` 实测 `Lean (version 4.35.0, …, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)` ✓ |
| 8 | `ls /tmp/lean-4.35.0/bin` | **重大在案发现**：v4.35.0 工具链 bin 自带 `lake / lean / leanchecker / leanchecker-paranoid / lean4lean / leanexport / nanoda_bin / con-leche / con-ron` 等全套复核/导出组件——Comparator 并轨链在官方发行物内即齐套 |

### 1.2 Rust/nanoda 链

| # | 命令/动作 | 结果一句话 |
|---|---|---|
| 9 | `api.github.com/repos/digama0/nanoda` → 404；搜索定位 | nanoda 正身＝`ammkrn/nanoda`，其 README 首行自宣 **DEPRECATED**，活跃件＝`ammkrn/nanoda_lib` |
| 10 | ghfast 克隆 `ammkrn/nanoda_lib`（depth 1） | 克隆成功（Rust crate，edition 2021，无 rust-version 硬性下钉） |
| 11 | rustup 安装：`sh rustup-init.sh`（官方源）前台超时、后台 20 分钟停滞于 "downloading installer" | **阻塞点**：static.rust-lang.org 数据流在本环境实质不可用 |
| 12 | 改 `RUSTUP_DIST_SERVER=https://rsproxy.cn RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup` 重装 | rsproxy 镜像通道成功：rustc/cargo **1.99.1**（58cf8f9c3 2026-10-13）落 /tmp/rustup+/tmp/cargo ✓ |
| 13 | `cargo build --release`（nanoda_lib，2 核） | **构建成功，耗时 5m38s**，产出 `nanoda_bin` ✓（crates sparse 索引慢但通） |

### 1.3 lean4export 链

| # | 命令/动作 | 结果一句话 |
|---|---|---|
| 14 | `api.github.com …/commits?path=lean-toolchain` | lean4export HEAD 已漂移至 **v4.36.0-rc1**（df81913，2026-10-14）；与我方钉 v4.35.0 精确匹配之最近钉＝**`5a9a355dc6c5`**（2026-10-12，"bump toolchain to v4.35.0 (#56)"）——供应链漂移实例，R4 风险簿活证 |
| 15 | ghfast 克隆 + `git fetch --deepen 10` + 检出 `5a9a355dc6c5` | 检出成功，`lean-toolchain` 内容实测＝`leanprover/lean4:v4.35.0` ✓ |
| 16 | `PATH=/tmp/lean-4.35.0/bin lake build`（lean4export 仓内） | **构建绿**（6 jobs，Export:c.o 4.0s + exe 4.3s），产出 `.lake/build/bin/lean4export` ✓ |

### 1.4 最小目标端到端首跑（暖缓存基线机制之最小件实证）

最小目标工程 `/tmp/spike-min`：单文件 `SpikeMin/Basic.lean`（3 decl：`add_comm_two`/`two`/`two_eq`），`lakefile.lean` + `lean-toolchain=v4.35.0`。

| # | 命令/动作 | 结果一句话 |
|---|---|---|
| 17 | `lake build`（spike-min） | 构建绿（4 jobs），产出 SpikeMin.olean 两件 ✓ |
| 18 | 冷跑 `lake env lean4export SpikeMin > out1.ndjson` | **22.07s**，产出 345,691,022 字节 NDJSON（单文件亦全量带出 Init prelude 传递闭包——量级特征在案） |
| 19 | 暖跑同命令 > out2.ndjson；`cmp out1 out2` | **21.77s，两跑字节级完全一致**；out1 sha256＝`57d8f44db458ec8a70308ce68e43c81692135e5502fb7f5e80b01d730873dbe3`——**导出器字节确定性首证在案** |
| 20 | 自构 nanoda_lib `nanoda_bin nanoda-config.json`（permitted_axioms 白名单五常项+trustCompiler+sorryAx，hard_error=false） | **复核 59,352 decl 零类型错误，EXIT=0，59.46s** ✓（导出链→异构 kernel 直通） |
| 21 | `lake comparator --help` | v4.35.0 原生内建：config 五要件（challenge/solution_module、theorem_names、permitted_axioms 强制显式声明）、`--paranoid` 跑全五外部复核器、`--*-from-export` 接 NDJSON、bwrap 沙箱默认强制 |
| 22 | comparator 首跑（challenge=solution=out1.ndjson，config 钉两定理） | **受阻**：本机无 bwrap（无 root），拒跑并明示 EXIT=2 语 |
| 23 | comparator `--inadvisably-no-sandbox` 同参重跑 | **判定通过："Your solution is okay!"，2m14.6s**（Lean default kernel 复核全 59k decl 环境）✓ |
| 24 | comparator `--inadvisably-no-sandbox --paranoid` 同参 | **六复核器全过，9m12.6s**：Lean default + Lean paranoid + lean4lean（57,919 decl）+ nanoda（跳过 sorryAx，白名单外不硬拒）+ con-leche（57,922，--verified）+ con-ron（57,922，--verified）——**TB-06 机制之异构多核并轨最小实证完成** ✓ |

---

## 二、go/no-go 判定

**判定：GO（带三项条件）。**

依据：子件 A 三要件——①Lean v4.35.0 本体、②导出链（lean4export @5a9a355 / 工具链自带 leanexport）、③异构复核器（nanoda_lib 自构 + 工具链自带五复核器）——在本受限环境**全部可得且最小目标端到端贯通**（导出→Comparator 判定→六复核器交叉全绿，三段时间实测在案）。TB-06 由「机制已设计、基线未跑（T0）」推进至「机制最小件实测绿、真实规模基线未定」，已具备转 T1 之机器佐证要件（S2 machine_checks 六字段可实填：tool=lake comparator / tool_version=v4.35.0 / verdict=accepted / as_of=2026-10-22 / run_id 与 log_sha256 待 CI 通道复跑回填）。

三项条件（均入 §五阻塞清单）：C-a 真实 NsGalerkin+mathlib 规模基线须走 CI 通道或 ≥8GB 内存机；C-b 生产判定须补 bwrap 沙箱层（本环境只能 `--inadvisably-no-sandbox`，其自身输出即声明 "this run is not trustworthy"——spike 通道可用、验收通道不可用）；C-c rustup/Lean 下载依赖 ghfast/rsproxy 两镜像通道，供应链假设须入册。

---

## 三、六条信任假设入册草稿（TB-06 口径，逐条 T 级定级建议）

| # | 信任假设 | 内容（Comparator 链） | 信任性质 | 本次实测佐证 | T 级建议 |
|---|---|---|---|---|---|
| TA-1 | **导出器保真性** | leanexport/lean4export 将 kernel 环境忠实序列化为 NDJSON，无声明丢失/篡改/语义改写 | 已证伪可审计（双跑比对+异构 kernel 拒收即检出）；导出器实现正确性本身含 TCB 成分 | #18/#19 双跑字节级一致；#20/#24 异构 kernel 全收——「导出件可被独立 kernel 完整消费」实证 | **T1**（机器佐证在案；保真性之 TCB 残留随 TB-01 口径披露） |
| TA-2 | **复核器正确性** | nanoda/lean4lean/leanchecker/con-leche/con-ron 各 kernel 实现无系统性误判（accept↔Lean kernel accept 一致） | **TCB**（异构交叉仅旁证，不能体系内自证——同 TB-01 法理） | #24 六复核器对同一导出件判定一致（全 accept）；反向负控（拒收失配件）未跑 | **T1**（正向交叉一致在案；负控实验入子件 B 待办，跑后方稳） |
| TA-3 | **环境确定性** | 同钉输入（同 olean 集、同工具链）导出/判定结果字节级可复现 | 已证伪可审计（双跑 cmp + sha256 对照即机制） | #19 字节级一致 + sha256 在案 | **T1**（最小件实测；NsGalerkin 规模复现为基线报告要件） |
| TA-4 | **缓存完整性** | `.olean`（含 mathlib cache 命中件）未被污染；Comparator 从 olean 导出故承此假设 | 已证伪可审计（anchor_only——TB-04 口径：命中仅证环境等价，不证内容）；关闭路径＝全量重编对照 | 本次最小件无外部缓存介入（本地全新构建）；mathlib cache 场景未测 | **T0**（机制在案未跑——未定+理由：须待 NsGalerkin 规模基线窗，与 TB-04 关闭路径同窗执行） |
| TA-5 | **版本一致** | 工具链/导出器/复核器/导出格式四方版本相干（导出格式版本须与产 olean 之 compiler 同源） | 已证伪可审计（版本钉对照 + githash 字段机读核验） | #14 实测漂移活证（HEAD→v4.36.0-rc1，须钉 5a9a355dc6c5）；#18 导出件 meta 头自带 `lean.githash=eb6cafb…` 机读钉；工具链自带 leanexport「deliberately not configurable」从机制上消除一维漂移 | **T1**（钉法+机读核验字段均在案且实战一次） |
| TA-6 | **时间测量** | 15–60min 暖缓存基线之计时口径可信：冷/暖定义、单时钟域 UTC(Z)、机器规格、测量方法（`time` real/user/sys）四项成文 | 未审计 → 可证伪（规程成文+机器钉登记后即可复核） | 本次四段计时（22.07s/21.77s/59.46s/2m14.6s/9m12.6s）均带机器钉（2C/4GB）；规程文本未成册 | **T0**（数据在案、规程未成文——子件 B 成文后即升 T1） |

---

## 四、验估报告骨架（子件 B · 1–1.5pd · 预填槽位）

```
TRUSTBOUNDARY-SPIKE-REPORT-01（kernel 化一期 spike 验估报告）
CLASSIFY: L1
0. 卷首：受理编号钉 / 双截止钉核验（相对事件钉 vs 2026-11-04，先到者）
1. spike 范围回顾：子件 A 实录指针（本文）+ 子件 B 本文
2. Comparator 并轨实测结论
   2.1 go/no-go 与三条件【填：本文 §二 + CI 通道复跑结果槽】
   2.2 暖缓存基线报告【填：NsGalerkin 规模 15–60min 实测｜未定+理由结转】
       - 槽：冷跑/暖跑计时表（机器钉）、导出件体量、sha256、log_sha256
       - 槽：--paranoid 六复核器逐核 verdict/计时/decl 计数
   2.3 负控实验【填：故意失配件（改陈述/越白名单公理）之拒收实录】
3. 六条信任假设入册定稿【填：本文 §三草稿 + 判定席定级裁决槽】
4. C2 Gap 引理簇可裁减集锁定论证【填：D01 九项 W1–W9 中 3–5 引理子集之选取理由、
   行数折算（800–950 行预算内闭合性论证）、估爆回退轨（降级登记预案）】
5. schema 试金石 S1–S6 预检【填：S2 machine_checks 六字段实测回填样（本 spike 首跑）、
   S4 dual_kernel 字段以 nanoda/con-leche 双核 dry-run 实填】
6. 人周核算：子件 A 实耗 vs 2–3pd 估算【填：实耗如实登】＋一期 5.2–6.5pw 维持/修正建议
7. 风险簿更新：R1 估爆 / R4 漂移（lean4export HEAD 活证已入）/ 新增【填：bwrap 沙箱层、
   镜像通道供应链、/tmp 易失层三项】
8. 合规自检：语纪律 / UTC(Z) 钉 / 版本钉齐 / 未定项清单收口
```

---

## 五、阻塞项清单（「未定+理由」，逐条关闭路径）

| # | 阻塞项 | 状态 | 理由与关闭路径 |
|---|---|---|---|
| B1 | **NsGalerkin+mathlib 规模暖缓存基线（15–60min）未跑** | 未定 | 理由：①mathlib cache CDN 连通性本环境未测；②本机 4GB RAM，nanoda 旧版 README 明示新 mathlib 体量可 OOM，导出件体量将远超 345MB；③/2pd 预算内首跑排障应走稳态通道。关闭：公域 CI 通道（TB-05 路径，ubuntu-latest 7GB RAM 规格）或 ≥8GB 内存机执行，log_sha256 同窗回填 |
| B2 | **bwrap 沙箱缺位** | 未定 | 理由：无 root、无 bwrap 二进制，comparator 默认沙箱拒跑（EXIT=2）；本次以 `--inadvisably-no-sandbox` 通过，其输出自宣 "not trustworthy"——spike 探测有效、验收判定不可援引。关闭：CI runner 自带 bwrap/userns 实测；或 bwrap setuid 静态二进制投递（须供应链登记） |
| B3 | **static.rust-lang.org 数据流停滞** | 未定（已绕行） | 理由：HEAD 200 但安装流实质不通，rustup 官方道在本环境不可用；绕行＝rsproxy.cn 镜像（非常规供应链，假设未入册）。关闭：镜像通道入 TB-02 供应链扩展登记 + CI 通道 rustup 官方源对照 |
| B4 | **/tmp 易失层** | 未定 | 理由：会话机有重启前科，本次全部安装产物（Lean/rustup/nanoda/导出件）于重启即失，基线数据不可跨会话援引。关闭：基线报告正式跑批落 CI 通道产物槽（artifact 三哈希入册惯例），本地仅留实录文本 |
| B5 | **comparator 负控未跑** | 未定 | 理由：本次仅正向（challenge=solution）判定；「失配必拒」之证伪性未实证。关闭：子件 B 期内构造改陈述件/越白名单公器件各一，跑拒收实录（机制在案，预估 <0.5pd） |

---

## 六、合规自检（本文件行文）

无新数学断言；全部计时/判定为 2026-10-22 本席实测并带机器钉；版本钉：Lean v4.35.0（githash eb6cafb7290e8bd5f2937522d8d804f58f02bafc）/ lean4export @5a9a355dc6c5 / nanoda_lib v0.4.26（ammkrn，HEAD depth-1）/ rustc 1.99.1 / 导出格式 NDJSON 3.1.0；未定项五条均按「未定+理由」登记（§五）；不涉及任何「NS 已解决」表述。Clay NS 未解决、未颁奖。

—— WS-H 攻坚线 R4 受理席 · 枢/PIVOT-01 体系 · EXT-WAVE-18「攻」续执行批三 · 2026-10-22
