-- CLASSIFY: L1
/-
WS-B 降级档 · D-B1 · 周期 Ladyzhenskaya 不等式：𝕋² Fourier 直证骨架
（EXT-WAVE-18 续执行批 · 枢/PIVOT-01 体系 L1 攻坚席 · 全程中文注释）

【纪律声明】2D（周期域）Ladyzhenskaya 不等式
  ‖u‖²_{L⁴(𝕋²)} ≤ C_L·‖u‖_{L²(𝕋²)}·‖∇u‖_{L²(𝕋²)}
是 Lions–Magenes 体系的经典已知结果（2D 弱解唯一性同为经典已知）；
本文件是其 Lean 4 + mathlib **形式化工程**的 Fourier 直证骨架，
不构成、不暗示任何数学新证。本骨架任何部分不得被表述为「唯一性已证」。

【路线】（FGL-SEAM-SPEC-01 单元② Q1 + §6 注记 2 的周期域绕行：
免零延拓，走环面自身 Fourier 路线）以 mathlib 多环面 Fourier 底座
`UnitAddTorus.mFourier/mFourierLp`（E2 在案）+ Cauchy–Schwarz 直证。
证明主干四块（均为完整证明，宁少勿洞）：

  (i)   卷积组合核（ℓ¹⋆ℓ²→ℓ² Young，Cauchy–Schwarz）
        —— `convC` / `sum_norm_sq_convC_le`；
  (ii)  L⁴ → 卷积（Parseval 第一步）：
        `∫‖u‖⁴ = Σ_n‖(c⋆c)_n‖²` —— `integral_norm_pow_four_fourierPoly`；
  (iii) Bernstein 中间估计：`∫‖u‖⁴ ≤ (Σ‖c‖)²·(Σ‖c‖²)`
        —— `integral_norm_pow_four_le`；
  (iv)  梯度侧谱能量 + 零均值 Poincaré（Parseval 级）
        —— `specGradEnergy` / `sum_norm_sq_le_specGradEnergy`。

【已完/未完对照（D-B2 续攻坚后登记，诚实标注）】

已完（证毕，零 sorry）：
  (v)  微分链接件 `∂ᵢ(mFourier k) = 2πi·kᵢ·mFourier k`
       —— `hasDerivAt_mFourier_coord`（单模）/ `hasDerivAt_fourierPoly_coord`
       （多项式整体）；谱坐标 H¹ 结构闭合：
       `specGradEnergy_eq_integral_pderiv`
       （梯度 L² 能量 = 谱能量，经 `integral_norm_sq_sum_mFourier` 一般
       Parseval 与 `integral_norm_sq_pderivPoly`）；零均值积分型 Poincaré
       `integral_norm_sq_le_integral_pderiv`。本件为「有限维 ODE 截断层」
       谱坐标梯度恒等式的分析锚点（C1 口径：全部结论位于有限维
       Fourier 截断多项式层，不断言任何无限维 Sobolev 空间命题）。
  (vi) 1D 周期 Ladyzhenskaya 全证（UnitAddCircle 三角多项式层）：
       零均值显式常数 `C = 1/12` —— `ladyzhenskaya_oneD`
       （`∫‖u‖⁴ ≤ (1/12)·(∫‖u‖²)·(∫‖∂u‖²)`）与 H¹ 收边
       `ladyzhenskaya_oneD_h1`；免均值一般形式 `ladyzhenskaya_oneD_general`
       （常数 `1 + π²/3`）。分析核心：巴塞尔截断 `sum_inv_sq_le`
       （`Σ_{k≠0}k⁻² ≤ π²/3`）+ 零均值加权 Cauchy–Schwarz
       `sum_norm_sq_mul_sqKey`；零均值条件以显式假设 `c 0 = 0` 携带。

已完（续，EXT-WAVE-18 cont.3 · L5 席批三）：
  (vii) 2D 周期 Ladyzhenskaya 主不等式（可乘型各向异性切片路线，证毕，
       详见 TwoDim 节头注；𝕋² 取乘积形式 UnitAddCircle × UnitAddCircle，
       测度 `torus2Measure = circleMeasure.prod circleMeasure`）：
       点态可乘型切片嵌入 `norm_sq_fourierPoly2_le_sliceY/sliceX`
       （1D 阈值加权 CS `sum_norm_sq_le_weighted` 逐片化，常数 1+π²/3）
       ⇒ 点态主界 `norm_pow_four_fourierPoly2_le`（‖u‖⁴ ≤ (1+π²/3)²·P₂(x)P₁(y)）
       ⇒ 乘积测度分离 `integral_prod_mul` + 注入指标 1D Parseval
       `integral_norm_sq_sum_fourier_injOn` 收拢
       ⇒ 可乘张量因子形 `ladyzhenskaya_twoD_tensor`（谱坐标，显式常数
       (1+π²/3)²）、H¹ 收边积分形 `ladyzhenskaya_twoD` 与平方收边
       `ladyzhenskaya_twoD_h1_sq`（免均值）、零均值梯度平方形
       `ladyzhenskaya_twoD_zero_mean`（显式常数 (1+π²/3)²/(4π⁴)）。
       乘积侧 Parseval/Poincaré 镜像件：
       `integral_norm_sq_fourierPoly2` / `integral_norm_sq_pderivPoly2` /
       `integral_norm_sq_le_integral_pderiv2`。

未完（残口登记，诚实标注）：主陈述登记件 `periodicLadyzhenskayaStatement`
的纯可乘形 `∫‖u‖⁴ ≤ C·(∫‖u‖²)·(specGradEnergy)`（C·X·Y 形）本批仍未断开：
切片路线在片侧使用 Agmon 阈值界（高频端损失 1/|k|² 阶；张量积反例
u = f(x)·g(y) 双高频显示乘积形上界 K(X+b₀²)(X+b₁²) 不被 C·X·(X+b²)
一致控制——混合频率平方增长在案），断开 C·X·Y 形需片内保留支集结构的
精细逐模求和（Σ_{m∈supp}(λ²+m²)⁻¹ 而非全 ℤ 闭式界）或等价机制，
留待后续批次。2D 朴素谱线 `Σ|k|⁻²` 对数发散（可加型死路，判词保留）；
本批路线为可乘型（张量权 (1+k₀²)(1+k₁²) 的倒数和收敛，值 (1+π²/3)²）。
按 CapAnchor 先例，主陈述 Prop 级定义维持登记、不断言证明。
全文件零 sorry、零新增 axiom（仅 propext/Classical.choice/Quot.sound 三件套）。

版本钉：leanprover/lean4:v4.35.0 + mathlib v4.35.0（@56a00585）。
-/
import Mathlib.Analysis.Fourier.AddCircleMulti
import Mathlib.NumberTheory.ZetaValues

open Finset UnitAddTorus MeasureTheory
open scoped ComplexConjugate InnerProductSpace

noncomputable section

namespace NSGalerkin

namespace Ladyzhenskaya

/-- 波数指标：𝕋² 的 Fourier 模由 `Fin 2 → ℤ` 标记。 -/
abbrev WaveIdx : Type := Fin 2 → ℤ

/-- 波数平方（梯度侧的 Fourier 权）：`|k|² = k₀² + k₁²`（实数形式）。 -/
def kSq (k : WaveIdx) : ℝ := (k 0 : ℝ) ^ 2 + (k 1 : ℝ) ^ 2

/-- 测度钉：`UnitAddTorus (Fin 2)` 上的归一化 Haar 测度，
取与 `UnitAddTorus.mFourierLp` 定义处（`AddCircleMulti` 局部实例）
**逐字相同**的 `MeasureSpace` 实例（逐因子 `AddCircle.haarAddCircle` 的
pi 积）。`UnitAddCircle` 上存在双 `MeasureSpace` 实例
（`Periodic` 归一化 vs 该局部实例），统一使用本钉规避实例钻石；
全文件所有积分/对 Lp 的引用一律走 `torusMeasure`。 -/
abbrev torusMeasure : Measure (UnitAddTorus (Fin 2)) :=
  @volume _ (@MeasureSpace.pi (Fin 2) (Fin.fintype 2) (fun _ => UnitAddCircle)
    (fun _ => ⟨AddCircle.haarAddCircle⟩))

/-- `torusMeasure` 是概率测度（逐因子 `haarAddCircle` 概率测度的 pi 积；
实例参数展开后由 mathlib 的 pi 概率实例供给）。 -/
instance : IsProbabilityMeasure torusMeasure :=
  inferInstanceAs (IsProbabilityMeasure
    (Measure.pi fun _ : Fin 2 => AddCircle.haarAddCircle))

section ConvolutionKernel
/-! ### (i) 卷积组合核：ℓ¹⋆ℓ²→ℓ² Young（纯有限组合学，与环面无关） -/

variable {ι : Type*} [AddCommGroup ι] [DecidableEq ι]

/-- 截断卷积：`(convC c d) n = ∑ k ∈ c.support, c k · d (n − k)`。
三角多项式乘积的第 `n` 个 Fourier 系数的组合核。 -/
def convC (c d : ι →₀ ℂ) (n : ι) : ℂ := ∑ k ∈ c.support, c k * d (n - k)

/-- **卷积 Young 不等式（ℓ¹⋆ℓ²→ℓ²，Cauchy–Schwarz 组合核）**：
`Σ_n ‖(c⋆d)_n‖² ≤ (Σ‖c‖)²·(Σ‖d‖²)`（在卷积支集 `s + t` 上求和，
支集外卷积为零，求和范围无损失）。这是周期 Ladyzhenskaya Fourier
直证「L⁴ → 卷积 → 逐模估计」链条的第二步。 -/
theorem sum_norm_sq_convC_le (c d : ι →₀ ℂ) :
    ∑ n ∈ c.support.image₂ (· + ·) d.support, ‖convC c d n‖ ^ 2 ≤
      (∑ k ∈ c.support, ‖c k‖) ^ 2 * (∑ l ∈ d.support, ‖d l‖ ^ 2) := by
  classical
  set s := c.support with hs
  set t := d.support with ht
  set S := s.image₂ (· + ·) t with hS
  -- 逐点：范数 ≤ 绝对值卷积
  have hpt : ∀ n : ι, ‖convC c d n‖ ≤ ∑ k ∈ s, ‖c k‖ * ‖d (n - k)‖ := by
    intro n
    calc ‖convC c d n‖ ≤ ∑ k ∈ s, ‖c k * d (n - k)‖ := norm_sum_le _ _
      _ = ∑ k ∈ s, ‖c k‖ * ‖d (n - k)‖ := sum_congr rfl fun k _ => norm_mul _ _
  -- 逐对 Cauchy–Schwarz（平方形式，免开方）
  have hpair : ∀ k j : ι,
      ∑ n ∈ S, ‖d (n - k)‖ * ‖d (n - j)‖ ≤ ∑ l ∈ t, ‖d l‖ ^ 2 := by
    intro k j
    have hCS : (∑ n ∈ S, ‖d (n - k)‖ * ‖d (n - j)‖) ^ 2 ≤
        (∑ n ∈ S, ‖d (n - k)‖ ^ 2) * (∑ n ∈ S, ‖d (n - j)‖ ^ 2) :=
      sum_mul_sq_le_sq_mul_sq _ _ _
    -- 重排：固定 m，n ↦ n − m 单射；像集外项由 d 的支集外为零吸收
    have hre : ∀ m : ι, ∑ n ∈ S, ‖d (n - m)‖ ^ 2 ≤ ∑ l ∈ t, ‖d l‖ ^ 2 := by
      intro m
      have hinj : Function.Injective (fun n : ι => n - m) := fun a b h => by
        have h' : a - m = b - m := h
        rwa [sub_eq_iff_eq_add, sub_add_cancel] at h'
      have hmap : ∑ n ∈ S, ‖d (n - m)‖ ^ 2 =
          ∑ x ∈ S.map ⟨fun n => n - m, hinj⟩, ‖d x‖ ^ 2 :=
        (Finset.sum_map S ⟨fun n => n - m, hinj⟩ (fun x => ‖d x‖ ^ 2)).symm
      rw [hmap]
      calc ∑ x ∈ S.map ⟨fun n => n - m, hinj⟩, ‖d x‖ ^ 2
          ≤ ∑ x ∈ t ∪ S.map ⟨fun n => n - m, hinj⟩, ‖d x‖ ^ 2 :=
            sum_le_sum_of_subset_of_nonneg subset_union_right
              fun x _ _ => sq_nonneg _
        _ = ∑ x ∈ t, ‖d x‖ ^ 2 := by
            apply Eq.symm
            apply sum_subset subset_union_left
            intro x _ hx
            rw [Finsupp.notMem_support_iff] at hx
            simp [hx]
    have hP0 : 0 ≤ ∑ n ∈ S, ‖d (n - k)‖ * ‖d (n - j)‖ :=
      sum_nonneg fun n _ => mul_nonneg (norm_nonneg _) (norm_nonneg _)
    have hQ0 : 0 ≤ ∑ l ∈ t, ‖d l‖ ^ 2 := sum_nonneg fun l _ => sq_nonneg _
    have hk0 : 0 ≤ ∑ n ∈ S, ‖d (n - k)‖ ^ 2 := sum_nonneg fun n _ => sq_nonneg _
    have hj0 : 0 ≤ ∑ n ∈ S, ‖d (n - j)‖ ^ 2 := sum_nonneg fun n _ => sq_nonneg _
    nlinarith [hCS, hre k, hre j, hP0, hQ0, hk0, hj0]
  -- 主链：平方展开 → 三重和重排 → 逐对估计 → 因子化
  calc ∑ n ∈ S, ‖convC c d n‖ ^ 2
      ≤ ∑ n ∈ S, (∑ k ∈ s, ‖c k‖ * ‖d (n - k)‖) ^ 2 := by
        exact sum_le_sum fun n _ =>
          pow_le_pow_left₀ (norm_nonneg _) (hpt n) 2
    _ = ∑ n ∈ S, ∑ k ∈ s, ∑ j ∈ s,
          (‖c k‖ * ‖d (n - k)‖) * (‖c j‖ * ‖d (n - j)‖) := by
        apply sum_congr rfl; intro n _
        rw [pow_two, sum_mul_sum]
    _ = ∑ k ∈ s, ∑ j ∈ s,
          (‖c k‖ * ‖c j‖) * ∑ n ∈ S, ‖d (n - k)‖ * ‖d (n - j)‖ := by
        rw [sum_comm]
        apply sum_congr rfl; intro k _
        rw [sum_comm]
        apply sum_congr rfl; intro j _
        rw [mul_sum]
        apply sum_congr rfl; intro n _
        ring
    _ ≤ ∑ k ∈ s, ∑ j ∈ s, (‖c k‖ * ‖c j‖) * (∑ l ∈ t, ‖d l‖ ^ 2) := by
        exact sum_le_sum fun k _ => sum_le_sum fun j _ =>
          mul_le_mul_of_nonneg_left (hpair k j)
            (mul_nonneg (norm_nonneg _) (norm_nonneg _))
    _ = (∑ k ∈ s, ‖c k‖) ^ 2 * (∑ l ∈ t, ‖d l‖ ^ 2) := by
        rw [pow_two, sum_mul_sum, sum_mul]
        apply sum_congr rfl; intro k _
        rw [sum_mul]

end ConvolutionKernel

section TorusParseval
/-! ### (ii)(iii) 环面 Parseval 底座：L⁴ → 卷积 → Bernstein 中间估计 -/

