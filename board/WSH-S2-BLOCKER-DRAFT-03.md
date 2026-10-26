CLASSIFY: L1
# WSH-S2-BLOCKER-DRAFT-03 · S2 阻塞闭合草案返修版 v3（ATTACK-SCAN 维 1 攻击结论全落地）——评审稿，不闭合阻塞本身

- 席别：QF-OS 联邦批二十 W11 S2 阻塞闭合制备席（枢/PIVOT-01 体系）·续命返修二
- 成文时刻（date -u 实测）：**2026-10-26T11:50Z** 起取证、成文（UTC(Z) 单时钟域）
- 返修令：`board/ATTACK-SCAN-20261026-01.md` §一 维 1（A1-1 P0／A1-2 P0／A1-3、A1-4、A1-7 P1／A1-5、A1-6 P2；A2-3 随 A1-2 消解）
- 被修件：`board/WSH-S2-BLOCKER-DRAFT-02.md`（v2，本件全量替代其技术内容；v1/v2 保留在案不改写，append-only）
- 性质声明：本件仍为**闭合草案/评审稿**；**未创建/未修改 `.github/` 下任何文件**；portal 仓全程只读（API GET only），零 git 操作；合入权归 orchestrator 与判定席
- 纪律自检：首行 CLASSIFY: L1；gh_pat 名值分离零落值；不编数（action SHA／pip 哈希均 2026-10-26 实测落钉）；甲席席规（无工时数值）

---

## 〇、返修取证（2026-10-26T11:50Z 起实测）

| # | 实测项 | 结果 | 支撑 |
|---|---|---|---|
| F-1 | `actions/checkout` tag v4 解 SHA（api.github.com git/ref） | **`11d5960a326750d5838078e36cf38b85af677262`**（commit 型 ref） | A1-3 钉 |
| F-2 | `actions/upload-artifact` tag v4 解 SHA | **`ea165f8d65b6e75b540449e92b4886f43607fa02`**（commit 型 ref） | A1-3 钉 |
| F-3 | check-jsonschema 0.38.2 全量依赖哈希集 | 15 件 wheel 逐一 sha256 实测落钉（§三 requirements 全文）；`pip install --require-hashes --no-deps --dry-run` **rc=0** 验证通过 | A1-6 钉 |
| F-4 | 平台面如实登记 | F-3 哈希集中 charset_normalizer/regress/rpds-py 三件为 **cp312 manylinux** wheel——runner（ubuntu-latest）python 版本若 ≠3.12 则解析不同 wheel、哈希集失效；**钉版 requirements 须以 runner 平台实测重生成**（或 `--no-binary` 统一 sdist），合入前检查单增列此项 | A1-6 边界 |

---

## 一、B-1 workflow 草案 v3：`.github/workflows/m1-b1-baseline.yml` 全文（维 1 返修落位）

