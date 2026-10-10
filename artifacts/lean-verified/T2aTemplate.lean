-- CLASSIFY: L1
-- CERT-T2A-TEMPLATE-01 · T2a 参数化一般化（SURGE01 lvlu 提案 · 下波主攻候选执行）
-- 目标：把 Rice 桥从单点实例升格为可参数化调用的定理模板
-- 云端通道：Axle verify_proof（无 key 公共层）
-- 验证记录（环境 lean-4.28.0，okay=true）：
--   rice_bridge      41e07431-e53b-465d-b920-c4898fa257c0
--   ext_of_pointwise 2d611c78-046b-4e1f-91bf-7ab9a2a59aa3
--   rice_pointwise   c39c5b84-bc93-4415-a5e2-fda74020a265
--   inst_const_zero  4ee3fbb4-a0e0-4319-a270-67df7e883082
--   inst_succ        d6fba622-b277-4e67-8927-da561d8ab989
--   inst_double      2e3b960c-7916-4f11-a608-43da3d4f74ca
-- 公理审计：6/6 仅 [propext, Classical.choice, Quot.sound]，无 sorryAx。
import Mathlib

open Denumerable Computable Part Nat.Partrec Nat.Partrec.Code

namespace T2aTemplate

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

/-- 参数化实例发生器：对任意值域避开某点 k 的输出函数 g，
    「存在某输入使输出为 g m」不可计算。 -/
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

/-- 实例一：输出常 0 不可判定（原 t2a_instance 的模板化再现）。 -/
theorem inst_const_zero :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some 0 :=
  rice_pointwise (fun _ => 0) 1 (fun _ => Nat.zero_ne_one)

/-- 实例二：输出为输入后继不可判定。 -/
theorem inst_succ :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (m + 1) :=
  rice_pointwise (fun m => m + 1) 0 (fun m => Nat.succ_ne_zero m)

/-- 实例三：输出为输入两倍不可判定。 -/
theorem inst_double :
    ¬ ComputablePred fun c => ∃ m, eval c m = Part.some (2 * m) :=
  rice_pointwise (fun m => 2 * m) 1 (fun m => by show 2 * m ≠ 1; omega)

end T2aTemplate
