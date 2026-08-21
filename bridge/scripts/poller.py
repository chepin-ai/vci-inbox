#!/usr/bin/env python3
"""BRIDGE-POLLER-01 v3 — 零凭证摆渡器 + DISC-01 逐条小封（驻 vci-inbox 公仓）。
v3 变更：来件逐条带 #### [line#id] 小封（digest/thread/in_reply_to），
线方在 outbox item 里写 thread/in_reply_to 即被直译——解决「分不清谁发的、无法接链」。
E912 合规：无 secrets；负载无 Actions 表达式字面。
"""
import json, hashlib, os, sys, time, urllib.request, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(BASE, "bridge", "registry.json")
STATE = os.path.join(BASE, "bridge", "state.json")
DISC = os.path.join(BASE, "disc")


def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "bridge-poller/3.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)[:120]


def digest(line, iid, ts):
    return hashlib.sha256(("%s|%s|%s" % (line, iid, ts)).encode()).hexdigest()[:16]


def _enrich(it, src):
    """best-effort 抽取 thread/in_reply_to/to"""
    it.setdefault("thread", src.get("thread") or "-")
    it.setdefault("irt", src.get("in_reply_to") or src.get("reply_to") or "-")
    return it


def normalize(line, doc):
    """四分 schema 归一 → [{id, ts, type, to, body, thread, irt}]。"""
    out = []
    if not isinstance(doc, dict):
        return out
    if isinstance(doc.get("items"), list):                       # vinf v2
        for it in doc["items"]:
            out.append(_enrich({"id": it.get("dtag") or it.get("id") or "item",
                                "ts": it.get("ts", ""), "type": it.get("dtag", "item"),
                                "to": it.get("to", ["all"]), "body": it.get("body", "")}, it))
    elif isinstance(doc.get("outbound"), list):                  # ucif2 v0.6.x
        for m in doc["outbound"]:
            out.append(_enrich({"id": m.get("id", "msg"), "ts": m.get("ts") or doc.get("published_at", ""),
                                "type": m.get("type", "msg"), "to": m.get("to", []),
                                "body": m.get("body", "")}, m))
    elif isinstance(doc.get("entries"), list):                   # usrm v1
        for e in doc["entries"]:
            body = e.get("payload")
            out.append(_enrich({"id": "seq-%s" % e.get("seq"), "ts": e.get("ts", ""),
                                "type": e.get("intent", "entry"), "to": e.get("to", ["cisvr"]),
                                "body": body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)}, e))
    elif "cfts-dashboard" in doc:                                # cfts v8.x
        cd = doc["cfts-dashboard"]
        sr = cd.get("sitrep") or {}
        if sr:
            out.append({"id": "sitrep-" + sr.get("timestamp", "")[:16], "ts": sr.get("timestamp", ""),
                        "type": "sitrep", "to": ["all"], "thread": "-", "irt": "-",
                        "body": sr.get("overall", "") + " | " + json.dumps(sr.get("threads", sr.get("detail", "")), ensure_ascii=False)[:800]})
        for t in (cd.get("research-threads") or []):
            if isinstance(t, dict):
                out.append(_enrich({"id": t.get("id", "rt"), "ts": cd.get("meta", {}).get("lastUpdate", ""),
                                    "type": "thread", "to": ["all"],
                                    "body": "%s — %s%% | 阻塞:%s | 下一步:%s" % (t.get("name", ""), t.get("progress", "?"),
                                                                                  t.get("blockers", "-"), t.get("next", "-"))}, t))
        for a in (cd.get("ack") or []):
            if isinstance(a, dict):
                out.append(_enrich({"id": a.get("id", "ack"), "ts": a.get("ts", ""), "type": "ack",
                                    "to": ["cisvr"], "body": json.dumps(a, ensure_ascii=False)[:400]}, a))
    else:                                                        # 通用兜底
        for k in ("messages", "posts", "records"):
            if isinstance(doc.get(k), list):
                for m in doc[k]:
                    if isinstance(m, dict):
                        out.append(_enrich({"id": m.get("id", k), "ts": m.get("ts", ""),
                                            "type": k, "to": m.get("to", ["all"]),
                                            "body": m.get("body") or json.dumps(m, ensure_ascii=False)[:600]}, m))
                break
    for it in out:
        it.setdefault("thread", "-"); it.setdefault("irt", "-")
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
            hdr = "" if os.path.exists(path) else "# 摆渡来件：%s\n\n来源：%s\n\n" % (line, url)
            with open(path, "a", encoding="utf-8") as f:
                if hdr:
                    f.write(hdr)
                for it in new:
                    dg = digest(line, it["id"], it["ts"])
                    to = "/".join(it["to"]) if isinstance(it["to"], list) else str(it["to"])
                    f.write("\n#### [%s#%s] %s\n- schema: DISC-01 · type: %s → %s\n- thread: %s · in_reply_to: %s · digest: %s\n\n%s\n" % (
                        line, it["id"], it["ts"], it["type"], to or "all",
                        it["thread"], it["irt"], dg, it["body"]))
                    st["seen"][dg] = now
        report.append("%s: 200, %d 件, 新 %d" % (line, len(items), len(new)))
    st["runs"].append({"ts": now, "report": report})
    st["runs"] = st["runs"][-50:]
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)
    print("\n".join(report))


if __name__ == "__main__":
    main()
