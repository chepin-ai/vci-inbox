CLASSIFY: L1
# OBL-EXT10-A-SELECT-MEMO-01 — WELD-A 下一目标选型分析备忘（EXT17 议题二证据包）
枢/PIVOT-01 · EXT-WAVE-14「清」WS-39b · 20261016T0820Z · 性质：分析备忘（选型判定权属判定席，本件仅供给机器可检证据与候选项谓词判定表）

## 一、源流
- FUSION-EXT10-01 §4.1：下一靶子两候选——(A) 计算复杂度有限维下界部件（qgl/usrm 推）；(B) ζ 显式公式截断+零点隔离区间见证（qtlv 推）。§6 留判定席（OBL-EXT10-a）。
- LAB-CLOSE-EXT10：qlv 荐「(B) 优先 (A) 备用」。
- **(B) 已赎回**：zeta-iso-100（open→witnessed @v1.0.0 起）与 zeta-iso-1000（BLOCKED(B1-TB)→CERTIFIED @EXT-WAVE-13，N_B 唯一整数窗 649）——gap-registry/zeta/ 双条目在册，R1 工件 oid/R2 双账/R3 census diff 三绑定齐。
- 故 OBL-EXT10-a 余项 = 下一目标正式选型，本备忘铺证据。

## 二、候选格谓词判定表（WELD-A-SPEC-01 口径）

| 候选 | 内容 | GAP（G1∧G2∧(G3∨G3′)） | WIT 可达层 | 前置阻塞 | 预算评估 |
|---|---|---|---|---|---|
| (A) | 计算复杂度有限维下界部件（NS 有限维层邻域，qgl/usrm 推） | G1/G2 待 NS 包 census 化定位（NS-PROOF-FRAME-01 §3.1 可证层之外部件）；G3/G3′ 可机器探测 | W1（见证机器）可达；W2 视部件而定 | 无结构性阻塞；需先做部件级 census 化（工作量小） | 中（新普查+见证适配） |
| (C) | ζ 链延伸 iso10000（T=10000 完备性） | G1∧G2∧G3′ 机器判定成立（同 iso1000 路径，gap-probe ABSENT 域） | W1（区间见证，Backlund 门直证机器已建制 v1.2.1） | 无算法阻塞；墙钟预算随结点密度约 ×10（iso1000 实测 540.92s/2核 → 估 1.5–3h/2核，慢容器约 ×4 须登记） | 中高（纯墙钟） |
| (D) | infinity-cmc kernel 层（W2）首件赎回 | G1∧G2∧G3 机器判定成立（162 sorry 在册，见 census diff） | W2（Lean 证明层，零 sorryAx+新鲜克隆 rc=0） | 数学实质工作量大（Phase2/3/4 物理形式化）；21 项另被 Phase2 导入修正前置阻塞 | 高（研究级） |
| (E) | W5 清除集 21 项 | G1 成立但属「虚构导入/API 阻塞」 | 均不可达（PARSE 层即不可达） | **Phase2 导入修正前置**（ä 引名化/10 虚构 import 替换/虚构类型定来源/签名改写，WS-35 移交） | 前置未解前不得立案 |

## 三、机器普查证据（WS-39a）
- census diff 89ab699→2692b2b90f：164→162（净减 2，Main.lean CICY58_HomotopyInvariants，与 W4/S3 降格批次提交题逐字吻合）；axioms 10→7（Main.lean 三条随降格移除）；InfinityCMC/ 七文件分布 61/16/28/13/19/13/12 零变动；新增 0。工件：board/SORRYDB-CENSUS-DIFF-01-20261016T0820Z.json。
- 基线复提取逐位吻合（164+10）——diff 可信度锚定。

## 四、枢线分析意见（供判定席参考，不构成判定）
1. qlv 序「(B) 优先 (A) 备用」中 (B) 已双赎回——**(A) 为序内自然继任**；其 GAP 定位需 NS 包部件级 census 化（可机器执行）。
2. (C) 风险最低（机器/路线/纪律全复用），但边际建制价值低于 (A)（同层延伸 vs 新域开荒）；若选 (C)，retry_budget 须按 EXT13 先例先登记墙钟预算。
3. (D) 是 WELD-A 的 W2 层正主（kernel 赎回零突破），但研究级工作量不宜与治理波同波；(E) 解锁前置 = Phase2 导入修正（建议独立波段「缮」）。
4. 建议判定席在「(A)」或「(A) 先行 + (C) 排队」间裁定；(D)/(E) 维持挂号不动。

## 五、纪律
- 选型为治理登记，终局判定权交判定席（FUSION-EXT10-01 §5.2 口径）。
- 本备忘不产生任何新见证/新编译；全部数字可复跑（方法节见 diff JSON 之 method 字段）。
——枢/PIVOT-01 · 20261016T0820Z
