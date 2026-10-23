CLASSIFY: L1
# WSF-EVIDENCE-SWEEP-20261023-01 · WS-F 挂账 6+2 项外部证据搜索(饱和批 R2 席)

- 搜索 as-of:2026-10-23
- 本地定义锚:board/W-NS-03-REFORGE-CHARTER-01.md §2.2/§2.3 diff 主表(L86–L114);LAB-CLOSE-EXT18-20261020T2304Z.md L19/L52
- 执行:R2 席(explore,只读,零本地改动);本件由枢整编登记

## 一、WS-F diff 无证据 6 项

### U-04|yaml L25 短钉「qf-os://…NS-PROOF-FRAME-01.md@58dfb9a94311」(12-hex 短钉、协议未登记)
**判定:部分证据。** 12-hex 短钉形式有 git 官方依据,但短钉唯一性是仓库相对且非永久的;「qf-os://」协议无外部登记,仍需内部登记解析规则或换 40-hex。
- git-scm.com/book/en/v2/Git-Tools-Revision-Selection(Pro Git 官方):「Git can figure out a short, unique abbreviation for your SHA-1 values… it defaults to using seven characters but makes them longer if necessary to keep the SHA-1 unambiguous」「Generally, eight to ten characters are more than enough to be unique within a project.… no two objects whose SHA-1s are identical in the first 12 characters.」
- git-scm.com/docs/git-rev-parse:「--short[=<length>] Same as --verify but shortens the object name to a unique prefix with at least length characters. The minimum length is 4…」
- 佐证(惯例层):renenyffenegger.ch 注记「the recommendation is to up this value to 12 (at least for Linux Kernel development)」。
- 检索式留痕:①git abbreviated commit hash uniqueness short SHA official documentation ②git rev-parse --short core.abbrev minimum unique abbreviation ③"qf-os" protocol scheme URI git(0 命中,证 qf-os 无外部登记)。

### U-12|capAnchorP1 / zetaAnchorImpliesRHCriticalLine 二 decl 公理字段未被审计清单覆盖
**判定:部分证据**(审计方法学有 Lean 官方依据;具体公理集仍须随 L2-2 复算窗口实跑)。涉 RH 截断钉:**「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」**。
- lean-lang.org/doc/reference/latest/ValidatingProofs/《Validating a Lean Proof》:「check that it reports only the built-in axioms `propext`, `Classical.choice`, and `Quot.sound`」「This command prints the set of axioms used by the theorem and the theorems it depends on.」
- leanprover-community.github.io《Did you prove it?》:「after `#print axioms my_proof` the system should return `[propext, Classical.choice, Quot.sound]` (or some subset of these axioms). User-defined axioms, or `sorryAx` … indicate that your proof is incomplete.」
- lean-lang.org Axioms §8.4:「There are four standard axioms in Lean. The first three axioms are important parts of how mathematics is done in Lean: `Classical.choice` … `propext` … `Quot.sound` …」

### U-13|galerkinNS_exists_unique_solution_upto 打包 decl 未逐件审计(拟以「由三已审组分直接打包」桥接)
**判定:部分证据。** `#print axioms` 报告传递闭包,「打包件公理集=组分公理集之并」的桥接方法学成立;但打包 decl 是否引入额外依赖只能实跑判定,桥接不能替代审计。
- 同 U-12 来源 1:「the set of axioms used by the theorem **and the theorems it depends on**」;proofspath.com《Sorry-Free Discipline and Axiom Auditing in Lean 4》(2026-09-26):「#print axioms is transitive, not local. The command reports every axiom in the transitive dependency closure.」

### U-17|yaml alignment 第 5 条指帧 §3.2「CAP 证书锚/ζ 锚」,帧 §3.2 实无此条目(编号归属不符)
**判定:部分证据。** 归属不符是内部登记问题,外部搜索不能销账;ζ 锚所指 RH 临界线语义有 Clay 官方出处,可支撑 yaml 指针修订后的语义目标。涉 RH 截断钉:「有限高度 T=100/1000 截断」「区间见证层 PASS、kernel 层未证、非 RH 证据」。
- claymath.org/millennium/riemann-hypothesis/(官方问题页):「The Riemann hypothesis asserts that all interesting solutions of the equation ζ(s) = 0 lie on a certain vertical straight line.」「This has been checked for the first 10,000,000,000,000 solutions.」(Bombieri 官方 PDF 两处 URL 抓取失败,标**待核**。)

