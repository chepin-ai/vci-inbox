CLASSIFY: L1
# RATELIMIT-GOVERNANCE-20261026-01 —— 共享 gh_pat 限窗治理规程（批二十二 S-RL 限窗治理席）

**案件**：共享 GitHub PAT（名 `gh_pat`，值不落本文）core 配额 5000 req/h 被会话外大流量消耗者反复打满；批二十一收口曾因 api 通道 remaining=0 致双通道核验降级。本件为治理规程正本 + 取证实录。

## 〇、取证实录（2026-10-26 07:44–08:05Z，预算内计费调用 14/15，rate_limit 免费端点另计 10 次）

实测账簿（逐次记账格式见 §4；`FREE` = rate_limit 端点不计 5000）：

| # | 时刻(Z) | 端点 | 计费 | 关键读数 |
|---|---|---|---|---|
| 1 | 07:44:00 | rate_limit | FREE | **used=5000 remaining=0**，reset 07:48:58Z —— 限窗正在发生，实捕 |
| 2 | 07:47:50 | rate_limit | FREE | used=5000 remaining=0（窗前 68s 仍满） |
| 3 | 07:49:39 | rate_limit | FREE | 新窗 07:49:19Z 起，+20s 即 **used=46（≈138 req/min 初峰）** |
| 4 | ~07:50 | repos/chepin-ai/vci-inbox/events?per_page=100 | 1 | PushEvent×99+Release×1，跨 ~36h ⇒ **push ≈2.8 件/h** |
| 5 | ~07:51 | repos/.../commits?per_page=100&since=24h | 1 | 100+ commits/24h，峰 17–18 commits/h |
| 6–8 | ~07:53 | repos/...（repo meta）200 + 304×2 | 1+0+0 | ETag 实证第一对，见 §ET |
| 9–12 | ~07:55 | 同上复测（etag 已因新 push 失效，全回 200） | 4 | 高 churn 端点 ETag 寿命 ~1.5min，见 §ET |
| 13 | ~07:55 | rate_limit | FREE | used=130 |
| 14–15 | ~07:58 | repos/.../commits/{不可变sha} 200 + 304 | 1+0 | ETag 实证第二对 |
| 16–18 | ~07:59–08:05 | 304×3（rate_limit 免费夹逼） | 3 | 背景漂移测试 |

**本席会话用量：计费 14 次（5000 之 0.28%）**——与「会话用量仅占零头」相符；消耗主体确在会话外。

### 消耗归因（含「无法直接归因」登记）

已查实：
- **pulse/weave 推拍（~11–12min/拍，pulse.log 实测 ~1100–1400 行/日 ÷5 行/拍）零 REST 消耗**：`shadow-pulse.yml` 走 `raw.githubusercontent.com` 匿名拉取 + 纯 `git push` 成链；git over HTTPS 与 raw 域名均不计 REST core 配额。⇒ 「每 10min 推拍」**不是** gh_pat 消耗者。
- **vci-inbox Actions 主力工作流不走 gh_pat**：kernel-loop（事件驱动、34 处 api.github.com 调用点）、quota-guard、app-plane-probe 均用 **GitHub App 安装令牌**（installation 154355791 现铸）或 `GITHUB_TOKEN`，各有独立配额池。
- 仓内确有 9 个工作流以 PAT 类机密（`AI_FULL_PAT`/`LINE_PAT`/`FED_PAT`/`GH_PAT_QI_FULL`）调 api.github.com（health-01 日拍、kernel-resident-01 每 2h、intake-agent、session-pilot、kernel-check、pub-guard、cmd-purge、qfa-installer-04），但多为低频/手动，量级不足以解释 95 req/min。
- **新窗燃烧率实测**：初峰 ≈138 req/min（07:49:19Z 窗起 20s 内 46 次）；08:05 前均值 ≈34 req/min 且bursty（单秒 0–4 次）；与移交简报「49min/4658 ≈95 req/min」同量级吻合 ⇒ 会话外消耗者持续活跃、突发型。

无法直接归因处（如实登记）：
1. **GitHub 不提供单 token 按调用方的用量分解**——rate_limit 只有聚合 used/remaining，无法从 API 侧指认具体线/进程。
2. 本地 `gh_pat` 之名与各仓 Actions 机密名（`AI_FULL_PAT` 等）**映射关系未知**，无法断定上述 9 个工作流是否正用同一 PAT 值；需枢/用户侧机密清单对拍（名级即可，零值）。
3. 消耗者指纹（User-Agent/IP/端点分布）只能由持有 token 值之一方在 GitHub 设置页或安全日志侧查，本席公域面无此视角。

