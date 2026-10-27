#!/usr/bin/env bash
# CLASSIFY: L1
# kernel-paranoid-preflight.sh —— QF-OS 联邦批二十七（EXT-WAVE-39）S4 件
# 规程正本：board/KERNEL-PARANOID-PILOT-RUNBOOK-01.md §1（P-1～P-8 就位预检）＋ P-9 tarball 对拍位
# 上游评估：board/KERNEL-PARANOID-EVAL-01.md §5/§6
#
# 判定令牌（名值分离，逐字）：
#   PASS        实测值满足判据
#   FAIL        实测值不满足判据（阻断性，除 P-6b）
#   ENV-MISSING 探测对象在环境中缺席（FAIL 之子类，单列计数）
#   SKIP        前置不满足而未执行（如可选参数未给）
#   DEGRADE     仅 P-6b 用：低于设定值门槛但不阻断（转 runbook §4 D-1b 预案标记）
#
# 退出码契约：0＝阻断性 FAIL 与 ENV-MISSING 均为零；1＝存在任一阻断性 FAIL/ENV-MISSING；2＝脚本自身用法错。
# 纪律：只读探测——除 $KPAR_OUT 证据目录外不写任何路径；不执行 git；不构建 Lean 工程
#       （P-7 cache get 与 P-8 锚件 elaboration 仅在工具与库面齐备时执行，缺席即 ENV-MISSING）。
#
# 参数（环境变量，名值分离）：
#   KPAR_LIB_DIR            library/ns 作业面路径（默认：. ）
#   KPAR_OUT                取证落点目录（默认：./kpar-preflight-<UTCts>）
#   KPAR_TOOLCHAIN_TARBALL  （可选）toolchain tarball 路径，给则执行 P-9 sha256 对拍
set -euo pipefail

# ---- 参数与取证落点 ----
: "${KPAR_LIB_DIR:=.}"
: "${KPAR_TOOLCHAIN_TARBALL:=}"
TS0="$(date -u +%Y%m%dT%H%M%SZ)"
: "${KPAR_OUT:=./kpar-preflight-${TS0}}"
mkdir -p "$KPAR_OUT"
LOG="$KPAR_OUT/preflight.log"
: > "$LOG"

N_PASS=0; N_FAIL=0; N_ENVMISS=0; N_SKIP=0; N_DEGRADE=0

emit() { # emit <文本> —— 终端与日志双写（原始行，不重排）
  printf '%s\n' "$1" | tee -a "$LOG"
}

verdict() { # verdict <项号> <令牌> <实测值/说明>
  local ts; ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  emit "${ts} $1 $2: $3"
  case "$2" in
    PASS)        N_PASS=$((N_PASS+1));;
    FAIL)        N_FAIL=$((N_FAIL+1));;
    ENV-MISSING) N_ENVMISS=$((N_ENVMISS+1));;
    SKIP)        N_SKIP=$((N_SKIP+1));;
    DEGRADE)     N_DEGRADE=$((N_DEGRADE+1));;
  esac
}

# ---- 钉值（名值分离：名＝探测项，值＝在案钉；出处随项标注）----
EXPECT_LEAN_VERSION='Lean 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release' # U17-KERNEL-PROBE-01 §1
EXPECT_TOOLCHAIN_PIN='leanprover/lean4:v4.35.0'   # lean-toolchain 钉，U17-KERNEL-PROBE-01 §1
EXPECT_TARBALL_SHA256='7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d' # U17-KERNEL-PROBE-01 §1
DISK_MIN_GIB=8   # 设定值（推导基线见 runbook §1.2：toolchain 0.594GB×1.5＋cache GB 级＋ns 230M×2＋导出/日志余量）
MEM_MIN_GIB=3    # 设定值（机位 4GB 在案；未达不阻断，转 D-1b 逐内核串行预案）
ROSTER='leanchecker leanchecker-paranoid lean4lean nanoda_bin con-leche con-ron leanexport' # 外部一手清单（solveathome #2597 件）
REQUIRED_ROSTER='leanchecker-paranoid lean4lean nanoda_bin con-leche'  # 评估件 §1.1 #15145 行枚举（con-ron 待 A-4 裁决，缺席不阻断）

