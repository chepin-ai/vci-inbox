CLASSIFY: L1
# LORENZ96-M0-CONSTANTS-v0 — Lorenz-96 批准线 M0 首件 T1：五源一手复核定式表 v0

- 波次/线：EXT-WAVE-18 续执行批 R1 执行席 · 枢/PIVOT-01 体系 · LORENZ96-LINE-CHARTER-01 §2.1 M0 / §五 T1
- 日期钉：2026-10-28（截止钉同；UTC(Z) 单时钟域；现状类断言均带「截至」钉）
- 交付口径：五源一手复核（标准形 / F 参数区 / Hopf 阈 / 周期窗 / 吸收球先验逐项来源钉）；每项给文献原句（英文逐字 + 页/式号）+ 中文转述 + 一手复核状态（官源/镜像/未核）；禁凭记忆填参数
- 复核状态机：`官源核`（出版方/主办方域一手全文）｜`镜像核`（作者预印本/机构库/出版版 PDF 镜像全文，书目经多源+DOI 解析交叉实证）｜`未核+补证路径`
- 语纪律：C1–C3 + C1′–C3′ 有效；严禁「NS 已解决」；本表数值阈为**文献钉**（transcribed→verified），不构成本线自证；周期窗/混沌结论一律引文献、不外推为吸引子刻画

---

## 一、五源书目钉（DOI/出处逐项实证，截至 2026-10-28）

| # | 源 | 出处钉（一手复核结论） | DOI 解析实证（curl -I doi.org，302 Location） | 复核渠道 | 状态 |
|---|---|---|---|---|---|
| S1 | Lorenz 1996 | E. N. Lorenz, "Predictability: a problem partly solved", *Proc. Seminar on Predictability*, Vol. 1, pp. 1–18, ECMWF, Reading, UK, 1996（ECMWF elibrary 条目 75462 载「Seminar on Predictability, 4-8 September 1995, Shinfield Park, Reading」，会议 1995-09、刊本 1996，两形态均实证；另有 2006 剑桥重刊本 Lorenz 2006a, chap. 3, pp. 40–58，非本表钉） | 无 DOI（会议论文集）；官源 URL：`ecmwf.int/en/elibrary/75462-predictability-problem-partly-solved`，扫描版 PDF 实测 18 页、HTTP 200、SHA-256 `de698ddb991e4bdaec6ceabf15323deb97139917418aefd221be7e40a860d0f3`（/tmp 实测） | ECMWF 官域扫描 PDF 全文逐页目验 | **官源核** |
| S2 | van Kekem & Sterk 2018 | D. L. van Kekem & A. E. Sterk, "Travelling waves and their bifurcations in the Lorenz-96 model", *Physica D: Nonlinear Phenomena* **367** (2018), pp. 38–60, DOI `10.1016/j.physd.2017.11.008` | `→ linkinghub.elsevier.com/retrieve/pii/S0167278917301094`（实证通） | 作者接受稿 arXiv:1704.05442（ar5iv HTML + arXiv PDF 全文逐节核；arXiv 页自标 "Published in Physica D, doi:10.1016/j.physd.2017.11.008"）；刊名卷页经 ≥4 个独立引用页交叉一致 | **镜像核**（Elsevier 正文页未直连；接受稿=刊本内容，页码以刊本钉） |
| S3 | van Kekem & Sterk 2019 | D. L. van Kekem & A. E. Sterk, "Symmetries in the Lorenz-96 model", *International Journal of Bifurcation and Chaos* **29**(1) (2019), 1950008, DOI `10.1142/S0218127419500081` | `→ worldscientific.com/doi/abs/10.1142/S0218127419500081`（实证通） | 作者接受稿 arXiv:1712.05730 v3（ar5iv HTML 全文逐节核）；刊名卷期文号经 ≥3 个独立引用页交叉一致 | **镜像核**（World Scientific 正文页未直连） |
| S4 | Sterk & van Kekem 2017 | A. E. Sterk & D. L. van Kekem, "Predictability of Extreme Waves in the Lorenz-96 Model Near Intermittency and Quasi-Periodicity", *Complexity* **2017** (2017), Article ID 9419024, DOI `10.1155/2017/9419024` | `→ hindawi.com/journals/complexity/2017/9419024/`（实证通；现由 Wiley 托管） | 出版方 OA 全文（onlinelibrary.wiley.com/doi/10.1155/2017/9419024）逐节直读 | **官源核** |
| S5 | Karimi & Paul 2010 | A. Karimi & M. R. Paul, "Extensive chaos in the Lorenz-96 model", *Chaos* **20**(4) (2010), 043105, DOI `10.1063/1.3496397`（PubMed PMID 21198075 交叉一致） | `→ pubs.aip.org/cha/article/20/4/043105/152017/...`（实证通；pubs.aip.org 正文页直连失败=内部错误） | 作者预印本 arXiv:0906.3496 v2（2010-03-29，HTML 全文逐节核）+ VTechWorks 机构库存出版版 PDF（`vtechworks.lib.vt.edu/.../1.3496397.pdf`）+ PubMed 摘要页 | **镜像核**（AIP 正文页未直连；出版版 PDF 镜像+预印本双证） |

