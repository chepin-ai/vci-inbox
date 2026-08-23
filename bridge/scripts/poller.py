#!/usr/bin/env python3
"""BRIDGE-POLLER-01 v3.4 — 公域指针摘要模式（驻 vci-inbox 公仓）。
v3.2 变更：注册双轨（url 主 + fallback 镜像轨）+ lines_status 探针注记带 ts（qlv 建议1/2，root 准）。
v3.1（防多副本冲突）：公域 disc/from-<线>.md 只落「小封头+摘要(≤400字)+正本指针」，
全量正文唯一归档在私域 ci-inbox/reading/（由 BRIDGE-GUARD-01 v2 ARCHIVE beat 直落）。
正本=各线出件箱；任何副本与正本 digest 不符即弃。E912 合规：无 secrets。
v3.4 变更：usrm-v1 支 body 回退（payload 缺省时取 body，对齐 outbox_append 双键）。"""
import json, hashlib, os, sys, time, urllib.request, datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # v3.3 fix: 仓根(scripts 在 bridge/scripts/)
REG = os.path.join(BASE, "bridge", "registry.json")
STATE = os.path.join(BASE, "bridge", "state.json")
DISC = os.path.join(BASE, "disc")


def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "bridge-poller/3.1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)[:120]


def digest(line, iid, ts):
    return hashlib.sha256(("%s|%s|%s" % (line, iid, ts)).encode()).hexdigest()[:16]


def _enrich(it, src):
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
            body = e.get("payload") or e.get("body") or ""
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
        for t_ in (cd.get("research-threads") or []):
            if isinstance(t_, dict):
                out.append(_enrich({"id": t_.get("id", "rt"), "ts": cd.get("meta", {}).get("lastUpdate", ""),
                                    "type": "thread", "to": ["all"],
                                    "body": "%s — %s%% | 阻塞:%s | 下一步:%s" % (t_.get("name", ""), t_.get("progress", "?"),
                                                                                  t_.get("blockers", "-"), t_.get("next", "-"))}, t_))
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


def fetch_line(cfg):
    """双轨：主 url 不通走 fallback 镜像轨。返回 (code, raw, via, used_url)"""
    code, raw, used = 0, "no-url", "-"
    for via in ("url", "fallback"):
        u = cfg.get(via)
        if not u:
            continue
        code, raw = fetch(u)
        if code == 200:
            return code, raw, via, u
        used = u
    return code, raw, "none", used


def main():
    reg = json.load(open(REG))
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"seen": {}, "runs": [], "lines_status": {}}
    st.setdefault("lines_status", {})
    os.makedirs(DISC, exist_ok=True)
    report = []
    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    for line, cfg in reg["lines"].items():
        code, raw, via, url = fetch_line(cfg)
        st["lines_status"][line] = {"ts": now, "code": code, "via": via}
        if code != 200:
            report.append("%s: HTTP %s（双轨俱废）" % (line, code or raw))
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
            hdr = "" if os.path.exists(path) else "# 摆渡来件：%s（指针摘要模式 v3.1）\n\n正本：%s\n全量归档：ci-inbox/reading/from-%s.md（私域单份）\n\n" % (line, url, line)
            with open(path, "a", encoding="utf-8") as f:
                if hdr:
                    f.write(hdr)
                for it in new:
                    dg = digest(line, it["id"], it["ts"])
                    to = "/".join(it["to"]) if isinstance(it["to"], list) else str(it["to"])
                    body = it["body"] if isinstance(it["body"], str) else json.dumps(it["body"], ensure_ascii=False)
                    summ = body[:400] + (" …[截断]" if len(body) > 400 else "")
                    f.write("\n#### [%s#%s] %s\n- schema: DISC-01 · type: %s → %s\n- thread: %s · in_reply_to: %s · digest: %s\n- 摘要：%s\n- 正本：%s #%s\n" % (
                        line, it["id"], it["ts"], it["type"], to or "all",
                        it["thread"], it["irt"], dg, summ.replace("\n", " ⏎ "), url, it["id"]))
                    st["seen"][dg] = now
        report.append("%s: 200(%s轨), %d 件, 新 %d" % (line, via, len(items), len(new)))
    st["runs"].append({"ts": now, "report": report})
    st["runs"] = st["runs"][-50:]
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)
    print("\n".join(report))


if __name__ == "__main__":
    main()
