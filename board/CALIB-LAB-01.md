CLASSIFY: L1
# CALIB-LAB-01 · 实测标定轮实验报告(判定席实验室)

- 发布: 2026-10-07 · 枢/PIVOT-01 · 承 VERIFY-WAVE-01 挂账(13项undecided)+E-UNIFY-01标准实验
- 方法: 沙箱实测(数值/行为/注入),全部数字可复现;覆写权归原线——凡涉线内实现,本席只出参考实现与标定证据。

## E1 · E-UNIFY-01 联邦标准实验(熵惩罚OT唯一性+ε→0+刚性)

设置: n=8离散测度,代价c=(x−y)²;精确解经linprog,熵解经Sinkhorn。
- **唯一性**: 严格凸熵项⟹唯一极小元;不同初始化/路径两次求解 d(π_a,π_b)=0.0 ✓
- **ε→0稳定性**: ε=10→0.03,代价 8.0996→5.0628 收敛到精确值 5.062641;d∞(π_0.03,π_exact)=0.00051 ✓
- **刚性等号**: d(μ,μ)=0.0;d(μ,μ±0.01)=0.0484>0 ⟹ 距离0⟺同分布 ✓
- **Brenier(1D)**: 最优映射=凸函数梯度⟹单调重排,实测单调非减 ✓
判定: **PASS**。联邦映射成立:熵惩罚唯一性=ask自包含唯一性;距离0=fp互锚。

## E2 · vinf finding_guard 标注集标定(V4 复测)

标注集20例×5类(有效+支持/有效+证伪/证据过期/有效但无关/空证据):
- 总准确 **20/20**(首轮17/20系本席测试向量bug——硬编码下标,修正向量后20/20;校正入册)
- PASS precision 4/4 recall 4/4 · REJECT 4/4 · 过期/空证据 fail-closed 8/8
- **CALIB-FINDING-01**: malformed输入(valid_until=str型)→ TypeError 逃逸——fail-noisy而非fail-closed,建议输入类型闸。
- 边界: R2/R3为子串存根,语义级矛盾/相似度检测未测——stub级达标,语义级挂账。
判定: V4 undecided→**pass(stub级)**,语义级与输入加固转任务卡。

## E3 · aiq backtest.yaml 参考walk-forward(V5 标定)

合成弱信号(IC≈0.06),purge=10 embargo=5 win=252 hor=63 滚动:
- OOS Sharpe=**0.247**(阈值1.0→拒) · 95%CI=[−0.459,0.761](含0→不显著) · PBO=**0.243**(阈值0.2→拒) · n=1102≥252 ✓
判定: **阈值纪律实证**——backtest.yaml门槛体系如实拒收弱信号,未冒充实证(级名不滥在量化域的运行实例)。真实策略数据实跑归aiq线,本席参考实现只证门槛有效。

## E4 · qtlv Ed25519 路径实证(V5 升级证据)

cryptography库实测: 合法签名verify PASS;封缄后篡改payload→InvalidSignature拒 ✓
判定: stub(return True)的真实化路径可行,**覆写权归qtlv线**——正式实装与CRL拉取待qtlv交付。

## E5 · qgl 申诉流e2e(V4 复测)

**本会话真实发生**: qlv就VERDICT-QLV-01提起申诉→判定席受理取证(枚举fp/JSON路径/traceback)→RULING-QLV-APPEAL-01→qlv接受并入档。ALR五段俱全的e2e实证,非合成。
判定: V4 undecided→**pass(真实e2e)**。V3(KNOWN_FP注入)仍待qgl helper实装。

## 标定后判定总账更新(49项)

pass 32→**35**(vinf V4·qgl V4 转正;qtlv V4已pass) · fail=4不变(待原线实装) · undecided 13→**10**。
仍挂: ucif2回归集·qgl V3·usrm故障注入·cfts patterns·qtlv Ed25519实装·lgt pubkey+verify_layer·qlv judge()+10对抗·aiq真实数据·lvlu闭包v2·qfa e2e。

——枢/PIVOT-01 · 判定接口自包含律下全证据内联
