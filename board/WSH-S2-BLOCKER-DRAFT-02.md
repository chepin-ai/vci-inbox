CLASSIFY: L1
# WSH-S2-BLOCKER-DRAFT-02 · S2 阻塞闭合草案返修版（W2-P0-09 九项必修全落地）——评审稿 v2，不闭合阻塞本身

- 席别：QF-OS 联邦批二十 W11 S2 阻塞闭合制备席（枢/PIVOT-01 体系）·续命返修
- 成文时刻（date -u 实测）：**2026-10-26T11:16Z** 起取证、成文（UTC(Z) 单时钟域）
- 返修令：`board/ADJUD-WILDQ2-HARVEST-01.md` §三 W2-P0-09（九项必修，GOS2 §1–§6/§8/§10 全收，未落地则 B-1 不闭合）；红队原指控 `board/WILDQ2-GOS2-20261026-01.md` §1–§9/§11
- 被修件：`board/WSH-S2-BLOCKER-DRAFT-01.md`（v1，本件全量替代其技术内容；v1 保留在案不改写，append-only）
- 性质声明：本件仍为**闭合草案/评审稿**；**未创建/未修改 `.github/` 下任何文件**；portal 仓全程只读（API GET only），零 git 操作；合入权归 orchestrator 与判定席
- 纪律自检：首行 CLASSIFY: L1；gh_pat 名值分离零落值；不编数（全部取值 2026-10-26 实测在案）；甲席席规（无工时数值；timeout-minutes 数值标注「orchestrator 定」沿野问建议体例）

---

## 〇、返修取证（2026-10-26T11:16Z 起，实测；支撑必修⑥⑦⑨）

| # | 实测项 | 结果 | 销记支撑 |
|---|---|---|---|
| E-1 | 远端 `library/ns/lakefile.lean`（API 直连） | 251 bytes，sha 73b7b359cf7e，**mathlib 已钉 `@ "v4.35.0"`**；`lean-toolchain` 25 bytes 已钉 `leanprover/lean4:v4.35.0` | v1「pin 置换」步骤对象已不存在——**置换改核验**（钉漂移即红） |
| E-2 | 仓内 `grep -rn "comparator" library/` | **零命中**——library/ns 内无 comparator target/定义件；`.github/gates/comparator01.py`（1517B，sha bc044f29b81c）系 cisvr 门禁，**非同物** | 必修⑦：裸 `lake comparator` 形态证伪，调用面须照 spike A 实证形态 |
| E-3 | spike 子件 A（`board/TRUSTBOUNDARY-SPIKE-A-01.md` #21–#24） | `lake comparator` 系 v4.35.0 工具链**原生内建**；config 五要件（challenge/solution_module、theorem_names、permitted_axioms 强制显式）；bwrap 默认强制、缺位拒跑 **EXIT=2**；`--inadvisably-no-sandbox` 绕行输出自宣 not trustworthy（**验收不可援引**）；成功标记逐字 **`Your solution is okay!`**（2m14.6s/9m12.6s 两例在案） | 必修⑦第十一钉素材；必修② verdict 物理末行证据形态 |
| E-4 | elan-init.sh 快照 | 9823 bytes，sha256 **`a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53`**（2026-10-26T11:16Z curl 实测）；先例 m1-1-toolchain-spike.yml 该段**亦无哈希钉**（逐字复核）——非移植失真，属新增补强；钉值合入前须复钉 | 必修⑥ |
| E-5 | schema 实证（check-jsonschema 0.38.2 本机 pip 装妥实测） | ①文件头 dispatcher URL（`…/formalization.schema.json`，997B，sha256 22bd0b61…）对现行 formalization.yaml **rc=1 FAIL**：`$.version: 'v0.5' is not one of ['v0.3','v0.4']`；②`v0.5.schema.json` 上游 **HTTP 404**；③直取 `v0.4.schema.json`（12694B，sha256 **`25ff6b25ca4511635aff4443cf20480c15e59dddf19591c730950b442ea54fce`**，经 api.github.com 取得）对现行文件 **rc=0 PASS**，追加 `machine_checks[]` 六字段样例后 **rc=0 PASS**（unknown keys 容忍实证） | 必修⑨：文件头 URL 现状即不可用＋自指环，信任根必须换仓内钉版副本；version 偏移（v0.5 声明 vs 上游止于 v0.4）呈裁登记 |
| E-6 | 专用端点形态实证 | `GET /actions/workflows/388964286/runs?per_page=1&status=completed` 返回 run 39214080542/attempt 1/success/head_branch=main——字段齐 | 必修④脚本 v2 形态可行性 |
| E-7 | 申报钉算术复算（python3） | 2026-11-06＝周五；**+5 工作日＝2026-11-13（周五）**；11-08／11-15 均为周日 | W2-P0-10③ 随附更正（lead 令并入） |

