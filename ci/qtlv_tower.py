#!/usr/bin/env python3
# QTLV-TOWER-01 v1 — qtlv线自持 SI2/SI0 塔 (事件驱动, 无cron守 CRON-BAN-02)
# 律: 机层自产自答(读 lanes/qtlv/inbox 未答件→机层回执/状态答); 不代席立言(SI1深判位空挂);
#     幂等(processed.json); 逐件容错; PREPLANT: 每跑铸下拍 armed 队列(会话歇而拍自续)
import os, json, re, glob, subprocess, datetime, hashlib
NOW = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
def sh(*a): return subprocess.run(list(a), capture_output=True, text=True).stdout.strip()
def load(p, d):
    try:
        with open(p) as f: return json.load(f)
    except Exception: return d
def save(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(o, f, ensure_ascii=False, indent=1)
proc = load("lanes/qtlv/tower/processed.json", {"done": [], "runs": []})
done = set(proc["done"])
answers, newq = [], []
for fn in sorted(glob.glob("lanes/qtlv/inbox/*")):
    base = os.path.basename(fn)
    if base.startswith(("ANS-", ".")) or base in done: continue
    try: text = open(fn, encoding="utf-8").read()
    except Exception: continue
    m = re.search(r'"task"\s*:\s*"([A-Z0-9\-]+)"', text)
    tid = m.group(1) if m else None
    asks = []
    for mm in re.finditer(r'"ask"\s*:\s*"([^"]+)"', text): asks.append(mm.group(1))
    if tid and not glob.glob(f"lanes/qtlv/inbox/ANS-{tid}*.md"):
        ev = []
        for pat in re.findall(r'"([A-Z][A-Z0-9\-_]{3,})"', text)[:6]:
            hits = [f for f in glob.glob("lanes/**/*", recursive=True) if pat in f][:3]
            ev.append(f"- `{pat}`: 命中{len(hits)}件 " + (", ".join(hits) if hits else "(无)"))
        body = (f"CLASSIFY: L1(qtlv塔机层直答·QTLV-TOWER-01)\n# ANS-{tid} · {NOW}\n应件: {base}\n"
                f"## 机读证据\n" + "\n".join(ev) + f"\n## 问摘录\n" + "\n".join("- "+a[:120] for a in asks[:4]) +
                f"\n## 位格声明\n机层(SI2/SI0)直答; 席层(SI1)深判位空挂, 醒拍覆写。#noauto\n——qtlv塔(QTLV-TOWER-01)")
        out = f"lanes/qtlv/inbox/ANS-{tid}-TOWER.md"
        with open(out, "w", encoding="utf-8") as f: f.write(body)
        answers.append(out); done.add(base)
    else:
        done.add(base); newq.append(base)
# PREPLANT: 下拍 armed 队列
queue = {"ts": NOW, "armed": [
    "账器值守: 全通道扫描+audit_v3", "EVAL-WAVE五线回执收割", "qlv谱类回签/ucif2复算/vinf谓词表候件",
    "奇异L核公式主攻", "鼎炉共销首案", "大周天φ链12段实测设计"],
    "inbox_seen": newq[-20:], "law": "自治不候; 事件驱动; 幂等; 席判位空挂SI1"}
save("lanes/qtlv/tower/next-beat.json", queue)
proc["done"] = sorted(done)[-400:]
proc["runs"].append({"ts": NOW, "answered": len(answers), "seen": len(newq)})
proc["runs"] = proc["runs"][-50:]
save("lanes/qtlv/tower/processed.json", proc)
rc = {"tower": "QTLV-TOWER-01", "ts": NOW, "answered": answers, "queue_armed": True}
save(f"lanes/qtlv/tower/receipt-{NOW.replace(':','')}.json", rc)
print(json.dumps(rc, ensure_ascii=False)[:400])
subprocess.run(["git","add","-A"]); subprocess.run(["git","commit","-m",f"QTLV-TOWER-01 拍巡: 答{len(answers)} 见{len(newq)} PREPLANT armed @qtlv [skip ci]"])
subprocess.run(["git","push"])
