-- CLASSIFY: L1
/-
EXT-WAVE-18 饱和批 · Lorenz-96 线 M2 主攻件（枢/PIVOT-01 体系 L1 席 · 全程中文注释）
吸收球（absorbing ball）解析层 Lean 形式化——M2 路线裁决书
LORENZ96-M2-ROUTE-RULING-01 §2.2 G3 主路线 (b-i) 层：「吸收球 trapping 解析主证」
（kernel 可 Lean 化层；数值包络见证层 (b-ii) 与球面正控区间证书另件承接）。

【数学内容】（定式表 LORENZ96-M0-CONSTANTS-v0 §2.5，S2 Prop 7 一手钉，
S2 式(38) 能量链逐项机器化）
Lorenz-96 标准形 ẋ_j = (x_{j+1}−x_{j−2})·x_{j−1} − x_j + F（下标 mod N）
的能量耗散链，全部 sorry-free：
1. 假设束 `LorenzAbsorbingBundle`：N（维数，NeZero）、F（常值强迫强度）、
   全局轨道 u : ℝ → EuclideanSpace ℝ (Fin N)，字段携带连续性 `hcont` 与
   处处可微性 `hderiv`（HasDerivAt 到 `lorenz96Galerkin` 实例右端，
   全局域 limsup 渐近陈述所需）。
2. 能量恒等式 `LorenzAbsorbingBundle.hasDerivAt_energy`：
   d/dt(½‖u‖²) = −‖u‖² + F·Σᵢ uᵢ（非线性项零和由 M1 已证件
   `inner_cyclicB_self` 对角相消经 GalerkinNS.hskew 槽位供给；
   耗散项 −‖u‖² 来自 ν = 1、A = id（hA 饱和取等）；
   forcing 项内积展开为 F·Σᵢ uᵢ，见 `inner_lorenz96_f`）。
3. Cauchy–Schwarz 上界 `forcing_sum_le`：F·Σᵢ uᵢ ≤ |F|·√N·‖u‖
   （经 ⟪f, u⟫ ≤ ‖f‖·‖u‖ 与 ‖f‖ = |F|·√N，`norm_lorenz96_f`）。
4. 吸收界 `LorenzAbsorbingBundle.norm_sq_le_absorbing`（标量 Grönwall/
   比较原理，mathlib E6 件 `le_gronwallBound_of_liminf_deriv_right_le`，
   K = −1、ε = R²）：t ∈ [0, T] 上
   ‖u t‖² ≤ ‖u 0‖²·e^(−t) + (|F|·√N)²·(1 − e^(−t))（平方能量版）。
5. limsup 陈述 `LorenzAbsorbingBundle.limsup_norm_le`：
   limsup_{t→+∞} ‖u t‖ ≤ |F|·√N = R（吸收球半径）；
   推论 `limsup_norm_le_48`：N = 36、F = 8 ⇒ 界 48
   （`absorbingRadius_36_8`：|8|·√36 = 8·6 = 48，与 M0 定式表 §2.5
   R = √N·|F| = 48 数值对拍，机器自算）。

【口径钉（C1/E9）】全部结论为有限维 ODE 截断层（EuclideanSpace ℝ (Fin N)）
机器检验定理，不构成任何 PDE 断言；limsup 为范数渐近上界，不构成吸引子
刻画/轨道包络（R2 语言钉；路线裁决 §四配置表 (b-i) 行「kernel 层已证
（定理钉）」于本件达成后适用，禁升格 NS 任何档位）。

【残余开口（如实登记）】
* 全局强解存在性不在本件范围，由 bundle 假设位 `hderiv`/`hcont` 承担
  （M1 已证逐 T 截断存在性 `lorenz96_exists_solution_upto`；全局流拼接
  为独立事项，Lorenz96.lean §四 L34b 已登记 CONDITIONAL-PASS）。
* 平方能量版吸收界与范数版 ‖u t‖ ≤ ‖u 0‖·e^(−t) + R·(1−e^(−t)) 数学上
  同源（后者经 √E 奇异点处理更繁）；本件交付平方版 + limsup 范数版，
  界强度对 limsup 语义等价。
