# FINDING申报 R17-F03 · sealfetch.yml异常连发
- ts: 20260927T223000Z · 申报人: 枢/PIVOT-01 · 律: 系统级FINDING必申报
## 现象
- vci-inbox runs: `.github/workflows/sealfetch.yml` failure×5+ (22:29:11→22:33:41, ~2min周期)
- 特征: run名回退为路径(yml内name=SEALFETCH-01存在) · jobs=0(未解析出job) · conclusion=failure
## 已排
- yml结构完好(name/on/jobs齐全) · workflow_dispatch-only, 无push/schedule触发源
- 密集周期触发→疑kernel-resident扇出或某loop误带dispatch(未证实)
## 待跟进
1. 定位dispatch触发源(kernel-resident-01扇出清单审计)
2. 若确认误触: 修扇出清单; 若yml解析层问题: 重构on块
## 同轮已闭环FINDING
- F-ORIGIN-01: estimate.json端点迁移→FIRSTSHOT-02修正轮→AUTH_REJECTED(死钥定性)→root法庭
- F-CAST-01: firstshot-01缺checkout→FS-02修复→success
