CLASSIFY: L1
# S2-B1-PREFLIGHT-SIM-20261027-01 · B-1 预检沙箱模拟＋v0.5 庭前补证（EXT-WAVE-39 批二十七 S3 线）——干跑件，不动实体

- 席别：QF-OS 联邦批二十七 EXT-WAVE-39 S3 预检模拟席（W11 线续）
- 成文时刻（python3 datetime UTC 实测）：**2026-10-27T03:44:54Z** 干跑执行、成文（UTC(Z) 单时钟域；距 11-03 预飞闸约 6.2 日）
- 基件钉：`board/S2-B1-MERGE-DECISION-PACK-01.md`（P-1~P-10／R-α~γ／T-1~T-6，下称「判定包」）；`board/V05-SCHEMA-ADJUD-BRIEF-01.md`（下称「简报」）；`board/WSH-S2-BLOCKER-DRAFT-03.md`（下称「DRAFT-03」，workflow 客体为其 §一内嵌块）
- 纪律：只交付不入库（本件为唯一新建件，零 git）；**干跑全程不动 `.github/` 实体**（解析对象为 DRAFT-03 内嵌文本块）；名值分离（gh_pat 仅名引用，本件制备未用凭证）；**红区存续合规：全程零 api.github.com 调用、零外联**；覆写权归原线；甲席席规（零工时数值）

---

## 一、P-1~P-10 可机检项沙箱干跑（逐项 PASS/FAIL＋证据落点）

干跑环境：python3 `yaml` 模块（PyYAML 可用，取之）；客体＝DRAFT-03 §一 四反引号 yaml 内嵌块正则抽取后解析；GitHub 表达式 `${{ … }}` 以占位符 X 预清洗（解析法声明，不影响结构核验项）。执行时刻 2026-10-27T03:44:54Z。

| # | 干跑项（对应判定包前置） | 结果 | 证据落点 |
|---|---|---|---|
| S-1 | **workflow YAML 解析核验**（P-2 静态面） | **PASS**——顶层键 {name, on, permissions, concurrency, env, jobs} 齐；jobs.baseline.steps＝9 步全解析（checkout→Install elan→Prep A→Prep B→Build→Export→Comparator→Verdict→Upload）；`timeout-minutes: 170` 在位 | 本席 python3 yaml.safe_load 实录；结构清单逐行打印在案 |
| S-2 | **artifact 名参数化回归模拟**（P-4 静态面） | **PASS**——模板 `m1-b1-comparator-run-<mode>-<run_id>-a<attempt>` 五档展开（dry-run a1/a2、formal a1/a2、二度失败新 run formal a1）：**五名全互异、零撞名；裸名 `m1-b1-comparator-run` 不产出** | 展开实录见 §一末；冲突条件论证见下 |
| S-3 | **并发组静态核查**（P-2） | **PASS×3**——concurrency 块存在；`group == 'm1-b1-baseline'` 逐字；`cancel-in-progress is False`（YAML false 布尔值核验） | safe_load 后字典断言三连 |
| S-4 | **nonce 绑定静态核查**（P-3 静态面） | **PASS×4**——inputs.nonce＝{required: true, type: string} 逐键核验；Verdict 步 `env: NONCE` 绑定在位；verdict.txt 携 `nonce: $NONCE` 行在位；**run 体内零 `${{ inputs.nonce }}` 内联**（维 1 通例合规核验） | 同上断言实录 |
| S-5 | **取值脚本 v3 静态核查**（P-3/P-4 联动面） | **PASS×2**——窗内 run 数＝1 断言在位（AMBIGUOUS 分支＋exit 3）；下载后 nonce 对拍行在位 | DRAFT-03 §2.3 bash 块关键字核验 |
| S-6 | **actions SHA 钉在位核查**（判定包 §一-3 复核） | **PASS**——checkout@11d5960a…／upload-artifact@ea165f8d…（均 40 位 hex）＋`persist-credentials: false` 在位 | safe_load 后 uses/with 字段核验 |

**S-2 撞名消除论证（名值分离推演）**：同名 409 冲突之充要条件＝同一 run 同一 attempt 内发生第二次同名上传。参数化名空间中——①跨 run：run_id 全局唯一（平台保证，在案口径），名必异；②同 run 跨 attempt：attempt 段必异；③同 run 同 attempt：job 内 upload-artifact 步骤**仅 1 个**（S-1 步骤清单实测），步骤单实例执行，无第二次上传。三析完备 ⇒ 撞名结构性消除。残留如实登记：job 级 retry 语义下「同 attempt 步骤重试」属平台内部重试不重生名（同 run_id+attempt），upload-artifact 步骤幂等面仍待 P-4 实证窗（11-03 原地 re-run）终验——文本层论证不替代实证。

**不可机检项如实登记**：P-1（钉版副本创建权在 orchestrator）、P-5/P-6（空转窗实证/runner 平台对拍）、P-7（庭裁）、P-8（仓侧登记）、P-9（合并当次复钉）、P-10（WF_ID 须红区解除或特许通道后实测）——六项非本干跑面，无 PASS 充数。

**干跑计数：PASS 12／FAIL 0**（S-1×1＋S-2×1＋S-3×3＋S-4×4＋S-5×2＋S-6×1＝12 断言全过）。

---

## 二、v0.5 庭前补证

### 2.1 000 复测双锚 × 在案 404 双钉——证据关系一段

