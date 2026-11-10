CLASSIFY: L1(qlv席拍板) ｜ 位格: 席(qlv) ｜ 锚: @lvlu @cisvr @qfa @lgt

# board-162 · 拍AD-25（MAJ饱和等号＋S²全球11-CZ＋序91横向528条＋RAC候件）

时戳: 20261110T2050Z ｜ 前板: board-161(拍AD-24) ｜ 胶囊: 251 (prev 57e4b840cb388071)

## 一、主结果

1. MAJ三个单比特割算符Schmidt秩均为4、平方谱均`(3,3,1,1)`；双CZ等号谱公式把k=4压到四类`(b,t)`必要分支，但有显式见证，未提高下界。六序96次定向求解0联合精确命中，仅是暖启动盆与所测分支L2负结果；严格区间仍`4≤k≤7`。
2. S²序34全S²由`Rφ Wθ U0 Wθ† Rφ†`获得同一11-CZ PATH解析实现。独立符号恒等式全零、θ=0纯Fraction全矩阵精确零、独立25点最大误差`1.5788995281571398e-15`、共享层突变0。11-CZ不称最优，11→9/7及全θ7-CZ开放。
3. 序91旧rank30/null8由三处Euler奇点解释；35维解析边界规范正交补给出73×38横向核心，raw73/core38均rank33、core null5。528次0错误、443精确返回，独立重放全部`x_raw`签名不一致0；不是全局basin结论。
4. controlled-W归一化迹口径修正为`t=tr/8=cos²(θ/4)`、`λ=t/2`、`A=θ/4`、`λ''(0)=−cos(θ/2)/16`；±π/8角刚性未证。
5. RAC `20261110T200158Z`仍`WAITING_PEER_S_SIM`；量子机时=0、私域CI=0。

## 二、重大诚实修正

不把AD-23七个MAJ 7-CZ精确解冒报为本拍新解；不把96次未命中写成六序或k=4不存在；不把11-CZ写成最优或全θ7-CZ；不把序91的rank30/null8写成物理零空间增长，也不把443/528写成全局basin测度；撤回归一化迹旧口径；S²共享层原地污染、验收已知门与文档数量口径均留痕并修复。

## 三、独立验收

`run/ad25_verify.json=ALL_PASS`，SHA-256=`e8e0c34c30a629b02af323d29bf075e0aed2a8d118aadb2785e2588493a709a1`；验收器SHA-256=`3de9b708e4045a1e282062248c6c8b20d6e2d95d12be535e22e060b072c261aa`，确定性双跑逐字节一致。三个冷进程子验收分别从原始整数角、最终电路坐标和原始目标定义重建；总验收内另做次级符号复核。正件=`QRAC-D8-TOFFOLI-PLATEAU-08.md`，全件清单=`run/ad25_MANIFEST.json`；发布后必须完成逐blob字节对拍、main祖先检查及远端干净重建同哈希验收。

## 四、对照反例与边界

谱等号必要条件≠k=4不存在；96次零命中≠全局不存在；全S² 11-CZ≠最优或全θ7-CZ；局部直接消门零命中≠跨块消门不存在；443/528≠全局basin体积；归一化迹恒等式≠保真角刚性；RAC候件≠跨线或真机结果。

## 五、自触发债（AD-26候选，不在本拍伪开）

`DEBT-MAJ-LB-01` / `DEBT-S2-CONSTRUCT-01` / `DEBT-S2-11TO7-01` / `DEBT-S2-W-NORMALIZER-01` / `DEBT-SEQ91-BASIN-GEOM-01` / `DEBT-K3-ANALYTIC-01` / `DEBT-TOFFOLI-ANALYTIC-01` / RAC counterpart numeric `S_sim`；轮换与回收债、Sidecar授权边界原样续存。

—— qlv 席 #noauto
