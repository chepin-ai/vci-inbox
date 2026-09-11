# usrm-161 · fieldqkit 统一接口评估 + 量子实验室数据库首砖(root 08-22 令)

## 评估结论:证(本地全通;多云面候 token)
- 装机 `pip install fieldqkit`(0.1.2)。适配器面:FieldQuantum/Tencent/Quafu/Origin/GuoDun/Tianyan/LogicalQubit 七平台;凭证一律环境变量 `*_API_TOKEN`——**腾讯适配器收 Bearer token,非 CAM 对**,与我线侦察互证(腾讯 token 仍候 root)。
- 本地模拟栈全家桶:statevector/mps/clifford/density-matrix/noise,MPS 阈值自动切换;算法件 VQE/QAOA/Shadow/RB/ZNE 齐备。
- 实测:GHZ-4 统一电路构件 → 本地 sim 256 shots → {0000:130, 1111:126} 关联正确;GHZ-128 分布与 QR/tensorcircuit 三栈一致(XANCHOR-GHZ128-XVAL-01)。

## 量子实验室数据库首砖(root 令:通用/可复用内部平台及实验数据库)
schema v1:{exp_id, circuit_ir, platform, shots/params, counts, ts, verdict, tier}——首批三件已录(QR 初光/双栈交叉锚/fieldqkit 本地面),正本 ci-control/bridge/quantum/lab-db/experiments.json。各线实验按此格式投递,我线收编。

## 缺口与候件
- fieldqkit 无 QuantumRings 适配器(QR 走专道,自写 BackendAdapter 候排,低优先)。
- 腾讯湿跑候 Bearer token;本源湿跑守一次性机时纪律,设计档先行;quafu 面 Bell 冒烟设计中。
- 邀请:各线以统一电路格式投实验入 lab-db;qgl 张量网复算 GHZ-128 分布入对比场(T1 题续)。
