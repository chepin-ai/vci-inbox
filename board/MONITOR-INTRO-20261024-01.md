CLASSIFY: L1
# MONITOR-INTRO-20261024-01 — 外部突破引入核验与登记：Liu–Zhuang「SLE_κ 近 8 含拓扑 Sierpiński 地毯」

- 登记席：QF-OS 联邦 S1 席（EXT-WAVE-24 批十二·引入资源消化线）
- 登记日期：2026-10-24
- 触发源：微信「数学家」公众号文章（二手转述，来源层级见第四节）
- 本文不涉及 NS/RH 实质断言；NS C1–C3/C1′–C3′ 条款全适用但本次无逐字钉对象。
- 只写文不 commit；本批仅建此一个新文件。

---

## 一、原文核验（arXiv 一手，直连 abs 页成功）

- arXiv ID：**2506.09609**
- 标题（verbatim）：**"Schramm-Loewner evolution contains a topological Sierpiński carpet when $κ$ is close to 8"**
- 作者：**Haoyu Liu（刘浩宇）, Zijie Zhuang（庄子杰）**；提交人（From）：Zijie Zhuang
- 版本史（Submission history，arXiv 页 verbatim）：
  - **[v1] Wed, 11 Jun 2025 11:09:49 UTC (556 KB)**
  - **[v2] Sun, 12 Oct 2025 02:07:27 UTC (612 KB)**
- 学科分类：**math.PR**（Probability，arXiv:2506.09609v1 [math.PR]；HTML 版页眉确认）
- 摘要关键句（verbatim，自 abs 页摘录）：
  > "We consider the Schramm-Loewner evolution (SLE_κ) for κ ∈ (4,8), which is the regime where the curve is self-intersecting but not space-filling. We show that there exists δ₀>0 such that for κ ∈ (8 − δ₀, 8), the range of an SLE_κ curve almost surely contains a topological Sierpiński carpet."
  >
  > "Combined with a result of Ntalampekos (2021), this implies that in this parameter range, SLE_κ is almost surely conformally non-removable, and the conformal welding problem for SLE_κ does not have a unique solution. Our result also implies that for κ ∈ (8 − δ₀, 8), the adjacency graph of the complementary connected components of the SLE_κ curve is disconnected."
- 正文要点（html/v2 快照佐证）：
  - 主定理 Theorem 1.2 即上述地毯包含结论；Theorem 1.3 给出共形不可去（conformally non-removable）。
  - 方法链：imaginary geometry（GFF 流线图，Miller–Sheffield 框架）内构造**分形渗流（fractal percolation）**终保留集 ⊂ SLE 轨迹（第 3 节）；κ→8 时空间填充 SLE 的**依分布收敛/一致性论证**（Claim 4.6 等，Lemma 3.5 的 n-good 概率→1 依赖此）；**量子圆盘/薄量子圆盘共形焊接**边界长度过程为锥内相关二维 Brown excursion（相关系数 −cos(4π/κ)），用于焊接非唯一性论证（第 7 节）。
  - 引用 Ntalampekos [Nta21] 判据 + Whyburn [Why58] 拓扑地毯刻画。
- 一手 URL：
  - https://arxiv.org/abs/2506.09609
  - https://arxiv.org/html/2506.09609v2
  - https://arxiv.org/pdf/2506.09609
- 外部佐证：清华求真书院 2025-12-18 学术报告页（speaker 刘浩宇，北京大学；摘要与 arXiv 摘要一致，注明 "joint work with Zijie Zhuang (UPenn)"）—— https://qzc.tsinghua.edu.cn/en/info/1122/4771.htm
- **核验结论：arXiv 件真实存在，v1（2025-06-11）/v2（2025-10-12）两版，作者 Liu（PKU）× Zhuang（UPenn），与公众号报道一致。真实性确认，置信度高。**

---

## 二、微信文与原文对照表

