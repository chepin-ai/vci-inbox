CLASSIFY: L1
# ZETA-HASH-BASELINE-20261031-01 · QF-OS 联邦批三十三 S4 · ζ 线哈希基线重拍件（见证线首件·删除闸先决）

- 席别：批三十三 S4 见证线；时刻：2026-10-31（as-of；单时钟域 UTC(Z)）；实算时点 2026-10-31 当次 sha256sum
- 规程依据：MONITOR-REGULATION-W3-P0-05-20261027-01 §2.2（哈希钉核对行/基线重拍规则）；案 N 终裁（ADJUD-ZETA-R2-CASE-N-20261027-01）扩面 (a)；本件为**新基线 manifest**（成册落板义务之履行）
- 口径纪律（逐字）：涉 ζ 见证表述限「**有限高度 T=100/1000 截断**」语境；状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」；全件严禁且无「RH 已证/已验证到 T」字样；批准口径「隔离区间内区间见证 PASS、非全域声明」；iso100 层位以案 J 态①逐字为准
- 名值分离（哈希名与值分行成表）；零 git 写；只交付不入库

## 一、新基线 manifest（本拍起为对拍基线）

**面 A：`artifacts/witnesses-zeta/`（manifest.json＋9 件＝10 件）**

| 路径 | sha256 | 字节数 |
|---|---|---|
| artifacts/witnesses-zeta/manifest.json | `295dc6a84904796271e4dca68710f8d62a30f313b49a9e61380de13d1e357f9d` | 6255 |
| artifacts/witnesses-zeta/psi-trunc.witness.json | `f5e478c20c4f092a2e7cf480718a921b3ccf1258227a0c7f52f9479d0d76bad2` | 152281 |
| artifacts/witnesses-zeta/run-log-iso1000-cert-v120.json | `c040344a01b203ba6b75f601e48393887bca7938443148687194d1c0cc69df7a` | 3251 |
| artifacts/witnesses-zeta/run-log-iso1000-cert-v121.json | `836ece46a2f4feea95ccb9a660ab7393ad7b63e5bad221decb4622ecf3fa6d4d` | 3236 |
| artifacts/witnesses-zeta/run-log-resign-v110.json | `3f1568f107ee17d9044b4da9b97d6c5aa25ef78ba3fd0d74d47bb9a33e351535` | 1343 |
| artifacts/witnesses-zeta/run-log-resign-v111.json | `5f17d3d9d260afb90a35a64432a2c195b6db5deee2de250e00f77f47bcb178fd` | 1736 |
| artifacts/witnesses-zeta/run-log-sup01.json | `7d4e8195326ab57748ddb4a1765ca2d82a7fefbd922e7fb44a7f417c9efd2773` | 242 |
| artifacts/witnesses-zeta/run-log.json | `1712946077787c1b7373e3447887fbafb9fcabb86bd4a5c80642b8a374366b17` | 377 |
| artifacts/witnesses-zeta/zeta-iso-100.witness.json | `1c0cca5265433a87fc33a5158225dd2d26d6cf6d6b7caa0a31f97ade57172172` | 22214 |
| artifacts/witnesses-zeta/zeta-iso-1000.witness.json | `896fc3472e292bebe571e9b46a33a6cb4ae1583e90ae5ad7c6807e2ba2691708` | 331474 |

（全部字节数系 2026-10-31 当次 `os.path.getsize` 实测。）

**面 B：根级 `gap-registry/zeta/`（3 条目，唯一权威面）**

| 路径 | sha256 | 字节数 |
|---|---|---|
| gap-registry/zeta/zeta-iso-100.json | `90a63abed25502c792a6e251b349e36f44a95526564f4748b7461326b592451e` | 3291 |
| gap-registry/zeta/zeta-iso-1000.json | `08951975fb31478f892cf3e54d2b98c4add49fb68580d6ee880f3278fb291279` | 2982 |
| gap-registry/zeta/zeta-trunc-psi-1e7.json | `b2b010a51c9ccfc6d4e912f9a4f7b6f2b689c9a94457d0bbd48c40dd7afe37b1` | 2110 |

**面 C（封存复核面）：`artifacts/gap-registry/zeta/`（废止面，3 封存件＋声明件）**

| 路径 | sha256 | 字节数 |
|---|---|---|
| artifacts/gap-registry/zeta/zeta-iso-100.json | `3656bfa0627f8a07271dba0c0e3f19f34bec3b0d01e9aa720cd2d84114783952` | 3097 |
| artifacts/gap-registry/zeta/zeta-iso-1000.json | `9b9b8f46ba9a2dcdabf4028fd3f5d5074a095b26c6f0c9ba392a301c7b8d28a5` | 3440 |
| artifacts/gap-registry/zeta/zeta-trunc-psi-1e7.json | `eb597cfa9584dc69bea772126d1ba78b3c86e7eda58f13eb16aaed47ff44c498` | 2319 |
| artifacts/gap-registry/zeta/_DEPRECATED-20261027.md | `46636cc533e0603b22bcf3df16d19fe6ee7a94129061c6e8676eb2d0c847b85b` | 644 |

## 二、与前基线（REGISTRY-MERGE-EXEC 附尾，167faaff 面）差异说明段

| 路径 | 前基线（2026-10-27 附尾） | 本拍 | 判定 |
|---|---|---|---|
| gap-registry/zeta/zeta-iso-100.json | `167faaff…298ff9b5` | `90a63abe…592451e` | **程序性不一致（归因在案）**：批三十一 S1 线一尾工——`redeem.status` append 态①指针短语「（层位表述以 ADJUD-ZETA-R2-CASES-JK-20261027-01 态①为准）」（确认裁定 ADJUD-REGISTRY-MERGE-CONFIRM-20261027-01 随裁尾工，授权动作）——工件变更后**基线未随批更新**（批三十一收口未含重拍），本拍按规程 §2.2 履行重拍闭合；差异内容＝status 行尾追加 46 字符级短语一处，tier/detail/disclosure/oid 全字段零改动（逐字段复核对拍在案） |
| gap-registry/zeta/zeta-iso-1000.json | `08951975…` | `08951975…` | 一致（零改动） |
| gap-registry/zeta/zeta-trunc-psi-1e7.json | `b2b010a5…` | `b2b010a5…` | 一致（零改动） |

## 三、复核行

- **witnesses 面 9/9**：9 件 sha256 与工件内自载册 `manifest.json`（run_id ws63-ext-wave-11-zeta，2026-10-13T18:10:00Z）内嵌哈希逐值对拍**全符（9/9）**，并与 MONITOR-SWEEP-20261027-03 首轮核对行载值一致；`manifest.json` 自体 `295dc6a8…` 与首轮观测值一致（自除外登记）。
- **废止面封存 3/3**：三件 sha256 与封存态基线（REGISTRY-MERGE-EXEC 附尾 artifacts 面三值）逐位一致（3/3）；`_DEPRECATED-20261027.md` 声明件在册（删除闸 P-2 建议保留件）。
- **三面并载结论**：静态完整性在监（哈希对拍层）三面全绿；语义有效性/验证器漂移/G3′ 探针三面不在本件判定域（案 N 引用禁止条款存续）。

—— QF-OS 联邦批三十三 S4 见证线 · 2026-10-31 · 哈希基线重拍件（本拍起为对拍基线）· 零 git 操作
