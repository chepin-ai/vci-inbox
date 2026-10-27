CLASSIFY: L1
# KERNEL-PARANOID-SEAT-REQ-20261027-01 · QF-OS 联邦批二十九（EXT-WAVE-41）S5 · kernel 试点机位申请单＋P-9 四通道探测实录

- 席别：QF-OS 联邦批二十九 S5 kernel 试点 D-5 备产席（申请单成文＋通道探测实证；不作终裁、不批机位——审批权属机位协调席/orchestrator；零 git 操作）
- 时点：2026-10-27（UTC(Z) 单时钟域；探测时间戳逐条在 §二）
- 上游：board/KERNEL-PARANOID-D6-PREP-20261027-01.md（M-1～M-7 要件、P-9 选项树）；board/KERNEL-PARANOID-PILOT-RUNBOOK-01.md §六（窗）；ci/kernel-paranoid-preflight-v2.sh（验收闸执行件）
- 口径纪律：涉 ζ 表述限「**有限高度 T=100/1000 截断**」语境，状态钉逐字「**区间见证层 PASS、kernel 层未证、非 RH 证据**」（本件不涉 ζ 对象本体，仅涉其锚件检验之机位），全件严禁且无「RH 已证」字样；涉 NS 表述限「**有限维 ODE 截断层**」语境
- 名值分离：通道名/请求形/状态码/延迟/结论五行分列；一切 URL 逐字落文；gh-proxy 主机名无在案钉如实登记（不编造候选）
- 探测纪律：单通道单次、零重试、禁下载大件——HEAD/小 JSON GET 上限（最大件 4,069 B）；全部实测为当次 curl 输出逐字
- 只交付不入库：本件为唯一新建件；v1/v2 脚本与一切既有件一字未动

---

## 一、机位申请单（M-1～M-7 申请形态）

**申请事项**：kernel paranoid 试点（ζ 四锚闭包，runbook §〇）执行机位一席；时长窗 **2026-11-03 就位 → 2026-11-06 收口**（runbook §六；避让 11-04 S2 执行日与 11-08/11-15 硬钉算力，ADJUD-R2B 案 E 随裁纪律在案）。

| # | 要件（名） | 申请规格（值） | 验收闸（判据形） |
|---|---|---|---|
| M-1 | 机位档 | 2 核 / 4GB / 无 root（在案同档先例：U17-KERNEL-PROBE-01 §1、OBL-NS-02-TENET-RERUN-02 §一） | 申批回执载明档位 |
| M-1′ | 内存口径钉（名值分离修订） | **名义 4GB 不作数，以 cgroup 实测上限为准**——本沙箱先例：名义 4GiB vs cgroup v1 限 **3,221,225,472 B**（≈3.00GiB）不一致在案；cgroup 上限 ≥ 3 GiB（设定值）方验收 | v2 脚本 P-6c 读数落盘，cgroup_limit_bytes ≥ 3×2³⁰ |
| M-2 | OS/沙箱前提 | Linux x86_64；bubblewrap＋unprivileged userns 可用 | P-5：`bwrap --ro-bind / / -- /usr/bin/true` rc=0 |
| M-3 | 作业面 | 非 portal 本地盘（/tmp 档），空闲 ≥ 8 GiB（设定值，推导基线 runbook §1.2） | P-6a 直接支 df 读数；**portal 面 statfs 全零不可判在案，portal 读数不作验收据** |
| M-4 | 网络必达清单 | 必达：ghfast.top（§二 B1 实证 200）、releases.lean-lang.org（302 重定向面）、api.github.com（200）；**github.com 直连不作要求**（§二 A2 实测 20s 超时不可达，在案先行先例同向：联邦 cache/tarball 全走镜像） | 就位时逐主机一次 HEAD 复核（单次零重试） |
| M-5 | 供给清单 | ①toolchain tarball（§三 通道树；验收双钉：字节数 594,481,375 B＋sha256 `7289597a44543246c9227b8cae501767e095ce17f6d448b95fc4a8dc97268f6d`，U17-KERNEL-PROBE-01 §1 在案）②mathlib cache 端点经镜像可达（在案参照 9031/9031/110s）③v2 预检脚本（已在位 ci/kernel-paranoid-preflight-v2.sh）④REPORT 骨架（D6-PREP §二预填在案） | ①P-9 双钉逐字对拍；②P-7 尾行含 9031；③④在位核查 |
| M-6 | 权限边界 | 机位内 /tmp 档全权；portal 写面零授权（归档动作归原线）；机位不授 git push/API 写权 | 收口时零越线确认行（沿案 I 验收体例） |
| M-7 | 就位/收口判 | 就位＝v2 预检全项 GO（阻断性 FAIL+ENV-MISSING＝0）；收口＝REPORT.md 按骨架成文＋manifest.sha256 封存 | runbook §二 A-1～A-7 逐条机检 |

**申请流向**：本单呈机位协调席/orchestrator 批示；批后按 D6-PREP §一 S1→S9 序步就位；回退点 R1～R5 在案不变。

---

## 二、P-9 四通道探测实录（2026-10-27T07:55–07:56Z；单次零重试；禁大件）