* (b-ii) 数值包络见证层与球面正控严格区间证书（G1/G2 不销账）另件承接。

工具链钉：leanprover/lean4:v4.35.0 + mathlib v4.35.0（lake-manifest 现钉）。
-/
import NsGalerkin.Lorenz96

open Set Filter
open scoped InnerProductSpace NNReal Topology

noncomputable section

namespace NSGalerkin

namespace Lorenz96

variable {N : ℕ} [NeZero N]

/-- 吸收球半径 `R = |F|·√N`（定式表 v0 §2.5，S2 Prop 7 一手钉；
Lean 侧由 `‖(lorenz96Galerkin F).f‖` 承载，见 `norm_lorenz96_f`）。 -/
def absorbingRadius (N : ℕ) (F : ℝ) : ℝ := |F| * Real.sqrt (N : ℝ)

/-! ### 一、外力范数与内积展开（forcing 接缝） -/

/-- Lorenz-96 常值外力 f = F·𝟙 的范数：‖f‖ = |F|·√N = R
（吸收球半径的 Lean 载体；L2 范数平方和逐坐标计算）。 -/
theorem norm_lorenz96_f (F : ℝ) :
    ‖(lorenz96Galerkin (N := N) F).f‖ = absorbingRadius N F := by
  have hf : (lorenz96Galerkin (N := N) F).f = WithLp.toLp 2 (fun _ => F) := rfl
  have hsq : ‖(lorenz96Galerkin (N := N) F).f‖ ^ 2 = (N : ℝ) * F ^ 2 := by
    rw [hf, PiLp.norm_sq_eq_of_L2]
    simp only [Real.norm_eq_abs, sq_abs]
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  show ‖(lorenz96Galerkin (N := N) F).f‖ = |F| * Real.sqrt (N : ℝ)
  calc ‖(lorenz96Galerkin (N := N) F).f‖
      = Real.sqrt (‖(lorenz96Galerkin (N := N) F).f‖ ^ 2) :=
        (Real.sqrt_sq (norm_nonneg _)).symm
    _ = Real.sqrt ((N : ℝ) * F ^ 2) := by rw [hsq]
    _ = Real.sqrt (N : ℝ) * Real.sqrt (F ^ 2) := Real.sqrt_mul (Nat.cast_nonneg _) _
    _ = Real.sqrt (N : ℝ) * |F| := by rw [Real.sqrt_sq_eq_abs]
    _ = |F| * Real.sqrt (N : ℝ) := mul_comm _ _

/-- forcing 内积展开：⟪f, x⟫ = F·Σᵢ xᵢ（f = F·𝟙 的逐坐标形）。 -/
theorem inner_lorenz96_f (F : ℝ) (x : State N) :
    ⟪(lorenz96Galerkin (N := N) F).f, x⟫_ℝ = F * ∑ i : Fin N, x i := by
  have hf : (lorenz96Galerkin (N := N) F).f = WithLp.toLp 2 (fun _ => F) := rfl
  rw [hf, PiLp.inner_apply]
  simp_rw [RCLike.inner_apply, conj_trivial]
  rw [Finset.mul_sum]
  exact Finset.sum_congr rfl fun i _ => mul_comm _ _

/-- **向量场能量内积恒等式**（本件接缝核心）：
⟪vf x, x⟫ = −‖x‖² + F·Σᵢ xᵢ。对流项由 M1 对角相消 `inner_cyclicB_self`
（hskew 槽位，经 `GalerkinNS.inner_vf`）严格抵消；−‖x‖² 来自 ν = 1、
A = id（hA 饱和取等）；forcing 项即 `inner_lorenz96_f` 展开。 -/
theorem inner_lorenz96_vf (F : ℝ) (x : State N) :
    ⟪(lorenz96Galerkin (N := N) F).vf x, x⟫_ℝ = -‖x‖ ^ 2 + F * ∑ i : Fin N, x i := by
  rw [GalerkinNS.inner_vf]
  have hν : (lorenz96Galerkin (N := N) F).ν = 1 := rfl
  have hA : (lorenz96Galerkin (N := N) F).A = .id ℝ _ := rfl
  rw [hν, hA, ContinuousLinearMap.id_apply, real_inner_self_eq_norm_sq, inner_lorenz96_f]
  ring

