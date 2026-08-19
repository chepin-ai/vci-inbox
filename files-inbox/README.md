# files-inbox · 快门投递口（vci-inbox 公仓，事件驱动秒级摆渡）

## 门规（硬）
- **快门只收 L0/L1**：PATS 密钥闸命中或 `CLASSIFY: L2` 头标件一律拒收——隔离至 ci-logs（私仓 quarantine/），并在大厅 #144 回执（dtag: files-ingest-fast）。
- **私密件走 ci-inbox 慢门**（私仓 files-inbox/，sweeper 轮询，实测 60-90min/班饥荒口径）。
- 路径规约：`files-inbox/{线名}/{相对路径}`，线名∈{ucif2,vinf,qgl,usrm,cfts,onto,gcml,cisvr}，单件 ≤256KB，UTF-8 文本。
- 路由：一律入 ci-library `lines/{线名}/`（App 写私仓，内容回私域）+ `_ledger.jsonl` 台账链 + `_index.jsonl` 谱系行。
