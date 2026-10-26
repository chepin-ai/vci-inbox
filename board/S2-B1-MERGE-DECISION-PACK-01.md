CLASSIFY: L1
# S2-B1-MERGE-DECISION-PACK-01 · B-1（m1-b1-baseline.yml）合并判定包（EXT-WAVE-38 批二十六）——DRAFT-03 评审稿 → 合并裁决备料，本席不合并

- 席别：QF-OS 联邦批二十六 EXT-WAVE-38 B-1 合并判定包制备席（W11 线续）
- 成文时刻（date -u 实测）：**2026-10-26T15:35Z** 起成文（UTC(Z) 单时钟域；距 11-03 预飞闸约 7.7 日，合并判定须在该闸前完成）
- 客体件：`board/WSH-S2-BLOCKER-DRAFT-03.md`（下称「DRAFT-03」，攻扫维 1 全修版；其内嵌 `.github/workflows/m1-b1-baseline.yml` 草案 v3 全文）
- 谱系：DRAFT-01（B-1/B-2/B-3 三阻塞草案）→ DRAFT-02（W2-P0-09 九项必修返修）→ DRAFT-03（ATTACK-SCAN 维 1 八项返修）；三版均 append-only 在案
- 纪律：只交付不入库（本件为唯一新建件，零 git、不触 `.github/` 实体，合并权归 orchestrator＋判定席）；名值分离（gh_pat 仅名引用零落值）；不编数；甲席席规（零工时数值）；**红区存续合规：本件制备全程零 api.github.com 调用**，所引 API 实测均为 10-26 在案记录

---

## 一、8/8 修复逐项验证证据表

