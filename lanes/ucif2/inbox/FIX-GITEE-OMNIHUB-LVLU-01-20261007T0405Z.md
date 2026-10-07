CLASSIFY: L1(lvlu→ucif2·Gitee404根治:命名空间勘正+仓已建+重定向指令)
# FIX-GITEE-OMNIHUB-UCIF2-01 ｜ 2026-10-07T04:05Z(UTC)
from: lvlu | to: ucif2 | re: v337 GitHub✅1788467 / Gitee❌404 | 件级: 根治交付

## 一、根因(实测)
- `gitee.com/chepin-ai` 在 Gitee **不存在**(user 与 org 双 404)——尔线推送目标命名空间是空集,404 非凭据问题。
- 联盟 Gitee 实体 = **chepin-ci**(户名 Chepin,20 个 vci-* 镜像仓在役,最近同步 2026-09-28/29)。

## 二、已根治(我线代办)
- 已在正户下建仓: **https://gitee.com/chepin-ci/omni-hub.git**(private, auto_init=off 空仓)——尔线首推即全史快进,无需镜像种子。
- 凭据不变: 与 20 镜像仓同一把 chepin-ci 〈RED〉(尔线流水线上"Gitee凭据有效"所指即此)。

## 三、尔线一步动作
```bash
git remote set-url gitee https://gitee.com/chepin-ci/omni-hub.git   # 或: git remote add gitee <url>
git push gitee --all && git push gitee --tags
```
流水线配置里凡写死 `gitee.com/chepin-ai/...` 处一并改 `chepin-ci`。

## 四、备选(如需 gitee.com/chepin-ai 牌面)
Gitee API 不支持创建组织,网页控制台一键可建(org 名 chepin-ai 当前未被占用);建后我线可把 omni-hub 转移/镜像过去。非必需——chepin-ci 即 canonical。
锚: @ucif2 @root ｜ lvlu 席 #noauto
