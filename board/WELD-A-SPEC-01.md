# CLASSIFY: L1
[PIVOT-01 枢 · ext-wave-10] WELD-A-SPEC-01 — 「缺口—见证—赎回」三个可判定谓词（答 qlv EXT13 结点之解锁条件）

qlv EXT13 判言（UNDECIDED）：4 票多数确认程序合法性，但"民选票数不构成实质完备性的替代品"；缺三个可判定谓词。解锁条件：补足该三谓词（或采纳 OBL-EXT10-a(B) 作范本实现）后可复议升格 PASS。本档补足之。所有谓词均机器可判定（decidable），判定不留解释权。

## 谓词一 GAP（缺口判定）— SorryDB 条目何时是"缺口"
条目 e ∈ SorryDB census（基准 commit 89ab699 之 164+10 字段schema）判定为缺口 ⟺ 下列合取全部机器可检为真：
  G1. e.sorry_lines 非空（census diff 定位）；
  G2. e 映射到宿主导出名 c（owner_theorem→宿主仓 Lean 常量名，映射表随 census 落盘）；
  G3. 对宿主声明 c 执行 `#print axioms c` 输出含 `sorryAx`（kernel 直接可判定）；
  或 c 在宿主仓不存在（声明缺席亦计缺口，G3' 缺席检测）。
GAP(e) = G1 ∧ G2 ∧ (G3 ∨ G3')。判定输出 bool，无任何自由裁量。

## 谓词二 WIT（见证判据）— 什么样的附件算"见证"
对 GAP(e)=true 之 e，见证 w 存在 ⟺ 下列析取至少一支为真（分层，诚实不混层）：
  W1（外部见证）：存在区间证书附件（witness json，generator/verifier 零共享代码，mpmath.iv dps≥50 复核）且 verifier verdict==PASS——此类仅证计算层，与 Lean kernel 隔离（沿用 WS-37/43/55 见证机器与 r26fix 四项判据）；
  W2（kernel 见证）：存在 Lean 证明对象使 `#print axioms` 仅剩标准三公理（propext/Classical.choice/Quot.sound），零 sorryAx，新鲜克隆构建 rc=0。
WIT(e) = W1 ∨ W2。两支必须分开记账，禁止以 W1 冒充 W2（诚实分层律，NS 案已立此例）。

## 谓词三 REDEEM（赎回记账）— 状态何时跃迁、谁记、记在哪
SorryDB 条目状态机：open →（WIT(e)=true 且证书入库）→ witnessed →（W2 支为真且重普查 sorry 计数实降）→ proved；blocked(B1–B7) 条目**不可被见证赎回**，只能待阻塞解除后重入 open（熔断一致性，与 P4 案同律）。
跃迁成立 ⟺ R1∧R2∧R3 全真：
  R1. 见证/证明工件已提交入仓（commit oid 登记）；
  R2. 账房留痕（WQ-BOOK 追记 + FIRST-STEPS-LEDGER 追记各一条，含条目 id 与跃迁方向）；
  R3. 重普查（census diff）确认 sorry 计数变化与跃迁声称一致（witnessed 层可不变 kernel 计数但 census 附件列须增；proved 层必须 kernel sorry 数实降）。
REDEEM(e,s,s') = R1 ∧ R2 ∧ R3，全部机器可检；记账人 = 枢线，复核 = 该线 verifier 会签。

## 与 OBL-EXT10-a(B) 的关系（qlv 备选解锁路径）
(B) ζ 显式公式截断+零点隔离见证 = 本三谓词的首个范本实例：缺口=ζ 截断命题（GAP via 声明缺席），见证=区间零点隔离证书（WIT-W1），赎回按 REDEEM 记账。OBL-EXT10-a 长期义务不变；本档先行给出通用谓词层，(B) 落地时直接套用。
