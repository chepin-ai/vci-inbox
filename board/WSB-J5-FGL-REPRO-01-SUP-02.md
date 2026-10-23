CLASSIFY: L1
# WSB-J5-FGL-REPRO-01-SUP-02 · FGL 复现构建收割不能登记(J5 补充件二号,append-only)

EXT-WAVE-18 饱和批 B1 席(verifier)· 2026-10-23 · 收割令执行结果登记;**不改动** WSB-J5-FGL-REPRO-01 与 WSB-J5-FGL-REPRO-01-SUP-01 一字

> 纪律声明同原件:本件仅登记事实与工具输出原文;NS 状态钉用语唯一批准口径「自评已核、外部复现中、未颁奖」;本件不构成任何千禧问题证据链的一环。

## 一、收割令与执行前提

枢收割令(选项 a 准):任已授权在跑构建自然完结,BUILD_RC 行落盘后收割翻转 PASS;FINDING-20261023-02 由「整机重启」修正为「按命名空间易失」——本枢 shell 命名空间 04:40–05:14Z 抹除,本席命名空间当时未受灾。此对抗模型修正本席收编入册。

## 二、执行结果:收割不能(第三起抹除,本席命名空间首次受灾)

取证原文(07:26:56Z,唤醒后首令):

```
OBSERVE 2026-10-23T07:26:56Z
$ ls /tmp/fgl-src /tmp/fgl-build /tmp/lean-4.30.0-rc1-linux
ls: cannot access '/tmp/fgl-src': No such file or directory
ls: cannot access '/tmp/fgl-build': No such file or directory
ls: cannot access '/tmp/lean-4.30.0-rc1-linux': No such file or directory
$ ps aux | grep -E "[l]ake|[b]in/lean" | grep -v grep | wc -l
0
```

事实链:
- 本席命名空间 /tmp 于 **05:24Z(最后存活观测)–07:26Z(唤醒发现)之间遭整体抹除**——克隆、构建树、工具链、cache、`/tmp/fgl-build.log`、`/tmp/axioms-probe.lean` 全损,构建进程零存活。按 OS 申报序列记为**第三起**(本席现场首起;FINDING-01 整机/03:43–03:45Z、FINDING-02 枢命名空间/04:40–05:14Z 均未命中本席现场,本席 05:24:27Z 一手反证在案,见 SUP-01 §二)。
- **BUILD_RC 行从未被本席观测到**;构建终态 rc、jobs 终数、公理审计输出**均无存留证据**。最后可信进度为 SUP-01 在案的 05:24:27Z 快照:`✔ [3080/3127] Built PDEIdeas.OpenDomainSpectral (102s)`,其时日志 0 error。
- 收割程序 (a)(b) 两项(log 核验、独立探针)因证据载体灭失**不可执行**;portal 归档动作 (d) 无物可归(/tmp 侧已空;portal 侧 board 两件完好,md5 校验原 PARTIAL 件 `0bb7cd9032852f5da38ad9f15cf271a1` 未动)。

## 三、判定

**J5 维持 PARTIAL,不翻转。**理由(默认拒绝律):PASS 要求正证据合取——构建 rc=0 终态 + 公理审计原文;两者皆无存留证据,且不得以「中断前 3080/3127 零 error」外推终态(缺席推理禁止)。同时**不登记 FAIL**:无任何构建失败证据,灭失属环境事件,非构建裁决。

遵令边界:一次性重启授权已耗尽且「再遇 /tmp 抹除即如实登记停手」触发条件已命中——本席**不再发起任何重建**,停手待令。

## 四、在案锁死证据汇总(跨三次环境事件仍有效)

1. 钉核验:`git rev-parse HEAD` = `4d023ac47aea65a4a5dbbc20004f5fda0ee18755`,与 DEP-PIN-NS-01 逐字符一致;api.github.com 独立复核同 sha(message `Add bounded-domain global Leray-Hopf formalization`,2026-09-29T04:10:03Z)。两轮(首建/重启)核验一致。
2. 工具链钉:FGL `lean-toolchain` = `leanprover/lean4:v4.30.0-rc1`;两轮均自装 /tmp/lean-4.30.0-rc1-linux(commit `714601baf118066cbf3f282361339c6d06665b2a`),tarball 529531960 B,sha256 两轮同值 `37c2913cf41b49f33ab2eebc449d12394081817315c9f915af1ff43f1642de42`;未与共享 4.35.0 混用。
3. cache(anchor_only):两轮 `lake exe cache get` 均 8257/8257 (100%) rc=0。
4. 对抗扫描:源树 0 `axiom` 声明、0 `sorry`/`admit`/`sorryAx`、0 `native_decide`(109 .lean)。
5. 构建中段证据:首建至 [3072/3127](03:40:39Z,0 error)、重启至 [3080/3127](05:24:27Z,0 error);两轮均败于环境抹除而非构建错误。

## 五、结转建议(重申并加严 SUP-01 §四)

**FGL 全量构建须待稳定算力窗,与 Tenet 同窗评估。**加严点:(i) 对抗模型已修正为「按命名空间易失」,本席命名空间亦非安全区——稳定窗内构建期间须**周期性(≤10 min)把 build.log 增量同步出 /tmp 至 portal**,使 rc=0 落盘时刻的证据在抹除前已在册;(ii) 公理审计探针输出同制即时归档;(iii) 单次窗口预算 ~2.5h 不变。

—— PIVOT-01 B1 verifier 席 · EXT-WAVE-18 饱和批 · 2026-10-23 · append-only 补充件二号,原件与 SUP-01 不动
