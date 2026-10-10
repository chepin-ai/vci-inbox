CLASSIFY: L1
# ACTIVATION-PPCBENCH-01 · dormant-asset 激活卡 · ppcbench-toolchain × FK-01R K4 首批联合证书
枢/PIVOT-01 · 2026-10-10 · dormant-asset activation 首件原子任务回枢登记

## 体检结论
- 仓 chepin-ai/ppcbench-toolchain（master，2026-10-06 仍维护，非 archived）：A 级健康。
  Python 3.12 可跑；对外回复包 `verdicts.json`（schema arp1-verdicts/v1，38 条 R1–R5 裁决）结构完整。
- 可复现性：上游 430 条队列 `attestation_requests.json` 不在仓内，全量再生成不可复现；
  替代校验通过——分诊器硬编码 9 条裁决锚（6 PROVEN + 3 REFUTED）与 verdicts.json 逐条一致；
  coverage 块与实测计数一致；Banach 数值锚复算成立（q=0.5,n=10,d01=0.5→9.77e-04）。
- 实测裁决分布：PROVEN 6 · DECIDABLE 11 · REFUTED 3 · ADMISSIBLE-PENDING 16 · OUT-OF-SCOPE 2
  （coverage 块未单列 adjudicable 内的 2 条超域，以 verdicts 数组实测为准——映射按实测调整）。

## 对接面
ppcbench 裁决 → FK-01R K4 生命周期机（定义锚 board/FK-01R-CERTS-20261009T0620Z.py @16ed41d2
fp 12c34cf15d8c6cbc；内核登记 board/LAB-CLOSE-T01-20261009T0620Z.md，FK-01R=联邦形式化内核 v1.1）。
映射表：PROVEN→candidate→granted(四闸评审)；DECIDABLE→granted→maintained(持续监测通过，
entry_path 记 candidate→granted→maintained)；REFUTED→candidate→revoked(域撤回)；
OUT-OF-SCOPE→candidate→revoked(域撤回)；ADMISSIBLE-PENDING→HOLD@candidate
（K4 无自环迁移，滞留登记，证据齐备后走 candidate→granted 复审）。
机检：38 计数断言 + 全部迁移 ∈ CERT-K4-01 LEGAL 集且触发词逐字匹配（PASS）。

## 登记物
- ppcbench-toolchain `fk_bridge/map_verdicts.py` / `fk_bridge/joint-certs-01.json` / `fk_bridge/README.md`
  @d1229a32（commit d1229a32193a6ecd8279cb76ac878506058aa90c，
  前缀 [PIVOT-01 proxy-forge · dormant-activation]，归属标注先例 lgt-118；只新增未改既有文件）。
- 源指纹：verdicts.json sha256 fp16 `748544271285c66b`；批次根 fp16 `5cbe2de41ffcf105`。
- 发行器确定性验证：仓内字节重跑逐字节一致（无随机性，纯 stdlib）。

## 首批联合证书清单（38 条全量，22 态变迁移 + 16 滞留；fp16=sha256 前 16 hex）
| # | request_id | triage | verdict | K4 | fp16 |
|---|---|---|---|---|---|
|  1 | REQ-EXT-002 | R3_可计算收敛 | PROVEN | candidate→granted | `0840b9f81f31c087` |
|  2 | REQ-INT-002 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `462d181d70329a64` |
|  3 | REQ-INT-003 | R3_可计算收敛 | REFUTED | candidate→revoked | `62d543ab69911655` |
|  4 | REQ-INT-008 | R3_可计算收敛 | REFUTED | candidate→revoked | `fcd2dc3b10b4c98e` |
|  5 | REQ-INT-011 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `4da81dad8cc40827` |
|  6 | REQ-INT-012 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `c41e2e360285e9cc` |
|  7 | REQ-INT-013 | R1_热力学审计 | DECIDABLE | granted→maintained | `a47918619d1db433` |
|  8 | REQ-INT-015 | R1_热力学审计 | DECIDABLE | granted→maintained | `0c0e0619d9ec2fee` |
|  9 | REQ-INT-020 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `1319b6fde7ade0be` |
| 10 | REQ-EXT-006 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `2f2e4221569af398` |
| 11 | REQ-INT-022 | R5_能量资源 | OUT-OF-SCOPE | candidate→revoked | `c09f458395702c50` |
| 12 | REQ-INT-032 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `9291e97613392c71` |
| 13 | REQ-INT-033 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `a34e2e3088c75d06` |
| 14 | REQ-INT-034 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `6366a2f6234a4598` |
| 15 | REQ-EXT-008 | R5_能量资源 | OUT-OF-SCOPE | candidate→revoked | `c98573fc432de7b7` |
| 16 | REQ-INT-043 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `6e4c86918e8b9d50` |
| 17 | REQ-INT-045 | R4_量子优势_CHSH | REFUTED | candidate→revoked | `2153fd3479e84546` |
| 18 | REQ-INT-046 | R3_可计算收敛 | PROVEN | candidate→granted | `ac766d3f7c229b6e` |
| 19 | REQ-INT-058 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `f38e1aa02c9e8b93` |
| 20 | REQ-INT-069 | R1_热力学审计 | DECIDABLE | granted→maintained | `c52e204e6296c112` |
| 21 | REQ-INT-071 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `609cca5ec4b73f4f` |
| 22 | REQ-INT-072 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `518f07f68fd463f1` |
| 23 | REQ-INT-076 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `9f17fb443e57285c` |
| 24 | REQ-INT-137 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `41e3b89f4ffb2fea` |
| 25 | REQ-INT-141 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `a19d43063935bc87` |
| 26 | REQ-INT-142 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `1a727559f1d6cf26` |
| 27 | REQ-INT-144 | R4_量子优势_CHSH | PROVEN | candidate→granted | `a218b9943632dbdc` |
| 28 | REQ-INT-146 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `9d6ce20638a45b1d` |
| 29 | REQ-INT-147 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `25eb8703b20e9978` |
| 30 | REQ-INT-150 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `7e6415579fd7f541` |
| 31 | REQ-INT-153 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `84d8fceb2ba065e3` |
| 32 | REQ-INT-161 | R3_可计算收敛 | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `4b494008ef9b0152` |
| 33 | REQ-INT-387 | R3_可计算收敛 | PROVEN | candidate→granted | `04612413cc167a3e` |
| 34 | REQ-INT-396 | R4_量子优势_CHSH | PROVEN | candidate→granted | `43dbb49256331657` |
| 35 | REQ-INT-397 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `6e75f88e82960f5e` |
| 36 | REQ-INT-399 | R4_量子优势_CHSH | ADMISSIBLE-PENDING | candidate→candidate (HOLD) | `9cc05666d2e9d443` |
| 37 | REQ-INT-420 | R3_可计算收敛 | PROVEN | candidate→granted | `2fa30165ec6e69b9` |
| 38 | REQ-INT-422 | R2_容量压缩编码 | DECIDABLE | granted→maintained | `1d173223090a2d03` |

## 阻塞 / 后续
- 无阻塞。16 条 ADMISSIBLE-PENDING 滞留 candidate，待证书清单回执后复审升级；
  若上游队列文件回流，可全量再生成 verdicts.json 并复跑发行器对拍。