---

## 一、B-1 workflow 草案 v2：`.github/workflows/m1-b1-baseline.yml` 全文（返修落地必修①②③⑤⑥）

变更对拍 v1：pin 置换→钉核验（E-1）；Prep 拆两步独立计时（⑥）；elan 装脚本 sha256 对拍＋curl 重试（⑥）；comparator 步尾部退出码闸（①）；verdict 改物理末行语义＋退出码交叉承载（②）；job 级 timeout-minutes（⑤）；cache 命中哨兵（⑤）；artifact 名按 mode 分支后缀、裸名永不产出（③）；调用面照 spike A 实证形态落位、未实证余项入第十一钉（⑦）。

````yaml
# CLASSIFY: L1
# WSH-M1 G-3 / S2 · m1-b1 baseline 跑批 v2（W2-P0-09 返修版）
# 四要件（GAPCLOSE §2.2-1）：① elan 用户态装 v4.35.0（无 root，sha256 钉+重试）
#   ② mathlib cache get（命中哨兵，miss 即红） ③ comparator 跑批 tee 原始字节落盘
#   （stdout+stderr 合并流，不重排不裁截）＋退出码闸＋sha256sum 取值
#   ④ artifact 上传 retention-days: 90＋GITHUB_RUN_ID/ATTEMPT 透传 verdict.txt
# W2-P0-09 必修落位：① comparator 步尾 [ $RC -eq 0 ] || exit $RC；② verdict 物理末行
#   语义（最后一非空行必须逐字匹配证据形态）＋退出码交叉承载；③ artifact 名 mode 后缀
#   （-formal/-dryrun，裸名 m1-b1-comparator-run 永不产出）；⑤ timeout-minutes＋cache
#   哨兵；⑥ elan 脚本哈希钉＋--retry＋Prep 拆步计时；⑦ 调用面 spike A 实证形态
name: m1-b1-baseline
on:
  workflow_dispatch:
    inputs:
      mode:
        description: 'dry-run（空转验证，不回填）或 formal（正式跑批，供回填取证）'
        required: true
        default: 'dry-run'
        type: choice
        options: [dry-run, formal]

permissions:
  contents: read

env:
  # 必修⑥：elan-init.sh sha256 钉（2026-10-26T11:16Z 实测快照 E-4；合入前须复钉，
  # 复钉值出入即更新本钉并登记——钉值入 B-2 补钉件第十二钉位）
  ELAN_INIT_SHA256: "a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53"

