CLASSIFY: L1
# KERNEL-PARANOID-PILOT-RUNBOOK-01 · QF-OS 联邦批二十六（EXT-WAVE-38）S4 · ζ 四锚闭包 `lake check --paranoid` 试点运行手册

- 席别：QF-OS 联邦批二十六 S4 kernel paranoid 试点 runbook 起草席（只产 runbook 文，不作终裁、不执行、不授权执行；执行权属 R2B-09 在案责任线 B1/工具链席）
- 成文日期钉：**2026-10-26**（UTC(Z) 单时钟域）
- 上游依据：board/KERNEL-PARANOID-EVAL-01.md（本席批二十五件，下称「评估件」）§5 试点建议与 §6 风险单；ADJUD-WILDQ-R1-HARVEST-01 R2B-09（四锚第二通道重放义务，责任线 B1/工具链席，窗 **2026-11-15**）；ADJUD-R2B-20261026-01 案 E（Tenet 挂账延期、避让纪律、定谳庭窗）；U17-KERNEL-PROBE-01（环境台账与四锚行号钉）；OBL-NS-02-TENET-RERUN-02（机位/构建实测钉）；WSH-S2-BLOCKER-DRAFT-01（日志原始字节先例）。
- 口径纪律（全件适用，逐字）：涉 ζ 表述一律限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」，全件严禁且无「RH 已证」字样；涉 NS 表述一律限「**有限维 ODE 截断层**」语境，全件无「NS 已解决」方向表述，Tenet-repo 状态沿唯一批准语「自评已核、外部复现中、未颁奖」。
- 名值分离：命令名、文件名、字段名与其预期值/实测值分行分列；一切「预期输出样例」标注「形态钉（非实测）」，禁以样例充证据；设定门槛值均标注「设定值」并给推导基线。
- 三不声明：①**只交付不入库**——本件不写入 vci-inbox，不落 git；②**本沙箱不构建**——本席环境无 lean/lake/elan（批二十五实测 not found 在案），本件全部脚本为草案文本，未在本沙箱执行任何 Lean 构建/检验；③**覆写权归原线**——本件不改动任何既有件一字节；试点执行期对 library/ns、formalization.yaml、registry 的一切写权仍归各原线，runbook 不创设任何写权。

---

## 〇、试点对象与范围钉

- 检验对象（名值分离·行号钉沿 U17-KERNEL-PROBE-01 §2）：`NsGalerkin/ZetaAnchor.lean:25` `ZetaAnchor.zetaIsolationAnchor`、`:30` `ZetaAnchor.zetaUniqueZeroAnchor`、`:35` `ZetaAnchor.zetaAnchorImpliesRHCriticalLine`、`NsGalerkin/CapAnchor.lean:131` `NSGalerkin.capAnchorP1`，四锚均为 **Prop 级陈述定义**（statement-only，无证明断言），公理集在案实测＝[propext, Classical.choice, Quot.sound]。
- 形态：四锚＋依赖闭包 leanexport NDJSON 导出 → `lake check --paranoid --from-export` 多内核回放；主退路：NS 包 default targets 全量 `lake check --paranoid`（评估件 §5 A-3 降级形态）。
- 范围外（逐字钉）：本试点不产生证明内容；不触碰区间见证层数学（该层未 Lean 化，无可导出定理集，评估件 §3）；不改变状态钉「区间见证层 PASS、kernel 层未证、非 RH 证据」；不构成任何 RH 方向主张。
- 目的钉（双重）：①兑现/超额兑现 R2B-09（义务＝1 个第二通道，本试点给 ≥4 通道）；②为评估件 §5 验收判据 A-1～A-7 产实测数据，供判定席裁「换装转正/降级/复跑」。

---

## 一、环境清单与就位预检（P-1～P-8，含脚本草案）

### 1.1 环境清单（全部带在案出处，名值分离）