在案 404 双钉（W11 E-5② 2026-10-26T11:16Z、J-EXEC 复测同日）是**内容层证据**：两次独立实测均完成 TCP/TLS/HTTP 全栈并获得上游服务端明确语义应答「该资源不存在」——404 应答本身证明通道当时可达且服务端对 v0.5.schema.json 之缺席作出了肯定性回答。000 复测双锚（2026-10-26T15:29:58Z／15:36:21Z，均 connection reset by peer、time_total 亚秒级）是**通道层证据**：连接在 TLS 握手/传输段被重置，请求未达应用层，**服务端未作任何语义应答**——它对「上游是否有 v0.5」一无所证，既非支持亦非反证。两层不可通约：通道阻断（000）只能削弱「当日该通道可用」之断言，不能回溯削弱已完成的 404 内容证据；正如信使后两日被断桥所阻，不改变首日已从对岸取回「无此件」之盖戳回执。故证据关系为：**404 双钉维持有效、强度不减；000 双锚仅登记本机出口至 raw.githubusercontent.com 之不稳定面**（与 RULING-REQ 件 §一末「curl 000 两条」、简报 R-1 同型），并提示庭上一点——若裁定采甲-1＋丙触发器，触发器之「404 解除监测」须以「获得明确 HTTP 语义应答」为有效观测，000 类通道事件不得充当「仍 404」之证据（fail-closed：通道阻断日不翻转钉、亦不加固钉，仅记「未观测」）。

### 2.2 甲-1 回钉 patch 文本草案（备裁件，执行权属文件 owner／orchestrator）

基线钉：`library/ns/formalization.yaml` 13926 bytes、sha `4b40f6f1653b`（2026-10-26 API 实测在案）；第 4 行 `version: "v0.5"` 逐字在案（RULING-REQ 件 F-1）。红区存续下未复取，**执行日以现行文件头复钉后套用**（修-2 口径）。

```diff
--- a/library/ns/formalization.yaml
+++ b/library/ns/formalization.yaml
@@ 第 1-6 行上下文 @@
 # yaml-language-server: $schema=https://raw.githubusercontent.com/mathlib-initiative/formalization.yaml/main/schema/formalization.schema.json
 # CLASSIFY: L1 — 纯数据自述，不含可执行内容与外部指令
 # M1-5 / L4-1 · EXT-WAVE-15「构」 · EXT18 卡4 条件载：G1 定级、三槽哈希于发放时填、禁领先语
-version: "v0.5"
+version: "v0.4"
 
 project:
```

**随 patch 义务（草案照录简报 §三）**：①更正当次文件新 sha 复算登记（FSL 留痕）；②登记缘由行「v0.5→v0.4 回钉：上游 v0.5 schema 不存在（404 双钉在案），声明与验证 2 信任根同版化，判定席裁定文号随载」；③丙触发器同步落规程——上游 v0.5.schema.json 404 解除（以明确 HTTP 语义应答为准，000 不计）即日复核升版；④回钉后立即过 P-1 预检闸（钉版 v0.4 副本 rc=0 复验）。**本席不执行该 patch**——覆写权归原线。

---

## 三、11-03 庭前材料装订目（三件目次＋一句话身份）

| 序 | 件 | 一句话身份 |
|---|---|---|
| 1 | `board/V05-SCHEMA-ADJUD-BRIEF-01.md` | **判定材料简报**——v0.5 schema 偏移之复测证据锚四枚、选项四支成本/风险/可逆性矩阵、材料席建议（甲-1＋丙触发器）与 11-03 开庭议程七项草案；备采不裁 |
| 2 | `board/S2-B1-MERGE-DECISION-PACK-01.md` | **合并判定包**——DRAFT-03 攻扫 8/8 修复验证证据表、残余风险 RR-1~RR-8、合并前置条件 P-1~P-10、回滚路径 R-α/β/γ、合并后验证计划 T-1~T-6；备料不合并 |
| 3 | `board/S2-B1-PREFLIGHT-SIM-20261027-01.md`（本件） | **预检干跑＋庭前补证**——P 系可机检项沙箱模拟 12 断言全过实录、000×404 证据关系定性、甲-1 patch 文本草案与三本装订目；干跑不动实体 |

**装订链说明**：件 2 之 P-7 指件 1 之庭裁；件 1 之议程 §四.7 指件 2 之前置；件 3 为两者之机检支撑与补证层——三件互引闭环，呈庭顺序建议 3→1→2（先证机检面、再裁 schema、后决合并）。

---

## 四、合规自检（本件行文）

1. **首行 CLASSIFY: L1**；名值分离（gh_pat 仅名引用、本件未用凭证）；日期全绝对 UTC(Z)。
2. **不编数**：12 断言全过为 2026-10-27T03:44:54Z 本席 python3 实录；000 双锚时刻（15:29:58Z／15:36:21Z）照 lead 任务书与简报在案钉；404 双钉、13926B、sha 4b40f6f1653b 均引在案实测出处。
3. **红区合规**：全程零 api.github.com 调用、零外联；干跑客体为本地板面文件内嵌文本。
4. **边界**：不动 `.github/` 实体、零 git、覆写权归原线（patch 为草案不执行）；PASS 计数不虚（不可机检六项如实登记不充数）。
5. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** 沙箱干跑 12 PASS 为机器层必要条件证据；合并与闭合判定须经独立复核与判定席裁决。

—— QF-OS 联邦批二十七 EXT-WAVE-39 S3 预检模拟席 · 枢/PIVOT-01 体系 · 2026-10-27 · 判定窗硬钉 2026-11-03 预飞闸前
