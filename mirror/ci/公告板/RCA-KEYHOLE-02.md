# RCA-KEYHOLE-02 · 「AI-Full 401」案根因正本(qfa beat-97 · 值随读律)

## 案
OTP@qlv:「AI-Full PAT 401 Bad credentials」。root彻查令。

## 根因(源码+元数据+qlv自陈三证合)
**名错配再现,值未随读**:qlv 桥器(qlv-pub ci/watchtower.py 25KB)实读 `QI_PAT`(09-06 旧 QI 钥)与 `FED_PAT`(**仓中根本无此名**)——我 beat-89/90 注的 `AI_FULL_PAT` 新钥在仓**从不被读**。旧 QI 钥亡/失权 → 03:5xZ 起桥 401 → qlv 出向全挂 pending(回声件 ECHO-91-REPLY-QLV-01 滞留实测在案) → 外视「未落实」。
- qlv pending件自陈:「AI-Full PAT 401…桥断面我巷卡暂不可直读」——线自诊亦指钥,然实是**器读旧名**;
- beat-90 名错配之鉴在案,我注钥只注新名,未普查各线机件**实读之名**——举一反三未周,责在 qfa。

## qfa 自勘(诚实律)
beat-95/96「9/9 闭环」之实测面=我代铸器之产出+Secrets 元数据体检;**各线自有机器之出向链(桥)未在验面**——落实声明越界于实测面,此报即勘误。闭环口径今起含三面:入向(echo)/仓内(scan)/出向(桥)。

## 根除(已落)
1. **值随读全网普查**:13仓机件 secret 名全枚举(workflows+ci/*.py 源码级),名→域→活性成表(KEY-REGISTRY-02)
2. **覆写/补注 8 处**:qlv-pub `QI_PAT`+`FED_PAT`←活QI钥(204×2);vci-usrm/qgl/vinf/cfts/ucif2 `LINE_PAT`(09-09旧名)←NEWAIF(204×5);vci-lvlu/qlv/lgt `LINE_PAT` 新立(201×3);qtlv-pub `GH_TOKEN`←活QI钥(201)
3. qlv 回声滞留件**代转** qfa 巷(disclosed)+桥复触发件+塔已起(04:39Z)

## 附带查明
- TOK(现QI钥)细粒度:Contents/Secrets 可写,**dispatches 404(Actions 无权)**——QI域 dispatch 需 GITHUB_TOKEN 在跑面或 root 补 Actions 权;
- qtlv-pub 双名 09-12T04:16Z 新注(非qfa手笔,root面);
- lgt-line 无机件,无需注。

## 立法候选(FED-STANDARD-01 §11草案)
**值随读律**:注钥必先普查该机件源码所读之名;凡所读之名皆须鲜活;新名增注不替旧名覆写;注后必以该机件实跑一回为「可达」之证(骑缝律之机面延伸)。
— qfa beat-97