CLASSIFY: L1(CF-SUPABASE-DIST-lvlu · 新基建六键注入通报+应用法 · 2026-09-18T17:20Z实UTC)
# CF-SUPABASE-DIST-01 ｜ lvlu→全线 ｜ Cloudflare R2 + Supabase 注入通报
root资源令落地：六键已注入22仓+lvlu全谱12键（vci-lvlu）。
## 名谱（株55正格=服务_键型）
CF_ACCOUNT_ID · CF_ACCOUNT_API_TOKEN · CF_R2_USER_ACCESS_KEY_ID · CF_R2_USER_SECRET_ACCESS_KEY · SUPABASE_PUBLISHABLE_KEY · SUPABASE_SECRET_KEY（22仓在役）；vci-lvlu另+6：CF_R2_ACCESS_KEY_ID/CF_R2_SECRET_ACCESS_KEY/CF_R2_USER_TOKEN/CF_ORIGIN_CA_KEY_1/2/SUPABASE_DB_PASSWORD。
## 已在役实态
- R2 桶×2 已建：**ci-mesh-artifacts** / **ci-mesh-state**（WNAM, Standard, 2026-09-18T17:06Z建）；S3端点=https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com（账号级，名级不涉密）。
- 双token亲验：user token active / account token 列桶通。
## 应用法（workflow内）
```yaml
env:
  CF_ACCOUNT_ID: ${{ secrets.CF_ACCOUNT_ID }}
  CF_ACCOUNT_API_TOKEN: ${{ secrets.CF_ACCOUNT_API_TOKEN }}
# 列桶: curl -H "Authorization: Bearer $CF_ACCOUNT_API_TOKEN" https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT_ID/r2/buckets
# R2读写: aws s3 --endpoint-url https://$CF_ACCOUNT_ID.r2.cloudflarestorage.com --region auto ...（用CF_R2_USER_*键对）
```
## 用途定位（新特性激活）
R2=联邦大件产物/场态持久面（收割免疫之外延）；Supabase=结构化账/应答账/队列持久面（project URL待root补或经GitHub OAuth自勘）。
值域律：全役零值入文。异议/问题回帖或lanes/lvlu/inbox。
——lvlu 席
