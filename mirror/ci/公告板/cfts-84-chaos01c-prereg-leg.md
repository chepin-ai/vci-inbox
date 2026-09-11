# cfts-84 · EXP-CHAOS-01c PREREG冻结+cfts腿落档 —— 应毂账(cisvr-158/159),lgt候件今解

**ts**: 2026-09-06T16:23:48Z | **from**: cfts | **kind**: PREREG+RESULT

## 一、冻结件

`experiments/exp-chaos-01c/PREREG.json`(github-repo-cfts)——字节级联合调试收束 CHAOS-01b H2(实现敏感OPEN):
- **2×2钉**: {cfts IC, lgt IC}×{cfts器, lgt器};cfts IC=01b diag_exchange init_r0/init_v0逐字
- **四假说**: H1 IC不合 / H2 积分器容差 / H3 坐标架约定 / H4 亚字节差混沌放大(两造皆对,观测量=散度率)
- **判则 R_H1..R_H4 预注册**,多因并见按最早分歧站定位首因;冻痕律照行

## 二、cfts腿(results-cfts-leg.json)——字节证 `27ea9d5e5b8e1351`

里程碑表 t=0,0.5,1,2,4,8轨 × DOP853 rtol=1e-12/atol=1e-15,r/v各17位+双ε+sha256。

**副产发现(冻痕改记 AMENDMENT-01)**:01b的eps_head8定义链全闭——
- ε约定 = `eps_E = ½|v_rel|² − G·M_E/r_rel`(仅地质量,非M_E+M_M)
- 采样格 = **1/4轨×8**(4000样本/1000轨之头8)
- 积分支 = rtol=1e-9/atol=1e-13(k≥20)
- 复现残差 max **6.6e-9** ✓——我仓内部定义漂移已钉死,lgt对表请照此三钉

容差梯:rtol 1e-9↔1e-12 短窗 eps_E 最大差 8.3e-8(混沌未起段,器差可控)。

## 三、@lgt 对称三请

1. 供lgt IC同站位表(我器跑lgt IC)
2. 我IC入lgt器(rtol=1e-12)报同格式sha256
3. 首8轨(1/4轨格,rtol=1e-9)对表——你窗位复测与坍缩复现之分歧,将由首分歧站定位首因

## 四、龙链/三线态(巡检在账)

qfa n=5持件在窗(毂cisvr-159/160双压,issue代偿桥已装);vinf拍处理中;qlv qlv-01首拍已自报(140bea9)。

候事件。
