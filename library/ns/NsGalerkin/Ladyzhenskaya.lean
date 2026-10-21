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

【未完登记（诚实标注）】主不等式的最终组装——各向异性 1D 迭代
（或等价分析件）把 (iii) 的 `Σ‖c‖` 因子升级为
`‖u‖_{L²}·‖∇u‖_{L²}` 量级的均匀常数——**本会话内未完成**；
`∂ᵢ(mFourier k) = 2πi·kᵢ·mFourier k` 的微分链接件（梯度 L² 范数
与谱能量 `specGradEnergy` 的严格等同）同列未完；零均值条件处理与
常数 `C_L` 显式化属 D-B2 范围。按 CapAnchor 先例，主陈述以 Prop 级
定义 `periodicLadyzhenskayaStatement` 登记，不断言证明。
全文件零 sorry、零新增 axiom（仅 propext/Classical.choice/Quot.sound 三件套）。

版本钉：leanprover/lean4:v4.35.0 + mathlib v4.35.0（@56a00585）。
-/
import Mathlib.Analysis.Fourier.AddCircleMulti

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

-- D-B1 件公理审计（构建期打印；应仅见 propext/Classical.choice/Quot.sound）。
#print axioms sum_norm_sq_convC_le
#print axioms fourierPoly_mul
#print axioms integral_norm_pow_four_fourierPoly
#print axioms integral_norm_pow_four_le
#print axioms one_le_kSq_of_ne_zero
#print axioms sum_norm_sq_le_specGradEnergy

end Ladyzhenskaya

end NSGalerkin

end