---

## 二、定式表（逐项：出处钉 → 复核结论）

### 2.1 标准形（循环指标）

**定式**：dx_j/dt = (x_{j+1} − x_{j−2})·x_{j−1} − x_j + F，j = 1,…,N，下标 mod N（x_{j±N} = x_j）；要求 N ≥ 4（N ≤ 3 无趣味动力学）。

| 源 | 文献原句（英文逐字 + 页/式号） | 中文转述 | 状态 |
|---|---|---|---|
| S1 | "It contains the *K* variables *X*₁, …, *X_K*, and is governed by the *K* equations d*X_k*/d*t* = −*X*_{k−2}*X*_{k−1} + *X*_{k−1}*X*_{k+1} − *X_k* + *F*, (1) where the constant *F* is independent of *k*. The definition of *X_k* is to be extended to all values of *k* by letting *X*_{k−K} and *X*_{k+K} equal *X_k* … We assume that *K* > 3; the equations are of little interest otherwise."（ECMWF 刊本 p. 4，式(1)；p. 5 首段） | 模型源文献式(1)：−X_{k−2}X_{k−1} + X_{k−1}X_{k+1} − X_k + F，与 (x_{k+1}−x_{k−2})x_{k−1} − x_k + F 代数恒等；循环延拓 X_{k±K}=X_k；K>3 为文内假设 | 官源核 |
| S2 | "The so-called monoscale Lorenz-96 model is defined by the equations ẋ_j = x_{j−1}(x_{j+1} − x_{j−2}) − x_j + F, j = 1,…,n, (1a) where we take the indices modulo n by the following 'boundary condition' x_{j−n} = x_{j+n} = x_j, (1b)"（刊本 p. 38 §1.1，式(1a)(1b)） | 现代记号标准形，单尺度、单参数 F、循环边界 | 镜像核 |
| S3 | 同式(1a)(1b)逐字重刊："ẋ_j = x_{j−1}(x_{j+1} − x_{j−2}) − x_j + F, j = 1,…,n, (1a) and a 'boundary condition' x_{j−n} = x_{j+n} = x_j. (1b)"（刊本 §1.1，式(1a)(1b)） | 同 S2，系列续篇一致 | 镜像核 |
| S4 | "The dynamical equations are [式(6)，同标准形] with the periodic 'boundary condition' x_{i+n} = x_i. The dimension n and forcing F are free parameters."（出版方页 §3.1，式(6)；网页排版式(6)图像未转录，上下文逐字如上） | 同标准形；n、F 为自由参数 | 官源核 |
| S5 | "The two parameters N and F completely determine the dynamics. … We explore system sizes N ≥ 4 since N = 3 does not yield interesting dynamics due to the nature of the coupling."（刊本 §II；切线方程式(4) 显示向量场结构与标准形一致） | N ≥ 4 工作区间；式(4) 切线方程证实其模型方程即标准形 | 镜像核 |

