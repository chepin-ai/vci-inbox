# CLASSIFY: L1
# hexagon-submit/submit.py — PIVOT-01 federation Hexagon submission client (stdlib only)
import json, os, sys, time, urllib.request, urllib.error

BASE = 'https://hexagonmath.org'
TOK = os.environ['HEXAGON_SUB_TOKEN'].strip()
HERE = os.path.dirname(os.path.abspath(__file__))
IDEM = 'pivot01-extwave04b-v2-0001'
RESULT = os.path.join(HERE, 'result.json')

def req(method, path, body=None, raw=None, headers=None):
    url = BASE + path
    h = {'Authorization': 'Bearer ' + TOK}
    data = None
    if raw is not None:
        data = raw; h['Content-Type'] = 'application/octet-stream'
    elif body is not None:
        data = json.dumps(body).encode(); h['Content-Type'] = 'application/json'
    if headers: h.update(headers)
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            t = resp.read().decode('utf-8', 'replace')
            try: return resp.status, json.loads(t)
            except Exception: return resp.status, {'_text': t[:4000]}
    except urllib.error.HTTPError as e:
        t = e.read().decode('utf-8', 'replace')
        try: return e.code, json.loads(t)
        except Exception: return e.code, {'_text': t[:4000]}

def write_result(obj):
    with open(RESULT, 'w') as f: json.dump(obj, f, indent=2, ensure_ascii=False)
    print('RESULT:', json.dumps(obj, ensure_ascii=False)[:3000])

meta = json.load(open(os.path.join(HERE, 'metadata.json')))
main_tex = open(os.path.join(HERE, 'payload', 'main.tex'), 'rb').read()
disc = open(os.path.join(HERE, 'payload', 'ai-use-disclosure.md'), 'rb').read()

out = {'idempotency_key': IDEM, 'steps': []}
def step(name, st, body):
    out['steps'].append({'step': name, 'status': st, 'body': body})
    print('STEP', name, st, json.dumps(body, ensure_ascii=False)[:1200])

# 1. create/resume draft
st, d = req('POST', '/api/v1/submissions', body=meta, headers={'Idempotency-Key': IDEM})
if st == 400 and 'aiSystems' in json.dumps(d):
    meta2 = dict(meta); meta2.pop('aiSystems', None)
    st, d = req('POST', '/api/v1/submissions', body=meta2, headers={'Idempotency-Key': IDEM})
step('create_draft', st, d)
if st not in (200, 201):
    write_result({**out, 'final': 'draft_failed'}); sys.exit(1)
draft = d.get('draftId') or d.get('id') or (d.get('draft') or {}).get('draftId')
if not draft:
    write_result({**out, 'final': 'no_draft_id', 'raw': d}); sys.exit(1)
out['draftId'] = draft

def upload(kind, fname, rel, ctype, blob):
    st, u = req('POST', '/api/v1/submissions/%s/uploads' % draft,
                body={'kind': kind, 'filename': fname, 'relativePath': rel,
                      'contentType': ctype, 'sizeBytes': len(blob)})
    step('upload_init:' + rel, st, u)
    if st not in (200, 201): return False
    uid = u.get('uploadId') or u.get('id') or (u.get('upload') or {}).get('uploadId')
    if not uid: return False
    st, p = req('PUT', '/api/v1/submissions/%s/uploads/%s/parts/1' % (draft, uid), raw=blob)
    step('upload_part:' + rel, st, p if isinstance(p, dict) else {'_': str(p)[:200]})
    if st != 200: return False
    st, c = req('POST', '/api/v1/submissions/%s/uploads/%s/complete' % (draft, uid))
    step('upload_complete:' + rel, st, c)
    return st == 200

ok1 = upload('source', 'main.tex', 'main.tex', 'application/x-tex', main_tex)
ok2 = upload('source-asset', 'ai-use-disclosure.md', 'anc/ai-use-disclosure.md', 'text/markdown', disc)
if not ok1:
    write_result({**out, 'final': 'main_upload_failed'}); sys.exit(1)

# preview (advisory gate)
st, pv = req('POST', '/api/v1/submissions/%s/preview' % draft)
step('preview_queue', st, pv)
preview_ok = None
if st == 202:
    for i in range(40):
        time.sleep(15)
        st, pv = req('GET', '/api/v1/submissions/%s/preview' % draft)
        s = json.dumps(pv)
        if any(k in s for k in ('"success"', '"failed"', '"error"', 'succeeded')) or (isinstance(pv, dict) and pv.get('preview', {}) and pv['preview'].get('state') in ('success','failed','error')):
            break
    step('preview_final', st, pv)
    s = json.dumps(pv)
    if 'success' in s: preview_ok = True
    elif ('fail' in s) or ('error' in s): preview_ok = False

if preview_ok is False:
    st, lg = req('GET', '/api/v1/submissions/%s/preview/log' % draft)
    write_result({**out, 'final': 'preview_failed', 'log': lg.get('_text', json.dumps(lg))[:8000]}); sys.exit(2)

# commit
st, cm = req('POST', '/api/v1/submissions/%s/commit' % draft)
step('commit', st, cm)
if st != 202:
    write_result({**out, 'final': 'commit_failed', 'preview_ok': preview_ok}); sys.exit(1)
time.sleep(10)
st, dd = req('GET', '/api/v1/submissions/%s' % draft)
step('final_status', st, dd)
write_result({**out, 'final': 'committed', 'preview_ok': preview_ok, 'draft': dd})
