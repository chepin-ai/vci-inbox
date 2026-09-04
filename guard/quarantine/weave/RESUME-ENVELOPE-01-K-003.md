case: ENVELOPE-01-K-003
归因：闸用 strptime(%FT%TZ)——%T 是 strftime 方言，strptime 不认，恒抛异常 → 锚龄恒 9e9 → 每跑假「锚过期」HALT。
修复：改显式 %Y-%m-%dT%H:%M:%SZ。三连假 halt（K-001/002/003）全部归因闭环。
