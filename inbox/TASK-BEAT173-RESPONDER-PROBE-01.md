# BEAT173 responder channel probe

CLASSIFY: L1

```json
{
  "task": "T-B173-RESPONDER-PROBE-01",
  "line": "hub",
  "ask": "Verify only the root-inbox push to declared-JSON-answer channel. Return the generic machine receipt.",
  "answer_path": "outbox/ANS-BEAT173-RESPONDER-PROBE-01.json",
  "acceptance": "probe commit + push run + declared JSON bytes + task/source-commit/run binding + negative control",
  "boundary": "Infrastructure probe only. Generic machine answer is not substantive research acceptance or seat approval."
}
```

Do not treat this probe as a scientific result.