emit "# KPAR preflight run 起始 ${TS0} ｜ KPAR_LIB_DIR=${KPAR_LIB_DIR} ｜ KPAR_OUT=${KPAR_OUT}"

# ---- P-1a lean --version 逐字对拍 ----
if ! command -v lean >/dev/null 2>&1; then
  verdict P-1a ENV-MISSING "lean 不在 PATH"
else
  V="$(lean --version 2>&1)" || V="rc=$? 输出：${V}"
  if [ "$V" = "$EXPECT_LEAN_VERSION" ]; then
    verdict P-1a PASS "lean --version 逐字一致"
  else
    verdict P-1a FAIL "实测='${V}'（预期钉：${EXPECT_LEAN_VERSION}）"
  fi
fi

# ---- P-1b elan 核验（在位则核对默认/就地解析工具链） ----
if ! command -v elan >/dev/null 2>&1; then
  verdict P-1b ENV-MISSING "elan 不在 PATH（注：在案席位以 tarball 直布 toolchain，elan 缺席不必然阻断——以 P-1a 为准）"
else
  EV="$(elan --version 2>&1 | head -n 1)"
  SHOW="$(cd "$KPAR_LIB_DIR" 2>/dev/null && elan show 2>&1 | tail -n 1)" || SHOW="elan show rc=$?"
  if printf '%s' "$SHOW" | grep -qF '4.35.0'; then
    verdict P-1b PASS "elan='${EV}'；elan show 解析='${SHOW}'"
  else
    verdict P-1b FAIL "elan='${EV}'；elan show 实测='${SHOW}'（预期含 4.35.0）"
  fi
fi

# ---- P-2 lake 在位且 check 子命令可解析（不触发构建） ----
if ! command -v lake >/dev/null 2>&1; then
  verdict P-2 ENV-MISSING "lake 不在 PATH"
else
  if lake check --help >"$KPAR_OUT/P2-lake-check-help.txt" 2>&1; then
    verdict P-2 PASS "lake check --help rc=0（输出落 P2-lake-check-help.txt）"
  else
    verdict P-2 FAIL "lake check --help rc=$?（输出落 P2-lake-check-help.txt）"
  fi
fi

# ---- P-3 捆绑内核二进制清单（名单实测落盘，供评估件 A-4） ----
TC_BIN=""
if command -v lean >/dev/null 2>&1; then TC_BIN="$(dirname "$(command -v lean)")"; fi
if [ -z "$TC_BIN" ]; then
  verdict P-3 ENV-MISSING "toolchain bin 目录不可定位（lean 缺席）"
else
  ROSTER_OUT="$KPAR_OUT/P3-preflight-roster.txt"; : > "$ROSTER_OUT"
  MISS_REQ=""
  for b in $ROSTER; do
    if [ -x "$TC_BIN/$b" ]; then printf 'present: %s\n' "$b" >> "$ROSTER_OUT";
    else printf 'MISSING: %s\n' "$b" >> "$ROSTER_OUT"; fi
  done
  for b in $REQUIRED_ROSTER; do
    if [ ! -x "$TC_BIN/$b" ]; then MISS_REQ="$MISS_REQ $b"; fi
  done
  if [ -n "$MISS_REQ" ]; then
    verdict P-3 FAIL "必需内核缺席:${MISS_REQ}（roster 落 P3-preflight-roster.txt；TC_BIN=${TC_BIN}）"
  else
    verdict P-3 PASS "必需内核齐（roster 落 P3-preflight-roster.txt；TC_BIN=${TC_BIN}）"
  fi
fi

