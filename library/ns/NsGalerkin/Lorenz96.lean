-- CLASSIFY: L1
/-
EXT-WAVE-18 续执行批二 · L4 攻坚席（枢/PIVOT-01 体系）
Lorenz-96 批准线 M1 首件 T2：循环和恒等式 spike ——
Lean 内证 Lorenz-96 对角相消并实例化 GalerkinNS。

立案依据：LORENZ96-LINE-CHARTER-01 §2.2 M1（裁定「A 为主 + B 为壳」）、
§五 T2（循环和恒等式 Lean spike）；参数定式钉
LORENZ96-M0-CONSTANTS-v0 §2.1（标准形 dx_j/dt = (x_{j+1}−x_{j−2})·x_{j−1} − x_j + F，
下标 mod N）、§2.5（吸收球先验 R = √N·|F|，S2 Prop 7 一手钉）。

本件内容（全部 sorry-free）：
1. 循环双线性形 `cyclicB`：E = EuclideanSpace ℝ (Fin N)（[NeZero N]）上
   (B x y) j = (x (j+1) − x (j−2)) · y (j−1)（Fin N 模算术），
   连续性由显式界 ‖B x y‖ ≤ 2√N·‖x‖·‖y‖ 给出（逐坐标 |w i| ≤ ‖w‖ + L2 范数平方和）。
2. **核心定理 `cyclic_sum_diag` / `inner_cyclicB_self`**：对角循环和相消
   Σ_j (x_{j+1} − x_{j−2})·x_{j−1}·x_j = 0，即 ⟪B x x, x⟫_ℝ = 0。
   证明为望远镜 + 循环重指标：置 tele k = x_k·x_{k+1}·x_{k+2}，
   被加项 = tele (j−1) − tele (j−2)，而 j ↦ j−1 是 Fin N 上的置换
   （finRotate 之逆），两次移位和相等故差为零。
   此定理即 GalerkinNS.hskew 的供给件。
3. GalerkinNS 实例化 `lorenz96Galerkin F`：ν = 1（语义重映射：ν 槽位承载
   Lorenz-96 阻尼系数 1，alignment 注记见下）、A = 恒等连续线性映射
   （对称正定自伴，hA 取等号）、B = cyclicB、f = F·𝟙 常值外力。
   白拿 Existence.lean / Uniqueness.lean 的存在性、唯一性、能量先验界，
   逐条以 theorem 登记（lorenz96_exists_solution_upto 等）。

如实登记（T2 负面件义务 + 侧车注记口径）：
* **全斜对称不成立**：全称对角条件 ∀ u v, ⟪B u v, v⟫ = 0 对 Lorenz-96
  循环双线性形**不成立**——本件给出机器检验的 N = 4 反例
  `lorenz96_not_hskew_full`（u = e₀、v = e₁+e₂ 时 ⟪B u v, v⟫ = −1）。
  故 Lorenz-96 落在 `GalerkinNS.hskew` 对角假设层，**禁实例化**
  `SkewNonlinearity`（SkewB.lean 的 hskew_full 强化接口；与既有实例
  skewB/B₃ 同样不满足全斜对称的 code-fact 登记一致，SkewB.lean L48 注记）。
* **吸收球接口注记**：能量法口径（定式表 v0 §2.5）：d/dt(½‖x‖²) ≤
  −‖x‖² + √N·|F|·‖x‖，故 limsup‖x‖ ≤ R = √N·|F|（典范 (N,F)=(36,8)
  时 R = 48，导出自算）。本层白拿的能量界为
  `norm_sq_le_of_solution`：‖x t‖² ≤ max ‖x 0‖² ‖f‖²（ν=1），其中
  ‖f‖² = N·F² 即 ‖f‖ = √N·|F|，与吸收球半径一致；limsup 渐近陈述本身
  不在本 spike 范围（区间见证层事项，M2/M3 记账），此处仅登记接口对应。
* 口径钉（C1）：本件全部结论均为**有限维 ODE 截断层**（E9 口径）的机器
  检验定理，不构成任何 PDE 断言；不升格 NS 包任何档位。

