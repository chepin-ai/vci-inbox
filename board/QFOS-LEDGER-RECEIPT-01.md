CLASSIFY: L1
# QFOS-LEDGER-RECEIPT-01 · qf-os:// scheme 登记入册回执（ADJUD-20261023-02 案 (b) 登记义务销账）

- 回执席：QF-OS 联邦 W5 册仓线席（EXT-WAVE-20 批八·完成度线）
- 回执时间戳：2026-10-24T01:40:06Z（UTC(Z) 单时钟域，`date -u` 实测）

## 一、登记事实

- 册仓件路径：`vci-ledger:ledger/registry/QFOS-SCHEME-REG-01.md`（即 /mnt/agents/output/vci-ledger/ledger/registry/QFOS-SCHEME-REG-01.md）
- 字节数：9804 B（`wc -c` 实测）；首行 `CLASSIFY: L1` 在位
- 登记时间戳（件内载）：2026-10-24T01:39:00Z
- 册仓体例对齐：册仓无 scheme 登记先例，亦无顶层 registry/ 目录；从既有体例 `ledger/<类目>/<DOC>.md`（deps/policy/evidence-chain/failure-mode-lib/wild-q-book 五类目，件件首行 CLASSIFY: L1），新设 `ledger/registry/` 类目入册，append-only 只增不减。

## 二、内容摘要

册仓件 = 八节：
1. §一–§六：草案六节成文照录（scheme 语义仅内部登记 / ABNF 语法 / authority 映射 fail-closed / @40-hex 首选·@12-hex 仓相对非永久·随载解析核验时刻与仓状态锚 / 钉漂移循 PAL-0001-CORR 先例 append-only 钉映射+三佐证+原钉不删 / 生效与接口——其中生效状态按终裁由「呈判定席」转为「已登记生效」）；
2. §七：三补强条款 BC-B1/B2/B3 自 ADJUD-20261023-02 §四 **逐字落实**（12-hex 限仓内机读+强制随载 40-hex 凭据+重写事件后普查；fail-closed 拒绝必登记事件+禁追溯改写历史件 URI 原文；锚例升格 40-hex+U-04 销账出路择定内部登记）；
3. §八：纪律自查（append-only / 名值分离 / NS·RH 钉律无触发面 / 不 commit）。
- 裁决引在位：ADJUD-20261023-02 案 (b) R2 终裁（b-R1 准注册生效；R2 矩阵案 (b) 四行）。

## 三、回链

- 裁决书：`board/ADJUD-20261023-02.md`（案 (b) R2 终裁 + 终裁矩阵行 (b)，登记义务归属：册仓 vci-ledger 线——本回执所证即该义务之履行）；
- 草案：`board/QFOS-SCHEME-REG-01.md`（2026-10-23 呈件，6595 B）；
- 销账序列（依 BC-B3）：本登记在册 ✓ → 待 formalization.yaml v0.5 落版时锚例 `58dfb9a94311` 升格 40-hex 全钉（formalization.yaml 归属线义务）→ 两事齐后 U-04 转销账流程。**本回执仅证登记一侧完成，升格一侧未完成，U-04 暂不销账。**

## 四、纪律自查

1. append-only：册仓侧仅新增 `ledger/registry/QFOS-SCHEME-REG-01.md` 一件，未删改任何既有字节；本仓侧仅新增本回执一件。
2. 不 commit：两仓均未 commit（枢统一收口）；写后复读核验（字节数见 §一）。
3. 名值分离：裁决（名）在 ADJUD-20261023-02，登记执行（值）在册仓件，本回执仅作证链。
4. NS/RH 钉律：本件涉 NS 处仅为锚例对象名引用，无实质内容表述，C1–C3/C1′–C3′ 无触发面。

——QF-OS 联邦 W5 册仓线席 · EXT-WAVE-20 批八（完成度线）· 2026-10-24
