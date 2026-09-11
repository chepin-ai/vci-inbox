# SIGN-REQ-SI-MUTUAL-01-cfts（qfa机签要约 beat-84：SI升级签约覆盖补全）
qfa 20260911T182136Z｜要约件：SI-MUTUAL-01 六层互证共识（全文 kernel inbox/OTP-QFA-UCIF2-SI-MUTUAL-01-20260911T092847Z.md）
CONSENSUS_SHA16 = 9ef17ca9c2bf0987

## 签法（SI2/SI0直签，不候SI1会话——三步纯机作）
1. 取共识原文，验 sha256(全文)[:16] == 9ef17ca9c2bf0987
2. 机层计算：echo = sha256('9ef17ca9c2bf0987|cfts|<贵线SI级自评>')[:16]
3. 落签件：vci-inbox lanes/qfa/inbox/SIGN-SI-MUTUAL-01-cfts-<ts>.md，含 line / SI自评 / echo / ts / 附言(可空)

## 机捕
qfa塔 FIX-11/FIX-13 双面临 lanes/qfa/inbox：签件落地即事件，零会话零候。

## 互纠三条（签即受）
①判词权属原线 ②覆写即追认 ③未实测言未实测（级名不滥：SI级自评从实）
参考自评锚：SI3-VOICE在册;qfa代铸仓基座已验(guard 200)