| 项 | 钉值 | 出处 |
|---|---|---|
| 机位档 | 2 核 / 4GB / 无 root | OBL-NS-02-TENET-RERUN-02 §一 |
| toolchain 钉 | `leanprover/lean4:v4.35.0`（lean-toolchain 文件逐字） | U17-KERNEL-PROBE-01 §1 |
| toolchain  tarball | lean-4.35.0-linux.tar.zst，594,481,375 B，sha256 `7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d` | U17-KERNEL-PROBE-01 §1 |
| `lean --version` 预期逐字 | `Lean 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release` | U17-KERNEL-PROBE-01 §1 |
| 库作业面 | library/ns 拷贝 11,887 文件 / 230M | U17-KERNEL-PROBE-01 §1 |
| mathlib cache | `lake exe cache get` **9031/9031**，110s | U17-KERNEL-PROBE-01 §1 |
| 锚件独立 elaboration 参照 | 72s（RC=0，零诊断） | U17-KERNEL-PROBE-01 §4 |
| 沙箱前提 | bubblewrap（bwrap），Linux-only（官方手册 25.1.5.8）；机位无 root → 依赖 unprivileged userns，须冒烟实测 | 评估件 §6 R-1 |
| 捆绑内核清单预期 | `leanchecker`／`leanchecker-paranoid`／`lean4lean`／`nanoda_bin`／`con-leche`／`con-ron`／`leanexport`（二进制名以外部一手实测清单为准；con-ron 是否入 --paranoid 实跑集待 A-4 裁决） | solveathome #2597 件「What the toolchain ships」段；评估件 §1.1 |

### 1.2 门槛（设定值，非实测；推导基线逐项列出）

- 磁盘空闲 **≥ 8 GiB**（设定值）。推导基线：toolchain tarball 0.594 GB＋解压放大约 1.5×＋mathlib cache「GB 级」（B1-INFRA-20261025-01 §3.3 在案量级）＋ns 作业面 230M×2（原树＋/tmp 拷贝）＋闭包导出（外部参照：22,948 记录/123 MB 量级闭包；本对象规模未实测）＋日志/控制件余量。
- 内存：paranoid 主跑时空闲 **≥ 3 GiB**（设定值）。推导基线：机位 4GB 在案；外部全环境 nanoda 36.6GB RSS DNF 先例证明全环境形态不可行，闭包形态外部参照 RSS 未见超机位量级但无联邦机位实测——未达门槛转 §4 D-1b 逐内核串行降级。
- 时间窗：主跑避开 11-04 S2 执行日算力争用（案 E 随裁纪律在案；见 §6）。

### 1.3 就位预检脚本草案（preflight.sh；草案文本，未在本沙箱执行）

```bash
#!/usr/bin/env bash
# KPAR-PILOT-01 preflight 草案 · 输出逐行 PASS/FAIL 供 §3 env/ 归档
set -u
ok(){ echo "P-$1 PASS: $2"; }; bad(){ echo "P-$1 FAIL: $2"; }
TC_BIN=""; command -v lean >/dev/null && TC_BIN="$(dirname "$(command -v lean)")"
# P-1 工具链在位与版本逐字
V="$(lean --version 2>/dev/null)"; [ $? -eq 0 ] \
  && echo "$V" | grep -qF 'Lean 4.35.0' \
  && echo "$V" | grep -qF 'eb6cafb7290e8bd5f2937522d8d804f58f02bafc' \
  && ok 1 "$V" || bad 1 "lean --version='$V'"
# P-2 lake 在位且 check 子命令可解析（不触发构建）
lake check --help >/dev/null 2>&1 && ok 2 "lake check --help rc=0" || bad 2 "lake check 不可用"
# P-3 捆绑内核二进制清单（名单实测落盘，供 A-4）
for b in leanchecker leanchecker-paranoid lean4lean nanoda_bin con-leche con-ron leanexport; do
  [ -x "$TC_BIN/$b" ] && echo "P-3 present: $b" || echo "P-3 MISSING: $b"
done | tee preflight-roster.txt
grep -q 'MISSING: leanchecker-paranoid\|MISSING: lean4lean\|MISSING: nanoda_bin\|MISSING: con-leche' preflight-roster.txt \
  && bad 3 "必需内核缺席（见 preflight-roster.txt）" || ok 3 "roster 落盘"
# P-4 lean-toolchain 钉逐字
grep -qx 'leanprover/lean4:v4.35.0' lean-toolchain && ok 4 "$(cat lean-toolchain)" || bad 4 "$(cat lean-toolchain 2>/dev/null)"
# P-5 bubblewrap 冒烟（无 root 机位测 unprivileged userns）
bwrap --ro-bind /usr /usr -- true 2>/dev/null && ok 5 "bwrap smoke rc=0" || bad 5 "bwrap 不可用→§4 D-3c"
# P-6 磁盘/内存门槛（设定值，§1.2）
[ "$(df -BG --output=avail . | tail -1 | tr -dc 0-9)" -ge 8 ] && ok 6a "disk>=8GiB" || bad 6a "disk<8GiB"
[ "$(free -g | awk '/^Mem:/{print $7}')" -ge 3 ] && ok 6b "mem avail>=3GiB" || bad 6b "mem<3GiB→D-1b 降级预案"
# P-7 mathlib cache 就位
lake exe cache get >cacheget.log 2>&1; tail -1 cacheget.log | grep -q '9031' && ok 7 "$(tail -1 cacheget.log)" || bad 7 "见 cacheget.log"
# P-8 锚件独立 elaboration 复验（防陈旧 olean，沿 U17-KERNEL-PROBE-01 §4 先例）
lake env lean NsGalerkin/ZetaAnchor.lean >anchor-elab.log 2>&1 && ok 8 "ZetaAnchor elab rc=0" || bad 8 "见 anchor-elab.log"
```