### U-20|三槽 SHA-256 + 联合指纹未复算(登记转引二级)
**判定:部分证据。** SHA-256 权威复算基准(NIST FIPS 180-4)外部在位,复算动作仍须内部执行。
- nvlpubs.nist.gov/nistpubs/fips/nist.fips.180-4.pdf《FIPS PUB 180-4, Secure Hash Standard》:「This Standard specifies secure hash algorithms, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256. All of the algorithms are iterative, one-way hash functions that can process a message to produce a condensed representation called a message digest.」

### U-23|帧 §4.3「无 NL↔Lean 对齐缝(定理陈述即所证)」自评未审
**判定:无证据**(对主张本身;≥3 组措辞穷尽)。外部权威**反向支持挂账/降级**:kernel 通过与「陈述忠实于自然语言原意」是两个问题,后者须独立审计。
- lean-lang.org ValidatingProofs Trust 节:「This check is meaningful if one believes the formal theorem statement corresponds to its intended informal meanings and one trusts the authors of the imported libraries to be honest.」
- arxiv.org/html/2609.19814v3(MIP*=RE 形式化论文):「Because the Lean kernel cannot verify whether that target signature faithfully captures the informal theorem in the paper, one of the authors … audited the top-level theorem and its transitive definitions down to Lean primitives to rule out weakened conclusions or unintended hypotheses.」
- 佐证:aidiscoverywire.com(2026-10-11)「compilation is not semantic fidelity」;invarians.org wiki(2026-10-15)「The checks do not answer the other question, whether the statement means what it is taken to mean.」
- 检索式留痕:①Lean 4 kernel axiom closure transitive dependencies theorem ②Lean 4 kernel trusted computing base type checking theorem statement official documentation ③Carneiro "The Type Theory of Lean" thesis kernel soundness ④natural language Lean theorem statement fidelity alignment audit formalization gap。

## 二、帧 v1.2 两项

### U-22|帧 §4.3「Lean 4.10.0」口径过时,v1.2 拟升级钉 v4.35.0
**判定:有证据(可销账)。** v4.35.0 为官方正式版;另发现该版自带 `lake check`/`lake comparator` 与四个外部内核,可直接服务 U-12/U-13/U-20 复算窗口。
- lean-lang.org/doc/reference/latest/releases/v4.35.0/《Lean 4.35.0 (2026-10-12)》:「For this release, 214 changes landed.」「It also adds `lake check` and `lake comparator`, which check a project with Lean's kernel and, if requested, with several independent kernels that now come with the toolchain.」「#14990 adds `lake check`, which builds the default targets of the current project, exports them, replays the export through the kernel, and fails if anything uses an axiom other than the standard ones.」
- github.com/leanprover-community/mathlib4/releases(2026-10-16 快照):「v4.35.0 — chore: bump toolchain to v4.35.0 (#44806)」。

### U-27|帧 §3.3-A HWY 首现未展开,v1.2 拟展开为 Hou–Wang–Yang(HWY)
**判定:有证据(可销账)。** HWY 预印本实存,作者全名、语态、待评审状态全部可外部锚定。语态钉保持「报告了」;该文为待评审预印本,结论未确立;涉 Clay 表述维持「自评已核、外部复现中、未颁奖」纪律(HWY 初始数据在原点奇异,不触及 Clay 光滑数据备选——与本包「有限维 ODE 截断层」域限无涉)。
- arxiv.org/abs/2509.25116《Nonuniqueness of Leray-Hopf solutions to the unforced incompressible 3D Navier-Stokes Equation》(Authors: Thomas Hou, Yixuan Wang, Changhe Yang;v1 2025-09-29,v2 2026-03-19):「we provide, to our knowledge, the first rigorous computer-assisted proof demonstrating such nonuniqueness… The invertibility of the linearized operator restricted to the image of this finite-rank approximation is then rigorously verified using computer-assisted proofs.」
- github.com/Bingham-Research-Center/brc-navier-stokes dossier(2026-07-24):「**Status:** preprint claim; independent reproduction not yet completed」「Why this does not settle Clay: The initial data are critical and singular at the initial time.」

## 三、结转建议

可销账:**U-22、U-27**(外部证据足,帧 v1.2 照升级口径/展开 HWY 即可)。维持挂账:U-04/U-12/U-13/U-17/U-20(部分证据仅证方法/基准,须内部登记、实跑审计与复算)、U-23(主张无证据且外部权威反向支持降级)。下一步:借 v4.35.0 自带 `lake check --paranoid`/`lake comparator` 开设 L2-2 复算窗口,一并消化 U-12/U-13/U-20;qf-os 解析规则成文登记。
