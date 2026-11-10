"""AD-22 发布前RAC候件差集核查；私有件只记录状态，不回显正文。"""
import base64,json,re,sys,time
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0,'/mnt/agents/output/.stash/ad21/run')
from ad21_publish import request,VAULT
R=Path('/mnt/agents/output/.stash/ad22/run')
BASES={'chepin-ai/ci-inbox':'43ea0157796eab310c131a020fcea0ba8cc87bf1','chepin-ai/vci-inbox':'685af987c492b2092c85c3ee9f2e69007977bf55','chepin-qi/qlv-pub':'781f101908b534c6d23d56c66bc8a3cda9ff5be2'}

def main():
 out={'beat':'AD-22','checked_at':time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()),'repos':{},'fingerprint_arrived':False,'quantum_machine_consumption':0}
 for repo,base in BASES.items():
  token=(VAULT/('qi_pat.txt' if repo.startswith('chepin-qi/') else 'fed_pat.txt')).read_text().strip()
  head=request('GET',f'/repos/{repo}/git/ref/heads/main',token)['object']['sha']
  cmp=request('GET',f'/repos/{repo}/compare/{base}...{head}',token)
  candidates=[]
  for f in cmp.get('files',[]):
   name=f['filename']
   if not re.search(r'RAC|LGT|QUAFU',name,re.I):continue
   item={'path':name,'status':f['status'],'has_numeric_S_sim':False,'queue_only':False}
   if f['status']!='removed':
    quoted_name=quote(name,safe='/')
    doc=request('GET',f'/repos/{repo}/contents/{quoted_name}?ref={head}',token)
    if doc.get('encoding')=='base64':
     text=base64.b64decode(doc['content']).decode(errors='replace')
     item['has_numeric_S_sim']=bool(re.search(r'S_sim\s*[:=]\s*(?:[0-9]+(?:\.[0-9]*)?|0x[0-9a-fA-F]+)',text))
     item['queue_only']=('In Queue' in text and 'returned_shots=0' in text)
   item['has_numeric_S_sim']=bool(item['has_numeric_S_sim']);out['fingerprint_arrived']|=item['has_numeric_S_sim'];candidates.append(item)
  out['repos'][repo]={'base':base,'head':head,'ahead_by':cmp.get('ahead_by'),'behind_by':cmp.get('behind_by'),'candidates':candidates}
 out['verdict']='WAITING_PEER_S_SIM' if not out['fingerprint_arrived'] else 'FINGERPRINT_CANDIDATE_REQUIRES_INDEPENDENT_REPLAY'
 (R/'ad22_rac_check.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'checked_at':out['checked_at'],'fingerprint_arrived':out['fingerprint_arrived'],'verdict':out['verdict'],
                   'heads':{k:v['head'] for k,v in out['repos'].items()},
                   'candidate_counts':{k:len(v['candidates']) for k,v in out['repos'].items()}},indent=2))
if __name__=='__main__':main()