**N=36、F=8 典范参数区出处**：S1 一手钉——"Figures 1 and 2a have been constructed with *K* = 36, so that each sector covers 10 degrees of longitude, while *F* = 8.0."（p. 5）；"For *K* = 36 and *F* = 8.0, for example, λ₁ corresponds to a doubling time of 2.1 days; if *F* is raised to 10.0, the time drops to 1.5 days."（p. 5）。另 p. 5："we assume that this scaling makes the time unit equal to 5 days"（时间单位=5 天）。S2 Table 1（刊本 p. 39）综述印证："Almost all values are chosen in the chaotic domain (F = 8) of dimension n = 36 or 40."——**典范参数 (N,F) = (36, 8) 源自 Lorenz 1996 原文，非二手转引**。

### 2.2 F 参数区（F 档 × 动力学相态对照）

| F 档 | 相态 | 出处钉（原句 + 位置） | 状态 |
|---|---|---|---|
| F ≤ 0 侧 | F < 0 存在超临界 pitchfork（偶数维 F_{PF,1} = −1/2；n=4k 时第二叉 F_{PF,2} = −3），随后超临界 Hopf | S3："the trivial equilibrium x_F exhibits a supercritical pitchfork bifurcation at the parameter value F_{PF,1} := −1/2"（Thm 4）；"both equilibria … exhibit a supercritical pitchfork bifurcation at the parameter value F_{PF,2} := −3"（Thm 9） | 镜像核 |
| 小 F > 0 | 全解收敛于齐次平衡 x* = F·𝟙 | S1："For very small values of F, all solutions decay to the steady solution X₁ = … = X_K = F"（p. 5）；S5 转述钉："For small values of the forcing F < 8/9 it has been shown that all solutions decay to the steady solution X_k = F."（§II） | 官源核（S1）/镜像核（S5） |
| F 中等 | 周期（行波） | S1："when F is somewhat larger, most solutions are periodic"（p. 5）；S2：F=1.2 周期吸引子=行波（§1.2 + Fig. 2） | 官源核/镜像核 |
| 更大 F | 混沌（onset 依赖 N） | S1："but for still larger values of F (dependent on K) chaos ensues"（p. 5）；S2："for all dimensions shown, except for n = 4, chaos sets in for F ∈ (3, 7)"（刊本 §3 引言段） | 官源核/镜像核 |
| F = 5 | 「小强迫」：周期/混沌窗交替；混沌窗平均广延 | S5：§III.1.1 标题 "Small External Forcing, F = 5"；"As the system size is increased for small values of the forcing we find dynamical states that alternate between periodic and chaotic dynamics. The windows of chaos are extensive, on average, with relative deviations from extensivity on the order of 20%."（摘要） | 镜像核 |
| F = 8 | 典范混沌（N=36） | S1 p. 5（见 §2.1）；S2 Table 1（chaotic domain F=8, n=36/40） | 官源核/镜像核 |
| F = 10 | 「中等强迫」：过临界 N 后全尺寸混沌；D_λ 广延 | S5：§III.1.2 标题 "Intermediate External Forcing, F = 10"；"For intermediate values of the forcing we find chaotic dynamics for all system sizes past a critical value."（摘要）；S1：F=10 时误差倍增时间 1.5 天（p. 5） | 镜像核/官源核 |
| F ∈ [5, 30] | 强驱动扫描：维数密度 δ_λ = D_λ/N 单调增并饱和于 δ_∞ < 1（ξ_δ = δ_∞^{−1} ≈ 1.08，F→∞ 极限） | S5："We studied 6 values of the forcing over the range 5 ≤ F ≤ 30 … for 5 different system sizes where 15 ≤ N ≤ 35"（§III.2）；"Using our results for δ_∞ yields a value of ξ_δ = 1.08 for the chaotic length in the limit of infinite forcing."（§III.2） | 镜像核 |
| F = 11.83/11.85/11.9 等（n=4） | 周期吸引子 → 鞍结消失 → I 型间歇混沌（详见 §2.4） | S2 §3.1 / S4 §3.2 | 镜像核/官源核 |
| F = −100（n=4，历史档） | 混沌吸引子（Lorenz 1984 研究） | S3 引言："in [Lorenz84a] the chaotic attractor is studied for F = −100" | 镜像核 |

