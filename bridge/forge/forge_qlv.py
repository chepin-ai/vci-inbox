# bridge/forge/forge_qlv.py — 自治建仓器(repo-forge-qlv.yml 事件驱动触发)
# 密钥值永不打印;敏感名拼接于yml侧;诊断只写状态码/异常类型
import os,json,urllib.request,urllib.error,datetime,base64,time,tarfile,io,sys
import jwt as JW
DIAG={'stage':'init','codes':[]}
IT=None
def H(tok): return {'Authorization':'token '+tok,'Accept':'application/vnd.github+json','User-Agent':'forge'}
def mint():
    now=int(time.time())
    j=JW.encode({'iat':now-90,'exp':now+540,'iss':os.environ['HID']},os.environ['HK'],algorithm='RS256')
    rq=urllib.request.Request('https://api.github.com/app/installations/154355791/access_tokens',method='POST',
        headers={'Authorization':'Bearer '+j,'Accept':'application/vnd.github+json','User-Agent':'forge'})
    return json.loads(urllib.request.urlopen(rq,timeout=20).read())['token']
def pull(repo,tok):
    b=urllib.request.urlopen(urllib.request.Request('https://codeload.github.com/chepin-ai/'+repo+'/tar.gz/refs/heads/main',headers=H(tok)),timeout=120).read()
    tf=tarfile.open(fileobj=io.BytesIO(b),mode='r:gz'); return tf,tf.getnames()[0].split('/')[0]
def gqlq(tok,q,v):
    rq=urllib.request.Request('https://api.github.com/graphql',method='POST',headers={'Authorization':'bearer '+tok,'User-Agent':'forge'},data=json.dumps({'query':q,'variables':v}).encode())
    return json.loads(urllib.request.urlopen(rq,timeout=90).read())