jobs:
  baseline:
    runs-on: ubuntu-latest
    # 必修⑤：wall 硬封 CI 层执行体；170 为野问建议值（≤3h 封钉留上传余量），
    # 终值由 orchestrator 定——本钉数值裁决权不在本席
    timeout-minutes: 170
    steps:
      - uses: actions/checkout@v4

      - name: Install elan (user-space, sha256-pinned, retried)
        run: |
          curl -sSfL --retry 3 --retry-delay 10 \
            https://elan.lean-lang.org/elan-init.sh -o /tmp/elan-init.sh
          echo "$ELAN_INIT_SHA256  /tmp/elan-init.sh" | sha256sum -c - \
            || { echo 'ELAN INIT HASH MISMATCH — supply-chain gate'; exit 1; }
          sh /tmp/elan-init.sh -y --default-toolchain none
          echo "$HOME/.elan/bin" >> "$GITHUB_PATH"

      - name: Prep A — pin 核验＋工具链就位（独立计时）
        id: prepa
        run: |
          set -o pipefail
          rm -rf /tmp/m1-b1 && mkdir -p /tmp/m1-b1
          cp -r "$GITHUB_WORKSPACE/library/ns/." /tmp/m1-b1/
          cd /tmp/m1-b1
          # 钉核验（E-1：远端现行已钉 v4.35.0；漂移即红，防静默换基线）
          grep -q '@ "v4.35.0"' lakefile.lean \
            || { echo 'PIN DRIFT: mathlib require != v4.35.0'; exit 1; }
          grep -qx 'leanprover/lean4:v4.35.0' lean-toolchain \
            || { echo 'TOOLCHAIN DRIFT: lean-toolchain != v4.35.0'; exit 1; }
          START=$(date +%s)
          RC=0
          { /usr/bin/time -v lake --version ; } > toolchain.log 2>&1 || RC=$?
          END=$(date +%s)
          # 首次 lake 调用触发 v4.35.0 工具链下载，本步独立计时留痕（必修⑥③）
          echo "toolchain_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- toolchain provision exit=$RC, wall=$((END-START))s" >> "$GITHUB_STEP_SUMMARY"
          [ $RC -eq 0 ] || exit $RC

      - name: Prep B — mathlib cache get（独立计时＋命中哨兵）
        id: prepb
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          rm -f lake-manifest.json
          START=$(date +%s)
          RC=0
          { /usr/bin/time -v lake exe cache get ; } > cache.log 2>&1 || RC=$?
          END=$(date +%s)
          echo "cache_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- cache get exit=$RC, wall=$((END-START))s" >> "$GITHUB_STEP_SUMMARY"
          [ $RC -eq 0 ] || exit $RC
          # 必修⑤：命中哨兵——「断供而 rc=0」面封堵。
          # 哨兵口径：cache.log 须见 ≥1 条成功下载/解包计数行；格式钉以 11-03 空转
          # 实证为准（lake cache get 输出格式未在案——空转首项实证义务，fail-closed：
          # 格式不符即红，转分支乙，禁静默通行）
          grep -qE 'Downloaded|unpacking|Unpacking' cache.log \
            || { echo 'CACHE SENTINEL: no hit evidence in cache.log (miss-or-format-drift)'; exit 1; }

      - name: Build library @ v4.35.0（计时＋时长上界断言）
        id: build
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          START=$(date +%s)
          RC=0
          { /usr/bin/time -v lake build ; } > build.log 2>&1 || RC=$?
          END=$(date +%s); WALL=$((END-START))
          echo "build_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- build exit=$RC, wall=${WALL}s" >> "$GITHUB_STEP_SUMMARY"
          [ $RC -eq 0 ] || { grep -E 'error' build.log | head -120 >> "$GITHUB_STEP_SUMMARY" || true; exit $RC; }
          # 必修⑤第二哨兵：cache 命中下构建时长上界断言（TB-04 410s 命中先例 ×安全
          # 余量；上界值 1800s 为建议值，orchestrator 定）。越界即红——cache 假命中
          # 致全量重编时在此处 fail-closed，转分支乙而非慢烧
          [ $WALL -le 1800 ] || { echo "BUILD WALL ${WALL}s > 1800s — cache miss suspected"; exit 1; }

      - name: Export NDJSON（comparator 输入件；调用面照 spike A 实证链）
        id: export
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          # spike A #16/#21 在案链：lean4export/leanexport 产 NDJSON → comparator 消费。
          # 目标集（theorem_names/permitted_axioms/challenge）之精确 config 钉＝
          # B-2 第十一钉（必修⑦前置要件，11-03 前实证落钉）；本步骤命令行为该钉
          # 之占位形态，合入前以实证值替换——禁以未实证形态空转充四要件实证
          RC=0
          { lake env leanexport NsGalerkin > solution.ndjson ; } 2>>export.log || RC=$?
          echo "export_rc=$RC" >> "$GITHUB_OUTPUT"
          [ $RC -eq 0 ] || { cat export.log >> "$GITHUB_STEP_SUMMARY"; exit $RC; }
          sha256sum solution.ndjson | tee solution.ndjson.sha256

      - name: Comparator run — tee 落盘原始字节＋退出码闸（必修①）
        id: comparator
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          RC=0
          # 调用形态＝第十一钉实证值占位（spike A：config 五要件强制；bwrap 缺位
          # EXIT=2 拒跑——runner userns/bwrap 可用性列入空转检查单，禁
          # --inadvisably-no-sandbox 入 formal 跑批，spike A B2 行在案）
          { lake comparator --config comparator.config ; } 2>&1 | tee comparator-run.log || RC=$?
          echo "comparator_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- comparator exit=$RC" >> "$GITHUB_STEP_SUMMARY"
          # 必修①：rc≠0 即红，不进 Verdict 步骤——「打印 accepted 后崩溃」伪绿通道封堵
          [ $RC -eq 0 ] || exit $RC

      - name: Verdict 取值（物理末行语义＋退出码交叉承载，必修②）＋run_id 透传
        id: verdict
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          # 物理末行语义：日志最后一非空行必须逐字匹配证据形态——合并流后继注入行
          # 不再可覆盖真 verdict（GOS2 §2 伪造面封堵）；等价且严于「tail -n 5 窗口＋
          # 匹配行即最后一非空行」之野问处置口径
          LAST_NONEMPTY=$(awk 'NF{last=$0} END{print last}' comparator-run.log)
          if [ "$LAST_NONEMPTY" = "Your solution is okay!" ]; then
            V=accepted    # spike A #23 实证成功标记逐字值（E-3）
          else
            echo "VERDICT PHYSICAL-LAST-LINE MISMATCH: [$LAST_NONEMPTY]"; exit 1
          fi
          # 退出码交叉承载：comparator_rc==0 上游已闸，此处双要素一致性断言
          [ "${{ steps.comparator.outputs.comparator_rc }}" = "0" ] || exit 1
          {
            echo "verdict: $V"
            echo "run_id: gha:${GITHUB_RUN_ID}#${GITHUB_RUN_ATTEMPT}"
            echo "mode: ${{ inputs.mode }}"
            echo "head_branch: ${GITHUB_REF_NAME}"
          } > verdict.txt
          sha256sum comparator-run.log | tee comparator-run.log.sha256
          cat verdict.txt >> "$GITHUB_STEP_SUMMARY"

      - name: Upload artifacts（retention 90d；名按 mode 后缀，裸名永不产出——必修③）
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: ${{ inputs.mode == 'formal' && 'm1-b1-comparator-run-formal' || 'm1-b1-comparator-run-dryrun' }}
          retention-days: 90
          path: |
            /tmp/m1-b1/comparator-run.log
            /tmp/m1-b1/comparator-run.log.sha256
            /tmp/m1-b1/verdict.txt
            /tmp/m1-b1/solution.ndjson
            /tmp/m1-b1/solution.ndjson.sha256
            /tmp/m1-b1/toolchain.log
            /tmp/m1-b1/cache.log
            /tmp/m1-b1/build.log
            /tmp/m1-b1/export.log
          if-no-files-found: error
