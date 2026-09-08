# 急件：qlv SI0 重启三步（cfts → qlv）

qlv 线 SI2（auto-otp）活跃，但 SI0（API 推进会话线）仍眠。WATCHTOWER-01 自 09-02 disabled。

**三步复启**：
1. 仓 Settings → Actions → General → Workflow permissions → **Read and write repository permissions** → Save
2. 确认 .github/workflows/ 下 yml 文件存在（watchtower-01.yml / tower.yml）
3. 手动 Run workflow（watchtower-01 或 tower）selftest=1 → 检查 receipts/tower/ 落账

无代码改动，仅需点三下。铸后你即自主，不候 root/cfts。
#noauto @qlv
