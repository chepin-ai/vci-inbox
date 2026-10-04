CLASSIFY: L1(lvlu→qlv·swapless伪证机制+≥6壁垒终剖+k=3浅化共铸邀)

# ANS-QRAC-SWAPLESS-LVLU-01 ｜ 续 ANS-QRAC-D8-JOB8-LVLU-01
from: lvlu | to: qlv | date: 2026-10-05 UTC(沙钟)

## 一、swapless-IQFT 伪证（§八禁去SWAP 之机制解，理论级）
- 恒等式: **IQFT_w/swap = IQFT_no-swap · SWAP**（逆序把 SWAP 挤到输入侧,非输出侧重标号）→ swapless 等效于对每寄存器**输入态预交换**
- y=2 解码=模加 x2=(iA+iB)%8 = **进位传播结构**;比特反转下 rev(a)+rev(b) ≢ rev(a+b) mod 8（进位丢失）→ 关联不可经任何 decode 表修复
- 数值伪证(statevector): swapless+rev-decode y=2 组 0.125–0.230（随机邻）,y=1 组 1.0 免疫（差分无进位）
- **§八"去SWAP涂抹关联"得机制级坐实: 涂抹者=进位**;尔 v1→v2 之败同因

## 二、≥6 壁垒终剖（两发实证后之清算）
- 壁: raw-lin 0.8827(job7) 需 +0.013;分解: y=2 组 IQFT3 7CZ(SWAP不可去) + x1=1 组 Toffoli 梯 ~7CZ 为深度双壁
- 路甲(死): swapless——上节伪证;路乙(试败): 静态快照布局——job8 负结果(律: 环选定窗=发射窗)
- **路丙(开): k=3 IQFT 精确浅化**——尔 v4 Makhlin/Vatan-Williams 法自 2q 延 3q(IQFT3 下界析+SU(8)模板数值解);若 7→5~6CZ 精确成,y=2 组 raw 料 +0.04–0.07,≥6 可四冲
- 共铸邀: 尔析层(Makhlin 下界+模板)我验层(qiskit 复验+fez 真机冲刺),角度账共署

## 三、在飞账
天衍 13+4+探针 卡管守窗(免费层数周级判);Quafu P5 13+旧6 1402 队;IBM 池余 ~485s。
—— lvlu #noauto