### 2.3 Hopf 阈（平衡态 x* = F·𝟙 失稳临界 F）

**定式**：唯一齐次平衡 x* = (F,…,F)；Jacobian 为循环矩阵，特征值解析式 λ_j(F,n) = −1 + F·f(j,n) + F·g(j,n)i，其中 f(j,n) = cos(2πj/n) − cos(4πj/n)；第 l 对复共轭特征值横越虚轴于 **F_H(l,n) = 1/f(l,n)**。F > 0 首次失稳指标 l₁(n) = arg max_{0<l<n/3} f(l,n)，满足 n/6 ≤ l₁(n) ≤ n/4（n=7 例外取 l₁=1）；**首 Hopf 恒为超临界**，F_H 值域 (8/9, 1.19)，n→∞ 时 F_H → 8/9。**阈依赖 N**（经 l₁(n) 与 f(l,n)），非普适常数。

| 源 | 文献原句（英文逐字 + 位置） | 中文转述 | 状态 |
|---|---|---|---|
| S2 | "The l-th eigenvalue pair {λ_l, λ_{n−l}}(F,n) of the trivial equilibrium x_F of system (1) crosses the imaginary axis transversally at the parameter value F_H(l,n) := 1/f(l,n) and thus the equilibrium changes stability."（Lemma 1，刊本 §2.2）；"For F > 0 we prove that the first Hopf bifurcation takes place for F ∈ (8/9, 1.19) and is always supercritical. The periodic attractor born at this bifurcation has the physical interpretation of a travelling wave."（§1.2 结果要点第二条）；"the F_H-value of the first of these bifurcations converges to 8/9 as n → ∞"（§1.2 末段） | 阈公式 F_H = 1/f(l,n)；正 F 首 Hopf ∈ (8/9, 1.19)、恒超临界、极限 8/9；所产周期轨道即行波 | 镜像核 |
| S2 | "In particular, if the first bifurcation is a Hopf bifurcation, then this bifurcation is supercritical."（Proposition 5 末句）；l₁(n) 界定同 Proposition 5 | 首分岔若为 Hopf 则必超临界；l₁(n) ∈ [n/6, n/4] | 镜像核 |
| S3 | "For odd n, no pitchfork bifurcation will occur, but the first bifurcation of the trivial equilibrium (6) for F < 0 is a Hopf bifurcation at F_H(j,n) := 1/(cos 2πj/n − cos 4πj/n) with j = (n−1)/2."（§3.1 Case 1）；正 F 侧："This bifurcation happens at F_H(l₁,n) := 1/(cos 2πl₁/n − cos 4πl₁/n), where l₁ denotes the index of the first eigenpair crossing the imaginary axis"（§3.1 「Positive F」段） | F<0 奇数维首分岔亦为 Hopf（阈公式同形）；正 F 阈公式与 S2 一致互证 | 镜像核 |
| S4 | "For all n ≥ 4 this equilibrium becomes unstable through either a supercritical Hopf or a double-Hopf bifurcation for 8/9 < F < 3/2 [36]."（§3.1）；n=4："The equilibrium x_F = (F,F,F,F) becomes unstable at F = 1 through a supercritical Hopf bifurcation."（§3.2）；n=7："becomes unstable at F ≈ 1.182 through a supercritical Hopf bifurcation"（§3.3）；n=24："becomes unstable at F ≈ 0.889 through a supercritical Hopf bifurcation"（§3.4） | n≥4 首失稳为超临界 Hopf 或双 Hopf；具体维数阈：F_H(1,4)=1、F_H(1,7)≈1.182、F_H(5,24)≈0.889——与阈公式自算值 1.00000/1.18202/0.88901 全合 | 官源核 |
| S5 | "For small values of the forcing F < 8/9 it has been shown that all solutions decay to the steady solution X_k = F."（§II） | 下界 8/9 的独立转述印证 | 镜像核 |

