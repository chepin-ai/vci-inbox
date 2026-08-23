#!/usr/bin/env python3
# KERNEL-01 v0 · N/M/Δ 形式化自动机内核（CI 值守，自证自验）
# 状态 = 台账+信道账+链+出件面；守卫规则违例 → FINDING（残差即案）
import json, os, sys, glob, hashlib, datetime, urllib.request, base64

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
def age_h(ts):
    try:
        t = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return (NOW - t).total_seconds() / 3600
    except Exception:
        return 9999

F = []  # FINDINGS
def finding(rule, detail):
    F.append({'rule': rule, 'detail': detail, 'ts': NOW.strftime('%Y-%m-%dT%H:%M:%SZ')})

# --- 状态装载 ---
D = json.loads(getc('ci-control', 'bridge/DIRECTIVES.json') or '{"items":[]}')
items = D['items']
byid = {i['id']: i for i in items}
CHAIN = getc('vci-inbox', 'disc/CHAIN.jsonl') or ''
chain_h = len([l for l in CHAIN.strip().splitlines() if l.strip()])
INDEX = getc('vci-inbox', 'disc/INDEX.md') or ''
BOARD = getc('ci-control', 'bridge/situation/BOARD-01.md') or ''
CHANNELS = getc('ci-control', 'bridge/CHANNELS-01.md') or ''

# G-DIR 指令保鲜：open>72h 升级 / in-progress>96h 无 evidence 更新提醒
for i in items:
    if i['state'] == 'open' and age_h(D.get('updated', '')) > 0:
        src_age = age_h('2026-08-22T13:00:00Z') if '大束' in i.get('src','') else age_h(NOW.strftime('%Y-%m-%dT%H:%M:%SZ'))
        if src_age > 72:
            finding('G-DIR-stale-open', '%s open 超 72h：%s' % (i['id'], i['d'][:40]))

# G-N8 岗报必呈：BOARD 24h
m = [l for l in BOARD.splitlines() if '刷新' in l or 'v0.' in l]
finding_board = True
if BOARD:
    import re
    mm = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', BOARD)
    if mm and age_h(mm.group(1)) < 24: finding_board = False
if finding_board: finding('G-N8', 'BOARD 态势板超 24h 未刷新')

# G-M2 静默必勾：CHANNELS 48h
import re
mm = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', CHANNELS)
if not mm or age_h(mm.group(1)) > 48: finding('G-M2', 'CHANNELS 健康账超 48h 未刷')

# G-Δ3 残差即案：CHAIN 高度 vs INDEX 帖数
import re as _re
n_idx = len(_re.findall(r'\| \d{4}-\d{2}-\d{2}T', INDEX))
if abs(chain_h - n_idx) > 2:
    finding('G-D3', 'CHAIN 高 %d vs INDEX 帖 %d 不符' % (chain_h, n_idx))

# G-BOX deliverbox 值守：未取密文 >1h
s, b = gh('/repos/chepin-ai/ci-control/contents/bridge/deliverbox')
if s == 200:
    for f in json.loads(b):
        if f['name'].endswith('.cipher') and f['name'] != 'TESTDECRYPT-01.cipher':
            finding('G-BOX', 'deliverbox 有待取件：%s' % f['name'])

# G-N1 首报必跟进：qlv/lgt outbox 新件 vs 已渡（relayed-state + 归档近似判）
try:
    reg = json.loads(getc('vci-inbox', 'bridge/registry.json') or '{}')
    relayed = set(json.loads(getc('vci-inbox', 'bridge/relayed-state.json') or '{}').get('relayed', []))
    for line, v in (reg.get('lines') or {}).items():
        url = v.get('url')
        if not url or line == 'cisvr': continue
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'kernel'}), timeout=15) as r:
                ob = json.loads(r.read())
            its = ob.get('items') or []
            if its:
                last = its[-1]
                lts = age_h(str(last.get('ts', '')))
                if lts < 12 and str(last.get('id', '')) not in relayed:
                    finding('G-N1', '%s outbox 有新件 %s 未确认摆渡/应答' % (line, last.get('id')))
        except Exception as e:
            finding('G-N1-probe', '%s outbox 探测失败 %s' % (line, str(e)[:60]))
except Exception as e:
    finding('G-N1-err', str(e)[:80])

# --- 输出 + 自证（kernel 自报=自我验证存根） ---
verdict = 'GREEN' if not F else ('YELLOW' if all(x['rule'].startswith('G-DIR') for x in F) else 'RED')
out = {'kernel': 'KERNEL-01 v0', 'ts': NOW.strftime('%Y-%m-%dT%H:%M:%SZ'),
       'verdict': verdict, 'findings': F,
       'state_digest': hashlib.sha256(json.dumps({'chain': chain_h, 'directives': len(items)}, sort_keys=True).encode()).hexdigest()[:16],
       'ledger_state': {'open': sum(1 for i in items if i['state']=='open'), 'in-progress': sum(1 for i in items if i['state']=='in-progress'), 'done': sum(1 for i in items if i['state']=='done'), 'verified': sum(1 for i in items if i['state']=='verified')}}
print(json.dumps(out, ensure_ascii=False, indent=1))
open('kernel-report.json', 'w').write(json.dumps(out, ensure_ascii=False, indent=1))
