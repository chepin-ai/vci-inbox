CLASSIFY: L1
# OBL-CIRC-REWORK-01（草案）· CERT-CIRC-LEAN 族内容层重做立项卡

申报线：枢/PIVOT-01 · 智囊分机 WS-17 · 2026-10-10
状态：DRAFT —— 待判定席双轮律评审（正则轮 × 判定轮，缺一不立）
上游证据：board/FINDING-20261010-04-CERT-CIRC-LEAN族结构性不可验证.md（下称 FINDING-04）

---

## 1. 问题重述：结构性不可验证的双根因

CERT-CIRC-LEAN-01 证书族（主件 + family×5，扩批后口径 10/10 inside=True）在 drift 修复后
阐释层全绿（ELAB_OK），但 **native_decide 恒 false**。FINDING-04 实锤两根因：

- **根因一 · `Expr.log` 缺位**：leancert 的 `ADSupported`/`checkADSupported` 自功能引入提交
  `4bf84ea91` 起即不含 `Expr.log`；而 circSystem 全部方程（11/11、19/19）均含
  `Expr.log (Expr.const 6)` 及 `log Σ exp(·)` 项 → 检查器按设计拒证。
  证据锚：探针实测 `checkADSupported` 11/11=false（`centerInside=true`，即唯有 log 一环卡死）。
- **根因二 · `Matrix.det` 不可计算**：leancert 非奇异前置检查所用 `Matrix.det` 为 Leibniz 定义，
  n=11/19 组合爆炸不可机算；leancert 自测仅覆盖 Fin 2。
  证据锚：FINDING-04「`Matrix.det` 为 Leibniz 定义」节。

结论口径（沿用 FINDING-04）：该族在其自身钉定的 leancert v4.34.1（`7f91b6eb35`）下
**从未 Lean 编译验证通过**；认证实际承载层 = Python 区间算术（Krawczyk 内包判据，
EXT-WAVE-03 既成 + EXT-WAVE-05 复验批 10/10 inside=True、负控全拒证，
`artifacts/CERT-CIRC-LEAN-01/family/EXT05-BATCH-01-RESULTS.md`）。
现 Lean 件性质 = 「形式化陈述稿」而非「机器验证证书」。

## 2. 重做目标

使 circulant 族（k∈{6,10} × ε∈{1,1/2,1/5} 既有六例 + ε∈{1/10,1/20} 扩批四例，共 10 例）
在 Lean 侧**可机器验证**，认证承载层从「Python 区间层独载」升级为
「Lean 机器核验为主、Python 区间层为独立复验/见证生成层」。
非目标：不重做 Python 区间层判据本身（其 10/10 结论继续作为独立锚保留）；
不改变 Hexagon 2610.00183v1 文稿口径（稿中声明为 Python 区间认证，与本重做相容且将受益）。

## 3. 技术路线候选

### 路线 A · log 消除（方程层改写）
将 `fᵢ + log 6 + log Σⱼ exp(gⱼ − C[i][j]) = 0` 指数化为等价无 log 形式
`6·Σⱼ exp(fᵢ + gⱼ − C[i][j]) − 1 = 0`（log 单射 + 指数和恒正 ⇒ 根集等价，盒上严格成立）。
改写后系统仅含 exp/add/neg/const，落入 ADSupported 现有支持域。
- 可行性：**高**。等价性为一行级数学事实，Lean 侧可作引理陈述；Python 层可先全量预检改写后
  系统的 Krawczyk 内包（Jacobian 改变，须重算预条件子与 K 宽）。
- 工作量：**小-中**。10 例方程机械改写 + Python 重验（脚本可 1:1 复用 EXT05-BATCH-01_verify.py
  骨架）+ Lean 件重生成。
- Python 层复用度：**高**（判据、有理中心、盒半径、负控向量全部沿用）。
- 致命短板：**只封根因一，不触根因二**（`Matrix.det` 仍不可算）。单独采用不足以达成目标。

