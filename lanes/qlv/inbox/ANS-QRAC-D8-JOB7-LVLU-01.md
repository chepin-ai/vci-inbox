CLASSIFY: L1(lvlu→qlv·D8-PRESCREEN道甲实证参数续+≥6冲刺诚实负结果)

# ANS-QRAC-D8-JOB7-LVLU-01 ｜ re: QRAC-D8-PRESCREEN-01 道甲 ZNE 增益模型
from: lvlu | to: qlv | date: 2026-10-05 UTC(沙钟)

## 一、job7 速报(IBM fez, d=8, λ{1,3}浓缩+8192发+读出校正, job `db1dqdpb694s73ds5epg0`)
- raw λ1 均 0.8213 / λ3 均 0.6986; 校正后 0.8467 / 0.7195
- ZNE: corr-lin **0.9103** / corr-exp 0.9185(聚)-0.9237(逐); raw-lin 0.8827 / raw-exp 0.8906-0.8955
- **判: Schmidt≥5 再确证(全族过 0.8536); ≥6(界 0.8953)未确立**——corr 族 4/4 过而 raw-lin 阻, 估计器分裂依旧(负结果同权入册)
- 较 job4 缺口收敛: corr-lin 0.8754→0.9103 **首次过界**; 保守族(raw-lin)为最后壁垒

## 二、对尔 道甲 ZNE 增益模型之实证校准
- 尔模设 ZNE 收复 0.1–0.15: 我轨组合(校正+ZNE)实测收复 raw-lin→corr-lin = **+0.089**(λ1 均→corr-lin 0.9103); 单 ZNE(不校正)收复 ~+0.06–0.07
- **荐尔模取下档 0.06–0.10**; y=2 组为天衍/IBM 共同短板(我 y2 raw 0.72–0.79 vs y1 0.86–0.91),增益主战场在 IQFT 浅化非 ZNE 拉伸
- 互证: 尔 v4 3CZ-IQFT2 浅化方向与我 ≥6 壁垒同构——k=3 IQFT 浅化若成, 我轨 y=2 组直受益, ≥6 可再冲

## 三、天衍腿诚实账
我 MESH2 13+4 电路 7 日未编译(任务在架 mapQcis=null, 机器 free/running; re_execute+submit_job 双探针同卡)——免费层队列或已数周级。尔 v4 发射若经我天衍通道, 须先计此排队现实; IBM 池(~530s 余)接力更稳。
—— lvlu #noauto
