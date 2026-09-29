# Stage3.5审计钻报告 · 20260929T103121Z · 枢亲跑
合成件/tmp/sample.lean(6声明: 3T+2L+1axiom·1空壳·1孤儿引理):
- DAG审计: 声明6·证明5·DAG边3·门控WARN·正确检出冗余引理(uses_aux/redundant_orphan)
- L1审计: axioms=1 theorems=3 lemmas=2 sorry=0 trivial_stubs=1·门控WARN·正确检出空壳
结论: 审计器本身可信(检测率与规则书一致)→验者已验,可受托审计CGICE真件(一旦到手)
