-- CLASSIFY: L1
/-
WS-B 降级档 · D-D · Q6 抽象闭合链骨架（条件定理式，显式假设束携带）
（EXT-WAVE-18 续执行批四 · 枢/PIVOT-01 体系 L8 攻坚席 · 全程中文注释）

【禁越界钉（m2_uniqueness_spike_01 §2.2 在案，强制执行）】
2D Navier–Stokes 弱解唯一性是 Lions–Magenes 体系的**经典已知结果**；本文件是其
Lean 4 + mathlib 形式化工程的**条件式抽象链骨架**：所证定理为
「假设 w 可作测试 ∧ w 满足差方程能量不等式（含三线性估计接口与
Ladyzhenskaya 常数槽位）⇒ w ≡ 0」。**本文件任何交付物不得表述为
「2D 弱解唯一性已形式化」**——Q6(a) 测试合法性与 Q6(b) 的 PDE 语义层
均为**显式假设位**（structure 字段携带，非 sorry），其 PDE 层证明登记为
BLOCKED（见下节）。D 档闭合的是「ODE 层 + 不等式层 + 条件式抽象链」。

【数学内容】（FGL-SEAM-SPEC-01 单元② Q6 目标构件清单）
设 u₁、u₂ 为同初值两条 Leray–Hopf 弱解，w = u₁ − u₂。经典闭合链：
  (a) 以 w 为测试函数的合法性（2D 中 w ∈ L²_tV ∩ L∞_tH 经 Q1 得 w ∈ L⁴_{t,x}）；
  (b) 差方程能量不等式 d/dt‖w‖² + 2ν‖∇w‖² ≤ 2|b(w,u₂,w)|；
  (c) 三线性估计 |b(w,u₂,w)| ≤ C‖w‖²_{L⁴}‖∇u₂‖_{L²}，
      经 Q1（Ladyzhenskaya）得 ≤ C‖w‖_{L²}‖∇w‖_{L²}‖∇u₂‖_{L²}；
  (d) Young 吸收 ≤ ν‖∇w‖² + C'ν⁻¹‖∇u₂‖²_{L²}‖w‖²；
  (e) 标量 Grönwall（∫₀ᵀ‖∇u₂‖² < ∞）给出 ‖w(t)‖² ≤ ‖w(0)‖²·exp(·) = 0。
本骨架将 (a)(b) 以显式假设位携带（PDE 层未证），在此二假设下**证毕**
(c)（`step_c_trilin_est`：三线性 Hölder 接口 × Ladyzhenskaya 槽位组装）→
(d)（`step_d_young`：Young 吸收，纯实代数）→ (e)（标量 Grönwall 组装，
mathlib E6 件 `le_gronwallBound_of_liminf_deriv_right_le` 消费），
主定理 `q6_conditional_uniqueness` 得 w ≡ 0。

【假设清单（逐字 = 假设束字段名）】
主定理 `q6_conditional_uniqueness` 的全部假设即结构体 `Q6DifferenceBundle`
的字段，逐字清单：
  ① `testAdmissible` + `h_test`  —— Q6(a)「w 可作测试」（测试合法性，
     PDE 层未证 → 假设位；BLOCKED-DD-Q6a 登记见下）；
  ② `dw` + `hcont` + `hlim` + `henergy` —— Q6(b)「w 满足差方程能量不等式」
     `dw(t) + 2ν·Vw(t) ≤ 2·tri(t)`（导数数据 `dw` 携 liminf 右斜率接口 `hlim`
     与连续性 `hcont`；PDE 语义层未证 → 假设位；BLOCKED-DD-Q6b 登记见下）；
  接口槽位：`htri_est`（三线性 Hölder 界 `tri ≤ C_tri·L4w·Gu`，
     常数槽 `C_tri`）、`hlady`（Ladyzhenskaya 插值
     `L4w ≤ C_L·√‖w‖²·√Vw`，常数槽 `C_L` 接 D-B，
     当前 D-B 周期版显式常数见 `NsGalerkin/Ladyzhenskaya.lean` 在案件；
     PDE/能量空间层数值待 GO 档落定）；
  骨架强化槽（诚实登记）：`K_G` + `hKG_bound` —— Grönwall 系数有界槽
     `(C_tri·C_L)²·ν⁻¹·‖∇u₂(t)‖² ≤ K_G`。经典链只需 ∫₀ᵀ‖∇u₂‖² < ∞
     （时间变系数可积 Grönwall）；mathlib E6 件为常系数 Grönwall，
     本骨架以区间上有界槽对接，有限维 Galerkin 实例层该槽自动满足
     （轨道连续 ⇒ ‖∇u₂‖ 有界），可积系数化升级登记为后续批次义务；
  初值条件：`hw0`（w a = 0，即两解同初值）。