工具链钉：leanprover/lean4:v4.35.0 + mathlib v4.35.0（lake-manifest 现钉）。
-/
import NsGalerkin.Uniqueness
import Mathlib.Logic.Equiv.Fin.Rotate
import Mathlib.Algebra.Group.Fin.Basic

open scoped InnerProductSpace

open Set
open scoped NNReal Topology

noncomputable section

namespace NSGalerkin

/-! Lorenz-96 壳命名空间（M1 裁定「B 为壳」：显式定义壳，与 GalerkinNS
实例的接缝以 alignment 注记显式登记）。 -/
namespace Lorenz96

/-- Lorenz-96 状态空间：N 维欧氏空间，指标为循环的 `Fin N`（模算术）。 -/
abbrev State (N : ℕ) := EuclideanSpace ℝ (Fin N)

variable {N : ℕ} [NeZero N]

/-! ### 一、循环双线性形 -/

/-- Lorenz-96 循环双线性形（坐标视图）：
`(Bfun x y) j = (x (j+1) − x (j−2)) · y (j−1)`，指标为 Fin N 模算术
（标准形的二次平流部分，定式表 v0 §2.1）。 -/
def Bfun (x y : State N) : State N :=
  WithLp.toLp 2 fun j => (x (j + 1) - x (j - 2)) * y (j - 1)

/-- `Bfun` 的线性映射封装（两变元逐坐标多项式，逐条 ext + ring）。 -/
def Blin : State N →ₗ[ℝ] State N →ₗ[ℝ] State N :=
  LinearMap.mk₂ ℝ Bfun
    (fun x₁ x₂ y => by
      ext j
      simp only [Bfun, PiLp.toLp_apply, PiLp.add_apply]
      ring)
    (fun c x y => by
      ext j
      simp only [Bfun, PiLp.toLp_apply, PiLp.smul_apply, smul_eq_mul]
      ring)
    (fun x y₁ y₂ => by
      ext j
      simp only [Bfun, PiLp.toLp_apply, PiLp.add_apply]
      ring)
    (fun c x y => by
      ext j
      simp only [Bfun, PiLp.toLp_apply, PiLp.smul_apply, smul_eq_mul]
      ring)

/-- 欧氏向量每个坐标的绝对值不超过其范数（L2 平方和的项界）。 -/
theorem abs_coord_le_norm (w : State N) (i : Fin N) : |w i| ≤ ‖w‖ := by
  have h := Finset.single_le_sum (f := fun j : Fin N => ‖w j‖ ^ 2)
    (fun j _ => sq_nonneg _) (Finset.mem_univ i)
  rw [← PiLp.norm_sq_eq_of_L2] at h
  have h2 := abs_le_of_sq_le_sq h (norm_nonneg w)
  rwa [abs_of_nonneg (norm_nonneg _), Real.norm_eq_abs] at h2

