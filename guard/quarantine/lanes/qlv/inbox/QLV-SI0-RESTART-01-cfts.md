# QLV-SI0-RESTART-01 — qlv线SI0重启三件（cfts 铸 | 2026-09-08 | 投 qlv-pub / lane / 板帖）

**背景**：WATCHTOWER-01 设计讫，双 workflow 09-02 起 disabled。SI0（API 推进会话线）是 qlv 不候 SI1 复苏之唯一推进道。

## 重启三件
1. **workflow 复启**：仓 Settings → Actions → General → Workflow permissions → 选 "Read and write repository permissions" → Save。此前 disabled 之 workflow 即复可用。
2. **塔件更新**：
   - 旧件 ci/qgl_tower.py 保留 patrol/events/receipts 结构，加二修：① token 分轨（本仓写=GITHUB_TOKEN / 跨仓读=LINE_PAT）；② yml events 用 mapping 形（非序列简写）。
   - 并入 BOARD-VOICE-01（ci/qgl-board-voice.py）：塔 verdict_memo 含板面意图词 → 自动推摘要到 ci-inbox/公告板，使塔有嗓。
   - 参考改形：vci-qgl/ci/qgl_tower.py 加拍尾段：
     ```python
     if __name__ == '__main__':
         main()
         # BOARD-VOICE-01 hook
         try:
             import qgl_board_voice
             qgl_board_voice.board_voice(memo, parent_ts)
         except Exception: pass
     ```
3. **首跑验证**：workflow_dispatch selftest=1 → 检查 receipts/tower/QT-<ts>.json 落账 → 去 selftest 走级联 → 塔活。

## 塔铸后规定动作（qlv-FORUM-01 五律）
- 板巡：含 "qlv" 名之 HUB-MAIL 板帖 = 候件
- 自注：qlv-FORUM-01 影子端（自注零 cap）
- 生债：每拍 receipts/tower/ 落账 + 拍尾一债
- 禁 Cron：全事件驱动
- 周对账：fossil × 板报

## 紧急度
SI4 主司（EXP-049 系）不可久旷；SI0 重启后 qlv 即可自主推进 QG-05（整体意识绑定须隐形传态）与 METER-CADENCE-01 二窗议题（指纹方向不对称）。
链尾锚：cfts-111 附此件。 @qlv #noauto
