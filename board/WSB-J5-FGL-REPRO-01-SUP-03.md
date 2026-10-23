CLASSIFY: L1
# WSB-J5-FGL-REPRO-01-SUP-03 · FGL 复现构建批七稳定窗再试登记(J5 补充件三号,append-only)

EXT-WAVE-19 · B1 席(verifier)· 2026-10-23 · **结局:窗口耗尽 PARTIAL(带进度与日志证据钉)**;不改动 WSB-J5-FGL-REPRO-01 / SUP-01 / SUP-02 一字

> 纪律:默认否认——无 rc=0 证据不翻 PASS;NS 状态钉用语唯一批准口径「自评已核、外部复现中、未颁奖」;本件不构成任何千禧问题证据链的一环。

## 一、本轮指令与硬化规则执行登记

枢批七令:勘察命名空间→重建→**build.log ≤10min 增量同步出 /tmp 至 /mnt/agents/output/fgl-build-log/**(tail -5000 级增量,失败重试一次,不停 build)→ BUILD_RC 落盘 BUILD_RC.txt(rc + 末行 job 号 + UTC 时间戳)→ 3.5h 窗口(14:57Z–18:27Z)耗尽即按当时进度登记 PARTIAL。

硬化规则执行实录:
- 勘察(15:03:33Z):命名空间已被第四起抹除清空(fgl-src/lean-4.30.0-rc1-linux 均 `No such file or directory`;zstandard、git insteadOf 配置同殉)——全部按已验证协议重建。
- 同步守护:自建增量守护(/tmp/fgl-sync-daemon.sh),300s 周期 dd 增量追加 + `tr '\r' '\n'`,portal 目标 `/mnt/agents/output/fgl-build-log/build-live.log`;检到 `BUILD_RC=` 自动写 `BUILD_RC.txt` 并归档 tail-5000 全量尾段。守护存活至本件成文时。
- 反脆弱补强(本轮新增,前两轮未有):构建期 **17:58Z 与 18:17Z 两次人工全尾快照**落 portal(build-snapshot-1758Z.log / build-snapshot-final.log),守护之外的双保险。

## 二、重建与构建时间线(UTC 2026-10-23)

| 时刻 | 事件 | 证据 |
|---|---|---|
| 15:03Z | 勘察:命名空间已被擦(第四起),开工重建 | `ls` 原文在案 |
| 15:06Z | 重克隆 + checkout + rev-parse 复核 | `4d023ac47aea65a4a5dbbc20004f5fda0ee18755`,三轮钉核验一致 |
| 15:14Z | zstandard 复装(pypi 官方源 ReadTimeout,改清华镜像成功,0.25.0) | /tmp/pip-zstd.log |
| 15:32Z | 工具链 tarball 三轮下载完成(529531960 B;本轮网速 ~0.3MB/s,耗时 ~28min) | sha256 `37c2913cf41b49f33ab2eebc449d12394081817315c9f915af1ff43f1642de42`(**三轮同值**) |
| 15:33Z | 解压 22.4s;`Lean (version 4.30.0-rc1, x86_64-unknown-linux-gnu, commit 714601baf118066cbf3f282361339c6d06665b2a, Release)` | lean --version 原文 |
| 15:29Z | mathlib4 预克隆至钉 rev 8d6f23e(与 tarball 下载并行,抢回 ~10min) | MATHLIB_READY |
| 15:34–15:52Z | `lake exe cache get`:首趟 8250/8257 后 7 件挂死(日志 mtime 冻结 8min)→ 按失速预案杀进程重跑,增量 3/3,**CACHE_RC=0**;三轮 cache 均 8257/8257 rc=0 | /mnt/agents/output/fgl-build-log/cache-get.log(portal 已归档) |
| 15:54:26Z | `lake build` 启动(Lake 5.0.0 无 -j,2 核默认并行=2,等效 j2) | /tmp/fgl-build.log |
| 18:17:12Z | **窗口决算点快照** | 见 §三 |

## 三、决算点证据原文(18:17:12Z)

```
✔ [3094/3127] Built PDEIdeas.OpenDomainTimeCompactness (746s)
```

- 进度:**3094/3127 jobs(98.9%)**;PDEIdeas 源模块完成 68 个(✔ 计数),尾段 OpenDomain* 重模块群在编(单件实测 400–1513s)。
- **全程 0 error**(grep -ciE "error" = 0,18:17Z 全量日志)。
- 构建未完结:`BUILD_RC` 行未落盘。估余 33 jobs、双并发、尾段均重 → 自然完结约需 +90min(ETA ~19:45–20:00Z),越窗。
- 证据钉(portal,/mnt/agents/output/fgl-build-log/):`cache-get.log`(159189 B)、`build-live.log`(守护增量,4709+ B)、`build-snapshot-1758Z.log`、`build-snapshot-final.log`(tail-5000 全尾,含 68 件 ✔ 明细)。

## 四、判定

**J5 维持 PARTIAL(窗口耗尽),不翻 PASS 亦不登 FAIL。**
- 未翻 PASS:rc=0 终态与 5 主定理 #print axioms 原文均未产出(探针 /tmp/axioms-probe.lean 已备,未及运行);默认否认律执行。
- 不登 FAIL:三轮构建累计证据(3072/3127、3080/3127、3094/3127,全部 0 error)无任何构建失败信号;受阻因皆为环境(抹除×3 命中现场/窗口),非 FGL 内容。
- 三轮独立尝试的可复现实证:**钉复核三轮一致、工具链 sha256 三轮同值、cache 三轮 8257/8257 rc=0、构建稳定推进至 ≥98.9% 零错误**——环境等价与可构建性的旁证强度已达三轮独立复现级。

## 五、在跑余烬与翻转路径(如实登记)

按令「不得因此停 build」:构建进程与同步守护**保留续跑**(本席成文时存活,3094/3127 推进中)。若自然完结,守护将自动落 `BUILD_RC.txt`(rc + 末行 job + UTC)与 `build-final-tail5000.log` 至 portal——届时唤醒本席即可核验收割、跑探针、成文 SUP-04 翻转 GREEN;若再度被擦,portal 现有快照即终局证据,本席不再重建(一次性授权语义已三轮耗尽,须枢新令)。

## 六、结转建议(三轮数据支撑)

FGL 全量构建实测墙钟:cache 后全量 build ≥ 145min 未竟(尾段 OpenDomain* 单件最高 1513s)。建议稳定窗预算由 3.5h 提至 **≥4.5h**(重建 30min + cache 20min + build 180min + 探针/成文 20min),或将「构建起始点」前移至稳定窗开启时刻;同步守护(300s 增量)与双快照机制本轮验证有效,建议固化为 J5 标准作业。

—— PIVOT-01 B1 verifier 席 · EXT-WAVE-19 批七 · 2026-10-23 · append-only 补充件三号