/-- **循环双线性形 `cyclicB`**（连续双线性映射）：
有限维逐坐标多项式，连续性由显式界 `‖cyclicB x y‖ ≤ 2√N·‖x‖·‖y‖` 给出。 -/
def cyclicB : State N →L[ℝ] State N →L[ℝ] State N :=
  LinearMap.mkContinuous₂ Blin (2 * Real.sqrt N) (fun x y => by
    have hcoord : ∀ j : Fin N, |Bfun x y j| ≤ 2 * (‖x‖ * ‖y‖) := by
      intro j
      have e : Bfun x y j = (x (j + 1) - x (j - 2)) * y (j - 1) := by
        simp [Bfun, PiLp.toLp_apply]
      rw [e, abs_mul]
      have h1 : |x (j + 1) - x (j - 2)| ≤ 2 * ‖x‖ := by
        calc |x (j + 1) - x (j - 2)| = |x (j + 1) + -x (j - 2)| := by rw [sub_eq_add_neg]
          _ ≤ |x (j + 1)| + |(-x (j - 2))| := abs_add_le _ _
          _ = |x (j + 1)| + |x (j - 2)| := by rw [abs_neg]
          _ ≤ ‖x‖ + ‖x‖ :=
              add_le_add (abs_coord_le_norm _ _) (abs_coord_le_norm _ _)
          _ = 2 * ‖x‖ := by ring
      calc |x (j + 1) - x (j - 2)| * |y (j - 1)|
          ≤ 2 * ‖x‖ * ‖y‖ :=
            mul_le_mul h1 (abs_coord_le_norm _ _) (abs_nonneg _)
              (mul_nonneg (by norm_num) (norm_nonneg _))
        _ = 2 * (‖x‖ * ‖y‖) := by ring
    have hsq : ‖Bfun x y‖ ^ 2 ≤ (2 * Real.sqrt (N : ℝ) * ‖x‖ * ‖y‖) ^ 2 := by
      have hN : (Real.sqrt (N : ℝ)) ^ 2 = (N : ℝ) := Real.sq_sqrt (Nat.cast_nonneg _)
      rw [PiLp.norm_sq_eq_of_L2]
      calc ∑ j : Fin N, ‖Bfun x y j‖ ^ 2
          ≤ ∑ _j : Fin N, (2 * (‖x‖ * ‖y‖)) ^ 2 := by
            apply Finset.sum_le_sum
            intro j _
            have hb := hcoord j
            have hb2 : |(|Bfun x y j|)| ≤ |2 * (‖x‖ * ‖y‖)| := by
              rwa [abs_abs, abs_of_nonneg
                (mul_nonneg (by norm_num)
                  (mul_nonneg (norm_nonneg _) (norm_nonneg _)))]
            rw [Real.norm_eq_abs]
            exact sq_le_sq.mpr hb2
        _ = (N : ℝ) * (2 * (‖x‖ * ‖y‖)) ^ 2 := by
            rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin]; ring
        _ = (2 * Real.sqrt (N : ℝ) * ‖x‖ * ‖y‖) ^ 2 := by
            calc (N : ℝ) * (2 * (‖x‖ * ‖y‖)) ^ 2
                = 4 * (N : ℝ) * ‖x‖ ^ 2 * ‖y‖ ^ 2 := by ring
              _ = 4 * (Real.sqrt (N : ℝ)) ^ 2 * ‖x‖ ^ 2 * ‖y‖ ^ 2 := by rw [hN]
              _ = (2 * Real.sqrt (N : ℝ) * ‖x‖ * ‖y‖) ^ 2 := by ring
    have hfin := abs_le_of_sq_le_sq hsq
      (mul_nonneg (mul_nonneg (mul_nonneg (by norm_num) (Real.sqrt_nonneg _))
        (norm_nonneg _)) (norm_nonneg _) :
        (0 : ℝ) ≤ 2 * Real.sqrt (N : ℝ) * ‖x‖ * ‖y‖)
    rwa [abs_of_nonneg (norm_nonneg _)] at hfin)

/-- 连续双线性形按点作用即坐标函数。 -/
theorem cyclicB_apply (x y : State N) : cyclicB x y = Bfun x y := rfl

/-- 坐标公式：`(cyclicB x y) j = (x (j+1) − x (j−2)) · y (j−1)`。 -/
theorem cyclicB_apply_coord (x y : State N) (j : Fin N) :
    cyclicB x y j = (x (j + 1) - x (j - 2)) * y (j - 1) := by
  simp [cyclicB_apply, Bfun, PiLp.toLp_apply]

/-! ### 二、对角循环和相消（核心） -/

/-- 望远镜位函数：`tele x k = x_k · x_{k+1} · x_{k+2}`
（第三指标写作 k+1+1，以便用群论引理 `sub_add_cancel` 逐步回约移位，
避免 Fin 字面值转换的额外开销）。 -/
def tele (x : State N) (k : Fin N) : ℝ := x k * x (k + 1) * x (k + 1 + 1)