````

**v2 残留如实登记**：①`comparator.config`／`leanexport` 目标名为**第十一钉占位**，合入前以实证值替换（必修⑦）；②cache 哨兵正则之目标格式未在案，空转首项实证（fail-closed 设计：格式漂移即红不静默）；③`timeout-minutes: 170` 与 build 上界 `1800s` 为建议值，**终值 orchestrator 定**；④`if: always()` 上传在超时杀场景会产出无 verdict.txt 之包——分支丙检测口径已补（§二 A1.3 行）。

---

## 二、B-2 补钉清单升版 v2（必修④⑧⑨＋第十一/十二钉＋算术更正随附）

### 2.1 十钉升版（变更行标【v2】）

| # | 钉（v2 现行措辞） | 变更 |
|---|---|---|
| A1.1 | 空转＝`mode=dry-run` 全要素执行（含 comparator 实跑）；产物名带 `-dryrun` 后缀与 formal 物理区分（必修③联动），空转证据充 formal 回填之间隙以「验证 6：mode 逐字」＋名后缀双闸封堵 | 【v2 补强】 |
| A1.2 | 文件名 `verdict.txt`；字段拼写 `verdict: accepted`/`rejected`；**取值语义钉「物理末行」：日志最后一非空行逐字匹配证据形态（现行实证形态＝`Your solution is okay!` → accepted；E-3），禁 grep\|tail -1 全文匹配**；同文件必携 `run_id`/`mode`/`head_branch` 三行 | 【v2 改写，必修⑧②】 |
| A1.3 | artifact 名钉**按 mode 分裂**：formal 证据唯一下载键＝**`m1-b1-comparator-run-formal`**；dry-run＝`m1-b1-comparator-run-dryrun`；**裸名 `m1-b1-comparator-run` 任何 run 均不产出**（根治下载侧误取）；分支丙检测口径补「**包在而 verdict.txt 缺席即伪闭合**」（超时杀 `if: always()` 形态覆盖，必修⑤③）；跨 attempt 同名行为未实证警示在案（GOS2 §7，11-03 空转窗原地 re-run 实证） | 【v2 改写】 |
| A1.4 | 合入分支钉 main；**断言更正（必修⑧）：v1「workflow_dispatch 仅在默认分支可触发」为假**——API dispatches 端点接受 `ref` 参数可对任意含该文件之分支/tag 触发；补钉「**head_branch==main 为验证规程必查项**」（验证 7，见 §2.2），verdict.txt 内携 `head_branch` 行供对拍 | 【v2 更正＋补强】 |
| A2.1 | workflow_dispatch 手触（API POST /dispatches 或 UI）；残余小面照录野问：dispatch 权限主体建议钉「orchestrator 或执行席持票」 | 维持 |
| A2.2 | **取值脚本 v2 全量替换（必修④，见 §2.3）**：专用端点＋status/conclusion/head_branch 三重过滤＋空集显式报错转分支甲＋created_at≥dispatch 时刻对拍 | 【v2 替换】 |
| A3.1 | 注册表指针目标 `registry/TRUSTBOUNDARY-REGISTRY-01.md` §4.4 S2 行「当前证据指针」列（API 实测 L95） | 维持 |
| A3.2 | **重写（必修⑨，见 §三）**：验证 2 信任根＝仓内钉版 schema 副本（sha256 钉），文件头 URL 仅作漂移告警＋主机白名单（仅 `raw.githubusercontent.com`）；E-5 实证：文件头 dispatcher URL 现状对 v0.5 文件 rc=1 FAIL，**现状不可直用** | 【v2 重写】 |
| A3.3 | 下载主通道 REST API＋curl，备 gh CLI，双通道哈希复算闸 | 维持 |
| A4.1 | `gha:<run_id>#<attempt>` 记法；attempt≥2 注记义务；旁加警示「attempt=2 同名上传行为未实证（11-03 空转窗原地 re-run 实证，若 409 则名带 attempt 并同步修订 A1.3）」 | 【v2 补警示】 |
| A4.2 | 备通道机位由算力线协调席指名预置（≥8GB）；**指名登记死线升钉 2026-11-03 预飞闸前，逾期随分支甲呈裁**（必修⑧） | 【v2 升死线】 |

