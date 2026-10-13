# CLASSIFY: L1
# KI-EXT11-1 · WS-63 ζ 见证链 known-issue 登记（枢线 PIVOT-01，2026-10-13）

## 登记事项
WS-63 核验器 Backlund 交叉核验门（backlund_N_equals_winding）**结构性不健全**：
围道盒包络以盒中心多边形辐角累加估绕数，未将各盒辐角张角余量计入包络宽。

## 实测证据
- T=100 围道 232 盒，张角总量 Σw=171.95 rad（measure_backlund.py 实测）
- N_B 区间化复算 = [29.09812430226496, 29.09812430426496] —— 区间内无唯一整数，
  fail-closed 拒证成立（诚实仲裁证据保留，不调参逼 PASS）
- 存在性层（29 组 IVT 括号端点包络）完全区间健全，不受本项影响

## 裁决（P4 律 · 不升格）
- 存在性 = WIT-W1 PASS（计算层区间见证）
- iso100 完备性层降格「数值演示级」；iso1000 完备性维持 BLOCKED(B1) time-box 诚实登记
- 每证书逐字披露：「区间见证层 PASS、kernel 层未证、非 RH 证据」「有限高度 T=100/1000 截断」
- 严禁「RH 已证/已验证到 T」（C3′ 律）

## 后续挂号
- OBL-EXT11-a：绕数严格化（盒级 argwidth 余量入包络，或改指数和/quadrature 路线）

## 附：FINDING-20261013-01 关联
本 KI 首版随 ~/ws63-hub 环境重置损毁（未入库），本版为重建版；
定理面内容与原案一致（补丁谱系与实测数据均有多重留痕）。

## 枢线修补登记（hub 接管 WS-63 尾段，覆写权归原线——修补限测试/驱动层，核判据未动）
- #1-#2 g_trunc/trunc_residual 残差包络：iv 有理除法外向舍入天然包络（替代 mp.nextafter 过渡案）
- #3 verify _check_common + 测试×3：canonical_sha256 剥 witness_sha256 自字段
- #4 verify c_low 门：精确有理比较（Fraction ≥ 1/5）
- #5 测试钉档本 KI：iso100 预期 FAIL 且败因恰为 Backlund
- #6-#12 测试层 drift 修复（schema 签名/紧度界含 θ 余项内禀宽/FE 盒改包含断言/
  _certify_bracket 四元组/篡改测试改路径+ok=False/full_verify 返回结构/CLI --json 列表）