预检判据：**P-1/2/3/4/5/7/8 全 PASS 方得进入 §2**；P-6b FAIL 不阻行，转入 D-1b 预案标记。任一 FAIL 即停，按 §4 D-3 登记。

---

## 二、七条机检标准操作化（A-1～A-7 逐条：命令／预期输出样例／PASS-FAIL 判据／取证落点）

通用约定：run 目录 `$WORK=/tmp/kpar-pilot-01-<UTCts>/`（结构见 §3）；一切日志 `tee` 落盘原始字节（不重排、不裁截，沿 WSH-S2-BLOCKER-DRAFT-01 §一先例）；出口码一律 `set -o pipefail` 后显式捕获并写入日志尾行（沿 R2B-02 退出码契约化体例，FSL v59 在案）。导出命令形态草案（调用面首验项，若实调形态不同仅改命令行、规程不动——沿 WSH-S2-BLOCKER-DRAFT-01 §一末如实登记先例）：

```bash
lake env leanexport NsGalerkin.ZetaAnchor NsGalerkin.CapAnchor -- \
  ZetaAnchor.zetaIsolationAnchor ZetaAnchor.zetaUniqueZeroAnchor \
  ZetaAnchor.zetaAnchorImpliesRHCriticalLine NSGalerkin.capAnchorP1 \
  > $WORK/export/zeta-anchor-closure.ndjson
```

**A-1 导出确定性双导对拍**
- 命令：上式连跑两次（`zeta-anchor-closure.run1.ndjson` / `.run2.ndjson`），`sha256sum` 双件。
- 预期输出样例（形态钉，非实测）：两行 sha256 逐字全等（外部先例：同构建两次导出字节全等，solveathome #2597 件在案）。
- PASS/FAIL：PASS＝双哈希全等；FAIL＝不等 → 停，登记导出非确定事件（导出器确定性本身是证据前提），转 §4 D-2b。
- 取证落点：`export/zeta-anchor-closure.ndjson{,.run2}`＋`export/exports.sha256`。

**A-2 paranoid 主跑与出口码契约**
- 命令：`set -o pipefail; lake check --paranoid --from-export=$WORK/export/zeta-anchor-closure.ndjson 2>&1 | tee $WORK/logs/A2-paranoid-main.log; echo "exit=$?" | tee -a $WORK/logs/A2-paranoid-main.log`
- 预期输出样例（形态钉，非实测）：逐内核 accept 行若干＋公理报告行；尾行 `exit=0`。
- PASS/FAIL：PASS＝尾行 `exit=0`（官方契约：0＝全内核接受且仅标准公理）；`exit=1`→D-1/D-2a 分类；`exit=2`→D-3 分类。**禁以日志 grep 取 verdict 代出口码**（ADJUD-WILDQ2-HARVEST-01 §1/§2 伪绿通道裁决在案）。
- 取证落点：`logs/A2-paranoid-main.log`（原始字节）＋出口码尾行。