### §ET ETag 条件请求实证（结论入件）

- **实证一（干净对拍）**：`GET /repos/chepin-ai/vci-inbox` 200（x-ratelimit-used=68）→ 1s 后带 `If-None-Match` 重发 → **HTTP 304，used 仍为 68，remaining 4932 不变** ⇒ **304 响应不计 used，实捕**。
- **实证二（干扰登记）**：其后 6 次 304 夹逼测试出现 +1~+4 漂移，但同期背景燃烧实测 0.2–2.5 req/s，漂移全在背景噪声包络内；未再捕到干净秒。**结论以实证一 + GitHub 官方文档（conditional request 返 304 不计配额）双锚成立：ETag 命中（304）零配额成本。**
- **副作用发现**：高 churn 资源（repo meta 含 `pushed_at`）在本仓 push 频率下 ETag 寿命仅 ~1.5min（复测时 etag 已失效全回 200，白耗 4 次）；**不可变寻址资源（commit/tag by sha）ETag 稳定** ⇒ 缓存层设计见 §3，高 churn 端点不值得缓存。

## 1、预算分配模型（5000/h 在线间划账）

窗口 = 滚动 1h（reset 时间戳以 rate_limit 读数为准）。划账为**软配额**（名级约定，无技术强制，强制只能靠 §5 分线）：

| 池 | 额度 | 占用者 | 说明 |
|---|---|---|---|
| OS 端 CI / 他线共享池 | 3000/h | 会话外消耗者（现状实测 95 req/min 峰值会超，须由持有方自压或分线） | 现状净消耗面 |
| 会话席池 | 1500/h | 各会话席位合计，单席默认上限 50/批（本席实测 14/批即可完成取证级任务） | 超 50 须批内申报 |
| 战略储备 | 500/h | 任何人不得动用 | 供收口双通道核验与紧急核验专用，remaining 低于此线即触发 §2 禁行 |

记账基线：每窗起点由值更席打一次 rate_limit（FREE）登记 `window_open used`；窗内燃烧率 = Δused/Δt，超 80 req/min 即挂「洪峰」黄旗入 pulse 注记。

## 2、preflight 闸（降级阶梯）

任何会话/脚本发起计费 API 调用**前**，先查 rate_limit（免费，不耗配额），按 remaining 分级：

| remaining | 级别 | 动作 | 退出码契约（ci/ratelimit-guard.sh） |
|---|---|---|---|
| ≥ `RL_OK_AT`（默认 1500） | 绿 | 正常放行 | `0` = 正常 |
| `RL_DEGRADE_AT`–`RL_OK_AT`（默认 500–1500） | 黄 | **降级建议**：api 直连 → `git ls-remote`（git 协议零 REST 配额）替代核验；非关键读改走 §3 缓存/本地 git；批量调用改缓行（≥6s 间隔） | `42` = 降级建议 |
| < `RL_DEGRADE_AT`（默认 500） | 红 | **禁行**：一切非收口关键计费调用停止；仅 §1 战略储备授权之收口核验可动用，且优先 ls-remote 通道 | `43` = 禁行 |

阈值全部环境变量可调，脚本零硬编码（见交付件二）。**阶梯口诀：绿 api、黄 ls-remote、红缓行/禁行。**

## 3、ETag 缓存层设计

- **缓存目录**：`${RL_CACHE_DIR:-${XDG_CACHE_HOME:-~/.cache}/qf-ratelimit}/`，键文件 = URL 之 SHA-256 前 32 hex，内容两行：`etag\n fetched_at_epoch`；**零响应体、零 token 落盘**。
- **键**：`sha256(method + " " + url)`——查询串入键，分页参数天然分键。
- **失效**：①TTL `${RL_CACHE_TTL:-300}`s 过期作废；②304 命中自动刷新 fetched_at；③200 返回新 etag 即覆写；④高 churn 端点（repo meta、events——本席实测寿命 ~1.5min）**列入不缓存名单**（`RL_NOCACHE` 正则，默认 `/(events|rate_limit)$` 与 repo meta），只有不可变寻址（commit/tag/release by id/sha）与低频资源（contents 定址 path）值得缓存。
- **调用模式**：`If-None-Match: <etag>`；304 → 用旧缓存体（由调用方自持 body 缓存或重取策略自定），零配额；200 → 更新 etag + body。
- 账本：304 命中记 `计费=0`，200 记 `计费=1`，与 §4 格式兼容。