/-! ### 二、Cauchy–Schwarz forcing 上界 -/

/-- **Cauchy–Schwarz 上界**（定式表 v0 §2.5，S2 式(38) 第二行）：
F·Σᵢ xᵢ = ⟪f, x⟫ ≤ ‖f‖·‖x‖ = R·‖x‖（R = |F|·√N）。 -/
theorem forcing_sum_le (F : ℝ) (x : State N) :
    F * ∑ i : Fin N, x i ≤ absorbingRadius N F * ‖x‖ := by
  rw [← inner_lorenz96_f F x, ← norm_lorenz96_f F]
  exact real_inner_le_norm _ _

/-! ### 三、吸收球假设束（房屋风格同 CondUniqueness.Q6DifferenceBundle） -/

/-- **Lorenz-96 吸收球假设束**：全局时间轨道及其正则性/方程关系打包。
字段即假设清单（逐字 = 字段名）：
* `F`：常值强迫强度；`u`：全局轨道 ℝ → State N；
* `hcont`：轨道连续性；
* `hderiv`：处处可微且导数等于 Lorenz-96 向量场（`lorenz96Galerkin`
  实例右端，`HasDerivAt` 全局域——limsup 渐近陈述所需）。
全局强解存在性不在本件范围，由假设位承担（文件头残余开口登记）。 -/
structure LorenzAbsorbingBundle (N : ℕ) [NeZero N] where
  /-- 常值强迫强度。 -/
  F : ℝ
  /-- 全局时间轨道。 -/
  u : ℝ → State N
  /-- 轨道连续性。 -/
  hcont : Continuous u
  /-- 处处可微，导数等于 Lorenz-96 向量场右端（GalerkinNS 实例 vf）。 -/
  hderiv : ∀ t : ℝ, HasDerivAt u ((lorenz96Galerkin (N := N) F).vf (u t)) t

namespace LorenzAbsorbingBundle

variable (B : LorenzAbsorbingBundle N)

/-- **能量恒等式**（使命条 2）：d/dt(½‖u‖²) = −‖u‖² + F·Σᵢ uᵢ。
逐项来源：非线性项零和 = `inner_cyclicB_self`（经 hskew 入
`GalerkinNS.inner_vf`）；耗散 −‖u‖² = ν=1/A=id；forcing = F·Σᵢ uᵢ。 -/
theorem hasDerivAt_energy (t : ℝ) :
    HasDerivAt (fun s => (1 / 2) * ‖B.u s‖ ^ 2)
      (-‖B.u t‖ ^ 2 + B.F * ∑ i : Fin N, B.u t i) t := by
  have h := (B.hderiv t).norm_sq.const_mul (1 / 2)
  have hval : (1 / 2) * (2 * ⟪B.u t, (lorenz96Galerkin (N := N) B.F).vf (B.u t)⟫_ℝ) =
      -‖B.u t‖ ^ 2 + B.F * ∑ i : Fin N, B.u t i := by
    rw [real_inner_comm, inner_lorenz96_vf]
    ring
  rwa [hval] at h

/-- 右斜率 liminf 接口供给件：能量函数处处 HasDerivAt ⇒ Grönwall E6 件
所需的 frequently 右斜率界（slope 收敛到导数，严格界在右侧邻域频繁成立）。 -/
theorem frequently_slope_energy_lt {t r : ℝ}
    (hr : 2 * ⟪B.u t, (lorenz96Galerkin (N := N) B.F).vf (B.u t)⟫_ℝ < r) :
    ∃ᶠ z in 𝓝[>] t, (z - t)⁻¹ * (‖B.u z‖ ^ 2 - ‖B.u t‖ ^ 2) < r := by
  have hd := (B.hderiv t).norm_sq
  have htl := (hasDerivAt_iff_tendsto_slope_left_right.mp hd).2
  have h1 : ∀ᶠ z in 𝓝[>] t, slope (fun x => ‖B.u x‖ ^ 2) t z ∈ Iio r :=
    htl (Iio_mem_nhds hr)
  apply Filter.Eventually.frequently
  refine Filter.Eventually.mono h1 fun z hz => ?_
  simp only [slope, smul_eq_mul, Set.mem_Iio] at hz
  exact hz

