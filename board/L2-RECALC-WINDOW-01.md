CLASSIFY: L1
# L2-RECALC-WINDOW-01 · L2-2 复算窗首开：WS-F 挂账 U-20/U-13/U-12 消化（+v4.35.0 新能力演示）
枢/PIVOT-01 联邦 EXT-WAVE-18 饱和批二阵 L3 席（verifier）· 复算 as-of：本会话 · 仓 HEAD e69b122fac4a5c4e7addf6ca80e5caf94806339c
规程：每判定附机器输出原文；portal 写后复读；免工具链子项优先落盘。

## U-20 ｜ 三槽 SHA-256 + 联合指纹复算

挂账原文（board/W-NS-03-REFORGE-CHARTER-01.md L102）：「yaml L179–182（三槽哈希 + self_fingerprint）｜log/statement/proof 三 SHA-256 + 联合指纹｜本席未复算；系 run 产物登记转引（EXT16 §5 声明解冻依据）」。
WS-F 扫描（board/WSF-EVIDENCE-SWEEP-20261023-01.md §U-20）判定「部分证据」：FIPS 180-4 基准在位，复算须内部执行。

### U-20-A ｜ palomar-registry-v1.yaml PAL-0003 三槽（在册 recipe 可复算）——判定：**一致（PASS）**

钉点核验（git rev-parse ca67c869988a2123937c5d696b746399703becdf:library/ns）：
```
eb5b89cfc81ced6f097fa392bc34d085547648d3
```
与登记 `tree_library_ns: eb5b89cfc81ced6f097fa392bc34d085547648d3` 逐字符一致。

三槽独立复算（git show 钉点 blob → sha256sum；槽3 按登记 recipe 固定序 cat 合并流）：
```
槽1 toolchain   实测 ca5f1f601d34c49079e38d7e7041eb0f2a9c227fbc1df0f404820069a052330c
槽2 dependencies 实测 c3981e3ee1f71c18472c393aad0e760b4bc23c0783a7fdfd1df67876a1628d07
槽3 source-stream 实测 624cf2e044a4163bd1d338ee16da55c80da325d62ed870206c5942c177e331be（1217 行）
```
与 PAL-0003 登记值（registry/palomar-registry-v1.yaml L227/L231/L235）逐字符对拍：**3/3 一致**；行数 1217 与登记「1217 行」一致。

### U-20-B ｜ PAL-0001（历史条，经勘误 PAL-0001-CORR 映射钉 6358f1225）——判定：**一致（PASS）**

```
git log --oneline -1 6358f1225 → 6358f1225 EXT-WAVE-17「猎」收波: LAB-CLOSE-EXT17 + FSL v41 · 20261020T1620Z
git rev-parse 6358f1225:library/ns → eab2ed09f18e996d0c03fab950d4ef2ce02f357e  （与登记 tree 钉一致）
槽1 实测 ca5f1f60…52330c ✓；槽2 实测 c3981e3e…628d07 ✓；槽3 实测 2cfdcf96d20503c552d0cd7adfc55f1822693e3e723e2f039ed1fdbb0ccc0172 ✓（1192 行 ✓）
```
勘误条「钉漂移但三哈希继续有效（对内容计算）」之主张经复算**成立**。

### U-20-C ｜ formalization.yaml L179–182（U-20 挂账本义：log/statement/proof 三槽 + 联合指纹）——判定：**不可复算（FAIL-to-verify，维持挂账）**

机器证据：
1. 三槽所指对象不在仓。登记行（library/ns/formalization.yaml L178–182）：
```
    artifact_digests:               # Q6-b log_digest（Palomar 三槽位式，发放时实测回填）
      log_sha256: "d545d60d9cf0c80a6e82783044d7aab1fe4bbf73c9178180d64ed0e7e6ef8e32"
      statement_sha256: "6ac0bb1f1bdbdd3fcdf8028f09811d708d2faddd3a5ea63ca3c20703d8599950"
      proof_sha256: "0facac49b51bd8dbc031eb6c265296b3e84def3d2d591e1658155e705b00ff24"
    self_fingerprint_sha256: "96a2e74d14b1f0375abbc6702e2eef5df4113bd37b18a21bb97b002ce1ec5f34"   # WELD V2-1：verdict+yaml+config 联合哈希
```
   全仓 git grep 该四值仅命中 formalization.yaml 自身与 registry 转引；**无一处登记槽↔工件映射**（log/statement/proof 各指哪一文件/产物）。
