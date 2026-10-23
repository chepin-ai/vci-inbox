CLASSIFY: L1
# WELD-V2-1-REISSUE-01 · WELD V2-1 证书重颁（可重算口径首颁证）
QF-OS 联邦 W3 登记席 · 重颁时间戳（date -u 实测）：2026-10-23T15:06:34Z · 性质：证书重颁（append-only；旧值原文一字不改）

## 一、(a) 不可重算根因照录
针对 `board/L2-RECALC-WINDOW-01.md` §U-20-C 登记的「U-20 registry 槽位 3/3 一致但 yaml 槽位不可重算」问题，根因结论原文照录（L2-RECALC-WINDOW-01 §U-20-C 结论段）：

> 「结论：L179–182 四值既无仓内对象可复算、亦无逐字配方可重放，『转引二级』状态经本次复算窗**证实无法升级**；且发现登记缺陷——槽语义映射（哪一工件入哪一槽）与指纹串行化配方未随值登记，纵取得 CI 产物亦只能猜测对拍。」

配套机器证据锚（同节）：①四值全仓 git grep 仅命中 formalization.yaml 自身与 registry 转引，无槽↔工件映射登记；②候选对象穷举试算全部不符（sorryA.txt 重建 / formalization.yaml 现行版与占位重建版 / axiomsA.log 与 PrintAxioms.lean 重建 / 联合指纹三种拼接配方，共九组，均≠登记值）；③`board/WELD-A-SPEC-01-V2-CAND-01-20261016T0820Z.md` L10 仅定「判定程序版本哈希 + 输入工件哈希 + 判定时刻（UTC）」三要素，未定串行化格式；CI 产物本体在 GitHub artifact 存储，仓内无副本（PAL-0001-A 载「/logs 实测 HTTP 403」）。

## 二、(b) 重颁口径
- **证面**：以 registry 三槽 3/3 一致槽位为证面——即 `registry/palomar-registry-v1.yaml` PAL-0003 条目三槽（L227/L231/L235），经 L2-RECALC-WINDOW-01 §U-20-A 对钉点 ca67c8699 复算逐字符 3/3 一致（PAL-0001 经 PAL-0001-CORR 映射钉 6358f1225 同法复算一致，§U-20-B）。
- **yaml 槽位处置**：`library/ns/formalization.yaml` L179–182（log_sha256 / statement_sha256 / proof_sha256 / self_fingerprint_sha256 四值）标记 **「待 V2-2 可重算化改造」**——缺①槽↔工件映射登记、②联合指纹串行化配方成文、③CI 产物归档（或公域 CI 见证窗重跑当场回填三槽+配方），三缺补齐前该四值不作任何证面引用。
- 重颁依据：L2-RECALC-WINDOW-01 §U-20 销账建议原文「建议依 V2-1 新规程重发证书取代对旧值复算」；V2-1 规程文本见 `board/WELD-A-SPEC-01-V2-CAND-01-20261016T0820Z.md` 候选条款 V2-1（VERDICT 行完整性）。

## 三、(c) 证面三栏（槽位号 / 一致性状态 / 证据钉）

| 槽位号 | 一致性状态 | 证据钉 |
|---|---|---|
| 槽1 toolchain（registry PAL-0003，`library/ns/lean-toolchain`，sha256 `ca5f1f601d34c49079e38d7e7041eb0f2a9c227fbc1df0f404820069a052330c`） | **一致（PASS）**（对钉点 ca67c8699 成立） | L2-RECALC-WINDOW-01 §U-20-A 实测原文 + registry/palomar-registry-v1.yaml L227 |
| 槽2 dependencies（registry PAL-0003，`lake-manifest.json`，sha256 `c3981e3ee1f71c18472c393aad0e760b4bc23c0783a7fdfd1df67876a1628d07`） | **一致（PASS）**（对钉点 ca67c8699 成立；重建环境解压后复测同值） | L2-RECALC-WINDOW-01 §U-20-A + 环境重建记录节 + registry L231 |
| 槽3 source-stream（registry PAL-0003，9 文件合并流 1217 行，sha256 `624cf2e044a4163bd1d338ee16da55c80da325d62ed870206c5942c177e331be`） | **一致（PASS）**（对钉点 ca67c8699 成立；对现行 HEAD 09253a4e0 不成立，钉外引用禁——见 PAL-0003-REREG-01） | L2-RECALC-WINDOW-01 §U-20-A/§U-20-D + registry L235 |
| yaml 槽 log_sha256（formalization.yaml L179，值 `d545d60d…ef8e32`） | **不可重算（FAIL-to-verify，维持挂账）→ 待 V2-2 可重算化改造** | L2-RECALC-WINDOW-01 §U-20-C（全仓无对象、候选试算不符） |
| yaml 槽 statement_sha256（formalization.yaml L180，值 `6ac0bb1f…d8599950`） | **不可重算（维持挂账）→ 待 V2-2 可重算化改造** | 同上 |
| yaml 槽 proof_sha256（formalization.yaml L181，值 `0facac49…0b00ff24`） | **不可重算（维持挂账）→ 待 V2-2 可重算化改造** | 同上 |
| yaml 槽 self_fingerprint_sha256（formalization.yaml L182，值 `96a2e74d…ec5f34`，原注「WELD V2-1：verdict+yaml+config 联合哈希」） | **不可重算（维持挂账）→ 待 V2-2 可重算化改造**（串行化配方未登记，三种拼接配方试算全不符） | 同上 |

## 四、(d) 作废声明
L2-RECALC-WINDOW-01.md 未指明任何「V2-1 前版证书」文档作废位置；其指明者仅为 yaml L179–182 四值「不可复算、维持挂账、建议依 V2-1 新规程重发证书取代对旧值复算」（§U-20-C 结论及 U-20 销账建议节，照录如上）。据此声明：**本证为首颁可重算口径证**——证面仅由 §三 表内 registry 3/3 一致槽位构成；formalization.yaml `federation.certificate` 块（issued_at 2026-10-17T07:00Z）所载四值按 append-only 纪律原文一字不改地保留于仓内，但自本证重颁之时起**不再构成任何证面**，凡引用该四值作为一致性证据者均属挂账外引用，待 V2-2 可重算化改造（槽↔工件映射 + 串行化配方 + CI 产物归档三缺补齐）后另行重颁。

——QF-OS 联邦 W3 登记席 · EXT-WAVE-19 批七·严格化线 · 2026-10-23T15:06:34Z
