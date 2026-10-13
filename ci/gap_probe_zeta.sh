#!/usr/bin/env bash
# CLASSIFY: L1
# WS-64 · gap_probe_zeta — G3' absence probe (WS-62 scheme b, elaborator level,
# fail-closed). Runs inside the NS library directory (library/ns) with
# `lake env lean`. One probe file per candidate name (so one bad name cannot
# mask the attribution of another). Verdicts:
#   ABSENT  — stderr contains "unknown identifier '<name>'"  → absence TRUE
#   PRESENT — elaboration rc=0                                → name exists (probe negative)
#   UNKNOWN — any other failure, or control name `riemannZeta` itself fails
#             → environment untrusted; absence may NOT be reported (fail-closed)
set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIB_DIR="${NS_LIB_DIR:-$REPO_ROOT/library/ns}"
ART_DIR="$REPO_ROOT/artifacts/gap-probe"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$ART_DIR/zeta-probe-$TS.log"
mkdir -p "$ART_DIR"

IMPORTS="import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.Dirichlet"

CONTROL="riemannZeta"
CANDIDATES=("riemannZeta_ne_zero_of_one_le_re" "HardyZFunction")

probe_one() {
  # $1 = name ; prints verdict on stdout; appends full output to $LOG
  local name="$1" f out rc
  f="$(mktemp --suffix=.lean)"
  printf '%s\n#check @%s\n' "$IMPORTS" "$name" > "$f"
  out="$(cd "$LIB_DIR" && lake env lean "$f" 2>&1)"
  rc=$?
  {
    echo "===== probe: $name ====="
    echo "--- file ---"; cat "$f"
    echo "--- rc=$rc ---"; echo "$out"
  } >> "$LOG"
  rm -f "$f"
  if [ "$rc" -eq 0 ]; then
    echo "PRESENT"
  elif printf '%s' "$out" | grep -qF "unknown identifier '$name'"; then
    echo "ABSENT"
  else
    echo "UNKNOWN"
  fi
}

{
  echo "WS-64 G3' absence probe · $TS"
  echo "lib_dir=$LIB_DIR"
  echo "lean: $(cd "$LIB_DIR" && lake env lean --version 2>&1)"
  echo
} >> "$LOG"

ctrl="$(probe_one "$CONTROL")"
echo "control $CONTROL : $ctrl"

verdict="UNKNOWN"
if [ "$ctrl" != "PRESENT" ]; then
  echo "PROBE VERDICT: UNKNOWN (control $CONTROL failed; fail-closed, no absence claim)"
else
  all_absent=1
  for n in "${CANDIDATES[@]}"; do
    v="$(probe_one "$n")"
    echo "candidate $n : $v"
    [ "$v" = "ABSENT" ] || all_absent=0
  done
  if [ "$all_absent" -eq 1 ]; then
    verdict="ABSENT"
    echo "PROBE VERDICT: ABSENT=TRUE for all G3' candidates (${CANDIDATES[*]}) on mathlib v4.10.0"
  else
    echo "PROBE VERDICT: not all candidates absent (see above; per-name verdicts stand)"
  fi
fi

echo "log: $LOG"
# exit code: 0 = absence confirmed; 2 = UNKNOWN; 1 = at least one name present
[ "$verdict" = "ABSENT" ] && exit 0
[ "$verdict" = "UNKNOWN" ] && exit 2
exit 1
