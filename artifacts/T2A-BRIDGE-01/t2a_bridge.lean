/-
CLASSIFY: L1
T2A-BRIDGE-01 · FK-01R T2a（domain-limit 必要性）的 Mathlib Rice 归约桥
Axle 云端严格验证（verify_proof，无 sorry/白名单公理内/签名匹配）：
  t2a_bridge   request_id=c2a58cfa-dd32-4bcb-a8c1-b06f93d25c08
  t2a_instance request_id=a446bfd2-d9a0-4727-afe3-d5f13b63a401
环境 lean-4.28.0（Mathlib 快照含 ComputablePred.rice₂, Carneiro ITP2019）。
-/
import Mathlib

open Denumerable Computable Part Nat.Partrec Nat.Partrec.Code

namespace FedKernel

/-- T2a 归约桥（Mathlib Rice 直达）：任何外延封闭且非平凡的 Code 性质不可判定。 -/
theorem t2a_bridge (C : Set Code)
    (Hext : ∀ cf cg, eval cf = eval cg → (cf ∈ C ↔ cg ∈ C))
    (hnt : C ≠ ∅ ∧ C ≠ Set.univ) :
    ¬ ComputablePred fun c => c ∈ C := by
  intro h
  rcases (ComputablePred.rice₂ C Hext).1 h with h0 | hu
  · exact hnt.1 h0
  · exact hnt.2 hu

/-- T2a 具体实例：「存在零点」语义性质不可判定（内核 A_{M,w} 构造的 Mathlib 化身）。 -/
theorem t2a_instance : ¬ ComputablePred fun c => ∃ m, eval c m = Part.some 0 := by
  apply t2a_bridge (C := {c | ∃ m, eval c m = Part.some 0})
  · intro cf cg H
    simp only [Set.mem_setOf_eq]
    constructor <;> intro ⟨m, hm⟩
    · exact ⟨m, H ▸ hm⟩
    · exact ⟨m, H.symm ▸ hm⟩
  · constructor
    · intro hempty
      have hmem : Code.const 0 ∈ {c : Code | ∃ m, eval c m = Part.some 0} := ⟨0, by simp⟩
      rw [hempty] at hmem
      exact hmem
    · intro huniv
      have hmem : Code.const 1 ∈ {c : Code | ∃ m, eval c m = Part.some 0} := by
        rw [huniv]; exact Set.mem_univ _
      obtain ⟨m, hm⟩ := hmem
      simp at hm

end FedKernel