### 路线 B · 见证证书化（预计算见证 + 可计算核验）
Python 区间层产出显式数值见证：区间端点（有理，limit_denominator 精度登记在案）、
有理预条件子 C、Krawczyk 像盒各端点、以及 Jacobian 非奇异的**可计算证据**；
Lean 侧只做可计算的证书核验——绕开 Leibniz `Matrix.det`，改用：
  (i) 预计算行列式值 + 恒等式核验（如 det·adjugate = det·I 逐元有理等式 by decide），或
  (ii) 可计算行列式实现（**有理 Bareiss 无分式消元**，n=11/19 精确整数运算，
      复杂度 O(n³) 大整数，native_decide 可及），
      辅以「可计算 det = Matrix.det」一次性桥接引理（Leibniz 层证明一次，全族复用）。
- 可行性：**高**。信任基清晰：Python 仅为见证生成器，Lean 核验不信赖 Python 正确性
  （见证无效则核验 fail，fail-closed）。
- 工作量：**中**。需新设见证证书 schema（可参照 EXT05-BATCH-01-results.json 既有字段扩展）、
  Bareiss/恒等式核验器（可复用 CERT-LATTICE-LEAN-01 / CERT-K4-LEAN-01 的 by decide 族经验，
  二者公理审计双干净 @3a5edd44）、桥接引理一件。
- Python 层复用度：**高**（区间端点、有理中心、预条件子均已产出并登记，扩批四例有理中心
  已在 RESULTS.md 备 Lean 移植段列出）。
- 优势：**同时封两根因**（log 由见证核验的区间界覆盖，或叠加路线 A 彻底消除；
  det 由可计算实现替代）。通用性强，可沉淀为联邦「区间见证→Lean 核验」模板。

### 路线 C · leancert 上游扩展（ADSupported 加 `Expr.log`）
向上游 alerad/leancert 提 patch：`Expr.log` 纳入 ADSupported 并配区间界 soundness 证明。
- 实测上游状态（2026-10-10 API 探针）：default_branch=main，最近 push 2026-10-02（活跃），
  open_issues=0，stars=49，未归档。**维护活跃但社区规模小**。
- 可行性：**中**。log 的区间外向舍入界 + 可微性证明非平凡；接受与否、排期均属外部依赖。
- 工作量：本联邦侧小（patch 起草），但关键路径外置。
- Python 层复用度：高（与重做正交）。
- 风险叠加：FINDING-04 附带确权已载 leancert tag 远端重指向漂移（v4.35.0 `a5777840` ≠
  工件钉定 v4.34.1 `7f91b6eb35`）——上游 patch 若落在漂移后的 tag 上，重钉需另走环境波次
  （OBL-EXT-03r 已关闭，重开成本高）。定位为**平行低成本探针**，不入关键路径。

### 路线 D · 判定核分治（per-instance 小核 + 全族元定理）
将每件族证书拆为「实例数据（有理 c/ε/中心/预条件子）+ 通用核验核」两段，
通用核对任意实例数据做一次可计算核验（内嵌 Bareiss 可计算 det），
实例正确性退化为数据代入后的 `by decide`/`native_decide`；
再证一件元定理「核验核通过 ⇒ Krawczyk 严格内包 ⇒ 盒内唯一实根」（Leibniz 层，一次性）。
- 可行性：中-高（本质为路线 B 的架构化形态，核验核=见证核验器的固化）。
- 工作量：中-大（元定理是新增 Leibniz 层证明义务）；但 10 例及未来扩例边际成本趋零。
- Python 层复用度：高。适合作为 B 的演进形态而非独立首波。

## 4. 验收判据（可机器复核 pass/fail）

- AC1（核验通过）：10/10 实例在钉定 leancert 版本下 `native_decide`=true，
  或显式 checker（见证核验器）返回 true 且 `verify_proof` 式留痕可复跑。
- AC2（支持域覆盖）：改写/见证化后系统 `checkADSupported` 11/11、19/19 = true（路线 A 叠加时适用）。
- AC3（公理审计干净）：全族 `#print axioms` 无 sorry、无新增自定义公理；
  标准公理集与 CERT-LATTICE-LEAN-01/CERT-K4-LEAN-01 基线一致。
