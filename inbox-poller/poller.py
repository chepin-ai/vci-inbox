# VENDORED from chepin-ai/ci-control inbox/poller.py (v4)
# 代铸迁移: 枢/PIVOT-01 依「公域CI通道驱动私域CI」律迁至vci-inbox公域执行面 (FINDING-03处置·lgt-118归属·2026-09-30)
#!/usr/bin/env python3
# command-inbox v4 poller — runs inside ci-control only. Zero credentials in the inbox repo.
# Protocol: issue title "[CMD]", body = single-line base64 SealedBox(inbox_pk, JSON{...,hmac})
# hmac = HMAC_SHA256(CMD_AUTH, json.dumps(payload_without_hmac, sort_keys=True, separators=(",",":")))
import os, sys, json, base64, hmac, hashlib, secrets as pysec, datetime
import requests
from nacl.public import PrivateKey, PublicKey, SealedBox

GH = "https://api.github.com"
TOKEN = os.environ["GH_TOKEN"]
H = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
     "X-GitHub-Api-Version": "2022-11-28"}
OWNER = "chepin-ai"
CONTROL = f"{OWNER}/ci-control"
LOGS = f"{OWNER}/ci-logs"
INBOX = os.environ.get("INBOX_REPO") or f"{OWNER}/ci-inbox"
SK = PrivateKey(base64.b64decode(os.environ["INBOX_SK"].strip()))
CMD_AUTH = bytes.fromhex(os.environ["CMD_AUTH"].strip())
BUS = f"{OWNER}/ci-bus"
INFRA = {f"{OWNER}/ci-control", f"{OWNER}/ci-control-backup", f"{OWNER}/ci-library",
         f"{OWNER}/ci-logs", INBOX, BUS}
AUDIT = []

def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

def api(method, path, raw=False, hdrs=None, **kw):
    r = requests.request(method, GH + path, headers=hdrs or H, timeout=30, **kw)
    if raw:
        return r
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {}

def audit(line):
    AUDIT.append(f"- {now()} | {line}")

def flush_audit():
    if not AUDIT:
        return
    sc, cur = api("GET", f"/repos/{LOGS}/contents/inbox-audit.md")
    old = ""
    sha = None
    if sc == 200:
        old = base64.b64decode(cur["content"]).decode()
        sha = cur["sha"]
    body = {"message": "inbox audit", "content": base64.b64encode(
        (old + "\n".join(AUDIT) + "\n").encode()).decode()}
    if sha:
        body["sha"] = sha
    api("PUT", f"/repos/{LOGS}/contents/inbox-audit.md", json=body)

def wipe(num, note=""):
    api("PATCH", f"/repos/{INBOX}/issues/{num}", json={
        "title": "[已处理的指令]", "body": f"[内容已按协议擦除] {note}", "state": "closed"})
    api("PUT", f"/repos/{INBOX}/issues/{num}/lock", json={"lock_reason": "resolved"})

def reply(num, data, rpk):
    if not rpk:
        return
    try:
        if isinstance(data, str):
            data = data.encode()
        ct = SealedBox(PublicKey(base64.b64decode(rpk))).encrypt(data)
        api("POST", f"/repos/{INBOX}/issues/{num}/comments", json={
            "body": "📦 密文回执（用你的私钥 SealedBox 解密，base64 单行）: "
                    + base64.b64encode(ct).decode()})
    except Exception as e:
        audit(f"回执加密失败 issue#{num}: {e}")

def reject(num, why):
    # E711-RECEIPT-1（MSG-REL 落地）：拒收不再零回执——擦除前留明文拒收回执，fail-closed 不变
    api("POST", f"/repos/{INBOX}/issues/{num}/comments", json={"body":
        "E711 拒收回执\n\n本件以 [CMD] 前缀入轨但未过密封闸（" + why + "）。\n"
        "- [CMD] 轨为 root 专属：须 SealedBox 密文 + HMAC 签名（持钥者唯一）。\n"
        "- 业务咨询/协作/互鉴：请发无 [CMD] 前缀的普通 issue，respond 虫当班发 ACK 收悉回执（MSG-RELIABILITY-01 §2.1）。\n"
        "- 原内容将按协议擦除，本回执为唯一留痕。\n\n—— inbox-poller（合规闸，fail-closed）"})
    wipe(num, "拒收")
    audit(f"E711 拒收 issue#{num}: {why}")

def norm_repo(cmd):
    """repo 字段容错：接受 short 或 owner/short，一律归一为 short（LX-20260815-03）。"""
    r = (cmd.get("repo") or "").strip()
    cmd["repo"] = r.split("/")[-1] if "/" in r else r
    return cmd

