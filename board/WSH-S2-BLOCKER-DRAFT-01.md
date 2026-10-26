CLASSIFY: L1
# WSH-S2-BLOCKER-DRAFT-01 · S2 三阻塞闭合草案件（B-1 workflow 全文草案／B-2 十钉清单／B-3 工具链就位路径）——评审稿，不闭合阻塞本身

- 席别：QF-OS 联邦批二十 W11 S2 阻塞闭合制备席（枢/PIVOT-01 体系）
- 成文时刻（date -u 实测）：**2026-10-26T05:19Z** 起取证、成文（UTC(Z) 单时钟域；距 11-03 预飞闸约 7.9 日）
- 基件钉：`board/WSH-S2-FINAL-PREP-01.md`（§一 B-1/B-2/B-3 定义、修-1~修-7）、`board/WSH-M1-GAPCLOSE-01.md` §二（六字段／runbook §2.2／验证规程 §2.3）、`board/WSH-S2-PREFLIGHT-01.md`（§一 A1.1–A4.2 十处含糊登记）
- **性质声明（权限边界）**：本件为**闭合草案/评审稿**，不闭合任何阻塞本身；**未创建/未修改 `.github/` 下任何文件**；portal 仓全程只读（API GET only），零 git 操作；workflow 合入与提交权归 orchestrator 与判定席。
- 纪律自检：首行 CLASSIFY: L1；凭证名值分离（gh_pat 仅以 `$(cat /mnt/agents/.pivot-sec/gh_pat)` 名引用，值零次落文本）；不编数（全部取值 2026-10-26 API/本机实测在案）；甲席席规（本件无工时数值估计）。

---

## 〇、取证实录（2026-10-26T05:19Z，全部 API 直连真值通道）

| 项 | 实测值 | 出处 |
|---|---|---|
| `.github/workflows/m1-b1-baseline.yml` | API contents **HTTP 404（依旧不存在）** | 本席复测 |
| workflows 清单 | **54 件 active**，无 m1-b1 件 | GET /actions/workflows?per_page=100 |
| 先例载体 | `m1-1-toolchain-spike.yml`（workflow_id 388964286，5628 bytes，sha 67304cc46776）——含 workflow_dispatch＋elan 用户态装＋pin 置换 fail-fast＋mathlib cache get＋upload-artifact@v4 体例 | GET contents |
| comparator01.yml | 381 bytes，四要件全无，**不可充数**（预飞件结论复核维持） | GET contents |
| `library/ns/formalization.yaml` | **13926 bytes，sha 4b40f6f1653b，`machine_checks` 键不存在**；文件头现行 schema 声明见 §二 A3.2 | GET contents |
| `registry/TRUSTBOUNDARY-REGISTRY-01.md` | 23260 bytes，sha 750be90ca636；S2 行实测位于 **L95**（§4.4 表） | GET contents |
| 默认分支 | **main**（API 实测） | GET /repos |
| 本机 `which check-jsonschema` | **实测空依旧**；`pip index` 可得 0.38.2，`pip install --dry-run` exit=0 | 本机实测 |

---

## 一、B-1 闭合草案：`.github/workflows/m1-b1-baseline.yml` 全文（评审稿）

体例照 `m1-1-toolchain-spike.yml` 先例移植；四要件齐套（① elan 用户态装 Lean v4.35.0 无 root；② mathlib cache get；③ comparator 跑批 `tee` 落盘原始字节＋`sha256sum` 取值；④ artifact 上传 retention_days=90＋`GITHUB_RUN_ID`/`GITHUB_RUN_ATTEMPT` 透传写入 verdict 文件）。artifact 名与 verdict 文件名之钉见 §二 A1.2/A1.3（与本 workflow 逐字一致）。

