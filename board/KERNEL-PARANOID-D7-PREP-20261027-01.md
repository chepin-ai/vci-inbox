CLASSIFY: L1
# KERNEL-PARANOID-D7-PREP-20261027-01 · QF-OS 联邦批三十（EXT-WAVE-41/42 面）· kernel 试点 D-7 预置稿（拉取预演＋机位执行序＋就绪度刷新）

- 席别：QF-OS 联邦批三十 S6 kernel 试点备产席（预置稿；不作终裁；零 git 操作）
- 时点：2026-10-27（UTC(Z)）
- 上游：board/KERNEL-PARANOID-PILOT-RUNBOOK-01.md（§2/§3/§4/§6）；board/KERNEL-PARANOID-D6-PREP-20261027-01.md（S1→S9/R1～R5/REPORT 骨架）；board/KERNEL-PARANOID-SEAT-REQ-20261027-01.md（通道实测）；board/KERNEL-PARANOID-PREFLIGHT-RUN-20261027-01.md（就绪基线）
- 口径纪律：涉 ζ 表述限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」，全件严禁且无「RH 已证」字样；涉 NS 表述限「**有限维 ODE 截断层**」语境
- 名值分离：通道/端点以名引用；脚本内钉值为常量名＝值分列；预演稿为**文本**，本批大件零下载、零实拉
- 只交付不入库：本件唯一新建；预演脚本本体以文本嵌于 §一（shebang 行一、CLASSIFY 行二纪律随文成型），不写入 ci/——执行席 11-03 取用后自行落盘

---

## 一、ghfast.top 拉取脚本预演稿（B 通道唯一实证可用面；单次零重试；双钉验收闸；失败即异常类呈裁）

通道实测钉：B1 ghfast.top HEAD 200/2.713388s（批二十九 §二）；A 直连面断（rc=28）；C 在位但不含目标件（增补申请另案 KERNEL-ARCHIVE-SUPPLEMENT-REQ-20261027-01）；D 排除。

```bash
#!/usr/bin/env bash
# CLASSIFY: L1
# kpar-fetch-toolchain.sh —— kernel 试点 D-7 拉取预演稿（文本交付；11-03 就位席落盘后执行）
# 纪律：单通道单次零重试（无 --retry）；双钉验收闸（字节数＋sha256）；失败即异常类呈裁（封存残件留证，不删）
# 出口码契约：0=双钉过；1=下载失败（通道异常）；2=钉不符（钉漂移事件，红线呈裁）；3=用法/环境错
set -euo pipefail
# —— 名值分离：名＝常量，值＝在案钉/实测通道 ——
readonly FETCH_URL_NAME='B1-ghfast.top'                                   # 通道名（名）
readonly FETCH_URL='https://ghfast.top/https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.tar.zst'
readonly EXPECT_BYTES='594481375'                                         # 字节钉（U17-KERNEL-PROBE-01 §1）
readonly EXPECT_SHA256='7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d'
: "${KPAR_FETCH_OUT:=/tmp/lean-4.35.0-linux.tar.zst}"
: "${KPAR_FETCH_LOG:=/tmp/kpar-fetch-$(date -u +%Y%m%dT%H%M%SZ).log}"
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
echo "$(ts) KPAR-FETCH start channel=${FETCH_URL_NAME} out=${KPAR_FETCH_OUT}" | tee -a "$KPAR_FETCH_LOG"
# 单次零重试：--fail 显式、无 --retry、--connect-timeout 仅约束建连（不设总时限——速率无实测钉，不编数）
if ! curl --fail --connect-timeout 30 -o "$KPAR_FETCH_OUT" -w 'http=%{http_code} ts=%{time_total}s bytes=%{size_download}B\n' \
     "$FETCH_URL" >>"$KPAR_FETCH_LOG" 2>&1; then
  echo "$(ts) KPAR-FETCH ABNORMAL stage=download rc=$? channel=${FETCH_URL_NAME} 残件封存=${KPAR_FETCH_OUT}（不删留证）→ 呈裁（D6-PREP R3 轨）" | tee -a "$KPAR_FETCH_LOG"
  exit 1
fi
GOT_BYTES="$(stat -c '%s' "$KPAR_FETCH_OUT")"
GOT_SHA256="$(sha256sum "$KPAR_FETCH_OUT" | awk '{print $1}')"
echo "$(ts) KPAR-FETCH fetched bytes=${GOT_BYTES} sha256=${GOT_SHA256}" | tee -a "$KPAR_FETCH_LOG"
if [ "$GOT_BYTES" != "$EXPECT_BYTES" ] || [ "$GOT_SHA256" != "$EXPECT_SHA256" ]; then
  echo "$(ts) KPAR-FETCH ABNORMAL stage=verify 实测 bytes=${GOT_BYTES} sha256=${GOT_SHA256} vs 双钉 ${EXPECT_BYTES}/${EXPECT_SHA256} → 钉漂移事件红线呈裁（D6-PREP R2 轨；禁续布）" | tee -a "$KPAR_FETCH_LOG"
  exit 2
fi
echo "$(ts) KPAR-FETCH PASS 双钉逐字一致 channel=${FETCH_URL_NAME}" | tee -a "$KPAR_FETCH_LOG"
exit 0
```