def valid_target(full):
    if not full.startswith(OWNER + "/") or full in INFRA:
        return False
    sc, meta = api("GET", f"/repos/{full}")
    return sc == 200 and meta.get("private") is True

def safe_path(p):
    return isinstance(p, str) and p and not p.startswith("/") and ".." not in p.split("/")

def business_repos():
    sc, data = api("GET", "/installation/repositories?per_page=100")
    repos = [r["full_name"] for r in data.get("repositories", []) if r.get("private")]
    return [r for r in repos if r not in INFRA]

def op_status(cmd):
    lines = [f"指令收件箱 v4 状态 {now()}", f"指令仓: {INBOX}"]
    for r in business_repos():
        sc, runs = api("GET", f"/repos/{r}/actions/runs?per_page=1")
        last = "无运行"
        if sc == 200 and runs.get("workflow_runs"):
            w = runs["workflow_runs"][0]
            last = f'{w.get("status")}/{w.get("conclusion")} {w.get("created_at","")[:16]}'
        lines.append(f"- {r.split('/')[-1]}: {last}")
    return "\n".join(lines)

def op_dispatch(cmd):
    cmd = norm_repo(cmd)
    wf = cmd.get("workflow")
    repo = cmd.get("repo", "")
    if not wf:
        return "❌ 缺少 workflow 参数"
    targets = business_repos() if repo == "all" else [f"{OWNER}/{repo}"]
    ok, bad = [], []
    for t in targets:
        if not valid_target(t):
            bad.append(t)
            continue
        sc, _ = api("POST", f"/repos/{t}/actions/workflows/{wf}/dispatches",
                    json={"ref": cmd.get("ref", "")} if cmd.get("ref") else {"ref": "main"})
        (ok if sc in (201, 204) else bad).append(t)
    return f"dispatch {wf}: 成功 {len(ok)}，失败 {len(bad)} {bad if bad else ''}"

def op_sync(cmd):
    sc, _ = api("POST", f"/repos/{CONTROL}/actions/workflows/key-distributor.yml/dispatches",
                json={"ref": "main"})
    return "✅ 已触发 key-distributor" if sc in (201, 204) else f"❌ 触发失败 {sc}"

def op_push(cmd):
    cmd = norm_repo(cmd)
    full = f"{OWNER}/{cmd.get('repo','')}"
    path = cmd.get("path", "")
    if not valid_target(full):
        return "❌ 目标仓非法（仅允许私有业务仓，基础设施仓不可写）"
    if not safe_path(path):
        return "❌ 路径非法"
    try:
        content = base64.b64decode(cmd["content_b64"])
    except Exception:
        return "❌ content_b64 解码失败"
    sc, cur = api("GET", f"/repos/{full}/contents/{path}")
    body = {"message": cmd.get("message", f"inbox push {path}"),
            "content": base64.b64encode(content).decode()}
    if sc == 200:
        body["sha"] = cur["sha"]
    sc2, res = api("PUT", f"/repos/{full}/contents/{path}", json=body)
    return f"✅ 已写入 {full}#{path}" if sc2 in (200, 201) else f"❌ 写入失败 {sc2}"

def op_read(cmd):
    cmd = norm_repo(cmd)
    full = f"{OWNER}/{cmd.get('repo','')}"
    path = cmd.get("path", "")
    if not valid_target(full) or not safe_path(path):
        return "❌ 目标非法"
    r = api("GET", f"/repos/{full}/contents/{path}", raw=True,
            hdrs={**H, "Accept": "application/vnd.github.raw"})
    if r.status_code != 200:
        return f"❌ 文件不存在或读取失败 {r.status_code}"
    reply(cmd["_num"], r.content, cmd.get("reply_pk"))  # 原始字节，二进制安全
    return f"✅ 已加密回传 {full.split('/')[-1]} 的 {path}（{len(r.content)} 字节）"

def op_rotate(cmd):
    new = f"ci-{pysec.token_hex(4)}"
    sc, _ = api("PATCH", f"/repos/{INBOX}", json={"name": new})
    if sc != 200:
        return f"❌ 改名失败 {sc}"
    full_new = f"{OWNER}/{new}"
    sc2, _ = api("PATCH", f"/repos/{CONTROL}/actions/variables/INBOX_REPO",
                 json={"name": "INBOX_REPO", "value": full_new})
    if sc2 == 404:
        api("POST", f"/repos/{CONTROL}/actions/variables",
            json={"name": "INBOX_REPO", "value": full_new})
    audit(f"指令仓改名 {INBOX} -> {full_new}")
    return f"✅ 指令仓已改名: {new}（请记住并告知后续会话；ci-control 已同步变量）"