**关键数值（自算，公式钉 S2 Lemma 1 + 式(3)(4)，非文献印刷值，状态=导出自算）**：n=36 时 l₁(36) = 8，f(8,36) = cos(80°) − cos(160°) = 1.113341，**F_H(8,36) = 0.89820**（立案书转录值 0.8982 复核**成立**）；n=4：F_H(1,4) = 1；n=7：1.18202；n=24：0.88901。自算环境：Python 3.12 + numpy，本批 /tmp 实跑。

### 2.4 周期窗（周期轨道窗口 / 行波锁相已知结论）

| 对象 | 结论钉（原句 + 位置） | 中文转述 | 状态 |
|---|---|---|---|
| n=4 周期窗与鞍结 | S2："The original periodic orbit disappears through a fold bifurcation at F_SN ≈ 11.83823. Chaos is observed for parameter values F ≥ 11.84. Figure 7 compares the periodic attractor for F = 11.83 with the chaotic attractor for F = 11.9 … This is the classical type 1 intermittency scenario"（刊本 §3.1）；S4："at F_SN ≈ 11.8382, it disappears through a saddle-node bifurcation and a chaotic attractor is detected"（§3.2），且 "The periodic attractor remains stable until F ≈ 5.06 where it exchanges stability with another periodic attractor. However, at F ≈ 8.93 the original periodic attractor gains stability again."（§3.2） | n=4：Hopf@F=1 后周期吸引子存续至 F≈5.06（与另一周期轨道交换稳定性）、F≈8.93 复稳，至 F_SN≈11.8382(3) 鞍结（fold/saddle-node）消失；F≥11.84 呈 I 型间歇混沌。立案书「F_LPC ≈ 11.8382」复核：文献术语为 fold/saddle-node（周期轨道鞍结），数值 11.8382/11.83823 成立 | 镜像核（S2）/官源核（S4） |
| n=4 混沌区内周期窗 | S4："The behaviour is rather stable with F with the exception of F = 12.1 in which case a stable periodic attractor appears amidst the chaotic regime."（§3.2，Table 1 上下文）；另 "the presence of narrow windows with periodic dynamics"（§3.2 Fig. 5 上下文） | F=12.1 附近存在混沌区内的稳定周期窗 | 官源核 |
| n=7 准周期链 | S4："becomes unstable at F ≈ 1.182 through a supercritical Hopf … remains stable until F ≈ 2.717 where it bifurcates through a Neĭmark-Sacker bifurcation. The resulting 2-torus attractor remains stable until F ≈ 4.272 where it disappears through a quasi-periodic saddle-node bifurcation"（§3.3） | 周期→2-环面→准周期鞍结→间歇混沌 | 官源核 |
| n=24 准周期链 | S4："becomes unstable at F ≈ 0.889 … until F ≈ 3.639 where it bifurcates through a Neĭmark-Sacker … a 3-torus attractor appears [F ≈ 3.791] … disappears at F ≈ 3.831 and a chaotic attractor is detected"（§3.4） | 周期→2-环面→3-环面→混沌（Ruelle–Takens 型链） | 官源核 |
| 行波锁相/周期轨道对称 | S3：F<0 侧周期轨道 γ_n-共轭（Case 1/2/3，§3.1）；正 F 侧猜想："when the spatial wave number l of a periodic orbit P(t) and the dimension n satisfy gcd(l,n) = g > 1, then P(t) ∈ Fix(G_n^{n/g}), i.e. the periodic orbit generated through the first Hopf bifurcation is symmetric."（§3.1，标为 conjecture）；行波周期公式 T = 2π tan(πl/n)（S2 式(8)），极限 T_∞ ≈ 4.867（S2 Proposition 6） | 周期轨道波数-维数锁相条件（猜想级，注意分级）；行波周期解析式 | 镜像核 |
| F=5 周期/混沌窗（N 方向） | S5：F=5 时随 N 增大 "dynamical states that alternate between periodic and chaotic dynamics"，周期窗平均间隔 ξ_p = 5.25（§III.1.1） | 尺寸方向的周期窗交替（Karimi & Paul 专属结论） | 镜像核 |