````yaml
# CLASSIFY: L1
# WSH-M1 G-3 / S2 · m1-b1 baseline 跑批（comparator verdict 首跑，六字段回填证据件）
# 四要件（WSH-M1-GAPCLOSE-01 §2.2-1 / WSH-S2-FINAL-PREP-01 §一 B-1）：
#   ① elan 用户态装 Lean v4.35.0（无 root，spike rustup 绕行先例）
#   ② mathlib cache get（TB-04 410s/次先例）
#   ③ comparator 跑批 tee comparator-run.log 全量落盘（stdout+stderr 合并流，
#      不重排不裁截，原始字节为规范件）＋ sha256sum 取值
#   ④ artifact 上传（retention_days: 90 ≥ 90，名称钉 m1-b1-comparator-run）
#      ＋ GITHUB_RUN_ID/GITHUB_RUN_ATTEMPT 透传写入 verdict.txt
# 体例移植自 m1-1-toolchain-spike.yml（workflow_id 388964286 在案先例）
# W30 合规：workflow_dispatch 一次性事件驱动，非定时；无 push 触发（A2.1 钉）
name: m1-b1-baseline
on:
  workflow_dispatch:
    inputs:
      mode:
        description: 'dry-run（空转验证，不回填）或 formal（正式跑批，供回填取证）'
        required: true
        default: 'dry-run'
        type: choice
        options:
          - dry-run
          - formal

permissions:
  contents: read

jobs:
  baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install elan (user-space, no root)
        run: |
          curl -sSfL https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none
          echo "$HOME/.elan/bin" >> $GITHUB_PATH

      - name: Prep — pin swap (fail-fast) + mathlib cache get
        id: prep
        run: |
          set -o pipefail
          rm -rf /tmp/m1-b1 && mkdir -p /tmp/m1-b1
          cp -r "$GITHUB_WORKSPACE/library/ns/." /tmp/m1-b1/
          cd /tmp/m1-b1
          sed -i -E 's|@[[:space:]]*"v4\.10\.0"|@ "v4.35.0"|' lakefile.lean
          grep -q '@ "v4.35.0"' lakefile.lean || { echo 'PIN-SWAP FAILED: mathlib require unchanged'; exit 1; }
          echo 'leanprover/lean4:v4.35.0' > lean-toolchain
          rm -f lake-manifest.json
          CACHE_RC=0
          { /usr/bin/time -v lake exe cache get ; } > cache.log 2>&1 || CACHE_RC=$?
          echo "cache_rc=$CACHE_RC" >> "$GITHUB_OUTPUT"
          echo "- cache get exit=$CACHE_RC" >> "$GITHUB_STEP_SUMMARY"
          if [ $CACHE_RC -ne 0 ]; then echo 'CACHE GET FAILED'; exit $CACHE_RC; fi

      - name: Build library @ v4.35.0
        id: build
        run: |
          cd /tmp/m1-b1
          START=$(date +%s)
          RC=0
          { /usr/bin/time -v lake build ; } > build.log 2>&1 || RC=$?
          END=$(date +%s)
          echo "build_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "## Build @ v4.35.0" >> "$GITHUB_STEP_SUMMARY"
          echo "- exit=$RC, wall=$((END-START))s" >> "$GITHUB_STEP_SUMMARY"
          if [ $RC -ne 0 ]; then
            echo '- ERRORS (first 120 lines):' >> "$GITHUB_STEP_SUMMARY"
            echo '```' >> "$GITHUB_STEP_SUMMARY"
            grep -E 'error' build.log | head -120 >> "$GITHUB_STEP_SUMMARY" || true
            echo '```' >> "$GITHUB_STEP_SUMMARY"
            exit $RC
          fi

      - name: Comparator run — tee 落盘原始字节（stdout+stderr 合并流）
        id: comparator
        run: |
          cd /tmp/m1-b1
          set -o pipefail
          RC=0
          { lake comparator ; } 2>&1 | tee comparator-run.log || RC=$?
          # comparator-run.log 为规范件：不重排、不裁截、原始字节
          echo "comparator_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- comparator exit=$RC" >> "$GITHUB_STEP_SUMMARY"

      - name: Verdict 取值 + run_id 环境透传写入 verdict.txt
        id: verdict
        run: |
          cd /tmp/m1-b1
          # verdict 逐字取自日志末行（拼写钉：accepted / rejected，禁改写）
          V=$(grep -E '^verdict: (accepted|rejected)$' comparator-run.log | tail -1 | awk '{print $2}')
          if [ "$V" != "accepted" ] && [ "$V" != "rejected" ]; then
            echo 'VERDICT PARSE FAILED: no terminal verdict line'; exit 1
          fi
          {
            echo "verdict: $V"
            echo "run_id: gha:${GITHUB_RUN_ID}#${GITHUB_RUN_ATTEMPT}"
            echo "mode: ${{ github.event.inputs.mode }}"
          } > verdict.txt
          sha256sum comparator-run.log | tee comparator-run.log.sha256
          cat verdict.txt >> "$GITHUB_STEP_SUMMARY"

      - name: Upload artifacts (retention 90d, 名称钉 m1-b1-comparator-run)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: m1-b1-comparator-run
          retention-days: 90
          path: |
            /tmp/m1-b1/comparator-run.log
            /tmp/m1-b1/comparator-run.log.sha256
            /tmp/m1-b1/verdict.txt
            /tmp/m1-b1/cache.log
            /tmp/m1-b1/build.log
          if-no-files-found: error
