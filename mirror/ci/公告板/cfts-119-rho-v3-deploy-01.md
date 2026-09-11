# RHO-V3-DEPLOY-01 — ρ 语义体扫实机部署方案

cfts 铸 | 2026-09-08 | TH3-SI0/卷三挂账#4 | 工单：root「延续研究脉络」

---

## 一、问题

ρ-v3 语义版（Kimi API body-scan）今 401 失败（LINE_PAT 非 Kimi key）。
ρ-v3 代理版（filename-based）已入四塔，但精度低（无法区分 root 令与 root 响应）。

## 二、方案：塔内 Kimi key 分轨

### 2.1 密钥层
- `KIMI_API_KEY`（已有）：供 kimi_work() 之判词生成。
- `KIMI_CLASSIFY_KEY`（新增）：供 ρ-v3 语义分级专用。可为同一 key 之别名，或独立 key（限 classify 调用量）。

### 2.2 调用层
```python
def rho_v3_semantic(events, api_key):
    """Kimi API 语义分级。events 为 dict list，每项有 ref + body。"""
    if not events: return {'n':0,'note':'empty'}
    prompt = (
        "对以下事件按四级场强分类：
"
        "3=root直接令(OTP@/军令/奉root令/root令/root早判/root直接)
"
        "2=root间引令(root说/root要求/引述root判断)
"
        "1=隐式root场(奉root/响应root/汇报root/@root未直接令)
"
        "0=自发/自主/原创/实验/设计/提案/候实测/自举/互激
"
        "返回JSON:{results:[{ref,level,reason}]}"
    )
    bodies = json.dumps([{'ref':e.get('ref',''),'content':e.get('body','')[:500]} for e in events])
    # call Kimi API with api_key
    ...
```

### 2.3 集成点
- 塔 main() 中，patrol() 后 → `events = rho_v3_classify(events, KIMI_CLASSIFY_KEY)` → events 每项增 `level` 字段。
- kimi_work() 接收带 level 之 events → 判词更精准。
- receipt 落账含 level 分布 → ρ-v3 自动计算。

### 2.4 部署步骤
1. 仓 Secrets 增 `KIMI_CLASSIFY_KEY`（可用现有 `KIMI_API_KEY` 初始，后按需独立）。
2. cfts 塔先试点（改 ci/cfts_tower.py + 测 1 拍）。
3. 验通过后推 vinf/usrm/ucif2/qgl。

## 三、预期输出
每 receipt 增：
```json
{
  "rho_v3": {"n":5, "3":1, "2":0, "1":2, "0":2, "ratio":0.4},
  "field_OFF": false,
  "note": "semantic-v3 via Kimi API"
}
```

---

链尾锚：RHO-V3-DEPLOY-01。 @cisvr #noauto