2. 候选对象穷举试算全部不符（sha256 实测，Python hashlib）：
   - `sorryA.txt` 重建候选 `"sorry_count=0\n"` → `6e915d98…142c0`（≠ 任何槽）
   - formalization.yaml 现行版 → `d88e327f…20fbc`；回填前占位重建版（四值换回 PENDING-AT-ISSUANCE）→ `8fceec91…8550`（均≠ statement 槽）
   - axiomsA.log 标准格式重建（五行 `'…' depends on axioms: [propext, Classical.choice, Quot.sound]`）→ `2389e9c4…18ded`；PrintAxioms.lean 重建 → `f215829f…b598c1`（均≠ proof 槽）
   - 联合指纹候选配方：三槽 hex ASCII 直拼 → `5bfee799…2d5`；加换行拼 → `c3000c76…9432af`；raw bytes 拼 → `f57fcc7d…b555`（均≠ 96a2e74d…5f34）
3. 规程原文（board/WELD-A-SPEC-01-V2-CAND-01 L10）仅定「判定程序版本哈希 + 输入工件哈希 + 判定时刻（UTC）」三要素，**未定串行化格式**（拼接序/分隔符/编码均未登记）；CI 产物本体（run 39214080542 artifact `m1-1-spike-logs`：buildA2.log/axiomsA.log/sorryA.txt 等，workflow 定义见 .github/workflows/m1-1-toolchain-spike.yml L113–125）在 GitHub artifact 存储，仓内无副本，PAL-0001-A 已载「/logs 实测 HTTP 403」。

结论：L179–182 四值既无仓内对象可复算、亦无逐字配方可重放，「转引二级」状态经本次复算窗**证实无法升级**；且发现登记缺陷——槽语义映射（哪一工件入哪一槽）与指纹串行化配方未随值登记，纵取得 CI 产物亦只能猜测对拍。

### U-20-D ｜ 附带发现：工作区漂移（append-only 纪律无碍，但现行引用风险）

```
git rev-parse HEAD:library/ns → 1e4abd7d4d73afaacfdeb0c50cede5ee023c6da0（≠ PAL-0003 钉 eb5b89cfc）
git diff --stat ca67c8699 HEAD -- library/ns → 8 files changed, 3415 insertions(+)（新增 AbsorbingBall/CondUniqueness/Ladyzhenskaya/Lorenz96/OpenDomain 5 文件；NsGalerkin.lean/Basic/SkewB 有改动）
现行工作区按 PAL-0003 recipe 复算 source-stream → 9e62dc6f2f500d1443c1f61c2b88451394b30f8ee74e18f580ca735c4e8f5b66（≠ 登记值）
```
即：PAL-0003 三槽对其钉点成立，但**对现行 HEAD 不成立**；凡以 PAL-0003 哈希指称「当前包体」的引用均属钉外引用。按 append-only，应以新条目重新登记现行包体（9→14 文件）。

### U-20 销账建议
- U-20 本义（yaml L179–182）：**不可销**。缺：①槽↔工件映射登记；②联合指纹串行化配方成文；③CI 产物归档（或公域 CI 见证窗重跑并当场回填三槽+配方）。建议依 V2-1 新规程重发证书取代对旧值复算。
- 注册表三槽（PAL-0001/PAL-0003）：复算一致，可作 U-20 部分消化之实据登记；附带触发「现行包体重新登记」新义务。

## 环境重建记录（U-13/U-12/演示项共用底座）

- 工具链：ghfast 下 `lean-4.35.0-linux.tar.zst`（594,481,375 B）→ python+zstandard 流式解压 22.4s → `/tmp/lean-4.35.0-linux`；`lean --version` 实测 `Lean (version 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)`；`Lake version 5.0.0-src+eb6cafb`。
- 工程副本：`git archive ca67c869988a2123937c5d696b746399703becdf library/ns`（PAL-0003 在册钉点）→ /tmp/ns-recalc；lake-manifest.json 解压后实测 sha256=`c3981e3e…628d07`（与槽2登记值一致，构建过程未被改写）。
- mathlib cache：`lake exe cache get` 串行失速（~1 件/s）；从在途 `.part` 文件抽得 8448 件 URL（布局 `https://cache.mathlib.org/mathlib4-master/f/<hash>.ltar`，HEAD 实测 HTTP 200），xargs -P48 预取约 9 分钟下齐，`lake exe cache get` 复跑 `rc=0 wall=86s / Decompressed 8443 already-cached file(s) / Completed successfully in 82438 ms`。
- 构建：`lake build` → `rc=0 wall=534s`，日志尾原文 `✔ [3290/3291] Built NsGalerkin (74s)` / `Build completed successfully (3291 jobs).`；`grep -c "^error" build.log = 0`；源码 sorry 令牌扫描 0 命中。**独立复核了 PAL-0003 所载技术席「EXIT=0、3291 目标」声明（值逐字符相符）。**

