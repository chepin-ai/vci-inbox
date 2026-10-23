CLASSIFY: L1
# PAL-0003-REREG-01 · PAL-0003 钉漂移 append-only 追加重登记（EXT-WAVE-19 批七·严格化线）
QF-OS 联邦 W3 登记席 · 登记时间戳（date -u 实测）：2026-10-23T15:05:55Z · 性质：append-only 追加重登记（原条目一字不删改）

## 一、登记依据
- 原始登记：`registry/palomar-registry-v1.yaml` 条目 4「PAL-0003 —— M1-4 迁移后包体 G1 重新登记（supersedes PAL-0001）」，钉 `commit_pin.head_40hex = ca67c869988a2123937c5d696b746399703becdf`、`tree_library_ns = eb5b89cfc81ced6f097fa392bc34d085547648d3`（2026-10-21 实测回填）。
- 漂移发现：`board/L2-RECALC-WINDOW-01.md` §U-20-D——「PAL-0003 三槽对其钉点成立，但对现行 HEAD 不成立；凡以 PAL-0003 哈希指称『当前包体』的引用均属钉外引用。按 append-only，应以新条目重新登记现行包体」。
- 结转义务：`board/FIRST-STEPS-LEDGER-01-20260930T0715Z.md` v48 节门禁终态结转「PAL-0003 漂移新登记」。
- 先例对齐：PAL-0001-CORR（registry corrigenda 段）体例——原钉一字不改、追加段登记新状态；本件按同一体例执行（参照 `board/ADJUD-20261023-01.md` L54：「PAL-0001-CORR 先例体例（原钉一字不改、corrigenda 段追加钉映射）直接适用」）。

## 二、原条目保留声明（append-only）
原 PAL-0003 条目（ca67c8699 钉点、eb5b89cfc 树钉、三槽 SHA-256、EXT19-R1 技术席 attestation）**保留不删改**：其对钉点 ca67c8699 之成立性经 L2-RECALC-WINDOW-01 §U-20-A 复算逐字符核验（3/3 一致），历史证面有效；失效的仅是「以该钉指称现行包体」的钉外引用。

## 三、追加新条目：现行 HEAD 树状态登记（三样命令实跑摘要，2026-10-23T15:05Z 本会话实测）

1. `git rev-parse HEAD` →
```
09253a4e06f12eec90ddd7f69318878bd3ac4b35
```
（批六 HEAD；`git log --oneline -1` 题：EXT-WAVE-18 saturation batch-6 close: FSL v48）

2. `git rev-parse HEAD^{tree}` →
```
33ec6476f07aefbab4af49f0cc22ce96794e5915
```
子树钉：`git rev-parse HEAD:library/ns` → `1e4abd7d4d73afaacfdeb0c50cede5ee023c6da0`（≠ 原登记树钉 eb5b89cfc81ced6f097fa392bc34d085547648d3，漂移确证）。

3. `git log --oneline ca67c869988a2123937c5d696b746399703becdf..HEAD --stat` 尾部摘要：
```
区间共 58 提交（ca67c8699..09253a4e0）；触及 library/ns 者 10 提交。
git diff --stat ca67c8699 HEAD -- library/ns：
 library/ns/NsGalerkin.lean                |    5 +
 library/ns/NsGalerkin/AbsorbingBall.lean  |  320 +++++
 library/ns/NsGalerkin/Basic.lean          |  101 ++
 library/ns/NsGalerkin/CondUniqueness.lean |  307 +++++
 library/ns/NsGalerkin/Ladyzhenskaya.lean  | 2024 +++++++++++++++++++++++++++++
 library/ns/NsGalerkin/Lorenz96.lean       |  408 ++++++
 library/ns/NsGalerkin/OpenDomain.lean     |  216 +++
 library/ns/NsGalerkin/SkewB.lean          |   34 +
 8 files changed, 3415 insertions(+)
```
包体规模：NsGalerkin 源文件 9 → 14（新增 AbsorbingBall/CondUniqueness/Ladyzhenskaya/Lorenz96/OpenDomain 五件）；与 L2-RECALC-WINDOW-01 §U-20-D 登记值（+3415 行、8 files changed）逐字符相符。

## 四、漂移定性
**非篡改、非事故。** 漂移系本地源提交未同步所致的正常演进：`board/ADJUD-20261023-01.md` 裁决（b）已查明「本地独有 47 commits 全为源提交」（裁决时点计数；本登记实测 ca67c8699..HEAD 区间 58 提交，批五/批六续增），并经裁决 b-1 裁定「采 merge 并轨为本轮及默认形态」、裁决 b-4 裁定「联邦公域 pulse 链允许 merge 泡（非线性历史）；钉稳定性优先于历史线性」。即：漂移=登记后正常演进+同步未落地，非任何完整性事件。

## 五、义务登记
- 本件仅登记**本地仓现行 HEAD**（09253a4e0）树状态；不构成对 registry 原条目之修改（registry 侧 append-only corrigendum 另行办理）。
- **再登记义务**：merge 执行（ADJUD-20261023-01 钩 B2，按 b-3 窗口判据执行一次 merge+push [skip ci]）落地后，远端 head 前进，本席须就新 head 再追加一次重登记（同体例，原钉不动），并随钩 B3 首批续扫逐项核验钉可达性。
- 引用纪律钉：自本登记起，凡指称「当前包体」者一律引本件 HEAD 钉（09253a4e0 / tree 33ec6476f / library/ns 子树 1e4abd7d4）；凡指称 PAL-0003 原始证面者仍引 ca67c8699 / eb5b89cfc。名值分离，两钉并存，互不顶替。

——QF-OS 联邦 W3 登记席 · EXT-WAVE-19 批七·严格化线 · 2026-10-23T15:05:55Z