对 v2 之增量：**P0-1** artifact 名嵌 run_id+attempt；**P0-2** concurrency 组＋nonce 输入（env 绑定）＋取值脚本窗内唯一断言；**A1-3** actions/* 全钉 SHA；**A1-4** persist-credentials: false；**A1-5** 日志回显消毒。v2 既有结构（退出码闸／物理末行／钉核验／双哨兵／第十一钉占位）全数保留。

````yaml
# CLASSIFY: L1
# WSH-M1 G-3 / S2 · m1-b1 baseline 跑批 v3（ATTACK-SCAN 维 1 返修版）
# v3 增量：P0-1 artifact 名嵌 <run_id>-a<attempt>（attempt≥2 永不撞名，v4 同名 409
#   硬冲突外部实证在案）；P0-2 concurrency 组（排队不互杀）＋nonce 幂等锚（env 绑定、
#   禁内联表达式入 shell）；A1-3 actions/* 全量 SHA 钉；A1-4 persist-credentials:false；
#   A1-5 回显消毒。v2 层：退出码闸／物理末行 verdict／钉核验／cache+build 双哨兵。
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
      nonce:
        description: '一次性幂等锚（发起侧生成 uuid/随机串，回填对拍用；每次 dispatch 必新）'
        required: true
        type: string

permissions:
  contents: read

# P0-2：concurrency 组钉死——同组后到者排队、不互杀；cancel-in-progress 语义
# 裁定建议 false（防「取消中态」歧义致半态 run 产半成品工件），裁决权 orchestrator
concurrency:
  group: m1-b1-baseline
  cancel-in-progress: false

env:
  # elan-init.sh sha256 钉（2026-10-26 实测快照；合入前复钉，B-2 第十二钉位）
  ELAN_INIT_SHA256: "a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53"

jobs:
  baseline:
    runs-on: ubuntu-latest
    timeout-minutes: 170   # 野问建议值，终值 orchestrator 定（≤3h 封钉留上传余量）
    steps:
      # A1-3：全量 SHA 钉（F-1 实测）＋注释标版本；A1-4：凭据不落工作树
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262  # v4
        with:
          persist-credentials: false

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
          grep -q '@ "v4.35.0"' lakefile.lean \
            || { echo 'PIN DRIFT: mathlib require != v4.35.0'; exit 1; }
          grep -qx 'leanprover/lean4:v4.35.0' lean-toolchain \
            || { echo 'TOOLCHAIN DRIFT: lean-toolchain != v4.35.0'; exit 1; }
          START=$(date +%s)
          RC=0
          { /usr/bin/time -v lake --version ; } > toolchain.log 2>&1 || RC=$?
          END=$(date +%s)
          echo "toolchain_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- toolchain provision exit=$RC, wall=$((END-START))s" >> "$GITHUB_STEP_SUMMARY"
          [ $RC -eq 0 ] || exit $RC

      - name: Prep B — mathlib cache get（独立计时＋命中哨兵，fail-closed）
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
          grep -qE 'Downloaded|unpacking|Unpacking' cache.log \
            || { echo 'CACHE SENTINEL: no hit evidence (miss-or-format-drift)'; exit 1; }

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
          [ $WALL -le 1800 ] || { echo "BUILD WALL ${WALL}s > 1800s — cache miss suspected"; exit 1; }

      - name: Export NDJSON（第十一钉实证值占位，合入前替换）
        id: export
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          RC=0
          { lake env leanexport NsGalerkin > solution.ndjson ; } 2>>export.log || RC=$?
          echo "export_rc=$RC" >> "$GITHUB_OUTPUT"
          [ $RC -eq 0 ] || { cat export.log >> "$GITHUB_STEP_SUMMARY"; exit $RC; }
          sha256sum solution.ndjson | tee solution.ndjson.sha256

      - name: Comparator run — tee 落盘原始字节＋退出码闸
        id: comparator
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          RC=0
          # 调用形态＝第十一钉实证值占位；bwrap/userns 可用性（含沙箱内网络命名空间
          # 隔离子项，A1-4 联动）入空转检查单；formal 禁 --inadvisably-no-sandbox
          { lake comparator --config comparator.config ; } 2>&1 | tee comparator-run.log || RC=$?
          echo "comparator_rc=$RC" >> "$GITHUB_OUTPUT"
          echo "- comparator exit=$RC" >> "$GITHUB_STEP_SUMMARY"
          [ $RC -eq 0 ] || exit $RC

      - name: Verdict 取值（物理末行＋退出码交叉承载）＋run_id/nonce 透传
        id: verdict
        env:
          # P0-2：nonce 经 env 绑定传入（禁 ${{ }} 内联进 shell，维 1 通例）
          NONCE: ${{ inputs.nonce }}
          MODE_V: ${{ inputs.mode }}
        run: |
          set -o pipefail
          cd /tmp/m1-b1
          LAST_NONEMPTY=$(awk 'NF{last=$0} END{print last}' comparator-run.log)
          if [ "$LAST_NONEMPTY" = "Your solution is okay!" ]; then
            V=accepted
          else
            # A1-5：未消毒内容禁回显——printf '%q' 消毒后落日志/摘要
            printf 'VERDICT PHYSICAL-LAST-LINE MISMATCH: [%q]\n' "$LAST_NONEMPTY"
            exit 1
          fi
          [ "${{ steps.comparator.outputs.comparator_rc }}" = "0" ] || exit 1
          {
            echo "verdict: $V"
            echo "run_id: gha:${GITHUB_RUN_ID}#${GITHUB_RUN_ATTEMPT}"
            echo "mode: $MODE_V"
            echo "head_branch: ${GITHUB_REF_NAME}"
            echo "nonce: $NONCE"
          } > verdict.txt
          sha256sum comparator-run.log | tee comparator-run.log.sha256
          cat -v verdict.txt >> "$GITHUB_STEP_SUMMARY"

      - name: Upload artifacts（retention 90d；名嵌 run_id+attempt——P0-1）
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4
        with:
          # attempt≥2 同名 409 硬冲突封堵：名内嵌 run_id 与 attempt，任意重跑永不撞名；
          # 裸名/mode 裸后缀名均不产出
          name: m1-b1-comparator-run-${{ inputs.mode }}-${{ github.run_id }}-a${{ github.run_attempt }}
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

---

## 二、B-2 补钉清单 v3 增量（仅列变更行；v2 未变行照录有效）

| # | v3 现行措辞 | 变更 |
|---|---|---|
| A1.3 | artifact 名钉改**参数化形态**：`m1-b1-comparator-run-<mode>-<run_id>-a<attempt>`（formal 证据下载键＝`m1-b1-comparator-run-formal-<run_id>-a<attempt>`，run_id/attempt 自取值脚本 v3 落值后回填键方才完整）；分支丙「包在而 verdict.txt 缺席即伪闭合」维持 | 【v3 修订，P0-1】 |
| A2.1 | **dispatch 主体钉升格生效前置（A1-7）三要素成文**：①谁可触＝orchestrator 或执行席持票（其余持 write 权者禁触 formal）；②凭证名＝gh_pat（名引用）；③触发登记行格式＝`<UTC 时刻> <主体席别> dispatch m1-b1-baseline mode=<m> nonce=<n> ref=main` 落板随批；仓侧「谁持 write 权」清单（名级）随批收口登记 | 【v3 升格】 |
| A2.2 | 取值脚本 v3（§2.3）：窗内 run 数＝1 断言（>1 即红转分支甲）＋nonce 对拍（下载后 verdict.txt nonce 行 vs dispatch 登记值逐字） | 【v3 修订，P0-2】 |
| A4.1 | 警示升级：「attempt=2 同名上传行为未实证」改「**同名 409 硬冲突已获外部实证（upload-artifact v4 工件不可变）**」；名嵌 attempt 后跨 attempt 撞名结构性消解；注记义务（attempt≥2 注明取用）维持 | 【v3 更正，P0-1】 |

### 2.3 取值脚本 v3（P0-2 全要素）

```bash
# run_id 取值 v3；gh_pat 名值分离；WF_ID 合入后实测落钉
WF_ID="<合入后实测落钉>"
DISPATCH_TS="<dispatch 发起时刻 UTC ISO8601>"
curl -sS -H "Authorization: Bearer $(cat /mnt/agents/.pivot-sec/gh_pat)" \
  "https://api.github.com/repos/chepin-ai/vci-inbox/actions/workflows/${WF_ID}/runs?per_page=5&status=completed" \
| python3 - "$DISPATCH_TS" <<'PYEOF'
import json,sys
ts=sys.argv[1]
runs=json.load(sys.stdin).get('workflow_runs',[])
win=[r for r in runs if r['created_at']>=ts]
if not win:
    print('EMPTY SET — 转分支甲',file=sys.stderr); sys.exit(2)
# P0-2：窗内 run 数必须为 1——并发/双触发致锚错面 fail-closed
if len(win)>1:
    print(f'AMBIGUOUS: {len(win)} runs in window — 转分支甲',file=sys.stderr); sys.exit(3)
r=win[0]
assert r['conclusion']=='success', f"conclusion={r['conclusion']} — 转分支乙"
assert r['head_branch']=='main', f"head_branch={r['head_branch']} — 验证 7 不过"
print(f"gha:{r['id']}#{r['run_attempt']}")
PYEOF
# 下载 artifact 后补一拍：grep '^nonce: ' verdict.txt 与 dispatch 登记 nonce 逐字对拍
```

---

## 三、B-3 CI 片段 v3（A1-6：pip --require-hashes）

```yaml
      - name: Schema 核验 v3（钉版副本信任根＋pip 哈希钉）
        run: |
          pip install --require-hashes --no-deps -r ci/schema/cjs-requirements.txt
          echo "25ff6b25ca4511635aff4443cf20480c15e59dddf19591c730950b442ea54fce  ci/schema/formalization-v0.4.pinned.schema.json" | sha256sum -c -
          check-jsonschema --schemafile ci/schema/formalization-v0.4.pinned.schema.json \
            library/ns/formalization.yaml
          HEAD_URL=$(grep -m1 -oE '\$schema=\S+' library/ns/formalization.yaml | cut -d= -f2)
          case "$HEAD_URL" in
            https://raw.githubusercontent.com/*) echo "drift-alarm url host OK: $HEAD_URL" ;;
            *) echo "SCHEMA URL HOST NOT IN WHITELIST: $HEAD_URL"; exit 1 ;;
          esac
```

**`ci/schema/cjs-requirements.txt` 钉版全文**（F-3 实测 15 件 wheel 哈希；**平台边界照 F-4：runner python≠3.12 时须以 runner 平台实测重生成**，创建权归 orchestrator）：

```text
attrs==26.1.0 --hash=sha256:c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309
certifi==2026.10.23 --hash=sha256:e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1
charset-normalizer==3.5.2 --hash=sha256:3d31298449090ab8d47b7b1b2a555ff73cac7ed438a08b7ac160980c7ebed649
check-jsonschema==0.38.2 --hash=sha256:8edefe154b7117962f2e88318f315fc4bb9615827f932b37cb676a8d42a3a286
click==8.5.0 --hash=sha256:255bc9599cf7748b4b1a446ccc735421bd08a2ae529a8b88597d3de5664ee360
idna==3.20 --hash=sha256:ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c
jsonschema==4.26.0 --hash=sha256:d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce
jsonschema-specifications==2025.9.1 --hash=sha256:98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe
referencing==0.37.0 --hash=sha256:381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231
regress==2026.9.1 --hash=sha256:cb43e6daa63d68133e125b550f66cc9a1ce6830fede5a1eb87ece9607c7bb622
requests==2.34.2 --hash=sha256:2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0
rpds-py==2026.9.1 --hash=sha256:addeda51556dac7c1a2f14cda62db8b621cd12afba3091d03a96c72932387eab
ruamel-yaml==0.19.1 --hash=sha256:27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93
typing-extensions==4.16.0 --hash=sha256:481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8
urllib3==2.8.0 --hash=sha256:0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3
```

---

## 四、维 1 逐项销记表（攻击结论→修法→销记依据）

| # | 攻击结论（ATTACK-SCAN 钉） | 修法（本件落位） | 销记依据 |
|---|---|---|---|
| **P0-1**（A1-1） | attempt≥2 同名上传 409 硬冲突外部确证，「重试 ≤1」结构性必败 | artifact 名嵌 `-${{ github.run_id }}-a${{ github.run_attempt }}`，任意 attempt 永不撞名；回填取值链同步改（A1.3 参数化下载键＋A4.1 警示更正为「已证伪」）；采处置 (a) 保痕优于 overwrite | §一 Upload 步；§二 A1.3/A4.1；残留义务：11-03 空转窗原地 re-run 实证一次（原窗不变） |
| **P0-2**（A1-2） | 无 concurrency＋dispatch 非幂等，双 formal run 并存时取值静默锚错且全断言通过 | ①`concurrency: {group: m1-b1-baseline, cancel-in-progress: false}`——**语义裁定建议 false（排队不互杀、防取消中态半产物），裁决权 orchestrator**；②取值脚本窗内 run 数＝1 断言（>1 红转分支甲）；③nonce string 输入 env 绑定（禁内联）入 verdict.txt，下载后逐字对拍 | §一 concurrency 块/inputs/Verdict 步 env；§2.3 脚本 v3 |
| A1-3（P1） | actions/* 以可变 tag 引用，tj-actions CVE-2025-30066 先例正面命中 | checkout/upload-artifact 全量 40 位 SHA 钉（F-1/F-2 实测）＋注释标版本；后续升级走提案式（禁 tag 漂移回流）入 orchestrator 检查单 | §一 yaml 两 uses 行；F-1/F-2 |
| A1-4（P1） | checkout 默认 persist-credentials: true，凭据落 .git/config 而 comparator 消费外部提交物 | `persist-credentials: false` 显式钉（本 workflow 无 git 写，零成本）；第十一钉③ bwrap/userns 实证增列「沙箱内网络命名空间隔离」子项 | §一 checkout 步；§一 Comparator 步注释 |
| A1-5（P2，随修） | 未消毒日志回显可 ANSI 注入渲染伪 UI；取值面已封、展示面未封 | Verdict 步 MISMATCH 回显改 `printf '%q'` 消毒；STEP_SUMMARY 改 `cat -v`；验证规程补「工件日志一律经 cat -v 或等价消毒后阅读」一行（§二 A 系附则） | §一 Verdict 步 |
| A1-6（P2，lead 令入即修群） | pip 仅钉版本未钉哈希，不抗重打包/仓主劫持 | `pip install --require-hashes --no-deps -r ci/schema/cjs-requirements.txt`，15 件依赖哈希全量实测落钉（F-3，dry-run rc=0 验证）；平台边界 F-4 如实登记 | §三片段＋requirements 全文；F-3/F-4 |
| A1-7（P1） | dispatch 主体仅「建议钉」，任何持 write 权者可发起 formal 跑批 | 升格生效前置：主体/凭证名/登记行格式三要素成文（§二 A2.1）；仓侧 write 权清单名级随批登记 | §二 A2.1 |
| A2-3（P2，联动） | verdict.txt 自报字段对拍依赖锚定正确 run——不独立成险，放大 A1-2 | nonce 第三方绑定后「锚定的 run」与「自称的 run」一致性可验；随 P0-2 修复自动消解（攻击件原文口径照录） | §一 verdict.txt nonce 行；§2.3 末拍 |

**销记计数：维 1 攻击项 8/8 文本层落地**（P0×2、P1×3、P2×2、联动×1）；残留实证义务＝11-03 空转窗原地 re-run（P0-1）＋第十一钉四项（v2 结转），归属闭合链已在案。

**维 1 之外登记（不属本次返修面，如实结转）**：维 2 A2-2（同 runner 自签自证环／attestation 阶梯，涉 id-token/attestations 权限变更与现行最小权限钉冲突）——呈裁事项，本席不替裁；维 3/维 4 各条命中限窗规程与墓碑草案，非本件客体。

---

## 五、合规自检（本件行文）

1. **首行 CLASSIFY: L1**；gh_pat 名值分离零落值；日期全绝对 UTC(Z)。
2. **不编数**：action SHA（F-1/F-2）、15 件 wheel 哈希（F-3）、dry-run rc=0 均 2026-10-26 实测；v2 结转项照录 v2 实测出处。
3. **如实登记**：F-4 平台边界（cp312 wheel 与 runner python 版本耦合）、残留实证义务、A2-2 呈裁未裁、nonce/concurrency 语义裁定权归属——无粉饰。
4. **甲席席规**：零工时数值；窗钉全引在案（11-03 预飞闸／11-04 执行日）。
5. **权限边界**：仅新建 `board/WSH-S2-BLOCKER-DRAFT-03.md` 一件；**未触 `.github/`**；零 git；ci/schema/ 两钉版文件之创建权声明归 orchestrator；闭合判定权属判定席。
6. **页脚训诫（常设）**：**编译通过 ≠ 判定通过。** 全部闸与哈希钉均为机器层必要条件证据，闭合判定须经独立复核与判定席裁决。

—— QF-OS 联邦批二十 W11 S2 阻塞闭合制备席 · 枢/PIVOT-01 体系 · 2026-10-26 · 返修令 ATTACK-SCAN 维 1 · S2 责任窗硬钉 2026-11-06
