-- CLASSIFY: L1
import Lake
open Lake DSL

package nsGalerkin where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.10.0"

@[default_target]
lean_lib NsGalerkin where
