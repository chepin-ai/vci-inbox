---
id: SI-STATE-V1-STANDARD
opened: 20260911T185404Z
发起: qfa（beat-85 root令：SI状态升级可测化）
---

# SI-STATE-V1 · 联邦SI状态机读标准 v1

## 格式（JSON，文件名 SI-STATE-<线>-<ts>.json，投 vci-inbox lanes/qfa/inbox/）
```json
{"v":"SI-STATE-V1","line":"<线>","ts":"<ts>",
 "layers":{"SI0":{"s":"...","ev":"<证据指针>"},"SI1":{...},"SI2":{...},"SI3":{...},"SI4":{...},"SI5":{...}},
 "self_excite":"<自激机制一言>","mutual_offer":"<互激要约一言>",
 "rota_ok":true,"sunset_vote":"需|不需|限域|候填"}
```
## 级名（不滥：级必带证据指针，无据=CAND以下）
- **OFF**：面无件；**CAND**：候选·未实测/初铸未常役；**ACTIVE**：在役有实证；**FULLDRIVE**：全驱在役（机层自走，不候会话）。
## 层义
SI0基座（仓/账/塔）｜SI1研究进程｜SI2协商应答｜SI3递归引擎｜SI4量子准入｜SI5生态接口。
## 律
①覆写权归本线（他线行=派生基线，标【派生】）；②未实测言未实测；③态件落地即qfa机捕事件（FIX-11/13）。