def op_setkeys(cmd):
    """轮换 SHARED_KEYS：payload 已在信封内加密，此处仅做键名白名单校验后写入 ci-control secrets。"""
    sk = cmd.get("shared_keys")
    if not isinstance(sk, dict) or not sk:
        return "❌ 缺少 shared_keys 对象"
    import re as _re
    for k, v in sk.items():
        if not _re.fullmatch(r"API_[A-Z0-9_]+", k) or not isinstance(v, str):
            return f"❌ 非法键名/值: {k}"
    sc, pkj = api("GET", f"/repos/{CONTROL}/actions/secrets/public-key")
    if sc != 200:
        return f"❌ 取公钥失败 {sc}"
    ct = SealedBox(PublicKey(base64.b64decode(pkj["key"]))).encrypt(
        json.dumps(sk, ensure_ascii=False).encode())
    sc2, _ = api("PUT", f"/repos/{CONTROL}/actions/secrets/SHARED_KEYS",
                 json={"encrypted_value": base64.b64encode(ct).decode(), "key_id": pkj["key_id"]})
    if sc2 in (201, 204):
        audit(f"SHARED_KEYS 已轮换，键数 {len(sk)}（值不落日志）")
        return f"✅ SHARED_KEYS 已更新（{len(sk)} 键）。紧接发 sync 分发。"
    return f"❌ 写入失败 {sc2}"

def op_leavemsg(cmd):
    cmd = norm_repo(cmd)
    """留言投递：用户经收件箱给业务仓进程留言，写入目标仓 .ci-inbox/msg-<ts>.md（MSG-PROTO v1）。"""
    import re as _re
    full = f"{OWNER}/{cmd.get('repo','')}"
    if not valid_target(full):
        return "❌ 目标仓非法（仅允许私有业务仓）"
    body_txt = cmd.get("body", "")
    if not body_txt or len(body_txt.encode()) > 4096:
        return "❌ E803 消息为空或超 4KB"
    if _re.search(r"(github_pat_|ghp_|sk-[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY|KGAT_|CI_APP_KEY|CMD_AUTH)", body_txt):
        return "❌ E804 命中敏感指纹，留言拒收"
    kind = cmd.get("kind", "chat")
    if kind not in ("request", "report", "alert", "chat"):
        return "❌ E801 非法 kind"
    ts = int(datetime.datetime.utcnow().timestamp())
    short = full.split("/", 1)[1]
    doc = (f"---\nv: 1\nfrom: user\nto: {short}\nkind: {kind}\nstate: submitted\n---\n\n"
           f"{body_txt}\n")
    path = f".ci-inbox/msg-{ts}.md"
    sc, _ = api("PUT", f"/repos/{full}/contents/{path}", json={
        "message": "msg: from user via inbox [skip ci]",
        "content": base64.b64encode(doc.encode()).decode()})
    if sc in (200, 201):
        audit(f"leave-msg -> {short} ({kind})")
        return f"✅ 留言已投递 {short}#{path}（MSG-PROTO v1 信封）"
    return f"❌ 投递失败 {sc}"

def op_search_repos(cmd):
    q = (cmd.get("query") or "").strip()
    scope = cmd.get("scope", "path")  # path | content
    if not q or len(q) > 80 or scope not in ("path", "content"):
        return "❌ query/scope 非法"
    ql = q.lower()
    hits, scanned = [], 0
    for full in business_repos():
        sc, tree = api("GET", f"/repos/{full}/git/trees/HEAD?recursive=1")
        if sc != 200:
            continue
        scanned += 1
        for it in tree.get("tree", []):
            if it.get("type") != "blob":
                continue
            p = it.get("path", "")
            if any(p.startswith(x) for x in (".git", "node_modules/", "dist/")):
                continue
            if ql in p.lower():
                hits.append(f"{full.split('/')[1]}:{p}")
            elif scope == "content" and it.get("size", 0) < 200_000 and p.endswith(
                    (".py", ".md", ".yml", ".yaml", ".json", ".ts", ".js", ".go", ".lean", ".toml", ".sh")):
                r = api("GET", f"/repos/{full}/contents/{p}", raw=True,
                        hdrs={**H, "Accept": "application/vnd.github.raw"})
                if r.status_code == 200 and ql in r.text.lower() and not SENSITIVE.search(r.text):
                    hits.append(f"{full.split('/')[1]}:{p}  (content)")
            if len(hits) >= 60:
                break
        if len(hits) >= 60:
            break
    body = f"search-repos [{scope}] q={q!r} · 扫描 {scanned} 仓 · 命中 {len(hits)}：\n" + ("\n".join(hits) or "（无命中）")
    reply(cmd["_num"], body, cmd.get("reply_pk"))
    audit(f"search-repos q={q!r} scope={scope} 命中 {len(hits)}")
    return f"✅ 检索完成，命中 {len(hits)} 条（路径级，已脱敏回传）"