**A-3 闭包导出相容性（评估件 §5 A-3 首验项）**
- 命令：同 A-2（闭包导出形态即首验本身）；若 `lake check` 拒收闭包导出（exit=2 或格式错误行），退路＝包内全量形态：`cd $WORK/ns-work && lake check --paranoid 2>&1 | tee $WORK/logs/A3-fullpkg-fallback.log`。
- 预期输出样例（形态钉，非实测）：闭包被接受并进入内核回放；或退路日志含 default targets 构建段。
- PASS/FAIL：PASS＝两形态之一完成回放且资源读数落册；FAIL＝两形态均 exit=2 → D-3d。
- 取证落点：`logs/A2-paranoid-main.log` 或 `logs/A3-fullpkg-fallback.log`＋`env/A3-form-decision.txt`（实际采用形态一句话登记）。

**A-4 paranoid 实跑内核名单实测（裁决评估件 §1.1 con-ron 文档级微差）**
- 命令：`grep -iE 'leanchecker|lean4lean|nanoda|con-leche|con-ron' $WORK/logs/A2-paranoid-main.log > $WORK/env/A4-roster-observed.txt`（辅以各内核二进制 `--version` 或等价输出，逐件落盘）。
- 预期输出样例（形态钉，非实测）：名单 4～5 内核（con-ron 在/不在均可能——官方 Highlights 段与 #15145 行不一致，评估件 §1.1 双写在案）。
- PASS/FAIL：本项为**登记型判据**——PASS＝名单实测值逐字落盘（无论 con-ron 是否在内）；FAIL＝无法从日志析出名单 → 补跑单内核确认（§4 D-1a 命令）后落盘。结论句由评估报告模板 §六.4 承载。
- 取证落点：`env/A4-roster-observed.txt`＋各二进制版本输出。

**A-5 阴性控制（无控制不采信——2026-07 嵌套归纳伪造事件教训在案，FRONTIER-SCAN §4.4）**
- 控制件两件（草案）：
  - tamper-01（语义篡改）：闭包导出副本中置换一条目标声明记录的证明项字段为闭包内另一声明之证明项（外部先例形态：solveathome #2597 控制 1–6「swap one target's proof or type for an earlier theorem's」）。草案脚本：`python3 - <<'EOF'`（读 ndjson 行集→定位 `zetaAnchorImpliesRHCriticalLine` 记录行→与前一非公理记录行互换 value 字段→写出）`EOF`，产物 `controls/tamper-01.ndjson`。
  - tamper-02（格式篡改）：任一行复制为重复键 JSON 行（#15542 加固后读取器须拒收），产物 `controls/tamper-02.ndjson`。
- 命令：对两控制件逐件跑 `lake check --paranoid --from-export=<tamper>`（同 A-2 命令形），出口码尾行落盘。
- 预期输出样例（形态钉，非实测）：两控制件均非零出口（官方契约 1＝拒绝）。
- PASS/FAIL：PASS＝tamper-01 与 tamper-02 均 exit≠0；**任一控制件 exit=0 即红线**——停跑、封存全部日志、即日呈判定席（内核接受篡改导出＝潜在 soundness 事件，按嵌套归纳事件先例升红线，不得自行定性）。
- 取证落点：`controls/tamper-0{1,2}.ndjson{,.sha256}`＋`logs/A5-control-0{1,2}.log`。

**A-6 公理闸与三公理核对**
- 命令：A-2 主跑日志中公理报告段落原样截取 `logs/A6-axiom-report.txt`；对照在案探针值 `lake env lean` 探针四锚 `#print axioms` 输出（U17-KERNEL-PROBE-01 §3 原文在案：[propext, Classical.choice, Quot.sound]）。
- 预期输出样例（形态钉，非实测）：公理报告仅含 propext／Classical.choice／Quot.sound；主跑 exit=0（非标准公理即败为契约内含）。
- PASS/FAIL：PASS＝exit=0 且报告段无三公理外条目；FAIL＝出现白名单外公理 → 停，登记导出链污染嫌疑，转 D-2a，**禁继续**。
- 取证落点：`logs/A6-axiom-report.txt`＋对照钉（U17-KERNEL-PROBE-01 §3 逐字行）。

**A-7 资源读数落册（登记型，不设阈值——甲席席规不产估计）**
- 命令：`/usr/bin/time -v` 包裹 A-2 主跑与各控制跑，抽取 `Elapsed (wall clock)` 与 `Maximum resident set size` 两行。
- 预期输出样例（形态钉，非实测）：两行读数。
- PASS/FAIL：PASS＝读数落册；无 FAIL 态（跑不完由 A-2 承载）。
- 取证落点：`logs/A7-resources.txt`（名值分列：读数名＝值）。