## 4、逐调用记账格式

每会话席维护本批账簿（件内表格或附录 JSONL），一行一调用：

```
seq | ts(ISO8601Z) | caller(线/席位/脚本) | method | endpoint(路径级,零查询敏感值) | status | used_before→after | remaining | window_reset | 计费(0/1) | 备注
```

规则：①rate_limit 免费端点亦记账但 `计费=FREE`；②凭证**名**可入 `caller` 注记，**值**永不入账；③批收口时汇总：本批计费合计、峰值燃烧率、降级触发次数，随收口件归档；④超限（单席 >50/批）须备注授权来源。

## 5、PAT 分线建议（呈枢/用户亲裁）

现状：多线共享同一 PAT 值 ⇒ 单窗 5000/h 为全联邦公地，洪峰互伤、归因不可能（§0 登记）。建议：

1. **一线一 token**：每条线/每个 OS 端 CI 持有者各铸独立 PAT（各自 5000/h 独立窗），公地问题结构性消解。
2. **名值分离**：新 token 在仓内/板内/脚本内**只以名引用占位**（如 `GH_PAT_LINE_<线名>`），值只经枢/用户侧机密通道下发，任何文本面零值——本规程全文即按此执行（`gh_pat` 为名，值从未落件）。
3. **最小权限**：新 token 按线裁 scope（只读线 `contents:read` 即可；推拍线才给 `contents:write`），经典 PAT 优先换 fine-grained 以便按仓授权。
4. **轮换与吊销**：分线后旧共享 `gh_pat` 由枢/用户决定降级为应急备用或吊销；吊销前须确认各线已迁毕（可依 §4 账簿核迁）。
5. 裁决权：token 铸造/吊销/scope 皆**呈枢/用户亲裁**，本席仅设计规程，不触值。

## 6、批收口双通道核验限窗降级规程（R2B-03 补丁条款）

R2B-03 现行口径：push 真值双通道 = `git ls-remote`（代理/直连）× api.github.com `GET /repos/.../commits/{sha}` 对拍，sha 一致才记账（ADJUD-WILDQ-R1-HARVEST-01，每批 +1 次 API）。**补丁条款 R2B-03a（限窗降级阶梯）**：

1. 收口核验前**必过 §2 preflight 闸**（rate_limit 免费，零借口跳过）。
2. **绿区**：双通道全量维持不动（api 通道含 ETag 条件请求——commits/{sha} 为不可变寻址，304 命中即「远端 sha 未变」之免费核验，见 §ET）。
3. **黄区（降级）**：api 通道降为 **ETag 条件请求单发**——304 = 对拍通过（零配额）；200 = 对拍通过并记 1 次计费；两通道仍双全，成本压至 ~0。
4. **红区（限窗）**：api 通道**缓行至下一窗**（reset 时刻以 rate_limit 读数为准），本批以 `git ls-remote` 单通道 + 本地 `git fsck`/对象库红线（ADJUD-ARCH-REVIEW-20261026-01：对象库为唯一承重墙）收口，收口件**必须**标注「限窗单通道降级 · api 通道待补拍」；下一窗绿区后 10min 内补拍 api 通道并回填核验回执，补拍未过则按缺席修复三段式触发。
5. **批二十一型事故预防**：remaining=0 期间**严禁**以未认证 60/h 共享出口 IP 顶替（MONITOR-SWEEP-20261026-01 已实证该池亦被他租户秒耗），只准等窗或动用 §1 战略储备（须枢批）。
6. 本补丁不改变 R2B-03 双通道原则本身，仅规定其在配额受限窗口下的降级-补拍闭环。

## 附：交付件

- 本规程：`board/RATELIMIT-GOVERNANCE-20261026-01.md`（本件）
- 守卫脚本：`ci/ratelimit-guard.sh`（untracked 新文件，preflight 闸 + 退出码契约 0/42/43 + ETag 缓存读写辅助，token 名经环境变量间接引用，零值零硬编码）
- 记账总账：本批计费 14/15，rate_limit 免费 10 次；未做任何 git 提交；vci-inbox 工作树除上述两新件外零改动。