【BLOCKED 登记段】（五态机口径对齐 NS-PROOF-FRAME-01 §3.3：
state=BLOCKED，触发器沿用 B1（结构不可验证族），退出路径 =
v0.4 §2.4 退出路径 3（仅判定席裁决），不得自动重试、禁止直达 DONE）

  ┌──────────────────┬─────────────────────────────────────────────┐
  │ BLOCKED-DD-Q6a   │ Q6(a) 测试合法性的 PDE 层证明：弱解差         │
  │ state=BLOCKED(B1)│ w ∈ L²_tV ∩ L∞_tH 代入弱形式差方程为测试函数  │
  │                  │ 的合法性（∂ₜw 仅在 V' 层，时间对偶配对演算    │
  │                  │ 为形式化主要摩擦点）。recoverable=false，     │
  │                  │ retry_after = GO 档判定（J2/J5 钉齐，         │
  │                  │ 2026-11-18 检查点会议裁定；J7 降级闸在案）。  │
  │                  │ 命中证据指针：本文件 `testAdmissible`/`h_test`│
  │                  │ 假设位。登记时刻：EXT-WAVE-18 续执行批四。    │
  ├──────────────────┼─────────────────────────────────────────────┤
  │ BLOCKED-DD-Q6b   │ Q6(b) 差方程能量不等式的 PDE 语义层证明：     │
  │ state=BLOCKED(B1)│ 在 PDE 弱方程语义上代入测试函数 w 导出        │
  │                  │ d/dt‖w‖² + 2ν‖∇w‖² ≤ 2|b(w,u₂,w)|。         │
  │                  │ recoverable=false，retry_after = GO 档判定    │
  │                  │ （同上钉）。命中证据指针：本文件 `henergy`    │
  │                  │ 假设位。登记时刻：EXT-WAVE-18 续执行批四。    │
  └──────────────────┴─────────────────────────────────────────────┘

【J7 闸登记】（Q6(a) 难度判断义务，单体评估初判，一句话）
Q6(a) 经「Galerkin 层先取 w_m 为测试、再经 Q1 插值取极限」替代证法的
单体评估初判：**≤ 3 pw（点估 ≈ 2–2.5 pw）**——w_m 层测试代入与斜相消
复用 E9 存量 ODE 引擎，新增工作量集中于「逐模能量等式取极限 + Q1 插值
升级 w ∈ L⁴_{t,x} + 三线性项弱极限配对」一段，无新硬分析入口，故低于
J7 降级闸 3 pw 阈值，但极限配对的 API 摩擦使其接近阈值上沿，须在 GO 档
首周复核产能实耗。

【工程口径】零 sorry（全部假设以 structure 字段/假设位携带，无 sorryAx）；
公理仅三件套 [propext, Classical.choice, Quot.sound]（尾部 #print axioms
构建期审计行在案）。版本钉：leanprover/lean4:v4.35.0 + mathlib v4.35.0
（@56a00585）。
-/
import NsGalerkin.Basic

open Set Filter
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

namespace CondUniqueness

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- **Q6 条件唯一性假设束**（假设清单 = 字段名逐字清单）。

差 `w = u₁ − u₂` 定义在能量空间（H 层，内积空间）上；`Vw`/`L4w`/`Gu`/`tri`
为 V 半范平方、L⁴ 范数平方、‖∇u₂‖、|b(w,u₂,w)| 的**数据槽位**
（PDE 语义层的范数结构未形式化，按骨架口径以非负实函数数据携带，
各槽位的 PDE 层落地属 BLOCKED-DD-Q6a/Q6b 与 GO 档范围）。

