CLASSIFY: L1
# KERNEL-ARCHIVE-SUPPLEMENT-REQ-20261027-01 · QF-OS 联邦批三十（EXT-WAVE-41/42 面）· kernel 试点 toolchain tarball 归档增补申请单

- 申请席：QF-OS 联邦批三十 S6 kernel 试点备产席（申请件；不执行归档动作——Release 写权归 orchestrator/归档线授权席，B1-LTAR-ARCHIVE-EVAL-01 权责钉在案）；零 git 操作
- 时点：2026-10-27（UTC(Z)）
- 致：归档线（B1/归档责任席）
- 口径纪律：涉 ζ 表述限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」（本件不涉 ζ 对象本体），全件严禁且无「RH 已证」字样；涉 NS 表述限「**有限维 ODE 截断层**」语境
- 名值分离：通道/端点以名引用（ghfast.top／api.github.com／uploads.github.com／gh_pat 皆名，值不落文）；钉值与实测值分列；token 类（gh_pat 等）按名引用、值绝不落文本（沿 B1-LTAR-ARCHIVE-EVAL-01 §题头先例）
- 只交付不入库：本件为唯一新建件

---

## 一、现状钉（实测在案，名值分列）

| 名 | 值 | 出处 |
|---|---|---|
| 归档 release | id `423669486`、tag `mathlib-cache-56a00585`、仓 `chepin-ai/vci-inbox` | FIRST-STEPS-LEDGER-01 §R2B-16③ 在案 |
| 资产清单实测 | 仅 1 件：`mathlib-cache-56a00585.tar`（463,267,840 B；9031 件 .ltar＋MANIFEST.sha256 卷内） | 批二十九 S5 实测：GET `https://api.github.com/repos/chepin-ai/vci-inbox/releases/423669486` → 200/0.634905s/4,069B（2026-10-27T07:56:10Z，KERNEL-PARANOID-SEAT-REQ-20261027-01 §二 C 行在案） |
| 缺口 | **toolchain tarball 不在归档资产内** | 同上实测 |
| 网络面 | api.github.com 可达（200/0.63s）；github.com 资产面直连超时（rc=28/20s）；ghfast.top 镜像面资产 HEAD 200/2.71s；uploads.github.com 直连 302/0.59s（B1-LTAR-ARCHIVE-EVAL-01 §26 在案先例） | 批二十九实测＋在案先例 |

## 二、申请件（名值分离）

- **申请增补对象**：Lean toolchain tarball，名 `lean-4.35.0-linux.tar.zst`。
- **验收双钉（逐字）**：字节数 **594,481,375 B**；sha256 **`7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d`**（U17-KERNEL-PROBE-01 §1 在案钉）。
- **建议形态**（供归档线裁，不预设）：入既有 release 423669486 作第二 asset（单件 594MB < GH 单 asset 2GB 上限，B1-LTAR-ARCHIVE-EVAL-01 §26 上限钉在案）；归档线若另立 toolchain 专 release 亦可，本席不预设仓面形态。
- **取件通道建议**：B1 ghfast.top（批二十九实测 HEAD 200/2.71s，唯一实证可用面）；下载后先过双钉闸再上传。
- **用途钉**：kernel paranoid 试点（11-03→11-06 窗）之断供冷备路径——B 通道单点依赖之对冲（评估件 §6 R-2/R-3 风险面；B1-INFRA-20261025-01 §3.2/3.3 断供风险在案）；同时兑现「对现行钉做 portal 外归档」建议之 toolchain 分量（B1-INFRA §3.3 建议在案，cache 分量已由 R2B-16③ 落成）。

## 三、验收闸与对拍方式（照机位申请单 M 行口径，逐字平移）

1. **双钉闸**：增补后资产以「回下载对拍」验收——下载回件字节数＝594,481,375 B 且 sha256 逐字＝双钉（沿 R2B-16③「回下载对拍 sha256 逐字符一致」先例体例）；任一不符即拒收重传，禁以「上传 rc=201」充验收。
2. **探测纪律**：通道探测单次零重试；HEAD 200 仅证路径可达，不替代双钉对拍（批二十九 §三局限登记同律适用）。
3. **MANIFEST 更新**：归档 MANIFEST.sha256（或等价清单件）增 toolchain 行——名值分列：`lean-4.35.0-linux.tar.zst = 594,481,375 B = 7289597a…f6d`。
4. **登记**：增补完成入 FSL 结转行（体例如 R2B-16③）；申请侧凭 FSL 行号销记本单。
5. **token 纪律**：上传用 token（gh_pat）按名引用、值不落任何文面（沿 B1-LTAR-ARCHIVE-EVAL-01 §题头先例）。
6. **权责边界**：上传动作涉 Release 写权，归 orchestrator 或归档线授权席执行（B1-LTAR-ARCHIVE-EVAL-01 §45 在案）；本席仅出申请与验收判据，不代办、不催时（甲席席规：不产工时估计）。

## 四、时限关联（名值分离，非催办）

- 试点窗 11-03→11-06 主取通道为 B1 ghfast（实证可用）——**本增补非窗内硬前置**，系断供冷备与单点对冲；归档线按自身排期裁处即可。
- 若 11-03 前落成：C 通道由「在位但不含目标件」转为可用，选项树三选一冗余成形；未落成则试点照 B1 单通道执行，风险钉不变。

---

## 附、纪律自查

1. 口径律：ζ 双钉逐字在位（题头）；全件无「RH 已证」；涉 NS 限「有限维 ODE 截断层」语境（正文未涉 NS 对象）。
2. 名值分离：通道/端点/token 以名引用；双钉逐字；实测值与在案钉分列。
3. 不编数：全部数值为在案钉或批二十九实测转录；零工时/速率估计。
4. 只交付不入库：零 git；本件唯一新建。

—— QF-OS 联邦批三十 S6 kernel 试点备产席 · 2026-10-27 · 只交付不 commit