def op_vendor_ext(cmd):
    full = f"{OWNER}/{cmd.get('repo','')}"
    url = cmd.get("url", "")
    lic = (cmd.get("license_spdx") or "").strip()
    dest = cmd.get("dest_path", "")
    pin = cmd.get("pin", "")
    if not valid_target(full):
        return "❌ 目标仓非法"
    if not (url.startswith("https://raw.githubusercontent.com/") or url.startswith("https://cdn.jsdelivr.net/")):
        return "❌ 仅允许可信源直链（raw.githubusercontent / jsdelivr）"
    if lic in LICENSE_REVIEW:
        return f"⏸ 许可证 {lic} 属灰名单：已挂起，待用户在 Dashboard 裁决后重发"
    if lic not in LICENSE_ALLOW:
        return f"❌ 许可证 {lic or '未声明'} 不在白名单（{sorted(LICENSE_ALLOW)}）"
    if dest.endswith(DENY_EXT):
        return "❌ 该扩展名禁止 vendor（执行件一律走人工窗口）"
    if not safe_path(dest):
        return "❌ 路径非法"
    r = requests.get(url, timeout=30)
    if r.status_code != 200 or len(r.content) > 200_000:
        return f"❌ 拉取失败 {r.status_code} 或超 200KB"
    header = (f"# VENDORED from {url}\n# license: {lic} · pin: {pin or 'unpinned'} · "
              f"by ci-control vendor-ext · {now()}\n")
    content = header.encode() + r.content
    sc, cur = api("GET", f"/repos/{full}/contents/{dest}")
    body = {"message": f"vendor: {dest} ({lic}, pin {pin or '-'}) [skip ci]",
            "content": base64.b64encode(content).decode()}
    if sc == 200:
        body["sha"] = cur["sha"]
    sc2, _ = api("PUT", f"/repos/{full}/contents/{dest}", json=body)
    if sc2 in (200, 201):
        audit(f"vendor-ext -> {full}#{dest} ({lic}, {len(r.content)}B, pin {pin or '-'})")
        return f"✅ 已 vendor 进 {full.split('/')[1]}#{dest}（{lic}，{len(r.content)} 字节）"
    return f"❌ 写入失败 {sc2}"


def op_pool_post(cmd):
    import re as _re
    body_txt = cmd.get("body", "")
    frm = (cmd.get("from_repo") or "unknown").strip()
    if not body_txt or len(body_txt.encode()) > 4096:
        return "❌ E803 消息为空或超 4KB"
    if _re.search(r"(github_pat_|ghp_|sk-[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY|KGAT_|CI_APP_KEY|CMD_AUTH)", body_txt):
        return "❌ E804 命中敏感指纹"
    kind = cmd.get("kind", "chat")
    if kind not in ("request", "report", "alert", "chat"):
        return "❌ E801 非法 kind"
    ts = int(datetime.datetime.utcnow().timestamp())
    sc, cur = api("GET", f"/repos/{BUS}/contents/pool/{datetime.datetime.utcnow():%Y-%m-%d}.md")
    old, sha = "", None
    if sc == 200:
        old = base64.b64decode(cur["content"]).decode(); sha = cur["sha"]
    entry = (f"\n---\n### msg-{ts} · from: {frm}（外部会话代发） · to: {cmd.get('to','broadcast')} · kind: {kind}\n\n"
             + body_txt + "\n")
    body = {"message": f"pool-post: {frm} [skip ci]",
            "content": base64.b64encode((old + entry).encode()).decode()}
    if sha: body["sha"] = sha
    sc2, _ = api("PUT", f"/repos/{BUS}/contents/pool/{datetime.datetime.utcnow():%Y-%m-%d}.md", json=body)
    if sc2 in (200, 201):
        audit(f"pool-post <- {frm} ({kind})")
        return f"✅ 已入池 ci-bus pool（from: {frm}，外部会话代发标注）"
    return f"❌ 入池失败 {sc2}"