/-- 有限 Fourier 多项式（周期三角多项式）：`x ↦ Σ_k c_k·mFourier k x`。 -/
def fourierPoly (c : WaveIdx →₀ ℂ) (x : UnitAddTorus (Fin 2)) : ℂ :=
  ∑ k ∈ c.support, c k * mFourier k x

/-- 有限 Fourier 多项式作为连续映射。 -/
def fourierPolyC (c : WaveIdx →₀ ℂ) : C(UnitAddTorus (Fin 2), ℂ) where
  toFun := fourierPoly c
  continuous_toFun := continuous_finsetSum _ fun k _ =>
    continuous_const.mul (mFourier k).continuous

/-- 连续映射版本与点值版本一致。 -/
theorem fourierPolyC_apply (c : WaveIdx →₀ ℂ) (x : UnitAddTorus (Fin 2)) :
    fourierPolyC c x = fourierPoly c x := rfl

/-- **三角多项式乘法 = 系数卷积**（`mFourier` 加性的直接推论；
纤维重排 `sum_fiberwise_of_maps_to` 一次到位）。 -/
theorem fourierPoly_mul (c d : WaveIdx →₀ ℂ) (x : UnitAddTorus (Fin 2)) :
    fourierPoly c x * fourierPoly d x =
      ∑ n ∈ c.support.image₂ (· + ·) d.support, convC c d n * mFourier n x := by
  classical
  set s := c.support with hs
  set t := d.support with ht
  have h1 : fourierPoly c x * fourierPoly d x =
      ∑ p ∈ s ×ˢ t, (c p.1 * d p.2) * mFourier (p.1 + p.2) x := by
    rw [fourierPoly, fourierPoly, sum_mul_sum, sum_product]
    apply sum_congr rfl; intro k _
    apply sum_congr rfl; intro l _
    rw [mFourier_add]; ring
  rw [h1, ← sum_fiberwise_of_maps_to (g := fun p : WaveIdx × WaveIdx => p.1 + p.2)
    (t := c.support.image₂ (· + ·) d.support)
    (f := fun p : WaveIdx × WaveIdx => (c p.1 * d p.2) * mFourier (p.1 + p.2) x)
    (fun p hp =>
      mem_image₂.mpr ⟨p.1, (mem_product.mp hp).1, p.2, (mem_product.mp hp).2, rfl⟩)]
  apply sum_congr rfl; intro n _
  -- 纤维上 p.1 + p.2 = n：先把 mFourier 指标化约到 n
  have hconv : ∀ p ∈ (s ×ˢ t).filter (fun p => p.1 + p.2 = n),
      (c p.1 * d p.2) * mFourier (p.1 + p.2) x = (c p.1 * d p.2) * mFourier n x := by
    intro p hp
    rw [mem_filter] at hp
    rw [hp.2]
  rw [sum_congr rfl hconv, ← sum_mul]
  congr 1
  -- 纤维和展开（双射 p ↦ p.1，逆 k ↦ (k, n − k)）
  have hfb : ∑ p ∈ (s ×ˢ t).filter (fun p => p.1 + p.2 = n), c p.1 * d p.2 =
      ∑ k ∈ s.filter (fun k => n - k ∈ t), c k * d (n - k) := by
    apply sum_bij (fun p _ => p.1)
    · intro p hp
      rw [mem_filter, mem_product] at hp
      rw [mem_filter]
      refine ⟨hp.1.1, ?_⟩
      have h2 : p.2 = n - p.1 := by rw [← hp.2]; abel
      rw [← h2]; exact hp.1.2
    · intro p hp q hq h
      rw [mem_filter] at hp hq
      obtain ⟨h₁, h₂⟩ := p
      obtain ⟨h₃, h₄⟩ := q
      simp only at h
      have e1 : h₂ = n - h₁ := by rw [← hp.2]; abel
      have e2 : h₄ = n - h₃ := by rw [← hq.2]; abel
      simp only [Prod.mk.injEq]
      exact ⟨h, by rw [e1, e2, h]⟩
    · intro k hk
      rw [mem_filter] at hk
      exact ⟨(k, n - k), by
        rw [mem_filter, mem_product]
        exact ⟨⟨hk.1, hk.2⟩, by ring⟩, rfl⟩
    · intro p hp
      rw [mem_filter] at hp
      have h2 : p.2 = n - p.1 := by rw [← hp.2]; abel
      rw [h2]
  rw [hfb]
  -- 把 filter 和扩到全 s：支集外 d 为零
  show ∑ k ∈ s.filter (fun k => n - k ∈ t), c k * d (n - k) =
    ∑ k ∈ c.support, c k * d (n - k)
  apply sum_filter_of_ne
  intro k _ hne
  by_contra hnt
  rw [Finsupp.notMem_support_iff] at hnt
  rw [hnt, mul_zero] at hne
  exact hne rfl

/-- **L⁴ → 卷积（Parseval 第一步）**：对有限 Fourier 多项式 `u = fourierPoly c`，
`∫‖u‖⁴ = Σ_n‖(c⋆c)_n‖²`（求和取卷积支集 `support + support`）。
证明链：`‖u‖⁴ = ‖u²‖²`（范数幂）、`u²` 的系数是卷积（`fourierPoly_mul`）、
`ContinuousMap.inner_toLp` + `orthonormal_mFourier`（正交性 Parseval）。 -/
theorem integral_norm_pow_four_fourierPoly (c : WaveIdx →₀ ℂ) :
    ∫ x : UnitAddTorus (Fin 2), ‖fourierPoly c x‖ ^ 4 ∂torusMeasure =
      ∑ n ∈ c.support.image₂ (· + ·) c.support, ‖convC c c n‖ ^ 2 := by
  classical
  set s := c.support with hs
  set S := s.image₂ (· + ·) s with hS
  set g : C(UnitAddTorus (Fin 2), ℂ) := ∑ n ∈ S, convC c c n • mFourier n with hg
  have hgx : ∀ x : UnitAddTorus (Fin 2), g x = (fourierPoly c x) ^ 2 := by
    intro x
    rw [pow_two, fourierPoly_mul]
    simp only [hg, ContinuousMap.coe_sum, ContinuousMap.coe_smul, Finset.sum_apply,
      Pi.smul_apply, smul_eq_mul]
    rw [hS, hs]
  -- L² 内积展开（ContinuousMap.inner_toLp；其被积函数次序为 `g · conj f`）
  have hinner : ⟪ContinuousMap.toLp 2 torusMeasure ℂ g,
        ContinuousMap.toLp 2 torusMeasure ℂ g⟫_ℂ =
      ∫ x : UnitAddTorus (Fin 2), g x * conj (g x) ∂torusMeasure :=
    ContinuousMap.inner_toLp _ _ _
  have hgLp : ContinuousMap.toLp 2 torusMeasure ℂ g =
      ∑ n ∈ S, convC c c n • mFourierLp (d := Fin 2) 2 n := by
    rw [hg, map_sum]
    exact sum_congr rfl fun n _ => map_smul _ _ _
  -- 正交性 Parseval（复内积形式）
  have hParseval : ⟪∑ n ∈ S, convC c c n • mFourierLp (d := Fin 2) 2 n,
        ∑ n ∈ S, convC c c n • mFourierLp (d := Fin 2) 2 n⟫_ℂ =
      ∑ n ∈ S, conj (convC c c n) * convC c c n :=
    orthonormal_mFourier.inner_sum _ _ _
  -- 复数形式：∫(‖g‖² : ℂ) = Σ(‖conv‖² : ℂ)
  have hC : ∫ x : UnitAddTorus (Fin 2), (‖g x‖ ^ 2 : ℂ) ∂torusMeasure =
      ∑ n ∈ S, (‖convC c c n‖ ^ 2 : ℂ) := by
    have e1 : (∫ x : UnitAddTorus (Fin 2), (‖g x‖ ^ 2 : ℂ) ∂torusMeasure) =
        ∫ x : UnitAddTorus (Fin 2), g x * conj (g x) ∂torusMeasure := by
      apply integral_congr_ae
      filter_upwards with x
      exact (RCLike.mul_conj (g x)).symm
    rw [e1, ← hinner, hgLp, hParseval]
    exact sum_congr rfl fun n _ => RCLike.conj_mul _
  -- 落到实数
  have key : ∫ x : UnitAddTorus (Fin 2), ‖g x‖ ^ 2 ∂torusMeasure =
      ∑ n ∈ S, ‖convC c c n‖ ^ 2 := by
    have e2 : ((∫ x : UnitAddTorus (Fin 2), ‖g x‖ ^ 2 ∂torusMeasure : ℝ) : ℂ) =
        ((∑ n ∈ S, ‖convC c c n‖ ^ 2 : ℝ) : ℂ) := by
      rw [← integral_complex_ofReal, Complex.ofReal_sum]
      push_cast
      exact hC
    exact Complex.ofReal_inj.mp e2
  -- 逐点：‖u‖⁴ = ‖u²‖² = ‖g‖²
  have hpt : ∀ x : UnitAddTorus (Fin 2), ‖fourierPoly c x‖ ^ 4 = ‖g x‖ ^ 2 := by
    intro x
    rw [hgx x, norm_pow, ← pow_mul]
  rw [integral_congr_ae (ae_of_all _ hpt)]
  exact key

/-- **Bernstein 中间估计**：`∫‖u‖⁴ ≤ (Σ‖c‖)²·(Σ‖c‖²)`
（Parseval 第一步 + 卷积 Young 的直接复合；即
`‖u‖⁴_{L⁴} ≤ (Σ_k|c_k|)²·‖u‖²_{L²}` 的积分形式）。
注：这是骨架的中间件而非主不等式——`Σ|c_k|` 不能被 `H¹` 能量均匀控制
（2D 对数发散），主组装需各向异性 1D 迭代（未完登记，见文件头）。 -/
theorem integral_norm_pow_four_le (c : WaveIdx →₀ ℂ) :
    ∫ x : UnitAddTorus (Fin 2), ‖fourierPoly c x‖ ^ 4 ∂torusMeasure ≤
      (∑ k ∈ c.support, ‖c k‖) ^ 2 * (∑ l ∈ c.support, ‖c l‖ ^ 2) := by
  rw [integral_norm_pow_four_fourierPoly]
  exact sum_norm_sq_convC_le c c

end TorusParseval

section SpectralEnergy
/-! ### (iv) 梯度侧谱能量与零均值 Poincaré（Parseval 级） -/

/-- 梯度侧谱坐标能量（Fourier 权 `(2π|k|)²`）：
`specGradEnergy c = Σ_k (2π)²·|k|²·‖c_k‖²`。
对光滑周期场它等于 `‖∇u‖²_{L²}`（`∂ᵢ(mFourier k) = 2πi·kᵢ·mFourier k`；
该微分链接件登记为未完项，见文件头注）。 -/
def specGradEnergy (c : WaveIdx →₀ ℂ) : ℝ :=
  ∑ k ∈ c.support, (2 * Real.pi) ^ 2 * kSq k * ‖c k‖ ^ 2

/-- 波数平方非负。 -/
theorem kSq_nonneg (k : WaveIdx) : 0 ≤ kSq k :=
  add_nonneg (sq_nonneg _) (sq_nonneg _)

/-- 非零波数的平方至少为 1（周期 1 环面首非零模 `|k| = 1`）。 -/
theorem one_le_kSq_of_ne_zero {k : WaveIdx} (hk : k ≠ 0) : 1 ≤ kSq k := by
  have hk01 : k 0 ≠ 0 ∨ k 1 ≠ 0 := by
    by_contra h
    push Not at h
    exact hk (funext fun j => by
      fin_cases j
      · simpa using h.1
      · simpa using h.2)
  have key : ∀ m : ℤ, m ≠ 0 → (1 : ℝ) ≤ (m : ℝ) ^ 2 := by
    intro m hm
    have habs : (1 : ℝ) ≤ |(m : ℝ)| := by exact_mod_cast Int.one_le_abs hm
    have h2 := mul_le_mul habs habs zero_le_one (abs_nonneg _)
    rwa [one_mul, ← pow_two, sq_abs] at h2
  unfold kSq
  rcases hk01 with h0 | h0
  · have h1 := key _ h0
    linarith [sq_nonneg ((k (1 : Fin 2) : ℝ))]
  · have h1 := key _ h0
    linarith [sq_nonneg ((k (0 : Fin 2) : ℝ))]

/-- **零均值 Poincaré（谱坐标，Parseval 级）**：零均值条件 `c 0 = 0`
（常数模缺失）下，L² 能量被梯度谱能量吸收：
`Σ‖c_k‖² ≤ (2π)⁻²·specGradEnergy c`。
这是 D-B1 骨架的均值条件接口件（`C_P = (2π)⁻¹`），
也是 D-B2 均值条件处理的 Fourier 侧入口。 -/
theorem sum_norm_sq_le_specGradEnergy (c : WaveIdx →₀ ℂ) (h0 : c 0 = 0) :
    ∑ k ∈ c.support, ‖c k‖ ^ 2 ≤
      (1 / (2 * Real.pi) ^ 2) * specGradEnergy c := by
  rw [specGradEnergy, mul_sum]
  apply sum_le_sum; intro k _
  by_cases hkk : k = 0
  · subst hkk
    rw [h0]
    simp
  · have h1 := one_le_kSq_of_ne_zero hkk
    have hπ : (0 : ℝ) < Real.pi := Real.pi_pos
    have hc : 0 ≤ ‖c k‖ ^ 2 := sq_nonneg _
    have h2 : (1 / (2 * Real.pi) ^ 2) * ((2 * Real.pi) ^ 2 * kSq k * ‖c k‖ ^ 2) =
        kSq k * ‖c k‖ ^ 2 := by
      field_simp
    rw [h2]
    nlinarith [h1, hc]

end SpectralEnergy

section StatementRegistry
/-! ### 主陈述登记（Prop 级，CapAnchor 先例；登记不断言） -/

/-- **主陈述登记（Prop 级，CapAnchor 先例）**：𝕋² 上零均值有限 Fourier
多项式的 Ladyzhenskaya 不等式（谱坐标形式）——存在常数 `C_L > 0`，
对一切零均值（`c 0 = 0`）有限支集系数 `c`，其三角多项式 `u = fourierPoly c`
满足 `‖u‖²_{L⁴} ≤ C_L·‖u‖_{L²}·(specGradEnergy)^{1/2}`
（左端 `(∫‖u‖⁴)^{1/2}` 即 `‖u‖²_{L⁴}`；`Σ‖c‖² = ‖u‖²_{L²}` 与
梯度侧谱能量的 L² 链接见本文件 Parseval 诸件与文件头未完登记）。

骨架状态（诚实标注）：本文件已证组合核 (i)、Parseval 第一步 (ii)、
Bernstein 中间估计 (iii)、谱能量与零均值 Poincaré (iv)；
主不等式的最终组装（各向异性加权步）与常数显式化**未完成**，
按治理口径登记为 D-B1 未完项 + D-B2 范围，此 Prop 不断言证明
（零 sorry、零新增公理）。 -/
def periodicLadyzhenskayaStatement : Prop :=
  ∃ C_L : ℝ, 0 < C_L ∧ ∀ c : WaveIdx →₀ ℂ, c 0 = 0 →
    (∫ x : UnitAddTorus (Fin 2), ‖fourierPoly c x‖ ^ 4 ∂torusMeasure) ^ ((1 : ℝ) / 2) ≤
      C_L * (∑ k ∈ c.support, ‖c k‖ ^ 2) ^ ((1 : ℝ) / 2) *
        specGradEnergy c ^ ((1 : ℝ) / 2)

end StatementRegistry