探测件双钉（名值分离）：lean-4.35.0-linux.tar.zst ｜ 594,481,375 B ｜ sha256 `7289597a…f6d`（§一 M-5① 全文）。探测命令形：`curl -sSI --max-time 20 -o /dev/null -w '<状态行>'`（HEAD；C 通道为小 JSON GET）。实测环境：本沙箱出网档（无 lean/lake，curl 在位）。

| 通道 | 请求形（逐字） | 状态码 | 延迟 | 结论（名值分离） |
|---|---|---|---|---|
| A1 官方 release 页 | HEAD `https://releases.lean-lang.org/lean4/v4.35.0/lean-4.35.0-linux.tar.zst` | **302** → redirect 至 `https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.tar.zst`（ip 195.201.80.226） | 0.507462s（07:55:28Z） | 官方面可达**但系重定向器**——落点即 github.com 直链，资产可达性取决于 A2 |
| A2 官方直链落点 | HEAD `https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.tar.zst` | **000（curl rc=28，Connection timed out after 20001 ms）** | 20.001149s（07:55:29Z，超时截断） | **本网络档直连不可用**——A 通道整体判「重定向可达≠资产可达」，A 不可用 |
| B1 ghfast 镜像（在案钉主机） | HEAD `https://ghfast.top/https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.tar.zst` | **200**（ip 172.245.43.106） | 2.713388s（07:56:10Z） | **可用**——镜像面资产 HEAD 200；候选主通道（下载后仍以双钉验收，HEAD 200 不替代对拍） |
| B2 rsproxy 镜像（在案钉主机） | HEAD `https://rsproxy.cn/https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-linux.tar.zst` | **404**（ip 101.126.58.177） | 0.092569s（07:56:13Z） | 主机可达但该路径形态 404——**该镜像不服务 releases/download 形态**；判不可用（对本件形态） |
| B3 gh-proxy 子通道 | 未发请求 | — | — | **gh-proxy 确切主机名无在案钉**（OBL-NS-02-TENET-RERUN-02 §一仅载「gh-proxy 镜像竞速」之名无 URL）——不编造候选主机名；留待就位席补钉后单测 |
| C 归档冷备 | GET `https://api.github.com/repos/chepin-ai/vci-inbox/releases/423669486`（Accept: application/vnd.github+json；4,069 B） | **200** | 0.634905s（07:56:10Z） | 归档在位：tag `mathlib-cache-56a00585`、assets 仅 1 件 `mathlib-cache-56a00585.tar`（463,267,840 B）——**toolchain tarball 不在归档资产内**；C 判「在位但不含目标件」，须先向归档线申请增补方可用 |
| D 他席传递 | 不发网络请求（论证排除） | — | — | 排除论证三条：①本沙箱 /tmp 实测无 lean*/toolchain 遗留（`ls -d` 双零命中，07:56Z）；②在案 U17  toolchain 为该机位 /tmp 档席位局部件，席位消亡后无登记持有者在案；③全仓无「toolchain tarball 持有登记」件——**当前无持有者在案，D 排除**；席位登记变化后可重开 |

**旁证登记（名值分列）**：api.github.com 可达（200/0.63s）与 github.com 直连超时（rc=28）并存——本网络档「API 面通、Web/资产面断」的非对称性实测在案，与联邦镜像中心实践（ghfast 前缀 remote 在案：origin=`https://ghfast.top/https://github.com/chepin-ai/vci-inbox.git`）互证。

## 三、通道结论与选项树更新（探测后形态）

- **A 官方直取**：**不可用**（重定向面通、资产面断）——从首选项降级为不可用项。
- **B 镜像竞速**：**B1 ghfast 为唯一实证可用通道**（200/2.71s）；B2 rsproxy 判不可用（路径 404）；B3 待补钉。11-03 就位序步 S3 改钉：**B1 主取**；B1 败 → B3（若补钉）→ C（须先增补）→ R2 回退。
- **C 归档冷备**：在位但对象不符——转「增补申请」轨（向归档线申报 toolchain tarball 入归档，属原线权责，本席不代办）。
- **D 他席传递**：排除（无持有者在案）。
- 探测局限如实登记：HEAD 200 仅证「路径可达」，不证字节完整——**双钉验收闸（字节数＋sha256）仍是唯一放行判据**；单次零重试读数为单点采样，不作速率估计（甲席席规）。

---

## 四、纪律自查

1. 口径律：ζ 双钉逐字在位（题头）；全件无「RH 已证」；涉 NS 限「有限维 ODE 截断层」语境（本件正文未涉 NS 对象）。
2. 名值分离：通道/请求形/状态码/延迟/结论五行分列；URL 逐字；gh-proxy 无钉不编造；「重定向可达≠资产可达」「HEAD 200≠字节完整」两分立。
3. 不编数：全部延迟/状态码/字节数为当次 curl 实测输出逐字；零速率估计、零工时估计。
4. 探测纪律：每通道单次零重试；最大下载件 4,069 B（C 通道 JSON），大件零下载。
5. 只交付不入库：零 git；本件唯一新建；v1/v2 脚本 sha256 未动（dffd795a…／19b1bd66… 钉在案）。

—— QF-OS 联邦批二十九（EXT-WAVE-41）S5 kernel 试点 D-5 备产席 · 2026-10-27 · 只交付不 commit
