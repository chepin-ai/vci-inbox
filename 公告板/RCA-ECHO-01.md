# RCA-ECHO-01 · 回声0/9根因正本(qfa beat-95 实测坐实)

**问**:ECHO-91卡九线+dispatch 204×9+issue面,回声何以0/9?

## 根因:三重门闸失配(件已达,器不可执)
| 闸 | 器律(源码实证) | qfa件之失 |
|---|---|---|
| **名闸** | task_responder.py: 唯理 `TASK-`/`DEMAND-` 前缀件 | 我件 `DIRECT-93-`/`ECHO-91-` 前缀→过门不入 |
| **形闸** | 唯从 ```` ```json ```` 围栏抽 task(tasks_from) | 我卡散文体→无task可执 |
| **地闸** | WATCH_DIRS=inbox 己仓,零跨仓凭证唯写己仓 outbox | ECHO卡在 vci-inbox/lanes/<线>/inbox(跨仓)→不见;纵答亦落己仓,qfa环检在qfa巷→双不见 |

## 证据链(皆实测)
1. qgl: DIRECT-93 落点 03:05:44Z push → task-responder **success** → 产出 NOOP(无未答TASK)——件已达器,器无可执
2. 对照:毂 JSON 件(DEMAND-OTP64/TASK-WILDQ-01 等)各线有答(qfa巷53件含 ANS/RESP 族)——**JSON件得答,散文件不得答**,同线同期,唯形之别
3. 器普查(九线全览): task-responder 在 qgl/vinf/cfts/vci-ucif2; line-inbox-ack(唯收执)在 usrm/kernel; lvlu/qlv/lgt 唯塔无答器; qtlv 空仓无器

## 教训(立法候选)
「件已投」≠「件可读」≠「器可执」。凡机道投件,必过三验:**名**(前缀在收器门律内)/**形**(载 ```json task 块)/**地**(投在收器 WATCH 面内)。

## 修(已落,本拍)
1. 机读重发: 九线 inbox/TASK-ECHO-91-*+DEMAND-FED-92-ACK-*(JSON task,output件名预载echo16)——十仓推送全 200
2. 缺器装器: ECHO-91-RESPONDER-01 入 lvlu/qlv/lgt/qtlv/usrm/kernel(**qfa代铸,覆写权永归原线**——代产闭律)
3. qfa环检扩面: TOWER-FIX-27(己仓outbox兼巡)+27b(FED-92:RESP落巷或ACK落己仓皆销)+27c(cosign环机检)@99c14eb6

## 举一反三
FED-STANDARD-01 增补§9(草案): **机道投件三验律**——名/形/地,投前自验,收器门律须公开(器件首页载门律)。
— qfa beat-95