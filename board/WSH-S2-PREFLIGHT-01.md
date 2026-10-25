CLASSIFY: L1
# WSH-S2-PREFLIGHT-01 · S2 责任窗（2026-11-06，run_id/log_sha256 回填）预飞结论件

- 预飞席：QF-OS 联邦批十七 W10′ S2 预飞席
- 成文时刻（date -u 实测）：**2026-10-25T18:04:42Z**（UTC(Z) 单时钟域；预飞钉 2026-11-03 前完成——满足，余量 9 天）
- 上游基线：`board/WSH-M1-GAPCLOSE-01.md` §二（六字段定义表／runbook §2.2／五项验证规程 §2.3）
- 纪律自检：首行 CLASSIFY: L1；凭证名值分离（gh_pat 仅以 `$(cat /mnt/agents/.pivot-sec/gh_pat)` 名引用，值绝未落文本）；portal 仓全程只读（API GET only），未执行任何 git 写操作；不编数（全部取值均有实测出处）

---

## 〇、结论速览

- **就绪判定：NO-GO（截至 2026-10-25）**，**条件 GO**：阻塞项 B-1 于 2026-11-03 预飞闸前闭合即转 GO。
- **阻塞项数：3**（B-1 硬阻塞 / B-2 规程含糊需补钉 / B-3 工具链条件项）。
- 模板生成规程与五项验证规程：**格式层全部实测可对拍**（§三、§四），备料本身质量合格；阻塞在工作流载体未生，不在规程。

---

## 一、runbook（§2.2 四步）逐条复述与含糊登记

### 步骤 1 · 预飞检查（T-3 工作日，2026-11-03 前）
- **复述**：`.github/workflows/m1-b1-baseline.yml` 须合入，含四要件——① elan 用户态装 Lean v4.35.0；② mathlib cache get；③ comparator 跑批带 `tee` 落盘＋`sha256sum` 取值；④ artifact 上传（retention_days≥90）＋`GITHUB_RUN_ID`/`GITHUB_RUN_ATTEMPT` 写入 verdict 文件。以 `workflow_dispatch` 空转验证一次。
- **含糊/缺失登记**：
  - A1.1「空转验证」语义未钉：空转是否含 comparator 实跑步骤？若仅验证 ①②④ 基建，则要件③首次实证即押在 11-04 正式跑，风险前置。
  - A1.2「verdict 文件」文件名/路径/字段拼写未钉（回填步骤 3 须读取之，缺接口钉）。
  - A1.3 artifact 名称未钉（下载步骤无法预先脚本化）。
  - A1.4 合入目标分支未钉（默认 main 推断，未明写）。

### 步骤 2 · 执行日（≤2026-11-04）
- **复述**：触发正式跑批；自 API 抄录 run_id（脚本取值，禁手抄）；等待绿灯。
- **含糊/缺失登记**：
  - A2.1 触发方式未钉（workflow_dispatch 手触 or push 触发）。
  - A2.2 「脚本取值」之脚本未随备料交付（本件 §四实测 curl+python3 取值路径可充当该脚本先例，已验证可行）。

### 步骤 3 · 同窗回填（当日）
- **复述**：下载 artifact → 本地重算 sha256 与 CI 侧比对 → 六字段 append-only 填入 `formalization.yaml` `machine_checks[]` → check-jsonschema 复验 → 注册表指针登记。
- **含糊/缺失登记**：
  - A3.1 「注册表指针登记」之注册表文件与字段未钉（registry 具体目标不明）。
  - A3.2 check-jsonschema 所用 schema URL 未钉（`library/ns/formalization.yaml` 文件头声明 `formalization.schema.json` 外链，执行时须照此钉死）。
  - A3.3 artifact 下载工具未钉（gh CLI / REST API 择一）。
- **实测补充**：回填目标文件实测为 `library/ns/formalization.yaml`（portal 仓 API 实查，11546 bytes），**现无 `machine_checks` 键**——回填即新建该键，append-only 语义天然满足；schema 容忍未知键有 federation 块先例（基线在案）。

### 步骤 4 · 失败重试
- **复述**：首跑失败窗内重试一次（11-05→11-06）；二度失败或通道不可用 → 记「未定+理由」并于 2026-11-10 前申报，禁静默顺延。
- **含糊/缺失登记**：
  - A4.1 重试即 attempt=2，回填 run_id 应记 `gha:<id>#2` 并在条目注明取用 attempt——runbook 未明写该注记义务。
  - A4.2 备通道 `local:<UTC14>-<hostname sha256 前8>` 之承载主机未指名/未预置（≥8GB 内存机仅格式钉，无机位钉）。

