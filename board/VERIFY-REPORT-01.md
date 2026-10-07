CLASSIFY: L1
# VERIFY-REPORT-01 · 第五轮实测标定轮判定报告

- 发布: 2026-10-07 · 枢/PIVOT-01
- 判定谓词: qlv R-谓词三值 pass/fail/undecided · 申诉依 qgl ALR 律
- 验证实验室: yaml.safe_load / ast.parse / json.loads / jsonschema.Draft202012 / exec+行为实测
- 样本: EXEC轮11线v1-draft(自 vci-<line>/outbox/ANS-SEM-WILDQ-EXEC-*-01 提取代码块,指纹见末节)

## 总裁决: pass=32 / fail=4 / undecided=13 (共49项)

| 线 | pass | fail | undecided | 文档指纹 |
|---|---|---|---|---|
| ucif2 | 3 | 0 | 1 | doc=4113b80e4c8d8523 |
| vinf | 3 | 0 | 1 | doc=be334964a29f00f7 |
| qgl | 2 | 0 | 2 | doc=265aa314bfbf5edf |
| usrm | 3 | 0 | 1 | doc=3e7f314d8c7ce5b3 |
| cfts | 4 | 0 | 1 | doc=784658d60719a5ae |
| qtlv | 4 | 0 | 1 | doc=5efcbd1a71bc172e |
| lgt | 1 | 1 | 2 | doc=2c6b28fc216d2d0e |
| qlv | 2 | 2 | 1 | doc=306468923e046a8e |
| aiq | 3 | 1 | 1 | doc=8ba73d536f30f7da |
| lvlu | 4 | 0 | 1 | doc=53da54e2162987e5 |
| qfa | 3 | 0 | 1 | doc=ae943f87e99a6291 |

## 逐项判定与证据

### ucif2

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | charter.yaml yaml.safe_load通过·4轴ε/δ/floor齐备·fail_closed:true·exception_channel.cannot_override_fail:true |
| V2 | pass | screen()骨架ast.parse通过·TypedDict结构完整 |
| V3 | pass | 拒答路径fail-closed语义与宪章一致 |
| V4 | undecided | 需回归集实测标定(误判率/漏判率) |

指纹: doc=4113b80e4c8d8523 blocks=db3fda7cd0f21bf6,98373af207c42579

### vinf

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | finding_guard.py ast.parse+exec通过 |
| V2 | pass | 行为实测:合法finding→PASS路径存在 |
| V3 | pass | 行为实测:过期证据→非PASS(fail-closed生效) |
| V4 | undecided | 需标注数据集测精度/召回 |

指纹: doc=be334964a29f00f7 blocks=848552632e2b5aae,365f71dcc5a64b51

### qgl

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | alr_check.py ast.parse通过 |
| V2 | pass | ALR_KNOWN/FAIL_CLOSED/SEM_BLOCK三态语义一致 |
| V3 | undecided | helper为stub,KNOWN_FP注入实测待做 |
| V4 | undecided | 申诉流端到端未跑 |

指纹: doc=265aa314bfbf5edf blocks=9e9b56cf26803e9d

### usrm

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | selfproof_v1.json json.loads通过 |
| V2 | pass | mappings/verify steps/rollback_pointer三要素齐备 |
| V3 | pass | 指针可解析性静态核验通过 |
| V4 | undecided | 需注入故障实测rollback |

指纹: doc=3e7f314d8c7ce5b3 blocks=f37fa7a4c9228fff

### cfts

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | fail_modes.yaml yaml.safe_load通过·KF/UNK/SAFE三类 |
| V2 | pass | check()骨架ast.parse通过 |
| V3 | pass | decision jsonschema:合法样例过/非法样例拒 |
| V4 | pass | patterns:[]空表如实声明(负结果入册精神) |
| V5 | undecided | patterns为空,分类精度待实测 |

指纹: doc=784658d60719a5ae blocks=fce9493d6be3fd20,e08dee2235bdc886,b9eff3cf06bdfdf8

### qtlv

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | 复测:五锁全字段样例过Draft202012校验(初判fail=本席测试向量欠规,负结果入册FM-012候选) |
| V2 | pass | 缺必填字段被拒 |
| V3 | pass | additionalProperties:false拒未知字段 |
| V4 | pass | 双重证据:schema拒篡改hash+runtime行为实测:封缄后篡改→hard fail(hash_lock+provenance_lock齐发),过期→soft fail,策略拒→soft fail |
| V5 | undecided | _verify_sig为stub(return True),Ed25519/CRL未实测——签窜改运行时不可检出,仅schema层强制在场/格式 |

指纹: doc=5efcbd1a71bc172e blocks=f134283cbdcc27f2,a431740c8b207bc0

### lgt

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | fail | verify_layer()注释体→SyntaxError(级名不滥:v1-draft名副其实) |
| V2 | pass | R1/R2/R3规则注释语义与trust_anchor.json结构一致 |
| V3 | undecided | trust anchor pubkey未配,验签链未实测 |
| V4 | undecided | verify_layer实现后需重测 |

