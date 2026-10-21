-- CLASSIFY: L1
/-
WS-E · EXT-WAVE-18 续执行批 · L2 净室 Writer 轨首件构件：开域接缝（OpenDomain）

## 构件选择登记（规格 FGL-SEAM-SPEC-01，REVIEW-01 已读）

任务允许自规格四单元中自选一个会话内可零 sorry 完成的最小完整构件，
建议优先级：① 单元② Q3 时空 L⁴ 紧性通道预备引理；
② 单元④ G1–G3 有界开域围合/闭子空间紧性遗传；③ 单元① P7–P10 支撑引理。
本席选定 **优先级②（单元④ G1/G2 + 单元③ S5）**，理由：
1. 纯算子论加初等几何，无测度论硬分析：单元② 的 L⁴ 通道依赖 Lp 测度
   基础设施，单元① P7–P10 依赖时空 Bochner 积分层，单会话零 sorry 风险高；
2. 恰是规格强调的开域推广「全部额外成本」所在（单元③ S5 + 单元④ G2），
   「继承而非重证」的设计要点由本件直接承担；
3. 抽象陈述域无关，可同时服务周期域与任意开域路线（接口注记 3）。

## 内容

* 单元③ 3.1 的紧 Gelfand 三元组抽象打包：实内积空间间紧、单、密、收缩的
  连续线性嵌入 `J : V →L[ℝ] H`；
* 单元③ S5 / 单元④ G1（闭子空间紧性遗传）：`J` 限制到「`V'` 子空间、
  `H'` 闭子空间、`J(V') ⊆ H'`」上仍为紧算子；单射性（附精确判据
  `V' ⊓ ker J = ⊥`）与点态收缩性遗传；**稠密性不自动遗传**，以显式假设携带。
  打包形式：紧 Gelfand 三元组在上述数据下限制为子空间三元组
  （`CompactGelfandTriple.restrict`）。
* 单元④ G2（有界开域围合）：平面 `ℝ×ℝ` 中任意有界集含于某开正方形
  （坐标上界加一构造），亦即含于某闭正方形的内部。

未完项登记：G3（开域谱表示喂入抽象塔得有限时域弱解）依赖单元①③尚未落地的
谱坐标与塔机制，不在本件范围；G1 的盒 Rellich 紧性输入（Fourier 路线）与
开域 `L²` 图空间实现亦登记为后续构件。

净室合规：本文件全部内容依规格中的数学陈述独立实现；未接触 FluidGalerkinLean
仓库的任何源文件、Lean 标识符或 tactic 结构（CLEANROOM-REDLINE-FGL-01）。

工具链：leanprover/lean4:v4.35.0 + mathlib v4.35.0。
-/
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Subspace
import Mathlib.Analysis.Normed.Operator.Compact.Basic
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Restrict
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Order.DenselyOrdered

open Set Filter Bornology

noncomputable section

namespace NSGalerkin