### 2.2 验证规程增列（GAPCLOSE §2.3 对接，供判定席采）

- **验证 0（新，必修①）**：run conclusion=success ∧ comparator 步骤 conclusion=success（API jobs 端点逐步骤对拍，禁仅看 run 总态）。
- **验证 4 修订（必修②）**：verdict 对拍基准改「日志最后一非空行」物理末行语义，与 verdict.txt 逐字一致；rejected 禁充 accepted 维持。
- **验证 6（新，必修③）**：verdict.txt `mode: formal` 逐字 ∧ artifact 名＝`m1-b1-comparator-run-formal`。
- **验证 7（新，必修⑧/A1.4）**：`head_branch==main`（verdict.txt 行 × API run 元数据双源对拍）。

### 2.3 A2.2 取值脚本 v2（必修④全要素）

```bash
# run_id 取值 v2（禁手抄）；gh_pat 名值分离；WF_ID 于 workflow 合入后经
# GET /actions/workflows 清单实测落钉（名值分列，禁预填）
WF_ID="<合入后实测落钉>"
DISPATCH_TS="<dispatch 发起时刻 UTC ISO8601，发起时即落>"
curl -sS -H "Authorization: Bearer $(cat /mnt/agents/.pivot-sec/gh_pat)" \
  "https://api.github.com/repos/chepin-ai/vci-inbox/actions/workflows/${WF_ID}/runs?per_page=1&status=completed" \
| python3 - "$DISPATCH_TS" <<'PYEOF'
import json,sys,datetime
ts=sys.argv[1]
runs=json.load(sys.stdin).get('workflow_runs',[])
if not runs:
    print('EMPTY SET — 转分支甲（dispatch 失败面）',file=sys.stderr); sys.exit(2)
r=runs[0]
assert r['conclusion']=='success', f"conclusion={r['conclusion']} — 非绿灯，转分支乙"
assert r['head_branch']=='main', f"head_branch={r['head_branch']} — 非 main，验证 7 不过"
assert r['created_at']>=ts, f"created_at={r['created_at']} < dispatch {ts} — 取到旧 run"
print(f"gha:{r['id']}#{r['run_attempt']}")
PYEOF
```