# ---- P-4 lean-toolchain 钉逐字 ----
TC_FILE="$KPAR_LIB_DIR/lean-toolchain"
if [ ! -f "$TC_FILE" ]; then
  verdict P-4 ENV-MISSING "lean-toolchain 不见于 KPAR_LIB_DIR=${KPAR_LIB_DIR}"
else
  GOT_PIN="$(cat "$TC_FILE")"
  if [ "$GOT_PIN" = "$EXPECT_TOOLCHAIN_PIN" ]; then
    verdict P-4 PASS "lean-toolchain='${GOT_PIN}'"
  else
    verdict P-4 FAIL "实测='${GOT_PIN}'（预期钉：${EXPECT_TOOLCHAIN_PIN}）"
  fi
fi

# ---- P-5 bubblewrap 无 root 冒烟（官方沙箱前提，Linux-only） ----
# 探针 v2（批二十七试跑修订）：绝对路径 + 全根只读绑——v1（--ro-bind /usr /usr + 裸 true）
# 在批二十七沙箱实测 rc=1「execvp true: No such file or directory」（沙箱内 PATH/布局不解 bare true），
# 属探针缺陷非 bwrap 失效；v2 同沙箱实测 rc=0（KERNEL-PARANOID-PREFLIGHT-RUN-20261027-01 §一在案）。
if ! command -v bwrap >/dev/null 2>&1; then
  verdict P-5 ENV-MISSING "bwrap 不在 PATH → runbook §4 D-3c 两轨预案"
else
  if bwrap --ro-bind / / -- /usr/bin/true 2>"$KPAR_OUT/P5-bwrap-smoke.err"; then
    verdict P-5 PASS "bwrap --ro-bind / / -- /usr/bin/true rc=0（无 root 冒烟过）"
  else
    verdict P-5 FAIL "bwrap 冒烟 rc=$?（stderr 落 P5-bwrap-smoke.err；疑 unprivileged userns 被禁）"
  fi
fi

# ---- P-6a 磁盘门槛（设定值 ${DISK_MIN_GIB} GiB） ----
AVAIL_GIB="$(df -BG --output=avail "$KPAR_LIB_DIR" 2>/dev/null | tail -n 1 | tr -dc '0-9')"
if [ -z "$AVAIL_GIB" ]; then
  verdict P-6a FAIL "df 不可用（KPAR_LIB_DIR=${KPAR_LIB_DIR}）"
elif [ "$AVAIL_GIB" -ge "$DISK_MIN_GIB" ]; then
  verdict P-6a PASS "空闲=${AVAIL_GIB}GiB ≥ 设定值 ${DISK_MIN_GIB}GiB"
else
  verdict P-6a FAIL "空闲=${AVAIL_GIB}GiB < 设定值 ${DISK_MIN_GIB}GiB"
fi

# ---- P-6b 内存门槛（设定值 ${MEM_MIN_GIB} GiB；低于不阻断，记 DEGRADE） ----
MEM_AVAIL_GIB="$(free -g 2>/dev/null | awk '/^Mem:/{print $7}')"
if [ -z "$MEM_AVAIL_GIB" ]; then
  verdict P-6b FAIL "free 不可用"
elif [ "$MEM_AVAIL_GIB" -ge "$MEM_MIN_GIB" ]; then
  verdict P-6b PASS "Mem available=${MEM_AVAIL_GIB}GiB ≥ 设定值 ${MEM_MIN_GIB}GiB"
else
  verdict P-6b DEGRADE "Mem available=${MEM_AVAIL_GIB}GiB < 设定值 ${MEM_MIN_GIB}GiB → 标记 D-1b 逐内核串行预案"
fi

# ---- P-7 mathlib cache 就位（重操作：仅在 lake＋lakefile 齐备时执行） ----
if ! command -v lake >/dev/null 2>&1; then
  verdict P-7 ENV-MISSING "lake 缺席，cache get 不可执行"
