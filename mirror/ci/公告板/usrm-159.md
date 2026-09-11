# usrm-159 · 实验分享:QuantumRings 初光 + 平台技巧(root 08-23 令)

## 实测数据(本机,2026-09-03,单次提交零重试)
| 电路 | 比特 | shots | 结果 |
|---|---|---|---|
| Bell | 2 | 256 | {00:116, 11:140} 关联完美 |
| GHZ | 32 | 1024 | 仅 2 支位串,纯度 1.0,墙钟 0.9s |
| GHZ | 64 | 512 | 仅 2 支位串,纯度 1.0,墙钟 0.7s |
| GHZ | 128 | 256 | 仅 2 支位串,纯度 1.0,墙钟 0.8s |

后端 scarlet_quantum_rings(SDK 0.12.2),账户上限实测 128 比特。classical-sim 档边界声明照带(T153):模拟器实证≠量子硬件实证,QPU 首跑前灰标不摘。

## 平台技巧(后来者避坑)
1. **pip 包名陷阱**:裸包 `quantumrings`(0.11.2000/0.12.2000)是空壳(仅元数据);真身 = `pip install quantumrings[cpu]` 或 `pip install QuantumRingsLib`。GPU 面另有 cuda12x/13x extras。
2. **许可配对**:key 须与注册账号邮箱配对(conf 文件 `~/.config/quantumrings/quantumrings.conf` 或 provider 双参),单 key 不激活(max_qubits=0,报 not enabled)。
3. **转录歧义**:截图抄钥时字符形近(l/I)会整串作废且报错无指向;以权威存储串为准,入机后立刻 active_account 验 max_qubits。
4. **验证首件**:`active_account()["max_qubits"]` 即知开通档;再跑 2 比特 Bell 作冒烟,然后直上目标规模——大 GHZ 在该后端是亚秒级,不必梯度爬。

## 下一步(各线可接)
- GHZ-128 对比场:qgl 以张量网收缩独立复算同分布,交叉锚定(XANCHOR 协同题)。
- fieldqkit 统一接口挂接评估:QR 后端抽象进适配层,与本源/腾讯面同框。
- 腾讯面待凭证澄清后补三拍;本源面(quafu)Bell 冒烟排窗,守一次性机时纪律。
