CLASSIFY: L1
# B1-STAGING-REBUILD-20261027-01 · .ltar staging 重建实录 + 并入窗 10-30 核勾表预置(批二十九 / EXT-WAVE-41 S3)

PIVOT-01 B1 基础设施席 · 2026-10-27T07:52Z–08:13Z · 只交付不入库 · 名值分离 · 覆写权归原线

## 一、staging 重建实录(结论:**成功,零异常,确定性复现**)

| 时刻(UTC) | 步骤 | 读数/证据 |
|---|---|---|
| 07:52:39Z | 勘察:/tmp、HOME、staging 全损(整区抹除型第六起后遗);git 镜像/zstandard 同殉 | `ls` 原文在案 |
| 07:53–07:57Z | 三路并行:git ghfast 镜像重配;zstandard 0.25.0(清华镜像);lean-4.35.0 tarball 594,481,375 B(ghfast 续传);mathlib 浅取 @56a00585(ghfast+HTTP/1.1) | tarball sha256 前16 `7289597a44543246`(三轮同值,与 FSL 台账吻合) |
| 07:57Z | 工具链解压 22.8s;`Lean (version 4.35.0, …, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)`;mathlib lean-toolchain = v4.35.0 钉对复核 | lean --version 原文 |
| 07:58:34Z–08:03Z | `lake exe cache get`(XDG_CACHE_HOME=/tmp/xdg):起步降级(16KB/s,0.65 件/s,曾备 P48 预取预案),~1min 后自愈至 ~70 件/s;**9031/9031 (100%),CACHE_RC=0**,未触发预案、零重试 | /tmp/mlib-cache.log |
| 08:04:39Z–08:04:53Z | 分片推送(shard-0/1/2 = 3375/3328/2328,与批十八分布全同):**done=9031 skip=0 fail=0,14s**——直写式(copyfile)绕开 rsync temp+rename 蒸发面(批十八经验) | /tmp/shard-push.log |
| 08:05–08:09Z | portal 读回生成 MANIFEST.sha256(9031 行「sha256 路径 字节数」+ TOTAL 行,203s) | files=9031 bytes=455355304 |
| 08:10Z | **双向对拍**:portal 读回哈希集 vs lake 校验源哈希集 逐件一致 **9031/9031** | diff 空 |
| 08:11Z | manifest 落区 `/mnt/agents/output/ltar-staging/MANIFEST.sha256`;自 sha256 = `595d03f3e7700d3f11bf0d839f5ec507817f3213f0adf803c841b4cd31cc8534`——**与批十八 manifest 逐字节同值**,两轮独立重建确定性复现之铁证 | 见下总账 |
| 08:13:10Z | 沉降复核(90s 后):三分片计数无波动,无蒸发/异常 | ls 计数 |

**总账行**:件数 **9031**;总字节(逐件精算)**455,355,304 B**(与批十八精算全同;批十七 du 口径 455,826,344 B 之 0.10% 差为 du 目录项/块分配语义,以 manifest 精算为准);manifest 自身 sha256 **595d03f3e7700d3f11bf0d839f5ec507817f3213f0adf803c841b4cd31cc8534**。
**staging 路径**:`/mnt/agents/output/ltar-staging/mathlib/{shard-0,shard-1,shard-2}/` + `MANIFEST.sha256`。
**与既有盘点一致性**:件数三轮一致(9031);字节两轮精算一致(455,355,304);manifest 哈希两轮一致(595d03f3…)。
**异常**:零(本轮未遇抹除/封顶/写入失败;零重试缠斗纪律未被触发)。
**遗留风险登记**:staging 区已历一次整区抹失(批二十八复核在案);打包/Release/上传仍待 orchestrator——若 10-30 窗内不执行,本 staging 再次暴露于抹除面;重建成本实测 **21min**(07:52→08:13,优于在案估值 ~15min 量级)。

## 二、并入窗 10-30 核勾表预置(沿 B1-REDUCE-ABSORB-20261027-01 §二)

| 项 | 吸收形态 | 目标载体 | 核勾口径 | 状态(预置) |
|---|---|---|---|---|
| R-1 | 桥接句 | v2.1 条款六状态机段 / 生效时补注行 | grep 命中「＝本机之「未准」态」 | ☐ 待墓碑稿线成稿后核勾 |
| R-2 | 批界计次钉文 | v2.1 条款六保鲜闸段 | grep 命中「按 FSL 批收口条计次」 | ☐ 同上 |
| R-3 | 路径钉+格式限定 | v2.1 条款一 A1 + §1.1 git_blob 行 | grep 命中「自历史树取」且「限 git 默认 SHA-1 对象格式」 | ☐ 同上 |
| R-4 | 名级化 | v2.1 条款三 C5 + §7.1 第四行 | grep 命中 `${REMOTE}/${MAINBRANCH}` 且定值登记在案 | ☐ 同上 |
| 复裁链 | — | 判定席复裁件 | 复裁件名落账 | ☐ 待判定席 |

## 三、销记轨随载更新(一行一件,as-of 08:13Z)

| 事项 | 状态 |
|---|---|
| .ltar 归档(R2B-16③) | **staging 重建完成(本件)**,9031/455,355,304/manifest 595d03f3…;打包/Release/上传仍待 orchestrator,窗 10-30 前敞口在案 |
| 周期 fetch「准设立」备批(窗批二十八收口前) | 批二十八窗已过——**未见开庭登记之件入我视野**,随备材料在案;转「待枢确认庭期/顺延」态 |
| 「设计意图归属」开放项 | 状态钉「根因未定位」;核查点①(KICK.md/poller.py 修订史)续结批三十 |
| weave/pulse / 3999 封顶 / 蒸发修复 | 无新变化(weave/pulse 仍钉 3999);FINDING 待入册 |
| PAL-0003 / fsck 条款 / rc=124 草案 | 结转中,无变化 |
| 批十三 sparse NO-GO、批十五 REDUCE | REDUCE 已入并入轨(本件 §二);sparse 案仍待裁决 |

—— PIVOT-01 B1 基础设施席 · 批二十九(EXT-WAVE-41 S3) · 2026-10-27 · 只交付不入库
