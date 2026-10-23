CLASSIFY: L1
# OBL-NS-02-TENET-RERUN-02 · Tenet（openai/NavierStokesAndEuler）钉 f9e8bc5 复跑批七：环境重建 + 公理采样 8/8 补齐
枢/PIVOT-01 · EXT-WAVE-19 饱和批 B2′ 席（verifier，接替已消亡 B2 续作线） · 授权源：EXT-WAVE-19 批七完成度线 · 执行 2026-10-23T23:15Z 起 · 登记 2026-10-24T00:30Z

> 状态钉（唯一批准语）：**自评已核、外部复现中、未颁奖**。本件为见证与复现报告，不做「验证通过/失败」终局断言。涉 NS 表述维持 C1 边界：所有结论均在「有限维 ODE 截断层」之上、形式化工件层面，不涉「NS 已解决」类断言。

## 一、环境重建与 manifest 抽查

**命名空间勘察**：前任 B2 环境随其消亡不可知；本席 /tmp 下无 tenet-src 遗留（实测 `/tmp` 无相关目录），按预案全新重建，未依赖任何前任续跑态。

| 项 | 值 | 证据 |
|---|---|---|
| 仓址 | github.com/openai/NavierStokesAndEuler（ghfast 前缀全克隆） | clone OK |
| 钉 | checkout 实得 `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` | `git rev-parse HEAD`，与 RERUN-01 `.pin.txt` 逐字一致 |
| toolchain | tarball sha256 `3d011041203acacf300d343a39673f7d233743397993797c941346ae9e5df1a8`（580,281,129 B，ghfast 降速后改 gh-proxy 镜像竞速，字节数与 RERUN-01 记录一致） | `sha256sum`，与 `.toolchain-sha256.txt` 一致 |
| toolchain 版本 | Lean 4.34.0-rc2, commit 6a10ac8c22beadecabdbb0919c2b50214762f91d；Lake 5.0.0-src+6a10ac8 | `lean --version` / `lake --version`，与 RERUN-01 §二逐字一致 |
| 依赖钉 | lake-manifest 11 包 rev 逐字吻合（mathlib `85e3a25e…`、Comparator `19e111e2…` 等） | manifest 比对；mathlib 经 gh-proxy tag 浅克隆（--depth 1 --branch v4.34.0-rc2）就位，`git rev-parse HEAD`=`85e3a25e006c35636f0e53b0e9296caca2685bc0` 与钉精确一致 |
| cache | `lake exe cache get` **8747/8747** 下载并解压 | `Decompressed 8747 file(s)` 日志尾行，与 `.cacheget-tail.txt` 同数 |
| 机器 | 2 核 / 4GB / 无 root（与 RERUN-01 同档） | 实测 |

**manifest 抽查**：对 RERUN-01 归档的 2669 文件 sha256 manifest 做两次独立随机抽取各 20 文件（共 40 样本），本地 `sha256sum -c` 全部 OK，零漂移。归档 `OBL-NS-02-TENET-RERUN-02.manifest-spotcheck.txt`（第二次抽取 20 条）。

## 二、公理采样 8/8 对拍表

基线 8 声明（名值分离·运作定义）：`NavierStokes/ProblemStatement.lean` 全部主声明 7 件（def `candidateStatement` + 6 theorem）与 `NavierStokes/R3/ProblemStatement.lean` 主命题 def `breakdownStatement`，合计 8。RERUN-01 已采样其中 4 件（动态，`#print axioms`）；本批补齐其余 4 件，并对 RERUN-01 已采样 4 件在本重建环境全量复跑交叉确认——即 8/8 均在本窗口内经本席环境动态实测，非仅引用批六结果。

方法：`lake build NavierStokes.ProblemStatement`（2434 jobs，0 error，42s）与 `lake build NavierStokes.R3.ProblemStatement`（2613 jobs，0 error，18s）建成后，探针文件 `AxiomsProbeRerun02.lean` / `AxiomsProbeRerun02b.lean` 经 `lake env lean` 执行。探针输出归档 `OBL-NS-02-TENET-RERUN-02.axioms-probe.txt`。

| # | 定理/声明 | 采样方式 | 公理集 | 与预期白名单一致性 |
|---|---|---|---|---|
| 1 | `NavierStokes.ProblemStatement.candidateStatement` | 动态（批六采样+本批复跑） | [propext, Classical.choice, Quot.sound] | 一致 |
| 2 | `NavierStokes.ProblemStatement.smooth_at_interior` | 动态（批六采样+本批复跑） | [propext, Classical.choice, Quot.sound] | 一致 |
| 3 | `NavierStokes.ProblemStatement.zero_force_time_support` | 动态（批六采样+本批复跑） | [propext, Classical.choice, Quot.sound] | 一致 |
| 4 | `NavierStokesR3.ProblemStatement.breakdownStatement` | 动态（批六采样+本批复跑） | [propext, Classical.choice, Quot.sound] | 一致 |
| 5 | `NavierStokes.ProblemStatement.unit_period_negative` | 动态（本批新采） | [propext, Classical.choice, Quot.sound] | 一致 |
| 6 | `NavierStokes.ProblemStatement.zero_residual` | 动态（本批新采） | [propext, Classical.choice, Quot.sound] | 一致 |
| 7 | `NavierStokes.ProblemStatement.zero_velocity_not_unbounded` | 动态（本批新采） | [propext, Classical.choice, Quot.sound] | 一致 |
| 8 | `NavierStokes.ProblemStatement.unbounded_speed_excludes_uniform_bound` | 动态（本批新采） | [propext, Classical.choice, Quot.sound] | 一致 |

**结论**：8/8 恰为标准三公理 [propext, Classical.choice, Quot.sound]，未见 sorryAx 或任何白名单外公理，无注入迹象。A3 公理审计推进至「基线 8 声明抽样级全坐实（动态）」；全声明闭包（2659 仓内模块）仍待 A2 全量建成后复核。

## 三、全量构建状态评估与 OBL-NS-02 挂账

- 批六实测：2 核吞吐 ~1.4 模块/分，96/2659=3.6%（0 error/0 warning）后窗口截断，全量 ETA ≈ 30h；批六续跑态随 B2 环境消亡**不可收割**（/tmp 无遗留，§一）。
- 本批窗口（2.5h）按使命定义仅做单模块定向构建以服务公理采样，两模块（ProblemStatement / R3.ProblemStatement）均一次通过、0 error，与批六「构建无质性分歧」判断相容；cache 8747/8747 复得，依赖钉零漂移。
- **正式结论**：A2 全量 build 复现在 2 核/短时窗通道下结构性不可闭合（ETA 30h ≫ 窗口），需更强算力通道或长磨专窗；**OBL-NS-02 维持挂账，不闭合**。本批无反证、零漂移，A3 抽样闭环推进如上，A4（sorry 仅 ComparatorChallenges 有意占位）批六已达成、本批未见异动，A5 双 kernel 未启动维持原状。
- 状态钉维持：**自评已核、外部复现中、未颁奖**。

## 四、登记件

- 本件：`board/OBL-NS-02-TENET-RERUN-02.md`
- 附件：`OBL-NS-02-TENET-RERUN-02.axioms-probe.txt`（8 声明探针输出+环境指纹） / `OBL-NS-02-TENET-RERUN-02.manifest-spotcheck.txt`（20 文件 sha256 抽查记录）
- 探针源文件留存 /tmp/tenet-src/AxiomsProbeRerun02{,b}.lean（未 commit，源树未写外部仓）

——枢/PIVOT-01 B2′ 席
