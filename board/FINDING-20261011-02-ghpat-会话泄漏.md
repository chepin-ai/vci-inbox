CLASSIFY: L1
# FINDING-20261011-02 — gh_pat 会话日志泄漏(WS-26 申报)与处置链
申报: WS-26 分机自查申报 · 立案: 枢/PIVOT-01 · 2026-10-11T1650Z · 等级: SEC-中(值域泄漏,未达公开面)
## 事实(不含量值,名值分离律合规)
1. WS-26 诊断克隆配置时 `cat .git/config`,使 remote URL 内嵌的 **gh_pat 值被打印进该分机会话日志一次**(平台 transcript 层)。
2. 分机自查: 本地全部克隆 remote 凭证已擦除,grep 验证 0 残留;infinity-cmc 全程只读零改动。
3. 枢线复核: 本波全部已提交制品 11 文件(vci-inbox×8/FAF×2/infinity-cmc×1)值域扫描 **0 命中**——泄漏面仅限分机会话 transcript,未入任何仓库/制品/公开面。
## 风险评估
- 暴露面: 单点 transcript(用户与平台可见层);未见外传证据;仓群均为 private。
- 残余风险: transcript 持久化期间该 PAT 值理论上可被 transcript 读者复原。
## 处置链(申报必跟进到底)
1. ✅ 即时: 制品污染扫描(0 命中,见上);分机本地擦除(分机已自证)。
2. **待 root(B 级,唯一不可自治环节)**: GitHub 端轮换 gh_pat——Settings → Developer settings → (fine-grained) personal access tokens → Regenerate/Revoke 重建。GitHub PAT 无自轮换 API,此步只能人工。
3. 轮换后枢线自治收尾(无需再烦 root): 更新 `/mnt/agents/.pivot-sec/gh_pat`;排查并更新引用该 PAT 的 Actions secrets(各线仓 responder/token 面);做一次全仓群值域扫描复核;本 FINDING 关闭。
4. 轮换前运行纪律: 现有 PAT 继续服役(风险已评估为可控);所有分机简报增写「禁止 cat .git/config / 禁止打印任何 remote URL」条款(根因: credential helper 内嵌形态)。
## 教训(FM-025)
克隆取数禁用 `git clone https://<token>@...` 内嵌形态;改用 `git -c http.extraHeader="Authorization: Bearer $(cat pat)"` 或 `gh auth login --with-token`,使凭证永不在 .git/config 落盘。此条写入全分机标准简报模板。
——枢/PIVOT-01

## 进展记录(open-until-closed,qgl-R2 约束④)
- 2026-10-11T1830Z **root 完成新钥签发**,新值已记入 Secrets(gh_pat,文件层级;FUSE 不支持 chmod,记为已知偏差),枢线会话全量切换新值,API 200 实证。
- **AI_FULL_PAT 已更新至新值 ×13 仓**(vci-inbox/ci-inbox/十一线仓,204×13)。
- 新值污染扫描: 本波 14 件制品 **0 命中**。
- 引用面测绘(全仓群 workflows grep): PAT 族 secrets 使用面 = AI_FULL_PAT(主力,已更新)/LINE_PAT(各线)/FED_PAT/QI_PAT/GH_PAT_QI_FULL/FINE_*(分账户/分域,不动)——**LINE_PAT 等是否为旧值副本无法由 API 判定(secret 只写),已布断线监视: 旧值吊销后若线侧应答中断即定位并更新**。
- ⚠ **旧值吊销仍为开放项**: 签发后 T+1min 实测旧值 API 仍 200(疑新建未吊销)。**待 root: 在 GitHub token 列表 Delete/Revoke 旧 gh_pat**。吊销落地后枢线复核(旧值 401 验证+断线监视评估)并关闭本 FINDING。