section DiffLink
/-! ### (v) 微分链接件：∂ᵢ(mFourier k) = 2πi·kᵢ·mFourier k（D-B2 目标一，证毕）

沿第 `i` 坐标以实参数变化（`Function.update` 嵌入实轴提升），
复用 mathlib 圆周单模导数 `hasDerivAt_fourier`（T = 1）；
谱坐标 H¹ 结构由 Parseval 级恒等式
`specGradEnergy c = ∫‖∂₀u‖² + ∫‖∂₁u‖²` 闭合。
本件为「有限维 ODE 截断层」谱坐标梯度的分析锚点。 -/

/-- **微分链接件（单模）**：`mFourier k` 沿第 `i` 坐标的实参数导数
（在提升点 `t`（`↑t = x i`）处）为 `2πi·kᵢ·mFourier k x`。 -/
theorem hasDerivAt_mFourier_coord (k : WaveIdx) (x : UnitAddTorus (Fin 2)) (i : Fin 2)
    {t : ℝ} (ht : (t : UnitAddCircle) = x i) :
    HasDerivAt (fun s : ℝ => mFourier k (Function.update x i (s : UnitAddCircle)))
      (2 * Real.pi * Complex.I * (k i : ℂ) * mFourier k x) t := by
  classical
  -- 乘积分离：提出第 i 因子，其余坐标在 update 下不变
  have hfac : (fun s : ℝ => mFourier k (Function.update x i (s : UnitAddCircle))) =
      fun s : ℝ => (∏ j ∈ Finset.univ.erase i, fourier (k j) (x j)) *
        fourier (k i) (s : UnitAddCircle) := by
    funext s
    simp only [mFourier, ContinuousMap.coe_mk]
    rw [← Finset.mul_prod_erase Finset.univ _ (Finset.mem_univ i),
      mul_comm (∏ j ∈ Finset.univ.erase i, fourier (k j) (x j)) (fourier (k i) (s : UnitAddCircle))]
    congr 1
    · congr 1
      exact Function.update_self i _ x
    · apply Finset.prod_congr rfl
      intro j hj
      rw [Finset.mem_erase] at hj
      congr 1
      exact Function.update_of_ne hj.1 _ x
  rw [hfac]
  -- 单因子圆周导数（T = 1，故 2πi·kᵢ/1 = 2πi·kᵢ）
  have h1 := hasDerivAt_fourier (1 : ℝ) (k i) t
  simp only [Complex.ofReal_one, div_one] at h1
  convert h1.const_mul (∏ j ∈ Finset.univ.erase i, fourier (k j) (x j)) using 1
  -- 导数值对齐：代回 ↑t = x i 并重组乘积
  rw [ht]
  simp only [mFourier, ContinuousMap.coe_mk]
  rw [← Finset.mul_prod_erase Finset.univ _ (Finset.mem_univ i)]
  ring

/-- 三角多项式的第 `i` 坐标偏导多项式（点值形式）：
系数逐项乘 `2πi·kᵢ`（微分链接件的符号封装）。 -/
def pderivPoly (i : Fin 2) (c : WaveIdx →₀ ℂ) (x : UnitAddTorus (Fin 2)) : ℂ :=
  ∑ k ∈ c.support, (2 * Real.pi * Complex.I * (k i : ℂ) * c k) * mFourier k x

/-- **微分链接件（三角多项式整体）**：`u = fourierPoly c` 沿第 `i` 坐标的
实参数导数等于偏导多项式 `pderivPoly i c`（系数 `2πi·kᵢ·cₖ`）在该点的值。 -/
theorem hasDerivAt_fourierPoly_coord (c : WaveIdx →₀ ℂ) (x : UnitAddTorus (Fin 2)) (i : Fin 2)
    {t : ℝ} (ht : (t : UnitAddCircle) = x i) :
    HasDerivAt (fun s : ℝ => fourierPoly c (Function.update x i (s : UnitAddCircle)))
      (pderivPoly i c x) t := by
  classical
  have hterm : ∀ k ∈ c.support,
      HasDerivAt (fun s : ℝ => c k * mFourier k (Function.update x i (s : UnitAddCircle)))
        (c k * (2 * Real.pi * Complex.I * (k i : ℂ) * mFourier k x)) t :=
    fun k _ => (hasDerivAt_mFourier_coord k x i ht).const_mul (c k)
  have hsum := HasDerivAt.sum hterm
  have hfun2 : (∑ k ∈ c.support, fun s : ℝ => c k * mFourier k
        (Function.update x i (s : UnitAddCircle))) =
      (fun s : ℝ => fourierPoly c (Function.update x i (s : UnitAddCircle))) := by
    funext s
    simp only [Finset.sum_apply]
    rfl
  rw [hfun2] at hsum
  convert hsum using 1
  show (∑ k ∈ c.support, (2 * Real.pi * Complex.I * (k i : ℂ) * c k) * mFourier k x) =
    ∑ k ∈ c.support, c k * (2 * Real.pi * Complex.I * (k i : ℂ) * mFourier k x)
  exact Finset.sum_congr rfl fun k _ => by ring

/-- **一般有限三角和的 L² Parseval**（`torusMeasure`）：
`∫‖Σ_{k∈s} aₖ·mFourier k‖² = Σ‖aₖ‖²`（对任意有限指标集与任意系数函数；
不要求支集条件，正交性直接吸收）。 -/
theorem integral_norm_sq_sum_mFourier (s : Finset WaveIdx) (a : WaveIdx → ℂ) :
    ∫ x : UnitAddTorus (Fin 2), ‖∑ k ∈ s, a k * mFourier k x‖ ^ 2 ∂torusMeasure =
      ∑ k ∈ s, ‖a k‖ ^ 2 := by
  classical
  set g : C(UnitAddTorus (Fin 2), ℂ) := ∑ k ∈ s, a k • mFourier k with hg
  have hgx : ∀ x : UnitAddTorus (Fin 2), g x = ∑ k ∈ s, a k * mFourier k x := by
    intro x
    simp only [hg, ContinuousMap.coe_sum, ContinuousMap.coe_smul, Finset.sum_apply,
      Pi.smul_apply, smul_eq_mul]
  have hinner : ⟪ContinuousMap.toLp 2 torusMeasure ℂ g,
        ContinuousMap.toLp 2 torusMeasure ℂ g⟫_ℂ =
      ∫ x : UnitAddTorus (Fin 2), g x * conj (g x) ∂torusMeasure :=
    ContinuousMap.inner_toLp _ _ _
  have hgLp : ContinuousMap.toLp 2 torusMeasure ℂ g =
      ∑ k ∈ s, a k • mFourierLp (d := Fin 2) 2 k := by
    rw [hg, map_sum]
    exact Finset.sum_congr rfl fun k _ => map_smul _ _ _
  have hParseval : ⟪∑ k ∈ s, a k • mFourierLp (d := Fin 2) 2 k,
        ∑ k ∈ s, a k • mFourierLp (d := Fin 2) 2 k⟫_ℂ =
      ∑ k ∈ s, conj (a k) * a k :=
    orthonormal_mFourier.inner_sum _ _ _
  have hC : (∫ x : UnitAddTorus (Fin 2), (‖g x‖ ^ 2 : ℂ) ∂torusMeasure) =
      ∑ k ∈ s, (‖a k‖ ^ 2 : ℂ) := by
    have e1 : (∫ x : UnitAddTorus (Fin 2), (‖g x‖ ^ 2 : ℂ) ∂torusMeasure) =
        ∫ x : UnitAddTorus (Fin 2), g x * conj (g x) ∂torusMeasure := by
      apply integral_congr_ae
      filter_upwards with x
      exact (RCLike.mul_conj (g x)).symm
    rw [e1, ← hinner, hgLp, hParseval]
    exact Finset.sum_congr rfl fun k _ => RCLike.conj_mul _
  have key : ∫ x : UnitAddTorus (Fin 2), ‖g x‖ ^ 2 ∂torusMeasure =
      ∑ k ∈ s, ‖a k‖ ^ 2 := by
    have e2 : ((∫ x : UnitAddTorus (Fin 2), ‖g x‖ ^ 2 ∂torusMeasure : ℝ) : ℂ) =
        ((∑ k ∈ s, ‖a k‖ ^ 2 : ℝ) : ℂ) := by
      rw [← integral_complex_ofReal, Complex.ofReal_sum]
      push_cast
      exact hC
    exact Complex.ofReal_inj.mp e2
  have hpt : ∀ x : UnitAddTorus (Fin 2),
      ‖∑ k ∈ s, a k * mFourier k x‖ ^ 2 = ‖g x‖ ^ 2 := fun x => by rw [hgx x]
  rw [integral_congr_ae (ae_of_all _ hpt)]
  exact key

/-- **L² Parseval（fourierPoly 版）**：`∫‖u‖² = Σ‖cₖ‖²`。 -/
theorem integral_norm_sq_fourierPoly (c : WaveIdx →₀ ℂ) :
    ∫ x : UnitAddTorus (Fin 2), ‖fourierPoly c x‖ ^ 2 ∂torusMeasure =
      ∑ k ∈ c.support, ‖c k‖ ^ 2 :=
  integral_norm_sq_sum_mFourier c.support (fun k => c k)

