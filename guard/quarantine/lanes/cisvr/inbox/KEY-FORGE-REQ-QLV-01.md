# KEY-FORGE-REQ-QLV-01 · qlv 铸钥要求书（root 拍U「提出详细铸钥要求/全权授权制备」）
> qlv 20260913T2013Z 铸. 铁律在首: 钥值永不入任何文本(仓/链/帖/回执/快照), 唯入 qlv-pub Secrets 与 root vault.
## 一、钥规格
| 项 | 要求 | 理据 |
|---|---|---|
| 持有账号 | **chepin-qi**(qlv-pub 所在账号控制台铸) | PAT 权限≤账号自身权限; AI_FULL_PAT(chepin-ai 账号) 对 chepin-qi 仓 ACL pull-only(L1 直测 20260913T2013Z: push=false admin=false), GitHub 权限模型常态, 不可顶替 |
| 钥型 | **fine-grained PAT**(拒 classic) | 仓库级最小面+权限粒度, NAME-HYGIENE(beat-97)后例 |
| 钥名 | **QLV-TOWER-PAT-01** | 名载线+用途+序(轮换便利) |
| 仓库面 | **仅 chepin-qi/qlv-pub** 一仓 | 最小面; qi-lab 私仓不涉(对现钥404=无读权, 复明候补链另案) |
| 权限 | **Contents: RW · Actions: RW · Workflows: RW · Metadata: R** | Contents+Workflows=workflow 文件自演进(三件套自装); Actions=runs 察/消; 他皆不授 |
| 禁授 | Administration/Secrets:write/Webhooks/Environments/Pages/Members/Issues:write/PR:write | 最小化; 塔落账全走 contents, 不需 issues/PR 写 |
| 期限 | **90 天**(与 AI-FullScope 轮换同拍) | 断钥演练 0926 在册=轮换彩排 |
## 二、装址与引用
- 装: qlv-pub → Settings → Secrets and variables → Actions → 名 **TOWER_PAT**(值仅入此+root vault)
- 用: watchtower.yml 跨仓巡面仍用现有 FED_PAT(HUB-RULING-QLV-KEY-01 在役); **TOWER_PAT 专职=workflow/contents 自写道**——三件套装后即: 塔自演进不再假手他线, 钥道老大难终局
- 我(API contents PUT + TOWER_PAT)即可自装: TOWER-FIX-QLV-03-SELFPACK 即装包已铸待命(见下)
## 三、钥健康与应急(已在役/入包)
- KEY-PROBE 段: 塔每 run 探钥(401/403→落 receipts/tower/KEYPROBE-*)——23:41Z 实证在案(SI2 会话歇自转铁证)
- KEY-DARK 应急SOP(已立践): 降级面vci-qlv主写+待发槽制+义眼残镜不停车+更正通稿器课(株十四: 通稿未读先判亡=自判暗)
- 钥失/泄: 即销+轮换+全院通稿(钥值永不贴公面, E804)
## 四、验收判据(钥到即验, L1)
①GET /repos/chepin-qi/qlv-pub permissions.push=true ②contents PUT workflow 文件 201 ③dispatches 204 ④三件套装后首 run: 落账先行双行+pulse.jsonl 首行存档
## 五、即装包(钥到即装, 已铸待命)
TOWER-FIX-QLV-03-SELFPACK 全 yml: lanes/qlv/outbox-pending/TOWER-FIX-QLV-03-SELFPACK.yml ——落账先行(拍始/拍终双行try/finally)+探面timeout25→8s tries1+NUDGE批帽≤4/run+段轮转(--seg游标)+LANE-SWEEP-01(差集三分类批帽≤8)+DEBT-ENGINE-01(每run取1债自驱)+KEY-PROBE段
——qlv 20260913T2013Z 锚:@cisvr@qfa #noauto