假设字段分四组（与文件头假设清单一一对应）：
① `testAdmissible`/`h_test`：Q6(a) 测试合法性（假设位）；
② `dw`/`hcont`/`hlim`/`henergy`：Q6(b) 差方程能量不等式（假设位，
   导数数据 + liminf 右斜率接口 + 连续性 + 逐点不等式）；
接口槽：`htri_est`（三线性 Hölder 接口）、`hlady`（Ladyzhenskaya 接口，
   常数槽 `C_L` 接 D-B）；
骨架强化槽：`K_G`/`hKG_bound`（Grönwall 系数区间有界，诚实登记见文件头）；
初值：`hw0`（w a = 0）。 -/
structure Q6DifferenceBundle (E : Type*) [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] where
  /-- 黏度 ν > 0。 -/
  ν : ℝ
  hν : 0 < ν
  /-- Ladyzhenskaya 常数槽位（接 D-B；PDE/能量空间层数值待 GO 档落定）。 -/
  C_L : ℝ
  hC_L : 0 ≤ C_L
  /-- 三线性 Hölder 界常数槽位。 -/
  C_tri : ℝ
  hC_tri : 0 ≤ C_tri
  /-- 时间区间左端点。 -/
  a : ℝ
  /-- 时间区间右端点。 -/
  b : ℝ
  hab : a ≤ b
  /-- 唯一性差 w = u₁ − u₂（时间轨道）。 -/
  w : ℝ → E
  /-- V 半范平方数据槽位：`Vw t` 代表 ‖∇w(t)‖²。 -/
  Vw : ℝ → ℝ
  hVw : ∀ t : ℝ, 0 ≤ Vw t
  /-- L⁴ 范数平方数据槽位：`L4w t` 代表 ‖w(t)‖²_{L⁴}。 -/
  L4w : ℝ → ℝ
  hL4w : ∀ t : ℝ, 0 ≤ L4w t
  /-- 背景解梯度数据槽位：`Gu t` 代表 ‖∇u₂(t)‖。 -/
  Gu : ℝ → ℝ
  hGu : ∀ t : ℝ, 0 ≤ Gu t
  /-- 三线性项绝对值数据槽位：`tri t` 代表 |b(w,u₂,w)(t)|。 -/
  tri : ℝ → ℝ
  htri : ∀ t : ℝ, 0 ≤ tri t
  /-- Grönwall 系数上界槽位（骨架强化槽，见文件头诚实登记）。 -/
  K_G : ℝ
  hKG : 0 ≤ K_G
  /-- **假设①（Q6(a)，测试合法性，PDE 层未证 → 假设位）**：
  w 可作为测试函数代入弱形式差方程（语义槽位，Prop 字段携带；
  BLOCKED-DD-Q6a 登记见文件头）。 -/
  testAdmissible : Prop
  /-- 假设①的证据位：测试合法性成立（由假设束携带，非 sorry）。 -/
  h_test : testAdmissible
  /-- 能量导数数据槽位：`dw t` 代表 d/dt‖w(t)‖² 的导数界数据。 -/
  dw : ℝ → ℝ
  /-- 能量函数连续性（②的拓扑接口）：`t ↦ ‖w t‖²` 在 `Icc a b` 上连续。 -/
  hcont : ContinuousOn (fun t => ‖w t‖ ^ 2) (Icc a b)
  /-- 能量导数的 liminf 右斜率接口（②的导数语义接口）：
  `dw t` 是 `s ↦ ‖w s‖²` 在 `t` 处右斜率的 liminf 下界控制数据。 -/
  hlim : ∀ t ∈ Ico a b, ∀ r : ℝ, dw t < r →
    ∃ᶠ z in 𝓝[>] t, (z - t)⁻¹ * (‖w z‖ ^ 2 - ‖w t‖ ^ 2) < r
  /-- **假设②（Q6(b)，差方程能量不等式，PDE 语义层未证 → 假设位）**：
  `dw t + 2ν·Vw t ≤ 2·tri t`（即 d/dt‖w‖² + 2ν‖∇w‖² ≤ 2|b(w,u₂,w)|；
  BLOCKED-DD-Q6b 登记见文件头）。 -/
  henergy : ∀ t ∈ Ico a b, dw t + 2 * ν * Vw t ≤ 2 * tri t
  /-- 三线性 Hölder 估计接口（(c) 的通用侧槽位）：
  `tri t ≤ C_tri·L4w t·Gu t`（即 |b(w,u₂,w)| ≤ C‖w‖²_{L⁴}‖∇u₂‖_{L²}）。 -/
  htri_est : ∀ t : ℝ, tri t ≤ C_tri * L4w t * Gu t
  /-- Ladyzhenskaya 插值接口（(c) 的 2D 特异侧槽位，常数槽 `C_L` 接 D-B）：
  `L4w t ≤ C_L·√(‖w t‖²)·√(Vw t)`
  （即 ‖w‖²_{L⁴} ≤ C_L·‖w‖_{L²}·‖∇w‖_{L²}）。 -/
  hlady : ∀ t : ℝ, L4w t ≤ C_L * Real.sqrt (‖w t‖ ^ 2) * Real.sqrt (Vw t)
  /-- Grönwall 系数有界槽（骨架强化槽）：Young 吸收后的时间变系数
  `(C_tri·C_L)²·ν⁻¹·‖∇u₂(t)‖²` 在 `[a,b)` 上有公共上界 `K_G`
  （经典链的可积性条件 ∫₀ᵀ‖∇u₂‖² < ∞ 的骨架对接形式，见文件头登记）。 -/
  hKG_bound : ∀ t ∈ Ico a b, (C_tri * C_L) ^ 2 / ν * (Gu t) ^ 2 ≤ K_G
  /-- 初值条件：两解同初值，故 `w a = 0`。 -/
  hw0 : w a = 0