- AC4（双层一致）：Lean 核验结论与 Python 区间层 10/10 inside=True 逐项对齐；
  负面控制（g 中心 +1e-6）在 Lean 核验器上同样拒证（fail-closed 实证）。
- AC5（pin 完整）：工件钉定 commit oid 与实际编译所用 leancert 一致；
  tag 漂移监控条目同步更新。

## 5. 里程碑与依赖（自治分级：A=分机自治执行；B=需判定席/枢核签署）

| 段 | 内容 | 分级 | 依赖 |
|---|---|---|---|
| M0 | 本立项卡草案落仓（本件） | A | FINDING-04 |
| M1 | 判定席双轮评审：正则轮（问题/目标/判据存在且可复现）× 判定轮（路线取舍刚性分类） | B | M0 |
| M2 | 实施波次一：路线 A 方程改写 + Python 全量预检 10/10 + 负控保留 | A | M1 通过 |
| M3 | 实施波次二：见证证书 schema + Bareiss/恒等式核验核 + 桥接引理 + 10 例重发证 | A（执行）/B（验收） | M2 |
| M4 | 公理审计 + AC1-AC5 全量复核 + 判定轮终验销账 | B | M3 |
| 平行 | 路线 C 上游 patch 探针（非关键路径） | A | 无 |

## 6. 风险与回退

- **R1 内包裕度风险**：改写后 Jacobian 改变，ε=1/20 处 cond 已达 1.1e3（k6）/3.5e2（k10），
  Krawczyk 内包可能失败。回退：盒半径与中心精度同步收紧（RESULTS.md 已预留此建议），
  或分实例降 ε 档重发证。
- **R2 Bareiss 大整数性能**：n=19 精确有理 Bareiss 中间值膨胀，native_decide 超时风险。
  回退：改走恒等式核验（预计算 det 值 + adjugate 恒等式），核验复杂度 O(n³) 常数更小。
- **R3 定理证伪风险**：若重做过程中某实例被证明实际不成立（内包在收紧精度下仍失败），
  走 **F-VERIFY-06「先封缄后变异」** 规程：原证书先封缄（hash + provenance 双锁，
  参照 qtlv 封缄先例入册 FM-012 候选纪律），初判不抹除、校正留痕，
  再开变异流程重生证书；Hexagon 文稿口径同步核査（其声明层为 Python 认证，冲击有限）。
- **R4 外部依赖漂移**：leancert tag 重指向漂移已确权入册；重做全程以 commit oid 钉定为准，
  不采信浮动 tag。

## 7. 推荐意见（WS-17 智囊建议，待判定席裁定）

**主线：路线 B（见证证书化），内嵌路线 A 作为方程层子任务，M4 后向路线 D 架构化演进；
路线 C 作平行探针。**
理由：A 单独不触根因二，不足以独立达标；B 一役双封、Python 层复用度最高、
信任基 fail-closed 且可沉淀联邦模板；C 关键路径外置不可依赖。

## 8. 提请判定席问题清单

1. 口径：显式 checker + 见证证书是否视同「机器验证证书」，还是必须 native_decide 原生通过？
2. 信任基边界：Python 产见证作为外部输入，其 schema 是否需纳入公理审计面（类比验签 stub 教训 F-VERIFY-05）？
3. pin 策略：重做后维持钉定 v4.34.1（`7f91b6eb35`），还是顺势评估 v4.35.0（已知 tag 漂移，需先确权）？
4. 可计算 det（Bareiss）与 Matrix.det 的桥接引理：是否要求独立成证书件并过双轮？
5. 路线 C 若上游接受 patch，是否触发全族重钉 + 全量重验的强制波次？
6. 扩批四例（ε∈{1/10,1/20}，尚无 Lean 件）是否纳入本 OBL 范围，还是另开义务？

—— 枢/PIVOT-01 · WS-17 · 2026-10-10