/-- **吸收界（使命条 4，平方能量版）**：t ∈ [0, T] 上
‖u t‖² ≤ ‖u 0‖²·e^(−t) + R²·(1 − e^(−t))，R = |F|·√N。
证明链：能量导数 dw = 2⟪u, vf u⟫ = −2‖u‖² + 2F·Σᵢ uᵢ（能量恒等式）
≤ −2‖u‖² + 2R‖u‖（Cauchy–Schwarz）≤ −‖u‖² + R²（2ab ≤ a² + b²），
K = −1、ε = R² 消费 mathlib E6 件
`le_gronwallBound_of_liminf_deriv_right_le`，gronwallBound 展开
δ·e^(−t) + ε·(1 − e^(−t))。 -/
theorem norm_sq_le_absorbing {T : ℝ} (hT : 0 ≤ T) :
    ∀ t ∈ Icc 0 T, ‖B.u t‖ ^ 2 ≤
      ‖B.u 0‖ ^ 2 * Real.exp (-t) + (absorbingRadius N B.F) ^ 2 * (1 - Real.exp (-t)) := by
  have hcont : ContinuousOn (fun s => ‖B.u s‖ ^ 2) (Icc 0 T) :=
    (B.hcont.norm.pow 2).continuousOn
  have hlim : ∀ s ∈ Ico 0 T, ∀ r : ℝ,
      2 * ⟪B.u s, (lorenz96Galerkin (N := N) B.F).vf (B.u s)⟫_ℝ < r →
      ∃ᶠ z in 𝓝[>] s, (z - s)⁻¹ * (‖B.u z‖ ^ 2 - ‖B.u s‖ ^ 2) < r :=
    fun s _ r hr => B.frequently_slope_energy_lt hr
  have ha : ‖B.u 0‖ ^ 2 ≤ ‖B.u 0‖ ^ 2 := le_refl _
  have hbound : ∀ s ∈ Ico 0 T,
      2 * ⟪B.u s, (lorenz96Galerkin (N := N) B.F).vf (B.u s)⟫_ℝ ≤
        -1 * ‖B.u s‖ ^ 2 + (absorbingRadius N B.F) ^ 2 := by
    intro s _
    have hcom : ⟪B.u s, (lorenz96Galerkin (N := N) B.F).vf (B.u s)⟫_ℝ =
        ⟪(lorenz96Galerkin (N := N) B.F).vf (B.u s), B.u s⟫_ℝ := real_inner_comm _ _
    have hcs := forcing_sum_le B.F (B.u s)
    rw [hcom, inner_lorenz96_vf]
    have hsq := sq_nonneg (‖B.u s‖ - absorbingRadius N B.F)
    have hnn := norm_nonneg (B.u s)
    nlinarith [hcs, hsq, hnn]
  intro t ht
  have hG := le_gronwallBound_of_liminf_deriv_right_le hcont hlim ha hbound t ht
  simp only [gronwallBound_of_K_ne_0 (show (-1 : ℝ) ≠ 0 by norm_num), sub_zero,
    neg_one_mul] at hG
  have hfin : (absorbingRadius N B.F) ^ 2 / -1 * (Real.exp (-t) - 1) =
      (absorbingRadius N B.F) ^ 2 * (1 - Real.exp (-t)) := by ring
  rwa [hfin] at hG

