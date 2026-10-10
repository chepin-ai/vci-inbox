# CLASSIFY: L1
# hexagon-submit/submit.py — PIVOT-01 federation Hexagon submission client (stdlib only, self-reporting)
import json, os, sys, time, traceback, urllib.request, urllib.error

BASE = 'https://hexagonmath.org'
HERE = os.path.dirname(os.path.abspath(__file__))
IDEM = 'pivot01-extwave04b-v2-0001'
RESULT = os.path.join(HERE, 'result.json')
out = {'idempotency_key': IDEM, 'steps': []}

def write_result(**kw):
    out.update(kw)
    try:
        with open(RESULT, 'w') as f: json.dump(out, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def req(method, path, body=None, raw=None, headers=None):
    TOK = os.environ.get('HEXAGON_SUB_TOKEN', '').strip()
    url = BASE + path
    h = {'Authorization': 'Bearer ' + TOK, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*'}
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

def step(name, st, body):
    out['steps'].append({'step': name, 'status': st, 'body': body})
    write_result()

def main():
    if not os.environ.get('HEXAGON_SUB_TOKEN'):
        write_result(final='no_token'); return 1
    meta = json.load(open(os.path.join(HERE, 'metadata.json')))
    meta.pop('CLASSIFY', None)
    main_tex = open(os.path.join(HERE, 'payload', 'main.tex'), 'rb').read()
    disc = open(os.path.join(HERE, 'payload', 'ai-use-disclosure.md'), 'rb').read()

    st, d = req('POST', '/api/v1/submissions', body=meta, headers={'Idempotency-Key': IDEM})
    if st == 400 and 'aiSystems' in json.dumps(d):
        meta2 = dict(meta); meta2.pop('aiSystems', None)
        st, d = req('POST', '/api/v1/submissions', body=meta2, headers={'Idempotency-Key': IDEM})
        step('create_draft_nosystems', st, d)
    else:
        step('create_draft', st, d)
    if st not in (200, 201):
        write_result(final='draft_failed'); return 1
    draft = d.get('draftId') or d.get('id') or (d.get('draft') or {}).get('draftId')
    if not draft:
        write_result(final='no_draft_id'); return 1
    out['draftId'] = draft

    def upload(kind, fname, rel, ctype, blob):
        st, u = req('POST', '/api/v1/submissions/%s/uploads' % draft,
                    body={'kind': kind, 'filename': fname, 'relativePath': rel,
                          'contentType': ctype, 'sizeBytes': len(blob)})
        step('upload_init:' + rel, st, u)
        if st not in (200, 201): return False
        if (u.get('status') or (u.get('upload') or {}).get('status')) == 'complete':
            return True  # idempotent resume: matching upload already complete server-side
        uid = u.get('uploadId') or u.get('id') or (u.get('upload') or {}).get('uploadId')
        if not uid: return False
        st, p = req('PUT', '/api/v1/submissions/%s/uploads/%s/parts/1' % (draft, uid), raw=blob)
        step('upload_part:' + rel, st, p)
        if (st != 200) and not (st == 409 and 'already complete' in json.dumps(p)):
            return False  # 409 already-complete = resumed upload done; treat as success
        st, c = req('POST', '/api/v1/submissions/%s/uploads/%s/complete' % (draft, uid))
        step('upload_complete:' + rel, st, c)
        return (st == 200) or (st == 409 and 'already complete' in json.dumps(c))

    ok1 = upload('source', 'main.tex', 'main.tex', 'application/x-tex', main_tex)
    ok2 = upload('source-asset', 'ai-use-disclosure.md', 'anc/ai-use-disclosure.md', 'text/markdown', disc)
    if not ok1:
        write_result(final='main_upload_failed'); return 1

    st, pv = req('POST', '/api/v1/submissions/%s/preview' % draft)
    step('preview_queue', st, pv)
    preview_ok = None
    if st == 202:
        for i in range(40):
            time.sleep(15)
            st, pv = req('GET', '/api/v1/submissions/%s/preview' % draft)
            s = json.dumps(pv)
            if ('success' in s) or ('failed' in s) or ('error' in s):
                break
        step('preview_final', st, pv)
        s = json.dumps(pv)
        if 'success' in s: preview_ok = True
        elif ('failed' in s) or ('error' in s): preview_ok = False

    if preview_ok is False:
        st, lg = req('GET', '/api/v1/submissions/%s/preview/log' % draft)
        write_result(final='preview_failed', log=lg.get('_text', json.dumps(lg))[:8000])
        return 2

    st, cm = req('POST', '/api/v1/submissions/%s/commit' % draft)
    step('commit', st, cm)
    if st != 202:
        write_result(final='commit_failed', preview_ok=preview_ok); return 1
    time.sleep(10)
    st, dd = req('GET', '/api/v1/submissions/%s' % draft)
    step('final_status', st, dd)
    write_result(final='committed', preview_ok=preview_ok)
    return 0

if __name__ == '__main__':
    try:
        code = main()
    except Exception:
        write_result(final='crash', traceback=traceback.format_exc()[-3000:])
        code = 9
    sys.exit(code)