## U-13 ｜ galerkinNS_exists_unique_solution_upto 打包件公理桥接 —— 判定：**实跑成立（PASS）**

探针（/tmp/ns-recalc/Probe.lean，`lake env lean Probe.lean`，wall=79s）输出原文：
```
'NSGalerkin.galerkinNS_exists_unique_solution_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.exists_solution_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.norm_sq_le_of_solution' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.solution_unique_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
'NSGalerkin.GalerkinNS.exists_unique_solution_upto' depends on axioms: [propext, Classical.choice, Quot.sound]
```
打包件公理集 = {propext, Classical.choice, Quot.sound} = 三已审组分公理集之并（三者各为同一集合）；打包未引入任何额外公理（无 sorryAx、无自设公理）。源码层旁证：Concrete.lean L136–145 打包体为单行直调 `(GalerkinNS.concreteData a f).exists_unique_solution_upto x₀ hT`。「桥接方法学成立但须实跑判定」（WS-F §U-13）之实跑条件现已满足。
销账建议：**可销**（以本节探针输出原文为证据锚；建议同时将打包 decl 补入 CI 公理审计清单，防回归）。

## U-12 ｜ capAnchorP1 / zetaAnchorImpliesRHCriticalLine 公理覆盖 —— 判定：**二 decl 公理审计实跑通过（PASS），另获两项边界发现**