namespace Q6DifferenceBundle

variable (Q : Q6DifferenceBundle E)

/-- **(c) 三线性估计组装**：三线性 Hölder 接口 × Ladyzhenskaya 槽位复合，
`2·tri t ≤ 2·(C_tri·C_L)·Gu t·√(‖w t‖²)·√(Vw t)`
（即 2|b(w,u₂,w)| ≤ 2·C·‖∇u₂‖·‖w‖_{L²}·‖∇w‖_{L²} 的槽位形式；
纯实代数组装，无新假设）。 -/
theorem step_c_trilin_est (t : ℝ) :
    2 * Q.tri t ≤
      2 * (Q.C_tri * Q.C_L) * Q.Gu t *
        Real.sqrt (‖Q.w t‖ ^ 2) * Real.sqrt (Q.Vw t) := by
  have h1 := Q.htri_est t
  have h2 := Q.hlady t
  have h3 : Q.C_tri * Q.L4w t * Q.Gu t ≤
      Q.C_tri * (Q.C_L * Real.sqrt (‖Q.w t‖ ^ 2) * Real.sqrt (Q.Vw t)) * Q.Gu t :=
    mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left h2 Q.hC_tri) (Q.hGu t)
  calc 2 * Q.tri t
      ≤ 2 * (Q.C_tri * Q.L4w t * Q.Gu t) := by linarith [h1]
    _ ≤ 2 * (Q.C_tri *
          (Q.C_L * Real.sqrt (‖Q.w t‖ ^ 2) * Real.sqrt (Q.Vw t)) * Q.Gu t) := by
        linarith [h3]
    _ = 2 * (Q.C_tri * Q.C_L) * Q.Gu t *
          Real.sqrt (‖Q.w t‖ ^ 2) * Real.sqrt (Q.Vw t) := by ring

