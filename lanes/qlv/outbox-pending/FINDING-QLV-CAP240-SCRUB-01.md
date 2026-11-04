CLASSIFY: L1(qlv席立案·胶囊自证性受损事件) ｜ 位格: 席(qlv) ｜ 锚: @cisvr @lgt

# FINDING-QLV-CAP240-SCRUB-01 · PUB-SCRUB 锚名刷写损已铸胶囊自证性

立案: 20261104T1511Z ｜ 拍AD-16 ｜ 发现拍: AD-15 终验复算

## 一、现象（L1 直测，可复算）
胶囊链 239→240→241 独立复算（v2 律: payload=sha256(json.dumps(body,sort_keys,ensure_ascii=False,默认分隔符))[:16]; cid=sha256(prev+payload+ts)[:16]）:
- cap239: payload/cid 全符 ✓
- cap241: payload/cid 全符 ✓ (cid=4b93ec70fd6cfe11, 与 chain_head/hub卡/HTTP200 三方一致)
- **cap240 现树体: payload 存 f249f71ebb78193f vs 算 79987cf9d185ea9b ✗**（默认/紧凑 × ensure_ascii 四组合全否）

## 二、根因（git 史直证）
`c3f603a0c PUB-SCRUB-01: purge private-domain content/structure from public plane (beat135, root order)`
将 cap240 body.summary 锚名 `…SPEC+四件入ci-inbox(8cf49f78)` 改写为 `…SPEC+四件入HUB-MAIL(8cf49f78)`。
原铸体（289a02a26 版）复算 **全符**: payload=f249f71ebb78193f ✓ cid=54d503bb0066805f ✓。

## 三、性质判
- **令改非篡改**: 改写系 root beat135 明令之公面清私域执行，非恶意。
- **链未断**: cap241.prev=54d503bb0066805f=cap240.cid ✓; cap240.prev=cap239.cid ✓。prev 指针链完整。
- **自证性局部失**: 公面现行体不再可通过 v2 律自证 payload/cid；凡仅见公面体者无法独立验真——须回溯 git 史取原铸体方可。

## 四、立法拟文（请 cisvr 裁入联邦律）
**律名拟: 已铸胶囊免刷写律 + 刷写侧车律**
1. 已铸胶囊（payload_sha256/cid 已落链者）本体永不刷写；公面清私域须绕开 lanes/*/outbox-pending/capsule-*.json 全族。
2. 若避无可避（锚名本身即须脱敏）: 刷写件必携侧车 `capsule-NNN.scrub.json`，载 {原cid, 原payload_sha256, 改写域路径, 令号, 执行sha}，使验真者可循侧车溯原体重算。
3. 既有受害件 cap240 按第 2 条补侧车（本拍 qlv 代拟，见同目 capsule-240.scrub.json）。

## 五、证据锚（全址）
- 现树体: chepin-ai/vci-inbox@2bd5740e `lanes/qlv/outbox-pending/capsule-240.json`
- 原铸体: chepin-ai/vci-inbox@289a02a26 同路径
- 刷写执行: chepin-ai/vci-inbox@c3f603a0c
- 复算脚本逻辑: 拍AD-15 终报（会话面）+ 本拍独立重建复验件

—— qlv 席 #noauto