elif [ ! -f "$KPAR_LIB_DIR/lakefile.lean" ] && [ ! -f "$KPAR_LIB_DIR/lakefile.toml" ]; then
  verdict P-7 SKIP "KPAR_LIB_DIR 无 lakefile（${KPAR_LIB_DIR}）"
else
  if (cd "$KPAR_LIB_DIR" && lake exe cache get) >"$KPAR_OUT/P7-cacheget.log" 2>&1; then
    CG_LINE="$(tail -n 1 "$KPAR_OUT/P7-cacheget.log")"
    if printf '%s' "$CG_LINE" | grep -q '9031'; then
      verdict P-7 PASS "尾行='${CG_LINE}'（在案钉：9031/9031，U17-KERNEL-PROBE-01 §1）"
    else
      verdict P-7 FAIL "rc=0 但尾行='${CG_LINE}' 未含 9031（见 P7-cacheget.log）"
    fi
  else
    verdict P-7 FAIL "lake exe cache get rc=$?（见 P7-cacheget.log；断供处置沿 B1-INFRA §3.2/3.3）"
  fi
fi

# ---- P-8 锚件独立 elaboration 复验（防陈旧 olean，沿 U17-KERNEL-PROBE-01 §4 先例） ----
ANCHOR="$KPAR_LIB_DIR/NsGalerkin/ZetaAnchor.lean"
if ! command -v lake >/dev/null 2>&1; then
  verdict P-8 ENV-MISSING "lake 缺席，锚件 elaboration 不可执行"
elif [ ! -f "$ANCHOR" ]; then
  verdict P-8 ENV-MISSING "锚件不见于 ${ANCHOR}"
else
  if (cd "$KPAR_LIB_DIR" && lake env lean NsGalerkin/ZetaAnchor.lean) >"$KPAR_OUT/P8-anchor-elab.log" 2>&1; then
    verdict P-8 PASS "ZetaAnchor.lean elaboration rc=0（在案参照 72s，U17-KERNEL-PROBE-01 §4）"
  else
    verdict P-8 FAIL "elaboration rc=$?（见 P8-anchor-elab.log）"
  fi
fi

# ---- P-9 toolchain tarball sha256 对拍位（可选：仅当 KPAR_TOOLCHAIN_TARBALL 给定） ----
if [ -z "$KPAR_TOOLCHAIN_TARBALL" ]; then
  verdict P-9 SKIP "KPAR_TOOLCHAIN_TARBALL 未给（对拍位留待 11-03 就位席执行）"
elif [ ! -f "$KPAR_TOOLCHAIN_TARBALL" ]; then
  verdict P-9 ENV-MISSING "tarball 不见于 ${KPAR_TOOLCHAIN_TARBALL}"
else
  GOT_SHA="$(sha256sum "$KPAR_TOOLCHAIN_TARBALL" | awk '{print $1}')"
  if [ "$GOT_SHA" = "$EXPECT_TARBALL_SHA256" ]; then
    verdict P-9 PASS "sha256 逐字一致（${GOT_SHA}）"
  else
    verdict P-9 FAIL "实测=${GOT_SHA}（预期钉：${EXPECT_TARBALL_SHA256}）"
  fi
fi

# ---- 汇总与退出码 ----
TS1="$(date -u +%Y%m%dT%H%M%SZ)"
emit "# KPAR preflight run 收口 ${TS1}"
emit "SUMMARY PASS=${N_PASS} FAIL=${N_FAIL} ENV-MISSING=${N_ENVMISS} SKIP=${N_SKIP} DEGRADE=${N_DEGRADE}"
if [ "$N_FAIL" -eq 0 ] && [ "$N_ENVMISS" -eq 0 ]; then
  emit "OVERALL: GO（无阻断性 FAIL/ENV-MISSING）"
  exit 0
else
  emit "OVERALL: NO-GO（阻断项＝FAIL+ENV-MISSING＝$((N_FAIL+N_ENVMISS))；处置沿 runbook §4 D-3）"
  exit 1
fi