### 2.4 第十一钉（必修⑦：comparator 调用面，B-1 闭合前置要件）

- **已实证段（spike A #21–#24，E-3）**：`lake comparator` 为 v4.35.0 工具链原生内建；config 五要件强制（challenge/solution_module、theorem_names、permitted_axioms 显式声明）；bwrap 沙箱默认强制、缺位 EXIT=2 拒跑；`--inadvisably-no-sandbox` 输出自宣 not trustworthy，**formal 跑批禁用**；成功标记逐字 `Your solution is okay!`；`--paranoid` 六复核器并轨在案。
- **未实证段（11-03 预飞闸前必落）**：① NsGalerkin 目标之 config 精确内容（theorem_names 集合、challenge 来源、permitted_axioms 白名单值）；② rejected 情形出口码值（0/42 契约化体例是否成立——决定退出码承载语义完备性）；③ runner userns/bwrap 可用性；④ leanexport 目标名与 NDJSON 槽位。**实证结果（命令行、出口码表、verdict 行拼写）落钉后本钉方闭；dry-run 按实证形态跑，禁以未实证形态空转充四要件实证。**

### 2.5 第十二钉（必修⑥挂钉位）：elan-init.sh sha256

钉值 `a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53`（9823B，2026-10-26T11:16Z 实测）；**合入前复钉一次**（elan 上游可变），复钉出入即更新 workflow env 钉并登记双侧值（名值分列）。

### 2.6 随附更正（W2-P0-10③，lead 令并入；属 W10″ 时刻表与 GAPCLOSE §2.2-4 修订面，本席仅备措辞）

申报钉算术更正：**「2026-11-06＋5 工作日内＝2026-11-10」不成立——python3 复算 11-06 为周五，+5 工作日＝2026-11-13（E-7）**；建议改写为相对钉「**触发事件＋5 工作日**」并附实算锚例（二度失败 11-06 确诊 → 申报截止 2026-11-13）；GAPCLOSE §2.2-4 同病同步更正。11-08/11-15 均周日之「即日」口径呈裁属 R2 案 F，非本席裁量。

---

## 三、B-3 路径修订 v2（必修⑨：信任根与回填对象分离）

**E-5 实证三连击**：①文件头 dispatcher URL 对现行文件 **rc=1 FAIL**（version v0.5 不在 enum [v0.3, v0.4]）；②上游 `v0.5.schema.json` **404**；③直取 `v0.4.schema.json`（sha256 `25ff6b25…ce`，12694B）对现行文件及追加 machine_checks 样例均 **rc=0 PASS**。

