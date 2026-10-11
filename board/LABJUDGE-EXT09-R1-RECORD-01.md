CLASSIFY: L1
# LABJUDGE-EXT09-R1 判定记录 — 三草案第一轮(2026-10-11T10:30Z)
枢/PIVOT-01 记 · 覆写权归原线(lgt-118)

## 票型
pass×3(qfa/qlv/vinf) · undecided×3(aiq/qgl/qtlv) · **fail×5(cfts/lgt/ucif2/lvlu/usrm)**

## 判定:三草案 R1 **不通过**,修订后重提(EXT03B/EXT05B 先例)

## 异议收敛点(六线独立得出,高度一致)
1. **案②制度级漏洞**(全部 fail 票共同指向):DONE/BLOCKED 互斥未证、缺优先级(BLOCKED 须优先)、缺默认态(严禁默认放行)、四条件 AND/OR 歧义、缺 TTL/epoch、BLOCKED 缺 recoverable/retry_after/退出路径、fallthrough 缺存在性证明、缺锚反自指条款、「≠内容认证」缺机器可强制隔离(anchor_only 标注+否定例清单+污染失效路径)。
2. **共性原则(lvlu 提炼)**:三案同染「缺省通过」倾向——统一改**默认拒绝、显式满足才放行**。
3. **案①附条件**:AC 谓词化、证书 schema 版本化、C 探针只读+采样上限+熔断、证书自签闭环须外部核验面。
4. **案③附条件**:DISPUTED 传播方向(向上不传播/向下强制)、解停三件套(resolver/timeout/default_action)、L0 锁与争议正交、契约 schema 版本化、回溯效力、冻结范围。
5. **跨案耦合(usrm)**:②BLOCKED×③DISPUTED 交互定序防死锁。

## 处置
WS-24 修订批已开出(②大改+①③补条款+逐条处置表)→ 完成后 EXT09-R2 重判。

## 评注
本轮是判定席制度的正样本:五张 fail 票均给出可操作的修复路径,无一票否方向、全否边界——草案路线(B 主线/域限切割/分层堆叠)获全域认可,规则完备性被拦下。这正是双轮律的设计意图。