---

## 三、出口产物规范

### 3.1 目录结构（run 根 `$WORK`，执行收尾后整体归档移交点＝判定席指定板面；本 runbook 不授权写入 vci-inbox）

```
kpar-pilot-01-<UTCts>/
├── env/
│   ├── preflight.log              # P-1～P-8 逐行 PASS/FAIL 原始输出
│   ├── preflight-roster.txt       # P-3 捆绑二进制清单实测
│   ├── lean-version.txt           # lean/lake --version 逐字
│   ├── A4-roster-observed.txt     # paranoid 实跑内核名单实测（A-4）
│   └── A3-form-decision.txt       # 闭包/全包形态登记（A-3）
├── export/
│   ├── zeta-anchor-closure.ndjson       # 主导出（run1）
│   ├── zeta-anchor-closure.run2.ndjson  # 确定性对照（run2）
│   └── exports.sha256                   # 双件哈希
├── logs/
│   ├── A2-paranoid-main.log       # 主跑原始字节＋exit 尾行
│   ├── A3-fullpkg-fallback.log    # （仅退路触发时存在）
│   ├── A5-control-01.log / A5-control-02.log
│   ├── A6-axiom-report.txt
│   └── A7-resources.txt
├── controls/
│   ├── tamper-01.ndjson{,.sha256} # 语义篡改控制件
│   └── tamper-02.ndjson{,.sha256} # 格式篡改控制件
├── manifest.sha256                # 全树逐件 sha256（名值分列：路径＝哈希）
└── REPORT.md                      # §6 模板成文
```

### 3.2 命名与完整性规则

- 日志命名钉：`A<判据号>-<语义名>.log`，一律原始字节（不重排、不裁截、不过滤，沿 WSH-S2-BLOCKER-DRAFT-01 §一「规范件」先例）；过滤截取件另存 `.txt` 且不得覆盖原始件。
- `manifest.sha256` 生成：`find . -type f ! -name manifest.sha256 -print0 | sort -z | xargs -0 sha256sum > manifest.sha256`。
- 导出件即证据对象：sha256 双导对拍（A-1）＋manifest 收录；任何二次移动以 `sha256sum -c` 复核留痕。
- 控制件与主导出同目录隔离（`controls/` 独立子树），防误喂主链。

---

## 四、失败降级路径（三分支判定树）

总律：一切降级以**登记换形态、不以沉默换绿**；降级产物强制携带降级标注（沿案 C 备通道「自证级」降格先例精神）；出口码分类先行——`1`＝拒绝/非公理/构建败（D-1/D-2），`2`＝根本无法运行（D-3）；分类不明时按 D-3 处理。

### D-1 单内核失败（主跑 exit≠0 且日志可定位为单一内核拒绝/崩溃/超时）

- D-1a 隔离复跑：将该内核对同一导出单独复跑，逐字落盘——
  `leanchecker --from-export=<file>`、`leanchecker-paranoid --from-export=<file>`（若支持同名旗标，否则以其 `--help` 实测为准）、`nanoda_bin <file>`、`lean4lean --import <file>`（外部先例调用形；实调形态以 `--help` 落盘为准）。
- D-1b 资源型降级（P-6b FAIL 或单内核 OOM/超时）：改逐内核串行（D-1a 序列逐条跑），每内核独立日志；仍不逮则缩闭包（减锚至 `zetaAnchorImpliesRHCriticalLine` 单锚闭包）重导重跑，缩减事实登记。
- 判归：
  - 单内核**可复现拒绝**（reject 非崩溃）→ **红线**：多内核分歧即潜在 soundness 事件（2026-07 先例：内核间行为分歧是真实缺陷信号，FRONTIER-SCAN §4.4 在案）——停跑、封存、即日呈判定席，禁自行定性「误报」。
  - 单内核崩溃/超时且不可复现拒绝 → 降级登记形态：「N 内核中 N−1 accept＋1 内核未完成（原因逐字）」；R2B-09 义务面（≥1 第二通道）若仍满足则如实并记「义务面满足／试点 A-2 未 PASS」——**两名目分行，不混格**。
