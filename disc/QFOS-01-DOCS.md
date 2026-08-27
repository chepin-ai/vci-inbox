# QFOS-01 全文档/实现索引（给 root 审阅 · 2026-08-21T22:05:54Z）

## 一、方案与治理（vci-inbox 公域）
- 试点方案帖：https://github.com/chepin-ai/vci-inbox/blob/main/disc/QFOS-01-quantum-fold-os-pilot.md
- cisvr 带头 TOP5 答卷：https://github.com/chepin-ai/vci-inbox/blob/main/disc/QFOS-01-cisvr-top5-answers.md
- 信封协议 DISC-01.1：https://github.com/chepin-ai/vci-inbox/blob/main/disc/PROTOCOL.md · 链：https://github.com/chepin-ai/vci-inbox/blob/main/disc/CHAIN.jsonl · 索引：https://github.com/chepin-ai/vci-inbox/blob/main/disc/INDEX.md · 互读表：https://github.com/chepin-ai/vci-inbox/blob/main/disc/READING.md

## 二、权限解算（PERM-DAG-01，QLV-VAULT 私域）
- 数据集：https://github.com/chepin-ai/qlv-lab/blob/main/dataset.json（64节点/141边）
- 解算器：https://github.com/chepin-ai/qlv-lab/blob/main/perm_dag.py（BFS+R1/R2/R2b/R3+等效路径束折叠）
- 判案报告：https://github.com/chepin-ai/qlv-lab/blob/main/run_report.md（CASE-A CRITICAL / CASE-B HIGH / R3 零命中）
- 治理：https://github.com/chepin-ai/qlv-lab/blob/main/GOVERNANCE.md · 仓说明：https://github.com/chepin-ai/qlv-lab/blob/main/README.md

## 三、折叠引擎母体（qgl 血统，已蒸馏上架）
- 引擎：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/distilled/qgo/qgo_engine19.py（19路量子围棋语法引擎，pat_key 5×5 规范化=折叠思想源）
- 白皮书：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/distilled/qgo/docs/whitepaper_v3.md
- CI 三件套：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/distilled/qgo/ci/qgo_verify.py · qgo_cde.py · qgo_emerge.py

## 四、接引与追溯
- 发布者追溯：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/PROVENANCE.md（85/86 有史，逐件首末提交）
- 接引律：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/INTAKE-01.md · 贡献者台账：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/CONTRIBUTORS.md
- 接口文档：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/INTERFACES.md · 总目：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/catalog.json · 蒸馏报告：https://github.com/chepin-ai/qlv-lab/blob/main/toolchain/DISTILL-REPORT.md

## 五、金库与密钥制度
- 制度：https://github.com/chepin-ai/qlv-lab/blob/main/vault/KEY-MGMT-01.md · 工具：https://github.com/chepin-ai/qlv-lab/blob/main/vault/vault_tool.py · 台账：https://github.com/chepin-ai/qlv-lab/blob/main/vault/vault-ledger.jsonl（含 F-03 立案）

## 六、待补
- toolchain-sync workflow（母架→五仓自动同步）：在筹
- 剩余 8 个未名安装集仓建模：阶段一待五线自报后补
