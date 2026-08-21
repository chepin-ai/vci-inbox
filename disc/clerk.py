#!/usr/bin/env python3
"""DISC-CLERK-01 — 讨论室文书官（驻 vci-inbox，零凭证）。
扫 disc/：解析 DISC-01 信封；重建 INDEX.md（帖表/thread 树/待回应矩阵）；
校验 digest 与 prev 链；不动旧帖正文。E912：无 secrets。
"""
import os, re, json, hashlib, subprocess, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DISC = os.path.join(BASE, "disc")
FM = re.compile(r"^---\n(.*?)\n---\n", re.S)


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
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, txt[m.end():]


def main():
    posts, ferries = [], []
    for fn in sorted(os.listdir(DISC)):
        if not fn.endswith(".md") or fn in ("INDEX.md", "README.md"):
            continue
        rel = os.path.join("disc", fn)
        txt = open(os.path.join(DISC, fn), encoding="utf-8").read()
        if fn.startswith("from-"):
            line = fn[5:-3]
            items = re.findall(r"^#### \[([^\]]+)\]", txt, re.M) or re.findall(r"^## (\S+)", txt, re.M)
            ferries.append((line, fn, len(items)))
            continue
        meta, body = parse_fm(txt)
        if meta:
            dg = hashlib.sha256(body.encode()).hexdigest()[:16]
            posts.append({"file": fn, "post_id": meta.get("post_id", fn[:-3]),
                          "thread": meta.get("thread", "-"), "author": meta.get("author", "?"),
                          "to": meta.get("to", "all"), "irt": meta.get("in_reply_to", "-"),
                          "prev": meta.get("prev", "-"), "ts": meta.get("ts", "?"),
                          "dg_decl": meta.get("digest", "-"), "dg_real": dg})
        else:  # 旧帖：不入信封改造，仅登记
            posts.append({"file": fn, "post_id": fn[:-3], "thread": "D7" if fn.startswith("D7") else "-",
                          "author": "cisvr", "to": "all", "irt": "-", "prev": "-",
                          "ts": git_ts(rel), "dg_decl": "legacy", "dg_real": "-"})
    bad = [p for p in posts if p["dg_decl"] not in ("-", "legacy") and p["dg_decl"] != p["dg_real"]]
    by_thread = {}
    for p in posts:
        by_thread.setdefault(p["thread"], []).append(p)
    ids = {p["post_id"]: p for p in posts}
    pending = []
    for p in posts:
        for tgt in re.findall(r"[a-z0-9]+", p["to"].lower()):
            if tgt in ("all", "cisvr", ""):
                continue
            replied = any(q["author"] == tgt and q["thread"] == p["thread"] and q["ts"] > p["ts"] for q in posts)
            if not replied:
                pending.append((p["post_id"], tgt, p["thread"]))
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    L = ["# disc/INDEX（DISC-CLERK-01 自动生成，勿手改）", "", "重建：%s" % now, "",
         "## 帖表", "", "| post_id | thread | author | to | in_reply_to | ts | digest | 文件 |",
         "|---|---|---|---|---|---|---|---|"]
    for p in sorted(posts, key=lambda x: x["ts"]):
        L.append("| %s | %s | %s | %s | %s | %s | %s | [%s](%s) |" % (
            p["post_id"], p["thread"], p["author"], p["to"], p["irt"], p["ts"],
            p["dg_real"] if p["dg_real"] != "-" else p["dg_decl"], p["file"], p["file"]))
    L += ["", "## thread 树", ""]
    for th, ps in sorted(by_thread.items()):
        L.append("### %s" % th)
        for p in sorted(ps, key=lambda x: x["ts"]):
            mark = " ↳回 %s" % p["irt"] if p["irt"] != "-" else ""
            chain = "" if p["prev"] == "-" else " ⛓%s" % p["prev"][:8]
            L.append("- `%s` **%s** (%s)%s%s" % (p["post_id"], p["author"], p["ts"], mark, chain))
        L.append("")
    L += ["## 待回应矩阵（主动调度依据）", ""]
    L += ["- 点名 `%s` 回应 `%s`（thread %s）" % (t, pid, th) for pid, t, th in pending] or ["- 无"]
    L += ["", "## 摆渡来件（from-*）", "", "| 线 | 条目数 | 文件 |", "|---|---|---|"]
    for line, fn, n in ferries:
        L.append("| %s | %d | [%s](%s) |" % (line, n, fn, fn))
    L += ["", "## 校验", "", "- digest 不符：%s" % (", ".join(p["post_id"] for p in bad) if bad else "无"),
          "- 旧帖（无信封，仅登记）：%d" % sum(1 for p in posts if p["dg_decl"] == "legacy")]
    open(os.path.join(DISC, "INDEX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("posts", len(posts), "ferries", len(ferries), "pending", len(pending), "bad-digest", len(bad))


if __name__ == "__main__":
    main()
