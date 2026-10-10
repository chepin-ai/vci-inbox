// CLASSIFY: L1
// CERT-T2A-INSTANCES-EXT01 · T2a 更强实例批（OBL-EXT-04r · PIVOT-01 工程线）
// 模板源：artifacts/lean-verified/T2aTemplate.lean @577b1a4f（rice_bridge/ext_of_pointwise/rice_pointwise 拷贝件，不改原文件）
// 云端通道：Axle verify_proof 公共层（无 key），环境 lean-4.28.0
// 验证记录（verify_proof request_id，okay=true）：
//   inst_shift7     c5674825-412d-4877-b5cf-f8ae967ffe87
//   inst_square_ne3 bd879da4-b6c1-476c-b490-5d389374d438
//   inst_pow2_ne3   fdedfb82-095d-45dc-90ec-688e83bbdd6b
//   inst_fact_ne4   17c045dd-cefe-480d-a70c-995696508739
//   批量整件        77a0eaad-fbd2-48a6-9281-330f736fc8c2
// 公理审计（#print axioms 云端）：4/4 仅 [propext, Classical.choice, Quot.sound]，无 sorryAx。

import Mathlib

open Denumerable Computable Part Nat.Partrec Nat.Partrec.Code

namespace T2aExt

open ComputablePred

/-- 参数化 Rice 桥：任何外延的、非平凡的码谓词均不可计算。 -/
theorem rice_bridge (C : Set Code)
    (Hext : ∀ cf cg, eval cf = eval cg → (cf ∈ C ↔ cg ∈ C))
    (hnt : C ≠ ∅ ∧ C ≠ Set.univ) :
    ¬ ComputablePred fun c => c ∈ C := by
  intro h
  rcases (ComputablePred.rice₂ C Hext).1 h with h0 | hu
  · exact hnt.1 h0
  · exact hnt.2 hu

/-- 外延性模板：逐点输出等式形谓词天然外延。 -/
theorem ext_of_pointwise (g : ℕ → ℕ) :
    ∀ cf cg, eval cf = eval cg →
      ((∃ m, eval cf m = Part.some (g m)) ↔ (∃ m, eval cg m = Part.some (g m))) := by
  intro cf cg h
  constructor <;> intro ⟨m, hm⟩
  · exact ⟨m, h ▸ hm⟩
  · exact ⟨m, h.symm ▸ hm⟩

/-- 参数化实例发生器。 -/
theorem rice_pointwise (g : ℕ → ℕ) (k : ℕ) (hkg : ∀ m, g m ≠ k) :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (g m) := by
  apply rice_bridge (C := {c | ∃ m, eval c m = Part.some (g m)})
  · exact ext_of_pointwise g
  · constructor
    · intro hempty
      have hmem : Code.const (g 0) ∈ {c : Code | ∃ m, eval c m = Part.some (g m)} := ⟨0, by simp⟩
      rw [hempty] at hmem
      exact hmem
    · intro huniv
      have hmem : Code.const k ∈ {c : Code | ∃ m, eval c m = Part.some (g m)} := by
        rw [huniv]; exact Set.mem_univ _
      obtain ⟨m, hm⟩ := hmem
      simp at hm
      exact hkg m hm.symm

/-- 实例四（线性偏移，依赖输入分布）：输出为「输入 + 7」不可判定。 -/
theorem inst_shift7 :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (m + 7) :=
  rice_pointwise (fun m => m + 7) 3 (fun m => by show m + 7 ≠ 3; omega)

/-- 实例五（非平凡算术·平方避点）：输出为「输入平方」不可判定。
    见证：m < 2 时逐点枚举；m ≥ 2 时 m*m ≥ 4，避开 k = 3。 -/
theorem inst_square_ne3 :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (m * m) :=
  rice_pointwise (fun m => m * m) 3 (fun m => by
    show m * m ≠ 3
    rcases Nat.lt_or_ge m 2 with h | h
    · interval_cases m <;> decide
    · have h4 : 2 * 2 ≤ m * m := Nat.mul_le_mul h h
      omega)

/-- 实例六（递归结构·指数见证）：输出为「2 的输入次幂」不可判定。
    见证：对 m 归纳，2^0 = 1，2^(n+1) = 2·2^n 为偶，避开 k = 3。 -/
theorem inst_pow2_ne3 :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (2 ^ m) :=
  rice_pointwise (fun m => 2 ^ m) 3 (fun m => by
    show 2 ^ m ≠ 3
    induction m with
    | zero => decide
    | succ n ih =>
      rw [pow_succ]
      omega)

/-- 实例七（递归结构·阶乘见证 + 可除性）：输出为「输入阶乘」不可判定。
    见证：n < 3 时逐点枚举；n ≥ 3 时 3! = 6 整除 n!，故 n! ≥ 6，避开 k = 4。 -/
theorem inst_fact_ne4 :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (Nat.factorial m) :=
  rice_pointwise (fun m => Nat.factorial m) 4 (fun m => by
    show Nat.factorial m ≠ 4
    rcases Nat.lt_or_ge m 3 with h | h
    · interval_cases m <;> decide
    · have hd : Nat.factorial 3 ∣ Nat.factorial m := Nat.factorial_dvd_factorial h
      have hle : Nat.factorial 3 ≤ Nat.factorial m := Nat.le_of_dvd (Nat.factorial_pos m) hd
      have h3 : Nat.factorial 3 = 6 := rfl
      omega)

end T2aExt
