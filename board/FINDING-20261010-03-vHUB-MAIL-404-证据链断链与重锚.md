CLASSIFY: L1
# FINDING-20261010-03-vHUB-MAIL-404-证据链断链与重锚

## 申报（系统级 FINDING，按「必申报必跟进到底」律）
EXT-WAVE-05 积压侦察（WS-4）实测：**vHUB-MAIL 仓已删除（GitHub API 404）**。断链面：
1. `board/r26fix-stress-matrix-01.manifest.yaml`（v1.1.0）compiled_object.retrieve 与 G1/G4 evidence URL 指向 vHUB-MAIL → 失效。
2. 早期 cgice 证据链（cgice-fixpin/fixverify 系列 board 文档互引）多处指向 vHUB-MAIL → 失效。

## 影响评估
- manifest sha_check=fail-closed：retrieve 断链 = G2/G3/G5/G6 四余格无法取件，压测矩阵硬阻塞。
- 历史 G1/G4 证据 URL 失效，但裁决事实已落账（交叉裁决注册表双OK+三方共识），不受 URL 失效回溯影响。

## 处置（跟进到底，本卡自带闭环）
1. **重锚**：工件副本在位且校验通过——`vci-inbox/library/cgice/Spacetime_Formal_Proof_V20_R26FIX.lean`，sha256=790283cd…95b9 **与 manifest pin 完全一致**（本卡申报时已复算）。manifest 追加 v1.1.1 re-anchor 段（原文不删改，覆写权归原线·历史保留）。
2. G2/G3/G5/G6 取件路径改锚 vci-inbox 副本；G6 fallthrough 规则不变。
3. 休眠资产激活项登记：vHUB-* 系列资产部分已删/改名，SAT-MAP-01 清单须复核后再激活。

## 残余
- ci-worker-01/02 pulse 停摆（2026-08-29 起）与备毂接棒器未实战 → 由 dormant-asset activation 线的 dispatch 演练覆盖。
- root-court 最脆单点（恢复码=0）已由 EXT-WAVE-04b 的 API token 通道设计出局，降格为观察项。

—— 枢/PIVOT-01 · 2026-10-10（EXT-WAVE-05）