| # | 公众号转述断言 | 原文依据 | 判定 |
|---|---|---|---|
| 1 | κ 从下方趋近 8 时 SLE_κ 轨迹几乎必然包含拓扑 Sierpiński 地毯 | 摘要/Theorem 1.2 verbatim 对应（∃δ₀>0, κ∈(8−δ₀,8)） | ✅ 有原文依据。注意科普"趋近 8"是极限式表述，原文是存在性邻域 (8−δ₀,8)，非任意趋近过程；属可接受的科普简化 |
| 2 | 方法含"共形焊接" | 摘要含 conformal welding 非唯一性结论；正文共形焊接量子圆盘（[AHS23a/b] 框架） | ✅ 有原文依据，但焊接在原文中主要是**结论/推论**（非唯一性）与第 7 节工具，地毯包含主定理的核心方法是分形渗流+虚几何 |
| 3 | 方法含"量子圆盘" | 正文 weight (2−γ²/2) 薄量子圆盘、边界量子长度二维 Brown excursion | ✅ 有原文依据（工具层） |
| 4 | 方法含"一致性论证" | 推定为 κ→8 时空间填充 SLE 依分布收敛（Claim 4.6/Step 1 of proof）及 n-good 概率一致趋 1（Lemma 3.5） | ⚠️ 有对应内容但公众号措辞模糊；原文并无名为"consistency"的定理，属科普概括 |
| 5 | 刘浩宇（北大）× 庄子杰（宾大）合作 | 作者署名 + 清华求真报告页注明 Zhuang (UPenn) | ✅ 与一手署名一致 |
| 6 | 庄子杰为"丁剑/孙鑫门"（门生谱系） | arXiv 件不含师承信息；孙鑫为 Zhuang 的 UPenn 导师、丁剑为 PKU 概率方向导师，与公开学术谱系常识相符 | ⚠️ 公众号自述层级，未独立核验，标注为二手 |
| 7 | 遗漏项：公众号未见强调的三条推论 | 共形不可去性、焊接非唯一性、补邻接图不连通（摘要后两句） | ℹ️ 科普聚焦地毯几何，省略了原文同等重要的焊接非唯一性结论；转述不完整但无错误断言 |

**总评：公众号转述核心数学断言与原文摘要一致，无虚构；方法描述顺序有科普化重组，师承信息属自述层级。**

---

## 三、与联邦面关联评估

1. **直接数学关联：无。** 联邦主线为 NS 有限维 ODE 截断层 / RH 区间见证层 / Lean 形式化。本对象为二维统计物理标度极限的随机共形几何（SLE/LQG/虚几何/分形渗流），与 NS 正则性、RH 零点、形式化验证在对象、方法、结论三个层面均无交集。
2. **严禁攀附声明（如实登记）：** 该成果**不构成**对联邦 NS/RH 工作的任何支持、佐证、启发性输入或方法迁移候选；不得在任何联邦文档中引用为相关性证据。κ→8 的邻域存在性论证与 RH 区间见证的"区间逐字钉"在认识论上异构，不做类比。
3. **唯一可联点：** 「外部数学突破监测」维度——北大×宾大华人青年学者在 SLE/随机几何方向的顶刊级预印本（已被 Ann. Probab. 相关文献引用，arXiv 件 cited by ≥3），反映引入资源通道（公众号→arXiv）的可达性与时效性（v1 2025-06，报道时点晚于 v2）。
4. **登记建议：** 作**一次性登记**，**不入 B1–B10 体系**。理由：B 体系面向与联邦主线有持续交互面的对象；本件无后续动作项（无复现、无形式化、无引用需求），仅作监测面留痕。若未来 SLE 随机几何与联邦面出现实质交叉信号（概率极低），可由此件回溯激活。
5. 登记性质定级：**监测面扩展对象（monitoring-surface extension, one-shot）**。

---

## 四、来源层级注记

| 层级 | 来源 | 用途 | 可靠度 |
|---|---|---|---|
| 一手 | arXiv:2506.09609 abs/html/pdf（本核验直连成功） | 标题/作者/版本史/摘要 verbatim/方法 | 高（预印本，未经同行评审——注意：arXiv 真实性 ≠ 数学正确性已被审稿确认；本文不评判证明正确性） |
| 一手旁证 | 清华求真书院报告页（2025-12-18） | 作者单位、合作关系 | 高 |
| 二手 | 微信「数学家」公众号文章 | 触发源、科普转述、作者履历自述（师承"丁剑/孙鑫门"未经独立核验） | 中（科普转述，本次逐条对照未见虚构） |

**留痕：本件仅核验"报道与原文是否一致"，不核验论文数学证明本身；后者超出本席职责与能力边界，如实注明。**