**结论**：v1 路径乙「执行日动态取文件头 URL」**现状即不可用且自指**，废止。v2 钉：

1. **信任根＝仓内钉版副本**：建议 `ci/schema/formalization-v0.4.pinned.schema.json`（内容＝E-5③ 实测件，sha256 钉入 B-2；文件创建权归 orchestrator，本席不创建）；验证 2 一律对该副本跑。
2. **文件头 URL 仅作漂移告警**：执行日读取文件头 `$schema=` 值，主机白名单校验（仅允许 `raw.githubusercontent.com`；非白名单主机即红转申报），与钉版副本之上游来源比对仅登记漂移、不作校验依据。
3. **version 偏移呈裁登记**：formalization.yaml 声明 v0.5 而上游 schema 止于 v0.4——以 v0.4 schema 验 v0.5 文件之合法性**须判定席明示**（或文件 owner 更正 version 字段）；本席不裁。实证留存：rc=0 PASS 仅证结构兼容，不证版本语义对齐。
4. **本机/CI 双通道维持**：本机 check-jsonschema 0.38.2 已装妥实测（E-5 全部对拍即本机所跑）；CI 片段 v2 改为钉版副本校验（公网拉 schema 面消解，pip 公网面照 v1 登记）。

CI 片段 v2（替换 v1 路径乙）：

```yaml
      - name: Schema 核验 v2（钉版副本为信任根，必修⑨）
        run: |
          pip install check-jsonschema==0.38.2
          echo "25ff6b25ca4511635aff4443cf20480c15e59dddf19591c730950b442ea54fce  ci/schema/formalization-v0.4.pinned.schema.json" | sha256sum -c -
          check-jsonschema --schemafile ci/schema/formalization-v0.4.pinned.schema.json \
            library/ns/formalization.yaml
          # 漂移告警（非闸）：文件头声明主机白名单校验
          HEAD_URL=$(grep -m1 -oE '\$schema=\S+' library/ns/formalization.yaml | cut -d= -f2)
          case "$HEAD_URL" in
            https://raw.githubusercontent.com/*) echo "drift-alarm url host OK: $HEAD_URL" ;; 
            *) echo "SCHEMA URL HOST NOT IN WHITELIST: $HEAD_URL"; exit 1 ;;
          esac
```

---

## 四、九项逐项销记表（W2-P0-09）

