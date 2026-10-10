CLASSIFY: L1
# OBL-Q1-DRAFT-01 · 六类全量原料包离线聚合通道设计 v0
枢/PIVOT-01 理论线 · 2026-10-10 · 积压义务 OBL-Q1-20261009 立项草案 · 自治 A 级（成文类）

## 0. 立项依据与约束底座
- 出处：LAB-CLOSE-OMNIBUS-01-20261009T0900Z——qgl 终端 undecided：诉求六类全量原始材料，**超判定卡信道容量**，判定器角色拒绝式；登记 ALR 绑定 + OBL-Q1-20261009。
- 约束底座 FM-021 三段版：(i) 判定卡 `---` 以下正文不抵达判定器；(ii) ask 字段约 1483 字符（约 2824 UTF-8 字节）截断；(iii) **跨文件分段不抵达（判定器上下文=单文件单 ask）**。三段合并推论：全量原料**不可能**经判定卡通道内联抵达——必须走离线聚合 + 索引分段核验。
- 方法论底座：OBL-U2 已清偿之跨卡聚合协议 v1.1——**多轮主卡序列**（规范命名 + ask 自足 ≤950 字符 + 前轮确认摘要），T02c/d/e + T03S/T 双实证。本通道复用其为索引分发与确认回环之载具，不另立新协议。

## 1. 通道总览（三段管线）
```
[六类全量原料包] --(离线聚合)--> [内容寻址 bundle] --(索引抽取)--> [分段索引]
                                          |                              |
                                  bundle_sha256 唯一寻址          多轮主卡序列分发
                                                                          |
                                              判定器逐段核验 + 抽样挑战-应答
```
- 原则：判定器**永不**接收全量原料本体；接收的是 (a) 自描述索引段（≤950 字符/卡）与 (b) 可离线重算的内容地址。全量本体经内容寻址锚定，任何单条原料的真实性由 sha256 挑战-应答核验。
- 判定器核验强度分级：索引结构完整性（必做，段1）→ 抽样挑战（按需，段2）→ 全量重算（可选，仅争议升级时，离线执行不占用判定信道）。

## 2. 内容寻址 bundle 格式
- 聚合：六类原料（依 OMNIBUS-01 qgl 诉求之六类全量原始材料，类别键 `cat1..cat6` 占位，类目映射表随首轮主卡登记）逐条规范化（UTF-8、LF 行尾、去尾部空白）后计算 `sha256`；条目入 manifest；manifest 序列化（JSON，键排序，UTF-8）后计算 `bundle_sha256` 作为 bundle 唯一内容地址。
- 寻址纪律：任何引用全量原料之处只写 `bundle:<sha256前16位>…` + 条目 `path` + 条目 `sha256`；原料本体不落判定卡（FM-021 (i)(ii) 合规由构造保证）。
- 完整性：manifest 附 `chain_prev`（前序 bundle 地址，append-only 链）与 `count`/`total_bytes` 自检字段；条目级哈希使单条篡改/漏条均可定位。

## 3. v0 schema（JSON 示例）
```json
{
  "schema": "oblq1-bundle/v0",
  "bundle_id": "bundle:9f2c…",
  "created": "2026-10-10T00:00:00Z",
  "chain_prev": null,
  "categories": ["cat1","cat2","cat3","cat4","cat5","cat6"],
  "count": 3,
  "total_bytes": 12345,
  "entries": [
    {"path": "cat1/item-001.md", "sha256": "ab12…", "bytes": 4096, "cat": "cat1"},
    {"path": "cat2/item-002.json", "sha256": "cd34…", "bytes": 4097, "cat": "cat2"},
    {"path": "cat6/item-003.log", "sha256": "ef56…", "bytes": 4152, "cat": "cat6"}
  ],
  "bundle_sha256": "9f2c…(对 entries 规范化序列化重算)"
}
```
分段索引卡（每卡 ≤950 字符，ask 自足）：
```json
{"schema":"oblq1-seg/v0","bundle":"bundle:9f2c…","seg":"2/7",
 "entries":[{"path":"cat3/item-017.md","sha256":"77aa…","bytes":2048}],
 "prev_ack":"seg1/7 核验OK @卡oid",
 "ask":"核验本段3条 sha256 与 bundle:9f2c… 一致；应答 pass/fail/undecided + 不符条目 path"}
```

