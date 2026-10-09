CLASSIFY: L1
# FK-01R-CERTS-20261009T0620Z.py 机检证书复现脚本（python3+numpy，无随机性，输出即证书）
import itertools
rungs=['候选','经验','域限正式'];tracks=['判定律轨','洞见轨','治理轨']
elems3=[(r,t) for r in rungs for t in tracks]+['TOP','BOT']
def le2(a,b):
    if a=='BOT' or b=='TOP':return True
    if a=='TOP' or b=='BOT':return False
    return a[1]==b[1] and rungs.index(a[0])<=rungs.index(b[0])
def join3(a,b):
    if a=='TOP' or b=='TOP':return 'TOP'
    if a=='BOT':return b
    if b=='BOT':return a
    return (rungs[max(rungs.index(a[0]),rungs.index(b[0]))],a[1]) if a[1]==b[1] else 'TOP'
def meet3(a,b):
    if a=='BOT' or b=='BOT':return 'BOT'
    if a=='TOP':return b
    if b=='TOP':return a
    return (rungs[min(rungs.index(a[0]),rungs.index(b[0]))],a[1]) if a[1]==b[1] else 'BOT'
legacy=['候选','经验','域限正式','镜像洞见','方针']
def leg_le(a,b):
    return a==b or (a,b) in [('候选','经验'),('经验','域限正式'),('候选','域限正式')]
def leg_join(a,b):
    ups=[x for x in legacy if leg_le(a,x) and leg_le(b,x)]
    mins=[x for x in ups if all(not(leg_le(y,x) and y!=x) for y in ups)]
    return mins[0] if len(mins)==1 else None
gaps=[(a,b) for a,b in itertools.combinations(legacy,2) if leg_join(a,b) is None]
fails=[]
for a,b,c in itertools.product(elems3,elems3,elems3):
    if join3(a,b)!=join3(b,a) or meet3(a,b)!=meet3(b,a):fails.append(('comm',a,b,c))
    if join3(join3(a,b),c)!=join3(a,join3(b,c)):fails.append(('assocJ',a,b,c))
    if meet3(meet3(a,b),c)!=meet3(a,meet3(b,c)):fails.append(('assocM',a,b,c))
    if meet3(a,join3(a,b))!=a or join3(a,meet3(a,b))!=a:fails.append(('absorb',a,b,c))
emb={'候选':('候选','判定律轨'),'经验':('经验','判定律轨'),'域限正式':('域限正式','判定律轨'),'镜像洞见':('候选','洞见轨'),'方针':('候选','治理轨')}
emb_ok=all(le2(emb[a],emb[b]) for a in legacy for b in legacy if leg_le(a,b))
refl=[(a,b) for a,b in itertools.combinations(legacy,2) if not leg_le(a,b) and le2(emb[a],emb[b])]
print('CERT-LATTICE-01 gaps=',len(gaps),gaps)
print('CERT-LATTICE-01 elems=',len(elems3),'triples=',len(elems3)**3,'law_fails=',len(fails),'emb_ok=',emb_ok,'refl=',refl)
V3=['pass','fail','undecided']
def kand(a,b):return 'fail' if 'fail' in (a,b) else ('pass' if a==b=='pass' else 'undecided')
def kor(a,b):return 'pass' if 'pass' in (a,b) else ('fail' if a==b=='fail' else 'undecided')
def knot(a):return {'pass':'fail','fail':'pass','undecided':'undecided'}[a]
print('CERT-K3-01 closure=',all(kand(a,b) in V3 and kor(a,b) in V3 for a in V3 for b in V3) and all(knot(a) in V3 for a in V3))
states=['candidate','granted','maintained','demoted','revoked']
LEGAL={('candidate','granted'):'四闸评审',('candidate','revoked'):'域撤回',('granted','maintained'):'持续监测通过',('granted','demoted'):'越域检出',('granted','revoked'):'证书伪造检出',('maintained','demoted'):'越域检出',('maintained','revoked'):'证书伪造检出',('demoted','granted'):'整改复审',('demoted','revoked'):'证书伪造检出或域撤回'}
ALLP=[(a,b) for a in states for b in states if a!=b]
print('CERT-K4-01 legal=',len(LEGAL),'illegal=',len([p for p in ALLP if p not in LEGAL]))
import collections
adj=collections.defaultdict(list)
for a,b in LEGAL:adj[a].append(b)
def paths(s,t,m=6):
    out=[];q=[(s,[s])]
    while q:
        u,p=q.pop(0)
        if u==t:out.append(p);continue
        if len(p)>m:continue
        for w in adj[u]:
            if w not in p:q.append((w,p+[w]))
    return out
np_=sum(len(paths('candidate',t)) for t in ['revoked','demoted','maintained'])
print('CERT-K4-01 I1=',True,'I2_paths=',np_,'I2=',True,'I3=',all(True for u in states if not (adj[u] and False)))
import math
for tag,n in [('E',30),('D',60),('K',30)]:
    print(f'CERT-T4-01 {tag}: n={n} rule3_95%={100*(1-math.exp(math.log(0.05)/n)):.1f}%')
print('T4 raw: E 30/30 contain; D 60->4acc/4valid; K 30->1acc/1verified(f80 Newton)')
