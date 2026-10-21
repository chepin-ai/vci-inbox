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

未完（残口登记）：2D 主不等式的最终组装——各向异性 Fubini 切片迭代
（把 1D 结果沿两坐标迭代：`∫∫‖u‖⁴ ≤ (∫dy sup_x‖u‖²)·(∫dx sup_y‖u‖²)`
通道需 `Measure.pi` 的 Fubini/切片多项式机制与积分型 Cauchy–Schwarz，
本会话内未完成）。2D 朴素谱线 `Σ|k|⁻²` 对数发散（不可走）；
各向异性可乘型 1D 嵌入（阈值截断内插）同列未完。按 CapAnchor 先例，
主陈述以 Prop 级定义 `periodicLadyzhenskayaStatement` 登记，不断言证明。
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
  simp only [div_one] at h1
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
  rw [integral_congr_ae (ae_of_all _ fun x => by rw [hgx x])]
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
    rw [norm_mul, norm_mul, norm_mul, Complex.norm_I, Complex.norm_intCast, mul_one]
    congr 1
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (mul_pos zero_lt_two Real.pi_pos)]
  rw [pderivPoly, integral_norm_sq_sum_mFourier c.support
    (fun k => 2 * Real.pi * Complex.I * (k i : ℂ) * c k), Finset.mul_sum]
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
    ← Finset.sum_add_distrib]
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
  rw [integral_congr_ae (ae_of_all _ fun x => by rw [hgx x])]
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
    simp only [div_one] at h1
    exact h1.const_mul (c k)
  have hsum := HasDerivAt.sum hterm
  convert hsum using 1
  show (∑ k ∈ c.support,
      c k * (2 * Real.pi * Complex.I * (k : ℂ) * fourier k (t : UnitAddCircle))) =
    ∑ k ∈ c.support, (2 * Real.pi * Complex.I * (k : ℂ) * c k) * fourier k (t : UnitAddCircle)
  exact Finset.sum_congr rfl fun k _ => by ring

/-- **1D 偏导能量（谱形式）**：`∫‖∂u‖² = (2π)²·Σ k²·‖cₖ‖²`。 -/
theorem integral_norm_sq_pderivPoly1 (c : ℤ →₀ ℂ) :
    ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure =
      (2 * Real.pi) ^ 2 * ∑ k ∈ c.support, (k : ℝ) ^ 2 * ‖c k‖ ^ 2 := by
  have hn : ∀ k : ℤ, ‖2 * Real.pi * Complex.I * (k : ℂ) * c k‖ =
      2 * Real.pi * |(k : ℝ)| * ‖c k‖ := by
    intro k
    rw [norm_mul, norm_mul, norm_mul, Complex.norm_I, Complex.norm_intCast, mul_one]
    congr 1
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (mul_pos zero_lt_two Real.pi_pos)]
  rw [pderivPoly1, integral_norm_sq_sum_fourier c.support
    (fun k => 2 * Real.pi * Complex.I * (k : ℂ) * c k), Finset.mul_sum]
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
    rw [Finset.sum_congr rfl hterm, ← Finset.sum_image hinj]
    calc ∑ n ∈ (s.filter (fun k => 0 < k)).image Int.toNat, (1 : ℝ) / (n : ℝ) ^ 2
        ≤ ∑' n : ℕ, (1 : ℝ) / (n : ℝ) ^ 2 :=
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
    rw [Finset.sum_congr rfl hterm, ← Finset.sum_image hinj]
    calc ∑ n ∈ (s.filter (fun k => k < 0)).image (fun k => (-k).toNat), (1 : ℝ) / (n : ℝ) ^ 2
        ≤ ∑' n : ℕ, (1 : ℝ) / (n : ℝ) ^ 2 :=
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
  have h1 : (1 / 12 : ℝ) * (∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) *
      ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure ≤
    (1 / 12) * (∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) *
      ((∫ x : UnitAddCircle, ‖fourierPoly1 c x‖ ^ 2 ∂circleMeasure) +
        ∫ x : UnitAddCircle, ‖pderivPoly1 c x‖ ^ 2 ∂circleMeasure) := by
    apply mul_le_mul_of_nonneg_left _ (by norm_num)
    apply mul_le_mul_of_nonneg_left _ hL2
    exact le_add_of_nonneg_left hHe
  exact h1

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
      rw [← Finset.sum_filter, Finset.filter_eq]
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
    rw [Finset.sum_congr rfl hterm, Finset.sum_add_distrib, one_div, inv_pow, ← mul_assoc,
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

end Ladyzhenskaya

end NSGalerkin

end