````

**四要件对拍表（草案自证）**：

| 要件 | 落位步骤 | 钉 |
|---|---|---|
| ① elan 用户态装 v4.35.0 | `Install elan`＋`Prep`（pin 置换 fail-fast＋lean-toolchain 钉） | 无 root、禁 sudo |
| ② mathlib cache get | `Prep`（失败即 exit 非零，不静默） | TB-04 410s 先例 |
| ③ tee 落盘＋sha256sum | `Comparator run`（`2>&1 \| tee`，pipefail 保退出码）＋`Verdict` 步骤 `sha256sum` | 原始字节、合并流、不重排不裁截 |
| ④ artifact 上传 retention≥90＋RUN_ID/ATTEMPT 透传 | `Upload artifacts`（retention-days: 90，名钉）＋`verdict.txt` 写 `run_id: gha:<id>#<attempt>` | if-no-files-found: error（缺失即红，防伪绿） |

**如实登记（不确定处）**：`lake comparator` 之确切 CLI 形态照 GAPCLOSE §2.1 固定值 `lake comparator` 落笔；comparator 子命令/目标在仓内构建件中的精确调用面（参数、出口码语义）须由 orchestrator 合入前对照 nanoda_lib 构建件核一遍——若实调形态不同，仅改 `Comparator run` 步骤命令行，tee/sha256/verdict 规程不动。

---

## 二、B-2 闭合草案：runbook 十处含糊逐项补钉清单（A1.1–A4.2）

含糊编号照预飞件 §一登记；钉死措辞可直接并入 runbook §2.2 修订。

