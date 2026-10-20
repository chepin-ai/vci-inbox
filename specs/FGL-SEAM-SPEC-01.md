CLASSIFY: L1
# FGL-SEAM-SPEC-01 · FluidGalerkinLean 净室功能规格（Reader 轨产出）

## 0. 规格头

- **对象**：wwang-math/FluidGalerkinLean @ `4d023ac47aea65a4a5dbbc20004f5fda0ee18755`（tag `arxiv-v1`）。客观定性：Weinan Wang 单人 + LLM 辅助、约 10 天开发、零 sorry、无许可证（licenseInfo=null，默认保留全部权利）。
- **取材日期**：2026-10-21。
- **Reader 席署名**：QF-OS 联邦 EXT-WAVE-18「攻」WS-E 攻坚线 Reader 轨执行席（枢/PIVOT-01 体系）。
- **用途**：供 Writer 轨独立实现 2D 周期 Galerkin → Leray–Hopf 弱解接缝。Writer 仅依据本文件工作，不得打开 FGL 仓库。
- **引用惯例**：方括号内为来源元数据（FGL 文件路径或论文章节号，视同文献引用）；本文不出现 FGL 的任何 Lean 代码、声明名、tactic 结构。论文 arXiv:2609.33033 的数学陈述为公开学术内容，可引用。

### 红线合规自查表（CLEANROOM-REDLINE-FGL-01 逐条）

| # | 红线 | 自查 |
|---|---|---|
| 1 | 禁逐行搬译；规格只含数学内容 | ✓ 全文仅数学定义/命题/证明素描，无任何 FGL 源码转写 |
| 2 | 规格中不得出现 FGL 的 Lean 代码、标识符、证明 tactic 结构；文件路径仅作来源元数据 | ✓ 已逐段检查，标识符零出现；路径仅见于方括号来源标注 |
| 3 | 禁镜像比对 | ✓ 本次工作未打开任何我方实现文件做对照，接口注记只述数学需求 |
| 4 | 摘要隔离复核（自查：每段可被「只读规格、从未见过 FGL」的 Writer 理解为数学需求） | ✓ 已通读自查一轮，凡依赖 FGL 特定形式化选择的表述均改写为数学需求语言 |

---

## 1. 单元①：有限维 Galerkin 逼近的存在性、能量等式与极限通过（Leray–Hopf 接缝）

**数学目标**：对任意发散自由初值与任意有限时域，构造有限维 Galerkin 逼近列，证明其精确能量等式与一致先验界，并提取子列使弱形式方程逐项通过极限，得到 Leray–Hopf 弱解（能量空间时间平方可积、状态路径弱连续、满足能量不等式与时间测试弱方程）。

### 1.1 涉及定义（数学记号）

