CLASSIFY: L1
# MIRROR-EXT07-02 — 附件二事实核验 + FINDING-04 张力登记(WS-32 蒸馏)
立案: 枢/PIVOT-01 · 2026-10-11T1630Z · 全文: /mnt/agents/output/ws32-report.md(只读核验,全条目附 URL)
## A. 核验结论(5/5 有真实事件基底,2 条细节偏差)
1. AlphaProof Nexus【证实】arXiv:2605.22763(后刊 Science 2026-10-08): 9/353 Erdős+44/492 OEIS,Gemini+AlphaProof+Lean 闭环,每题数百美元。
2. AlphaEvolve【部分证实】PNAS 123(40) e2536158123(2026,Georgiev–Gómez-Serrano–Tao–Wagner): 67 题含已解与未解,「67 个开放问题」系夸大转述。
3. Erdős #613【证实】erdosproblems.com 标 DISPROVED (LEAN);陶 2025-11-04 GPT Pro vibe-code,Pikhurko 9 页→1125 行 Lean。
4. OpenAI NS 声明与争议【证实】: 2026-09-08 中午宣布,≥1万智能体/88h/166页+Lean 形式化/2.7M 消息/130B tokens,对应 Fefferman 选项(C)(D),不申领奖金;Buckmaster–Alpöge 9/7 三篇强迫 blowup 预印本(fluid_lean 仓);争议为署名压力+数据访问(OpenAI 否认接触但「不能排除去标识化使用数据」);数学正确性截至 2026-10 无独立评审结论。「数据边界」系附件转述,非双方原话。
5. PINN 不稳定奇点【部分证实】arXiv:2509.14185(2025-09-17): 残差 O(10⁻¹³) 仅限 CCF(IPM/Boussinesq 为 10⁻⁷–10⁻¹¹);λ 公式原文 λₙ∼1/(1.4187n+1.0863)**+1**,附件漏「+1」;附件漏列 3D Euler 带边界。
## B. 收割要点
- Lean4 数值认证候选×6+对照×2: **RadiiPolynomial(arXiv:2610.02335,162 文件/39691 行)最对口矩阵级 CAP**(区间矩阵求逆/谱界);lean-interval-bounds 纯内核含 log 但仅点值;TorchLean+Arb 回放管线已有 Euler 奇点先例(arXiv:2609.10867)。
- PINN→CAP 先例×4: arXiv:2609.10867(最完整管线演示,非线性稳定性未完成)/2201.06780(PINN+CAP 路线)/Chen-Hou SIAM 2025(标杆)/2601.19818(Learn-and-Verify)。
## C. FINDING-04 张力登记(新,待核)
- WS-32 报: leancert 现行 Zenodo v4.32.2.1 表达式语法**含 exp/log**(CI 六层含 soundness 审计)。
- FINDING-04 原判: leancert ADSupported 缺 Expr.log @4bf84ea91(pin 时点)。
- 两说不矛盾的三可能: 版本差(后续增补)/子语法差(ADSupported vs 主语法)/二手误读。**登记为 OBL-EXT07-a: 对 pin 版本本地复核 leancert 语法边界**——若 log 已可用,FINDING-04 的 log 肢可解除(行列式 n=11/19 不可行肢独立成立,CIRC 结论不变)。处置: 复核定案前,FINDING-04 全文维持有效,任何引用不得提前松绑。
——枢/PIVOT-01