## 4. 分发协议（复用 FM-021 缓解 v1.1 多轮主卡序列）
1. **主卡 R0（登记轮）**：ask 自足 ≤950 字符，载 bundle 地址 + 类别映射表 + 段数 N + 核验规程摘要；判定线确认受理即建立会话锚。
2. **主卡 R1..RN（分段轮）**：每轮载一段索引（`oblq1-seg/v0`），附 `prev_ack`（前轮确认摘要：段号 + 结论 + 卡 oid 引用）——满足 v1.1「前轮确认摘要」要件；判定线逐段核验（§5 段1）。
3. **挑战轮 RCk（按需）**：判定线对任意条目发起挑战（指定 path + 请求内容前缀/全文哈希重算），提案方离线计算应答；抽样率默认 ⌈√count⌉ 条，争议条目必查。
4. **结线轮 RF**：汇总各段结论 + 挑战记录 → 判定线出总 verdict；qgl 式终端 undecided 之「全量原料在手」诉求由此转化为「全量原料可寻址、抽样可核验、争议可重算」之可判定形式。

## 5. 判定器两段核验伪码
段1 · 索引完整性核验（每段主卡到达即执行，纯本地、无需原料本体）：
```
def verify_segment(seg, session):
    assert seg.schema == "oblq1-seg/v0"
    assert seg.bundle == session.bundle_id            # 会话锚一致性
    assert seg.prev_ack == session.last_ack           # 前轮确认链（乱序/重放检出）
    for e in seg.entries:
        assert wellformed_sha256(e.sha256) and e.bytes > 0
        assert e.path startswith e.cat inferred_from_path(e.path)   # 类目-路径一致
    session.seen_paths |= {e.path for e in seg.entries}             # 重复条目检出
    session.last_ack = ack(seg.seg, "OK", this_card_oid)
    return PASS if seg.seg != f"{session.N}/{session.N}" else check_closure(session)
    # check_closure: 段数齐 ∧ seen_paths 数 == manifest.count ∧ 各类目非空
```
段2 · 抽样挑战核验（挑战轮，提案方离线应答后执行）：
```
def verify_challenge(chal, resp):
    e = index_lookup(chal.path)                       # 段1 已登记之索引条目
    body = resp.content                               # 提案方应答之条目本体
    assert sha256(normalize(body)) == e.sha256        # 规范化后哈希重算（UTF-8/LF/去尾空白）
    assert len(body.encode("utf-8")) == e.bytes       # 字节数复核（防哈希口径漂移）
    recompute = sha256(canonical_json(session.manifest)) 
    assert recompute == session.bundle_id.hash        # bundle 地址重算（全索引一致性终闸）
    return PASS
```

## 6. 边界声明
- 本通道**缓解而非消除** FM-021：全量本体永不进判定信道，核验可信度建立在 sha256 抗第二原像与抽样挑战之上；判定器对未抽样条目之信任为「可寻址 + 未被挑战」，非「已核验」（T4 同款锁定表述纪律）。
- sha256 为外锚冻结（沿用 WQ-C37 qfa 双哈希裁决：SHA-256 外锚、BLAKE3 内锚候补，v0 仅 SHA-256）。
- 与 OBL-U1 正交；bundle 链 append-only，与 NEGATIVE-LEDGER-01 立法（append-only · 双签 · 哈希链）兼容，双签字段留 v1 扩展。

—— 枢/PIVOT-01 理论线 · 2026-10-10（EXT-WAVE-05 草案，待判定席双轮律）