- **抽象 Galerkin 系统**：实 Hilbert 空间 $(H,\langle\cdot,\cdot\rangle)$ 上的一对算子：有界自伴非负线性算子 $\mathcal A:H\to H$（扩散，$\langle \mathcal A u,v\rangle=\langle u,\mathcal A v\rangle$ 且 $\langle \mathcal A u,u\rangle\ge 0$）与有界双线性算子 $\mathcal B:H\times H\to H$（对流），满足**能量抵消** $\langle \mathcal B(u,u),u\rangle=0$。[来源：PDEIdeas/GalerkinSystem.lean]
- **斜对称强于抵消**：若三线性型 $b(u,v,w):=\langle \mathcal B(u,v),w\rangle$ 满足 $b(u,v,w)=-b(u,w,v)$（后两变元反对称），则 $b(u,u,u)=0$。这是流体经典恒等式 $\langle (u\cdot\nabla)u,u\rangle=0$ 的抽象形式。[来源：PDEIdeas/GalerkinSystem.lean]
- **有限维变分 Galerkin 系统**：有限维内积空间 $W$ 上的双线性扩散型 $d:W\times W\to\mathbb R$ 与三线性对流型 $c:W\times W\times W\to\mathbb R$，配显式常数 $C_b\ge 0$ 满足 $\|c(u,v,\cdot)\|_{W'}\le C_b\|u\|\,\|v\|$；假设 $d(u,u)\ge 0$（仅逐点非负，不要求强制性）与 $c(u,v,w)=-c(u,w,v)$。[来源：PDEIdeas/VariationalGalerkin.lean]
- **变分 Galerkin 问题**：上述系统 + 时间依赖对偶外力 $F:\mathbb R\to W'$（连续）+ 初值 $u_0\in W$。[来源：PDEIdeas/VariationalGalerkin.lean]
- **Riesz 组装的右端向量场**：定义 $r(t,u)\in W$ 为泛函 $v\mapsto -d(u,v)-c(u,u,v)+F(t)v$ 的 Riesz 表示元。意义：把「无界算子」层面的方程化为系数 ODE，全程只需弱型，不需要把 Stokes 算子当作能量空间上的有界算子。[来源：PDEIdeas/VariationalGalerkin.lean 模块头]
- **Galerkin 投影**：$H$ 的有限维子空间 $W$ 与投影 $P:H\to H$，$P|_W=\mathrm{id}$；正交投影时，投影方程经 $W$ 中向量测试后投影自动消去。[来源：PDEIdeas/GalerkinProjection.lean]
- **Leray–Hopf 弱解（有限时域 $[0,T]$）**：三元组（能量路径 $\tilde u\in L^2(0,T;V)$、状态路径 $u:[0,T]\to H$、相容性 $u(t)=J\tilde u(t)$ a.e.），满足：(i) 对每个 $y\in H$，$t\mapsto\langle u(t),y\rangle$ 连续（弱连续）；(ii) $u(0)=u_0$；(iii) 能量不等式 $\|u(t)\|^2+2\int_0^t\|\nabla \tilde u(s)\|^2\,ds\le\|u_0\|^2$（受迫情形右端加外力功项）；(iv) 时间测试弱方程（见 1.2 命题 P9）。[来源：PDEIdeas/OpenDomainLerayHopfStatement.lean；arXiv:2609.33033]

### 1.2 关键命题（数学陈述）

- **P1（右端估计）**：$\|r(t,u)\|\le \|d\|\,\|u\|+C_b\|u\|^2+\|F(t)\|_{W'}$；且在半径 $R$ 球上 $u\mapsto r(t,u)$ 为 Lipschitz，常数 $L(R)=\|d\|+2C_bR$（关于 $t$ 一致）。[来源：PDEIdeas/VariationalGalerkin.lean]
- **P2（局部存在）**：对任意初值，存在正时长上的唯一局部解（Picard–Lindelöf 定理的直接实例化；连续性由 $F$ 连续与 $r$ 的显式依赖给出）。[来源：PDEIdeas/VariationalGalerkin.lean]
- **P3（能量等式，Galerkin 层精确成立）**：任意局部解 $u$ 在 $[a,b]$ 上满足
$$\|u(b)\|^2+2\int_a^b d(u(s),u(s))\,ds=\|u(a)\|^2+2\int_a^b F(s)(u(s))\,ds.$$
关键点：只有限制到有限维空间上的弱型参与计算，对流项因斜对称严格抵消（等式而非不等式）。[来源：PDEIdeas/VariationalGalerkin.lean]
- **P4（先验界）**：若有强制性 $\nu\|u\|^2\le d(u,u)$（$\nu>0$），则由 P3 + 逐点 Young 不等式 $2\langle F,u\rangle\le \nu^{-1}\|F\|^2+\nu\|u\|^2$ + 标量吸收引理得
$$\|u(T)\|^2\le \|u_0\|^2+\nu^{-1}\int_0^T\|F(s)\|^2\,ds;$$
保留一份耗散的加强形式：$\|u(T)\|^2+\int_0^T d(u,u)\,ds\le \|u_0\|^2+\nu^{-1}\int_0^T\|F\|^2\,ds$。[来源：PDEIdeas/GalerkinCore.lean, GalerkinPointwiseYoung.lean, GalerkinIntegralEstimates.lean, GalerkinScalarAbsorption.lean]
- **P5（能量预算内的全局延拓）**：设解被控制在半径 $R$ 球内，外力对偶范数有连续上界 $M$。取统一步长 $\delta=1/(C+1)$，其中 $C=\|d\|(R+1)+C_b(R+1)^2+M$（保证 $C\delta\le 1$），则从球内任意状态出发的局部解都有公共正存活时间 $\delta$；邻接解在接点等值则可拼接；对「可达终点集」取上确界并反证，可得任意预定终点 $T$ 上的解。[来源：PDEIdeas/VariationalGalerkin.lean]
- **P6（受迫吸收的强制性替代）**：无强制性时，若底空间有 Poincaré 型不等式 $\|Ju\|_H\le C_P\|\nabla u\|$，则任意能量对偶外力可被扩散型吸收：$|F(t)(u)|\le \tfrac12 d(u,u)+\text{（与 }u\text{ 无关的余项）}$，从而 P4/P5 的机制对任意连续对偶外力仍成立。[来源：PDEIdeas/BoxPoincare.lean, BoxForcedSpectralGalerkin.lean]
- **P7（强 $L^2_tH$ 紧性——「有限模等度连续 + 谱尾」替代 Aubin–Lions）**：设 $V\overset{J}{\hookrightarrow}H$ 为紧嵌入，$\{u_m\}$ 为 Galerkin 逼近列（$u_m$ 取值于前 $m$ 个谱模式张成的子空间），满足一致能量界与对偶范数意义下的时间导数一致界。则：(a) 每个固定有限模族有等度连续性，由 Arzelà–Ascoli 紧；(b) 谱尾投影的算子范数随模数趋于 $0$（紧嵌入的直接推论）；(c) 故原序列被「逐模数紧的逼近族」一致逼近，其值域全有界（totally bounded），从而 $L^2(0,T;H)$ 中存在强收敛子列。[来源：PDEIdeas/GalerkinL2Compactness.lean, GalerkinStrongCompactness.lean]
- **P8（强-弱同步抽取）**：在 P7 的强子列基础上，$L^2(0,T;V)$（可分 Hilbert）中有界序列有弱收敛子列；再取一次子列可得同一子列同时强收敛于 $L^2(0,T;H)$、弱收敛于 $L^2(0,T;V)$，且两个极限由嵌入 $J$（及其时空提升的伴随）识别为同一条时空轨迹。[来源：PDEIdeas/LeraySpectralWeakCompactness.lean, BoxLerayWeakCompactness.lean]
- **P9（时间测试弱方程及其极限通过）**：Galerkin 层对任意标量测试 $\eta\in C^1([0,T])$（$\eta(T)=0$）与空间测试 $\varphi\in V$ 成立精确方程
$$-\int_0^T\langle u_m,\varphi\rangle\,\eta'\,ds+\int_0^T d(u_m,\varphi)\,\eta\,ds+\int_0^T c(u_m,u_m,\varphi)\,\eta\,ds=\langle u_m(0),\varphi\rangle\,\eta(0)+\int_0^T F(s)(\varphi)\,\eta\,ds.$$
极限通过：(i) 时间导数项与扩散项由强 $L^2_tH$ + 弱 $L^2_tV$ 直接通过；(ii) **对流项（2D 特异）**由单元②的 Ladyzhenskaya 通道把强 $L^2_tH$ + 有界 $L^2_tV$ 升级为强 $L^2_tL^4_x$，三线性型作为对测试变元连续的二次型经射影张量配对通过极限；(iii) 外力项的 Riesz 表示元是能量空间值有界连续路径，截断到 $[0,t]$ 后成为时空能量空间上的有界线性泛函，弱收敛直接通过。[来源：PDEIdeas/BoxLerayHopf.lean, BoxForcedLerayHopfLimit.lean, BoxForcedLerayHopf.lean, QuadraticWeakFormLimit.lean, LerayTimeTest.lean]
- **P10（极限的能量不等式与弱连续）**：Galerkin 层精确能量等式（P3）经「截断外力功的有界泛函化 + 范数平方的弱下半连续性」传至极限，得能量不等式（等式损失为不等式）；极限状态路径的弱连续性由一致能量界 + 有限模弱连续的稠密逼近得到。[来源：PDEIdeas/BoxForcedLerayHopf.lean, LeraySpectralWeakContinuity.lean]

### 1.3 证明策略素描

能量方法三段式。**第一段（ODE 层）**：Riesz 组装把弱型方程写成有限维 ODE；右端的显式二次增长界与球上 Lipschitz 常数给 Picard–Lindelöf；能量等式对 $\|u\|^2$ 微分、斜对称消去对流、微积分基本定理闭环；Young + 强制性 + 标量吸收给先验界；先验界反过来给出不爆破，统一步长 $\delta=1/(C+1)$ + 拼接 + 上确界论证拼到任意 $T$。**第二段（紧性层）**：不做完整 Aubin–Lions 定理，而是「谱尾趋于零（紧嵌入）+ 有限模等度连续（对偶导数界）⇒ 全有界」的紧逼近论证，配合可分 Hilbert 弱列紧做同步抽取。**第三段（极限层）**：时间测试弱方程逐项通过——线性项靠强-弱对，非线性项靠 2D Ladyzhenskaya 的 $L^2_tL^4_x$ 强通道，外力项靠 Riesz 路径的有界泛函化；能量不等式靠下半连续性；初值由弱连续 + 强 $L^2$ 收敛识别。

### 1.4 单元内数学依赖

P3 依赖（斜对称、FTC）；P4 依赖 P3 + Young + 强制性；P5 依赖 P1、P2、P4；P7 依赖（紧嵌入 ⇒ 谱尾 →0，单元③）+（对偶时间导数界，由 P1 型估计在公共试验空间上给出）；P8 依赖 P7 + 可分性；P9 依赖 P8 + 单元②的 Ladyzhenskaya 通道 + 单元③的谱坐标测试投影；P10 依赖 P3、P8、P9。

---

## 2. 单元②：唯一性所需估计（2D Ladyzhenskaya 不等式与 Grönwall 闭合链）

**数学目标**：建立 2D Ladyzhenskaya 不等式 $\|u\|_{L^4}^2\lesssim\|u\|_{L^2}\|\nabla u\|_{L^2}$ 的完整形式化链（从全空间 GNS 到能量空间闭包），并给出以其为唯一关键输入的 2D 弱解唯一性 Grönwall 闭合链的全部数学构件。

### 2.1 涉及定义

- **Gagliardo–Nirenberg–Sobolev（GNS）入口**：全平面 $\mathbb R^2$ 上，对 $C^1$ 紧支标量场 $q$：$\|q\|_{L^2}\le C_{GNS}\,\|\nabla q\|_{L^1}$（指数 $2$ 为 $n=2$ 的 Sobolev 共轭关系）。[来源：PDEIdeas/BoxLadyzhenskayaInequality.lean，消费 mathlib 的 GNS 定理]
- **图核与能量空间**：光滑发散自由、满足边界条件的场的「图点」$(u,Du)\in L^2\times L^2$ 之线性张成（图核），其闭包为能量空间 $V$；速度分量的闭包为枢轴空间 $H$；$J:V\to H$ 为第一分量投影（能量-状态映射）。[来源：PDEIdeas/BoxSobolevClosure.lean]
- **Ladyzhenskaya 实现**：一个连续线性映射 $V\to L^4$，与 $J$ 经有限测度包含 $L^4\hookrightarrow L^2$ 相容，并携带常数 $C_L$ 使不等式在整个 $V$ 上成立。[来源：PDEIdeas/BoxLadyzhenskayaClosure.lean]

### 2.2 关键命题

- **Q1（平面 Ladyzhenskaya）**：对 $C^1$ 紧支平面向量场 $u$，
$$\|u\|_{L^4}^2\le C_L\,\|u\|_{L^2}\,\|\nabla u\|_{L^2},\qquad C_L=2\,C_{GNS}.$$
证明：对 $q=\|u\|^2$ 用 GNS，$\nabla q=2\langle u,\nabla u\rangle$，Hölder 得 $\|\nabla q\|_{L^1}\le 2\|u\|_{L^2}\|\nabla u\|_{L^2}$。[来源：PDEIdeas/BoxLadyzhenskayaInequality.lean]
- **Q2（闭包延拓）**：光滑图核上的 Ladyzhenskaya 实现沿稠密等距包含连续延拓到闭包能量空间；有限测度包含 $L^4\hookrightarrow L^2$ 保证延拓后的 $L^4$ 代表元与 $J$ 的速度一致；不等式由连续性传到闭包。[来源：PDEIdeas/BoxLadyzhenskayaClosure.lean, BoxSmoothLadyzhenskaya.lean]
- **Q3（盒 Poincaré）**：$\|Jv\|_H\le C_P\,\|\nabla v\|$ 对一切 $v\in V$（GNS 用于 $u$ 本身得 $L^2\le C\|\nabla u\|_{L^1}$，紧支于盒内故 Hölder 把 $L^1$ 转 $L^2$）；推论：图范数与梯度半范数等价，且任意能量对偶外力可被扩散型吸收（单元① P6）。[来源：PDEIdeas/BoxPoincare.lean]
- **Q4（Ladyzhenskaya 紧性通道）**：若序列在 $L^2(0,T;H)$ 强收敛且在 $L^2(0,T;V)$ 有界，则它在 $L^2(0,T;L^4)$ 强收敛。这是 2D 非线性项极限通过的唯一特异通道（单元① P9(ii) 的输入）。[来源：PDEIdeas/BoxLadyzhenskayaLimit.lean, BoxSpectralLadyzhenskaya.lean, BoxSpectralLadyzhenskayaCompactness.lean]
- **Q5（ODE 层唯一性）**：有限维 Galerkin ODE 的任意两条有界解，在公共时间区间上逐点相等（球上 Lipschitz + Picard 唯一性，逐段拼接）。[来源：PDEIdeas/VariationalGalerkinUniqueness.lean]
- **Q6（2D 弱解唯一性的 Grönwall 闭合链——目标构件清单）**：设 $u_1,u_2$ 为同初值两条 Leray–Hopf 弱解，$w=u_1-u_2$。所需数学构件依次为：(a) 以 $w$ 为测试函数的合法性（2D 中 $w\in L^2_tV\cap L^\infty_tH$ 结合 Q1 给出 $w\in L^4_{t,x}$，使 $b(w,u_2,w)$ 可积）；(b) 差方程能量不等式 $\tfrac{d}{dt}\|w\|^2+2\nu\|\nabla w\|^2\le 2\,|b(w,u_2,w)|$；(c) 三线性估计 $|b(w,u_2,w)|\le C\|w\|_{L^4}^2\|\nabla u_2\|_{L^2}$，经 Q1 得 $\le C\|w\|_{L^2}\|\nabla w\|_{L^2}\|\nabla u_2\|_{L^2}$；(d) Young 吸收 $\le \nu\|\nabla w\|^2+C'\nu^{-1}\|\nabla u_2\|_{L^2}^2\|w\|^2$；(e) 因 $\int_0^T\|\nabla u_2\|^2<\infty$，标量 Grönwall 给出 $\|w(t)\|^2\le\|w(0)\|^2\exp\!\big(C'\nu^{-1}\int_0^t\|\nabla u_2\|^2\big)=0$。
**诚实性注记**：FGL @4d023ac 未包含 Q6 的 PDE 层形式化（论文亦未含唯一性）；本条为 Writer 实现唯一性端点时的数学需求清单，其中 (a)(c) 的构件已由 Q1–Q4 提供，(b)(d)(e) 为标准能量方法，需我方自行完成。

### 2.3 证明策略素描

Q1 是整条 2D 特异链的唯一「硬分析」入口，且全部重量压在全空间 GNS（$C^1$、紧支）上；盒域情形用盒外零延拓把盒上问题嵌入全平面，正则性衔接由图核定义吸收。Q2/Q3 是「光滑核 → 稠密延拓 → 闭包」的通用连续化模式。Q4 是插值不等式在时空层面的直接推论：强 $L^2_tH$ 控制空间 $L^2$ 因子，有界 $L^2_tV$ 控制梯度因子，乘积后在时间方向 Cauchy–Schwarz。Q6 是教科书级差分-吸收-Grönwall 链，2D 的特殊性全部经 Q1 进入；3D 情形同一链条在 (c) 处断裂（$L^4$ 插值指数不再匹配），故该链是 2D 专属。

### 2.4 单元内数学依赖

Q1 ← GNS；Q2 ← Q1 + 图核稠密性（单元③ 3.1 图空间实现）；Q3 ← GNS + 有限测度；Q4 ← Q2 + 时空 Cauchy–Schwarz；Q5 ← 单元① P1/P2；Q6(a)(c) ← Q1/Q4；Q6(e) ← 标量 Grönwall。

---

## 3. 单元③：图空间与谱坐标构造（Gram 算子 $J^*J$ 对角化）

**数学目标**：从「紧、单、密、收缩的 Hilbert 嵌入 $J:V\to H$」抽象地构造奇异坐标（$J^*J$ 对角化），得到能量/状态双正交基、递增有限穷举与 Galerkin 塔的全部有限层代数，使任何具体域只需产出该谱表示，其余机制域无关继承。

### 3.1 涉及定义

- **紧 Gelfand 三元组**：实 Hilbert 空间对 $(V,H)$ 与连续线性嵌入 $J:V\to H$，满足：单射、值域稠密、紧算子、收缩（$\|Jv\|_H\le\|v\|_V$）。枢轴映射 $H\to V'$ 由 $h\mapsto(v\mapsto\langle h,Jv\rangle_H)$ 给出。[来源：PDEIdeas/CompactGelfandTriple.lean]
- **图空间实现（具体域侧）**：$V=H^1_{0,\sigma}$ 型空间定义为光滑发散自由场图点 $(u,Du)$ 在 $L^2\times L^2$ 中的闭包（图范数），$H=L^2_\sigma$ 为速度分量闭包；$J$ 为分量投影。免 Stokes 算子/椭圆正则性：全程只用图范数与分量，不需要压力或 Stokes 特征函数。[来源：PDEIdeas/BoxSobolevClosure.lean, OpenDomainCore.lean]
- **谱坐标（奇异值分解）**：Gram 算子 $G:=J^*J:V\to V$ 紧、自伴、正、单射。由紧自伴谱定理：特征值 $\mu_1\ge\mu_2\ge\cdots>0$，仅以 $0$ 为聚点，每个特征空间有限维；取各特征空间标准正交基并合，得 $V$ 的 Hilbert 基 $\{e_i\}$（能量基）。令奇异值 $\sigma_i=\sqrt{\mu_i}$，定义状态基 $\varphi_i:=\sigma_i^{-1}Je_i$，则 $\{\varphi_i\}$ 为 $H$ 的 Hilbert 基，且
$$Je_i=\sigma_i\varphi_i,\qquad \langle Ju,\varphi_i\rangle_H=\sigma_i\langle u,e_i\rangle_V\ (\forall u\in V).$$
[来源：PDEIdeas/CompactEmbeddingSpectral.lean]
- **谱表示包**：可数指标集 $\iota$、递增有限穷举（对每个 $m$ 给出前 $m$ 项有限集「头」）、能量基、状态基、权 $\sigma_i$，满足 $|\sigma_i|\le 1$、$\sigma_i\ne0$、上列两个映射恒等式，以及 $J$ 的单/密/紧三性。[来源：PDEIdeas/CompactEmbeddingSpectral.lean]
- **有限层构件**：第 $m$ 层能量/状态子空间 $=$ 前 $m$ 个基向量的张成；归一化能量模式 $e_i/\sigma_i$（满足 $J(e_i/\sigma_i)=\varphi_i$，范数 $\sigma_i^{-1}$）；合成算子（系数向量 → 能量/状态代表元）；公共测试投影。[来源：PDEIdeas/AbstractGalerkinTower.lean]

### 3.2 关键命题

- **S1（指标可数性）**：可分 Hilbert 空间中任何正交族至多可数（半径 $1/2$ 球两两不交 + 可分性）。[来源：PDEIdeas/CompactEmbeddingSpectral.lean]
- **S2（谱坐标存在性）**：紧、单、密的 $J:V\to H$（可分 Hilbert 空间间）允许上述谱表示；权 ≤1 的归一化可由把 $J$ 换为 $\|J\|^{-1}J$ 吸收。[来源：PDEIdeas/CompactEmbeddingSpectral.lean]
- **S3（收缩性自动成立）**：谱表示一旦存在（权 ≤1），$\|Ju\|_H\le\|u\|_V$ 由 Parseval 逐坐标推出，无需单独假设。[来源：PDEIdeas/AbstractGalerkinTower.lean]
- **S4（谱尾趋于零）**：紧嵌入 ⇒ 尾投影（去掉前 $m$ 个模式）作为 $V\to H$ 算子的范数随 $m\to\infty$ 趋于 $0$。这是单元① P7 紧性通道的核心输入。[来源：PDEIdeas/CompactEmbeddingSpectral.lean, GalerkinL2Compactness.lean]
- **S5（紧性的子空间转移）**：设 $J:V\to H$ 紧，$V'\subset V$ 子空间、$H'\subset H$ **闭**子空间，$J(V')\subset H'$，则限制映射 $V'\to H'$ 仍紧；单射性由 $J$ 继承（精确判据：$V'\cap\ker J=\{0\}$）；**稠密性不自动继承**，判据为 $H'\subseteq\overline{J(V')}$；点态范数（收缩性）继承。打包形式：紧 Gelfand 三元组在上述数据下限制为子空间上的紧 Gelfand 三元组。机制：闭子空间的包含是闭嵌入，紧集原像仍紧。[来源：PDEIdeas/CompactSubspaceEmbedding.lean]
- **S6（抽象塔继承性）**：给定任一谱表示，有限层全部恒等式与界（合成算子范数、测试投影交换关系、逐层能量恒等式）与底层域无关；新域只需产出谱表示。[来源：PDEIdeas/AbstractGalerkinTower.lean, AbstractSpectralDynamics.lean]

### 3.3 证明策略素描

谱坐标的构造是「紧自伴谱定理 + 逐特征空间取基 + 像归一化」的初等组合，刻意绕开椭圆正则性：$J^*J$ 的谱理论只要求 $J$ 紧，不要求它是任何微分算子的逆。谱尾 →0 用「紧算子的值域被有限秩逼近」的标准论证。子空间转移的关键观察是紧性可沿闭嵌入「下降」，而稠密性是三元组中唯一不遗传的性质，必须以显式假设携带——这正是盒域 → 任意开域推广（单元④）的全部额外成本所在。

### 3.4 单元内数学依赖

S2 ←（紧自伴谱定理、S1）；S3 ← S2；S4 ← S2 + 紧性；S6 ← S2；S5 独立于谱构造（纯算子论），但在单元④中与 S2 合流。

---

## 4. 单元④：开域与全局化技术（OpenDomain 推广 + 时间全局化）

**数学目标**：把矩形盒上的全部机制经「闭子空间转移」推广到任意有界开平面域（无需边界正则性），并把有限时域弱解经「局部解族 + 限制相容」打包全局化到 $[0,\infty)$。

### 4.1 涉及定义

- **盒内开域数据**：矩形 $Q$ 与开集 $\Omega\subset\mathrm{int}(Q)$。光滑核改为：$C^1$、发散自由、**拓扑支集含于 $\Omega$** 的场；支集含于 $\Omega$ 自动蕴含在 $\partial Q$ 上的齐次 Dirichlet 条件，故该光滑核等距嵌入盒的光滑核。[来源：PDEIdeas/OpenDomainCore.lean]
- **开域能量/状态空间**：上述核的图点/速度闭包 $H^1_{0,\sigma}(\Omega)$、$L^2_\sigma(\Omega)$，分别是盒对应空间的闭子空间。[来源：PDEIdeas/OpenDomainCore.lean]
- **有限时域弱解（开域）**：与单元① 1.1 的 Leray–Hopf 结构同型，能量不等式与弱方程中的梯度替换为开域能量梯度分量。[来源：PDEIdeas/OpenDomainLerayHopfStatement.lean]
- **全局解打包**：三元组——全局状态路径 $u:[0,\infty)\to H$、对每个自然数 $n$ 的有限时域解族（$[0,n]$ 上的 Leray–Hopf 解）、限制相容（全局路径在每个 $[0,n]$ 上的限制等于该局部解的状态路径）。性质作为投影定理给出：弱连续（在 $t$ 处经 $\lceil t\rceil+1$ 局部化）、能量不等式、弱方程。[来源：PDEIdeas/OpenDomainGlobalLerayHopf.lean]

### 4.2 关键命题

- **G1（紧性遗传）**：开域能量-状态映射 $J_\Omega$ 经盒空间闭子空间包含与盒 $J_Q$ 交换；由单元③ S5 与盒的 Rellich 紧性（盒上经 Fourier 证明），$J_\Omega$ 紧；单射继承；稠密性由「支集于 $\Omega$ 的光滑场在 $L^2_\sigma(\Omega)$ 中稠密」的显式逼近假设提供。[来源：PDEIdeas/OpenDomainGelfandTriple.lean, OpenDomainCore.lean]
- **G2（有界开域围合）**：任意有界开平面集 $U$ 存在矩形 $Q$ 使 $U\subset\mathrm{int}(Q)$（取坐标上界加一的正方形）。推论：$U$ 上任意初值、任意有限时域存在 Leray–Hopf 弱解。[来源：PDEIdeas/OpenDomainBoundedEnclosure.lean]
- **G3（有限时域开域解）**：开域谱表示（G1 + 单元③ S2）喂入单元①的抽象塔与极限机制，得任意 $[0,T]$ 上的无迫 Leray–Hopf 解。[来源：PDEIdeas/OpenDomainLerayHopfStatement.lean]
- **G4（全局化）**：对每个 $n$ 取 $[0,n]$ 上的解族，经逐时域投影紧性做对角抽取，得单一全局路径与全部局部解限制相容；弱连续、能量不等式、弱方程逐性质从局部解投影到全局打包。[来源：PDEIdeas/OpenDomainGlobalLerayHopf.lean, OpenDomainGlobalBoundedEnclosure.lean]
- **G5（FGL 覆盖范围的诚实边界）**：FGL @4d023ac 中，受迫 Leray–Hopf 仅在矩形盒、有限时域；任意有界开域的全局解仅覆盖**无迫**情形。「受迫 + 任意开域 + 全局」的合流陈述与全空间（$\mathbb R^2$）推广均不在其内。[来源：研究档 F9/Counter-Narrative 1；PDEIdeas/PaperClaimChecks.lean 钉住的类型]
- **G6（全空间推广的数学需求——FGL 之外）**：$\mathbb R^2$ 情形的标准数学路线为域穷举：取递增球/盒列 $\Omega_k\uparrow\mathbb R^2$，每个 $\Omega_k$ 上由 G2–G4 得弱解 $u_k$；能量不等式给出与 $k$ 无关的一致界（外力取全空间对偶范数）；对角子列在每个紧子域上收敛；极限满足全空间弱方程。所需新增构件仅：与域无关的一致能量界、紧子域上的测试函数逼近、对角抽取。

### 4.3 证明策略素描

开域推广的全部成本被压缩进两个引理：支集包含 ⇒ 边界条件自动成立（光滑核嵌入盒核），以及闭子空间紧性转移（S5）。盒的 Rellich 紧性（Fourier 路线）只证一次，任意开域免费继承——这是「继承而非重证」的设计要点。全局化是纯粹的对角论证：性质逐条从有限时域投影，不打碎重证。

### 4.4 单元内数学依赖

G1 ← 单元③ S5 + 盒 Rellich；G3 ← G1 + 单元③ S2/S6 + 单元①全部；G4 ← G3 + 对角抽取；G2 为初等几何；G6 ← G2–G4 + 一致界。

---

## 5. 单元间数学依赖图（文字版）

```
[通用分析底座] GNS（全空间 C¹ 紧支）、紧自伴谱定理、Arzelà–Ascoli、
              可分 Hilbert 弱列紧、Picard–Lindelöf、标量 Grönwall、FTC
      │
      ├─→ 单元③（图空间实现（3.1） → 紧 Gelfand 三元组 → 谱坐标 S2 → 谱尾 S4、子空间转移 S5、抽象塔 S6）
      │         │
      ├─→ 单元②（GNS → Q1 Ladyzhenskaya → Q2 闭包 → Q3 Poincaré → Q4 时空紧性通道）
      │         │
      ▼         ▼
      单元①（P1–P6 ODE 层：存在/能量等式/先验界/全局延拓
              ← 单元② Q3 提供受迫吸收 P6
              P7–P8 紧性抽取 ← 单元③ S4 + 单元②的对偶导数估计接口
              P9 非线性极限 ← 单元② Q4（2D 特异）；测试投影 ← 单元③ S6
              P10 端点性质）
      │         │
      │         └─→ 单元② Q6（唯一性 Grönwall 闭合链；FGL 未含，目标构件清单）
      ▼
      单元④（G1 紧性遗传 ← 单元③ S5 + 盒 Rellich；G2 围合；G3 ← 单元①+③；G4 全局化）
```

要点：2D 的特殊性全部集中于单元② Q1 一处；谱坐标（单元③）使 Stokes 算子与椭圆正则性完全不出现；单元④ 对单元①②③ 只做继承不做修改。

---

## 6. 与我方 M2 需求的接口注记（仅述数学需求，不涉任何实现标识符）

> 本节供 Writer 轨对齐我方 2D 周期 Galerkin 有限维层与 M2 端点。只陈述「需要什么数学性质的构件」。

1. **有限维截断层（已有基础的升级方向）**：需要一个有限维内积空间上的变分 Galerkin 问题层：双线性扩散型（非负，最好带强制性常数）、三线性对流型（带**显式数据化**的界常数 $C_b$，而非仅导出算子范数）、斜对称或能量抵消、**时间依赖对偶外力**（Riesz 组装模式）与初值打包。我方方面常值向量外力是数学特例，无需改动既有接口，只需新增对偶外力变体。
2. **周期域 vs 盒域的路线分叉**：FGL 的 2D 链以「盒 + 零延拓 + 全平面 GNS」为入口（单元②）；周期域 $\mathbb T^2$ 情形的数学对应物为：环面上的 GNS/Ladyzhenskaya（无紧支要求，可用 Fourier 或直接的全空间定理于周期函数，均值条件按所取空间处理），可**绕开零延拓的正则性衔接**。周期域的 Rellich 紧性与 Poincaré（零均值）均为标准件。Writer 应把单元②的 Q1–Q4 理解为「在所用域上成立这些不等式与通道」的需求，而非复刻盒域路线。
3. **谱坐标构件**：M2 若走谱路线，需要数学上提供：紧、单、密、收缩嵌入 $J:V\to H$ 的谱表示（单元③ D/S 系列），含可数指标、递增有限穷举、双正交基与坐标恒等式。周期域上 $J$ 的紧性由 Fourier 直接给出，谱坐标甚至可与 Fourier 基对齐（此时 $J^*J$ 已对角），工作量远小于一般情形。
4. **紧性通道**：不实现完整 Aubin–Lions 定理；实现「有限模等度连续 + 谱尾 →0 ⇒ 强 $L^2_tH$」与「强-弱同步抽取」两个数学构件即可，另需公共试验空间上的对偶时间导数一致界（单元① P7 的输入）。
5. **唯一性端点**：单元② Q6 的链条在 FGL 中不存在，是我方可独立占据的端点；其全部硬输入为周期版 Ladyzhenskaya（接口注记 2）与标准标量 Grönwall。
6. **端点陈述模板**：全局弱解宜采用「全局路径 + 逐 $[0,n]$ 局部解族 + 限制相容」三字段打包，性质（弱连续/能量不等式/弱方程）作投影定理（单元④ G4 的数学结构）。
7. **受迫 + 任意域 + 全局的合流**：FGL 未覆盖（G5）；若 M2 目标包含受迫全局解，数学上只需把单元① P6 的受迫吸收与单元④ G4 的对角全局化复合，无新增硬分析。

---

## 7. 尾部

### 7.1 取材操作日志

1. `git clone https://ghfast.top/https://github.com/wwang-math/FluidGalerkinLean $HOME/fgl-ro`（只读克隆，成功）。
2. `git checkout 4d023ac47aea65a4a5dbbc20004f5fda0ee18755`：HEAD 核验输出 `4d023ac Add bounded-domain global Leray-Hopf formalization`；`git rev-parse HEAD` = `4d023ac47aea65a4a5dbbc20004f5fda0ee18755`（与任务指定哈希全等）；tag 列表含 `arxiv-v1`。
3. 规模核验：`find -name '*.lean'` 计 108 个文件（含 PDEIdeas.lean 与 lakefile.lean），`wc -l` 合计 32266 行（与研究档「107 文件/32252 行」口径差异：研究档未计入 lakefile/根模块或行数口径不同，不影响取材）。
4. 直读文件（只读，提取数学内容）：GalerkinSystem / GalerkinCore / GalerkinDynamics / GalerkinProjection / GalerkinScalarAbsorption / GalerkinIntegralEstimates / GalerkinPointwiseYoung / VariationalGalerkin（能量等式段）/ VariationalGalerkinUniqueness / CompactGelfandTriple / CompactSubspaceEmbedding / CompactEmbeddingSpectral / AbstractGalerkinTower / AbstractSpectralDynamics / BoxSobolevClosure / BoxLadyzhenskayaInequality / BoxLadyzhenskayaClosure / BoxLadyzhenskayaLimit / BoxPoincare / BoxForcedSpectralGalerkin / BoxForcedLerayHopf / BoxForcedLerayHopfLimit / BoxLerayHopf / BoxLerayWeakCompactness / LeraySpectralWeakCompactness / GalerkinL2Compactness / LerayTimeTest / QuadraticWeakFormLimit / OpenDomainCore / OpenDomainGelfandTriple / OpenDomainBoundedEnclosure / OpenDomainGlobalBoundedEnclosure / OpenDomainLerayHopfStatement（模块头与命题陈述层）。
5. 未执行任何 `git` 远端写操作；未对 FGL 仓库做任何修改；未执行 FGL 构建（只读纪律）。
6. 背景参考（只读，未做逐行对照）：/mnt/agents/output/research/frontier_dim03.md；我方 library/ns 文件未打开。

### 7.2 规格元数据

- 文件：/mnt/agents/output/vci-inbox/specs/FGL-SEAM-SPEC-01.md
- 行数：218
- SHA-256：9c0e0acd0ce4d29ba174befc0c0b148ce2dadb98ecf39d3de7508e5a335f7a99（填入本字段前文件内容之哈希，自引用不可避，留此约定）

——EXT-WAVE-18「攻」WS-E 攻坚线 Reader 轨执行席（枢/PIVOT-01 体系）· 2026-10-21
