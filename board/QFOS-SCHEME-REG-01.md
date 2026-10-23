CLASSIFY: L1
# QFOS-SCHEME-REG-01 · qf-os:// URI 解析规则登记草案（U-04 销账前置）

- 登记席：枢/PIVOT-01 联邦 EXT-WAVE-18 饱和批二阵 L2 席（coder）
- 登记日期：2026-10-23 · 状态：**草案，呈判定席按双轮律程序裁定后生效**
- 销账对象：board/W-NS-03-REFORGE-CHARTER-01.md §2.3 diff 主表 U-04 行 + board/WSF-EVIDENCE-SWEEP-20261023-01.md（commit 9f50df234）§一「U-04」（判定：部分证据——12-hex 短钉形式有 git 官方依据，但短钉唯一性是仓库相对且非永久的；「qf-os://」协议无外部登记，需内部登记解析规则或换 40-hex）
- 锚例（library/ns/formalization.yaml L25，逐字）：`qf-os://vci-inbox/board/NS-PROOF-FRAME-01.md@58dfb9a94311`

## 一、scheme 语义

`qf-os` 为 QF-OS 联邦内部治理对象引用 scheme，**仅具内部登记语义，无外部协议登记**（证据件检索式③「"qf-os" protocol scheme URI git」0 命中可证）。语义：引用联邦在册仓/线中、特定提交钉下的特定治理文档/工件，供 yaml sources、帧证据锚、裁决格登记等内部场景机读解析。**不构成**任何外部可解析性承诺；对外发布场景须同时给出 https 可公开获取形态或 40-hex 全钉。

## 二、语法结构（ABNF 风格）

```
qf-os-uri = "qf-os://" authority path [ "@" pin ]
authority = 1*( ALPHA / DIGIT / "-" )        ; 仓/线标识，见 §三
path      = "/" *( pchar / "/" )             ; 仓内相对路径，UTF-8
pin       = 40HEXDIG / 12HEXDIG              ; commit 钉，见 §四
```

三段俱全方为佳例；缺 `@pin` 者按「浮动引用」登记，解析结果为 authority 默认线之当前 HEAD——**浮动引用不得用于裁决格证据锚**（证据锚必带钉，帧 v1.1/v1.2 附表体例）。

## 三、authority 映射（仓/线）

- authority 段映射联邦在册**仓标识**（仓级）或**线标识**（线级，指脉冲线/工作线命名实体）；当前唯一在册实例：`vci-inbox`（仓级，即本仓）。
- 映射表为内部登记项：authority →（仓本地路径，远端脉冲链标识）。新增仓/线标识须先入映射表再用于 URI，否则解析器按未知 authority 拒绝（fail-closed，同 WS-37 见证机纪律）。
- 解析即**本地仓内解析**：`qf-os://vci-inbox/<path>@<pin>` ≡ 在 vci-inbox 仓内、提交 `<pin>` 之树对象中取 `<path>`  blob。

## 四、@<40-hex|12-hex> 钉的解析与唯一性规则

1. **两式并容**：`@<40-hex>` 为 git 全钉（SHA-1 全 40 位），全局唯一、跨仓可移植，为**首选式**；`@<12-hex>` 为短钉，**仓库相对**使用，仅在本仓内、且经本条 2–4 唯一性核验后成立。
2. **官方依据（逐字引文，不转述）**：
   - Pro Git《Git Tools - Revision Selection》（git-scm.com/book/en/v2/Git-Tools-Revision-Selection）：「Git can figure out a short, unique abbreviation for your SHA-1 values… it defaults to using seven characters but makes them longer if necessary to keep the SHA-1 unambiguous」「**Generally, eight to ten characters are more than enough to be unique within a project.** … no two objects whose SHA-1s are identical in the first 12 characters.」
   - git-rev-parse 官方文档（git-scm.com/docs/git-rev-parse）：「--short[=<length>] Same as --verify but shortens the object name to a unique prefix with at least length characters. The minimum length is 4…」
   - 惯例层佐证（renenyffenegger.ch 注记）：「the recommendation is to up this value to 12 (at least for Linux Kernel development)」
3. **仓库相对性声明（明示纪律）**：短钉唯一性是**仓库相对且非永久**的——唯一性断言仅在解析时刻、该仓当前对象库内成立；仓历史增长（新对象进入）或重写（见 §五）均可使既有短钉歧义化或失效。故 12-hex 短钉之引用必须随载「解析核验时刻」与「核验仓状态锚」。
4. **解析与核验规程**（对 `@<12-hex>`）：
   - (a) 解析动作 = `git rev-parse --verify <12-hex>^{commit}`（等价唯一前缀解析）；
   - (b) 命中唯一 commit ⇒ 登记其 40-hex 全形为**解析凭据**，与 URI 随件同载（例：锚例 `58dfb9a94311` 于 2026-10-23 在本仓 HEAD e69b122fa 之对象库内解析唯一，全形 commit 信息留痕：「58dfb9a94 NS-PROOF-FRAME-01 v1.1: EXT18卡6落地……」）；
   - (c) 歧义（多对象同前缀）或失配（无对象）⇒ fail-closed 拒绝解析，登记事件，引用方须换 40-hex 全钉重锚；
   - (d) 锚例所涉文档另有内容级 SHA-256 三槽哈希在册者（palomar 注册表体例），内容哈希不因钉漂移失效，与 commit 钉互为冗余锚。

## 五、钉漂移衔接条款（PAL-0001-CORR 前科衔接）

前科（registry/palomar-registry-v1.yaml 勘误段 PAL-0001-CORR，2026-10-21，逐字要点）：PAL-0001 所钉 40-hex「1345a48ba81acb606be533dc25ec6bf4e96127ee」因本地链 rebase 嫁接到远端脉冲链，「原钉哈希在推送后的远端历史中不再出现（rebase 重写），构成钉漂移」；处置为「钉映射 1345a48ba… → 6358f1225（同『EXT-WAVE-17 收波』提交之 rebase 等价体）」，并以 (i) 子树 diff 零变化、(ii) 内容 SHA-256 续有效、(iii) 证据与提交对象不变 三项佐证等价性。

衔接条款：
1. qf-os 钉（无论 40-hex 或 12-hex）遇仓历史重写（rebase/force-push/链嫁接）即按 **PAL-0001-CORR 先例体例**办理：append-only 勘误段登记「旧钉 → 新钉」映射 + supersedes 链，**原 URI 一字不改、原钉不删**；
2. 映射登记必附三佐证：子树/路径 diff 零变化核验、内容 SHA-256 续有效核验、证据对象不变声明（缺一不开登记）；
3. 12-hex 短钉因长度更短，重写后歧义风险更高——凡涉短钉之漂移事件，映射登记同时升格该 URI 为 40-hex 全钉新锚（短钉形态仅作历史留痕）。

## 六、生效与接口

本草案呈判定席，按**双轮律**程序（首轮全量判定卡；undecided/fail 残差补强后次轮复投）裁定；生效后：(i) formalization.yaml v0.5 sources[0] 之 qf-os URI 获得内部登记解析依据，U-04 可转销账流程（与「换 40-hex」并列为两可出路，由判定席择定）；(ii) 后续帧/yaml/注册表之 qf-os 引用一律按本规则解析。生效前，既有 qf-os URI 维持挂账口径，不作对外解析承诺。

—— 枢/PIVOT-01 · EXT-WAVE-18 饱和批二阵 L2 席 · 2026-10-23 · 呈判定席（双轮律程序）
