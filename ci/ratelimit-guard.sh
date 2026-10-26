#!/usr/bin/env bash
# CLASSIFY: L1 —— QF-OS 批二十二 S-RL 限窗守卫（规程正本 board/RATELIMIT-GOVERNANCE-20261026-01.md）
# ratelimit-guard.sh —— 共享 PAT(名引用,零值落盘) rate-limit preflight 闸 + ETag 条件请求缓存辅助
#
# 退出码契约:
#   0  = 正常放行 (remaining >= RL_OK_AT)
#   42 = 降级建议 (RL_DEGRADE_AT <= remaining < RL_OK_AT): api 直连降 git ls-remote / 缓存 / 缓行
#   43 = 禁行     (remaining < RL_DEGRADE_AT): 仅战略储备授权之收口核验可动
#
# 名值分离纪律: token 值只经环境变量间接引用 (变量名由 RL_TOKEN_ENV 指定, 默认 GH_PAT),
# 本脚本任何路径不出现 token 字面量; 日志/缓存零 token 零响应体。
#
# 用法:
#   source ci/ratelimit-guard.sh
#   rl_preflight                 # 查 rate_limit(免费端点) 并按契约退出码返回
#   rl_cond_get <url>            # ETag 条件 GET: 304 命中零配额, 自动维护缓存与账簿
#   rl_etag_read <url>           # 打印该 URL 缓存之 ETag (无或过期则空, rc=1)
#   rl_etag_write <url> <etag>   # 写缓存
#   rl_ledger <method> <endpoint> <status> <charged> [note]   # 追加一行逐调用记账

set -u

# ---- 可调参数 (全部环境变量覆盖, 脚本内仅默认占位, 无业务硬编码) ----
: "${RL_API_BASE:=https://api.github.com}"     # API 基址
: "${RL_TOKEN_ENV:=GH_PAT}"                    # 持 token 值之环境变量名(名级引用)
: "${RL_UA:=qf-ratelimit-guard}"               # User-Agent 指纹
: "${RL_OK_AT:=1500}"                          # 绿/黄阈: remaining 低于此即降级建议
: "${RL_DEGRADE_AT:=500}"                      # 黄/红阈: remaining 低于此即禁行
: "${RL_CACHE_DIR:=${XDG_CACHE_HOME:-$HOME/.cache}/qf-ratelimit}"
: "${RL_CACHE_TTL:=300}"                       # 缓存条目寿命(秒)
: "${RL_NOCACHE:=(events|rate_limit)$|/repos/[^/]+/[^/]+$}"  # 高 churn 不缓存名单(正则)
: "${RL_LEDGER:=$RL_CACHE_DIR/ledger.jsonl}"   # 逐调用账簿
: "${RL_CALLER:=unknown-line/unknown-seat}"    # 调用者名级标识(线/席位)

# ---- 内部: 取 token 值 (名值分离, 不落任何文本) ----
_rl_token() {
    # 值经间接展开取自 RL_TOKEN_ENV 指名之环境变量; 未设置则空(匿名, 60/h 共享池)
    local name="$RL_TOKEN_ENV"
    printf '%s' "${!name:-}"
}

_rl_have() { command -v "$1" >/dev/null 2>&1; }

# ---- 内部: 发请求, 头落临时文件, 体落 stdout 所指文件; 打印 http_code ----
# 用法: _rl_fetch <method> <url> <body_out> <hdr_out> [extra_header...]
_rl_fetch() {
    local method="$1" url="$2" body_out="$3" hdr_out="$4"
    shift 4
    local tok args
    tok="$(_rl_token)"
    args=(-sS -X "$method" -D "$hdr_out" -o "$body_out"
          -H "Accept: application/vnd.github+json" -H "User-Agent: $RL_UA")
    if [ -n "$tok" ]; then
        args+=(-H "Authorization: Bearer $tok")
    fi
    local extra
    for extra in "$@"; do args+=(-H "$extra"); done
    curl "${args[@]}" -w '%{http_code}' "$url" 2>/dev/null
}

_rl_hdr() { # 从响应头文件取字段值(去 CR)
    tr -d '\r' < "$2" | awk -v k="$1" 'BEGIN{IGNORECASE=1} $1==k":"{print $2; exit}'
}

# ---- 逐调用记账: ts|caller|method|endpoint|status|used|remaining|charged|note ----
rl_ledger() {
    local method="$1" endpoint="$2" status="$3" charged="$4" note="${5:-}"
    mkdir -p "$RL_CACHE_DIR" 2>/dev/null || return 0
    printf '{"ts":"%s","caller":"%s","method":"%s","endpoint":"%s","status":"%s","charged":"%s","note":"%s"}\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$RL_CALLER" "$method" "$endpoint" "$status" "$charged" "$note" \
        >> "$RL_LEDGER" 2>/dev/null || true
}