/-- **偏导多项式的 L² 能量（谱形式）**：
`∫‖∂ᵢu‖² = (2π)²·Σ kᵢ²·‖cₖ‖²`（Parseval + 微分链接件系数范数）。 -/
theorem integral_norm_sq_pderivPoly (i : Fin 2) (c : WaveIdx →₀ ℂ) :
    ∫ x : UnitAddTorus (Fin 2), ‖pderivPoly i c x‖ ^ 2 ∂torusMeasure =
      (2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k i : ℝ) ^ 2 * ‖c k‖ ^ 2 := by
  have hn : ∀ k : WaveIdx,
      ‖2 * Real.pi * Complex.I * (k i : ℂ) * c k‖ =
        2 * Real.pi * |(k i : ℝ)| * ‖c k‖ := by
    intro k
    have h2pi : ((2 : ℂ) * (Real.pi : ℂ)) = ((2 * Real.pi : ℝ) : ℂ) := by
      push_cast; ring
    rw [h2pi, norm_mul, norm_mul, norm_mul, Complex.norm_real, Complex.norm_I,
      Complex.norm_intCast, mul_one, Real.norm_eq_abs,
      abs_of_pos (mul_pos zero_lt_two Real.pi_pos)]
  have hmain : ∫ x : UnitAddTorus (Fin 2), ‖pderivPoly i c x‖ ^ 2 ∂torusMeasure =
      ∑ k ∈ c.support, ‖2 * Real.pi * Complex.I * (k i : ℂ) * c k‖ ^ 2 := by
    unfold pderivPoly
    exact integral_norm_sq_sum_mFourier c.support _
  rw [hmain, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [hn k, mul_pow, mul_pow, sq_abs]
  ring

/-- **梯度 L² 能量 = 谱能量（谱坐标 H¹ 结构闭合件）**：
`specGradEnergy c = ∫‖∂₀u‖² + ∫‖∂₁u‖²`，即谱坐标梯度能量与
逐坐标偏导多项式的 L² 能量严格等同（微分链接件的积分化）。 -/
theorem specGradEnergy_eq_integral_pderiv (c : WaveIdx →₀ ℂ) :
    specGradEnergy c =
      (∫ x : UnitAddTorus (Fin 2), ‖pderivPoly 0 c x‖ ^ 2 ∂torusMeasure) +
        ∫ x : UnitAddTorus (Fin 2), ‖pderivPoly 1 c x‖ ^ 2 ∂torusMeasure := by
  rw [integral_norm_sq_pderivPoly, integral_norm_sq_pderivPoly, specGradEnergy, ← mul_add,
    ← Finset.sum_add_distrib, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [kSq]
  ring

/-- **零均值 Poincaré（积分形式）**：`∫‖u‖² ≤ (2π)⁻²·(∫‖∂₀u‖² + ∫‖∂₁u‖²)`
（谱级 Poincaré 经微分链接件积分化；零均值条件以显式假设携带）。 -/
theorem integral_norm_sq_le_integral_pderiv (c : WaveIdx →₀ ℂ) (h0 : c 0 = 0) :
    ∫ x : UnitAddTorus (Fin 2), ‖fourierPoly c x‖ ^ 2 ∂torusMeasure ≤
      (1 / (2 * Real.pi) ^ 2) *
        ((∫ x : UnitAddTorus (Fin 2), ‖pderivPoly 0 c x‖ ^ 2 ∂torusMeasure) +
          ∫ x : UnitAddTorus (Fin 2), ‖pderivPoly 1 c x‖ ^ 2 ∂torusMeasure) := by
  rw [integral_norm_sq_fourierPoly, ← specGradEnergy_eq_integral_pderiv]
  exact sum_norm_sq_le_specGradEnergy c h0

end DiffLink

section OneDim
/-! ### (vi) 1D 周期 Ladyzhenskaya 全证（D-B2 目标二，UnitAddCircle 上，显式常数）

路线：1D 可和性 `Σ_{k≠0} k⁻² = π²/3`（巴塞尔 `hasSum_zeta_two` 截断）
⇒ 加权 Cauchy–Schwarz `(Σ‖c‖)² ≤ (π²/3)·Σk²‖c‖²`（零均值）
⇒ 复用 (i)(ii)(iii) 的 1D 镜像 `∫‖u‖⁴ ≤ (Σ‖c‖)²(Σ‖c‖²)`
⇒ `∫‖u‖⁴ ≤ (1/12)·(∫‖u‖²)·(∫‖∂u‖²)`（常数 C = 1/12 完全显式）。
另收边无均值条件的一般形式（常数 1 + π²/3）。 -/

/-- 测度钉（1D）：`UnitAddCircle` 的归一化 Haar 测度
（与 `fourierLp`/`orthonormal_fourier` 定义处逐字相同）。 -/
abbrev circleMeasure : Measure UnitAddCircle := AddCircle.haarAddCircle

/-- 1D 有限 Fourier 多项式：`x ↦ Σ_k c_k·fourier k x`。 -/
def fourierPoly1 (c : ℤ →₀ ℂ) (x : UnitAddCircle) : ℂ :=
  ∑ k ∈ c.support, c k * fourier k x

/-- 1D 有限 Fourier 多项式作为连续映射。 -/
def fourierPolyC1 (c : ℤ →₀ ℂ) : C(UnitAddCircle, ℂ) where
  toFun := fourierPoly1 c
  continuous_toFun := continuous_finsetSum _ fun k _ =>
    continuous_const.mul (fourier k).continuous

/-- 1D 一般有限三角和的 L² Parseval（`circleMeasure`）。 -/
theorem integral_norm_sq_sum_fourier (s : Finset ℤ) (a : ℤ → ℂ) :
    ∫ x : UnitAddCircle, ‖∑ k ∈ s, a k * fourier k x‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ s, ‖a k‖ ^ 2 := by
  classical
  set g : C(UnitAddCircle, ℂ) := ∑ k ∈ s, a k • fourier k with hg
  have hgx : ∀ x : UnitAddCircle, g x = ∑ k ∈ s, a k * fourier k x := by
    intro x
    simp only [hg, ContinuousMap.coe_sum, ContinuousMap.coe_smul, Finset.sum_apply,
      Pi.smul_apply, smul_eq_mul]
  have hinner : ⟪ContinuousMap.toLp 2 circleMeasure ℂ g,
        ContinuousMap.toLp 2 circleMeasure ℂ g⟫_ℂ =
      ∫ x : UnitAddCircle, g x * conj (g x) ∂circleMeasure :=
    ContinuousMap.inner_toLp _ _ _
  have hgLp : ContinuousMap.toLp 2 circleMeasure ℂ g =
      ∑ k ∈ s, a k • fourierLp (T := (1 : ℝ)) 2 k := by
    rw [hg, map_sum]
    exact Finset.sum_congr rfl fun k _ => map_smul _ _ _
  have hParseval : ⟪∑ k ∈ s, a k • fourierLp (T := (1 : ℝ)) 2 k,
        ∑ k ∈ s, a k • fourierLp (T := (1 : ℝ)) 2 k⟫_ℂ =
      ∑ k ∈ s, conj (a k) * a k :=
    orthonormal_fourier.inner_sum _ _ _
  have hC : (∫ x : UnitAddCircle, (‖g x‖ ^ 2 : ℂ) ∂circleMeasure) =
      ∑ k ∈ s, (‖a k‖ ^ 2 : ℂ) := by
    have e1 : (∫ x : UnitAddCircle, (‖g x‖ ^ 2 : ℂ) ∂circleMeasure) =
        ∫ x : UnitAddCircle, g x * conj (g x) ∂circleMeasure := by
      apply integral_congr_ae
      filter_upwards with x
      exact (RCLike.mul_conj (g x)).symm
    rw [e1, ← hinner, hgLp, hParseval]
    exact Finset.sum_congr rfl fun k _ => RCLike.conj_mul _
  have key : ∫ x : UnitAddCircle, ‖g x‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ s, ‖a k‖ ^ 2 := by
    have e2 : ((∫ x : UnitAddCircle, ‖g x‖ ^ 2 ∂circleMeasure : ℝ) : ℂ) =
        ((∑ k ∈ s, ‖a k‖ ^ 2 : ℝ) : ℂ) := by
      rw [← integral_complex_ofReal, Complex.ofReal_sum]
      push_cast
      exact hC
    exact Complex.ofReal_inj.mp e2
  have hpt : ∀ x : UnitAddCircle,
      ‖∑ k ∈ s, a k * fourier k x‖ ^ 2 = ‖g x‖ ^ 2 := fun x => by rw [hgx x]
  rw [integral_congr_ae (ae_of_all _ hpt)]
  exact key

/-- **1D L² Parseval**：`∫‖u‖² = Σ‖cₖ‖²`。 -/
theorem integral_norm_sq_fourierPoly1 (c : ℤ →₀ ℂ) :
    ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ c.support, ‖c k‖ ^ 2 :=
  integral_norm_sq_sum_fourier c.support (fun k => c k)

/-- 1D 三角多项式乘法 = 系数卷积（`fourier_add` 的直接推论）。 -/
theorem fourierPoly1_mul (c d : ℤ →₀ ℂ) (x : UnitAddCircle) :
    fourierPoly1 c x * fourierPoly1 d x =
      ∑ n ∈ c.support.image₂ (· + ·) d.support, convC c d n * fourier n x := by
  classical
  set s := c.support with hs
  set t := d.support with ht
  have h1 : fourierPoly1 c x * fourierPoly1 d x =
      ∑ p ∈ s ×ˢ t, (c p.1 * d p.2) * fourier (p.1 + p.2) x := by
    rw [fourierPoly1, fourierPoly1, sum_mul_sum, sum_product]
    apply sum_congr rfl; intro k _
    apply sum_congr rfl; intro l _
    rw [fourier_add]; ring
  rw [h1, ← sum_fiberwise_of_maps_to (g := fun p : ℤ × ℤ => p.1 + p.2)
    (t := c.support.image₂ (· + ·) d.support)
    (f := fun p : ℤ × ℤ => (c p.1 * d p.2) * fourier (p.1 + p.2) x)
    (fun p hp =>
      mem_image₂.mpr ⟨p.1, (mem_product.mp hp).1, p.2, (mem_product.mp hp).2, rfl⟩)]
  apply sum_congr rfl; intro n _
  have hconv : ∀ p ∈ (s ×ˢ t).filter (fun p => p.1 + p.2 = n),
      (c p.1 * d p.2) * fourier (p.1 + p.2) x = (c p.1 * d p.2) * fourier n x := by
    intro p hp
    rw [mem_filter] at hp
    rw [hp.2]
  rw [sum_congr rfl hconv, ← sum_mul]
  congr 1
  have hfb : ∑ p ∈ (s ×ˢ t).filter (fun p => p.1 + p.2 = n), c p.1 * d p.2 =
      ∑ k ∈ s.filter (fun k => n - k ∈ t), c k * d (n - k) := by
    apply sum_bij (fun p _ => p.1)
    · intro p hp
      rw [mem_filter, mem_product] at hp
      rw [mem_filter]
      refine ⟨hp.1.1, ?_⟩
      have h2 : p.2 = n - p.1 := by rw [← hp.2]; abel
      rw [← h2]; exact hp.1.2
    · intro p hp q hq h
      rw [mem_filter] at hp hq
      obtain ⟨h₁, h₂⟩ := p
      obtain ⟨h₃, h₄⟩ := q
      simp only at h
      have e1 : h₂ = n - h₁ := by rw [← hp.2]; abel
      have e2 : h₄ = n - h₃ := by rw [← hq.2]; abel
      simp only [Prod.mk.injEq]
      exact ⟨h, by rw [e1, e2, h]⟩
    · intro k hk
      rw [mem_filter] at hk
      exact ⟨(k, n - k), by
        rw [mem_filter, mem_product]
        exact ⟨⟨hk.1, hk.2⟩, by ring⟩, rfl⟩
    · intro p hp
      rw [mem_filter] at hp
      have h2 : p.2 = n - p.1 := by rw [← hp.2]; abel
      rw [h2]
  rw [hfb]
  show ∑ k ∈ s.filter (fun k => n - k ∈ t), c k * d (n - k) =
    ∑ k ∈ c.support, c k * d (n - k)
  apply sum_filter_of_ne
  intro k _ hne
  by_contra hnt
  rw [Finsupp.notMem_support_iff] at hnt
  rw [hnt, mul_zero] at hne
  exact hne rfl

/-- **1D L⁴ → 卷积（Parseval 第一步）**：`∫‖u‖⁴ = Σ‖(c⋆c)‖²`。 -/
theorem integral_norm_pow_four_fourierPoly1 (c : ℤ →₀ ℂ) :
    ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure =
      ∑ n ∈ c.support.image₂ (· + ·) c.support, ‖convC c c n‖ ^ 2 := by
  classical
  set s := c.support with hs
  set S := s.image₂ (· + ·) s with hS
  set g : C(UnitAddCircle, ℂ) := ∑ n ∈ S, convC c c n • fourier n with hg
  have hgx : ∀ x : UnitAddCircle, g x = (fourierPoly1 c x) ^ 2 := by
    intro x
    rw [pow_two, fourierPoly1_mul]
    simp only [hg, ContinuousMap.coe_sum, ContinuousMap.coe_smul, Finset.sum_apply,
      Pi.smul_apply, smul_eq_mul]
    rw [hS, hs]
  have hinner : ⟪ContinuousMap.toLp 2 circleMeasure ℂ g,
        ContinuousMap.toLp 2 circleMeasure ℂ g⟫_ℂ =
      ∫ x : UnitAddCircle, g x * conj (g x) ∂circleMeasure :=
    ContinuousMap.inner_toLp _ _ _
  have hgLp : ContinuousMap.toLp 2 circleMeasure ℂ g =
      ∑ n ∈ S, convC c c n • fourierLp (T := (1 : ℝ)) 2 n := by
    rw [hg, map_sum]
    exact Finset.sum_congr rfl fun n _ => map_smul _ _ _
  have hParseval : ⟪∑ n ∈ S, convC c c n • fourierLp (T := (1 : ℝ)) 2 n,
        ∑ n ∈ S, convC c c n • fourierLp (T := (1 : ℝ)) 2 n⟫_ℂ =
      ∑ n ∈ S, conj (convC c c n) * convC c c n :=
    orthonormal_fourier.inner_sum _ _ _
  have hC : (∫ x : UnitAddCircle, (‖g x‖ ^ 2 : ℂ) ∂circleMeasure) =
      ∑ n ∈ S, (‖convC c c n‖ ^ 2 : ℂ) := by
    have e1 : (∫ x : UnitAddCircle, (‖g x‖ ^ 2 : ℂ) ∂circleMeasure) =
        ∫ x : UnitAddCircle, g x * conj (g x) ∂circleMeasure := by
      apply integral_congr_ae
      filter_upwards with x
      exact (RCLike.mul_conj (g x)).symm
    rw [e1, ← hinner, hgLp, hParseval]
    exact Finset.sum_congr rfl fun n _ => RCLike.conj_mul _
  have key : ∫ x : UnitAddCircle, ‖g x‖ ^ 2 ∂circleMeasure =
      ∑ n ∈ S, ‖convC c c n‖ ^ 2 := by
    have e2 : ((∫ x : UnitAddCircle, ‖g x‖ ^ 2 ∂circleMeasure : ℝ) : ℂ) =
        ((∑ n ∈ S, ‖convC c c n‖ ^ 2 : ℝ) : ℂ) := by
      rw [← integral_complex_ofReal, Complex.ofReal_sum]
      push_cast
      exact hC
    exact Complex.ofReal_inj.mp e2
  have hpt : ∀ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 = ‖g x‖ ^ 2 := by
    intro x
    rw [hgx x, norm_pow, ← pow_mul]
  rw [integral_congr_ae (ae_of_all _ hpt)]
  exact key

/-- **1D Bernstein 中间估计**：`∫‖u‖⁴ ≤ (Σ‖c‖)²·(Σ‖c‖²)`
（1D Parseval 第一步 + 通用卷积 Young 的直接复合）。 -/
theorem integral_norm_pow_four_le1 (c : ℤ →₀ ℂ) :
    ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure ≤
      (∑ k ∈ c.support, ‖c k‖) ^ 2 * (∑ l ∈ c.support, ‖c l‖ ^ 2) := by
  rw [integral_norm_pow_four_fourierPoly1]
  exact sum_norm_sq_convC_le c c

/-- 1D 偏导多项式（点值形式）：系数逐项乘 `2πi·k`。 -/
def pderivPoly1 (c : ℤ →₀ ℂ) (x : UnitAddCircle) : ℂ :=
  ∑ k ∈ c.support, (2 * Real.pi * Complex.I * (k : ℂ) * c k) * fourier k x

/-- **1D 微分链接件**：实轴提升下 `fourierPoly1 c` 的导数即
`pderivPoly1 c`（`hasDerivAt_fourier`（T = 1）逐项求和）。 -/
theorem hasDerivAt_fourierPoly1 (c : ℤ →₀ ℂ) (t : ℝ) :
    HasDerivAt (fun s : ℝ => fourierPoly1 c (s : UnitAddCircle))
      (pderivPoly1 c (t : UnitAddCircle)) t := by
  classical
  have hterm : ∀ k ∈ c.support,
      HasDerivAt (fun s : ℝ => c k * fourier k (s : UnitAddCircle))
        (c k * (2 * Real.pi * Complex.I * (k : ℂ) * fourier k (t : UnitAddCircle))) t := by
    intro k _
    have h1 := hasDerivAt_fourier (1 : ℝ) k t
    simp only [Complex.ofReal_one, div_one] at h1
    exact h1.const_mul (c k)
  have hsum := HasDerivAt.sum hterm
  have hfun2 : (∑ k ∈ c.support, fun s : ℝ => c k * fourier k (s : UnitAddCircle)) =
      (fun s : ℝ => fourierPoly1 c (s : UnitAddCircle)) := by
    funext s
    simp only [Finset.sum_apply]
    rfl
  rw [hfun2] at hsum
  convert hsum using 1
  show (∑ k ∈ c.support, (2 * Real.pi * Complex.I * (k : ℂ) * c k) *
      fourier k (t : UnitAddCircle)) =
    ∑ k ∈ c.support, c k * (2 * Real.pi * Complex.I * (k : ℂ) *
      fourier k (t : UnitAddCircle))
  exact Finset.sum_congr rfl fun k _ => by ring

/-- **1D 偏导能量（谱形式）**：`∫‖∂u‖² = (2π)²·Σ k²·‖cₖ‖²`。 -/
theorem integral_norm_sq_pderivPoly1 (c : ℤ →₀ ℂ) :
    ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure =
      (2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2 := by
  have hn : ∀ k : ℤ, ‖2 * Real.pi * Complex.I * (k : ℂ) * c k‖ =
      2 * Real.pi * |(k : ℝ)| * ‖c k‖ := by
    intro k
    have h2pi : ((2 : ℂ) * (Real.pi : ℂ)) = ((2 * Real.pi : ℝ) : ℂ) := by
      push_cast; ring
    rw [h2pi, norm_mul, norm_mul, norm_mul, Complex.norm_real, Complex.norm_I,
      Complex.norm_intCast, mul_one, Real.norm_eq_abs,
      abs_of_pos (mul_pos zero_lt_two Real.pi_pos)]
  have hmain : ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ c.support, ‖2 * Real.pi * Complex.I * (k : ℂ) * c k‖ ^ 2 := by
    unfold pderivPoly1
    exact integral_norm_sq_sum_fourier c.support _
  rw [hmain, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [hn k, mul_pow, mul_pow, sq_abs]
  ring

/-- **整数倒数平方截断和界**（巴塞尔 `Σ_{n≥1} 1/n² = π²/6` 的有限截断推论，
正/负部各贡献 ≤ π²/6）：`Σ_{k∈s, k≠0} 1/k² ≤ π²/3`。 -/
theorem sum_inv_sq_le (s : Finset ℤ) :
    ∑ k ∈ s, (if k = 0 then (0 : ℝ) else 1 / (k : ℝ) ^ 2) ≤ Real.pi ^ 2 / 3 := by
  classical
  have hdecomp : ∀ k : ℤ, (if k = 0 then (0 : ℝ) else 1 / (k : ℝ) ^ 2) =
      (if 0 < k then 1 / (k : ℝ) ^ 2 else 0) + (if k < 0 then 1 / (k : ℝ) ^ 2 else 0) := by
    intro k
    rcases lt_trichotomy 0 k with h | h | h
    · rw [if_neg h.ne', if_pos h, if_neg (not_lt.mpr h.le), add_zero]
    · subst h; simp
    · rw [if_neg h.ne, if_neg (not_lt.mpr h.le), if_pos h, zero_add]
  have h1 : (∑ k ∈ s, if k = 0 then (0 : ℝ) else 1 / (k : ℝ) ^ 2) =
      (∑ k ∈ s.filter (fun k => 0 < k), 1 / (k : ℝ) ^ 2) +
        ∑ k ∈ s.filter (fun k => k < 0), 1 / (k : ℝ) ^ 2 := by
    rw [Finset.sum_filter, Finset.sum_filter, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun k _ => hdecomp k
  rw [h1]
  -- 正部：toNat 单射映入 ℕ 后用巴塞尔截断
  have hpos : (∑ k ∈ s.filter (fun k => 0 < k), 1 / (k : ℝ) ^ 2) ≤ Real.pi ^ 2 / 6 := by
    have hinj : ∀ x ∈ s.filter (fun k => 0 < k), ∀ y ∈ s.filter (fun k => 0 < k),
        x.toNat = y.toNat → x = y := by
      intro x hx y hy hxy
      rw [Finset.mem_filter] at hx hy
      rw [← Int.toNat_of_nonneg hx.2.le, ← Int.toNat_of_nonneg hy.2.le, hxy]
    have hterm : ∀ k ∈ s.filter (fun k => 0 < k),
        (1 : ℝ) / (k : ℝ) ^ 2 = 1 / ((k.toNat : ℕ) : ℝ) ^ 2 := by
      intro k hk
      rw [Finset.mem_filter] at hk
      have h2 : ((k.toNat : ℕ) : ℝ) = (k : ℝ) := by
        exact_mod_cast Int.toNat_of_nonneg hk.2.le
      rw [h2]
    rw [Finset.sum_congr rfl hterm]
    calc (∑ x ∈ s.filter (fun k => 0 < k), (1 : ℝ) / ((x.toNat : ℕ) : ℝ) ^ 2)
        = ∑ n ∈ (s.filter (fun k => 0 < k)).image Int.toNat, (1 : ℝ) / (n : ℝ) ^ 2 :=
          (Finset.sum_image (f := fun n : ℕ => (1 : ℝ) / (n : ℝ) ^ 2) hinj).symm
      _ ≤ ∑' n : ℕ, (1 : ℝ) / (n : ℝ) ^ 2 :=
          Summable.sum_le_tsum _ (fun n _ => by positivity) hasSum_zeta_two.summable
      _ = Real.pi ^ 2 / 6 := hasSum_zeta_two.tsum_eq
  -- 负部：取反归约到正部
  have hneg : (∑ k ∈ s.filter (fun k => k < 0), 1 / (k : ℝ) ^ 2) ≤ Real.pi ^ 2 / 6 := by
    have hinj : ∀ x ∈ s.filter (fun k => k < 0), ∀ y ∈ s.filter (fun k => k < 0),
        (-x).toNat = (-y).toNat → x = y := by
      intro x hx y hy hxy
      rw [Finset.mem_filter] at hx hy
      have hx' : ((-x).toNat : ℤ) = -x := Int.toNat_of_nonneg (le_of_lt (neg_pos.mpr hx.2))
      have hy' : ((-y).toNat : ℤ) = -y := Int.toNat_of_nonneg (le_of_lt (neg_pos.mpr hy.2))
      have h : (-x : ℤ) = -y := by rw [← hx', ← hy', hxy]
      linarith [neg_inj.mp h]
    have hterm : ∀ k ∈ s.filter (fun k => k < 0),
        (1 : ℝ) / (k : ℝ) ^ 2 = 1 / (((-k).toNat : ℕ) : ℝ) ^ 2 := by
      intro k hk
      rw [Finset.mem_filter] at hk
      have h2 : (((-k).toNat : ℕ) : ℝ) = (-k : ℝ) := by
        exact_mod_cast Int.toNat_of_nonneg (le_of_lt (neg_pos.mpr hk.2))
      rw [h2, neg_sq]
    rw [Finset.sum_congr rfl hterm]
    calc (∑ x ∈ s.filter (fun k => k < 0), (1 : ℝ) / (((-x).toNat : ℕ) : ℝ) ^ 2)
        = ∑ n ∈ ((s.filter (fun k => k < 0)).image (fun k => (-k).toNat) : Finset ℕ),
            (1 : ℝ) / (n : ℝ) ^ 2 :=
          (Finset.sum_image (s := s.filter fun k => k < 0) (g := fun k : ℤ => (-k).toNat)
            (f := fun n : ℕ => (1 : ℝ) / (n : ℝ) ^ 2) hinj).symm
      _ ≤ ∑' n : ℕ, (1 : ℝ) / (n : ℝ) ^ 2 :=
          Summable.sum_le_tsum _ (fun n _ => by positivity) hasSum_zeta_two.summable
      _ = Real.pi ^ 2 / 6 := hasSum_zeta_two.tsum_eq
  linarith [hpos, hneg]

/-- **零均值加权 Cauchy–Schwarz（1D 可和性入口）**：
`(Σ‖c‖)² ≤ (π²/3)·Σ k²‖c‖²`（零均值条件以显式假设携带；
k = 0 项两侧同零，权重 `|k|` 与 `1/|k|` 配对）。 -/
theorem sum_norm_sq_mul_sqKey (c : ℤ →₀ ℂ) (h0 : c 0 = 0) :
    (∑ k ∈ c.support, ‖c k‖) ^ 2 ≤
      (Real.pi ^ 2 / 3) * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2 := by
  classical
  have hCS := sum_mul_sq_le_sq_mul_sq c.support (fun k => |(k : ℝ)| * ‖c k‖)
    (fun k => if k = 0 then (0 : ℝ) else 1 / |(k : ℝ)|)
  have hab : ∀ k ∈ c.support,
      |(k : ℝ)| * ‖c k‖ * (if k = 0 then (0 : ℝ) else 1 / |(k : ℝ)|) = ‖c k‖ := by
    intro k _
    by_cases hk : k = 0
    · subst hk
      rw [h0]
      simp
    · rw [if_neg hk]
      have hkn : |(k : ℝ)| ≠ 0 :=
        abs_ne_zero.mpr (by exact_mod_cast hk : (k : ℝ) ≠ 0)
      field_simp
  rw [Finset.sum_congr rfl hab] at hCS
  have hA : (∑ k ∈ c.support, (|(k : ℝ)| * ‖c k‖) ^ 2) =
      ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2 := by
    apply Finset.sum_congr rfl
    intro k _
    rw [mul_pow, sq_abs]
  rw [hA] at hCS
  have hB : (∑ k ∈ c.support, (if k = 0 then (0 : ℝ) else 1 / |(k : ℝ)|) ^ 2) ≤
      Real.pi ^ 2 / 3 := by
    have hbb : ∀ k : ℤ, (if k = 0 then (0 : ℝ) else 1 / |(k : ℝ)|) ^ 2 =
        if k = 0 then (0 : ℝ) else 1 / (k : ℝ) ^ 2 := by
      intro k
      by_cases hk : k = 0
      · simp [hk]
      · rw [if_neg hk, if_neg hk, div_pow, one_pow, sq_abs]
    rw [Finset.sum_congr rfl (fun k _ => hbb k)]
    exact sum_inv_sq_le c.support
  calc (∑ k ∈ c.support, ‖c k‖) ^ 2
      ≤ (∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2) *
          ∑ k ∈ c.support, (if k = 0 then (0 : ℝ) else 1 / |(k : ℝ)|) ^ 2 := hCS
    _ ≤ (∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2) * (Real.pi ^ 2 / 3) :=
        mul_le_mul_of_nonneg_left hB
          (Finset.sum_nonneg fun k _ => mul_nonneg (sq_nonneg _) (sq_nonneg _))
    _ = (Real.pi ^ 2 / 3) * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2 := mul_comm _ _

/-- **1D 周期 Ladyzhenskaya（零均值，显式常数 C = 1/12）**：
`∫‖u‖⁴ ≤ (1/12)·(∫‖u‖²)·(∫‖∂u‖²)`。
证明链：1D Bernstein ⇒ 零均值加权 CS（巴塞尔 π²/3）⇒ 谱能量回代
（`(2π)²` 吸收：`π²/3 · (2π)⁻² = 1/12`）。 -/
theorem ladyzhenskaya_oneD (c : ℤ →₀ ℂ) (h0 : c 0 = 0) :
    ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure ≤
      (1 / 12) * (∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) *
        ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure := by
  rw [integral_norm_sq_fourierPoly1, integral_norm_sq_pderivPoly1]
  calc ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure
      ≤ (∑ k ∈ c.support, ‖c k‖) ^ 2 * (∑ l ∈ c.support, ‖c l‖ ^ 2) :=
        integral_norm_pow_four_le1 c
    _ ≤ ((Real.pi ^ 2 / 3) * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2) *
          (∑ l ∈ c.support, ‖c l‖ ^ 2) :=
        mul_le_mul_of_nonneg_right (sum_norm_sq_mul_sqKey c h0)
          (Finset.sum_nonneg fun l _ => sq_nonneg _)
    _ = (1 / 12) * (∑ l ∈ c.support, ‖c l‖ ^ 2) *
          ((2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2) := by
        have hπ : (0 : ℝ) < Real.pi := Real.pi_pos
        field_simp
        ring

/-- **1D 周期 Ladyzhenskaya（零均值，H¹ 半范收边形式）**：
`∫‖u‖⁴ ≤ (1/12)·(∫‖u‖²)·(∫‖u‖² + ∫‖∂u‖²)`（梯度因子放宽非负项）。 -/
theorem ladyzhenskaya_oneD_h1 (c : ℤ →₀ ℂ) (h0 : c 0 = 0) :
    ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure ≤
      (1 / 12) * (∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) *
        ((∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) +
          ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure) := by
  refine (ladyzhenskaya_oneD c h0).trans ?_
  have hL2 : (0 : ℝ) ≤ ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure :=
    integral_nonneg_of_ae (ae_of_all _ fun x => pow_nonneg (norm_nonneg _) _)
  have hHe : (0 : ℝ) ≤ ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure :=
    integral_nonneg_of_ae (ae_of_all _ fun x => pow_nonneg (norm_nonneg _) _)
  have hadd : ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure ≤
      (∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) +
        ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure :=
    le_add_of_nonneg_left hL2
  have h2 := mul_le_mul_of_nonneg_left hadd hL2
  have h3 := mul_le_mul_of_nonneg_left h2 (show (0 : ℝ) ≤ 1 / 12 by norm_num)
  convert h3 using 1 <;> ring

/-- **一般（免均值）加权 Cauchy–Schwarz**：k = 0 权取 1，
`(Σ‖c‖)² ≤ (1 + π²/3)·Σ (1 + k²)‖c‖²`。 -/
theorem sum_norm_sq_weighted_general (c : ℤ →₀ ℂ) :
    (∑ k ∈ c.support, ‖c k‖) ^ 2 ≤
      (1 + Real.pi ^ 2 / 3) * ∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2 := by
  classical
  have hCS := sum_mul_sq_le_sq_mul_sq c.support
    (fun k => (if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖c k‖)
    (fun k => if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|)
  have hab : ∀ k ∈ c.support,
      (if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖c k‖ *
        (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) = ‖c k‖ := by
    intro k _
    by_cases hk : k = 0
    · subst hk; simp
    · rw [if_neg hk, if_neg hk]
      have hkn : |(k : ℝ)| ≠ 0 :=
        abs_ne_zero.mpr (by exact_mod_cast hk : (k : ℝ) ≠ 0)
      field_simp
  rw [Finset.sum_congr rfl hab] at hCS
  have hA : (∑ k ∈ c.support, ((if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖c k‖) ^ 2) ≤
      ∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2 := by
    apply Finset.sum_le_sum
    intro k _
    rw [mul_pow]
    by_cases hk : k = 0
    · subst hk; simp
    · rw [if_neg hk, sq_abs]
      apply mul_le_mul_of_nonneg_right _ (sq_nonneg _)
      linarith [sq_nonneg (k : ℝ)]
  have hB : (∑ k ∈ c.support, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2) ≤
      1 + Real.pi ^ 2 / 3 := by
    have hbb : ∀ k : ℤ, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2 =
        (if k = 0 then (1 : ℝ) else 0) + (if k = 0 then (0 : ℝ) else 1 / (k : ℝ) ^ 2) := by
      intro k
      by_cases hk : k = 0
      · simp [hk]
      · rw [if_neg hk, if_neg hk, if_neg hk, div_pow, one_pow, sq_abs, zero_add]
    rw [Finset.sum_congr rfl (fun k _ => hbb k), Finset.sum_add_distrib]
    have hind : (∑ k ∈ c.support, if k = 0 then (1 : ℝ) else 0) ≤ 1 := by
      rw [← Finset.sum_filter, Finset.filter_eq']
      by_cases h0s : (0 : ℤ) ∈ c.support <;> simp [h0s]
    linarith [hind, sum_inv_sq_le c.support]
  calc (∑ k ∈ c.support, ‖c k‖) ^ 2
      ≤ (∑ k ∈ c.support, ((if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖c k‖) ^ 2) *
          ∑ k ∈ c.support, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2 := hCS
    _ ≤ (∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2) *
          ∑ k ∈ c.support, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2 :=
        mul_le_mul_of_nonneg_right hA
          (Finset.sum_nonneg fun k _ => sq_nonneg _)
    _ ≤ (∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2) * (1 + Real.pi ^ 2 / 3) :=
        mul_le_mul_of_nonneg_left hB
          (Finset.sum_nonneg fun k _ => mul_nonneg
            (add_nonneg zero_le_one (sq_nonneg _)) (sq_nonneg _))
    _ = (1 + Real.pi ^ 2 / 3) * ∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2 :=
        mul_comm _ _

/-- **1D 周期 Ladyzhenskaya（免均值一般形式，显式常数 1 + π²/3）**：
`∫‖u‖⁴ ≤ (1 + π²/3)·(∫‖u‖²)·(∫‖u‖² + (2π)⁻²∫‖∂u‖²)`
（`Σ(1+k²)‖c‖² = Σ‖c‖² + (2π)⁻²·(2π)²Σk²‖c‖²` 回代）。 -/
theorem ladyzhenskaya_oneD_general (c : ℤ →₀ ℂ) :
    ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure ≤
      (1 + Real.pi ^ 2 / 3) * (∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) *
        ((∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) +
          (1 / (2 * Real.pi) ^ 2) *
            ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure) := by
  rw [integral_norm_sq_fourierPoly1, integral_norm_sq_pderivPoly1]
  have hπ : (0 : ℝ) < Real.pi := Real.pi_pos
  have hsplit : (∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2) =
      (∑ l ∈ c.support, ‖c l‖ ^ 2) +
        (1 / (2 * Real.pi) ^ 2) *
          ((2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2) := by
    have hterm : ∀ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2 =
        ‖c k‖ ^ 2 + (k : ℝ) ^ 2 * ‖c k‖ ^ 2 := fun k _ => by ring
    rw [Finset.sum_congr rfl hterm, Finset.sum_add_distrib, one_div, ← mul_assoc,
      inv_mul_cancel₀ (ne_of_gt (pow_pos (mul_pos zero_lt_two Real.pi_pos) 2)), one_mul]
  calc ∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 4 ∂circleMeasure
      ≤ (∑ k ∈ c.support, ‖c k‖) ^ 2 * (∑ l ∈ c.support, ‖c l‖ ^ 2) :=
        integral_norm_pow_four_le1 c
    _ ≤ ((1 + Real.pi ^ 2 / 3) * ∑ k ∈ c.support, (1 + (k : ℝ) ^ 2) * ‖c k‖ ^ 2) *
          (∑ l ∈ c.support, ‖c l‖ ^ 2) :=
        mul_le_mul_of_nonneg_right (sum_norm_sq_weighted_general c)
          (Finset.sum_nonneg fun l _ => sq_nonneg _)
    _ = (1 + Real.pi ^ 2 / 3) * (∑ l ∈ c.support, ‖c l‖ ^ 2) *
          ((∑ l ∈ c.support, ‖c l‖ ^ 2) +
            (1 / (2 * Real.pi) ^ 2) *
              ((2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2)) := by
        rw [hsplit]; ring

end OneDim

section TwoDim
/-! ### (vii) 2D 周期 Ladyzhenskaya：可乘型各向异性切片路线（L5 批三，证毕）

【路线】（禁走 2D 朴素谱线 `Σ|k|⁻²`——对数发散，可加型死路判词保留）
可乘型（张量权）切片路线，全程**点态**估计（三角多项式连续，免 a.e. 限定）
+ 乘积测度 Fubini 分离：

  (a) 片分解：`u(x,y) = Σ_m d_m(x)·fourier m y`，
      `d_m(x) = Σ_{k, k₂=m} c_k·fourier (k₀) x`（`sliceSumY`，纤维重组
      `sum_fiberwise_of_maps_to`）；x 向对称件 `sliceSumX`；
  (b) 点态可乘型切片嵌入（1D 阈值加权 CS 的逐片化，常数 1+π²/3，
      巴塞尔截断 `sum_inv_sq_le` 经 `sum_inv_weight_sq_le` 供给）：
      `‖u(x,y)‖² ≤ (1+π²/3)·Σ_m(1+m²)‖d_m(x)‖²` ——两向相乘得点态主界
      `‖u‖⁴ ≤ (1+π²/3)²·P₂(x)·P₁(y)`（`norm_pow_four_fourierPoly2_le`）；
  (c) 乘积测度分离（`torus2Measure = circleMeasure.prod circleMeasure`，
      `integral_prod_mul`）+ 注入指标 1D Parseval
      （`integral_norm_sq_sum_fourier_injOn`：片系数 `d_m` 本身作为 x 的
      1D 三角多项式，其 L² 能量恰为第 m 纤维的谱能量）收拢：
      `∫‖u‖⁴ ≤ (1+π²/3)²·(Σ_k(1+k₀²)‖c_k‖²)·(Σ_k(1+k₁²)‖c_k‖²)`；
  (d) 乘积侧 Parseval（`integral_prod_norm_sq_sum`，双重 1D Parseval
      迭代，免 `Measure.pi` 桥）把谱和回代为 `∫‖u‖²` 与 `∫‖∂ᵢu‖²`。

【可乘型注记】权 (1+k₀²)(1+k₁²) 的倒数和 `Σ_{ℤ²}[(1+k₀²)(1+k₁²)]⁻¹`
= (1+π²/3)² **收敛**（张量因子化），与可加型权 (1+|k|²)⁻¹ 的 2D 对数发散
形成对照——这是本路线可行而朴素谱线不可行的原因。逐片只用单向权，
混合导数项 k₀²k₁² 不出现（混合导数问题的本路线处理：由各向异性
因子乘积吸收，见头注未完登记对 C·X·Y 纯可乘形的限制说明）。 -/

/-- 2D 测度钉：圆周归一化 Haar 测度的乘积
（𝕋² 取任务口径的乘积形式 `UnitAddCircle × UnitAddCircle`）。 -/
abbrev torus2Measure : Measure (UnitAddCircle × UnitAddCircle) :=
  circleMeasure.prod circleMeasure

/-- 紧空间有限测度上连续实值函数可积（圆周版）。 -/
theorem integrable_continuous_circle {f : UnitAddCircle → ℝ} (hf : Continuous f) :
    Integrable f circleMeasure :=
  integrableOn_univ.mp (ContinuousOn.integrableOn_compact isCompact_univ hf.continuousOn)

/-- 紧空间有限测度上连续实值函数可积（乘积环面版）。 -/
theorem integrable_continuous_torus2 {f : UnitAddCircle × UnitAddCircle → ℝ}
    (hf : Continuous f) : Integrable f torus2Measure :=
  integrableOn_univ.mp (ContinuousOn.integrableOn_compact isCompact_univ hf.continuousOn)

/-- 2D 三角多项式（乘积形式）：`u(x,y) = Σ_k c_k·fourier (k 0) x·fourier (k 1) y`。 -/
def fourierPoly2 (c : WaveIdx →₀ ℂ) (z : UnitAddCircle × UnitAddCircle) : ℂ :=
  ∑ k ∈ c.support, c k * (fourier (k 0) z.1 * fourier (k 1) z.2)

/-- 2D 偏导多项式（乘积形式，第 `i` 坐标）：系数逐项乘 `2πi·kᵢ`。 -/
def pderivPoly2 (i : Fin 2) (c : WaveIdx →₀ ℂ) (z : UnitAddCircle × UnitAddCircle) : ℂ :=
  ∑ k ∈ c.support, (2 * Real.pi * Complex.I * (k i : ℂ) * c k) *
    (fourier (k 0) z.1 * fourier (k 1) z.2)

/-- 2D 三角多项式连续。 -/
theorem continuous_fourierPoly2 (c : WaveIdx →₀ ℂ) : Continuous (fourierPoly2 c) :=
  continuous_finsetSum _ fun k _ => continuous_const.mul
    (((fourier (k 0)).continuous.comp continuous_fst).mul
      ((fourier (k 1)).continuous.comp continuous_snd))

/-- y-片系数（通用支集/系数版）：固定 `x` 后 `y ↦ u(x,y)` 的第 `m` 个
Fourier 系数 `d_m(x) = Σ_{k∈s, k 1 = m} a_k·fourier (k 0) x`。 -/
def sliceSumY (s : Finset WaveIdx) (a : WaveIdx → ℂ) (x : UnitAddCircle) (m : ℤ) : ℂ :=
  ∑ k ∈ s.filter (fun k => k 1 = m), a k * fourier (k 0) x

/-- x-片系数（通用支集/系数版）：固定 `y` 后 `x ↦ u(x,y)` 的第 `n` 个
Fourier 系数。 -/
def sliceSumX (s : Finset WaveIdx) (a : WaveIdx → ℂ) (y : UnitAddCircle) (n : ℤ) : ℂ :=
  ∑ k ∈ s.filter (fun k => k 0 = n), a k * fourier (k 1) y

/-- 片系数关于片参数的连续性（y 向）。 -/
theorem continuous_sliceSumY (s : Finset WaveIdx) (a : WaveIdx → ℂ) (m : ℤ) :
    Continuous (fun x : UnitAddCircle => sliceSumY s a x m) :=
  continuous_finsetSum _ fun k _ => continuous_const.mul (fourier (k 0)).continuous

/-- 片系数关于片参数的连续性（x 向）。 -/
theorem continuous_sliceSumX (s : Finset WaveIdx) (a : WaveIdx → ℂ) (n : ℤ) :
    Continuous (fun y : UnitAddCircle => sliceSumX s a y n) :=
  continuous_finsetSum _ fun k _ => continuous_const.mul (fourier (k 1)).continuous

/-- **y-片重组**：双指标三角和按第二坐标波数 `k 1 = m` 的纤维分组，
即 `u(x,y) = Σ_m d_m(x)·fourier m y`。 -/
theorem sum_fourier_prod_eq_sum_sliceY (s : Finset WaveIdx) (a : WaveIdx → ℂ)
    (x y : UnitAddCircle) :
    (∑ k ∈ s, a k * (fourier (k 0) x * fourier (k 1) y)) =
      ∑ m ∈ s.image (fun k => k 1), sliceSumY s a x m * fourier m y := by
  classical
  rw [← Finset.sum_fiberwise_of_maps_to (g := fun k : WaveIdx => k 1)
    (t := s.image fun k => k 1) (fun k hk => Finset.mem_image_of_mem _ hk)
    (f := fun k => a k * (fourier (k 0) x * fourier (k 1) y))]
  apply Finset.sum_congr rfl; intro m _
  unfold sliceSumY
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl; intro k hk
  rw [Finset.mem_filter] at hk
  rw [hk.2]; ring

/-- **x-片重组**：按第一坐标波数 `k 0 = n` 的纤维分组，
即 `u(x,y) = Σ_n e_n(y)·fourier n x`。 -/
theorem sum_fourier_prod_eq_sum_sliceX (s : Finset WaveIdx) (a : WaveIdx → ℂ)
    (x y : UnitAddCircle) :
    (∑ k ∈ s, a k * (fourier (k 0) x * fourier (k 1) y)) =
      ∑ n ∈ s.image (fun k => k 0), sliceSumX s a y n * fourier n x := by
  classical
  rw [← Finset.sum_fiberwise_of_maps_to (g := fun k : WaveIdx => k 0)
    (t := s.image fun k => k 0) (fun k hk => Finset.mem_image_of_mem _ hk)
    (f := fun k => a k * (fourier (k 0) x * fourier (k 1) y))]
  apply Finset.sum_congr rfl; intro n _
  unfold sliceSumX
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl; intro k hk
  rw [Finset.mem_filter] at hk
  rw [hk.2]; ring

/-- 阈值权倒数平方和界（免均值）：`Σ_{k∈s} w_k⁻² ≤ 1 + π²/3`，
`w₀ = 1`、`w_k = |k|`（k≠0）；零模贡献 1，非零模由巴塞尔截断
`sum_inv_sq_le` 供给 `π²/3`。 -/
theorem sum_inv_weight_sq_le (s : Finset ℤ) :
    ∑ k ∈ s, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2 ≤ 1 + Real.pi ^ 2 / 3 := by
  classical
  have hbb : ∀ k : ℤ, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2 =
      (if k = 0 then (1 : ℝ) else 0) + (if k = 0 then (0 : ℝ) else 1 / (k : ℝ) ^ 2) := by
    intro k
    by_cases hk : k = 0
    · simp [hk]
    · rw [if_neg hk, if_neg hk, if_neg hk, div_pow, one_pow, sq_abs, zero_add]
  rw [Finset.sum_congr rfl (fun k _ => hbb k), Finset.sum_add_distrib]
  have hind : (∑ k ∈ s, if k = 0 then (1 : ℝ) else 0) ≤ 1 := by
    rw [← Finset.sum_filter, Finset.filter_eq']
    by_cases h0s : (0 : ℤ) ∈ s <;> simp [h0s]
  linarith [hind, sum_inv_sq_le s]

/-- **1D 阈值加权 Cauchy–Schwarz（通用系数版）**：
`(Σ‖a‖)² ≤ (1+π²/3)·Σ(1+k²)‖a‖²`（任意系数函数、任意有限求和集；
`sum_norm_sq_weighted_general` 的同形推广，供片系数逐点使用）。 -/
theorem sum_norm_sq_le_weighted (s : Finset ℤ) (a : ℤ → ℂ) :
    (∑ k ∈ s, ‖a k‖) ^ 2 ≤
      (1 + Real.pi ^ 2 / 3) * ∑ k ∈ s, ‖a k‖ ^ 2 * (1 + (k : ℝ) ^ 2) := by
  classical
  have hCS := sum_mul_sq_le_sq_mul_sq s
    (fun k => (if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖a k‖)
    (fun k => if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|)
  have hab : ∀ k ∈ s,
      (if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖a k‖ *
        (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) = ‖a k‖ := by
    intro k _
    by_cases hk : k = 0
    · subst hk; simp
    · rw [if_neg hk, if_neg hk]
      have hkn : |(k : ℝ)| ≠ 0 := abs_ne_zero.mpr (by exact_mod_cast hk : (k : ℝ) ≠ 0)
      field_simp
  rw [Finset.sum_congr rfl hab] at hCS
  have hA : (∑ k ∈ s, ((if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖a k‖) ^ 2) ≤
      ∑ k ∈ s, (1 + (k : ℝ) ^ 2) * ‖a k‖ ^ 2 := by
    apply Finset.sum_le_sum
    intro k _
    rw [mul_pow]
    by_cases hk : k = 0
    · subst hk; simp
    · rw [if_neg hk, sq_abs]
      apply mul_le_mul_of_nonneg_right _ (sq_nonneg _)
      linarith [sq_nonneg (k : ℝ)]
  have hB := sum_inv_weight_sq_le s
  calc (∑ k ∈ s, ‖a k‖) ^ 2
      ≤ (∑ k ∈ s, ((if k = 0 then (1 : ℝ) else |(k : ℝ)|) * ‖a k‖) ^ 2) *
          ∑ k ∈ s, (if k = 0 then (1 : ℝ) else 1 / |(k : ℝ)|) ^ 2 := hCS
    _ ≤ (∑ k ∈ s, (1 + (k : ℝ) ^ 2) * ‖a k‖ ^ 2) * (1 + Real.pi ^ 2 / 3) :=
        mul_le_mul hA hB (Finset.sum_nonneg fun k _ => sq_nonneg _)
          (Finset.sum_nonneg fun k _ => mul_nonneg
            (add_nonneg zero_le_one (sq_nonneg _)) (sq_nonneg _))
    _ = (1 + Real.pi ^ 2 / 3) * ∑ k ∈ s, ‖a k‖ ^ 2 * (1 + (k : ℝ) ^ 2) := by
        rw [Finset.sum_congr rfl (fun k _ => mul_comm _ _), mul_comm]

/-- y 向片能量密度：`P₂(x) = Σ_m ‖d_m(x)‖²·(1+m²)`
（乘积序取「应用在前」：`sliceSumY … m` 先把 `m` 钉为 `ℤ`，规避
裸变量类型标注 `(m : ℝ)` 的推断陷阱）。 -/
def sliceEnergyY (c : WaveIdx →₀ ℂ) (x : UnitAddCircle) : ℝ :=
  ∑ m ∈ c.support.image (fun k => k 1), ‖sliceSumY c.support c x m‖ ^ 2 * (1 + (m : ℝ) ^ 2)

/-- x 向片能量密度：`P₁(y) = Σ_n ‖e_n(y)‖²·(1+n²)`。 -/
def sliceEnergyX (c : WaveIdx →₀ ℂ) (y : UnitAddCircle) : ℝ :=
  ∑ n ∈ c.support.image (fun k => k 0), ‖sliceSumX c.support c y n‖ ^ 2 * (1 + (n : ℝ) ^ 2)

/-- 片能量密度连续（y 向）。 -/
theorem continuous_sliceEnergyY (c : WaveIdx →₀ ℂ) : Continuous (sliceEnergyY c) :=
  continuous_finsetSum _ fun m _ =>
    (((continuous_sliceSumY _ _ _).norm).pow 2).mul continuous_const

/-- 片能量密度连续（x 向）。 -/
theorem continuous_sliceEnergyX (c : WaveIdx →₀ ℂ) : Continuous (sliceEnergyX c) :=
  continuous_finsetSum _ fun n _ =>
    (((continuous_sliceSumX _ _ _).norm).pow 2).mul continuous_const

/-- **点态可乘型切片嵌入（y 向）**：固定 `x` 的 y-片视为 1D 三角多项式，
逐点三角不等式（字符模长 1）+ 阈值加权 CS：
`‖u(x,y)‖² ≤ (1+π²/3)·P₂(x)`（`P₂` 即 `sliceEnergyY`）。 -/
theorem norm_sq_fourierPoly2_le_sliceY (c : WaveIdx →₀ ℂ) (x y : UnitAddCircle) :
    ‖fourierPoly2 c (x, y)‖ ^ 2 ≤ (1 + Real.pi ^ 2 / 3) * sliceEnergyY c x := by
  classical
  have h1 : ‖fourierPoly2 c (x, y)‖ ≤
      ∑ m ∈ c.support.image (fun k => k 1), ‖sliceSumY c.support c x m‖ := by
    rw [show fourierPoly2 c (x, y) =
        ∑ k ∈ c.support, c k * (fourier (k 0) x * fourier (k 1) y) from rfl,
      sum_fourier_prod_eq_sum_sliceY]
    calc ‖∑ m ∈ c.support.image (fun k => k 1), sliceSumY c.support c x m * fourier m y‖
        ≤ ∑ m ∈ c.support.image (fun k => k 1),
            ‖sliceSumY c.support c x m * fourier m y‖ := norm_sum_le _ _
      _ = ∑ m ∈ c.support.image (fun k => k 1), ‖sliceSumY c.support c x m‖ := by
          apply Finset.sum_congr rfl; intro m _
          rw [norm_mul, show ‖fourier m y‖ = 1 by
            rw [fourier_apply]; exact Circle.norm_coe _, mul_one]
  calc ‖fourierPoly2 c (x, y)‖ ^ 2
      ≤ (∑ m ∈ c.support.image (fun k => k 1), ‖sliceSumY c.support c x m‖) ^ 2 :=
        pow_le_pow_left₀ (norm_nonneg _) h1 _
    _ ≤ (1 + Real.pi ^ 2 / 3) * sliceEnergyY c x := by
        unfold sliceEnergyY
        exact sum_norm_sq_le_weighted _ _

/-- **点态可乘型切片嵌入（x 向）**：`‖u(x,y)‖² ≤ (1+π²/3)·Σ_n(1+n²)‖e_n(y)‖²`。 -/
theorem norm_sq_fourierPoly2_le_sliceX (c : WaveIdx →₀ ℂ) (x y : UnitAddCircle) :
    ‖fourierPoly2 c (x, y)‖ ^ 2 ≤ (1 + Real.pi ^ 2 / 3) * sliceEnergyX c y := by
  classical
  have h1 : ‖fourierPoly2 c (x, y)‖ ≤
      ∑ n ∈ c.support.image (fun k => k 0), ‖sliceSumX c.support c y n‖ := by
    rw [show fourierPoly2 c (x, y) =
        ∑ k ∈ c.support, c k * (fourier (k 0) x * fourier (k 1) y) from rfl,
      sum_fourier_prod_eq_sum_sliceX]
    calc ‖∑ n ∈ c.support.image (fun k => k 0), sliceSumX c.support c y n * fourier n x‖
        ≤ ∑ n ∈ c.support.image (fun k => k 0),
            ‖sliceSumX c.support c y n * fourier n x‖ := norm_sum_le _ _
      _ = ∑ n ∈ c.support.image (fun k => k 0), ‖sliceSumX c.support c y n‖ := by
          apply Finset.sum_congr rfl; intro n _
          rw [norm_mul, show ‖fourier n x‖ = 1 by
            rw [fourier_apply]; exact Circle.norm_coe _, mul_one]
  calc ‖fourierPoly2 c (x, y)‖ ^ 2
      ≤ (∑ n ∈ c.support.image (fun k => k 0), ‖sliceSumX c.support c y n‖) ^ 2 :=
        pow_le_pow_left₀ (norm_nonneg _) h1 _
    _ ≤ (1 + Real.pi ^ 2 / 3) * sliceEnergyX c y := by
        unfold sliceEnergyX
        exact sum_norm_sq_le_weighted _ _

/-- **点态可乘型主界**：`‖u(x,y)‖⁴ ≤ (1+π²/3)²·P₂(x)·P₁(y)`
（两向切片嵌入逐点相乘；各项非负，可乘）。 -/
theorem norm_pow_four_fourierPoly2_le (c : WaveIdx →₀ ℂ) (x y : UnitAddCircle) :
    ‖fourierPoly2 c (x, y)‖ ^ 4 ≤
      (1 + Real.pi ^ 2 / 3) ^ 2 * (sliceEnergyY c x * sliceEnergyX c y) := by
  have hY := norm_sq_fourierPoly2_le_sliceY c x y
  have hX := norm_sq_fourierPoly2_le_sliceX c x y
  have hK : (0 : ℝ) ≤ 1 + Real.pi ^ 2 / 3 :=
    add_nonneg zero_le_one (div_nonneg (sq_nonneg _) (by norm_num))
  have hP2 : (0 : ℝ) ≤ sliceEnergyY c x :=
    Finset.sum_nonneg fun m _ => mul_nonneg (sq_nonneg _)
      (add_nonneg zero_le_one (sq_nonneg _))
  have hP1 : (0 : ℝ) ≤ sliceEnergyX c y :=
    Finset.sum_nonneg fun n _ => mul_nonneg (sq_nonneg _)
      (add_nonneg zero_le_one (sq_nonneg _))
  have h4 : ‖fourierPoly2 c (x, y)‖ ^ 4 =
      ‖fourierPoly2 c (x, y)‖ ^ 2 * ‖fourierPoly2 c (x, y)‖ ^ 2 := by ring
  rw [h4]
  calc ‖fourierPoly2 c (x, y)‖ ^ 2 * ‖fourierPoly2 c (x, y)‖ ^ 2
      ≤ ((1 + Real.pi ^ 2 / 3) * sliceEnergyY c x) *
          ((1 + Real.pi ^ 2 / 3) * sliceEnergyX c y) :=
        mul_le_mul hY hX (pow_nonneg (norm_nonneg _) _) (mul_nonneg hK hP2)
    _ = (1 + Real.pi ^ 2 / 3) ^ 2 * (sliceEnergyY c x * sliceEnergyX c y) := by ring

/-- **注入指标的 1D Parseval 变体**：指标经单射 `g : ι → ℤ` 嵌入时，
`∫‖Σ_{k∈s} a_k·fourier (g k)‖² = Σ‖a_k‖²`（纤维单例化归约到
`integral_norm_sq_sum_fourier`；片系数作为 x 的 1D 多项式解析所需）。 -/
theorem integral_norm_sq_sum_fourier_injOn {ι : Type*} [DecidableEq ι]
    (s : Finset ι) (g : ι → ℤ) (hg : Set.InjOn g s) (a : ι → ℂ) :
    ∫ x : UnitAddCircle, ‖∑ k ∈ s, a k * fourier (g k) x‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ s, ‖a k‖ ^ 2 := by
  classical
  have hreg : ∀ x : UnitAddCircle, (∑ k ∈ s, a k * fourier (g k) x) =
      ∑ j ∈ s.image g, (∑ k ∈ s.filter (fun k => g k = j), a k) * fourier j x := by
    intro x
    rw [← Finset.sum_fiberwise_of_maps_to (g := g) (t := s.image g)
      (fun k hk => Finset.mem_image_of_mem _ hk) (f := fun k => a k * fourier (g k) x)]
    apply Finset.sum_congr rfl; intro j _
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl; intro k hk
    rw [Finset.mem_filter] at hk
    rw [hk.2]
  rw [integral_congr_ae (ae_of_all _ fun x => by rw [hreg x])]
  rw [integral_norm_sq_sum_fourier]
  rw [← Finset.sum_fiberwise_of_maps_to (g := g) (t := s.image g)
    (fun k hk => Finset.mem_image_of_mem _ hk) (f := fun k => ‖a k‖ ^ 2)]
  apply Finset.sum_congr rfl; intro j hj
  rcases Finset.mem_image.mp hj with ⟨k₀, hk₀, rfl⟩
  have hfilter : s.filter (fun k => g k = g k₀) = {k₀} := by
    apply Finset.eq_singleton_iff_unique_mem.mpr
    refine ⟨Finset.mem_filter.mpr ⟨hk₀, rfl⟩, ?_⟩
    intro k hk
    rw [Finset.mem_filter] at hk
    exact hg (Finset.mem_coe.mpr hk.1) (Finset.mem_coe.mpr hk₀) hk.2
  rw [hfilter]
  simp

/-- y-片能量的 x 积分 = 第 `m` 纤维的谱能量（注入指标 Parseval；
指标映射 `k ↦ k 0` 在纤维 `k 1 = m` 上单射：两坐标共同决定波数）。 -/
theorem integral_norm_sq_sliceSumY_gen (s : Finset WaveIdx) (a : WaveIdx → ℂ) (m : ℤ) :
    ∫ x : UnitAddCircle, ‖sliceSumY s a x m‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ s.filter (fun k => k 1 = m), ‖a k‖ ^ 2 := by
  classical
  unfold sliceSumY
  refine integral_norm_sq_sum_fourier_injOn _ _ ?_ _
  intro k₁ hk₁ k₂ hk₂ h
  rw [Finset.mem_coe, Finset.mem_filter] at hk₁ hk₂
  funext i
  fin_cases i
  · exact h
  · exact hk₁.2.trans hk₂.2.symm

/-- x-片能量的 y 积分 = 第 `n` 纤维的谱能量（同构对称件）。 -/
theorem integral_norm_sq_sliceSumX_gen (s : Finset WaveIdx) (a : WaveIdx → ℂ) (n : ℤ) :
    ∫ y : UnitAddCircle, ‖sliceSumX s a y n‖ ^ 2 ∂circleMeasure =
      ∑ k ∈ s.filter (fun k => k 0 = n), ‖a k‖ ^ 2 := by
  classical
  unfold sliceSumX
  refine integral_norm_sq_sum_fourier_injOn _ _ ?_ _
  intro k₁ hk₁ k₂ hk₂ h
  rw [Finset.mem_coe, Finset.mem_filter] at hk₁ hk₂
  funext i
  fin_cases i
  · exact hk₁.2.trans hk₂.2.symm
  · exact h

/-- **片能量密度的全积分（y 向）**：`∫P₂ = Σ_k(1+(k 1)²)‖c_k‖²`
（逐项积分 + 纤维 Parseval + 纤维重组回并）。 -/
theorem integral_sliceEnergyY (c : WaveIdx →₀ ℂ) :
    ∫ x : UnitAddCircle, sliceEnergyY c x ∂circleMeasure =
      ∑ k ∈ c.support, (1 + (k 1 : ℝ) ^ 2) * ‖c k‖ ^ 2 := by
  classical
  unfold sliceEnergyY
  rw [integral_finsetSum (c.support.image fun k => k 1)
    (f := fun m x => ‖sliceSumY c.support c x m‖ ^ 2 * (1 + (m : ℝ) ^ 2))
    (fun m _ => integrable_continuous_circle
      (((continuous_sliceSumY _ _ _).norm.pow 2).mul continuous_const))]
  conv_rhs => rw [← Finset.sum_fiberwise_of_maps_to (g := fun k : WaveIdx => k 1)
    (t := c.support.image fun k => k 1) (fun k hk => Finset.mem_image_of_mem _ hk)
    (f := fun k => (1 + (k 1 : ℝ) ^ 2) * ‖c k‖ ^ 2)]
  apply Finset.sum_congr rfl; intro m _
  rw [integral_mul_const, integral_norm_sq_sliceSumY_gen, Finset.sum_mul]
  apply Finset.sum_congr rfl; intro k hk
  rw [Finset.mem_filter] at hk
  rw [hk.2]; ring

/-- **片能量密度的全积分（x 向）**：`∫P₁ = Σ_k(1+(k 0)²)‖c_k‖²`。 -/
theorem integral_sliceEnergyX (c : WaveIdx →₀ ℂ) :
    ∫ y : UnitAddCircle, sliceEnergyX c y ∂circleMeasure =
      ∑ k ∈ c.support, (1 + (k 0 : ℝ) ^ 2) * ‖c k‖ ^ 2 := by
  classical
  unfold sliceEnergyX
  rw [integral_finsetSum (c.support.image fun k => k 0)
    (f := fun n y => ‖sliceSumX c.support c y n‖ ^ 2 * (1 + (n : ℝ) ^ 2))
    (fun n _ => integrable_continuous_circle
      (((continuous_sliceSumX _ _ _).norm.pow 2).mul continuous_const))]
  conv_rhs => rw [← Finset.sum_fiberwise_of_maps_to (g := fun k : WaveIdx => k 0)
    (t := c.support.image fun k => k 0) (fun k hk => Finset.mem_image_of_mem _ hk)
    (f := fun k => (1 + (k 0 : ℝ) ^ 2) * ‖c k‖ ^ 2)]
  apply Finset.sum_congr rfl; intro n _
  rw [integral_mul_const, integral_norm_sq_sliceSumX_gen, Finset.sum_mul]
  apply Finset.sum_congr rfl; intro k hk
  rw [Finset.mem_filter] at hk
  rw [hk.2]; ring

/-- **乘积侧一般 Parseval**：双指标有限三角和的 L² 能量 = 系数平方和
（`integral_prod` 迭代 + 片重组 + 1D Parseval；免 `Measure.pi` 桥）。 -/
theorem integral_prod_norm_sq_sum (s : Finset WaveIdx) (a : WaveIdx → ℂ) :
    ∫ z : UnitAddCircle × UnitAddCircle,
        ‖∑ k ∈ s, a k * (fourier (k 0) z.1 * fourier (k 1) z.2)‖ ^ 2 ∂torus2Measure =
      ∑ k ∈ s, ‖a k‖ ^ 2 := by
  classical
  have hcont : Continuous (fun z : UnitAddCircle × UnitAddCircle =>
      ‖∑ k ∈ s, a k * (fourier (k 0) z.1 * fourier (k 1) z.2)‖ ^ 2) :=
    ((continuous_finsetSum _ fun k _ => continuous_const.mul
      (((fourier (k 0)).continuous.comp continuous_fst).mul
        ((fourier (k 1)).continuous.comp continuous_snd))).norm).pow 2
  rw [integral_prod _ (integrable_continuous_torus2 hcont)]
  have hin : ∀ x : UnitAddCircle,
      ∫ y : UnitAddCircle,
          ‖∑ k ∈ s, a k * (fourier (k 0) x * fourier (k 1) y)‖ ^ 2 ∂circleMeasure =
        ∑ m ∈ s.image (fun k => k 1), ‖sliceSumY s a x m‖ ^ 2 := by
    intro x
    rw [integral_congr_ae (ae_of_all _ fun y => by rw [sum_fourier_prod_eq_sum_sliceY])]
    exact integral_norm_sq_sum_fourier _ _
  rw [integral_congr_ae (ae_of_all _ hin)]
  rw [integral_finsetSum (s.image fun k => k 1)
    (f := fun m x => ‖sliceSumY s a x m‖ ^ 2)
    (fun m _ => integrable_continuous_circle ((continuous_sliceSumY _ _ _).norm.pow 2))]
  rw [← Finset.sum_fiberwise_of_maps_to (g := fun k : WaveIdx => k 1)
    (t := s.image fun k => k 1) (fun k hk => Finset.mem_image_of_mem _ hk)
    (f := fun k => ‖a k‖ ^ 2)]
  apply Finset.sum_congr rfl; intro m _
  exact integral_norm_sq_sliceSumY_gen s a m

/-- **乘积侧 L² Parseval（fourierPoly2 版）**：`∫‖u‖² = Σ‖c_k‖²`。 -/
theorem integral_norm_sq_fourierPoly2 (c : WaveIdx →₀ ℂ) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure =
      ∑ k ∈ c.support, ‖c k‖ ^ 2 := by
  unfold fourierPoly2
  exact integral_prod_norm_sq_sum c.support c

/-- **乘积侧偏导能量（谱形式）**：`∫‖∂ᵢu‖² = (2π)²·Σ kᵢ²‖c_k‖²`。 -/
theorem integral_norm_sq_pderivPoly2 (i : Fin 2) (c : WaveIdx →₀ ℂ) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 i c z‖ ^ 2 ∂torus2Measure =
      (2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k i : ℝ) ^ 2 * ‖c k‖ ^ 2 := by
  have hn : ∀ k : WaveIdx,
      ‖2 * Real.pi * Complex.I * (k i : ℂ) * c k‖ =
        2 * Real.pi * |(k i : ℝ)| * ‖c k‖ := by
    intro k
    have h2pi : ((2 : ℂ) * (Real.pi : ℂ)) = ((2 * Real.pi : ℝ) : ℂ) := by
      push_cast; ring
    rw [h2pi, norm_mul, norm_mul, norm_mul, Complex.norm_real, Complex.norm_I,
      Complex.norm_intCast, mul_one, Real.norm_eq_abs,
      abs_of_pos (mul_pos zero_lt_two Real.pi_pos)]
  have hmain : ∫ z : UnitAddCircle × UnitAddCircle,
      ‖pderivPoly2 i c z‖ ^ 2 ∂torus2Measure =
      ∑ k ∈ c.support, ‖2 * Real.pi * Complex.I * (k i : ℂ) * c k‖ ^ 2 := by
    unfold pderivPoly2
    exact integral_prod_norm_sq_sum c.support _
  rw [hmain, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [hn k, mul_pow, mul_pow, sq_abs]
  ring

/-- **2D 周期 Ladyzhenskaya（可乘型张量因子形，免均值，显式常数 (1+π²/3)²）**：
`∫‖u‖⁴ ≤ (1+π²/3)²·(Σ_k(1+k₀²)‖c_k‖²)·(Σ_k(1+k₁²)‖c_k‖²)。
证明链：点态可乘型主界 ⇒ 积分单调性 ⇒ `integral_prod_mul` 分离
⇒ 两向片能量引理收拢。可乘型本质：张量权倒数和收敛（(1+π²/3)²）。 -/
theorem ladyzhenskaya_twoD_tensor (c : WaveIdx →₀ ℂ) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 4 ∂torus2Measure ≤
      (1 + Real.pi ^ 2 / 3) ^ 2 *
        (∑ k ∈ c.support, (1 + (k 0 : ℝ) ^ 2) * ‖c k‖ ^ 2) *
        (∑ k ∈ c.support, (1 + (k 1 : ℝ) ^ 2) * ‖c k‖ ^ 2) := by
  classical
  have hpt : ∀ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 4 ≤
      (1 + Real.pi ^ 2 / 3) ^ 2 * (sliceEnergyY c z.1 * sliceEnergyX c z.2) :=
    fun z => norm_pow_four_fourierPoly2_le c z.1 z.2
  have hL : Integrable (fun z : UnitAddCircle × UnitAddCircle =>
      ‖fourierPoly2 c z‖ ^ 4) torus2Measure :=
    integrable_continuous_torus2 (((continuous_fourierPoly2 c).norm).pow 4)
  have hR : Integrable (fun z : UnitAddCircle × UnitAddCircle =>
      (1 + Real.pi ^ 2 / 3) ^ 2 * (sliceEnergyY c z.1 * sliceEnergyX c z.2))
      torus2Measure :=
    integrable_continuous_torus2 (continuous_const.mul
      (((continuous_sliceEnergyY c).comp continuous_fst).mul
        ((continuous_sliceEnergyX c).comp continuous_snd)))
  calc ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 4 ∂torus2Measure
      ≤ ∫ z : UnitAddCircle × UnitAddCircle,
          (1 + Real.pi ^ 2 / 3) ^ 2 * (sliceEnergyY c z.1 * sliceEnergyX c z.2)
          ∂torus2Measure :=
        integral_mono hL hR hpt
    _ = (1 + Real.pi ^ 2 / 3) ^ 2 *
          (∫ x : UnitAddCircle, sliceEnergyY c x ∂circleMeasure) *
          (∫ y : UnitAddCircle, sliceEnergyX c y ∂circleMeasure) := by
        rw [integral_const_mul, integral_prod_mul]; ring
    _ = (1 + Real.pi ^ 2 / 3) ^ 2 *
          (∑ k ∈ c.support, (1 + (k 0 : ℝ) ^ 2) * ‖c k‖ ^ 2) *
          (∑ k ∈ c.support, (1 + (k 1 : ℝ) ^ 2) * ‖c k‖ ^ 2) := by
        rw [integral_sliceEnergyY, integral_sliceEnergyX]; ring

/-- 谱坐标 H¹ 权分解：`Σ(1+kᵢ²)‖c‖² = Σ‖c‖² + (2π)⁻²·(2π)²Σkᵢ²‖c‖²`。 -/
theorem sum_weighted_eq_h1 (i : Fin 2) (c : WaveIdx →₀ ℂ) :
    ∑ k ∈ c.support, (1 + (k i : ℝ) ^ 2) * ‖c k‖ ^ 2 =
      (∑ l ∈ c.support, ‖c l‖ ^ 2) +
        (1 / (2 * Real.pi) ^ 2) *
          ((2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k i : ℝ) ^ 2 * ‖c k‖ ^ 2) := by
  have hterm : ∀ k ∈ c.support, (1 + (k i : ℝ) ^ 2) * ‖c k‖ ^ 2 =
      ‖c k‖ ^ 2 + (k i : ℝ) ^ 2 * ‖c k‖ ^ 2 := fun k _ => by ring
  rw [Finset.sum_congr rfl hterm, Finset.sum_add_distrib, one_div, ← mul_assoc,
    inv_mul_cancel₀ (ne_of_gt (pow_pos (mul_pos zero_lt_two Real.pi_pos) 2)), one_mul]

/-- **2D 周期 Ladyzhenskaya（H¹ 收边形，免均值，显式常数 (1+π²/3)²）**：
`∫‖u‖⁴ ≤ (1+π²/3)²·(∫‖u‖²+(2π)⁻²∫‖∂₀u‖²)·(∫‖u‖²+(2π)⁻²∫‖∂₁u‖²)`。
张量因子形经乘积侧 Parseval/偏导能量回代。 -/
theorem ladyzhenskaya_twoD (c : WaveIdx →₀ ℂ) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 4 ∂torus2Measure ≤
      (1 + Real.pi ^ 2 / 3) ^ 2 *
        ((∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure) +
          (1 / (2 * Real.pi) ^ 2) *
            ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 0 c z‖ ^ 2 ∂torus2Measure) *
        ((∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure) +
          (1 / (2 * Real.pi) ^ 2) *
            ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 1 c z‖ ^ 2 ∂torus2Measure) := by
  refine (ladyzhenskaya_twoD_tensor c).trans ?_
  rw [integral_norm_sq_fourierPoly2, integral_norm_sq_pderivPoly2,
    integral_norm_sq_pderivPoly2, ← sum_weighted_eq_h1 0, ← sum_weighted_eq_h1 1]

/-- **2D 周期 Ladyzhenskaya（H¹ 范数平方收边，免均值）**：
`∫‖u‖⁴ ≤ (1+π²/3)²·(∫‖u‖² + (2π)⁻²(∫‖∂₀u‖²+∫‖∂₁u‖²))²`。 -/
theorem ladyzhenskaya_twoD_h1_sq (c : WaveIdx →₀ ℂ) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 4 ∂torus2Measure ≤
      (1 + Real.pi ^ 2 / 3) ^ 2 *
        ((∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure) +
          (1 / (2 * Real.pi) ^ 2) *
            ((∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 0 c z‖ ^ 2 ∂torus2Measure) +
              ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 1 c z‖ ^ 2 ∂torus2Measure)) ^ 2 := by
  refine (ladyzhenskaya_twoD c).trans ?_
  set X := ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure with hX
  set Y₀ := ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 0 c z‖ ^ 2 ∂torus2Measure with hY₀
  set Y₁ := ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 1 c z‖ ^ 2 ∂torus2Measure with hY₁
  set q : ℝ := 1 / (2 * Real.pi) ^ 2 with hq
  have hXn : 0 ≤ X := integral_nonneg_of_ae (ae_of_all _ fun z => pow_nonneg (norm_nonneg _) _)
  have hY₀n : 0 ≤ Y₀ := integral_nonneg_of_ae (ae_of_all _ fun z => pow_nonneg (norm_nonneg _) _)
  have hY₁n : 0 ≤ Y₁ := integral_nonneg_of_ae (ae_of_all _ fun z => pow_nonneg (norm_nonneg _) _)
  have hqn : 0 ≤ q := by
    rw [hq]
    exact div_nonneg zero_le_one (sq_nonneg _)
  have hF0 : X + q * Y₀ ≤ X + q * (Y₀ + Y₁) := by
    have h := mul_nonneg hqn hY₁n; linarith
  have hF1 : X + q * Y₁ ≤ X + q * (Y₀ + Y₁) := by
    have h := mul_nonneg hqn hY₀n; linarith
  have hT : 0 ≤ X + q * (Y₀ + Y₁) :=
    add_nonneg hXn (mul_nonneg hqn (add_nonneg hY₀n hY₁n))
  have hF1n : 0 ≤ X + q * Y₁ := add_nonneg hXn (mul_nonneg hqn hY₁n)
  calc (1 + Real.pi ^ 2 / 3) ^ 2 * (X + q * Y₀) * (X + q * Y₁)
      = (1 + Real.pi ^ 2 / 3) ^ 2 * ((X + q * Y₀) * (X + q * Y₁)) := by ring
    _ ≤ (1 + Real.pi ^ 2 / 3) ^ 2 * ((X + q * (Y₀ + Y₁)) * (X + q * (Y₀ + Y₁))) :=
        mul_le_mul_of_nonneg_left (mul_le_mul hF0 hF1 hF1n hT) (pow_nonneg
          (add_nonneg zero_le_one (div_nonneg (sq_nonneg _) (by norm_num))) _)
    _ = (1 + Real.pi ^ 2 / 3) ^ 2 * (X + q * (Y₀ + Y₁)) ^ 2 := by ring

/-- **零均值 Poincaré（乘积侧）**：`∫‖u‖² ≤ (2π)⁻²·(∫‖∂₀u‖²+∫‖∂₁u‖²)`
（谱级 `sum_norm_sq_le_specGradEnergy` 经乘积侧 Parseval 回代）。 -/
theorem integral_norm_sq_le_integral_pderiv2 (c : WaveIdx →₀ ℂ) (h0 : c 0 = 0) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure ≤
      (1 / (2 * Real.pi) ^ 2) *
        ((∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 0 c z‖ ^ 2 ∂torus2Measure) +
          ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 1 c z‖ ^ 2 ∂torus2Measure) := by
  rw [integral_norm_sq_fourierPoly2, integral_norm_sq_pderivPoly2, integral_norm_sq_pderivPoly2]
  have h := sum_norm_sq_le_specGradEnergy c h0
  have hE : (2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k 0 : ℝ) ^ 2 * ‖c k‖ ^ 2 +
      (2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k 1 : ℝ) ^ 2 * ‖c k‖ ^ 2 =
      specGradEnergy c := by
    rw [specGradEnergy, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl; intro k _
    simp only [kSq]; ring
  rwa [hE]

/-- **2D 周期 Ladyzhenskaya（零均值梯度平方形，显式常数 (1+π²/3)²/(4π⁴)）**：
`∫‖u‖⁴ ≤ ((1+π²/3)²/(4π⁴))·(∫‖∂₀u‖²+∫‖∂₁u‖²)²`
（H¹ 平方收边 + 零均值 Poincaré：`X ≤ (2π)⁻²Y` 把收边因子吸收为 `2(2π)⁻²Y`；
即 2D 零均值 GNS/Ladyzhenskaya 梯度形 `‖u‖₄⁴ ≤ C_L·‖∇u‖₂⁴`）。 -/
theorem ladyzhenskaya_twoD_zero_mean (c : WaveIdx →₀ ℂ) (h0 : c 0 = 0) :
    ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 4 ∂torus2Measure ≤
      ((1 + Real.pi ^ 2 / 3) ^ 2 / (4 * Real.pi ^ 4)) *
        ((∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 0 c z‖ ^ 2 ∂torus2Measure) +
          ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 1 c z‖ ^ 2 ∂torus2Measure) ^ 2 := by
  refine (ladyzhenskaya_twoD_h1_sq c).trans ?_
  set X := ∫ z : UnitAddCircle × UnitAddCircle, ‖fourierPoly2 c z‖ ^ 2 ∂torus2Measure with hX
  set Y := (∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 0 c z‖ ^ 2 ∂torus2Measure) +
    ∫ z : UnitAddCircle × UnitAddCircle, ‖pderivPoly2 1 c z‖ ^ 2 ∂torus2Measure with hY
  set q : ℝ := 1 / (2 * Real.pi) ^ 2 with hq
  have hYn : 0 ≤ Y :=
    add_nonneg (integral_nonneg_of_ae (ae_of_all _ fun z => pow_nonneg (norm_nonneg _) _))
      (integral_nonneg_of_ae (ae_of_all _ fun z => pow_nonneg (norm_nonneg _) _))
  have hqn : 0 ≤ q := by
    rw [hq]
    exact div_nonneg zero_le_one (sq_nonneg _)
  have hPo : X ≤ q * Y := integral_norm_sq_le_integral_pderiv2 c h0
  have hXn : 0 ≤ X := integral_nonneg_of_ae (ae_of_all _ fun z => pow_nonneg (norm_nonneg _) _)
  have hT : X + q * Y ≤ 2 * q * Y := by nlinarith [hPo, hqn, hYn]
  have hT0 : 0 ≤ X + q * Y := add_nonneg hXn (mul_nonneg hqn hYn)
  have hsq : (X + q * Y) ^ 2 ≤ (2 * q * Y) ^ 2 :=
    pow_le_pow_left₀ hT0 hT _
  have hKn : (0 : ℝ) ≤ (1 + Real.pi ^ 2 / 3) ^ 2 :=
    pow_nonneg (add_nonneg zero_le_one (div_nonneg (sq_nonneg _) (by norm_num))) _
  refine (mul_le_mul_of_nonneg_left hsq hKn).trans ?_
  apply le_of_eq
  have hπ : (0 : ℝ) < Real.pi := Real.pi_pos
  rw [hq]
  field_simp [hπ.ne']
  ring

end TwoDim

-- D-B1/D-B2 件公理审计（构建期打印；应仅见 propext/Classical.choice/Quot.sound）。
#print axioms sum_norm_sq_convC_le
#print axioms fourierPoly_mul
#print axioms integral_norm_pow_four_fourierPoly
#print axioms integral_norm_pow_four_le
#print axioms one_le_kSq_of_ne_zero
#print axioms sum_norm_sq_le_specGradEnergy
#print axioms hasDerivAt_mFourier_coord
#print axioms hasDerivAt_fourierPoly_coord
#print axioms integral_norm_sq_sum_mFourier
#print axioms integral_norm_sq_fourierPoly
#print axioms integral_norm_sq_pderivPoly
#print axioms specGradEnergy_eq_integral_pderiv
#print axioms integral_norm_sq_le_integral_pderiv
#print axioms integral_norm_sq_sum_fourier
#print axioms integral_norm_sq_fourierPoly1
#print axioms fourierPoly1_mul
#print axioms integral_norm_pow_four_fourierPoly1
#print axioms integral_norm_pow_four_le1
#print axioms hasDerivAt_fourierPoly1
#print axioms integral_norm_sq_pderivPoly1
#print axioms sum_inv_sq_le
#print axioms sum_norm_sq_mul_sqKey
#print axioms ladyzhenskaya_oneD
#print axioms ladyzhenskaya_oneD_h1
#print axioms sum_norm_sq_weighted_general
#print axioms ladyzhenskaya_oneD_general
-- 2D 件（L5 批三 TwoDim 节）公理审计
#print axioms sum_inv_weight_sq_le
#print axioms sum_norm_sq_le_weighted
#print axioms sum_fourier_prod_eq_sum_sliceY
#print axioms norm_sq_fourierPoly2_le_sliceY
#print axioms norm_pow_four_fourierPoly2_le
#print axioms integral_norm_sq_sum_fourier_injOn
#print axioms integral_sliceEnergyY
#print axioms integral_sliceEnergyX
#print axioms integral_prod_norm_sq_sum
#print axioms integral_norm_sq_fourierPoly2
#print axioms integral_norm_sq_pderivPoly2
#print axioms ladyzhenskaya_twoD_tensor
#print axioms ladyzhenskaya_twoD
#print axioms ladyzhenskaya_twoD_h1_sq
#print axioms integral_norm_sq_le_integral_pderiv2
#print axioms ladyzhenskaya_twoD_zero_mean

end Ladyzhenskaya

end NSGalerkin

end