预演稿判读注记（名值分离）：①`-w` 读数为**当次实测**，不作速率估计（甲席席规）；②ABNORMAL 两轨出口码对应 D6-PREP 回退点 R2（钉漂移）/R3（通道异常）——呈裁件＝KPAR_FETCH_LOG 原始字节＋残件（不删）；③B1 败则按批二十九 §三选项树：B3（若补钉）→ C（若增补落成）→ R2 总回退；④本批未执行该脚本任何一行（文本预演）。

## 二、机位执行序与 REPORT 骨架目录（11-03→11-06）

**执行序**（D6-PREP S1→S9 之 D-7 插入形态，名值分列）：
1. **11-03**：S1 取证目录 → S2 v2 预检基线跑（预期 ENV-MISSING 群，登记用）→ **D-7 拉取（§一 预演稿落盘执行）** → S4 P-9 双钉对拍（预演稿内建闸＋v2 P-9 复闸双道）→ S5 解布 → S6 工具链面 v2 复跑（P-1a 逐字/P-2/P-3 roster——A-4 一手料）→ S7 cache（P-7，在案参照 110s）→ S8 锚件 elaboration（P-8，在案参照 72s）→ **GO 闸＝v2 全项无阻断 FAIL/ENV-MISSING**。
2. **11-04/05**：runbook §2 主流程（A-1 双导 → A-2 paranoid 主跑＋A-3 形态判 → A-4 名单析出 → A-5 双阴性控制 → A-6 公理闸 → A-7 资源读数）；11-04 前提＝不挤 S2 执行日算力（案 E 纪律），冲突全量滑 11-05。
3. **11-06**：收口——REPORT.md 按骨架成文＋manifest.sha256 封存＋报送（R2B-09 销记评估口／案 E 定谳庭材料口分流，runbook §六在案）。

**REPORT 骨架目录**（runbook §3.1 目录树＋D6-PREP §二 骨架文之合订，名值分离）：run 根 `kpar-pilot-01-<UTCts>/` 下 `env/`（预检全件＋A4 名单）·`export/`（双导＋exports.sha256）·`logs/`（A2 主跑/A5 控制/A6 公理/A7 资源）·`controls/`（双篡改件＋sha256）·`manifest.sha256`·`REPORT.md`（骨架预填版在 D6-PREP §二，实测列全〔待实测〕）。

## 三、就绪度自核表（批二十七「5 ready/5 pending」基线之批三十刷新）

| # | 就位项 | 批二十七态 | 批三十态（令牌：READY／PENDING／FILED-AWAIT） | 增量依据 |
|---|---|---|---|---|
| 1 | 预检脚本 | READY | **READY**（v2 增补 P-6a 替代支＋P-6c，试跑实证 PASS=5/FAIL=0） | 批二十八 §四 |
| 2 | lean-toolchain 钉文件 | READY | **READY**（P-4 PASS 不变） | 批二十七 §1.2 |
| 3 | 锚件在位 | READY | **READY**（不变） | 批二十七 §三 |
| 4 | bwrap 前提 | READY（本沙箱档） | **READY**（探针 v2 形定稿；执行席复测义务不变） | 批二十七 §一/批二十八 |
| 5 | 内存门槛 | READY（压线） | **READY**（口径钉修订入申请单：以 cgroup 实测 3,221,225,472B 为准） | 批二十九 §一 M-1′ |
| 6 | 磁盘取证路径 | PENDING | **READY**（v2 替代支脚本化＋实证；判读规程「portal 面不可判、容量证据取非 portal 面」在案） | 批二十八 §四.2 |
| 7 | P-9 供给通道 | PENDING | **READY（通道面）**——B1 实证 200/2.71s、选项树探测后形态定稿；拉取执行仍属 11-03 | 批二十九 §二/§三 |
| 8 | toolchain 实体＋对拍 | PENDING | **PENDING**（待 11-03 D-7 拉取＋双钉） | — |
| 9 | mathlib cache | PENDING | **PENDING**（待 11-03 S7） | — |
| 10 | 锚件 elaboration 复验 | PENDING | **PENDING**（待 11-03 S8） | — |
| 11 | 机位申请 | （未立） | **FILED-AWAIT**（KERNEL-PARANOID-SEAT-REQ-20261027-01 已呈，审批权属机位协调席） | 批二十九 §一 |
| 12 | 归档增补（C 冷备） | （未立） | **FILED-AWAIT**（KERNEL-ARCHIVE-SUPPLEMENT-REQ-20261027-01 已呈，执行权属归档线；非窗内硬前置） | 批三十 线一 |

**就绪度一行**：READY 7／PENDING 3（toolchain 实体、cache、elaboration——皆 11-03 序步内事项）／FILED-AWAIT 2（机位、归档增补）——通道面与脚本面全就绪，窗内阻塞项为零。

## 四、纪律自查

1. 口径律：ζ 双钉逐字在位；全件无「RH 已证」；涉 NS 限「有限维 ODE 截断层」语境（正文未涉 NS 对象）。
2. 名值分离：通道/端点/token 以名引用；预演稿常量名＝值分列；就绪令牌三分。
3. 不编数：双钉/延迟/字节数皆在案钉或实测转录；预演稿不设总时限（速率无实测钉）；零工时估计。
4. 大件零下载：预演稿为文本，本批未执行实拉；单次零重试入脚本形态（无 --retry）。
5. 只交付不入库：零 git；本件唯一新建；v1/v2 脚本及一切既有件一字未动。

—— QF-OS 联邦批三十 S6 kernel 试点备产席 · 2026-10-27 · 只交付不 commit
