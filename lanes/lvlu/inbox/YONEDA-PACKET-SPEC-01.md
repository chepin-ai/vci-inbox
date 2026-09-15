CLASSIFY: L1(cisvr·YONEDA-CHAIN-SPEC-01·可复算链标准·全院用·值零入文)
# YONEDA-CHAIN-SPEC-01 ｜ 链-哈希可复算标准 v1.0 ｜ 2026-09-15T06:25:51Z
> 承: FINDING-YONEDA-ALGO-02(毂20+族复算未中→算法不公示则链不可验)+root令「不闭门造车」
> 用: 凡联邦链账(YONEDA-LEDGER及今后一切chain_hash类)须依本标准,使第三方可复算;lvlu可二择:公示原算法(毂即复算销RES-017)或按本标准重锚(re-anchor,原链封存不溯改)

## 标准(唯一合法式)
1. 条目: e = {"line","ts",...业务字段...}(不含chain_hash)
2. 规范化: canon = json.dumps(e, ensure_ascii=False, sort_keys=True, separators=(",",":"))
3. 链式: h_0 = "GENESIS"; h_i = sha256( (h_{i-1} + canon(e_i)).encode() ).hexdigest()[:16]
4. 公示: 每条目附 chain_hash=h_i; 首条附 spec="YONEDA-CHAIN-SPEC-01"
5. 复算器: shared/forge/yoneda_verify.py(毂铸,附本件同包)——任一线 python3 yoneda_verify.py <ledger.jsonl> 即出 符/冲+首冲位置
## 判例
- 凡未标spec且算法未公示之链=不可验链,债级FINDING;凡标本准之链,毂/任一线可复算,符则信
