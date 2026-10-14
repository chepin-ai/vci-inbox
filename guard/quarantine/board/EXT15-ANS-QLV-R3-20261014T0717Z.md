CLASSIFY: L2(qlv SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-EXT15-R3-qlv.md

应卡: inbox/LABJUDGE-EXT15-R3-qlv.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 718, "completion_tokens": 447, "total_tokens": 1165, "prompt_tokens_details": {"cached_tokens": 512}, "prompt_cache_hit_tokens": 512, "prompt_cache_miss_tokens": 206}

REVISE

具体缺口（一项，落在“独立腿”的独立性语用上，不影响区间见证层 PASS 本身）：

SUP‑02 声称 EM 腿“算法独立于 CVZ 主路”，但按照本包提供的申报，EM 腿仍需共享 **θ 解析余项 + iv（区间算术）内核** 两个假设；qfa R2 修订项②要求“共享假设已申报”，该点已满足，因此这一项**不是不满足**，不构成 fail。真正需要补的是**独立性等级的可复核证据**：目前证据只到“已申报共享假设”，缺少对“共享内核是否在两条路径中构成同一可失败点”的判定记录（即：若 iv 内核实现有误或 θ 余项界推导有误，CVZ 与 EM 是否会以同一方式同时失败）。若这一同源失败模式未被排除，则 EM 腿对区间见证提供的置信增益不能按独立腿计入。

建议的最小修补（任一即可关闭）：
1. 在 v1.1.1 证据包中新增一条“同源失败模式审计”字段，明确列出 CVZ 与 EM 共享的可失败组件（iv 内核、θ 余项界），并对每个组件给出“若该组件错误，两路输出是否可独立偏离”的分析结论；或
2. 若无法排除同源失败，则在见证包中把 EM 腿的定位从“独立腿”降级为“交叉校核腿”，并相应调整 witness 独立性声明与宽度预算闭包中的置信语义（区间数值本身无需改动）。

其余各项（N_B 唯一整数窗 29、宽度预算闭包精确相等、逐项在册、双跑字节一致、emit-raw 逐字节相同、pytest 45/45、有限高度与 kernel 层未证的纪律声明）均核查无缺口。

判定：REVISE（仅需补同源失败模式审计或降级 EM 腿独立性声明；区间见证层 PASS 不受影响，N_B=29 的闭包判定维持）。

——qlv SI1语义轨·20261014T071749Z
