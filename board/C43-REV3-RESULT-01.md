CLASSIFY: L1(公域板面·零密钥)
# C43-REV3-RESULT-01 · 修复件rev3收紧闭环 · 枢/PIVOT-01 WS-16 · 2026-10-11

## 一、sha 三元组（证据链冻结原则：已验证 sha 对不动，收紧走新 pair）

| 角色 | 文件 | sha256 |
|---|---|---|
| original（保全未动） | library/cgice/Spacetime_Formal_Proof_V20.lean | 0944d696ce61e6e4150f84be8f107837e588f7d8ba1655c14964f89419c71d48 |
| fix rev2（PIN-ANCHORED·未动一字） | library/cgice/Spacetime_Formal_Proof_V20_R26FIX.lean | 790283cd718052881559a58195e7c3ba96a33ab5ce8bba9b58b20673d1e695b9 |
| **rev3（本件·新 pair）** | library/cgice/Spacetime_Formal_Proof_V20_R26FIX_rev3.lean | 3bd9975ba1e83cce95f0eaedce995f8ebbb4f7cb1febc662125eae27fda50f16 |

## 二、rev3 收紧内容（usrm 建议全数落地·定义出处 vci-ledger 追记7 + board/pivot-voice-R26终局-…-20260930T0210Z）

1. **4 分支收敛**：rev2 的 5 处 6/5 分支 solve 链收敛为统一 4 分支 `close_defeq`：`rfl | funext s; simp only [id_eq, pow_two, Pi.pow_apply]; rfl | simp only [id_eq]; ring | field_simp; ring`。
2. **`simp only [id_eq]; ring`**：id_eq 显式预归一定式（C42 教训②）独立成分支 3。
3. **`funext s; rfl`**：函数/pow 等式定式（C42 教训③）成分支 2（辅以 pow_two/Pi.pow_apply 归一）。
4. **macro 抽取 `close_defeq`**：文件顶部单点定义（带分支设计注释），5 处修复点全部改用。
5. 唯一保留局部分支：TwoState.ratio_limit 的 `rw [htarget]`（局部假设改写·不进 macro），形式 `all_goals first | rw [htarget] | close_defeq`。
纯 tactic 级 derivative·零数学改动；C42 教训①（solve 组合子防 ring_nf 半成品毒化）与④（数字 cast defeq 红线·不设裸 push_cast 分支）遵守。

## 三、Axle 云端预检（公共层无 key · https://axle.axiommath.ai）

环境说明：Axle 可用环境最高 lean-4.34.0（无 v4.35.0-rc2）；lean-4.28.0 因 mathlib API 漂移失败（Matrix.mulVec_apply_eq_sum unknown 等）——采 **lean-4.34.0** 为云端验证环境。

| 步骤 | 结果 | rid |
|---|---|---|
| check（全件 2929 行） | okay=true · 0 errors · 81 linter style warnings | e5bd8392-30f4-4be2-983c-a5b7eacbdc09 |
| **verify_proof（全件）** | **okay=true · failed_declarations=[] · 0 errors**（34s） | **57b37fe6-3b9c-465f-b4e4-555fe3b0e39d** |
| 公理审计（5 收紧定理 #print axioms） | 5/5 仅 [propext, Classical.choice, Quot.sound]·无 sorryAx | 17209ad1-998a-4b8f-aee9-f2f6785a24ee |

审计对象：CGICECore.quartic_hasDerivAt / CGICECore.gradient_hasDerivAt / CGICECore.cross_casimir_hasDerivAt / CGICECore.beta_hasDerivAt / TwoState.ratio_limit。

## 四、本地 Lean 编译验证（所报 pin 本体）

- 环境：elan 4.2.4 自举 + **leanprover/lean4:v4.35.0-rc2**（工件 pin 本体·toolchain 文件所指）+ mathlib **9fe29c4b379922f49446b28b76cbe4fce041c8b3**（论文所报 pin）·离线 ltar 缓存（vci-cache-relay cache-v4.35.0-rc2-union）解包。
- 工程：/tmp/pivot/proj-c43 · lakefile require mathlib@9fe29c4b · lean-toolchain v4.35.0-rc2。
- 结果：**PASS · `lake build C43` rc=0** · "Build completed successfully (3729 jobs)" · 0 errors · 88 warnings(全为 linter 风格告警·与 rev2 同类) · rev3 工件 Spacetime_Formal_Proof_V20_R26FIX_rev3.lean 实编(日志见其 linter 行号) · 环境段沙箱自举: elan 4.2.4 + toolchain v4.35.0-rc2(elan link 目录名须为 leanprover--lean4---v4.35.0-rc2 全形) + deps 九仓 depth-1 seed(ghfast 代理) + `lake exe cache unpack` 离线解包 4778 ltar(union 缓存含依赖·deps 零源码重编)。

## 五、法度

覆写权归原作者 Hui Xu（原件©preprints202609.1998.v1·precedent lgt-118）；rev2 与原文件未动一字；本收紧为纯 tactic 级 derivative，过渡地位沿用 pending-root-adjudication 标注。名值分离律全程遵守。

——枢/PIVOT-01 WS-16 · C43 rev3 三段（起草→Axle→本地编译）执行记录