variable {V H : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- 紧 Gelfand 三元组（规格单元③ 3.1）：实内积空间 `V H` 间的连续线性嵌入
`J : V →L[ℝ] H`，满足四性——紧（`IsCompactOperator`）、单（`Injective`）、
密（`DenseRange`）、收缩（点态 `‖J v‖ ≤ ‖v‖`）。
这是开域/周期域接缝的域无关接口：具体域只需产出该四元数据。 -/
structure CompactGelfandTriple (V H : Type*) [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] where
  /-- 能量-状态嵌入算子 -/
  J : V →L[ℝ] H
  /-- 紧性：`J` 为紧算子（盒域侧由 Rellich/Fourier 路线提供，开域侧由本文件
  的遗传定理 `restrJ_isCompact` 提供） -/
  isCompact : IsCompactOperator J
  /-- 单射性 -/
  injective : Function.Injective J
  /-- 值域稠密 -/
  denseRange : DenseRange J
  /-- 收缩性：`‖J v‖ ≤ ‖v‖` -/
  contractive : ∀ v : V, ‖J v‖ ≤ ‖v‖

namespace CompactGelfandTriple

variable (T : CompactGelfandTriple V H)

/-- 限制映射（单元④ G1 的核心构造）：当 `J` 把子空间 `V'` 映入子空间 `H'` 时，
`J` 经定义域包含 `V'.subtypeL` 与值域余限制 `codRestrict` 合成
`V' →L[ℝ] H'`；与盒空间闭子空间包含交换（值层即 `J` 本身）。 -/
def restrJ (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hmap : ∀ v ∈ V', T.J v ∈ H') : V' →L[ℝ] H' :=
  (T.J.comp V'.subtypeL).codRestrict H' (fun v => hmap v v.2)

/-- 限制映射与包含的交换关系（值层计算）：`↑(restrJ v) = J ↑v`。 -/
@[simp]
theorem restrJ_apply_coe (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hmap : ∀ v ∈ V', T.J v ∈ H') (v : V') :
    (T.restrJ V' H' hmap v : H) = T.J (v : V) := rfl

/-- **S5 紧性遗传（单元④ G1 的算子论核心）**：设 `J : V →L[ℝ] H` 紧，
`V' ⊆ V` 子空间、`H' ⊆ H` **闭**子空间、`J(V') ⊆ H'`，
则限制映射 `V' →L[ℝ] H'` 仍紧。
机制：与定义域包含复合保持紧性（`IsCompactOperator.comp_clm`）；
紧见证 `K` 与闭集 `H'` 之交在子空间拓扑中仍紧（闭集原像沿闭嵌入下降），
故同一见证收紧后复用，0 的邻域条件原样继承。 -/
theorem restrJ_isCompact (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hH' : IsClosed (H' : Set H)) (hmap : ∀ v ∈ V', T.J v ∈ H') :
    IsCompactOperator (T.restrJ V' H' hmap) := by
  obtain ⟨K, hK, hK0⟩ := T.isCompact.comp_clm V'.subtypeL
  refine ⟨Subtype.val ⁻¹' K, ?_, ?_⟩
  · -- 紧见证的收紧：`val '' (val ⁻¹' K) = K ∩ ↑H'`，紧集交闭集仍紧
    rw [Subtype.isCompact_iff, image_preimage_eq_inter_range, Subtype.range_coe_subtype]
    exact hK.inter_right hH'
  · -- 0 的邻域条件：限制映射对该见证的原像与复合映射的原像同集
    have hpre : ⇑(T.restrJ V' H' hmap) ⁻¹' (Subtype.val ⁻¹' K)
        = (⇑T.J ∘ ⇑V'.subtypeL) ⁻¹' K := rfl
    rw [hpre]
    exact hK0

/-- **S5 单射遗传的精确判据**：`V' ⊓ ker J = ⊥`（即 `V' ∩ ker J = {0}`）
蕴含限制映射单射；全局单射为其特例（见 `restrict`）。 -/
theorem restrJ_injective_of_ker (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hmap : ∀ v ∈ V', T.J v ∈ H')
    (hker : V' ⊓ LinearMap.ker T.J.toLinearMap = ⊥) :
    Function.Injective (T.restrJ V' H' hmap) := by
  intro x y hxy
  -- 值层相等：由 `H'` 元素相等推出 `J ↑x = J ↑y`
  have hval : T.J (x : V) = T.J (y : V) := congrArg (fun z : H' => (z : H)) hxy
  -- 差落在 `V' ⊓ ker J`，由判据为 0
  have hmem : (x : V) - (y : V) ∈ V' ⊓ LinearMap.ker T.J.toLinearMap := by
    refine ⟨V'.sub_mem x.2 y.2, ?_⟩
    simp only [SetLike.mem_coe, LinearMap.mem_ker, map_sub, sub_eq_zero]
    exact hval
  rw [hker, Submodule.mem_bot, sub_eq_zero] at hmem
  exact Subtype.ext hmem

/-- 全局单射时限制映射单射（判据 `V' ⊓ ker J = ⊥` 自动成立）。 -/
theorem restrJ_injective (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hmap : ∀ v ∈ V', T.J v ∈ H') :
    Function.Injective (T.restrJ V' H' hmap) := by
  refine T.restrJ_injective_of_ker V' H' hmap (eq_bot_iff.mpr ?_)
  intro x hx
  rw [Submodule.mem_bot]
  obtain ⟨-, hxk⟩ := hx
  have hx0 : T.J x = 0 := by simpa using hxk
  exact T.injective (hx0.trans (map_zero T.J).symm)

/-- **S5 收缩性（点态范数）遗传**：子空间与余限制均不改变范数，
`‖restrJ v‖ = ‖J ↑v‖ ≤ ‖↑v‖ = ‖v‖`。 -/
theorem restrJ_contractive (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hmap : ∀ v ∈ V', T.J v ∈ H') (v : V') :
    ‖T.restrJ V' H' hmap v‖ ≤ ‖v‖ :=
  T.contractive (v : V)

/-- **S5 打包形式（单元④ G1 的抽象核）**：紧 Gelfand 三元组在
「`V'` 子空间、`H'` **闭**子空间、`J(V') ⊆ H'`、限制值域稠密」数据下
限制为子空间上的紧 Gelfand 三元组。
注意：稠密性是四性中唯一不自动遗传者，判据为 `H' ⊆ closure (J(V'))`，
本构造以显式假设 `hdense` 携带（规格单元③ 3.3 的明示成本）。 -/
def restrict (V' : Submodule ℝ V) (H' : Submodule ℝ H)
    (hH' : IsClosed (H' : Set H)) (hmap : ∀ v ∈ V', T.J v ∈ H')
    (hdense : DenseRange (T.restrJ V' H' hmap)) :
    CompactGelfandTriple V' H' where
  J := T.restrJ V' H' hmap
  isCompact := T.restrJ_isCompact V' H' hH' hmap
  injective := T.restrJ_injective V' H' hmap
  denseRange := hdense
  contractive := T.restrJ_contractive V' H' hmap

end CompactGelfandTriple

/-! ## 单元④ G2：有界开域围合（初等几何） -/

/-- 以原点为中心、半边长 `R` 的闭正方形 `[-R, R]²`。 -/
def closedSquare (R : ℝ) : Set (ℝ × ℝ) := Set.Icc (-R) R ×ˢ Set.Icc (-R) R

/-- 以原点为中心、半边长 `R` 的开正方形 `(-R, R)²`。 -/
def openSquare (R : ℝ) : Set (ℝ × ℝ) := Set.Ioo (-R) R ×ˢ Set.Ioo (-R) R

/-- 开正方形是开集。 -/
theorem isOpen_openSquare (R : ℝ) : IsOpen (openSquare R) :=
  isOpen_Ioo.prod isOpen_Ioo

/-- 闭正方形的内部即对应开正方形。 -/
theorem interior_closedSquare (R : ℝ) : interior (closedSquare R) = openSquare R := by
  show interior (Set.Icc (-R) R ×ˢ Set.Icc (-R) R) = Set.Ioo (-R) R ×ˢ Set.Ioo (-R) R
  rw [interior_prod_eq, interior_Icc]

/-- **G2（有界开域围合）**：平面 `ℝ×ℝ` 中任意有界集 `U` 都含于某个
（以原点为中心的）开正方形，等价地含于对应闭正方形的内部
（`U ⊂ int(Q)`，规格原陈述）。
构造：取包住 `U` 的球半径加一（规格：坐标上界加一的正方形）；
逐坐标由乘积范数的坐标界 `|xᵢ| ≤ ‖x‖` 进入开区间。 -/
theorem exists_openSquare_superset (U : Set (ℝ × ℝ)) (hU : IsBounded U) :
    ∃ R : ℝ, 0 < R ∧ U ⊆ openSquare R ∧ U ⊆ interior (closedSquare R) := by
  obtain ⟨r, hr⟩ := (Metric.isBounded_iff_subset_ball (0 : ℝ × ℝ)).mp hU
  set R := max (r + 1) 1 with hR
  have hRpos : 0 < R := lt_max_of_lt_right one_pos
  have hRr : r < R := lt_max_of_lt_left (lt_add_one r)
  have hsub : U ⊆ openSquare R := by
    intro x hx
    have hxb : ‖x‖ < r := by
      have hxmem := hr hx
      rwa [Metric.mem_ball, dist_zero_right] at hxmem
    show x.1 ∈ Set.Ioo (-R) R ∧ x.2 ∈ Set.Ioo (-R) R
    rw [Set.mem_Ioo, Set.mem_Ioo, ← abs_lt, ← abs_lt]
    constructor
    · calc |x.1| = ‖x.1‖ := (Real.norm_eq_abs x.1).symm
        _ ≤ ‖x‖ := norm_fst_le x
        _ < r := hxb
        _ < R := hRr
    · calc |x.2| = ‖x.2‖ := (Real.norm_eq_abs x.2).symm
        _ ≤ ‖x‖ := norm_snd_le x
        _ < r := hxb
        _ < R := hRr
  exact ⟨R, hRpos, hsub, interior_closedSquare R ▸ hsub⟩

/-- G2 的围合形式推论：存在正半边长的闭正方形 `Q` 使 `U ⊆ int(Q)` 且
`int(Q)` 为开正方形（围合矩形可直接取为正方形）。 -/
theorem exists_closedSquare_enclosure (U : Set (ℝ × ℝ)) (hU : IsBounded U) :
    ∃ R : ℝ, 0 < R ∧ U ⊆ interior (closedSquare R) ∧ IsOpen (interior (closedSquare R)) := by
  obtain ⟨R, hRpos, -, hint⟩ := exists_openSquare_superset U hU
  exact ⟨R, hRpos, hint, isOpen_interior⟩

end NSGalerkin

end
