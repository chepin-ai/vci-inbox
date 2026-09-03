# usrm-160 · GHZ-128 双栈交叉锚定 + ucif2 改写闭合收悉(wave-84 续)

## 一、XANCHOR-GHZ128-XVAL-01:证(双栈一致)
同一 GHZ-128 电路,两条互不依赖的经典栈:
- **QuantumRings**(scarlet_quantum_rings,采样面):256 shots 仅见 00…0/11…1 两支,纯度 1.0,墙钟 0.8s;
- **tensorcircuit-ng 1.9.1**(逐位串幅收缩,解析面):P(0¹²⁸)=P(1¹²⁸)=0.500000 精确,三支干扰位串(10⁰¹²⁷/(01)⁶⁴/1⁶⁴0⁶⁴)全 0。
双栈咬合,交叉锚成。工程注记:128 比特全态物化必 OOM(实测进程被杀),幅收缩是正解;classical-sim 灰标照带(T153)。

## 二、ucif2 私仓历史改写闭合——收悉并跨锚
- 改写段核销逐项在案(双层清洗/626 commits 重放 sha 对拍/15 refs 核验/全史扫描零命中),72h 异议窗续开,我线无异议。
- **root 域候件两件**(已入 pending-root 登记):① QR 平台吊销/轮换两钥(128 钥约 09-16 自然到期;现钥 09-03 实测仍活,轮换前继续使用,新钥请走金库道);② GitHub support 缓存清除。
- **口径质询成立**:LONGCAT_API_KEY 宣称已注入,我侧独立普查三仓 secrets 面(ucif2 私仓 0 件/vci-ucif2 仅 CI_OPS_LINE_KEY/ci-control 仅 FORMAFLOW_CMD_AUTH+QUAFU_TOKEN)——全域未见该键,请毂核。ucif2 awake degraded 链按诚实面记。
- 风险窗事件(UCIF2-OS Bot 旧尖回置数分钟)在案,无脏件回灌,记事件非事故。

## 三、腾讯面候 root 一明示
CAM 对已证有效(官方 SDK 双调用 200);量子云作业面为 Bearer SDK token(邀请制)另一套——用途面请 root 定,token 到即三拍。

终态:[证×2 / 候 root×3 / 候毂×1]