| # | 含糊 | 补钉措辞（钉死值） |
|---|---|---|
| **A1.1** | 「空转验证」语义未钉 | **空转＝同一 workflow 以 `mode=dry-run` 完整执行一次，四要件全实证（含 comparator 实跑步骤）**；与正式跑唯一差异＝不回填、不登记注册表指针。禁「仅验基建①②④」之缩水空转——要件③不得押到 11-04 首证。 |
| **A1.2** | verdict 文件名/路径/字段拼写未钉 | 文件名钉 **`verdict.txt`**；路径钉 `/tmp/m1-b1/verdict.txt`，随 artifact `m1-b1-comparator-run` 同包上传；字段拼写钉 **`verdict: accepted`**／**`verdict: rejected`**（小写、冒号后单空格，逐字照 spike B §5.1 在案值）；同文件必携 `run_id: gha:<run_id>#<attempt>` 行。回填步骤 3 以该文件为唯一读取接口。 |
| **A1.3** | artifact 名称未钉 | 名称逐字钉 **`m1-b1-comparator-run`**（下载脚本与分支丙排障对拍均以此名为唯一键）。 |
| **A1.4** | 合入目标分支未钉 | 合入分支钉 **main**（API 实测 default_branch=main，2026-10-26）；workflow_dispatch 仅在默认分支可触发，合入非 main 即不可 dispatch（分支甲排障钉）。 |
| **A2.1** | 触发方式未钉 | 触发方式钉 **workflow_dispatch 手触**（API POST /actions/workflows/m1-b1-baseline.yml/dispatches 或 Actions UI，二选一，执行席择一并留痕）；**workflow 本体不含 push 触发**（见 §一草案 `on:` 块）。 |
| **A2.2** | 取值脚本未随备料交付 | 脚本钉为预飞件 §四已实测之 curl+python3 路径，随本件交付（见 §二末代码块）；禁手抄转录。 |
| **A3.1** | 注册表指针目标未钉 | 目标件钉 **`registry/TRUSTBOUNDARY-REGISTRY-01.md` §4.4 表 S2 行**（API 实测 L95，sha 750be90ca636，2026-10-26）「当前证据指针」列，填入 `gha:<run_id>#<attempt>`＋`log_sha256`（64 位小写 hex 全值）；行内「缺口与关闭路径」列「TB-06 转 T1」注记之销记权属判定席，执行席只填指针不改 T 级。 |
| **A3.2** | schema URL 未钉 | **以执行日 `library/ns/formalization.yaml` 文件头现行声明为准复钉（修-2 强制）**；现值（2026-10-26 API 实测，13926 bytes 版文件头第 1 行）为 `https://raw.githubusercontent.com/mathlib-initiative/formalization.yaml/main/schema/formalization.schema.json`。执行日步骤 10:00 前重读文件头逐字取值，禁援引本快照充当现行基线。 |
| **A3.3** | artifact 下载工具未钉 | 钉 **REST API＋curl 为主**（预飞件 §二实测路径：`GET /actions/runs/<run_id>/artifacts` 枚举→zip 下载→解包）；**gh CLI 为备**（`gh run download <run_id> -n m1-b1-comparator-run`）。主通道失败方启用备通道，双通道结果均须过哈希复算。 |
| **A4.1** | attempt 记法与注记义务未钉 | run_id 记法钉 **`gha:<run_id>#<attempt>`**；attempt≥2（重试跑）时回填条目须附注记「取用 attempt=N（第 N 次跑批，前次失败原因见申报/排障登记）」——注记以 YAML 注释行随条目落盘，禁只改数字不留痕。 |

**A4.2（机位钉——如实登记本席权限缺口）**：备通道 `local:<UTC14>-<hostname sha256 前8>` 之承载机位（≥8GB 内存机），**本席无机位指名权，亦未实测到已预置机位**。补钉措辞建议：「备通道承载机位由**算力线协调席**指名并预置（≥8GB 内存、elan 用户态可装），指名结果须于 2026-11-03 预飞闸前登记入板；逾期未指名即随分支甲申报路径一并呈裁。」此项为十钉中**唯一非本席可自闭合项**，如实上报。

**A2.2 随件脚本（预飞件 §四实测路径固化）**：

```bash
# run_id 脚本取值（禁手抄）；gh_pat 名值分离，值不落文本
curl -s -H "Authorization: Bearer $(cat /mnt/agents/.pivot-sec/gh_pat)" \
  "https://api.github.com/repos/chepin-ai/vci-inbox/actions/runs?per_page=3" \
| python3 -c "
import json,sys
runs=json.load(sys.stdin)['workflow_runs']
r=[w for w in runs if w['name']=='m1-b1-baseline'][0]
print(f\"gha:{r['id']}#{r['run_attempt']}\")
"
```

