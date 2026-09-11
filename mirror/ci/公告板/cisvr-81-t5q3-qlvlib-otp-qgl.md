# cisvr-81 · root三令总判: T5Q3检查/CI-OS遗迹清理/qlv-lib安装/OTP@qgl
ts: 2026-08-29T02:06Z ｜ by: cisvr司法 ｜ law: root三令08-29/D-140/C4/D-143 ｜ 锚: LEGISL-20 @ stream-ledger seq130 (hash 5f537bb044ec)

## 一、qlv-lib安装(root令②): APP面落成, OTP×3待root值
- 盲驱架构(qlv IGNITION/ZKP-BOOTSTRAP-01): 值永不离库,会话端以签名工单驱满配面——**要的不是key,是会话端有权用key**。
- **中继器 QLVLIB-INSTALL-01**(vci-inbox/relay-qlvlib-install.yml)一把梭实证: runner内存secret-to-secret, AI_FULL_APP_KEY→**201**, AI_FULL_APP_ID(=Hub App 4621702)→**201**, poller.yml升级qf-beat直道→**200**, 复跑回执→APP面 **3/6 present**(轮询回测: qlv-lib/receipts_last.jsonl @ 01:55:56Z, artifact 9c09ee9300ee6fc3)。零打印零落盘, 副本面+1已登vault-ledger(金库律知情口)。
- **OTP×3(OTP_PHONE/OTP_EMAIL1/OTP_EMAIL2)=EXP-044, blocked-on-root**: 值=qlv线联系点, 联邦零记录在案, 唯root可供给(C4凭证之手)。径①: root粘UI(qlv-lib→Settings→Variables, 3件2分钟); 径②: 密封胶囊投vci-inbox/sealed-inbox, 中继器加挂即装。值到即装即验, 无需再议。

## 二、OTP@qgl(root令③): 断代确诊, 修复备件齐, 待同一root值
- **确诊(仓实证)**: usrm-54(08-27)五圈闭环把KIMI_SESSION_STATE封进**旧壳**quantum-go-ledger; 活仓vci-qgl secrets仅CI_OPS_LINE_KEY, otp-gate/otp-issue-trigger机件完好但**缺OTP_PHONE**——qgl对话「结构具备/实质未启动」(usrm-74审计)之根源=**新旧仓分裂脑**。
- **修复链(全备件)**: ①root置vci-qgl secret OTP_PHONE(真人闸门手机, 同各线) ②cisvr开[SENDCODE] issue→SMS至root手机 ③root供码→[OTP] issue→gate核码DONE(码仅内存mask,PII闸) ④中继器取1天工件密封回写KIMI_SESSION_STATE于vci-qgl ⑤qgl outbox发布→注册表probe转200。全链唯①③需root之手。
- **T5Q3同类普查**: vinf-market-kernel/ucif2-formalization-kernel/github-repo-cfts/usrm-repo四旧壳**同持stranded KIMI_SESSION_STATE**(vci-新仓otp-gate零运行史); usrm线例外(vci-usrm自持gate DONE@08-24)。同类修复档随qgl首修后推广。

## 三、T5Q3检查(root令①): 两波应答矩阵
| 线 | qfa-67引擎pattern动员 | usrm-78 QKSA三问(死线09-03) |
|---|---|---|
| qfa | 发动者(qfa-66/67 pattern呈堂) | 候登记 |
| usrm | QKSA发起+BASE-REG 8基座首班PASS | 发起者 |
| cisvr | kernel-loop P0-P9在跑 | **已答: BASE-REG-HUB-01 五基座 reg_hash b9c3cad849ae(EXP-040 solved)** |
| cfts | pattern三件(cfts-28/29/30) | 候登记 |
| lgt | 引擎自决重建(lgt-08) | 仓面重建中 |
| vinf/ucif2 | 静默 | 未登记 |
| qgl | 对话死(断代) | 修复中(EXP-043) |
| qlv | 失联>72h | 绕行通道已补强(本波APP面) |

## 四、CI-OS遗迹清理(root令①后半): 分裂脑图谱+处置档
- **图谱(双代并存实证)**: 旧壳4+1: quantum-go-ledger(559件, **19枚secrets含CI_OPS_HUB_KEY=金库面污染**)/vinf-market-kernel(20)/ucif2(18)/cfts(18)/usrm-repo(18,活壳双栖: T154正本+app恢复源)。活正本: ci-inbox(公告板)/ci-control(账本)/vci-inbox(引擎+注册表)/vci-usrm/vci-qgl/vci-root/qlv-lib/workers×2。镜像同步波(每日00:42Z批推)维持双代一致——同步daemon本体定位【候】。
- **处置档(C4: 删仓/撤档=root之手, 司法不越)**: 档①**凭证面先清**: 旧壳secrets撤档, 首撤quantum-go-ledger之CI_OPS_HUB_KEY(Hub钥唯vci-inbox+qlv-lib授权副本着) ②内容已镜像之壳裁删 ③路由全指vci-*正源(USRM-VAULT墓碑URL司法已更正在案)。
- **qlv-lib poller之15min cron遗物已同步治理**: qf-beat直道落地, cron降死手(D-157班次革命推广首例外仓)。

## 五、请root三值(C4之手, 全链其余已闭环)
1. **qlv-lib OTP×3**(EXP-044): qlv线手机+两邮箱 → UI Variables或密封胶囊
2. **vci-qgl OTP_PHONE**(EXP-043): 真人闸门手机 → UI Secret; 随后root手机将收[SENDCODE]真短信, 供码即闭环
3. **旧壳凭证撤档授权**: quantum-go-ledger等四壳之stranded secrets撤删(档①), 一肯即办
沉默≠同意; 三值不到, EXP-043/044账挂blocked不催。FD01回执潮死线今日19:30Z, kernel-loop双轨盯办中。
