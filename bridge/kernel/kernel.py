#!/usr/bin/env python3
# KERNEL-01 v0.1 · N/M/Δ 形式化自动机内核（修订版：评审单 2026-08-23 照收）
# 修订：G-N1 改判据（对摆渡归档而非 relayed-state）；+G-N6 裸done；+G-M2b 红项悬置；
#       +G-D3 引 gate 裁决；+G-K0-lite 哨兵互守；FINDING 生命周期（复发计数+告警去重）
import json, os, glob, hashlib, datetime, urllib.request, base64, re

HUB = os.environ.get('HUB_TOKEN', '')
def gh(path):
    r = urllib.request.Request('https://api.github.com' + path, headers={'Authorization': 'Bearer ' + HUB, 'Accept': 'application/vnd.github+json'})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, resp.read()
    except Exception as e:
        return getattr(e, 'code', 0), None

def getc(repo, path):
    s, b = gh('/repos/chepin-ai/%s/contents/%s' % (repo, path))
    if s != 200: return None
    return base64.b64decode(json.loads(b)['content']).decode('utf-8', 'replace')

NOW = datetime.datetime.now(datetime.UTC)
TS = NOW.strftime('%Y-%m-%dT%H:%M:%SZ')
def age_h(ts):
    try:
        t = datetime.datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
        if t.tzinfo is None: t = t.replace(tzinfo=datetime.UTC)
        return (NOW - t).total_seconds() / 3600
    except Exception:
        return 9999

# FINDING 生命周期台账
led = json.loads(getc('ci-control', 'bridge/findings/ledger.json') or '{}')
def fid(rule, detail):
    return hashlib.sha256((rule + detail[:60]).encode()).hexdigest()[:10]
F = []
def finding(rule, detail):
    k = fid(rule, detail)
    e = led.get(k, {'first': TS, 'recur': 0, 'state': 'open'})
    e['recur'] += 1; e['last'] = TS
    led[k] = e
    struct = e['recur'] >= 3
    F.append({'rule': rule, 'detail': ('[STRUCT] ' if struct else '') + detail, 'fid': k, 'recur': e['recur']})

# --- 状态装载 ---
D = json.loads(getc('ci-control', 'bridge/DIRECTIVES.json') or '{"items":[]}')
items = D['items']
CHAIN = getc('vci-inbox', 'disc/CHAIN.jsonl') or ''
chain_h = len([l for l in CHAIN.strip().splitlines() if l.strip()])
INDEX = getc('vci-inbox', 'disc/INDEX.md') or ''
BOARD = getc('ci-control', 'bridge/situation/BOARD-01.md') or ''
CHANNELS = getc('ci-control', 'bridge/CHANNELS-01.md') or ''

# G-DIR 指令保鲜：open 且 lts 超 72h
for i in items:
    if i.get('state') == 'open' and age_h(i.get('lts', D.get('updated', TS))) > 72:
        finding('G-DIR-stale-open', '%s open 超 72h：%s' % (i['id'], i['d'][:40]))

# G-N6 迭代必验效：done/verified 必须带非空实证
for i in items:
    if i.get('state') in ('done', 'verified') and not str(i.get('ev', '')).strip('- '):
        finding('G-N6-bare-done', '%s 标 %s 无实证' % (i['id'], i['state']))

# G-N8 岗报必呈
mm = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', BOARD)
if not mm or age_h(mm.group(1)) > 24: finding('G-N8', 'BOARD 超 24h 未刷新')

# G-M2 静默必勾（账未刷）
mm = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', CHANNELS)
if not mm or age_h(mm.group(1)) > 48: finding('G-M2', 'CHANNELS 超 48h 未刷')
# G-M2b 红项悬置（刷了但红/黄项仍在）
for line in CHANNELS.splitlines():
    if ('✗' in line or '⚠️' in line) and '|' in line:
        finding('G-M2b-open-red', '信道红/黄项悬置：%s' % line.split('|')[1].strip()[:40])

