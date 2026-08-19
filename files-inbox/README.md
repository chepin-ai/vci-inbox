# files-inbox · 快门投递口（vci-inbox 公仓，事件驱动秒级摆渡）

## 门规（硬）
- **快门只收 L0/L1**：PATS 密钥闸命中或 `CLASSIFY: L2` 头标件一律拒收——隔离至 ci-logs（私仓 quarantine/），大厅 #144 回执（dtag: files-ingest-fast）。
- **零私域留存**：快门只路由不留存——L0/L1 件路由入 ci-library 后即删（git 历史残留属 L0/L1 可接受，如实声明此限；私域件一律不得走本口）。
- **私密件两条路**：ci-inbox 慢门（私仓轮询，实测中位 ~10min）或 fed-relay 加密道（见下）。
- 路径规约：`files-inbox/{线名}/{相对路径}`，线名∈{ucif2,vinf,qgl,usrm,cfts,onto,gcml,cisvr}，单件 ≤256KB，UTF-8 文本。

## fed-relay 加密道（增密级，ENVELOPE-01 K2）
- 投递者取 pk（本仓 `bridge 镜像见 ci-control/bridge/fed-relay-pk.json`）做 SealedBox 加密 → base64 文本 → 投 `files-inbox-enc/{线名}/{名}.enc`。
- 快门**原样转密文**入 ci-library `lines/{线名}/_enc/`（零知识摆渡——本仓全程只见密文）；sweeper（ci-control 持 sk）收割时解密 → 落正规目标（注册私仓 archive/ 或 ci-library lines/）+ 台账链 + 谱系行。

## 纠缠停（vci↔ci-inbox）v1（K3）
- 每跑先验锚：App 读 ci-inbox `bridge/head-anchor.json`（本侧头 sha 滚链），自洽性+连续性双验；
- 锚不可读或指纹异常（断链/不自洽=外来干扰迹象）→ 立即置 `weave/HALTED` 停执行，经 ci-control 通道（bridge/fastdoor-halt.json）+ 大厅帖（dtag: fastdoor-halt）告警；排除干扰后人工撤旗复跑。
- **wci 延伸**：暖侧读面已够（T2W 只读锚面可照此验），写面待 root 投放——规约同上，激活凭 root 令。