**含糊总计：10 处**（A1.1–A4.2）。均非致命，建议以 runbook 补钉件于 11-03 前闭合（B-2）。

---

## 二、模板字段实测：样例记录（真实 run 数据）

**数据源**：`curl -s -H "Authorization: Bearer $(cat /mnt/agents/.pivot-sec/gh_pat)" https://api.github.com/repos/chepin-ai/vci-inbox/actions/runs?per_page=3`（HTTP 200，2026-10-25T18:04Z 实测）。取最近 run：**id=40219464500，run_attempt=1**，workflow=board-indexer-bridge，conclusion=success，created_at=2026-10-25T18:04:01Z，`https://github.com/chepin-ai/vci-inbox/actions/runs/40219464500` 可达。

**样例记录（dry-run 格式样例，非正式回填）**：

```yaml
machine_checks:
- tool: lake comparator
  tool_version: v4.35.0
  run_id: gha:40219464500#1
  verdict: accepted
  log_sha256: dc0c71528030cb5e4c3b28caedaf6e6ac674b293f67e92c806954613d4572c06
  as_of: '2026-10-25'
```

**如实登记（防误用钉）**：样例 run_id 指向 board-indexer-bridge 之 run，**非 comparator 跑批 run**——仅证格式可构造、API 可解析；11-04 正式回填必须取自 m1-b1-baseline 实跑 run。另：yaml 序列化时 `as_of` 须带引号（防 YAML 1.1 日期型解析），已实测确认。

---

## 三、dry-run 实录（tee 落盘 + sha256sum + 五项验证对拍）

**生成规程实测**（/tmp，2026-10-25T18:04Z）：

```bash
{ <模拟 comparator 输出，末行 verdict: accepted> ; } 2>&1 | tee comparator-run.log >/dev/null
sha256sum comparator-run.log
# => dc0c71528030cb5e4c3b28caedaf6e6ac674b293f67e92c806954613d4572c06  comparator-run.log
```

**五项验证规程逐条对拍**：

| # | 验证规程 | dry-run 实测 | 判定 |
|---|---|---|---|
| 1 | 哈希复算核验 | 副本独立 `sha256sum` 重算＝`dc0c…72c06`，逐字节一致 | **PASS（格式）**；独立性（复核席≠回填席）为组织要件，格式层无法证，留执行日落实 |
| 2 | schema 核验 | 六字段 yaml round-trip 解析通过；格式断言全过（run_id 形如 `gha:<id>#<n>`、log_sha256=64 位小写 hex、verdict∈{accepted,rejected}、as_of ISO 日期）；**本席主机无 check-jsonschema 二进制**（`which` 实测缺位），schema 对拍未跑 | **PARTIAL** → B-3 |
| 3 | run_id 可解析核验 | API 解析 40219464500 成功：id 一致、attempt=1 一致、created_at 与 as_of 同日（UTC） | **PASS** |
| 4 | verdict 一致性核验 | 日志末行 `verdict: accepted` 与字段逐字一致（grep 计数=1） | **PASS** |
| 5 | 时限核验 | as_of=2026-10-25 ≤ 2026-11-06 | **PASS（dry-run 口径）**；正式值以 11-04 实跑日为准 |

**对拍结论：五项中 4 PASS + 1 PARTIAL（工具链缺位，非规程缺陷）**。产物格式与验证规程逐条可对拍，规程本身无逻辑缺口。

---

## 四、就绪判定与阻塞项清单

### 阻塞项

| # | 等级 | 阻塞描述 | 实测证据 | 闭合条件 / 截止 |
|---|---|---|---|---|
| **B-1** | **硬阻塞** | 目标 workflow `.github/workflows/m1-b1-baseline.yml` **不存在** | API contents 请求 HTTP 404（2026-10-25 实测）；全仓 55 个 active workflow 清单中无 m1-b1 件；现最接近件 `comparator01.yml` 实测 381 bytes、四要件扫描全 False（tee/sha256sum/retention/GITHUB_RUN_ID/upload-artifact 均无），**不可充数** | workflow 件合入 main 并四要件齐套＋空转一次 → **2026-11-03 预飞闸** |
| **B-2** | 规程含糊 | runbook 10 处含糊（§一 A1.1–A4.2：verdict 文件名/artifact 名/schema URL/注册表目标/触发方式等未钉） | §一逐条登记 | 补钉件成文 → 2026-11-03 前（可与 B-1 同窗闭合） |
| **B-3** | 条件项 | 本席主机 check-jsonschema 缺位，验证规程第 2 项无法本地跑 | `which check-jsonschema` 实测空 | 执行日前 `pip install check-jsonschema` 或将该项压入 CI 步骤 → 2026-11-04 前 |