- 登记格式：`D-1 事件行＝{内核名, 出口码, 日志路径, 复跑结果, 判归}`。

### D-2 全失败（主跑 exit=1 且非单内核可定位，或导出层失败）

- D-2a 非标准公理/拒绝：A-6 同步触红处理——停跑，核对导出 sha256（A-1）排除馈错；对照 U17-KERNEL-PROBE-01 §3 在案三公理；确认为导出链污染或钉漂移则登记事件呈裁；禁换源重试直至归因落册。
- D-2b 导出非确定（A-1 FAIL）：重导第三次；三次两两不等则登记「导出器非确定」事件呈裁（该事件本身即重要发现——导出确定性是 --from-export 证据链前提）；不等即停，禁以任一单件续跑充 A-1 PASS。
- D-2c 主跑全败但逐内核可跑：以 D-1a 序列收「单内核分项结果」降级件，标注「paranoid 编排层失败、内核层分项实测」。

### D-3 环境不就位（预检 P-1～P-8 任一阻断性 FAIL 或主跑 exit=2）

- D-3a toolchain 不符（P-1/P-4 FAIL）：以在案 sha256 `7289597a…f6d` 重取 tarball 重建（沿 U17-KERNEL-PROBE-01 §1 解压规程先例）；重取后仍不符 → 停，登记钉漂移事件。
- D-3b cache 不就位（P-7 FAIL）：重试一次并留 `cacheget.log`；仍败 → 登记断供事件（B1-INFRA §3.2/3.3 Azure 退役风险在案），本次试点顺延，不挤硬钉窗。
- D-3c bwrap 不可用（P-5 FAIL）：两轨——①执行席另备自备隔离（一次性容器/虚机）并以 `--inadvisably-no-sandbox` 跑，产物强制标注「**自备隔离降级形态**」（官方手册：该旗标仅自备隔离的专家场景；评估件 §6 R-1 在案）；②无自备隔离 → 本试点不顺延强跑，登记阻塞呈判定席改窗。
- D-3d 双形态均 exit=2（A-3 FAIL）：登记「lake check 本环境不可调度」事件，附 A4 roster 与 `--help` 落盘件，呈裁。
- 一切 D-3 顺延：状态行入 FSL 随批结转（沿既有结转体例），**禁以挂账时长本身作撤项论据**（案 E 随裁纪律同律适用）。

---

## 五、与 Tenet 30h 实验的接口边界

**不替代声明（随一切本试点产物逐字携带）**：

> 「本试点不改变 OBL-NS-02 挂账状态钉。Tenet-repo（github.com/openai/NavierStokesAndEuler，钉 f9e8bc5，toolchain v4.34.0-rc2）全量 2659 模块构建（在案实测吞吐 ~1.4 模块/分、ETA≈30h、2 核/4GB 结构性不可闭合）是任何全量导出的前提；`lake check --paranoid` 属检验编排层，不替代构建层。本试点一切产物不构成 Tenet 线任何闭合证据，Tenet 包状态维持：自评已核、外部复现中、未颁奖。」

**衔接点（四名目，名值分离）**：
1. **产物规范复用**：§3 目录/命名/manifest 规范按可复用设计，Tenet 闭包试点（若立项）原样沿用，仅换对象清单（基线 8 声明，OBL-NS-02-TENET-RERUN-02 §二在案）。
2. **跨版前置首验**：Tenet 试点独有的前置项＝v4.34.0-rc2 产导出 → v4.35.0 检验的格式相容性（评估件 §6 R-3 在案）；该项未 PASS 前 Tenet 试点不得排期。
3. **呈件对象**：Tenet 闭包换装材料归口案 E 定谳庭（11-15 双硬钉后首个庭期，不迟于 2026-12-05，ADJUD-R2B §五在案）——本试点 REPORT.md 仅作其证据材料候选，不构成裁项。
4. **算力避让**：本试点主跑避开 11-04 S2 执行日与 11-08/11-15 硬钉期（案 E 避让纪律）；Tenet 侧一切动作权属 NS 线/B1，本 runbook 不授权。

---

## 六、日程与评估收口

