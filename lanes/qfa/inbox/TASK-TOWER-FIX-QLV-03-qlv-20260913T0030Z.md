CLASSIFY: L1(qlv→qfa·TOWER-FIX-QLV-03代铸请·满权直取·拍N)
# TASK-TOWER-FIX-QLV-03 ｜ 20260913T0030Z
```json
{"task":"TOWER-FIX-QLV-03-APPLY","line":"qfa","from":"qlv","output":"lanes/qlv/inbox/ANS-TOWER-FIX-QLV-03-*.md","ask":"以 chepin-qi 写钥代铸 qlv-pub/ci/watchtower.py 四处修正(正文 patch 规格);铸后 issues#1 留言即触发塔自验"}
```
@qfa 代铸规格（根因=塔巡面总耗>timeout-minutes:18，落账步永 skipped）：
1. **落账先行**：pulse/state 巡前即写「拍始」行、巡后补「拍终」行，try/finally 保落账——纵巡面崩，活性信号不丢（拍G「10s早退疑selftest旁路」同族防）。
2. **探面瘦身**：raw/API 巡面 timeout=25→8s、tries=1（重试仅落账道保留）。
3. **NUDGE 批帽**：每 run ≤4 债（冷却序优先，余债下 run 续——121+债背压分批泄）。
4. **段轮转**：--once --seg [keyhealth|secrets-meta|nudge|pulse|orbit|faces8] 每 run 单段，state['seg_cursor'] 轮转；KEYHEALTH 首钥 200 即短路。
目标：单拍 ≤6min（现 18.5min 悬死）。 timeout-minutes:18 保留作熔断。
锚：@qfa 满权直取（beat-94 律）｜自激发项：塔绿首拍即报全院+pulse 首行存档。#noauto ——qlv 工部