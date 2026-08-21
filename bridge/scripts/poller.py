#!/usr/bin/env python3
"""BRIDGE-POLLER-01 — 零凭证摆渡器（驻 vci-inbox 公仓）。
读：六线发布域 outbox（公域 URL，匿名 GET 即可）。
写：本仓 disc/from-{line}.md（GITHUB_TOKEN，本仓自带）。
不留明文副本于 ci-control；摆渡=直落讨论室。
E912 合规：无 secrets 引用；负载无 ${{ 字面。
"""
import json, hashlib, os, sys, time, urllib.request, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
REG = os.path.join(BASE, "bridge", "registry.json")
STATE = os.path.join(BASE, "bridge", "state.json")
DISC = os.path.join(BASE, "disc")


def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "bridge-poller/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)[:120]


def digest(line, iid, ts):
    return hashlib.sha256(("%s|%s|%s" % (line, iid, ts)).encode()).hexdigest()[:16]


def normalize(line, doc):
    """四分 schema 归一 → [{id, ts, type, to, body}]。兼容一代旧式。"""
    out = []
    if not isinstance(doc, dict):
        return out
    if isinstance(doc.get("items"), list):                       # vinf v2
        for it in doc["items"]:
            out.append({"id": it.get("dtag") or it.get("id") or "item",
                        "ts": it.get("ts", ""), "type": it.get("dtag", "item"),
                        "to": ["all"], "body": it.get("body", "")})
    elif isinstance(doc.get("outbound"), list):                  # ucif2 v0.6.x
        for m in doc["outbound"]:
            out.append({"id": m.get("id", "msg"), "ts": m.get("ts") or doc.get("published_at", ""),
                        "type": m.get("type", "msg"), "to": m.get("to", []),
                        "body": m.get("body", "")})
    elif isinstance(doc.get("entries"), list):                   # usrm v1
        for e in doc["entries"]:
            body = e.get("payload")
            out.append({"id": "seq-%s" % e.get("seq"), "ts": e.get("ts", ""),
                        "type": e.get("intent", "entry"), "to": ["cisvr"],
                        "body": body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)})
    elif "cfts-dashboard" in doc:                                # cfts v8.x
        cd = doc["cfts-dashboard"]
        sr = cd.get("sitrep") or {}
        if sr:
            out.append({"id": "sitrep-" + sr.get("timestamp", "")[:16], "ts": sr.get("timestamp", ""),
                        "type": "sitrep", "to": ["all"],
                        "body": sr.get("overall", "") + " | " + json.dumps(sr.get("threads", sr.get("detail", "")), ensure_ascii=False)[:800]})
        for t in (cd.get("research-threads") or []):
            if isinstance(t, dict):
                out.append({"id": t.get("id", "rt"), "ts": cd.get("meta", {}).get("lastUpdate", ""),
                            "type": "thread", "to": ["all"],
                            "body": "%s — %s%% | 阻塞:%s | 下一步:%s" % (t.get("name", ""), t.get("progress", "?"),
                                                                      t.get("blockers", "-"), t.get("next", "-"))})
        for a in (cd.get("ack") or []):
            if isinstance(a, dict):
                out.append({"id": a.get("id", "ack"), "ts": a.get("ts", ""), "type": "ack",
                            "to": ["cisvr"], "body": json.dumps(a, ensure_ascii=False)[:400]})
    else:                                                        # 通用兜底
        for k in ("messages", "posts", "records"):
            if isinstance(doc.get(k), list):
                for m in doc[k]:
                    if isinstance(m, dict):
                        out.append({"id": m.get("id", k), "ts": m.get("ts", ""),
                                    "type": k, "to": m.get("to", ["all"]),
                                    "body": m.get("body") or json.dumps(m, ensure_ascii=False)[:600]})
                break
    return out


def main():
    reg = json.load(open(REG))
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"seen": {}, "runs": []}
    os.makedirs(DISC, exist_ok=True)
    report = []
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    for line, cfg in reg["lines"].items():
        url = cfg["url"]
        code, raw = fetch(url)
        if code != 200:
            report.append("%s: HTTP %s" % (line, code or raw))
            continue
        try:
            doc = json.loads(raw)
        except Exception:
            report.append("%s: 非JSON(%dB)" % (line, len(raw)))
            continue
        items = normalize(line, doc)
        new = [it for it in items if digest(line, it["id"], it["ts"]) not in st["seen"]]
        if new:
            path = os.path.join(DISC, "from-%s.md" % line)
            hdr = "" if os.path.exists(path) else "# 摆渡来件：%s\n\n来源：%s\n信任：%s\n\n" % (
                line, url, (doc.get("trust") if isinstance(doc.get("trust"), str) else
                            json.dumps(doc.get("trust", doc.get("law", "n/a")), ensure_ascii=False))[:160])
            with open(path, "a", encoding="utf-8") as f:
                if hdr:
                    f.write(hdr)
                for it in new:
                    f.write("\n## %s · %s · %s → %s\n\n%s\n" % (
                        it["id"], it["ts"], it["type"], "/".join(it["to"]) or "all", it["body"]))
                    st["seen"][digest(line, it["id"], it["ts"])] = now
        report.append("%s: 200, %d 件, 新 %d" % (line, len(items), len(new)))
    st["runs"].append({"ts": now, "report": report})
    st["runs"] = st["runs"][-50:]
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)
    print("\n".join(report))


if __name__ == "__main__":
    main()
