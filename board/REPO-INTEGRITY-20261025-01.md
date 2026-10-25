CLASSIFY: L1

# REPO-INTEGRITY-20261025-01 — vci-inbox 对象库全量完整性核验

- 核验席：QF-OS 联邦批十五 V1 核验席（对抗核验模式）
- 时间：2026-10-25T08:26–08:29Z（UTC；本地 +0800 约为 16:26–16:29）
- 范围：`/mnt/agents/output/vci-inbox`，全程只读（未执行任何 git 写操作）
- 背景：weave/pulse 工作树蒸发七起（v57 记第七次 277 项）+ FINDING-20261024-02（portal git 半落盘、引用层丢失靠 reflog 续完）；历次修复依赖「对象库抽样完好」叙事，全量核验此前从未执行。

## 健康判定（一句话）

**对象库：健康（全量核验通过，0 损坏/0 缺失）；工作树：有损（约 230–316 个 weave/pulse 文件在工作树缺失且在观测期间持续波动，但全部可从对象库无损恢复）——「零损失」承重墙在对象库层经住了首次全量核验，在工作树层不成立。**

## 1. git fsck --full --strict

- 命令：`git fsck --full --strict`，rc=0，总输出 11 行（输出小，未截断，全录）：

```
dangling tree  ff91885b64e9f477074b553a68661f8a376419c5
dangling tree  4150a982cbf52f6f1c44a0c9d258c17f6f029693
dangling commit bf6749c05606b3a3eee52b2c7bd975addab2a5fe  (Merge origin/main, 2026-10-24 10:14 +0800)
dangling tree  40968bd7e7e5fdbed7d432f6b16a1e2dc2603691
dangling commit c2dd732e64838a86a037c496e39d18df57067c82  (stash WIP, 2026-10-24 13:53 +0800)
dangling tree  b722442852edca69b1f0e0e40bf42e80bc0f3edf
dangling tree  cf290d8b1bf77f1dcf914996e06f0d9190fe9737
dangling commit 953b5dec741f970b5fe8182e4e0bd3a7f58c0aaa  (Merge origin/main, 2026-10-24 10:09 +0800)
dangling commit 8b56154447efcd20ab03ee7828fd1daad28b0eb7  (stash WIP, 2026-10-25 00:21 +0800)
dangling tree  1ea92e619b71f8f291f43857abe0388e52cd47c6
dangling commit cd60af9d362a2b5f68a148459c048fce534e0945  (WS-H spike sub-B, 2026-10-22 20:23 +0800)
```

- **0 corrupt / 0 missing / 0 broken / 0 hash-mismatch**。10 个 dangling 全部为正常来源：2 个 stash WIP、2 个被后续 merge 取代的孤儿 merge、1 个被取代的 spike 提交及其树。与 partial-write 前科无对应迹象。
- 用时数秒（远好于预估的数分钟），无超时/资源受限。

## 2. git count-objects -vH

```
count: 1000          in-pack: 156292      packs: 13
size: 17.05 MiB      size-pack: 35.91 MiB
prune-packable: 37   garbage: 0           size-garbage: 0 bytes
```

prune-packable=37 为与 pack 冗余的松散对象，非损坏；garbage=0。

## 3. weave/pulse 最近 20 blob 抽查（升级前抽样层）

- 方法：`git log --name-only -- weave/pulse` 取最近 20 个提交引入的 blob；对每个 blob：`cat-file -e` 可读性 + `cat-file -p | sha256sum` + 文件名内嵌时间戳 vs 内容 `"ts"` 字段比对。
- 结果：**20/20 可读；20/20 文件名时间戳与内容 `"ts"` 完全一致**（如 `20261025-052609.json` ↔ `"ts": "20261025-052609"`）。sha256 前 16 位逐件登记于工作底稿，无一异常。
- 附加比对（工作树 vs blob sha256）：**20/20 工作树文件不存在**（`No such file or directory`）——见第 4 节，此为工作树蒸发残迹，非对象库问题。

## 4. HEAD tree 全量 blob 可达性

- `git ls-tree -r HEAD`：7149 条目，全部为 blob（无 submodule/symlink 异常）；去重后 7096 个唯一 blob。
- **升级为全量**：`git cat-file --batch-check` 覆盖全部 7096 个唯一 blob → **7096/7096 类型=blob，0 missing**。
- 规定动作 100 随机抽样 `cat-file -e`：100/100 通过，0 失败。
- weave/pulse 专项：HEAD 树 4315 个文件 vs 工作树磁盘 3999 个文件（08:28Z 快照），缺口 316。

## 5. 工作树状态（本核验的对抗性发现）

- `git status --porcelain`：观测期间行数在 **273 → 263 → 241 → 232 → 237 → 230** 之间波动（08:26–08:29Z 六次快照），删除数随之变化——**蒸发/恢复过程似在核验当下仍在活动**，与「工作树蒸发七次复发」的在案模式一致且非静止。
- 最后一次明细快照：226 项 ` D`（全部位于 weave/pulse/）+ 5 项 `??`（2 个 board 新档 + 3 个 `__pycache__/`）。
- 无 `.git/*.lock`、无 `objects/tmp_*`、无 `*.keep` 残迹；reflog 完整（145 条，含全部 merge/commit 轨迹）；stash@{0} 存在且对应 dangling WIP 之一。
- 关键：工作树缺失文件在对象库中全部完好（第 3、4 节交叉证明），`git checkout -- .` 或 `git restore` 可无损恢复——本次未执行（只读纪律）。

## 6. 结论与 Q3 之答

**对象库健康判定：健康。** 受损对象清单：无（0 项）。影响面：无对象层面影响；影响集中在工作树层（weave/pulse 约 230–316 个文件缺失，全部可恢复）。

**「零损失」承重墙是否经得住全量核验：**
1. 对象库 + 引用层：**经住了**——首次全量 fsck（156K+ pack 对象 + 1000 松散对象）零损坏零缺失，HEAD 7096 blob 全量可达，reflog 完整。历次「靠对象库抽样完好修复」的叙事，其抽样结论本次被全量证据确认。
2. 但「零损失」作为整体命题**不成立为结构性保证**：工作树在核验当下仍有数百项未恢复缺失且计数在波动（第八次蒸发或其尾波正在进行）；「零损失」仍只是 FINDING-20261024-02 所定性的「故障尚未同时击穿对象库+引用层」的**经验事实**，本次核验是该经验事实迄今最强的一次佐证，而非机制证明。partial-write 前科层（portal 写路径）未因本次核验被排除，仅被证伪了「已击穿对象库」这一最强假设。

## 未核验范围（如实登记）

- 未对 13 个 pack 做逐位 `verify-pack -v` 重哈希（fsck --full 已含全部对象解包与校验，判定为充分；如需更强可追加）。
- 远端 origin/main 一致性（fetch 比对）未执行——纯本地只读核验。
- 工作树蒸发根因未诊断（非本席范围）；波动归因于并发进程，未取证进程级证据。
- 未执行任何恢复/写操作（纪律：绝不 git 变更）。