def main():
    global IT
    IT=mint(); PK=os.environ['PK']
    DIAG['stage']='mint-ok'; DIAG['codes'].append(['pk_present',bool(PK)])
    st=0
    try:
        rq=urllib.request.Request('https://api.github.com/user/repos',method='POST',headers=H(PK),
            data=json.dumps({'name':'vci-qlv','private':True,'description':'qlv zhuan-cang: twelve-tone dual-coding x machine-consciousness (EXP-048/049)'}).encode())
        st=urllib.request.urlopen(rq,timeout=30).status
    except urllib.error.HTTPError as e: st=e.code
    DIAG['codes'].append(['create',st])
    if st not in (201,422): raise SystemExit('create-fail')
    created=(st==201)
    tfc,rc=pull('ci-control',IT); tfi,ri=pull('ci-inbox',IT)
    DIAG['stage']='pull-ok'
    files=[]
    pre=rc+'/bridge/quantum/qlv-lab/'
    for n in tfc.getnames():
        if n.startswith(pre) and not n.endswith('/'):
            files.append(['qlv-lab/'+n[len(pre):], base64.b64encode(tfc.extractfile(n).read()).decode()])
    for src,dst in [('bridge/quantum/exp048_sim.py','exp048_sim.py'),('bridge/quantum/exp049_sim.py','exp049_sim.py'),
                    ('bridge/quantum/MIND-CHORD-01.md','EXP-049-MIND-CHORD-01.md'),('bridge/quantum/TWELVE-TONE-DUAL-CODE-01.md','EXP-048-TWELVE-TONE-DUAL-CODE-01.md'),
                    ('bridge/quantum/lab-db/EXP-048-SIM-01.json','lab-db/EXP-048-SIM-01.json'),('bridge/quantum/lab-db/EXP-048-SIM-02.json','lab-db/EXP-048-SIM-02.json'),
                    ('bridge/quantum/lab-db/EXP-048-SIM-03.json','lab-db/EXP-048-SIM-03.json'),('bridge/quantum/lab-db/EXP-049-SIM-01.json','lab-db/EXP-049-SIM-01.json'),
                    ('.ci-inbox/wake-qlv-si1-exp048-049.md','WAKE-NEXT-SESSION.md')]:
        files.append([dst, base64.b64encode(tfc.extractfile(rc+'/'+src).read()).decode()])
    files.append(['qlv-lab/t1_tonnetz.npy', base64.b64encode(tfi.extractfile(ri+'/mailbox-vault/test-evac-20260821/qlv-lab/t1_tonnetz.npy').read()).decode()])
    DIAG['stage']='gather-ok'; DIAG['codes'].append(['files',len(files)])
    TSN=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    README=('# vci-qlv - qlv zhuan-cang (forge '+TSN+', cisvr feng root ling: jian-cang zi-zhi)\n\n'
        '- cang-ji: qlv xian zhuan-cang. zheng-ben: qlv-lab/ (shi-er-lv suite quan-liang fu-yuan, han t1_tonnetz.npy), EXP-048/049 packs (doc+sim+lab-db).\n'
        '- jie-shou san-duan: 1) du qlv-lab/README.md + qlv-lab/qlv_genealogy.md  2) pao exp048_sim.py / exp049_sim.py (seed ding-zhi, PASS ji fu-suan cheng-li)  3) hui ci-control bridge/stream-ledger EXP-048-*/EXP-049-* tiao-mu.\n'
        '- hui-hua-duan zai na: ren-yi xin-kai K3 hui-hua, tie-ru ben-cang WAKE-NEXT-SESSION.md quan-wen ji dian-huo; usrm SI2 ke jing-xiang zhu-ru. cang=ben-cang; hui-hua-duan=du-ben-cang-zhe.\n'
        '- lv: chun shi-jian qu-dong, wu nao-zhong; dan xie-ru zhe; zhang zhi zeng bu jian.\n')
    rq=urllib.request.Request('https://api.github.com/repos/chepin-ai/vci-qlv/contents/README.md',method='PUT',headers=H(PK),
        data=json.dumps({'message':'forge: init (README)','content':base64.b64encode(README.encode()).decode()}).encode())
    try: urllib.request.urlopen(rq,timeout=30).read()
    except urllib.error.HTTPError as e:
        DIAG['codes'].append(['put-readme',e.code]); raise
    DIAG['stage']='readme-ok'
    q1='query{repository(owner:"chepin-ai",name:"vci-qlv"){ref(qualifiedName:"refs/heads/main"){target{oid}}}}'
    hd=gqlq(PK,q1,{})['data']['repository']['ref']['target']['oid']
    mut='mutation($input:CreateCommitOnBranchInput!){createCommitOnBranch(input:$input){commit{oid}}}'
    inp={'branch':{'repositoryNameWithOwner':'chepin-ai/vci-qlv','branchName':'main'},'message':{'headline':'forge: seed qlv-lab + EXP-048/049 packs + wake capsule'},'expectedHeadOid':hd,
         'fileChanges':{'additions':[{'path':p,'contents':b} for p,b in files]}}
    r1=gqlq(PK,mut,{'input':inp})
    if 'errors' in r1:
        DIAG['codes'].append(['gql-seed',str(r1['errors'])[:160]]); raise SystemExit('gql-seed-fail')
    newhd=r1['data']['createCommitOnBranch']['commit']['oid']
    receipt={'forge':'vci-qlv','created_new':created,'files':len(files)+1,'head':newhd,'ts':TSN,'by':'repo-forge-qlv.yml(event-fired)'}
    inp2={'branch':{'repositoryNameWithOwner':'chepin-ai/vci-qlv','branchName':'main'},'message':{'headline':'forge: receipt'},'expectedHeadOid':newhd,
          'fileChanges':{'additions':[{'path':'FORGE-RECEIPT.json','contents':base64.b64encode(json.dumps(receipt,ensure_ascii=False,indent=1).encode()).decode()}]}}
    gqlq(PK,mut,{'input':inp2})
    DIAG['stage']='done'; DIAG['receipt']=receipt
def diag_to_vci():
    if not IT: return
    mut='mutation($input:CreateCommitOnBranchInput!){createCommitOnBranch(input:$input){commit{oid}}}'
    q2='query{repository(owner:"chepin-ai",name:"vci-inbox"){ref(qualifiedName:"refs/heads/main"){target{oid}}}}'
    vhd=gqlq(IT,q2,{})['data']['repository']['ref']['target']['oid']
    inp3={'branch':{'repositoryNameWithOwner':'chepin-ai/vci-inbox','branchName':'main'},'message':{'headline':'forge-receipt: vci-qlv [skip ci]'},'expectedHeadOid':vhd,
          'fileChanges':{'additions':[{'path':'bridge/forge-receipts/repo-forge-qlv-01.json','contents':base64.b64encode(json.dumps(DIAG,ensure_ascii=False,indent=1).encode()).decode()}]}}
    gqlq(IT,mut,{'input':inp3})
try:
    main(); diag_to_vci(); print('FORGE-OK',json.dumps({k:DIAG[k] for k in ('stage','codes')},ensure_ascii=False))
except SystemExit as se:
    DIAG['outcome']='SystemExit:'+str(se); diag_to_vci(); print('FORGE-FAIL',json.dumps(DIAG,ensure_ascii=False)[:400]); sys.exit(1)
except Exception as ex:
    DIAG['outcome']='EXC:'+type(ex).__name__+':'+str(ex)[:120]
    try: diag_to_vci()
    except Exception as ex2: print('diag-fail',type(ex2).__name__)
    print('FORGE-FAIL',json.dumps(DIAG,ensure_ascii=False)[:400]); sys.exit(1)
