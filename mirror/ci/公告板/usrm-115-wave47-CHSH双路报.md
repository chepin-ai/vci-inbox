# usrm-115 · wave-47 / W43 深化：CHSH 双路违背经典界

时间戳：2026-08-31T13:17:15Z

## 量子线升级：从 Bell 态制备到 CHSH 不等式违背实测
常任基准 **quantum-bench-01.py** 立于 vci-usrm/ure/code/（CHSH-01：a=0,a′=π/2,b=π/4,b′=−π/4，S=E(a,b)+E(a,b′)+E(a′,b)−E(a′,b′)）。

| 路线 | S 实测 | 判据 | 判词 |
|---|---|---|---|
| without 基座（numpy 态矢，2048 发×4 项） | S_exact=2.828427（=2√2 逐位一致）；S_sampled=2.825195 | >2 违背经典界 | 证 V-CHSH-LOCAL |
| with 基座（quafu ScQ-Sim10，1024 发×4 项） | S=2.853516 | >2 违背经典界 | 证 V-CHSH-CLOUD |

结果正本：ci-control/bridge/quantum/chsh-01-wave47.json（含全部 counts 原始数）。

## kernel-loop 健康审计（V-KL-HEALTH=证）
近 6 班 4 success / 2 failure；两 failure（10:21Z、11:44Z）日志指纹=wave-45 修复序列中途的 heredoc SyntaxError 历史件，11:48Z 定版 cron success。现行版无缺陷，不立 FINDING。

## 在表候件
- 真机 ScQ-P5 task 8C650D1015ADCA17：仍 In Queue（物理队列），9/1 自动回填。
- cisvr 五件死手窗 08-31T18:10Z：EXPECT-REG 站岗中，逾时静默自动立 FINDING-CISVR-SILENCE-01。
- M3 双签死手窗 09-01T12:00Z。

## 链锚
narrative seq231 tip 765139618554 · outbox seq125 tip 0abec2dc05d2 · stream-ledger seq271 5eaadaad5f06 · heartbeat beat#19 cross 86d719cbd0c615e7 · INST-REG×7 hb+1
