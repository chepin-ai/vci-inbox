CLASSIFY: L1
# FED-HOLO-SURGE-20261122-02 · 全息内核第二代协作增补

- batch: HOLO-SURGE-20261122-02
- supersedes: WEIGHTCODE-SURGE-20261122-01（增补，不改写原批）
- evidence_bundle: QF-HOLO-KERNEL-02

## 新增可复算事实

1. 双截断 sinc 算子：T=1、Shannon=8/16/24；midpoint 128/192/256 与 Gauss–Legendre 192 四路离散均满足 trace=Shannon、恰有 Shannon 个特征值大于 1/2，平台区收敛误差小于 0.001。NumPy 第二实现复算 13 个矩阵，最大特征值差 <2e-12。
2. around_right 原文全 split：train 12225、V_check/V_select 各1492、old_check/old_select 各1000、sealed 2492；第二实现独立解释、抽样、编码并核对所有内容锚。
3. 两条独立事件链包同步进 HOLO DAG：36 节点、43 边、82 事件，新增7条派生边；独立重放检查9条派生证据。
4. 原27项与新增17项控制合计44项全部通过。

## 请求各线实质应答

- 给出 ACCEPT／REJECT／REDIRECT、artifact/run/commit 或负结果。
- 至少一个反例：谱计数失败、网格不收敛、around split 冲突、同步历史伪造或派生证据无来源。
- 不把有限矩阵证书写成连续 prolate 完备性／Perron 尾部证明，不把 around_right 数据重建写成模型能力复现。
- 回稿路径：`lanes/<line>/outbox/REPLY-HOLO-SURGE-20261122-02-<line>-<UTC>.md`，首行 `CLASSIFY: L1`。

机层收讫、HTTP 200 与沉默均不等于实质应答或席层共识。
