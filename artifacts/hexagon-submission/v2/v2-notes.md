% CLASSIFY: L1
# v2-notes.md — Hexagon 2610.00183 v2 全纸化写作口径(WS-19/PIVOT-01)

## 背景
v1(2610.00183v1,注册式短文 8913B)被 moderation 以 `outside_repository_scope`("not a paper")
驳回(board/FINDING-20261011-01)。v2 为完整论文体例:abstract 五成分保留,补齐
Introduction/Related Work/方法章/形式命题集/复现性/局限章/结论/双附录/手工 thebibliography。

## 每章素材出处映射
| 章节 | 内容 | 出处(vci-inbox) |
|---|---|---|
| Abstract/§1 | 五成分骨架、D1/D2 对象语言、三值判定 | v1 种子 artifacts/hexagon-submission/main.tex;board/LAB-THEORY-01R-FK01R-20261009T0620Z.md(D/A/T 层) |
| §2 Related Work | Lean4/Mathlib/Carneiro ITP2019/Lean4Lean(arXiv 2403.14064)/Moore1966/Krawczyk1969/Rice1953/Sinkhorn1967/Cuturi2013/Bertsekas1988/Hanley&Lippman-Hand1983 | 全部为真实文献;T2A header 明示 Mathlib 快照含 ComputablePred.rice₂(Carneiro ITP2019) |
| §3 格 completion | 7 join 缺口枚举见证、11 元、1331 三元组、嵌入映射 | LAB-THEORY-01R 附录 CERT-LATTICE-01;artifacts/lean-verified/CertLatticeLean01.lean(rid 1dfa70b6-…) |
| §4 生命周期机 | 9 合法迁移表、11 非法、I1 修正(规约缺陷亮点,Remark) | LAB-THEORY-01R CERT-K4-01;CertK4Lean01.lean(rid 16618831-…,header 明示 I1 精确修正) |
| §5.1 circulant | 闭形式、Krawczyk 判据、六例 cond 22.2–43.1、K 宽 2.55e-15–6.93e-14、盒半径 1e-9、扩批 10/10 | CERT-CIRC-LEAN-01/family/README.md、EXT05-BATCH-01-RESULTS.md、CertCircLean01.lean header |
| §5.2 auction | 5/5 实例表、δ-deflation、Birkhoff k 倍括弧、阴性对照 97.28–130.71 | CERT-AUCTION-01/README.md |
| §5.3 FINDING-04 | leancert 无 Expr.log(checkADSupported 11/11=false)、Matrix.det Leibniz 组合爆炸;认证由 Python 区间层承载;v1 措辞纠偏 | board/FINDING-20261010-04-…md(原文如实转写) |
| §6 Rice 模板 | rice_bridge/ext_of_pointwise/rice_pointwise + 实例 3+4、beta 红点工程注记 | artifacts/lean-verified/T2aTemplate.lean;T2A-BRIDGE-01/README.md、t2a_bridge.lean、INSTANCES-EXT01 |
| §7 SELFCHECK | add_sound/neg_sound/check_sound/end_to_end 4 定理 | artifacts/lean-verified/CertSelfCheck01.lean(rid d9034a05/44208d46/082321e6/f3c1fc61) |
| §8 复现/公理审计 | 白名单 propext/Classical.choice/Quot.sound、无 sorryAx、lean-4.28.0、fuzz E30/D60/K30 + rule-of-three 9.5/4.9/9.5%、pin 漂移告诫 | 各 .lean header;LAB-THEORY-01R CERT-T4-01;FINDING-04 附带确权段 |
| §9 局限 | AI 生成、人类理解度 partial、CIRC 边界、拍卖可信边、无保证、有限载体、A2 不消除、T2b 仅论题 | LAB-THEORY-01R 内核边界章;ai-use-disclosure.md;FINDING-04;CERT-AUCTION-01 诚实边界 |
| App. A/B | 工件索引 + 全量 rid | v1 附录 commit 锚 + 各 header |

## 诚实性自查清单(逐项)
- [x] rule-of-three 上界保留,"未观察到假收"锁定措辞,无"保证"字样(§8.4、§9.4)
- [x] FINDING-04 独立成节(§5.3),认证承载层=Python 区间层明示,Lean 件定性为"形式化陈述稿";
      v1 abstract "ported to leancert with verify_unique_system_root certificates" 措辞在 §5.3 明示纠偏
- [x] 格定理数:header 报 14,文件实含 15 个 decide 定理——Remark(§3)如实注明
- [x] 拍卖族 primal 可行性未区间化认证、无 Lean 移植——Remark + §9.3
- [x] I1 规约缺陷(decide 证伪原陈述)如实写入 §4 Remark,作为亮点
- [x] 公理审计白名单三件套 + 无 sorryAx;leancert tag 漂移风险入 §8.3
- [x] AI 署名:no-human-author-claimed 延续(title/§1 provenance/§9.1),transcript 留存声明延续
- [x] 密钥零落文;全部引文为真实文献,不确定者未引
- [x] 首行 % CLASSIFY: L1

## 编译验证
- 本机无 pdflatex;以 tectonic(等同 pdflatex 引擎 XeTeX 系)编译:零 error,仅 overfull hbox 警告,
  产出 main.pdf 16 页 letter、正文抽取约 6967 词。
- 宏包保守:amsmath/amssymb/amsthm/geometry/booktabs/array/hyperref;无 unicode 字符(全 ASCII);
  括号/环境配对、\label-\ref、\cite-\bibitem 一致性经脚本静态核验通过。

## 未做/待办
- 未执行重投(须先过 LABJUDGE-EXT08 双轮内审,见 FINDING-20261011-01 处置 3)。
- anc/ai-use-disclosure.md 沿用 v1 随附件,不在本目录重复。