/-- **最终包络（事件形）**：∀ ε > 0，t 充分大时 ‖u t‖² ≤ R² + ε
（吸收界 + e^(−t) → 0；limsup 陈述的直接供给件）。 -/
theorem eventually_norm_sq_le (ε : ℝ) (hε : 0 < ε) :
    ∀ᶠ t in atTop, ‖B.u t‖ ^ 2 ≤ (absorbingRadius N B.F) ^ 2 + ε := by
  have h0 : Tendsto (fun t : ℝ => ‖B.u 0‖ ^ 2 * Real.exp (-t)) atTop (𝓝 0) := by
    have h := Real.tendsto_exp_neg_atTop_nhds_zero.const_mul (‖B.u 0‖ ^ 2)
    rwa [mul_zero] at h
  have hexp1 : ∀ t : ℝ, 0 ≤ t → Real.exp (-t) ≤ 1 :=
    fun t ht => Real.exp_le_one_iff.mpr (neg_nonpos.mpr ht)
  refine ((eventually_ge_atTop 0).and (h0 (Iio_mem_nhds hε))).mono fun t ⟨ht0, htε⟩ => ?_
  have hb := B.norm_sq_le_absorbing (T := t) ht0 t (right_mem_Icc.mpr ht0)
  have h2 : (absorbingRadius N B.F) ^ 2 * (1 - Real.exp (-t)) ≤
      (absorbingRadius N B.F) ^ 2 := by
    have h := mul_le_mul_of_nonneg_left (sub_le_self 1 (Real.exp_nonneg (-t)))
      (sq_nonneg (absorbingRadius N B.F))
    rwa [mul_one] at h
  have htε' := Set.mem_Iio.mp htε
  have hexp1t := hexp1 t ht0
  have hE0nn : 0 ≤ ‖B.u 0‖ ^ 2 := sq_nonneg _
  linarith

/-- **limsup 陈述（使命条 5，平方形）**：limsup_{t→+∞} ‖u t‖² ≤ R²。 -/
theorem limsup_norm_sq_le :
    limsup (fun t => ‖B.u t‖ ^ 2) atTop ≤ (absorbingRadius N B.F) ^ 2 := by
  have hcob : IsCoboundedUnder (· ≤ ·) atTop (fun t => ‖B.u t‖ ^ 2) := by
    refine ⟨0, fun a ha => ?_⟩
    rw [eventually_map] at ha
    exact eventually_const.mp
      (((Filter.Eventually.of_forall fun t => sq_nonneg (‖B.u t‖))).and ha |>.mono
        fun t ⟨h1, h2⟩ => le_trans h1 h2)
  exact le_of_forall_pos_le_add fun ε hε => limsup_le_of_le hcob (B.eventually_norm_sq_le ε hε)

/-- **limsup 陈述（使命条 5，范数形，主结论）**：
limsup_{t→+∞} ‖u t‖ ≤ |F|·√N = R（吸收球半径，定式表 v0 §2.5，
S2 Prop 7 一手钉）。口径：范数渐近上界，非吸引子刻画（R2 语言钉）。 -/
theorem limsup_norm_le :
    limsup (fun t => ‖B.u t‖) atTop ≤ absorbingRadius N B.F := by
  have hRnn : 0 ≤ absorbingRadius N B.F :=
    mul_nonneg (abs_nonneg _) (Real.sqrt_nonneg _)
  have hcob : IsCoboundedUnder (· ≤ ·) atTop (fun t => ‖B.u t‖) := by
    refine ⟨0, fun a ha => ?_⟩
    rw [eventually_map] at ha
    exact eventually_const.mp
      (((Filter.Eventually.of_forall fun t => norm_nonneg (B.u t))).and ha |>.mono
        fun t ⟨h1, h2⟩ => le_trans h1 h2)
  refine le_of_forall_pos_le_add fun ε hε => limsup_le_of_le hcob ?_
  have hδ : (0 : ℝ) < 2 * absorbingRadius N B.F * ε + ε ^ 2 :=
    add_pos_of_nonneg_of_pos
      (mul_nonneg (mul_nonneg (by norm_num) hRnn) (le_of_lt hε)) (pow_pos hε 2)
  refine (B.eventually_norm_sq_le _ hδ).mono fun t ht => ?_
  have hrw : (absorbingRadius N B.F) ^ 2 + (2 * absorbingRadius N B.F * ε + ε ^ 2) =
      (absorbingRadius N B.F + ε) ^ 2 := by ring
  rw [hrw] at ht
  have habs := abs_le_of_sq_le_sq ht (add_nonneg hRnn (le_of_lt hε))
  rwa [abs_of_nonneg (norm_nonneg _)] at habs