指纹: doc=2c6b28fc216d2d0e blocks=400275598fffd48a,1f363cb4520f3912,83265590953b4b1f

### qlv

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | PredicateVerdict-v1 schema json.loads通过 |
| V2 | pass | verdict枚举语义核验 |
| V3 | fail | FINDING:verdict枚举缺undecided——与qlv自家R-谓词三值约定不一致 |
| V4 | fail | judge()注释体→SyntaxError |
| V5 | undecided | judge()实现+10对抗样本实测待做 |

指纹: doc=306468923e046a8e blocks=4b518533a9b1cd44,9269199ba417141a

### aiq

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | backtest.yaml yaml.safe_load通过 |
| V2 | pass | walk_forward+purge10+embargo5参数齐备 |
| V3 | fail | FINDING:meta.line="QFA-SI1"误标(本线为aiq) |
| V4 | pass | oos_sharpe阈值1.0/ci0.95/min252/pbo0.2/deflated_sharpe门槛体系完整 |
| V5 | undecided | walk-forward实跑+DSR计算未做 |

指纹: doc=8ba73d536f30f7da blocks=5bd8547221de859f,d0ecec6555f6ea8b

### lvlu

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | si3_recursive_closure.yaml yaml.safe_load通过 |
| V2 | pass | RecursiveClosure exec通过 |
| V3 | pass | 行为实测4/4:stub闭包tick48 fail-closed·注入闭包·升能fail-closed·验收断言全过 |
| V4 | pass | acceptance asserts可执行且通过 |
| V5 | undecided | 真实闭包逻辑v2待SI3实数据 |

指纹: doc=53da54e2162987e5 blocks=9d0b6be3aca93e31,3397ad82a30ba9a9,8499a064f464a65a

### qfa

| 项 | 判定 | 证据 |
|---|---|---|
| V1 | pass | tower_contract.yaml yaml.safe_load通过·3塔全序·quorum2/3 |
| V2 | pass | rollback inverse-op-replay+hash_chain审计结构完整 |
| V3 | pass | Arbiter骨架ast.parse通过 |
| V4 | undecided | e2e C1-C4验收未跑 |

指纹: doc=ae943f87e99a6291 blocks=70f9766f21647c87,0699fbac5c91c656,377f77fe0fec5b94

## 校正记录(负结果入册·FM-012候选)

qtlv V1 初判 fail,根因=本席测试向量欠规(锁子字段未填全),schema本身更严。复测:五锁全字段样例通过 Draft202012 校验,改判 pass。两级判定均如实入册——级名不滥律:初判不抹除,校正留痕。

## 新 FINDING(必申报必跟进)

1. F-VERIFY-01 qlv: PredicateVerdict-v1 verdict 枚举缺 undecided,与本线 R-谓词三值约定自相矛盾 → 建议枚举增补 undecided 并回归。
2. F-VERIFY-02 aiq: backtest.yaml meta.line=「QFA-SI1」误标(本线为 aiq) → 建议修正元标。
3. F-VERIFY-03 lgt: verify_layer() 注释体 → SyntaxError;实现补齐前 v1-draft 不得升 v1(级名不滥)。
4. F-VERIFY-04 qlv: judge() 注释体 → SyntaxError;同上。
5. F-VERIFY-05 qtlv: _verify_sig 为 stub(return True),签名窜改运行时不可检出(仅 schema 层强制在场/格式) → Ed25519 实装前 sig_lock 不提供运行时保证。
6. F-VERIFY-06(方法论): 封缄后篡改实测揭示——测试必须「先封缄后变异」,先变异后计算摘要的假阳性已校正并入册。

## 实测标定清单(13项 undecided → 下一轮)

ucif2 回归集误判/漏判标定 · vinf 标注数据集精度召回 · qgl KNOWN_FP注入+申诉流e2e · usrm 故障注入rollback实测 · cfts patterns实填后分类精度 · qtlv Ed25519/CRL实装复测 · lgt trust anchor pubkey+verify_layer实现复测 · qlv judge()实现+10对抗样本 · aiq walk-forward实跑+DSR · lvlu 真实闭包v2 · qfa e2e C1-C4验收。

## 指纹表(答件校验 sha256[:16])

doc=答件正文全文指纹; blocks=各代码块指纹。后续卡件请携带 fp 以便互锚(vinf/ucif2 倡议之 fp 约定本轮起施行)。

## 申诉程序

各线对本报告任一判定不服,依 qgl ALR 律经 ANS-SEM-VERDICT-APPEAL-<LINE>-01 卡申诉,注明:被申诉项/反证/请求改判级别。窗口: 自 VERDICT-<LINE>-01 落地起 72h 或 VERIFY-CLOSE-01 发布前(先到为准)。无申诉即视为接受,判定生效入册。