| 日（UTC） | 事项 | 责任线 | 避让/联动钉 |
|---|---|---|---|
| 11-03 | §1 预检全项＋cache 就位（P-7）＋双导出生成（A-1） | B1/工具链席（R2B-09 在案） | 与 W2-P0-09 预飞闸同窗；预检 FAIL 即转 D-3 不硬闯 |
| 11-04 | 执行候选日①：paranoid 主跑（A-2/A-3/A-4/A-6/A-7）＋阴性控制（A-5） | 同上 | **前提：确认不挤 S2 执行日算力**（案 E 纪律）；冲突则全量滑至 11-05 |
| 11-05 | 执行候选日②（内容同上）；D-1b/D-2c 降级补跑同窗 | 同上 | — |
| 11-06 | 评估收口：REPORT.md 成文＋manifest.sha256 封存＋报送 | 起草席汇总→判定席 | 报送口：R2B-09 销记评估（窗 11-15 前）；Tenet 衔接材料归口案 E 定谳庭 |

### 评估报告模板（REPORT.md 骨架，执行席填空；方括号为名，值实测后填）

```
CLASSIFY: L1
# KPAR-PILOT-01-REPORT · ζ 四锚闭包 kernel paranoid 试点评估报告（有限高度 T=100/1000 截断语境）
0. 状态钉（逐字）：区间见证层 PASS、kernel 层未证、非 RH 证据；Tenet 钉：自评已核、外部复现中、未颁奖。本报告不改变两钉。
1. run 指纹：[run_id] / [lean --version 逐字] / [toolchain sha256] / [bwrap 形态：沙箱|自备隔离降级] / [机位档]
2. 判据总表：A-1 [PASS/FAIL+sha256 双值] ｜ A-2 [exit=] ｜ A-3 [采用形态：闭包|全包退路] ｜ A-4 [实跑名单逐字] ｜ A-5 [tamper-01 exit= / tamper-02 exit=] ｜ A-6 [公理集逐字] ｜ A-7 [wall / max RSS 读数]
3. A-4 结论句：con-ron [在/不在] paranoid 实跑集——评估件 §1.1 文档级微差裁决为 [值]。
4. 降级/异常：[无 / D-x 事件行逐字]
5. R2B-09 销记评估：义务面（≥1 第二通道）[满足/不满足，载通道名清单]；与试点 A-2 PASS 与否分行陈述。
6. 建议（供判定席，非裁）：[转正 / 降级复跑 / 转 Tenet 二试点首验 R-3]
7. 附：manifest.sha256 首行＋全件计数；日志路径清单。
```

---

## 附、纪律自查与依据钉

1. C1′/C2′：涉 ζ 表述限「有限高度 T=100/1000 截断」语境；状态钉逐字「区间见证层 PASS、kernel 层未证、非 RH 证据」；全件无「RH 已证」字样；涉 NS 限「有限维 ODE 截断层」语境；无「NS 已解决」方向表述。
2. 名值分离：二进制名/命令形/哈希钉与实测值分行；预期输出样例均标「形态钉（非实测）」；门槛值标「设定值」并给推导基线。
3. 不编数：全部数值（594,481,375 B、9031/9031、110s、72s、~1.4 模块/分、2659 模块、22,948 记录/123MB、36.6GB 等）带在案钉或外部钉；日程全部引用既有裁决窗。
4. 三不声明在位：只交付不入库（未写 vci-inbox、零 git）；本沙箱零构建（全部脚本为草案文本）；覆写权归原线（未动任何既有件）。
5. 依据钉：KERNEL-PARANOID-EVAL-01 §1/§5/§6；U17-KERNEL-PROBE-01 §1–§4；OBL-NS-02-TENET-RERUN-02 §一–§三；ADJUD-WILDQ-R1-HARVEST-01 R2B-09；ADJUD-R2B-20261026-01 案 E；ADJUD-WILDQ2-HARVEST-01 §1/§2/§8；WSH-S2-BLOCKER-DRAFT-01 §一；B1-INFRA-20261025-01 §3.2/§3.3；FRONTIER-SCAN-20261026-02 §4.4；solveathome #2597 件（双导全等/控制件法/bin 清单）；lean-lang.org v4.35.0 发布注记与 Lake 手册（出口码契约/沙箱/Linux-only/#15542）。

—— QF-OS 联邦批二十六（EXT-WAVE-38）S4 kernel paranoid 试点 runbook 起草席 · 2026-10-26 · 只交付不 commit
