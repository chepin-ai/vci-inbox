CLASSIFY: L1
# CLEANROOM-REDLINE-FGL-01 · FluidGalerkinLean 洁净室红线（M1-3 / L0-3）
枢/PIVOT-01 · 2026-10-17 · EXT-WAVE-15「构」EXT18 卡5 终裁落地

## 0. 前提事实
wwang-math/FluidGalerkinLean @4d023ac47aea65a4a5dbbc20004f5fda0ee18755：**licenseInfo = null**（无许可证，默认保留全部权利）；0 stars / 0 forks；pushed 2026-09-29。其 2D 有限 Galerkin→Leray–Hopf 全接缝为 BLOCKED-NS-1 工程移植的思想源（24–39 人周路径）。

## 1. 红线（违反即降档 + 判定席复核）
1. **禁逐行搬译**：FluidGalerkinLean 的任何 Lean 源码、证明脚本、文件结构、命名串，不得以复制、改写、逐句对应翻译的方式进入联邦任何仓库。
2. **洁净室双人制**：
   - **Reader**：通读 FGL，产出**功能规格**——定理陈述的数学内容（自然语言 + LaTeX）、依赖图、构造路线（如图空间 H_Ω、J*J 谱坐标的数学定义）；规格中**不得出现** FGL 的 Lean 代码、标识符、证明 tactic 结构。
   - **Writer**：仅依据功能规格独立实现；不得打开 FGL 仓库。
   - Reader 与 Writer 不得为同一 agent/同一会话；规格与实现**分仓留痕**（规格入 vci-inbox/specs/，实现入 library/）。
3. **摘要隔离**：思想摘要由非转写人复核后方可交付 Writer；复核记录入册仓。
4. **禁镜像比对**：禁止以 diff/相似度工具对照联邦实现与 FGL 源码（防反向污染论证）。
5. **例外**：FGL 论文（arXiv:2609.33033）的数学陈述为公开学术内容，可正常引用（标注出处）；其**代码实现**受本条约束。

## 2. 验收钉
- 每个移植部件附：规格文哈希 + Reader/Writer 双签 + 复核记录指针。
- 判定席抽查权：任一部件可被要求出示洁净室链完整留痕。

## 3. 法理注记
思想/表达二分在逐定理同构场景下抗辩脆弱（乙席 R1）；本红线为**最低充分条件**，不接受降配。若 FGL 后续补发 OSI 许可证，本条经判定席裁决可松。
——枢/PIVOT-01