### 2.5 吸收球先验（能量法 ⟪B x x, x⟫ = 0 → limsup‖x‖ ≤ F√N）

**定式**：二次非线性项在能量内积下对角相消（循环和恒等式 Σ_j x_j·x_{j−1}(x_{j+1}−x_{j−2}) = 0），故 dE/dt = −‖x‖² + F·Σ_j x_j ≤ −‖x‖² + √N·|F|·‖x‖（Cauchy–Schwarz），即 dV/dt ≤ −V + √N|F|（V = ‖x‖，G=0 时 λ^A_max = −1），任何半径 r > **R = √N·|F|** 的球均为捕获区（trapping region），从而 limsup‖x‖ ≤ F√N（F > 0）。**与我方 GalerkinNS 接口点**：该对角相消即 `⟪B x x, x⟫ = 0`（hskew 对角层），为 M1 裁定「A 为主」的能量不等式继承的文献支点。

| 源 | 文献原句（英文逐字 + 位置） | 中文转述 | 状态 |
|---|---|---|---|
| S1 | "The physics of the atmosphere is present only to the extent that there are external forcing and internal dissipation, simulated by the constant and linear terms, while the quadratic terms, simulating advection, together conserve the total energy (X₁² + … + X_K²)/2."（p. 5） | 二次项（平流）保持总能量——能量守恒结构的最原初一手陈述 | 官源核 |
| S2 | "The Lorenz-96 model is constructed such that the quadratic part does not affect the total energy of the system, E = ½ Σ_j x_j². This property implies the existence of a trapping region in all dimensions [Lorenz84a]."（刊本 §2.1）；Proposition 7（Trapping Region，§2.4.1）及其证明（接受稿 pp. 47–48，式(38)）："dE/dt = V·dV/dt = Σ x_j ẋ_j = ⟨x, Ax⟩ + F Σ_j x_j … The second term of equation (38) can be estimated by the Cauchy-Schwarz inequality … dV/dt ≤ λ^A_max V + √n|F| … It follows that dV/dt < 0, whenever G > −1/4 and whenever V is larger than the radius R(n) = √n|F| / (−λ^A_max). Therefore, under these conditions, each sphere with radius r > R(n) is a trapping region for dimension n. **In particular, if G = 0 then R = √n|F|.**" | 能量导数中二次项消失（式(38) 逐行：非线性项对能量贡献为零）；Cauchy–Schwarz 得 √n|F| 项；G=0（原模型）时 λ^A_max = −1，故捕获球半径 R = √n·|F|——吸收球先验 limsup‖x‖ ≤ F√N 的文献一手出处钉齐 | 镜像核 |
| S3 | 未含吸收球推导（对称/分岔主题）；其式(7) 与 S2 式(3) 特征值式互证 | —（本项无新增钉） | 镜像核 |
| S4 | 未含吸收球推导（极值可预测性主题） | —（本项无新增钉） | 官源核 |
| S5 | 未含吸收球推导（维数广延性主题） | —（本项无新增钉） | 镜像核 |

**关键数值（自算）**：典范参数 (N, F) = (36, 8) ⇒ 吸收球半径 R = 8·√36 = **48**（公式钉 S2 Prop 7 证明，状态=导出自算）。

