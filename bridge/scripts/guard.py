#!/usr/bin/env python3
"""BRIDGE-GUARD-01 — 双向搬运守护（驻 vci-inbox 公仓）。
IN : 本仓 disc/ 变动 → ci-inbox 私仓 archive/disc/（公面讨论即入私域存档）
OUT: ci-inbox/outbound/ → 本仓 disc/outbound/（私域指令即出公面）
凭证面：GITHUB_TOKEN 管本仓写；GUARD_APP_KEY（App 私钥，密封注入，值不出 runner）铸 token 管 ci-inbox。
E912/E913 合规；负载无 ${{ 字面；只打印计数，不打印内容。
"""
import json, os, time, hashlib, base64, urllib.request, datetime
import jwt

ORG = "chepin-ai"
PRIV = "ci-inbox"
APP_ID = "4621702"  # chepin-ci-ops 应用 ID（公开元数据，非秘密）
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISC = os.path.join(BASE, "disc")
STATE = os.path.join(BASE, "bridge", "guard-state.json")


def gh(url, token, method="GET", data=None):
    req = urllib.request.Request(
        url,
        headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json"},
        method=method,
        data=json.dumps(data).encode() if data is not None else None,
    )
    try:
        r = urllib.request.urlopen(req, timeout=30)
        b = r.read()
        return json.loads(b) if b else {"ok": r.status}
    except urllib.error.HTTPError as e:
        return {"_err": e.code}


def app_token():
    pk = os.environ["GUARD_APP_KEY"]
    now = int(time.time())
    t = jwt.encode({"iat": now - 60, "exp": now + 540, "iss": APP_ID}, pk, algorithm="RS256")
    insts = gh("https://api.github.com/app/installations", t)
    inst = [i for i in insts if i["account"]["login"] == ORG][0]
    r = gh("https://api.github.com/app/installations/%d/access_tokens" % inst["id"], t, method="POST", data={})
    return r["token"]


def sha_text(s):
    return hashlib.sha256(s.encode()).hexdigest()


def put_priv(tok, path, content, msg):
    cur = gh("https://api.github.com/repos/%s/%s/contents/%s" % (ORG, PRIV, path), tok)
    data = {"message": msg, "content": base64.b64encode(content.encode()).decode()}
    if isinstance(cur, dict) and cur.get("sha"):
        data["sha"] = cur["sha"]
    r = gh("https://api.github.com/repos/%s/%s/contents/%s" % (ORG, PRIV, path), tok, method="PUT", data=data)
    return isinstance(r, dict) and "commit" in r


def main():
    st = {"in": {}, "out": {}}
    if os.path.exists(STATE):
        st = json.load(open(STATE))
    tok = app_token()
    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    # IN：disc/ → ci-inbox/archive/disc/
    in_up = 0
    for root_, _dirs, files in os.walk(DISC):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(root_, fn)
            rel = os.path.relpath(full, DISC)
            txt = open(full, encoding="utf-8").read()
            h = sha_text(txt)
            if st["in"].get(rel) != h:
                if put_priv(tok, "archive/disc/" + rel, txt, "guard-IN: " + rel):
                    st["in"][rel] = h
                    in_up += 1

    # OUT：ci-inbox/outbound/ → disc/outbound/
    out_up = 0
    lst = gh("https://api.github.com/repos/%s/%s/contents/outbound" % (ORG, PRIV), tok)
    os.makedirs(os.path.join(DISC, "outbound"), exist_ok=True)
    if isinstance(lst, list):
        for f in lst:
            if f.get("type") != "file":
                continue
            if st["out"].get(f["name"]) == f.get("sha"):
                continue
            fc = gh(f["url"], tok)
            raw = base64.b64decode(fc["content"]).decode("utf-8", "replace")
            open(os.path.join(DISC, "outbound", f["name"]), "w", encoding="utf-8").write(raw)
            st["out"][f["name"]] = f.get("sha")
            out_up += 1

    st["last_run"] = now
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)
    print("guard IN:%d OUT:%d @%s" % (in_up, out_up, now))


if __name__ == "__main__":
    main()