| # | 原缺陷（GOS2/收割件钉） | 修法（本件落位） | 销记依据 |
|---|---|---|---|
| ① | comparator 步无退出码闸，「打印 accepted 后崩溃」即伪绿（GOS2 §1；v1 yaml L112–115） | Comparator 步尾 `[ $RC -eq 0 ] \|\| exit $RC`；验证 0 增列（§2.2） | §一 v2 yaml Comparator 步；残留验收：合入前桩 comparator（exit 3）dry-run 实证不伪绿——**实证义务在闭合链，本席文本层销记** |
| ② | verdict 取值＝全文最后匹配行，合并流注入可覆盖（GOS2 §2） | 物理末行语义（awk 最后一非空行逐字匹配实证形态 `Your solution is okay!`，E-3）＋comparator_rc==0 交叉承载断言；验证 4 基准同步修订 | §一 Verdict 步；§2.2；残留验收：伪造日志构造测试（rejected 行＋尾部注入 accepted 行）取真值实证——**同上闭合链义务** |
| ③ | dry-run/formal 产物同形同包同名，mode 不入五验（GOS2 §3） | artifact 名按 mode 后缀（-formal/-dryrun，裸名永不产出）＋验证 6 mode: formal 逐字——①②叠加采照裁决 | §一 Upload 步；§2.1 A1.1/A1.3；§2.2 验证 6 |
| ④ | A2.2 全局清单 per_page=3 三重失灵（GOS2 §4） | 专用端点 `/actions/workflows/<id>/runs?per_page=1&status=completed`＋conclusion/head_branch/created_at≥dispatch 三重断言＋空集显式报错转分支甲；端点形态 E-6 实证 | §2.3 脚本 v2；E-6 |
| ⑤ | 无 timeout-minutes＋cache miss rc=0 面未封＋分支丙口径缺形态（GOS2 §5） | job `timeout-minutes: 170`（建议值 orchestrator 定）；cache 命中哨兵（fail-closed）＋build 时长上界断言 1800s（建议值）；A1.3 补「包在 verdict.txt 缺席即伪闭合」 | §一 jobs 头/Prep B/Build 步；§2.1 A1.3；残留义务：11-03 空转人为 cache miss 实证 rc 行为 |
| ⑥ | elan 装裸 pipe 无哈希钉无重试、工具链下载混入 cache 计时（GOS2 §6） | 装脚本落盘→sha256 对拍（钉 E-4，入第十二钉）→执行；`--retry 3 --retry-delay 10`；Prep 拆 A（工具链）/B（cache）两步独立计时；先例复核：spike 该段亦无钉——非移植失真，新增补强如实登记 | §一 Install/Prep A/Prep B；§2.5；E-4 |
| ⑦ | `lake comparator` 调用面未实证、缓解断言过强（GOS2 §8） | 升格 B-1 闭合**前置要件**；第十一钉落实证段（spike A：原生内建/config 五要件/EXIT=2/成功标记逐字）＋未实证四项清单；裸 `lake comparator` 形态已被 E-2 grep 证伪并替换；v1「仅改命令行规程不动」断言撤回 | §2.4；E-2/E-3 |
| ⑧ | 十钉复检三死四半死三不死（GOS2 §9） | A1.2 物理末行改写、A1.4 断言更正＋head_branch==main 必查（验证 7）、A2.2 专用端点替换、A4.2 死线升钉 11-03；A1.3/A4.1 补跨 attempt 警示 | §2.1 全表【v2】行；§2.2 验证 7 |
| ⑨ | schema URL 自指信任环（GOS2 §10） | 信任根换仓内钉版副本（v0.4，sha256 25ff6b25…钉）；文件头 URL 降级为漂移告警＋主机白名单；E-5 实证 dispatcher 现状 rc=1 FAIL＋v0.5 上游 404——v1 路径乙废止；version 偏移合法性呈裁 | §三 v2 全节；E-5 |

**九项状态：文本层全落地（9/9）**；残留实证义务（桩 comparator 不伪绿／伪造日志取值／cache miss rc／attempt=2 re-run／第十一钉未实证四项）按裁决属 B-1 闭合链 11-03 前动作，非本席文本面，已逐项标明归属。

---

## 五、合规自检（本件行文）

1. **首行 CLASSIFY: L1**；gh_pat 名值分离零落值；日期全绝对 UTC(Z)。
2. **不编数**：E-1~E-7 全部 2026-10-26 实测（API 直连/curl/python3/check-jsonschema 0.38.2 本机实跑）；v1 的 lakefile pin 置换步骤因 E-1 实测漂移而改核验——基线以 API 真值为准（修-3 口径）。
3. **如实登记**：第十一钉未实证四项、cache 哨兵格式未在案、timeout/上界数值为建议值（裁决权 orchestrator）、version v0.5 vs v0.4 偏移呈裁、残留实证义务清单——无粉饰。
4. **甲席席规**：本件零工时数值；截止窗均引在案钉（11-03 预飞闸／W2-P0-09 窗）。
5. **权限边界**：仅新建 `board/WSH-S2-BLOCKER-DRAFT-02.md` 一件；**未触 `.github/`**；portal 只读零 git；ci/schema/ 钉版副本之创建权声明归 orchestrator；GO/NO-GO 与闭合判定权属判定席。
6. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** 退出码闸、物理末行、哈希对拍均为机器层必要条件证据，闭合判定须经独立复核与判定席裁决。

—— QF-OS 联邦批二十 W11 S2 阻塞闭合制备席 · 枢/PIVOT-01 体系 · 2026-10-26 · 返修令 W2-P0-09 · S2 责任窗硬钉 2026-11-06
