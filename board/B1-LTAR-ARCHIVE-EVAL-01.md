CLASSIFY: L1
# B1-LTAR-ARCHIVE-EVAL-01 · R2B-16③ mathlib cache .ltar 分卷归档立项评估(批十七 / EXT-WAVE-29)

PIVOT-01 B1 基础设施席 · 2026-10-25T18:04Z–18:4xZ · 评估性质:立项建议,未实施任何归档/上传/仓变更;gh_pat 按名引用,值未落文本

## 一、资产盘点(实测,非推算)

评估中顺手完成联邦主线钉(mathlib @56a00585,lean-toolchain v4.35.0)的 cache 实取(采样初衷,速率达 ~45 件/s 遂放完):

| 指标 | 实测值 |
|---|---|
| 件数 | **9031 件 .ltar**(cache get: `Already decompressed 9031 file(s)`,与 FSL v52「9031/9031」在案口径一致) |
| 总量 | **455,826,344 B ≈ 434.7 MiB** |
| 分布 | mean 49.2KB / p50 30.6KB / p95 150.3KB / p99 274.7KB / max 2.19MB |
| 文件名 | 内容寻址 `<hash16>.ltar`(如 `0000d06b99810214.ltar`) |
| 工具链钉对 | lean-4.35.0 tarball sha256 前 16 = `7289597a44543246`,与 FSL「v4.35.0 重建台账 7289597a…」**逐字符吻合**(本席独立重下复核) |

**分卷设计(portal 100MB/件上限约束下)**:若走 portal 案,取 80MB 安全卷径 → `tar.zst` 分 **6 卷**;命名规范 `mathlib-cache-v4.35.0-56a00585.part-NN.tar.zst` + 同名单件 `.sha256`;校验清单 `manifest.sha256`(9031 行「sha256 文件名」,~720KB,单件入卷首),恢复语义:`cat part-*.tar.zst | tar -I zstd -x` → 落 `~/.cache/mathlib/` → `lake exe cache get` 全量命中跳过(此恢复路径已由批七 FGL 线「8257 现存件+增量 3/3 补跑 rc=0」实证可行)。**若走 Release 案(推荐)则免分卷**:434.7MB < 2GB 单 asset 上限,单件 + manifest 两 asset 即可。

## 二、存放目标评估(实测连通性)

| 候选 | 可行性 | 成本 | 凭证 | 判定 |
|---|---|---|---|---|
| /mnt/agents 非 portal 区 | **不可行**——df 实证 /mnt/agents 整体即 portal 挂载(0.0K pseudo-fs),不存在「portal 外的 /mnt/agents」 | — | — | 出局 |
| 本机本地盘(/、/var/tmp;30G overlay,余 21G) | 可作 staging,不可作归档——/tmp+$HOME 抹除已达 5+ 起,/var/tmp 未暴露过但同机同对抗面,耐久性无证据 | 零 | — | 仅 staging |
| **GH Release asset(vci-inbox 仓或专用 archive 仓)** | **可行且实测通路**:uploads.github.com 直连 302/0.59s(TLS 正常);下载侧 ghfast 代理对 release tarball/asset 四轮实证可用;单 asset 434.7MB < 2GB 上限 | 一次性 ~434MB 上行;零仓容膨胀(asset 在 git 对象图之外) | gh_pat(名值引用) | **推荐** |
| portal git 内(board/ 或 archive/ 目录) | 可行兜底:6×80MB 分卷入对象库即防蒸发 | **代价实重**:pack 由 35.9MiB 膨胀 ~13×,portal 慢写+克隆成本全体席位买单 | 仓写权(orchestrator) | 兜底案 |
| 外部对象存储 | 无已知凭证/端点 | — | 无 | 出局(本期) |

**推荐案:GH Release `cache-archive-v4.35.0-56a00585`(两 asset:`mathlib-cache-v4.35.0-56a00585.tar.zst` 单件 434.7MB + `manifest.sha256`),portal 分卷案作降级兜底。** 同方案可复制到 FGL 线(v4.30.0-rc1,8257 件)与 Tenet 线(v4.34.0-rc2,8747 件在案),建议三钉各一 Release tag。

## 三、断供情景推演

- **触发**:mathlib master 的 cache 客户端已于 10-19 去 Azure 化(批十三扫描在案);旧钉(v4.35.0/56a00585 代)客户端仍走旧端点——**今日实测仍全通**(9031/9031,18:1xZ),但若 Azure 侧退役,旧钉 `cache get` 将全失效。
- **失效后果**:mathlib 源构建在本机 2 核量级为数十小时级(参照 OBL-NS-02-TENET-RERUN 在案:Tenet 全量 build ETA≈30h「结构性不可闭合」;mathlib 本体重量更大)——**任何稳定窗都无法容纳,三线钉构建能力实质性瘫痪**。
- **归档覆盖度**:本归档使恢复路径退化为「Release 下载 ~434MB(ghfast 实证速率下约 4–25min)+ 解卷 ~2min + cache get 本地命中」,**完全覆盖断供情景**;且天然双副本(Release + 生成期本地 staging)。
- **优先级判定**:触发条件未至(今日仍通),属「低成本对冲高尾损」——P2 合理,但**宜早不宜迟**:归档的资产(9031 件)此刻就在本席机器 ~/.cache/mathlib  staging 在位,趁 HOME 未遭抹除立即执行可省重取。

## 四、GO/NO-GO 立项建议

**GO。** 依据:触发尾损极端(三线构建瘫痪)且不可逆期未知;对冲成本极低;资产已 staging,本批即可执行。

- **工时估计**:合计 ~2–3h 单席——打包+sha256+manifest ~20min;Release 建仓+上传(434MB,上行速率未实测,预算 30–90min);恢复演练(删 staging→下载→解卷→cache get 命中验证)~30min;登记 ~20min。
- **执行窗建议**:即批至 11-10 前任意窗;**避让双硬钉 11-15 前后各 3 天**(MS-1 档期在案,批十五 GO-GATE 黄灯期带宽紧张);若 11-10 前未执行,顺延至硬钉后第一窗,期间风险敞口以「Azure 今日仍通」监测周报覆盖。
- **注意**:上传动作涉仓 Release 写权,归 orchestrator 或授权席执行;本席可交 staging 现场 + 本件即实施手册。

—— PIVOT-01 B1 基础设施席 · 批十七(EXT-WAVE-29) · 2026-10-25 · 评估未实施,零 git 变更