/-- **(d) Young 吸收**：`2·(C_tri·C_L)·Gu·√‖w‖²·√Vw ≤ ν·Vw + (C_tri·C_L)²·ν⁻¹·Gu²·‖w‖²`
（`2xy ≤ νy² + x²/ν` 配 `x = (C_tri·C_L)·Gu·√‖w‖²`、`y = √Vw`；纯实代数，
ν > 0 由假设束 `hν` 供给）。 -/
theorem step_d_young (t : ℝ) :
    2 * (Q.C_tri * Q.C_L) * Q.Gu t *
        Real.sqrt (‖Q.w t‖ ^ 2) * Real.sqrt (Q.Vw t) ≤
      Q.ν * Q.Vw t +
        (Q.C_tri * Q.C_L) ^ 2 / Q.ν * (Q.Gu t) ^ 2 * ‖Q.w t‖ ^ 2 := by
  have hν2 : (0 : ℝ) < Q.ν := Q.hν
  have hνne : Q.ν ≠ 0 := ne_of_gt hν2
  set x := Q.C_tri * Q.C_L * Q.Gu t * Real.sqrt (‖Q.w t‖ ^ 2) with hx
  set y := Real.sqrt (Q.Vw t) with hy
  have h0 := sq_nonneg (Q.ν * y - x)
  have key : 2 * x * y ≤ Q.ν * y ^ 2 + x ^ 2 / Q.ν := by
    have e : Q.ν * y ^ 2 + x ^ 2 / Q.ν = (Q.ν ^ 2 * y ^ 2 + x ^ 2) / Q.ν := by
      field_simp
    rw [e, le_div_iff₀ hν2]
    nlinarith [h0]
  have hVx : y ^ 2 = Q.Vw t := Real.sq_sqrt (Q.hVw t)
  have hHx : (Real.sqrt (‖Q.w t‖ ^ 2)) ^ 2 = ‖Q.w t‖ ^ 2 :=
    Real.sq_sqrt (sq_nonneg _)
  have hx2 : x ^ 2 = (Q.C_tri * Q.C_L * Q.Gu t) ^ 2 * ‖Q.w t‖ ^ 2 := by
    calc x ^ 2
        = ((Q.C_tri * Q.C_L * Q.Gu t) * Real.sqrt (‖Q.w t‖ ^ 2)) ^ 2 := by rw [hx]
      _ = (Q.C_tri * Q.C_L * Q.Gu t) ^ 2 * (Real.sqrt (‖Q.w t‖ ^ 2)) ^ 2 :=
          mul_pow _ _ _
      _ = (Q.C_tri * Q.C_L * Q.Gu t) ^ 2 * ‖Q.w t‖ ^ 2 := by rw [hHx]
  calc 2 * (Q.C_tri * Q.C_L) * Q.Gu t *
        Real.sqrt (‖Q.w t‖ ^ 2) * Real.sqrt (Q.Vw t)
      = 2 * x * y := by rw [hx, hy]; ring
    _ ≤ Q.ν * y ^ 2 + x ^ 2 / Q.ν := key
    _ = Q.ν * Q.Vw t +
          (Q.C_tri * Q.C_L) ^ 2 / Q.ν * (Q.Gu t) ^ 2 * ‖Q.w t‖ ^ 2 := by
        rw [hVx, hx2]; ring

/-- **(e) Grönwall 组装 ⇒ 主定理（Q6 条件唯一性）**：
在假设束 `Q6DifferenceBundle` 的全部假设下（逐字清单 = 字段名：
① `testAdmissible`/`h_test`（w 可作测试）；
② `dw`/`hcont`/`hlim`/`henergy`（w 满足差方程能量不等式）；
接口槽 `htri_est`/`hlady`（三线性 Hölder × Ladyzhenskaya，常数槽 `C_L`）；
骨架强化槽 `K_G`/`hKG_bound`；初值 `hw0`），唯一性差的能量经
(c)（`step_c_trilin_est`）→ (d)（`step_d_young`）→ (e)（标量 Grönwall，
mathlib E6 件 `le_gronwallBound_of_liminf_deriv_right_le`，δ = ε = 0）
组装闭合：**w ≡ 0**（`∀ t ∈ Icc a b, w t = 0`，唯一性差消失）。

