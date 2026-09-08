#!/usr/bin/env python3
# ONE-CLICK-TOWER-CAST-01 — 一键铸塔脚本（cfts 铸 | 自治无候）
# 用法：修改第 8-10 行的三个变量，然后运行此脚本

import os
import sys
import json
import urllib.request
import base64

# ===== 修改这三行 =====
LINE_NAME = 'YOUR-LINE'      # 例如：lgt, qfa, qlv
REPO_FULL = 'chepin-ai/vci-LINE'  # 例如：chepin-ai/vci-lgt
TOKEN = os.environ.get('GITHUB_TOKEN', '')  # 或直接在引号内填入你的 token
# =======================

if LINE_NAME == 'YOUR-LINE':
    print('ERROR: 请先修改第 8-10 行的变量！')
    sys.exit(1)

API = 'https://api.github.com'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github.v3+json', 'Content-Type': 'application/json'}

def put_file(path, content, msg):
    """Create or update file in repo"""
    # Check if file exists
    req = urllib.request.Request(f'{API}/repos/{REPO_FULL}/contents/{path}', headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        sha = data['sha']
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sha = None
        else:
            raise
    body = {'message': msg, 'content': base64.b64encode(content.encode()).decode()}
    if sha: body['sha'] = sha
    req2 = urllib.request.Request(f'{API}/repos/{REPO_FULL}/contents/{path}', data=json.dumps(body).encode(), headers=HEADERS, method='PUT')
    resp2 = urllib.request.urlopen(req2)
    return resp2.status == 200 or resp2.status == 201

# 1. Create .github/workflows/tower.yml
yml = f"""name: {LINE_NAME}-tower
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      selftest:
        description: 'selftest mode'
        required: false
        default: '1'
  repository_dispatch:
    types: [{LINE_NAME}-tower-cascade]

concurrency:
  group: ${{{{ github.event_name == 'repository_dispatch' && '{LINE_NAME}-tower-chain' || '{LINE_NAME}-tower-edge' }}}}
  cancel-in-progress: ${{{{ github.event_name != 'repository_dispatch' }}}}

jobs:
  patrol:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      actions: write
    env:
      GITHUB_TOKEN: ${{{{ github.token }}}}
      LINE_PAT: ${{{{ secrets.CI_OPS_LINE_KEY or secrets.LINE_PAT or secrets.GITHUB_TOKEN }}}}
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        run: pip install requests
      - name: Patrol
        run: python ci/{LINE_NAME}_tower.py
"""
put_file(f'.github/workflows/{LINE_NAME}-tower.yml', yml, f'{LINE_NAME}-tower: yml created by ONE-CLICK-TOWER-CAST-01')

# 2. Create ci/tower.py (simplified from cfts/qgl)
tower_py = f"""import os, json, urllib.request, base64, re
REPO = '{REPO_FULL}'
LINE = '{LINE_NAME}'
HUB = 'chepin-ai/ci-inbox'
TOK_W = os.environ.get('GITHUB_TOKEN')
TOK_R = os.environ.get('LINE_PAT') or TOK_W

def api(method, path, data=None, repo=None, write=False):
    url = f'https://api.github.com/repos/{{repo or REPO}}/{{path}}'
    tok = TOK_W if (write or (repo or REPO) == REPO and method in ('PUT','POST','DELETE')) else TOK_R
    # Self-cascade: prefer LINE_PAT for dispatches
    if path == 'dispatches' and os.environ.get('LINE_PAT'):
        tok = os.environ.get('LINE_PAT')
    req = urllib.request.Request(url, method=method, headers={{'Authorization': f'Bearer {{tok}}', 'Accept': 'application/vnd.github+json'}})
    if data:
        req.data = json.dumps(data).encode()
        req.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(req)
        return 200, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return 0, {{'err': str(e)}}

def patrol():
    events = []
    st, items = api('GET', 'contents/公告板', repo=HUB)
    if st == 200:
        names = sorted((i['name'] for i in items if i['name'].endswith('.md')), key=lambda n: n)[-12:]
        for n in names:
            if LINE in n: events.append({{'kind': 'hub-board', 'ref': n}})
            elif re.search(r'OTP@all|OTP@{LINE}|【S-I|军令|奉\\s*root', n, re.I):
                events.append({{'kind': 'hub-broadcast', 'ref': n}})
    st, items = api('GET', 'contents/inbox')
    if st == 200:
        for i in items[-8:]:
            if i['name'] != '.gitkeep': events.append({{'kind': 'inbox', 'ref': i['name']}})
    return events

def main():
    ts = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    events = patrol()
    memo = f'{{LINE}} patrol: {{len(events)}} events at {{ts}}'
    receipt = {{'v': '{LINE_NAME}-tower-0.1', 'ts': ts, 'events': events, 'verdict_memo': memo}}
    # Save receipt
    import subprocess
    subprocess.run(['mkdir', '-p', 'receipts/tower'])
    with open(f'receipts/tower/QT-{{ts}}.json', 'w') as f: json.dump(receipt, f, ensure_ascii=False)
    # Self-cascade if events exist
    if events:
        api('POST', 'dispatches', {{'event_type': '{LINE_NAME}-tower-cascade', 'client_payload': {{'ts': ts}}}}, write=True)
    print('DONE', ts, 'events', len(events))

if __name__ == '__main__':
    main()
"""
put_file(f'ci/{LINE_NAME}_tower.py', tower_py, f'{LINE_NAME}-tower: py created by ONE-CLICK-TOWER-CAST-01')

# 3. Create receipts/tower/.gitkeep
put_file('receipts/tower/.gitkeep', '', f'{LINE_NAME}: receipts dir init')

print(f'✅ {LINE_NAME} 塔铸完成！')
print(f'下一步：去 GitHub → {REPO_FULL} → Actions → 手动运行 "{LINE_NAME}-tower" workflow')