# ---- preflight 闸: 查 rate_limit(免费, 不计 5000), 按 remaining 分级 ----
# 打印 remaining 与降级建议; 退出码 0/42/43
rl_preflight() {
    local body hdr code remaining reset
    body="$(mktemp)"; hdr="$(mktemp)"
    code="$(_rl_fetch GET "$RL_API_BASE/rate_limit" "$body" "$hdr")"
    if [ "$code" != "200" ]; then
        rm -f "$body" "$hdr"
        printf 'rl_preflight: rate_limit 查询失败 http=%s —— 无法读数, 按黄区降级建议处理\n' "$code" >&2
        rl_ledger GET /rate_limit "$code" FREE "preflight-fail"
        return 42
    fi
    if _rl_have jq; then
        remaining="$(jq -r '.resources.core.remaining' "$body")"
        reset="$(jq -r '.resources.core.reset' "$body")"
    else
        remaining="$(_rl_hdr x-ratelimit-remaining "$hdr")"
        reset="$(_rl_hdr x-ratelimit-reset "$hdr")"
    fi
    rm -f "$body" "$hdr"
    rl_ledger GET /rate_limit 200 FREE "preflight remaining=$remaining"
    printf 'rl_preflight: remaining=%s reset=%s (ok_at=%s degrade_at=%s)\n' \
        "$remaining" "$reset" "$RL_OK_AT" "$RL_DEGRADE_AT" >&2
    if [ "$remaining" -lt "$RL_DEGRADE_AT" ]; then
        printf 'rl_preflight: 红区禁行 —— 停一切非收口关键计费调用; 收口核验走 git ls-remote 单通道+补拍闭环(R2B-03a)\n' >&2
        return 43
    elif [ "$remaining" -lt "$RL_OK_AT" ]; then
        printf 'rl_preflight: 黄区降级建议 —— api 直连降 git ls-remote; 非关键读走 ETag 缓存/本地 git; 批量改缓行(>=6s 间隔)\n' >&2
        return 42
    fi
    printf 'rl_preflight: 绿区放行\n' >&2
    return 0
}

# ---- ETag 缓存层 ----
_rl_key() { # URL -> 缓存键 (sha256 前32hex)
    printf '%s' "GET $1" | sha256sum | cut -c1-32
}

_rl_cacheable() { # 高 churn 端点不缓存
    ! printf '%s' "$1" | grep -qE "$RL_NOCACHE"
}

rl_etag_read() { # <url> -> etag 或 rc=1
    local url="$1" f now mtime etag
    _rl_cacheable "$url" || return 1
    f="$RL_CACHE_DIR/$(_rl_key "$url")"
    [ -f "$f" ] || return 1
    etag="$(sed -n 1p "$f")"
    mtime="$(sed -n 2p "$f")"
    [ -n "$etag" ] && [ -n "$mtime" ] || return 1
    now="$(date -u +%s)"
    [ $((now - mtime)) -le "$RL_CACHE_TTL" ] || return 1
    printf '%s' "$etag"
    return 0
}

rl_etag_write() { # <url> <etag>
    local url="$1" etag="$2"
    _rl_cacheable "$url" || return 0
    [ -n "$etag" ] || return 0
    mkdir -p "$RL_CACHE_DIR" || return 0
    printf '%s\n%s\n' "$etag" "$(date -u +%s)" > "$RL_CACHE_DIR/$(_rl_key "$url")"
}

# ---- ETag 条件 GET: 304 命中零配额(实证见规程 §ET) ----
# 打印 http_code; body 落 stdout 重定向? 否——体落 $RL_CACHE_DIR/<key>.body 供调用方取
# 用法: code=$(rl_cond_get "https://api.github.com/repos/o/r/commits/<sha>")
rl_cond_get() {
    local url="$1" etag body hdr code charged
    body="$(mktemp)"; hdr="$(mktemp)"
    etag="$(rl_etag_read "$url" 2>/dev/null || true)"
    if [ -n "$etag" ]; then
        code="$(_rl_fetch GET "$url" "$body" "$hdr" "If-None-Match: $etag")"
    else
        code="$(_rl_fetch GET "$url" "$body" "$hdr")"
    fi
    case "$code" in
        304)
            charged=0  # 实证: 304 不计 used
            # 刷新缓存时间戳
            rl_etag_write "$url" "$etag"
            ;;
        200)
            charged=1
            rl_etag_write "$url" "$(_rl_hdr etag "$hdr")"
            if _rl_cacheable "$url"; then
                cp "$body" "$RL_CACHE_DIR/$(_rl_key "$url").body" 2>/dev/null || true
            fi
            ;;
        *)  charged=1 ;;
    esac
    rl_ledger GET "${url#"$RL_API_BASE"}" "$code" "$charged" "etag_cond"
    rm -f "$body" "$hdr"
    printf '%s' "$code"
}

# ---- 直接执行入口: ./ratelimit-guard.sh preflight ----
if [ "${BASH_SOURCE[0]:-}" = "${0:-}" ]; then
    case "${1:-preflight}" in
        preflight) rl_preflight ;;
        *) printf 'usage: %s preflight\n' "$0" >&2; exit 2 ;;
    esac
fi