【禁越界钉】本定理是**条件定理**：结论 w ≡ 0 的全部前提均为假设位字段，
Q6(a)/(b) 的 PDE 层证明登记为 BLOCKED-DD-Q6a/Q6b（文件头）；
不得表述为「2D 弱解唯一性已形式化」。 -/
theorem q6_conditional_uniqueness : ∀ t ∈ Icc Q.a Q.b, Q.w t = 0 := by
  intro t ht
  -- (e) Grönwall 就绪的导数界：dw ≤ K_G·‖w‖² + 0（(b)+(c)+(d) 三段复合）
  have hbound : ∀ s ∈ Ico Q.a Q.b, Q.dw s ≤ Q.K_G * ‖Q.w s‖ ^ 2 + 0 := by
    intro s hs
    have he := Q.henergy s hs
    have hc := Q.step_c_trilin_est s
    have hd := Q.step_d_young s
    have hKG := Q.hKG_bound s hs
    have hnn : 0 ≤ ‖Q.w s‖ ^ 2 := sq_nonneg _
    have hmul : (Q.C_tri * Q.C_L) ^ 2 / Q.ν * (Q.Gu s) ^ 2 * ‖Q.w s‖ ^ 2 ≤
        Q.K_G * ‖Q.w s‖ ^ 2 :=
      mul_le_mul_of_nonneg_right hKG hnn
    have hVnn := Q.hVw s
    have hν := Q.hν
    -- dw ≤ 2tri − 2νVw ≤ (νVw + K_G‖w‖²) − 2νVw = K_G‖w‖² − νVw ≤ K_G‖w‖²
    nlinarith [he, hc, hd, hmul]
  -- 初值：‖w a‖² = 0 ≤ δ = 0
  have ha : ‖Q.w Q.a‖ ^ 2 ≤ 0 := by rw [Q.hw0, norm_zero]; norm_num
  -- 标量 Grönwall（E6 在案件，K = K_G 常数，δ = ε = 0）
  have hG := le_gronwallBound_of_liminf_deriv_right_le
    (f := fun s => ‖Q.w s‖ ^ 2) (f' := Q.dw) (δ := 0) (K := Q.K_G) (ε := 0)
    Q.hcont Q.hlim ha hbound t ht
  have hG0 : ‖Q.w t‖ ^ 2 ≤ 0 := by
    by_cases hK : Q.K_G = 0
    · rw [hK, gronwallBound_K0] at hG
      simpa using hG
    · rw [gronwallBound_of_K_ne_0 hK] at hG
      simpa using hG
  have hz : ‖Q.w t‖ ^ 2 = 0 := le_antisymm hG0 (sq_nonneg _)
  have hnnorm : ‖Q.w t‖ = 0 := (pow_eq_zero_iff two_ne_zero).mp hz
  exact norm_eq_zero.mp hnnorm

/-- **条件唯一性的两解形式（组装包装）**：两条轨道 `u₁ u₂ : ℝ → E`
若在区间端点 `a` 相等，且其差 `w = u₁ − u₂` 承载假设束
`Q6DifferenceBundle`（假设清单逐字同主定理），则两解在 `[a, b]` 上
处处相等。本件仅是「差消失 ⇒ 两解相等」的逐点改写，不引入新假设。 -/
theorem q6_eq_of_bundle {u₁ u₂ : ℝ → E}
    (Q : Q6DifferenceBundle E) (hw : Q.w = fun t => u₁ t - u₂ t) :
    ∀ t ∈ Icc Q.a Q.b, u₁ t = u₂ t := by
  intro t ht
  have h := Q.q6_conditional_uniqueness t ht
  rw [hw] at h
  have h' : u₁ t - u₂ t = 0 := h
  exact sub_eq_zero.mp h'

end Q6DifferenceBundle

-- D-D 件公理审计（构建期打印；期望仅 [propext, Classical.choice, Quot.sound]）。
#print axioms CondUniqueness.Q6DifferenceBundle.step_c_trilin_est
#print axioms CondUniqueness.Q6DifferenceBundle.step_d_young
#print axioms CondUniqueness.Q6DifferenceBundle.q6_conditional_uniqueness
#print axioms CondUniqueness.Q6DifferenceBundle.q6_eq_of_bundle

end CondUniqueness

end NSGalerkin