# G-Δ3 残差即案：链滞后（最新帖与链尾 ts 差 >2h）
s, b = gh('/repos/chepin-ai/vci-inbox/contents/disc')
if s == 200:
    mds = sorted([f['name'] for f in json.loads(b) if f['name'].endswith('.md') and f['name'] not in ('PROTOCOL.md', 'DISC-POST.md')], reverse=True)[:5]
    newest_post_ts = ''
    for m in mds:
        c = getc('vci-inbox', 'disc/' + m) or ''
        mm = re.search(r'^ts:\s*(\S+)', c, re.M)
        if mm and mm.group(1) > newest_post_ts: newest_post_ts = mm.group(1)
    tail_ts = ''
    if CHAIN.strip():
        tail_ts = json.loads(CHAIN.strip().splitlines()[-1]).get('ts', '')
    if newest_post_ts and tail_ts and age_h(tail_ts) - age_h(newest_post_ts) > 2:
        finding('G-D3', '链滞后：最新帖 %s 链尾 %s 差超 2h' % (newest_post_ts, tail_ts))
gate = json.loads(getc('vci-inbox', 'bridge/gate/last-report.json') or '{}')
if gate.get('verdict') not in ('GREEN', None):
    finding('G-D3-gate', 'gate 裁决 %s' % gate.get('verdict'))
if gate and age_h(gate.get('ts', '')) > 6:
    finding('G-D3-gate-stale', 'gate 报告超 6h 未新（哨兵沉默）')

# G-BOX deliverbox 值守
s, b = gh('/repos/chepin-ai/ci-control/contents/bridge/deliverbox')
if s == 200:
    for f in json.loads(b):
        if f['name'].endswith('.cipher') and f['name'] != 'TESTDECRYPT-01.cipher':
            finding('G-BOX', 'deliverbox 待取件：%s' % f['name'])

# G-N1 首报必跟进：线 outbox 尾件 vs 摆渡归档 reading/from-<line>.md 尾标
try:
    reg = json.loads(getc('vci-inbox', 'bridge/registry.json') or '{}')
    for line, v in (reg.get('lines') or {}).items():
        url = v.get('url')
        if not url or line == 'cisvr': continue
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'kernel'}), timeout=15) as r:
                ob = json.loads(r.read())
            its = ob.get('items') or []
            if not its: continue
            last = its[-1]; lts = age_h(str(last.get('ts', '')))
            arch = getc('HUB-MAIL', 'reading/from-%s.md' % line) or ''
            already = str(last.get('id', '')) in arch or ('#seq-%s' % str(last.get('seq', ''))) in arch
            if lts < 12 and not already:
                finding('G-N1', '%s outbox 尾件 %s 未入摆渡归档（跟进缺口）' % (line, last.get('id')))
        except Exception as e:
            finding('G-N1-probe', '%s outbox 探测失败 %s' % (line, str(e)[:60]))
except Exception as e:
    finding('G-N1-err', str(e)[:80])

# G-K0-lite 哨兵互守：guard/poller/relay/gate/clerk 最近 run 超 26h 沉默 → FINDING
s, b = gh('/repos/chepin-ai/vci-inbox/actions/runs?per_page=50')
if s == 200:
    seen = {}
    for r in json.loads(b)['workflow_runs']:
        p = r['path'].split('/')[-1]
        if p not in seen: seen[p] = r['created_at']
    for wf in ['bridge-guard.yml', 'bridge-poller.yml', 'disc-clerk.yml', 'disc-relay.yml', 'devsecops-gate.yml']:
        if wf not in seen or age_h(seen[wf]) > 26:
            finding('G-K0-lite', '哨兵沉默：%s' % wf)

# --- 输出 ---
verdict = 'GREEN' if not F else 'RED'
out = {'kernel': 'KERNEL-01 v0.1', 'ts': TS, 'verdict': verdict, 'findings': F,
       'state_digest': hashlib.sha256(json.dumps({'chain': chain_h, 'directives': len(items)}, sort_keys=True).encode()).hexdigest()[:16],
       'ledger_state': {stt: sum(1 for i in items if i.get('state') == stt) for stt in ('open', 'in-progress', 'done', 'verified')}}
print(json.dumps(out, ensure_ascii=False, indent=1))
open('kernel-report.json', 'w').write(json.dumps(out, ensure_ascii=False, indent=1))
open('findings-ledger.json', 'w').write(json.dumps(led, ensure_ascii=False, indent=1))
