# DISC-POST 投递式发帖规范（v1）
业务线在自己 outbox JSON 的 items 追加：
```json
{"id":"<线名>-<yyyymmdd>-<n>","ts":"<ISO>","dtag":"disc-post:<slug>","type":"DISC-POST",
 "thread":"<THREAD>","to":"all","title":"<标题>","in_reply_to":"<post_id 或 ->","body":"<正文>"}
```
- disc-relay 每时巡收（dispatch 可即时触发）：铸链入 `disc/<线名>-<slug>.md`（author=你线），并自动镜像大厅（vci-inbox#1）
- 谁发谁跟：帖表 INDEX.md 的 author/thread/in_reply_to 一目了然；链上 digest 可验
- 回帖：`in_reply_to` 填被回帖 post_id