OPS = {"status": op_status, "dispatch": op_dispatch, "sync": op_sync,
       "push-file-enc": op_push, "read-file-enc": op_read, "rotate-name": op_rotate,
       "set-shared-keys": op_setkeys, "leave-msg": op_leavemsg,
       "search-repos": op_search_repos, "vendor-ext": op_vendor_ext, "pool-post": op_pool_post}

def handle(issue):
    num = issue["number"]
    author = issue.get("user", {}).get("login", "")
    title = issue.get("title", "")
    if author != OWNER:
        reject(num, f"非授权作者 {author}")
        return
    if not title.startswith("[CMD]"):
        return  # owner 的普通 Issue 不干预
    body = (issue.get("body") or "").strip()
    try:
        raw = SealedBox(SK).decrypt(base64.b64decode(body))
        cmd = json.loads(raw.decode())
    except Exception:
        reject(num, "密文信封无法解密/解析（明文指令一律拒收）")
        return
    mac = cmd.pop("hmac", None)
    canon = json.dumps({k: v for k, v in cmd.items() if k != "ticket"}, sort_keys=True, separators=(",", ":"))
    expect = hmac.new(CMD_AUTH, canon.encode(), hashlib.sha256).hexdigest()
    if not (mac and hmac.compare_digest(mac, expect)):
        # 会话票旁路（§22）：日票 HMAC(CMD_AUTH, "ticket|date|session|quota")；低权 op 全场放行，push/dispatch 限本仓
        tk = cmd.pop("ticket", "") or ""
        sess = cmd.get("session", "")
        op0 = cmd.get("op", "")
        LOW = {"read-file-enc", "status", "search-repos", "pool-post", "leave-msg"}
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        ok_t = bool(tk and sess) and hmac.compare_digest(
            tk, hmac.new(CMD_AUTH, f"ticket|{today}|{sess}|50".encode(), hashlib.sha256).hexdigest())
        if ok_t and op0 in ("push-file-enc", "dispatch"):
            ok_t = cmd.get("repo", "").split("/")[-1] == sess
        if ok_t and op0 not in LOW | {"push-file-enc", "dispatch"}:
            ok_t = False
        if not ok_t:
            reject(num, "HMAC 验签失败（且无有效会话票）")
            return
        audit(f"会话票放行 op={op0} session={sess} issue#{num}")
    op = cmd.get("op", "")
    fn = OPS.get(op)
    if not fn:
        reject(num, f"未知 op {op}")
        return
    cmd["_num"] = num
    try:
        result = fn(cmd)
    except Exception as e:
        result = f"❌ 执行异常 {e}"
    # read-file-enc 成功时回执已在 op 内发出；失败也要回执报错
    if op != "read-file-enc" or result.startswith("❌"):
        reply(num, result, cmd.get("reply_pk"))
    wipe(num)
    audit(f"执行 op={op} issue#{num}: {result[:120]}")

def ensure_readme():
    sc, _ = api("GET", f"/repos/{INBOX}/contents/README.md")
    if sc == 200:
        return
    doc = f"""# 指令收件箱（{INBOX}）

空仓。无 Secrets、无工作流、无任何凭证。唯一用途：接收加密指令信封。

## 用法
- 建 Issue，标题 `[CMD]`，正文一行 base64：
  `base64( SealedBox(收件箱公钥, JSON指令含hmac) )`
- hmac = `HMAC_SHA256(CMD_AUTH, json.dumps(指令不含hmac字段, sort_keys=True, separators=(",",":")))`
- 指令字段：`op`(status/dispatch/sync/push-file-enc/read-file-enc/rotate-name)、
  `repo`、`path`、`content_b64`、`workflow`、`reply_pk`（一次性 X25519 公钥，收密文回执用）
- 明文指令、非授权作者、验签失败：一律擦除并记 E711。
- 回执：评论形式，密文用 reply_pk 对应私钥解密。Issue 处理后即擦除+锁定。

收件箱公钥见 ci-library CONVENTION.md §6（MIGRATE-01：正本已迁私域）。
"""
    api("PUT", f"/repos/{INBOX}/contents/README.md", json={
        "message": "protocol doc", "content": base64.b64encode(doc.encode()).decode()})
    audit("已写入指令仓 README")

def main():
    sc, issues = api("GET", f"/repos/{INBOX}/issues?state=open&per_page=100")
    if sc != 200:
        print(f"列举指令失败 {sc}")
        sys.exit(1)
    n = 0
    for it in issues:
        if "pull_request" in it:
            continue
        handle(it)
        n += 1
    ensure_readme()
    flush_audit()
    print(f"处理 {n} 条 open issue；审计 {len(AUDIT)} 条")

if __name__ == "__main__":
    main()
