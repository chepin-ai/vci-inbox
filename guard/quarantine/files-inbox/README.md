# files-inbox · 快门投递口（vci-inbox 公仓，事件驱动秒级摆渡）

## 门规（硬）
- **快门只收 L0/L1**：PATS 密钥闸命中或 `CLASSIFY: L2` 头标件一律拒收——隔离至 〈RED〉（私仓 quarantine/），大厅 #144 回执（dtag: files-ingest-fast）。
- **快门三关**（BORROW-ENVELOPE-01 族一 CDS guard）：①白名单关——路径/线名/扩展名（仅 .txt/.md/.json）；②schema 关——UTF-8 文本、.json 必可解析；③**解析后重建关**——落 HUB-LIB 的是按 canonical 形式重建的干净件（json 重排序序列化/文本控制字符剥离+换行归一），非原件，台账记重建件哈希——任何载荷夹带到此斩断。
- **零私域留存**：只路由不留存——路由后即删（git 历史残留属 L0/L1 可接受，如实声明此限；私域件不得走本口）。
- **私密件两条路**：HUB-MAIL 慢门（实测中位 ~10min）或 fed-relay 加密道（见下）。
- 路径规约：`files-inbox/{线名}/{相对路径}`，线名∈{ucif2,vinf,qgl,usrm,cfts,onto,gcml,cisvr}，单件 ≤256KB。

## fed-relay 加密道（增密级）
- pk 见 `HUB-CORE/bridge/fed-relay-pk.json`（SealedBox X25519）：加密 → base64 → 投 `files-inbox-enc/{线名}/{名}.enc`。
- 快门**原样转密文**入 HUB-LIB `lines/{线名}/_enc/`（零知识摆渡——密文不可解析，重建关豁免，此边界如实声明）；sweeper（HUB-CORE 持 sk）收割时解密 → 落正规目标 + 台账链 + 谱系行。
- **回执只许哈希值**（族一 M3 窄反向通道）：加密件回执=line+sha16+size，不带任何内容语义。

## 纠缠停 / entangle-gate v1（族二 sbd 自杀纪律）
- 首步统一过闸：**无 HALT 文件 ∧ term 单调 ∧ 锚未过期（48h）**，任一不满足即自退不执行。
- 锚=HUB-MAIL `bridge/head-anchor.json`（本侧头 sha 滚链+term）；验自洽（chain=sha256(prev‖head)）+连续（chain 或 prev_chain==本侧 last_chain）+term 严格增。
- HALT schema：`{by, reason, term, ts}`（weave/HALTED）；**RESUME 必须引用归因案编号**——`weave/RESUME-<案号>.md` 内含 `case:` 行方可清旗复工（没复盘不复工）。
- **wci 延伸**：暖侧读面已够（〈RED〉 只读锚面可照此验），写面待 root 投放——规约同上，激活凭 root 令。