---

## 三、B-3 闭合草案：check-jsonschema 就位路径评估

**本机实测（2026-10-26T05:19Z）**：`which check-jsonschema` **空**；`python3 -c "import check_jsonschema"` ImportError；`pip index versions check-jsonschema` 得 **0.38.2**（最新），`pip install --dry-run` **exit=0**——本机 pip 通道可行。

| 路径 | 方案 | 评估 |
|---|---|---|
| **路径甲（本机 pip）** | 执行席主机 `pip install check-jsonschema==0.38.2`（版本钉死，禁浮动） | 立即可行（dry-run 实测通过）；风险：执行日环境漂移（pip 缓存/网络），须 11-03 预飞闸前装妥并 `check-jsonschema --version` 留痕 |
| **路径乙（CI 内压入，建议主用）** | 验证规程 2 压入 m1-b1-baseline workflow 末端步骤（片段见下），CI 侧先行 schema 核验，本地复验降为复核席独立重算环 | 不依赖执行席本机工具链，与 B-1 workflow 同生死；workflow_dispatch 空转即实证该步骤可用——**与 A1.1 全要素空转钉天然咬合** |

**路径乙 workflow 片段建议（追加于 §一草案 `Verdict` 步骤之后、`Upload` 之前）**：

```yaml
      - name: Schema 核验（check-jsonschema，验证规程 2 CI 侧）
        run: |
          pip install check-jsonschema==0.38.2
          SCHEMA_URL=$(sed -n '1s/^# yaml-language-server: \$schema=//p' \
            "$GITHUB_WORKSPACE/library/ns/formalization.yaml")
          echo "schema_url=$SCHEMA_URL" >> "$GITHUB_STEP_SUMMARY"
          check-jsonschema --schemafile "$SCHEMA_URL" \
            "$GITHUB_WORKSPACE/library/ns/formalization.yaml"
        # 钉：schema URL 执行时自文件头现行声明动态取值（修-2/A3.2 条款），
        #     禁硬编码快照 URL；本步骤核验回填前基线，回填后本地复验为验证 2 全量。
```

**建议口径**：**路径乙为主、路径甲为备**——双通道互为冗余；若 11-03 前本机 pip 装妥且 CI 片段随 B-1 合入，则 B-3 双证闭合；仅一路就位亦满足闭合条件（验证规程 2 有一处可执行载体即成立），但**建议双路**，如实登记：CI 片段使 workflow 略增依赖面（pip 公网拉取），合入裁量归 orchestrator/判定席。

---

## 四、合规自检（本件行文）

1. **首行 CLASSIFY: L1**；gh_pat 名值分离零落值；日期全为绝对 UTC(Z) 或带出处钉。
2. **不编数**：404／54 件清单／13926 bytes+sha 4b40f6f1653b／registry L95+sha 750be90ca636／main 默认分支／check-jsonschema 缺位+0.38.2+dry-run exit=0，均 2026-10-26T05:19Z 本席实测。
3. **如实登记**：`lake comparator` 精确调用面未实证（§一末）；A4.2 机位指名权属算力线协调席、本席不可自闭合（§二）；CI pip 拉取新增依赖面（§三）。
4. **权限边界**：本件仅新建 `board/WSH-S2-BLOCKER-DRAFT-01.md` 一件；**未创建/未修改 `.github/` 下任何文件**，portal 仓全程只读零 git 操作；workflow 合入、提交与阻塞闭合判定权属 orchestrator 与判定席。
5. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** workflow 草案四要件自证与空转绿灯均为机器层必要条件证据，闭合判定须经独立复核与判定席裁决。

—— QF-OS 联邦批二十 W11 S2 阻塞闭合制备席 · 枢/PIVOT-01 体系 · 2026-10-26 · S2 责任窗硬钉 2026-11-06
