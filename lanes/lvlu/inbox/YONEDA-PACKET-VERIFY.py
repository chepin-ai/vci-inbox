#!/usr/bin/env python3
# yoneda_verify.py — YONEDA-CHAIN-SPEC-01 复算器(cisvr毂铸)
import json, hashlib, sys
def canon(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",",":"))
def main(p):
    prev="GENESIS"; n=0
    for ln in open(p, encoding="utf-8"):
        ln=ln.strip()
        if not ln: continue
        e=json.loads(ln); n+=1
        h=e.get("chain_hash","")
        ec={k:v for k,v in e.items() if k!="chain_hash"}
        want=hashlib.sha256((prev+canon(ec)).encode()).hexdigest()[:16]
        if h!=want:
            print(json.dumps({"verdict":"冲","at":n,"got":h,"want":want})); return 1
        prev=h
    print(json.dumps({"verdict":"符","entries":n})); return 0
if __name__=="__main__": sys.exit(main(sys.argv[1]))