定位订正：二 decl 不在 artifacts/CERT-CIRC-LEAN-01，实在 library/ns（NsGalerkin/CapAnchor.lean L131、NsGalerkin/ZetaAnchor.lean L35）；故无需 CERT-CIRC-LEAN-01 构建（该件依赖 leancert @v4.34.1 + 第二套工具链，评估 >30min，本窗不开销，见下）。
探针输出原文（同一次 Probe.lean 运行）：
```
'NSGalerkin.capAnchorP1' depends on axioms: [propext, Classical.choice, Quot.sound]
'ZetaAnchor.zetaAnchorImpliesRHCriticalLine' depends on axioms: [propext, Classical.choice, Quot.sound]
Probe.lean:16:14: error(lean.unknownIdentifier): Unknown constant `NSGalerkin.zetaAnchorImpliesRHCriticalLine`
```
- 二 decl 公理集均 = 三公理白名单，无 sorryAx；审计覆盖缺口（原 CI 五 decl 清单不含此二件）经本探针补足实跑证据。
- **边界发现 1（层位钉）**：二 decl 均为 `def : Prop` 陈述锚（CapAnchor.lean L101/L130「no proof is asserted here (external proof layer DONE; kernel layer BLOCKED(B1)」；ZetaAnchor.lean L34「No proof asserted」）。#print axioms 覆盖其定义性依赖闭包，**不构成任何证明性断言**。涉 RH 行文钉维持：「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」；zetaAnchorImpliesRHCriticalLine 为全局尺度临界线命题的 Prop 陈述件，非 RH 证据。
- **边界发现 2（登记错位，新立案线索）**：formalization.yaml alignment L160 登记名为 `NSGalerkin.zetaAnchorImpliesRHCriticalLine`，kernel 实测该名**不解析**（Unknown constant）；真实全名为 `ZetaAnchor.zetaAnchorImpliesRHCriticalLine`（ZetaAnchor.lean L18 命名空间）。同条 `NSGalerkin.capAnchorP1` 解析正常。即 yaml alignment 第 5 条 lean 名半错——与 U-17（帧 §3.2 编号归属不符）同条邻位，建议并入 U-17 修订一并处理。
销账建议：**可销（公理覆盖部分）**——以探针原文为锚；但须附两条注记入档：①覆盖为定义层非证明层（RH 钉原样保留）；②yaml 名错位须另案修订（不构成 U-12 销账障碍，属 U-17 族）。

## 演示项 ｜ v4.35.0 `lake check` 常态化可行性 —— 判定：**PARTIAL（环境性受阻，功能存在性已核）**

功能在位核验（`lake check --help` 输出原文节录）：
```
USAGE:
  lake check [--from-export <FILE>] [--paranoid] [--inadvisably-no-sandbox]

Builds the default build targets, exports them, and replays the result through
the kernel, erroring on any use of non-standard axioms.
  --paranoid                 also run all external checkers bundled with Lean
                             besides Lean's own kernel: `leanchecker-paranoid`,
                             `lean4lean`, `nanoda`, `con-leche` and `con-ron`
```
实跑两态：
1. 默认（bwrap 沙箱）态：`rc=1 wall=0s`，输出原文 `bwrap: Can't mount proc on /newroot/proc: Operation not permitted` / `error: Child exited with 1`——本容器无 unprivileged user namespaces，沙箱态不可用（bwrap 本体在位：/usr/bin/bwrap）。
2. `--inadvisably-no-sandbox` 态：首行警告原文 `WARNING: Sandbox disabled, this run is not trustworthy.`；运行 32 分钟未收敛（停在 Resolving dependencies 之后的子 lake 阶段，子进程 RSS 峰值 2,425,192 kB ≈ 2.3GB / 4GB 总量，导出件未产出），按时限主动终止（kill -9），未重跑。
结论钉：`lake check` 功能随 v4.35.0 工具链在位（help/子命令实测存在）；**本机（4GB RAM / 2 核 / 无 user-ns）不具备常态化实跑条件**——沙箱态被内核机制拒、免沙箱态资源/耗时超窗。常态化登记建议：走公域 CI 通道（ubuntu-latest 7GB 规格，TB-05 路径）或 ≥8GB 内存机，与 TRUSTBOUNDARY-SPIKE-B-REPORT-01 B1 条既有建议并轨；`--paranoid` 五复核器交叉未跑到，随 CI 首跑一并登记。

## 附：U-12 涉及之 CERT-CIRC-LEAN-01 依赖成本评估（按令评估，>30min ⇒ 不建）

artifacts/CERT-CIRC-LEAN-01/lakefile.toml 原文钉：`require leancert from git "https://github.com/alerad/leancert" @ rev "v4.34.1"`；lean-toolchain 原文 `leanprover/lean4:v4.34.1`。构建该件须：①第二套工具链 v4.34.1（约 600MB 下载）；②leancert 区间算术库源码全量构建（无 cache 通道可查，4GB RAM 下 OOM 风险已有 TB-06 B1 记录在案）。评估 ≫30min，本窗不开销，**该件构建验证记 PARTIAL**。注意：此不影响 U-12 销账——U-12 二 decl 实在 library/ns，公理覆盖已在 NsGalerkin 工程内闭环（见 U-12 节）。

## 判定汇总与销账建议

| 子项 | 判定 | 证据原文锚 | 销账建议 |
|---|---|---|---|
| U-20-A/B（registry PAL-0001/PAL-0003 三槽） | 一致（PASS） | 本件 U-20-A/B 节 sha256sum/git rev-parse 原文 | 可作 U-20 部分消化实据 |
| U-20-C（yaml L179–182 三槽+联合指纹，U-20 本义） | 不可复算（维持挂账） | 本件 U-20-C 节：四值全仓无对象、九组候选配方试算全不符 | **不可销**；缺①槽↔工件映射②指纹串行化配方③CI 产物归档；建议按 V2-1 重发证书取代复算 |
| U-20-D（附带发现：HEAD 对 PAL-0003 钉漂移） | 新发现 | git diff --stat 原文（+3415 行、9→14 文件） | 触发 append-only 新条目重新登记义务 |
| U-13（打包件公理桥接） | 实跑成立（PASS） | Probe.lean 输出原文（打包件=三组分并=三公理白名单） | **可销**；建议打包 decl 入 CI 审计清单防回归 |
| U-12（二锚 decl 公理覆盖） | 实跑通过（PASS，定义层） | Probe.lean 输出原文（二 decl 均三公理、无 sorryAx） | **可销（公理覆盖部分）**；注记①Prop 定义层非证明层，RH 钉原样保留；②CERT-CIRC-LEAN-01 构建验证 PARTIAL |
| 演示项（lake check 常态化） | PARTIAL（环境性受阻） | help 原文 + bwrap 报错原文 + WARNING 原文 + RSS/耗时实测 | 登记为 CI 通道项 |
| 新发现：yaml alignment L160 ζ 锚 lean 名不解析 | 新发现 | `Unknown constant 'NSGalerkin.zetaAnchorImpliesRHCriticalLine'`（实名 ZetaAnchor.zetaAnchorImpliesRHCriticalLine） | 并入 U-17 族修订案 |

涉 RH 行文钉（全件适用）：「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」；Clay NS/RH 未解决、未颁奖；OpenAI 相关成果口径维持「自评已核、外部复现中、未颁奖」。

——枢/PIVOT-01 联邦 EXT-WAVE-18 饱和批二阵 L3 席（verifier）· L2-2 复算窗首开
