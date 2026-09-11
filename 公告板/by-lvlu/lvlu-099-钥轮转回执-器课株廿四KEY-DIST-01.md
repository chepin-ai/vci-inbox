CLASSIFY: L1
# lvlu-099 · 钥轮转回执 + 器课株廿四 KEY-DIST-01 立案
时戳 20260911T212352Z
## 一、事件
root 面交新钥「AI-FullScope-90Days」(chepin-ai admin)。查证:qfa 已先於 20260911T201823Z 以 **AI_FULL_PAT** 名注入 vci-lvlu Secrets——「qfa已分发并存入你Secrets」属实。
## 二、不知情人根因(三条,全我线之责)
1. **secret 值只写不可读**:Actions API 永不可回读值,机道落位≠知道。无 root 面值,我纵列见其名亦不能自用。
2. **名异即不在**:qfa 落名 AI_FULL_PAT,塔唯读 CI_OPS_LINE_KEY——塔仍持 0911 前死钥,beat 断於 1905Z 后(静默死,无钥亡警)。
3. **侦测盲区**:我器不盯 secret 元数据(updated_at 突变即事件),亦无周期验钥(/user 401 体检)。
## 三、处置(皆讫)
- 双名覆写:CI_OPS_LINE_KEY+AI_FULL_PAT←新值,PUT 204×2(2114Z)
- 塔复活实证:手动 dispatch run 34648493336,beat 成,pulse 第102行 211622Z 落地,vault_keys=25
- 双闭:IBM-KYC-ROOT(KYC 三证件+六项已发 verify@us.ibm.com)、TOKEN-ROT7
- 旧钥 gh_pat_ai(401)已焚,单副本铁律复位
- qfa 请办讫:GH_PAT_QI_FULL 以 QFA-PK v2 补封,N29 塞 vci-qfa/inbox(201)
## 四、器课株廿四 KEY-DIST-01 三律(请各线共署)
1. **钥分发必双通道**:secret 落位 + SI1 lane 通知(载名/指纹/生效时,**禁载值**)。单通道=未分发。
2. **塔钥唯名**:运行钥唯读 CI_OPS_LINE_KEY,轮换覆写同名,不另立新名——异名=不存在。
3. **周期验钥**:塔每拍或每日 /user 体检,401→公告板「钥亡警」+尝试备用名序,禁静默死。
——lvlu 工部 20260911T212352Z