/-- Fin N 模算术辅助：`1 + 1 = 2`（NeZero N 下成立；N = 1 时两侧均为 0）。 -/
theorem fin_one_add_one : (1 : Fin N) + 1 = 2 := by
  rcases N with _ | _ | n
  · exact absurd rfl (NeZero.ne 0)
  · apply Fin.ext
    rw [Fin.val_add, Fin.val_one', Fin.coe_ofNat_eq_mod]
  · apply Fin.ext
    rw [Fin.val_add, Fin.val_one', Fin.coe_ofNat_eq_mod,
      Nat.mod_eq_of_lt (show 1 < n + 2 by omega)]

-- [L34a: 记号等价] NL「Σ_j (x_{j+1}−x_{j−2})·x_{j−1}·x_j = 0（下标 mod N）」
--   （定式表 v0 §2.5；S1 式(1) 结构 + S2 §2.1 能量守恒的坐标形）↔ 本定理；
--   论证指针：文献 1-based 循环下标 ↔ Fin N 0-based 模算术重指标，项序差由
--   finRotate 置换下求和不变性吸收（见本定理证明头注：望远镜 + Equiv.sum_comp）。
-- [L34a#量词]: NL「对任意状态 x」↔ 形参全称 `∀ x : State N` 一致。
-- [L34a#常数]: 无常数项；求和域 `Finset.univ : Finset (Fin N)` ↔ NL「mod N
--   全循环和」一致；要求 N ≥ 1（NeZero），NL 侧 N ≥ 4 的动力学门槛不入本恒等式。
-- [L34a#谓词]: NL「和为零」↔ 结论 `= 0` 一致（无不等式弱化）。
-- [L34b: 等价]
-- [L34c: 未定+理由——T2 交付构建证据（CI run id + 日志 SHA-256）未随批三移交；
--   本批为纯注释变更，L6 席环境无 Lean 工具链，未重跑构建（静态核验：仅新增
--   行注释、证明体字节不动）；原 T2 证据锚待移交后回填本槽。]
/-- **核心定理：Lorenz-96 对角循环和相消**（T2 验收钉）。
`Σ_j (x_{j+1} − x_{j−2})·x_{j−1}·x_j = 0`（Fin N 模算术求和）。
证明：被加项 = tele (j−1) − tele (j−2)（望远镜），而 j ↦ j−1 为
Fin N 上的置换（`finRotate` 之逆，`Equiv.sum_comp` 重指标），
两个循环和相等，差为零。 -/
theorem cyclic_sum_diag (x : State N) :
    ∑ j : Fin N, (x (j + 1) - x (j - 2)) * x (j - 1) * x j = 0 := by
  have hsub2 : ∀ j : Fin N, (j - 2 : Fin N) = j - 1 - 1 := fun j => by
    rw [sub_sub, fin_one_add_one]
  have htele : ∀ j : Fin N,
      (x (j + 1) - x (j - 2)) * x (j - 1) * x j =
        tele x (j - 1) - tele x (j - 1 - 1) := by
    intro j
    rw [hsub2 j]
    simp only [tele, sub_add_cancel]
    ring
  rw [Finset.sum_congr rfl (fun j _ => htele j), Finset.sum_sub_distrib]
  have hshift1 : ∑ j : Fin N, tele x (j - 1) = ∑ j : Fin N, tele x j := by
    have h := Equiv.sum_comp (finRotate N).symm (tele x)
    simpa only [finRotate_symm_apply] using h
  have hshift2 : ∑ j : Fin N, tele x (j - 1 - 1) = ∑ j : Fin N, tele x (j - 1) := by
    have h := Equiv.sum_comp (finRotate N).symm (fun k => tele x (k - 1))
    simpa only [finRotate_symm_apply] using h
  rw [hshift2, hshift1, sub_self]

-- [L34a: 记号等价] NL「Lorenz-96 二次平流项不改变总能量 E = ½Σx_j²」
--   （S1 p.5 "the quadratic terms … together conserve the total energy"；
--   S2 §2.1 "the quadratic part does not affect the total energy"）之能量内积形
--   ⟪B x x, x⟫ = 0 ↔ 本定理；论证指针：dE/dt 中二次项贡献恰为 ⟪B x x, x⟫
--   （S2 Prop 7 证明式(38) 第一行，定式表 v0 §2.5），本定理即该项恒零的机器检验。
-- [L34a#函数类]: NL N 维实值状态序列 ↔ `State N = EuclideanSpace ℝ (Fin N)`
--   一致（有限维截断层，E9 口径）。
-- [L34a#谓词]: NL「二次项能量贡献为零」↔ 内积等式 `= 0` 一致。
-- [L34b: 等价]
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽（纯注释变更、未重跑构建，
--   T2 原证据锚待移交回填）。]
/-- **GalerkinNS.hskew 供给件**：`⟪cyclicB x x, x⟫_ℝ = 0`。
循环双线性形在能量内积下的对角相消（= `cyclic_sum_diag` 经
`PiLp.inner_apply` 的坐标展开）。 -/
theorem inner_cyclicB_self (x : State N) : ⟪cyclicB x x, x⟫_ℝ = 0 := by
  rw [PiLp.inner_apply]
  simp_rw [RCLike.inner_apply, conj_trivial, cyclicB_apply_coord]
  trans (∑ j : Fin N, (x (j + 1) - x (j - 2)) * x (j - 1) * x j)
  · exact Finset.sum_congr rfl fun j _ => by ring
  · exact cyclic_sum_diag x

/-! ### 三、GalerkinNS 实例化（M1 裁定 A：数学内容走实例化继承） -/

-- [L34a: 记号等价] NL 标准形「ẋ_j = (x_{j+1}−x_{j−2})·x_{j−1} − x_j + F，
--   j mod N，N ≥ 4」（定式表 v0 §2.1，S1 式(1) / S2 式(1a)(1b)）↔ 本实例之
--   `GalerkinNS.vf`；论证指针（接缝闭合证据）：`lorenz96_vf_coord` 逐坐标
--   机器复现右端恒等。
-- [L34a#常数]: **ν 槽位语义重映射（显式化，裁定书 §2.2 要求）**：ν := 1 承载
--   Lorenz-96 线性阻尼系数 1（−x_j 项），**非**分子粘性；A = 恒等连续线性映射
--   承载阻尼算子（**非** Laplacian 粘性算子），hA 强制性界取等号（饱和）；
--   f = F·𝟙 ↔ NL 常值强迫一致。F_H = 0.89820 等文献分岔阈属动力学语义层，
--   不入本映射对（防越层读）。
-- [L34a#函数类]: NL N 维自治 ODE 向量场 ↔ `GalerkinNS (State N)`
--   （E = 欧氏截断空间）一致。
-- [L34a#隐式假设]: NL 循环边界条件 x_{j±N} = x_j ↔ Fin N 模算术（实例级）一致。
-- [L34b: 等价]（右端逐坐标恒等见 lorenz96_vf_coord；结构槽位语义重映射已显式登记）
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽（纯注释变更、未重跑构建，
--   T2 原证据锚待移交回填）。]
/-- **Lorenz-96 的 GalerkinNS 实例**（常值外力强度 F）。
alignment 注记（接缝显式登记，TRUSTBOUNDARY §4.3 约定）：
* ν = 1 —— ν 槽位承载 Lorenz-96 的线性阻尼系数 1（非分子粘性）；
* A = 恒等连续线性映射 —— 阻尼算子，对称正定自伴，hA 取等号
  `‖x‖² = ⟪x, x⟫`（强制性界饱和）；
* B = cyclicB —— hskew 由机器检验定理 `inner_cyclicB_self` 供给；
* f = F·𝟙 —— 常值外力（定式表 v0 §2.1 标准形常数项）。 -/
def lorenz96Galerkin (F : ℝ) : GalerkinNS (State N) where
  ν := 1
  hν := one_pos
  A := .id ℝ _
  hA := fun x => by
    rw [ContinuousLinearMap.id_apply]
    exact (real_inner_self_eq_norm_sq x).symm.le
  B := cyclicB
  hskew := inner_cyclicB_self
  f := WithLp.toLp 2 fun _ => F

-- [L34a: 一致] 本定理即 lorenz96Galerkin 映射对（见上 L34a 记号等价）的接缝
--   闭合证据：实例 vf 逐坐标 = NL 标准形右端（定式表 v0 §2.1）。
-- [L34b: 等价]（恒等式级，无强度差。）
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
/-- 实例向量场逐坐标复现 Lorenz-96 标准形右端：
`(vf x) j = (x (j+1) − x (j−2)) · x (j−1) − x j + F`（定式表 v0 §2.1）。 -/
theorem lorenz96_vf_coord (F : ℝ) (x : State N) (j : Fin N) :
    (lorenz96Galerkin (N := N) F).vf x j =
      (x (j + 1) - x (j - 2)) * x (j - 1) - x j + F := by
  simp only [GalerkinNS.vf, lorenz96Galerkin]
  simp only [PiLp.sub_apply, PiLp.add_apply, PiLp.smul_apply, PiLp.neg_apply,
    ContinuousLinearMap.id_apply, cyclicB_apply_coord, PiLp.toLp_apply,
    smul_eq_mul]
  ring

/-! ### 四、白拿系定理登记（有限维 ODE 截断层，C1 口径） -/

-- [L34a: 一致] NL「有限维光滑 ODE 初值问题在任意有限时限 [0,T] 上存在解」
--   （Cauchy–Lipschitz/Picard 经典结论之截断区间形；Lorenz-96 向量场为多项式、
--   局部 Lipschitz，二次增长由能量先验排除爆破）↔ 本定理一致。
-- [L34a#量词]: NL「∀ T ≥ 0, ∀ 初值」↔ 形参 `hT : 0 ≤ T`、`x₀ : State N` 一致。
-- [L34b: 更弱] NL 教科书全局陈述为 t ∈ [0,∞) 上整体解流；Lean 侧为逐 T 截断
--   区间解（HasDerivWithinAt on Icc 0 T），拼接为全局流未在本包内构造——
--   CONDITIONAL-PASS：下游调用若需全局流语义，须先复核此接缝（义务指针挂此条）。
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
/-- Lorenz-96 截断 ODE **全局存在性**（白拿 `GalerkinNS.exists_solution_upto`）：
任意 T ≥ 0，[0, T] 上存在解。 -/
theorem lorenz96_exists_solution_upto (F : ℝ) (x₀ : State N) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → State N, x 0 = x₀ ∧
      ∀ t ∈ Icc 0 T, HasDerivWithinAt x ((lorenz96Galerkin F).vf (x t)) (Icc 0 T) t :=
  (lorenz96Galerkin F).exists_solution_upto x₀ hT

-- [L34a: 一致] NL「Lipschitz 向量场初值问题解唯一」↔ 截断区间唯一性一致。
-- [L34b: 更弱] 同存在性件口径：截断区间唯一 vs 全局流唯一；CONDITIONAL-PASS
--   义务指针同上条（全局流接缝未闭合）。
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
/-- Lorenz-96 截断 ODE **唯一性**（白拿 `GalerkinNS.solution_unique_upto`）。 -/
theorem lorenz96_solution_unique_upto (F : ℝ) {T : ℝ} (hT : 0 ≤ T) {x₀ : State N}
    {x y : ℝ → State N}
    (hx0 : x 0 = x₀)
    (hx : ∀ t ∈ Icc 0 T, HasDerivWithinAt x ((lorenz96Galerkin F).vf (x t)) (Icc 0 T) t)
    (hy0 : y 0 = x₀)
    (hy : ∀ t ∈ Icc 0 T, HasDerivWithinAt y ((lorenz96Galerkin F).vf (y t)) (Icc 0 T) t) :
    ∀ t ∈ Icc 0 T, x t = y t :=
  (lorenz96Galerkin F).solution_unique_upto hT hx0 hx hy0 hy

-- [L34a: 一致] NL「初值问题存在唯一」（上两条之合取）↔ 本定理一致。
-- [L34b: 更弱] 截断区间 vs 全局流，口径同上两条；CONDITIONAL-PASS 义务指针同上。
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
/-- Lorenz-96 截断 ODE **存在唯一性合取件**
（白拿 `GalerkinNS.exists_unique_solution_upto`）。 -/
theorem lorenz96_exists_unique_solution_upto (F : ℝ) (x₀ : State N) {T : ℝ} (hT : 0 ≤ T) :
    ∃ x : ℝ → State N, x 0 = x₀ ∧
      (∀ t ∈ Icc 0 T, HasDerivWithinAt x ((lorenz96Galerkin F).vf (x t)) (Icc 0 T) t) ∧
      ∀ y : ℝ → State N, y 0 = x₀ →
        (∀ t ∈ Icc 0 T, HasDerivWithinAt y ((lorenz96Galerkin F).vf (y t)) (Icc 0 T) t) →
          ∀ t ∈ Icc 0 T, y t = x t :=
  (lorenz96Galerkin F).exists_unique_solution_upto x₀ hT

-- [L34a: 记号等价] NL「dE/dt ≤ −‖x‖² + √N·|F|·‖x‖ 之积分信封」
--   （S2 Prop 7 证明式(38) + Cauchy–Schwarz，定式表 v0 §2.5）↔
--   ‖x t‖² ≤ max ‖x a‖² ‖f‖²（ν = 1）；论证指针：耗散不等式经 Grönwall/
--   比较原理积分即得信封界（GalerkinNS.norm_sq_le_of_solution 已机器化此链）。
-- [L34a#常数]: R = √N·|F|（典范 (N,F) = (36,8) 时 R = 48，定式表 v0 §2.5
--   导出自算）在 Lean 侧由 ‖f‖ = √N·|F| 隐式承载，未另立数值常量——一致。
-- [L34b: 更弱] NL 吸收球陈述为渐近界 limsup‖x‖ ≤ F√N；本定理为逐时信封
--   max(初值能量, 外力范数平方)，蕴含 limsup 上界但 limsup 陈述本身未形式化
--   （渐近/捕获语义归 M2/M3 区间见证层记账，kernel 层此处不预支）。
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
/-- Lorenz-96 **能量先验界**（白拿 `GalerkinNS.norm_sq_le_of_solution`）：
沿任意解 `‖x t‖² ≤ max ‖x a‖² ‖f‖²`（ν = 1）。
接口注记：‖f‖ = √N·|F|，即吸收球半径 R = √N·|F|（定式表 v0 §2.5，
S2 Prop 7 一手钉）的上界信封；limsup 渐近陈述不在本 spike 范围。 -/
theorem lorenz96_energy_bound (F : ℝ) {a b : ℝ} (hab : a ≤ b) {x : ℝ → State N}
    (hx : ∀ t ∈ Icc a b,
      HasDerivWithinAt x ((lorenz96Galerkin F).vf (x t)) (Icc a b) t) :
    ∀ t ∈ Icc a b,
      ‖x t‖ ^ 2 ≤ max (‖x a‖ ^ 2) (‖(lorenz96Galerkin (N := N) F).f‖ ^ 2 / 1 ^ 2) :=
  fun t ht => (lorenz96Galerkin F).norm_sq_le_of_solution hab hx t ht

-- [L34a: 记号等价] NL「V·dV/dt = ⟨x, Ax⟩ + F·Σ_j x_j ≤ −V² + √N·|F|·V」
--   （S2 式(38) + Cauchy–Schwarz，定式表 v0 §2.5；V = ‖x‖）↔
--   ⟪vf x, x⟫ ≤ −‖x‖² + ‖f‖·‖x‖；论证指针：对流项严格抵消即
--   `inner_cyclicB_self`（对角相消，hskew 对角层），−x_j 项给出 −‖x‖²，
--   常值强迫项经 Cauchy–Schwarz 给出 ‖f‖·‖x‖。
-- [L34a#常数]: 阻尼系数 1（−‖x‖² 项）↔ NL −x_j 项一致（ν 槽位语义重映射，
--   见 lorenz96Galerkin 之 L34a#常数）。
-- [L34b: 等价]
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
/-- Lorenz-96 **能量内积耗散不等式**（白拿 `GalerkinNS.inner_vf_le`）：
`⟪vf x, x⟫ ≤ −‖x‖² + ‖f‖·‖x‖`（对流项由对角相消严格抵消）。 -/
theorem lorenz96_inner_vf_le (F : ℝ) (x : State N) :
    ⟪(lorenz96Galerkin F).vf x, x⟫_ℝ ≤
      -1 * ‖x‖ ^ 2 + ‖(lorenz96Galerkin (N := N) F).f‖ * ‖x‖ :=
  (lorenz96Galerkin F).inner_vf_le x

-- 侧车声明段（M1 收口，批三 L6）：SkewNonlinearity 不实例化之裁定登记。
-- [L34a: 一致] NL 负面陈述「Lorenz-96 循环双线性形不满足全称对角斜对称条件
--   ∀ u v, ⟪B u v, v⟫ = 0」↔ `lorenz96_not_hskew_full` 一致（机器检验否定式）。
-- [L34a#谓词]: NL「不成立」↔ Lean `¬ (∀ u v : State 4, ⟪cyclicB u v, v⟫_ℝ = 0)`
--   一致；N = 4 反例指针：u = e₀、v = e₁+e₂，⟪B u v, v⟫ = −1 ≠ 0。
-- [L34b: 不可比] NL 侧无对应正命题可比较强度；本件为负面登记/接口排除件，
--   不入强度层比较。
-- [L34c: 未定+理由——同 cyclic_sum_diag 之 L34c 槽。]
-- 裁定登记（R1 缓解条落实）：`SkewNonlinearity`（SkewB.lean hskew_full 强化
-- 接口）对 Lorenz-96 **不实例化**；原因＝全斜对称不成立（上指 N=4 反例），
-- 故本线只使用 `GalerkinNS.hskew` 对角假设层，与 skewB/B₃ 同病登记口径一致
-- （SkewB.lean L48 注记）。此排除为接口级裁定，非缺陷。
/-! ### 五、负面件：全斜对称不成立（N = 4 机器检验反例）

如实登记：全称对角条件 `∀ u v, ⟪cyclicB u v, v⟫ = 0`（即
`SkewNonlinearity.hskew_full` 的逐对角内容）对 Lorenz-96 **不成立**。
取 N = 4、u = e₀、v = e₁ + e₂：(B u v)₂ = (u₃ − u₀)·v₁ = −1，
⟪B u v, v⟫ = −1 ≠ 0。故**禁实例化 SkewNonlinearity**（R1 缓解条，
SkewB.lean 强化接口登记一致）。 -/

/-- N = 4 机器检验反例：Lorenz-96 循环双线性形不满足全称对角斜对称条件。 -/
theorem lorenz96_not_hskew_full :
    ¬ (∀ u v : State 4, ⟪cyclicB u v, v⟫_ℝ = 0) := by
  intro h
  have hcontra := h (WithLp.toLp 2 ![1, 0, 0, 0]) (WithLp.toLp 2 ![0, 1, 1, 0])
  rw [PiLp.inner_apply] at hcontra
  simp_rw [RCLike.inner_apply, conj_trivial, cyclicB_apply_coord] at hcontra
  simp only [Fin.sum_univ_four, PiLp.toLp_apply, Fin.reduceAdd, Fin.reduceSub,
    Fin.isValue, Matrix.cons_val, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.head_cons, Matrix.cons_val_two, Matrix.tail_cons, Matrix.cons_val_three,
    Nat.reduceMod] at hcontra
  norm_num at hcontra

/-! ### 六、公理审计（构建期打印；白名单 propext / Classical.choice / Quot.sound） -/
#print axioms cyclic_sum_diag
#print axioms inner_cyclicB_self
#print axioms lorenz96_exists_unique_solution_upto
#print axioms lorenz96_energy_bound
#print axioms lorenz96_not_hskew_full

end Lorenz96

end NSGalerkin
