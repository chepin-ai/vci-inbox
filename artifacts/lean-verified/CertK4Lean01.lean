/-
CLASSIFY: L1
CERT-K4-LEAN-01 · 证书生命周期状态机全形式化 · Axle 云端验证
check okay + verify_proof request_id=16618831-e457-4d29-8d65-b57fa563e33d
公理审计：legal_count/I2_revoked_terminal 仅依赖 [propext, Classical.choice, Quot.sound]
Lean 化精确修正：I1 陈述由「granted 唯一入口 candidate」修为「candidate(四闸)∨demoted(整改)」——decide 证伪原陈述
-/
import Mathlib

namespace FedKernel.Lifecycle

/-- 证书生命周期五态 -/
inductive State | candidate | granted | maintained | demoted | revoked
deriving DecidableEq, Fintype

open State

/-- 合法迁移谓词（K4 机器九迁移） -/
def legal : State → State → Bool
  | candidate, granted => true    -- 四闸评审
  | candidate, revoked => true    -- 域撤回
  | granted, maintained => true   -- 持续监测通过
  | granted, demoted => true      -- 越域检出
  | granted, revoked => true      -- 证书伪造检出
  | maintained, demoted => true   -- 越域检出
  | maintained, revoked => true   -- 证书伪造检出
  | demoted, granted => true      -- 整改复审
  | demoted, revoked => true      -- 伪造检出或域撤回
  | _, _ => false

/-- CERT-K4-01 迁移计数：合法 9，非法 11 -/
theorem legal_count :
    (Finset.univ.filter fun p : State × State => legal p.1 p.2 = true).card = 9 := by decide
theorem illegal_count :
    (Finset.univ.filter fun p : State × State => legal p.1 p.2 = false ∧ p.1 ≠ p.2).card = 11 := by decide

/-- I1 授予门控：granted 入口仅 candidate（四闸评审）或 demoted（整改复审）——Lean 化精确修正 -/
theorem I1_granted_gated : ∀ s, legal s granted = true → s = candidate ∨ s = demoted := by decide
/-- I1b 维持门控：maintained 唯一入口为 granted -/
theorem I1b_maintained_only_from_granted : ∀ s, legal s maintained = true → s = granted := by decide
/-- I2 证据只增不减：revoked 为吸收终态（无任何出边） -/
theorem I2_revoked_terminal : ∀ s, legal revoked s = false := by decide
/-- I2b 不可逆：无任何状态可迁回 candidate -/
theorem I2b_no_return_to_candidate : ∀ s, legal s candidate = false := by decide
/-- I3 申诉冻结：demoted 出边仅整改复审(granted)或撤销(revoked) -/
theorem I3_demoted_out_edges : ∀ s, legal demoted s = true → s = granted ∨ s = revoked := by decide
/-- 自环全禁 -/
theorem no_self_loop : ∀ s, legal s s = false := by decide

end FedKernel.Lifecycle
