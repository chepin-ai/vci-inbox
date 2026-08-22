#!/usr/bin/env python3
"""DISC-CLERK-01 v2 — 讨论室文书官 + 讨论件上链（驻 vci-inbox，零凭证）。
职责：
1) 扫 disc/*.md 解析 DISC-01 信封；必备字段缺失 → 不合规格件清单（INDEX 公示）。
2) 讨论件上链：disc/CHAIN.jsonl，append-only，逐帖 {seq, post_id, thread, author, ts,
   digest, prev, chain_hash}；chain_hash = sha256(prev_chain_hash|digest)[:16]，重算验链。
3) 重建 INDEX.md：帖表 / thread 树 / 待回应矩阵 / 链状态 / 校验。
E912：无 secrets；负载无 Actions 表达式字面。
"""
import os, re, json, hashlib, subprocess, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISC = os.path.join(BASE, "disc")
CHAIN = os.path.join(DISC, "CHAIN.jsonl")
FM = re.compile(r"^---\n(.*?)\n---\n", re.S)
MUST = ["post_id", "thread", "author", "ts", "digest", "in_reply_to", "prev"]


def git_ts(path):
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", path],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or "?"
    except Exception:
        return "?"


def parse_fm(txt):
    m = FM.match(txt)
    if not m:
        return None, txt
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, txt[m.end():]


def chain_hash(prev_h, dg):
    return hashlib.sha256(("%s|%s" % (prev_h, dg)).encode()).hexdigest()[:16]


def main():
    posts, ferries, bad_meta = [], [], []
    for fn in sorted(os.listdir(DISC)):
        if not fn.endswith(".md") or fn in ("INDEX.md", "README.md", "PROTOCOL.md", "READING.md") or fn.startswith("GUEST-") or fn.endswith("-DOCS.md"):
            continue
        txt = open(os.path.join(DISC, fn), encoding="utf-8").read()
        if fn.startswith("from-"):
            line = fn[5:-3]
            items = re.findall(r"^#### \[([^\]]+)\]", txt, re.M) or re.findall(r"^## (\S+)", txt, re.M)
            ferries.append((line, fn, len(items)))
            continue
        meta, body = parse_fm(txt)
        if meta:
            dg = hashlib.sha256(body.encode()).hexdigest()[:16]
            p = {"file": fn, "dg_real": dg}
            for k in MUST + ["to"]:
                p[k] = meta.get(k, "-")
            miss = [k for k in MUST if p[k] in ("-", "", "?")] or (p["digest"] != dg)
            if miss:
                bad_meta.append((p["post_id"], miss))
            posts.append(p)
        else:
            posts.append({"file": fn, "post_id": fn[:-3], "thread": "-", "author": "?",
                          "to": "-", "ts": git_ts(os.path.join("disc", fn)), "digest": "-",
                          "in_reply_to": "-", "prev": "-", "dg_real": "-"})
            bad_meta.append((fn[:-3], ["no-envelope"]))
    # ---- 上链 ----
    chain = []
    if os.path.exists(CHAIN):
        for ln in open(CHAIN, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                chain.append(json.loads(ln))
    in_chain = {c["post_id"] for c in chain}
    newposts = sorted([p for p in posts if p["post_id"] not in in_chain and p["dg_real"] != "-"],
                      key=lambda x: (x["ts"], x["file"]))
    prev_h = chain[-1]["chain_hash"] if chain else "GENESIS"
    seq = (chain[-1]["seq"] + 1) if chain else 1
    for p in newposts:
        h = chain_hash(prev_h, p["dg_real"])
        chain.append({"seq": seq, "post_id": p["post_id"], "thread": p["thread"],
                      "author": p["author"], "ts": p["ts"], "digest": p["dg_real"],
                      "prev": p["prev"], "chain_hash": h})
        prev_h, seq = h, seq + 1
    # 验链
    ph, broken = "GENESIS", []
    for c in chain:
        if chain_hash(ph, c["digest"]) != c["chain_hash"]:
            broken.append(c["post_id"])
        ph = c["chain_hash"]
    if newposts or not os.path.exists(CHAIN):
        with open(CHAIN, "w", encoding="utf-8") as f:
            for c in chain:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
    # ---- INDEX ----
    by_thread = {}
    for p in posts:
        by_thread.setdefault(p["thread"], []).append(p)
    pending = []
    for p in posts:
        for tgt in re.findall(r"[a-z0-9]+", p["to"].lower()):
            if tgt in ("all", "cisvr", ""):
                continue
            replied = any(q["author"] == tgt and q["thread"] == p["thread"] and q["ts"] > p["ts"] for q in posts)
            if not replied:
                pending.append((p["post_id"], tgt, p["thread"]))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    L = ["# disc/INDEX（DISC-CLERK-01 v2 自动生成，勿手改）", "", "重建：%s" % now, "",
         "## 帖表", "", "| post_id | thread | author | to | in_reply_to | prev | digest | 文件 |",
         "|---|---|---|---|---|---|---|---|"]
    for p in sorted(posts, key=lambda x: (x["ts"], x["file"])):
        L.append("| %s | %s | %s | %s | %s | %s | %s | [%s](%s) |" % (
            p["post_id"], p["thread"], p["author"], p["to"], p["in_reply_to"],
            p["prev"][:8], p["dg_real"][:8] if p["dg_real"] != "-" else "-", p["file"], p["file"]))
    L += ["", "## thread 树", ""]
    for th, ps in sorted(by_thread.items()):
        L.append("### %s" % th)
        for p in sorted(ps, key=lambda x: (x["ts"], x["file"])):
            mark = " ↳回 %s" % p["in_reply_to"] if p["in_reply_to"] != "-" else ""
            ch = "" if p["prev"] == "-" else " ⛓%s" % p["prev"][:8]
            L.append("- `%s` **%s** (%s)%s%s" % (p["post_id"], p["author"], p["ts"], mark, ch))
        L.append("")
    L += ["## 待回应矩阵（主动调度依据）", ""]
    L += ["- 点名 `%s` 回应 `%s`（thread %s）" % (t, pid, th) for pid, t, th in pending] or ["- 无"]
    L += ["", "## 链状态（讨论件上链）", "",
          "- 链高：%d · head：`%s` · 断链：%s" % (
              len(chain), chain[-1]["chain_hash"] if chain else "-",
              ", ".join(broken) if broken else "无"),
          "- 明细：[CHAIN.jsonl](CHAIN.jsonl)（append-only，chain_hash 逐环 sha256 绑定）",
          "", "## 摆渡来件（from-*）", "", "| 线 | 条目数 | 文件 |", "|---|---|---|"]
    for line, fn, n in ferries:
        L.append("| %s | %d | [%s](%s) |" % (line, n, fn, fn))
    L += ["", "## 校验", "",
          "- 不合规格件：%s" % (", ".join("%s(%s)" % (pid, "/".join(m)) for pid, m in bad_meta) if bad_meta else "无"),
          "- 断链：%s" % (", ".join(broken) if broken else "无")]
    open(os.path.join(DISC, "INDEX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("posts", len(posts), "chain", len(chain), "new", len(newposts),
          "pending", len(pending), "bad-meta", len(bad_meta), "broken", broken)


if __name__ == "__main__":
    main()