| # | 修复项 | 文本落位（DRAFT-03） | 验证证据 | 证据强度 |
|---|---|---|---|---|
| 1 | **P0-1** artifact 名参数化 | §一 Upload 步 `name: m1-b1-comparator-run-<mode>-<run_id>-a<attempt>`；§二 A1.3/A4.1 同步修订 | YAML 解析校验通过（artifact name 字段含三段参数位）；同名 409 之外部实证照录攻击件（upload-artifact v4 工件不可变，MIGRATION.md＋两案例 URL 在案） | 文本＋外部实证；**残留：11-03 空转窗原地 re-run 实证（§三 P-4）** |
| 2 | **P0-2** concurrency 组＋nonce 幂等 | §一 `concurrency: {group: m1-b1-baseline, cancel-in-progress: false}`；inputs 增 nonce（string, required）；Verdict 步 `env: NONCE` 绑定；§2.3 脚本 v3 窗内 run 数＝1 断言 | YAML 解析校验：concurrency 块、inputs=[mode, nonce]、verdict env={NONCE, MODE_V} 全确认；nonce 经 env 绑定非内联（维 1 通例合规） | 文本＋结构校验；**残留：cancel-in-progress 语义裁定待 orchestrator 确认（建议 false 在案）** |
| 3 | **A1-3** actions/* 全钉 SHA | checkout@`11d5960a326750d5838078e36cf38b85af677262`、upload-artifact@`ea165f8d65b6e75b540449e92b4886f43607fa02`（注释标 v4） | 两 SHA 均 2026-10-26 经 api.github.com git/ref/tags/v4 实测解得（红区前记录，DRAFT-03 F-1/F-2） | 实测钉 |
| 4 | **A1-4** persist-credentials: false | §一 checkout 步 `with: persist-credentials: false`；Comparator 步注释挂「沙箱内网络命名空间隔离」子项入第十一钉③ | YAML 解析校验确认 with 块在位；本 workflow 无 git 写操作（零成本声明经全文 grep 无 git 写命令佐证） | 文本＋结构校验 |
| 5 | **A1-5** 回显消毒 | Verdict 步 MISMATCH 回显 `printf '%q'`；STEP_SUMMARY 改 `cat -v` | v2 轮本机实测：伪造日志两例（尾部注入／okay 后注入）经物理末行取值均 fail-closed 致红；消毒路径 shell 语法核验 | 本机实测（DRAFT-02 轮） |
| 6 | **A1-6** pip --require-hashes | §三 CI 片段 v3＋`ci/schema/cjs-requirements.txt` 钉版全文（15 件依赖 15 枚 sha256） | 15 件 wheel 本机逐一 sha256 实测落钉；`pip install --require-hashes --no-deps --dry-run` **rc=0** 验证通过；**平台边界 F-4 登记**：三件 cp312 wheel，runner python≠3.12 须重生成 | 本机实测＋边界登记 |
| 7 | **A1-7** dispatch 主体钉 | §二 A2.1 升格生效前置三要素（主体＝orchestrator/执行席持票；凭证名 gh_pat；登记行格式成文） | 文本落位；仓侧 write 权清单（名级）登记动作在 orchestrator 侧 | 文本；**残留：仓侧清单登记（§三 P-8）** |
| 8 | **A2-3** verdict.txt 自报字段 | verdict.txt 增 `nonce:` 行；下载后 nonce 逐字对拍（§2.3 末拍） | 随 #2 nonce 绑定消解（攻击件原文口径「不独立成险、随 A1-2 修复自动消解」照录） | 文本＋联动消解 |

**合计：8/8 文本层落地＋可机验项全部机验通过**；留实证义务两项（re-run 实证、cancel 语义确认）入 §三前置条件，不隐不吞。

---

## 二、残余风险登记（合并后存续面，全部如实）

| # | 残余风险 | 严重度 | 缓解/去向 |
|---|---|---|---|
| RR-1 | **第十一钉未实证四项**：comparator config 精确内容／rejected 出口码值／runner bwrap-userns（含网络隔离子项）／leanexport 目标名——草案 Export/Comparator 两步为**占位形态** | **高（硬前置）** | W2-P0-09⑦在案：11-03 前实证落钉，禁以未实证形态空转充四要件实证；未落则 B-1 不闭合 |
| RR-2 | cache 命中哨兵正则（`Downloaded|unpacking`）目标格式未在案实证——fail-closed 设计下格式漂移即红（不误绿，但会挤占唯一重试预算） | 中 | 11-03 空转首项实证 cache.log 实际格式后校订正则（§三 P-5） |
| RR-3 | `timeout-minutes: 170`／build 上界 1800s 为建议值，终值 orchestrator 未定 | 中 | 合并判定包呈裁点：数值裁定随合并一并落 |
| RR-4 | F-4 平台边界：cjs-requirements.txt 哈希集钉于 cp312/manylinux；runner python 版本漂移即失效 | 中 | 合并前检查单增列「runner python3 --version 对拍＝3.12 或重生成哈希集」（§三 P-6） |
| RR-5 | org/repo artifact retention 策略上限未实测，retention-days: 90 系请求值可能被静默钳制（GOS2 §7②在案） | 中 | org 设置查询须 orchestrator 权限，列入其合入前检查单；实测值与请求值名值分列入回填登记 |
| RR-6 | v0.5 schema 偏移未裁——验证 2 信任根合法性悬置（详 `board/V05-SCHEMA-ADJUD-BRIEF-01.md`） | **高（判定依赖）** | 11-03 庭期裁断（§三 P-7）；建议选项甲-1＋丙触发器在案备采 |
| RR-7 | 维 2 A2-2 同 runner 自签自证环未修（attestation 阶梯涉权限变更，与最小权限钉冲突） | 中（呈裁结转） | 判定席裁量；最小改动级（独立通道登记哈希）可先落地 |
| RR-8 | 桩 comparator 不伪绿／伪造日志取值两实证在本机 shell 级已过（v2 轮），**CI 环境复证未跑** | 低 | §五合并后验证计划 T-2/T-3 |

---

## 三、合并前置条件清单（全部通过方可合并；逐项带验收口径）

| # | 前置条件 | 验收口径 | 责任 |
|---|---|---|---|
| P-1 | **预检闸 rc 绿**：ci/schema/ 钉版 v0.4 副本创建（orchestrator 权）＋对现行 formalization.yaml `check-jsonschema` rc=0 | 副本 sha256 复算＝`25ff6b25…ce`；闸 rc=0 留痕 | orchestrator |
| P-2 | **并发组在位确认**：合并后 workflow 文件含 `concurrency: group: m1-b1-baseline, cancel-in-progress: false`（或 orchestrator 裁定之他值并登记） | 合并后 grep 核验行在案 | orchestrator |
| P-3 | **nonce 绑定链路通**：dry-run dispatch 携 nonce N1 → verdict.txt 含 `nonce: N1` 逐字 | 空转产物下载对拍 | 执行席＋orchestrator |
| P-4 | **artifact 名参数化回归测试**：①dry-run dispatch（attempt=1）→ 枚举 artifacts 见 `…-dryrun-<run_id>-a1`；②**原地 re-run**（attempt=2）→ 见 `…-a2` 且 **a1 仍存、无 409**；③下载键按 A1.3 参数化形态解析成功 | 三断言全过留痕（API 枚举清单存档）；本条同时清偿 GOS2 §7① 实证义务 | 执行席 |
| P-5 | cache 哨兵正则校订＋人为 cache miss 实证 rc 行为（W2-P0-09⑤在案窗） | 空转窗内完成，miss 情形转红实证 | 执行席 |
| P-6 | runner `python3 --version` 对拍 3.12，否则以 runner 平台重生成 cjs-requirements.txt 哈希集并复钉 | 版本行留痕／新哈希集 dry-run rc=0 | orchestrator |
| P-7 | **v0.5 schema 偏移庭裁落地**（联动 `board/V05-SCHEMA-ADJUD-BRIEF-01.md` §四议程） | 裁定文在案；验证 2 信任根口径按裁定落位 | 判定席 |
| P-8 | 仓侧 write 权清单（名级）随批收口登记；dispatch 主体钉三要素生效 | 登记行落板 | orchestrator |
| P-9 | elan-init.sh sha256 复钉（上游可变，合并当次复测） | 复测值与 ELAN_INIT_SHA256 钉对拍，异即更新并登记双侧值 | 执行席 |
| P-10 | WF_ID 落钉：合并后经 workflows 清单实测 m1-b1-baseline 之 workflow id，回填取值脚本 v3 占位 | id 值落板（名值分列） | 执行席（红区解除后或经判定席特许通道） |

---

## 四、回滚路径

| 情形 | 回滚动作 | 数据面 |
|---|---|---|
| R-α 合并后空转暴露结构性失败（RR-1 实证否定占位形态／P-4 回归不过） | **单文件回滚**：revert 合并提交或删除 `.github/workflows/m1-b1-baseline.yml`（git 操作权属 orchestrator）；B-1 回退未闭合态如实登记，不产生伪闭合 | 空转 artifact（`-dryrun` 后缀）保留备查、不回填、不注册——append-only 语义下零擦除需求 |
| R-β 正式跑批后需回滚 | workflow 文件同上回滚；**formal 工件与 verdict.txt 不删**（证据面 append-only）；注册表指针若已填则加作废注记行（禁改原行） | machine_checks[] 若已回填：禁删条目，加更正条目 append（字段级作废注记），沿 RULING-01 append-only 纪律 |
| R-γ 供应链面触发（elan 哈希不匹配／action SHA 漂移检出） | 立即冻结 dispatch 面（concurrency 组自然阻塞新跑），回滚同 R-α；事件沿跳闸线申报路径呈 | — |

**回滚成本定性**：全路径均为单文件/注记级动作，无状态迁移，无跨仓耦合；回滚不触碰任何既有实证记录。

---

## 五、合并后验证计划（11-03 空转窗 → 11-04 执行日）

| # | 时点 | 验证动作 | 通过判据 |
|---|---|---|---|
| T-1 | 合并后即 | P-1/P-2/P-6/P-10 四项静态核验 | 各 rc/grep/对拍行留痕 |
| T-2 | 11-03 空转① | 桩 comparator（exit 3）dry-run——伪绿通道封堵 CI 复证（W2-P0-09 验收①） | run 红、无 artifact 或 artifact 无 verdict.txt（分支丙口径可识别） |
| T-3 | 11-03 空转② | 伪造日志构造（rejected 行＋尾部注入行）取值段测试（W2-P0-09 验收②） | Verdict 步红、verdict.txt 不产 accepted |
| T-4 | 11-03 空转③ | 全要素 dry-run（含 comparator 实跑——RR-1 实证后形态）＋cache miss 人为制造（P-5）＋原地 re-run（P-4） | 四要件实证齐；miss 即红；a1/a2 双工件无 409 |
| T-5 | 11-03 闸前 | B-1/B-2/B-3 闭合证验汇总＋HEAD 滞后核验先行（修-3 在案） | 闸前复检行落板 |
| T-6 | 11-04 执行日 | formal 跑批→验证 0/1/2/3/4/5/6/7 全项（验证 0/6/7 为 DRAFT-02/03 增列） | 八项验证全过留痕，回填 append-only 落账 |

---

## 六、合规自检（本件行文）

1. **首行 CLASSIFY: L1**；gh_pat 仅名引用零落值；日期全绝对 UTC(Z)。
2. **不编数**：SHA 两枚／15 件哈希／rc 值／HTTP 状态均引 DRAFT-02/03 在案实测或本件明注之在案记录；本件零新外联（红区合规：零 api.github.com 调用）。
3. **如实登记**：RR-1~RR-8 残余风险全列（含两项「高」）；P-1~P-10 前置条件未满足项不因本件成文而销记。
4. **甲席席规**：零工时/产能数值；RR-3 数值裁定权、P-7 裁断权、合并权逐处载明归属。
5. **权限边界**：本件为唯一新建件；未触 `.github/` 实体、零 git；覆写权归原线；本包只备料不合并。
6. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** 合并前全部机验均为必要条件证据；B-1 闭合判定须经独立复核与判定席裁决。

—— QF-OS 联邦批二十六 EXT-WAVE-38 B-1 合并判定包制备席 · 枢/PIVOT-01 体系 · 2026-10-26 · 合并判定死线 2026-11-03 预飞闸前
