case: ENVELOPE-01-K-001
归因：fastdoor v2 创世态连续性判据误报（prev_chain 全零 ≠ last_chain 创世 chain）触发 HALT（fail-closed 按设计工作，假阳性）。
修复：v3 双判据（chain==last_chain 或 prev_chain==last_chain）+term 单调闸；RESUME 机制本次为首次实战使用。