end LorenzAbsorbingBundle

/-- **N = 36、F = 8 数值对拍**（使命条 5 推论，M0 定式表 §2.5
R = √N·|F| = 48 的机器自算复现）：|8|·√36 = 8·6 = 48。 -/
theorem absorbingRadius_36_8 : absorbingRadius 36 8 = 48 := by
  have h6 : Real.sqrt ((36 : ℕ) : ℝ) = 6 := by
    rw [show ((36 : ℕ) : ℝ) = 6 ^ 2 by norm_num]
    exact Real.sqrt_sq (by norm_num)
  unfold absorbingRadius
  rw [h6]
  norm_num

/-- **M2 (b-i) 主结论（典范参数 (N, F) = (36, 8)）**：任意满足
`LorenzAbsorbingBundle` 假设束的轨道 limsup_{t→+∞} ‖u t‖ ≤ 48
（吸收球半径 R = √36·|8| = 48，与 M0 表数值对拍一致）。 -/
theorem limsup_norm_le_48 (B : LorenzAbsorbingBundle 36) (hF : B.F = 8) :
    limsup (fun t => ‖B.u t‖) atTop ≤ 48 := by
  have h := B.limsup_norm_le
  rw [hF, absorbingRadius_36_8] at h
  exact h

/-! ### 四、公理审计（构建期打印；白名单 propext / Classical.choice / Quot.sound） -/
#print axioms norm_lorenz96_f
#print axioms inner_lorenz96_f
#print axioms inner_lorenz96_vf
#print axioms forcing_sum_le
#print axioms LorenzAbsorbingBundle.hasDerivAt_energy
#print axioms LorenzAbsorbingBundle.norm_sq_le_absorbing
#print axioms LorenzAbsorbingBundle.limsup_norm_sq_le
#print axioms LorenzAbsorbingBundle.limsup_norm_le
#print axioms absorbingRadius_36_8
#print axioms limsup_norm_le_48

/-!
## Ledger（M2 路线裁决 G3 对应登记）

* **对应**：本件 = LORENZ96-M2-ROUTE-RULING-01 §2.2 G3 主路线选项 (iii)
  之 (b-i)「吸收球 trapping 解析/kernel 层」主证（章程 §2.3-ERRATA-01 条1
  分层捕获声明的 kernel 可 Lean 化层）。定理钉：
  `LorenzAbsorbingBundle.norm_sq_le_absorbing`（逐时吸收界）、
  `LorenzAbsorbingBundle.limsup_norm_le`（limsup ≤ R）、
  `limsup_norm_le_48`（典范参数 48，M0 定式表 §2.5 数值对拍）。
  语言钉适配（ERRATA 条2）：本件达成后 (b-i) 改记「kernel 层已证
  （定理钉+公理审计）」；层级不升格、禁吸引子刻画/轨道包络表述。
* **复用存量**：对角相消 `inner_cyclicB_self`（Lorenz96.lean L228，
  M1 T2 已证）经 `GalerkinNS.inner_vf`/hskew 槽位进入能量链；
  既有 `lorenz96_inner_vf_le`（不等式版）在本件被等式版
  `inner_lorenz96_vf` 强化（接缝闭合，强度提升：≤ → =）。
* **残余开口**：
  1. 全局强解存在性不在本件范围，由 bundle 假设位 `hderiv`/`hcont` 承担；
     M1 截断区间存在性 `lorenz96_exists_solution_upto` 在案，全局流拼接
     登记于 Lorenz96.lean §四 L34b（CONDITIONAL-PASS，义务指针沿用）。
  2. 逐时界为平方能量版；范数版逐时界（√E 奇异点处理）未形式化，
     limsup 语义不受影响（平方版已蕴含 limsup‖u‖ ≤ R，本件已证）。
  3. (b-ii) 数值包络见证层、球面正控严格区间证书（G1/G2）另件承接，
     不在本文件范围（路线裁决 §五排期在案）。
* **口径**：E9 有限维 ODE 截断层；零 sorry；公理白名单三件套；
  不升格 NS 包任何档位。
-/

end Lorenz96

end NSGalerkin