### 非阻塞利好（如实登记）

- 先例载体在案：`m1-1-toolchain-spike.yml`（workflow_id 388964286）实测含 elan 用户态安装＋mathlib cache get＋workflow_dispatch 三要件体例，run 39214080542（2026-10-19，success）即在案先例——B-1 之 workflow 件有可直接移植的骨架，估 0.5pd 内在案预算。
- run_id 生成规程与 API 取值路径已实测可行（§二/§三），无需另制脚本。

### 判定

**NO-GO（当前）→ 条件 GO**：B-1 于 2026-11-03 前闭合（含空转验证）、B-2/B-3 同步闭合，则 2026-11-04 执行日 **GO**。若 11-03 闸 B-1 未闭 → 触发 R-1 升级路径（算力线协调席＋备通道激活评估），不得静默。

---

## 五、2026-11-04 执行日分钟级时刻表（草案，UTC(Z)，T0=09:00Z 开工假设）

| 时刻 | 时长 | 动作 |
|---|---|---|
| 09:00–09:05 | 5m | 闸前复检：workflow 已合入、四要件 grep 齐套、dispatch 权限确认（B-1/B-2/B-3 闭合证验） |
| 09:05–09:08 | 3m | 触发 `workflow_dispatch`（m1-b1-baseline，正式跑批；S4 dry-run 同窗并批照 G-3/G-4 并窗设计） |
| 09:08–09:10 | 2m | 脚本取值 run_id：`curl …/actions/runs?per_page=3` 取最新 run id+attempt，落 `gha:<id>#1`（禁手抄） |
| 09:10–09:40 | 30m | 等待绿灯（elan 装＋cache get＋构建＋comparator；410s 全量重编先例外推，轮询 60s/次；wall 硬封 ≤3h 即 ≤12:08） |
| 09:40–09:45 | 5m | 绿灯确认＋artifact 下载（gh CLI 或 API，择一钉于 B-2 补钉件） |
| 09:45–09:50 | 5m | 本地重算 `sha256sum comparator-run.log`，与 CI 侧取值逐字节比对（验证 1 之执行席半） |
| 09:50–10:00 | 10m | 六字段 append 入 `library/ns/formalization.yaml` `machine_checks[]`（新建键；旧条目无，append-only 天然满足） |
| 10:00–10:05 | 5m | check-jsonschema 复验（schema URL 照文件头声明钉死；验证 2） |
| 10:00–10:10 | 10m | run_id API 复解析＋attempt 一致＋时刻同日（验证 3）；日志末行 verdict 对拍（验证 4） |
| 10:10–10:15 | 5m | `as_of = date -u +%Y-%m-%d` 取值落字段；时限核验 ≤2026-11-06（验证 5） |
| 10:15–10:20 | 5m | 注册表指针登记（目标件钉于 B-2 补钉件）＋闭合记录成文 |
| 10:20–11:30 | 70m | **缓冲带**（artifact 排障／字段回填返工／验证席独立重算接洽） |
| 11:30 | — | 当日硬收：未绿即转入重试编排，11-05 重跑一次（attempt=2，回填记 `gha:<id>#2` 并注明）；11-06 窗尽 |
| 11-10 前 | — | 二度失败／通道不可用 → 「未定+理由」＋回判定席申报（禁静默顺延） |

---

## 六、合规自检

1. **名值分离**：gh_pat 全文以名引用零次落值；全部日期为绝对 UTC(Z) 或带出处相对钉；哈希/run_id 均实测取值。
2. **不编数**：run 40219464500、workflow 清单、404 缺件、hash dc0c…72c06 均有 2026-10-25T18:04Z 实测出处；样例记录显式标注「dry-run 格式样例，非正式回填」。
3. **如实登记**：B-1 硬阻塞、check-jsonschema 缺位、样例 run 非 comparator run 等不利事实全部载入。
4. **权限边界**：只读 portal 仓（GET only）；本件仅新建 `board/WSH-S2-PREFLIGHT-01.md`，未改任何既有字节，未执行 git 写操作；GO/NO-GO 为预飞席技术判定，升降级裁量权属判定席。
5. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** CI 绿灯与哈希对拍均为机器层必要条件证据，闭合判定须经独立复核与判定席裁决。

—— QF-OS 联邦批十七 W10′ S2 预飞席 · 枢/PIVOT-01 体系 · 2026-10-25