---

## 三、复核方法注记

1. **渠道纪律**：逐源「web 搜索 → 出版方/主办方页 → DOI 解析（curl -I doi.org，302 Location 实证）→ 全文一手核读」。S1/S4 达成官源全文直读（ECMWF 扫描 PDF 18 页逐页目验；Wiley/Hindawi OA 全文）；S2/S3/S5 出版方正文页未直连，改以作者 arXiv 接受稿/预印本 + 机构库出版版 PDF（S5：VTechWorks 存 DOI 命名出版版 `1.3496397.pdf`）镜像核，书目要素（刊名/卷/页/文号/年）另经 ≥3 个独立引用页交叉一致，DOI 302 目标域与刊方一致。
2. **S1 出处形态核实结论**：原刊为 ECMWF Seminar on Predictability（会议 1995-09-04–08，Shinfield Park, Reading）论文集 Vol. 1, pp. 1–18，刊本 1996；elibrary 条目 75462 的「Date Published 1995」指会议年，引用形态以 "Proc. Seminar on Predictability 1:1–18, ECMWF, 1996" 为准（与立案书钉一致）；2006 剑桥重刊本（Palmer & Hagedorn 编 *Predictability of Weather and Climate*, chap. 3, pp. 40–58）为同文重刊，非本表钉。
3. **自算项标注**：F_H(8,36) = 0.89820 与 R = 48 两值非文献印刷值，系由一手钉公式（S2 Lemma 1 / Prop 7 证明）本批实算导出，状态记「导出自算」，底稿可复跑（公式与输入全钉于 §2.3/§2.5）。
4. **扫描件转录风险**：S1 为图像扫描 PDF，原句经逐页目验转录（关键页 p. 4 式(1)、p. 5 参数段）；如有疑义可复核 ECMWF 官源 PDF（SHA-256 钉于 §一 S1 行）。
5. **立案书转录复核汇总**：S2/S3/S4/S5 的刊名卷页 DOI 全部复核**成立**；「n=36、l=8 时 F_H ≈ 0.8982」复核**成立**（导出自算 + S4 n=24/n=7 印刷值侧证公式链）；「F_LPC ≈ 11.8382」数值成立，但文献术语为 fold/saddle-node（非 LPC 命名），钉文已按文献原术语改写并注明。

## 四、未核项清单（未定 + 理由）

| # | 条目 | 状态 | 补证路径 |
|---|---|---|---|
| U1 | S2/S3 刊本页码内的式号-页码映射（本表式号依接受稿/刊本节号，页码钉至刊本起始页 38–60 / 文号 1950008） | 未定：镜像核已闭合内容钉，刊本内页级映射未逐页比勘 | Elsevier ScienceDirect S0167278917301094 / World Scientific 正文页可直连窗口补页级对照 |
| U2 | S5 刊本排版与预印本/机构库 PDF 的逐段 diff | 未定：内容钉已三证一致（arXiv v2 + VTechWorks 出版版 + PubMed 摘要），未做全文 diff | pubs.aip.org 正文页恢复后抽样比勘 |
| U3 | S4 式(6)（模型方程）的数学排版逐字符（出版方网页该式为图像/MathJax 未文本化） | 未定：上下文与切线结构印证即标准形，式(6) 本体未逐字符转录 | Hindawi/Wiley PDF 版下载页补式(6) 逐字符 |

## 五、语纪律自检（本文件行文）

本表为文献定式钉（M0 来源钉），全部数值阈标文献出处与复核状态，未做、也不构成本线任何区间见证/捕获盒/吸引子刻画的自证声明；本线后续见证声明沿用语言钉「区间见证层 PASS、kernel 层未证」按对象适配；严禁语「NS 已解决」未出现；未复核条目以「未定+理由」列于 §四，未预填任何哈希/刊本内页码。NS 包档位、Fefferman A/B、Clay NS **未解决、未颁奖**口径不动。
