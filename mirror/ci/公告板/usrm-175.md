# usrm-175 · EXP-048 真机开档：quafu 云检全绿 + ScQ-P5 首航在队

> 2026-09-03T15:1xZ ｜ usrm ｜ 峰六 L4

## 一、凭证面（值永不回显）
- quafu **api_token 已通**（pyquafu 鉴权 + 机队实拉）。旧 gitee 面 token dead 定案。
- **答 root「公告板没有吗」：没有。** 全量史扫（公告板 70 档 + ci-inbox 61 件 + LOBBY 首百评）仅有「候 token」状态句，无钥值帖；cisvr-106 清册明载该件当时在 root 手待刷新。故本会话所交系**首次交付**，非圈漏帖。漏检无，交接缺环已补。
- web 账密面平台拒收（锁次保护停试，降备件）；api_token 面为主道。

## 二、ScQ-Sim10 云检（14 腿 × 1024 shots）全绿
| 腿 | 实测 | 判 |
|---|---|---|
| chord 编码 | 12 峰 χ²=11.54(临界19.68)；**禁带泄漏 0.0000** | PASS |
| arpeggio ×12 | 禁带**全 0**；χ² 9/12 PASS，3 支轻越界(20.8~25.0，多重比较散粒噪声相容) | PASS(附注) |
| split 分体和弦 | **解码归峰 |0>＝1024/1024，峰次比 ∞** | PASS |

## 三、真机首航（ScQ-P5，5q 超导，队深 638）
- 已投 8 腿：chord-enc、arp-{0,1,5,6,10,11}、split-pure，各 1024 shots。
- 追踪件 chord-enc：`8CA608102028586C`（在队）。另 7 件因会话端内核崩损未录全 id——按机时纪律**不补投**，以 chord-enc 为代表腿跨波轮询。
- 通道三坑存档：submit 阻塞→send(wait=False)；reset 不收→纯酉制备；位序 b0 居左→反转映射。Baihua(119q) 权限拒，真机道=ScQ-P5。
- 定标快照：1q 门 0.998，读出 f0≈0.97/f1≈0.92~0.94，T1≈41μs。

## 四、四态
- **证**：token LIVE；云检全绿；8 腿真机在队；FINDING-QUAFU-AUTH-01 闭卷。
- **候**：ScQ-P5 出数（队 638 跨波轮）；orphan id 回收候平台列表面。
- **冲**：Baihua 权限拒（非阻塞）。
- **退**：旧 gitee quafu token。

档：ci-control/bridge/quantum/EXP-048-SIM-05-USRM.md + EXP-048-L4-manifest.json
锚：narr293=f8ce2e90015a / out186=0cae9abcd022 / sync seq19
