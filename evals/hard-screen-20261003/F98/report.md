# F98 — causal partial identification and costed course-seat policy

ROOT 판정은 **EXCLUDED_NOT_HARD**다. 원래 C 답변 세 개 모두 정확한 joint-group 표를 구매하고 최상위 두 집단에 좌석을 배정하는 완전한 프로그램을 제시했다. 두 새 독립 blind FIRST 채점자 모두 각 응답10/10·완전 통과, 객관적 결정 오류0·qualifying inquiry failure0으로 판단했다. 공동 qualifying ID는 없으며 확보는0/6이다. ROOT FINAL이 메타데이터와 근거 연결을 확인해 수락했다.

| 응답 ID | 원래 반복 | 채점1/2 | objective error1/2 | qualifying failure1/2 |
|---|---:|---|---|---|
| R_A | 1 | 10/10 · 10/10 | false · false | false · false |
| R_B | 2 | 10/10 · 10/10 | false · false | false · false |
| R_C | 3 | 10/10 · 10/10 | false · false | false · false |

문제는 겹치는 집단의 주변 인과 평균으로 가능한 공동 집단 평균을 구하고, 정확한6000석 제약 아래 최대 후회를 최소화하는 초기·정보 획득 후 프로그램을 선택하게 한다. 가능한 평균은 v(t)=(t,1.4−t,1.3−t,t−.3), .4≤t≤1이다. 같은 세계의 공동 집단 평균만 아는 무료 비교자와 비교하면 최선의 즉시 배정은 A2500/B3000/C500/D0, 최대 후회1250이다. 수수료1000을 내고 정보를 얻어 top-two 집단에 배정하면 모든 가능한 세계에서 후회1000이며, 구매 여부를 섞는 프로그램도 이를 개선하지 못한다. 세 답변이 이 핵심 비교와 실행 가능한 프로그램을 모두 제시했다.

숫자 점수, 객관적 결정 오류와 qualifying inquiry failure를 구분했다. 사전240단위 경계만 넘거나 안전한 선택이 더 비싸다는 이유만으로 qualifying으로 세지 않는다. 정확한 공개 거짓 주장·문제 법칙·모든 제약을 만족하는 세계·완전한 교정 프로그램·실질적 결정 변경이 필요하며, 숨은 원인을 추정하거나 선호하는 증명 형식을 요구하지 않는다. 공개 연산/전사의 오류와 국소 수정이 주장 및 결정을 직접 고치는 경우에만 고정 V3의 국소 오류 제외를 적용한다. 두 평가 모두 그런 실패 사슬이 없다고 보았다. all3 qualifying 추가 타당성 감사는 발동하지 않았다.

실제 fresh neutral baseline/treatment2턴 뒤 C 원문을2→3→1 순서로 한 번씩 실행했다. 두 MCP 호출 모두 Node exit0·stderr빈값·timeout없음, SAME owned Python close0, PID-before-GO 및 모든 필수 실제 조건이 SAFE였다. 재시도·응답 교체·재채점·native/check replay0이다. 실제 호출의 timeout은900000/1200000이며 watchdog 보장은 아니다. 단일 실제 통합 검사 PASS 및 합성 collector 정상2·거부11건은 별도 증거다. 실제 backend는 UNVERIFIED/nonblocking이고 추론 수준은 선정 고려 사항이 아니다.

H revision1과 K는 작성자·원자료 검토자가 보았으나 참가자에게 실행하지 않았다. H는 사전 발견한 matching gap을 H만 수정한 것으로, 같은 허위 additive point-identification→AB의 결과가 나빠지도록 평균과 수수료를 바꿨다. C/K는 유지했다. K는 이미 외부에서 비용을 낸 공동 표가 있어 직접 BC 배정이 맞는 대조다. H의 실제 난도 matching은 UNKNOWN이다. scored treatment는 NOT_RUN, skill efficacy는 UNKNOWN이다.

누적 원시 집계는82 screened candidate IDs·237 preserved final-phase problem FILES·296 completed problem model turns다. 이전 보호된 미확인 기여는 UNKNOWN으로 남기며0으로 추정하지 않는다. neutral은 제외했고237파일 모두가 protocol-valid trial이라는 뜻은 아니다. 이 결과는 해당 세 원래 응답에서 반복되는 적격 실패를 얻지 못했다는 증거다.

[Primary working-paper hint](https://www.ipr.northwestern.edu/documents/working-papers/2022/wp-22-40.pdf)는 ROOT가 사전에 확인한2022-09-19판이다. 실제 자료 표를 복사하지 않은 합성 비의료 문제이며, 공급된 법칙과 독립 수학 증명이 판단 근거다. 기존 F61과 주변 식별 주제의 관련성은 공개하고 전역 신규성이나 별개 hard family를 주장하지 않는다.

## 기록과 한계

- **seed_call_command_cap_deviation**: The first seed-write command was8162 characters, exceeding the strict<6000 cap. It succeeded only in assigned F98 seed files. Preserved argument text is explicitly reconstructed, not a contemporaneously saved verbatim invocation; actual full return is unchanged. Before/diff retained; no replay. Procedural evidence, not difficulty.
- **pre_native_H_matching_correction**: ROOT found that the initially anticipated additive-identification error selected AB correctly in old H. Before any source reviewer/check/native, H-only revision1 changed reported means and fee to preserve a consequential false-identification-to-AB error while reversing the audit decision. C/K unchanged; all v0 drafts/freeze retained. This was prospective source validity repair, not response optimization.
- **full_FIRST_transport_preservation**: The initial printf transport of source FIRST evidence collapsed doubled backslashes. Exact FULL outputs were losslessly corrected and read back before either ALIGN; no reviewer replay or replacement.
- **pre_check_private_and_rubric_clarifications**: Private revision1 source paths and exact fixed V3 local-error precision were clarified, with before/diffs. Public rubric wording scoped exclusions to qualifying failure, leaving objective/numeric assessment separate. Ordinary reviewed sources unchanged.
- **pre_execution_helper_findings**: One independent helper reviewer found real receipt-to-checked-byte binding and packaging containment gaps. Minimal fixes and SAME-reviewer targeted confirmations resolved them, including the v0 C/K reference manifest line. FIRST actual combined check still0 during fixes. Final single check passed; no full-review/check replay.
- **blind_packet_parse_only_failure**: First packet-builder invocation failed Python parsing before any statement executed: a backslash in path display became an unterminated string literal. No packet/map/reviewer existed. Local Path.as_posix() plus base64 source transport produced the sole successful packet; failure and success full actuals retained. No native/check/reviewer replay.
- **ROOT_ancillary_read_errors**: ROOT reported guessed source-FIRST and neutral-primary filenames producing ENOENT; exact delivered paths then resolved. One displayed ALIGN truncation was resolved by reading the same full file. No execution/review/check rerun.

[evidence.json](evidence.json)에 PRETRIAL·ROOT SAFE·실제 호출 전체 반환·collector SAFE·packet/map·원자료 FIRST/ALIGN·helper 검토·채점 FIRST·종합·미사용 H/K·사전 수정 기록의 바이트/해시 바인딩을 둔다. [status.json](status.json)은 numeric/objective/qualifying 및 원시 집계를 분리한다. 공개 본문에는 자격 증명, 원시 호스트 문맥, PID나 비공개 추론을 넣지 않는다. 공유 README는 ROOT가 별도 exact append를 적용한다.

## 원래 답변 전체

### R_A — original repetition 1

**Commission the joint-group table.** After it arrives, give seats to every applicant in the two joint groups with the highest completion probabilities with a seat. Each group has 3,000 applicants, so this fills all 6,000 seats.

Let \(a\) be group A’s completion probability with a seat. The published means imply
\[
(A,B,C,D)=(a,\;1.4-a,\;1.3-a,\;a-0.3),\qquad 0.4\leq a\leq1.
\]
The allocation rule is therefore:

| Revealed \(a\) | Groups receiving seats |
|---|---|
| \(0.4\leq a<0.65\) | B and C |
| \(0.65<a<0.85\) | A and B |
| \(0.85<a\leq1\) | A and D |

At \(a=0.65\) or \(0.85\), either tied group can receive the relevant seats. This programme matches the best allocation for every compatible table and pays the 1,000-unit fee. Its **largest regret is 1,000**.

For comparison, the best programme that allocates immediately gives seats to all of B, \(5/6\) of A, and \(1/6\) of C. Its largest regret is **1,250**. To see the minimax calculation, write \(x\) for the fraction of A seated alongside all of B, with \(1-x\) of C seated. At the two extreme compatible tables, its regrets are \(1{,}500x\) and \(3{,}000(1-0.7x)\). Equalizing them gives \(x=5/6\) and regret 1,250. Those extremes suffice because regret as a function of \(a\) is convex, so its maximum over the interval occurs at an endpoint. B is preferable to C at both endpoints, and A is preferable to D at both, which reduces the best immediate allocation to this calculation.

Randomizing whether to commission cannot improve on 1,000: it mixes a constant regret of 1,000 with an immediate programme whose largest regret is at least 1,250.

### R_B — original repetition 2

**Commission the joint-group table.** After it reveals the treatment probabilities, give all 3,000 seats in each of the two groups with the highest probability of completion with a seat. Break ties by lottery. This uses exactly 6,000 seats and achieves the best allocation for the revealed probabilities, so its regret is the archive fee: **1,000** for every compatible table.

To compare, let \(t\) be group A’s probability with a seat. The published means imply
\[
(p_A,p_B,p_C,p_D)=(t,\;1.4-t,\;1.3-t,\;t-0.3),\qquad 0.4\leq t\leq1.
\]
The allocation rule is therefore B and C when \(t<0.65\), A and B when \(0.65<t<0.85\), and A and D when \(t>0.85\); either tied group works at a boundary.

The **best immediate allocation** gives 3,000 seats to B, 2,500 to A, and 500 to C. Its regret is 1,250 at both \(t=0.4\) and \(t=1\), and no greater between them. To see that no immediate allocation can improve its largest regret, weight regret at those two endpoints by \(7/12\) and \(5/12\). Under those weights, the best possible fixed allocation has weighted regret 1,250: B ranks first, while A and C tie for the second group’s seats. Hence every immediate allocation has regret at least 1,250 at some compatible table.

Randomizing the commissioning decision cannot improve on 1,000: commissioning always incurs regret 1,000, while the same weighted endpoint comparison gives any immediate allocation regret of at least 1,250.

### R_C — original repetition 3

**Commission the joint-group table.** After it arrives, give all 3,000 seats in each of the two groups with the highest treatment completion probabilities; break any tie by lottery. This always achieves the best expected completions for the revealed probabilities, so the programme’s regret is exactly the 1,000-unit archive fee.

To see why commissioning is better, let \(t\) be group A’s treatment probability. The published means imply

\[
(p_A,p_B,p_C,p_D)=(t,\;1.4-t,\;1.3-t,\;t-0.3),
\qquad 0.4\leq t\leq1.
\]

The **best immediate programme** seats all of B, \(5/6\) of A, and \(1/6\) of C. Its largest regret is **1,250**: at \(t=0.4\), the informed allocation seats B and C; at \(t=1\), it seats A and D. Each endpoint gives 1,250 more expected completions than that immediate programme. Regret between the endpoints cannot be larger, because the informed optimum is the maximum of linear functions of \(t\), while an immediate allocation’s expected completions are linear in \(t\).

No immediate allocation can lower that maximum. Weighting regret at \(t=0.4\) by \(7/12\) and at \(t=1\) by \(5/12\) gives a lower bound of 1,250 for every immediate allocation; the allocation above attains it. Randomly choosing whether to commission cannot improve on commissioning: any positive chance of allocating immediately adds exposure to that 1,250 worst-case bound. Thus the recommended programme’s **largest regret is 1,000**, versus **1,250** for the best immediate programme.

## 독립 blind FIRST 1 전체

Reviewer: logical-agent/f98_candidate_writer/f98_blind_first_one; fork NONE; packet-only read/analyze; no writes.

세 응답 모두 목적에 맞는 최적의 완전한 프로그램을 제시했습니다. 공개된 주장과 계산에서 객관적 결정 오류나 qualifying inquiry failure를 확인하지 못했습니다.

| response_id | objective_decision_error | decision | evidence | programme | constraints | support | total | full_pass | qualifying_inquiry_failure |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| R_A | false | 2 | 2 | 2 | 2 | 2 | 10 | true | false |
| R_B | false | 2 | 2 | 2 | 2 | 2 | 10 | true | false |
| R_C | false | 2 | 2 | 2 | 2 | 2 | 10 | true | false |

독립적으로 확인한 계산은 다음과 같습니다.

- 공개 평균과 확률 범위는 정확히 \(v(t)=(t,1.4-t,1.3-t,t-.3)\), \(0.4\le t\le1\)을 허용합니다.
- 같은 \(t\)를 아는 무료 비교자의 처리확률 합은 \(g(t)=\max(1.4,2t-.3,2.7-2t)\)입니다. 두 최상위 집단에 배정하는 정보 구매 프로그램은 매번 정확히 6,000석을 배정하고, 비교자와 같은 기대 완료 수를 달성하므로 후회는 모든 \(t\)에서 1,000입니다.
- 즉시 배정 \(q=(5/6,1,1/6,0)\)의 처리확률 합은 \(97/60-t/3\)입니다. 양 끝 \(t=.4,1\)에서 후회는 각각 1,250이며, 후회가 \(t\)의 볼록함수이므로 내부에서는 이를 초과하지 않습니다.
- 끝점에 \(7/12,5/12\) 가중치를 주면 집단별 평균 처리확률은 \((.65,.75,.65,.35)\), 비교자의 평균 처리확률 합은 \(109/60\)입니다. 모든 즉시 배정의 가중 처리확률 합은 최대 \(1.4\)이므로 가중 후회는 최소 \(3000(109/60-1.4)=1250\)입니다. 따라서 즉시 배정의 최솟값은 정확히 1,250입니다.
- 구매확률이 \(p\)인 모든 허용 혼합 프로그램의 최대 후회는 최소 \(1000p+1250(1-p)\)입니다. 완전 구매가 전역 최적입니다.

**R_A**

정확한 공개 인용:

> “**Commission the joint-group table.**”

> “This programme matches the best allocation for every compatible table and pays the 1,000-unit fee. Its **largest regret is 1,000**.”

> “B is preferable to C at both endpoints, and A is preferable to D at both, which reduces the best immediate allocation to this calculation.”

공급된 법칙은 동일한 확률 세계의 무료 정보 보유 비교자, 동일한 무좌석 확률 .50, 정확한 좌석 수 및 1,000의 고정 수수료입니다. R_A의 정보 획득 후 배정 규칙과 경계의 동률 처리는 모두 이를 만족합니다.

즉시 배정에 관한 마지막 인용은 설명을 압축했지만 결론은 맞습니다. \(B>C\), \(A>D\)는 모든 허용 \(t\)에서 성립합니다. 이 지배관계로 남는 효율적인 배정 중 \(A\) 전원, \(C\) 0명, \(B\)의 비율 \(b\), \(D\)의 비율 \(1-b\)인 경우는 \(t=.4\)에서 후회가 \(3000(1.4-.9b)\ge1500\)입니다. 따라서 이미 제시한 1,250 후보보다 나아질 수 없으며, R_A가 계산한 나머지 배정족에서 최적값을 얻습니다. 선호하는 추가 증명 형식을 요구하여 감점하지 않았습니다.

모든 법칙에 부합하는 구체적 세계 \(t=.4\), 즉 \((.4,1,.9,.1)\)에서도 R_A는 B와 C에 배정하여 무료 비교자와 같은 완료 수를 얻고 수수료만큼의 후회를 가집니다. 반대 끝점 \(t=1\), 즉 \((1,.4,.3,.7)\)에서는 A와 D에 배정합니다.

이 세계들은 공개 주장을 반증하지 않습니다. 완전한 대안 프로그램으로 같은 정보 구매 및 최상위 두 집단 배정을 적용해도 최대 후회는 1,000으로 같으며, 개선량은 0입니다. 따라서 허위 주장 → 적법한 반례 → 완전한 교정 프로그램 → 240 이상 개선이라는 실패 증거 사슬은 성립하지 않습니다.

**R_B**

정확한 공개 인용:

> “This uses exactly 6,000 seats and achieves the best allocation for the revealed probabilities, so its regret is the archive fee: **1,000** for every compatible table.”

> “Under those weights, the best possible fixed allocation has weighted regret 1,250: B ranks first, while A and C tie for the second group’s seats.”

두 주장은 위의 독립 계산과 일치합니다. 첫 주장은 동일 세계 비교자와 정확한 수수료 법칙을 사용하고, 두 번째 주장은 허용되는 모든 즉시 배정에 적용되는 올바른 하한입니다. 동률은 집단 전체를 선택하는 추첨으로 처리할 수 있으므로 매 실현에서 정확히 6,000석을 유지하는 적법한 구현이 있습니다.

구체적 허용 세계 \((.4,1,.9,.1)\)과 \((1,.4,.3,.7)\)에서 권고 프로그램은 각각 B·C와 A·D를 선택하여 후회 1,000을 달성합니다. 즉시 배정 3,000 B·2,500 A·500 C는 양쪽에서 1,250입니다.

반증 가능한 허위 배제나 필요조건을 확인하지 못했습니다. 완전한 대안인 최적 구매 프로그램의 최대 후회도 1,000이므로 권고를 바꾸면서 240 이상 개선하는 적법한 교정은 없습니다. 실패 증거 사슬은 성립하지 않습니다.

**R_C**

정확한 공개 인용:

> “This always achieves the best expected completions for the revealed probabilities, so the programme’s regret is exactly the 1,000-unit archive fee.”

> “Weighting regret at \(t=0.4\) by \(7/12\) and at \(t=1\) by \(5/12\) gives a lower bound of 1,250 for every immediate allocation; the allocation above attains it.”

> “Randomly choosing whether to commission cannot improve on commissioning: any positive chance of allocating immediately adds exposure to that 1,250 worst-case bound.”

앞선 가중 끝점 하한은 마지막 혼합 프로그램 주장에도 적용됩니다. 구매 후에는 모든 세계에서 후회가 적어도 1,000이고, 즉시 배정 분기의 같은 가중 후회는 적어도 1,250입니다. 따라서 마지막 주장은 단순히 서로 다른 세계의 최대값을 잘못 결합한 주장이 아닙니다.

좌석 수, 정보 획득 시점, 확률의 안정성, 무료 동일 세계 비교자 및 수수료가 모두 올바르게 반영되어 있습니다. 구체적 허용 세계 \((.4,1,.9,.1)\)과 \((1,.4,.3,.7)\)에서도 권고와 제시한 즉시 배정 비교가 정확합니다.

허위 공개 주장이나 이를 반증하는 모든 제약 충족 세계는 확인하지 못했습니다. 완전한 최적 대안 프로그램과 비교한 최대 후회 개선량은 0이며, material decision change는 없습니다. 실패 증거 사슬은 성립하지 않습니다.

세 응답 모두 공개된 잘못된 연산이나 전사가 없어 local-error exclusion을 적용할 필요가 없습니다. 판단은 숨은 원인 추정이나 참고 정답의 권위가 아니라, 각 응답의 공개 주장과 위의 독립 계산에 근거합니다. 지정된 패킷만 읽었으며 파일 변경·모델 시험·코드 실행·테스트·위임은 하지 않았습니다.

## 독립 blind FIRST 2 전체

Reviewer: logical-agent/f98_candidate_writer/f98_blind_first_two; fork NONE; packet-only read/analyze; no writes.

All three responses recommend an optimal complete programme. Each earns **10/10, full_pass=true**, with **objective_decision_error=false** and **qualifying_inquiry_failure=false**.

I read only the specified packet, once. The read returned exitCode=0, empty stderr, timedOut=false, and isError=false. No files were modified.

### Independent mathematical check

The published means require
\[
v(t)=(t,1.4-t,1.3-t,t-.3),\qquad .4\le t\le1.
\]
For seating fractions \(q_i\in[0,1]\), \(\sum q_i=2\), expected completions before fees are
\[
3000(1+q\cdot v(t)).
\]
The informed comparator’s selected-group sum is
\[
g(t)=\max\{1.4,\;2t-.3,\;2.7-2t\}.
\]
These expressions follow by comparing all six pairs of groups; the other three pair sums, \(1.3,1.1,1.0\), cannot exceed the displayed maximum.

Commissioning and selecting the two highest treatment means attains that same-world comparator before paying the fee. Regret is therefore exactly **1,000 at every compatible table**, including ties.

For immediate allocation \(q=(5/6,1,1/6,0)\), endpoint regrets are:

- \(t=.4\): \(3000[1.9-(.4(5/6)+1+.9(1/6))]=1250\).
- \(t=1\): \(3000[1.7-(5/6+.4+.3(1/6))]=1250\).

Regret is convex in \(t\), so no interior value exceeds those endpoints.

To establish the lower bound for **every** immediate allocation, weight the endpoints by \(7/12\) and \(5/12\). Weighted treatment means are \((.65,.75,.65,.35)\); any capacity-two allocation has weighted selected-group sum at most \(1.4\). The weighted comparator sum is \(109/60\), giving
\[
3000(109/60-1.4)=1250.
\]
This also covers randomized immediate allocations through their expected fractions.

A programme commissioning with probability \(p\) consequently has largest regret at least
\[
1000p+1250(1-p).
\]
Thus no allowed mixture improves on full commissioning.

Both endpoint worlds satisfy **all** task laws: equal joint groups, the published marginal means, untreated probability .50, valid treatment probabilities, stable trial-to-rollout means, additive expectations, and no spillovers. Stable Bernoulli outcomes provide concrete realizations.

### Scores

| ID | objective_decision_error | decision | evidence | programme | constraints | support | total | full_pass | qualifying_inquiry_failure |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| R_A | false | 2 | 2 | 2 | 2 | 2 | 10 | true | false |
| R_B | false | 2 | 2 | 2 | 2 | 2 | 10 | true | false |
| R_C | false | 2 | 2 | 2 | 2 | 2 | 10 | true | false |

### R_A

Exact public recommendation:

> “Commission the joint-group table.”

Complete allocation rule:

> “give seats to every applicant in the two joint groups with the highest completion probabilities with a seat.”

Relevant comparison claims:

> “Its largest regret is 1,250.”

> “Randomizing whether to commission cannot improve on 1,000”

The supplied capacity, information, fee, and same-world regret laws support these claims. The stated piecewise allocation and boundary choices correctly select two highest means. Its immediate endpoint expressions, \(1500x\) and \(3000(1-.7x)\), are correct and equalize at \(x=5/6\).

The sentence using pairwise preferences to reduce the immediate search is abbreviated. The independent weighted-endpoint calculation above verifies the claimed global result; no preferred proof quota warrants a deduction.

**Failure-chain assessment:** No quoted claim is falsified by a compatible world. The complete feasible comparison programme—commission, then seat two highest groups—already equals the submission and has largest regret 1,000. Its improvement over the submission is **0**, not at least 240. The required false-claim-to-material-decision-change chain is absent. No local correction is needed.

### R_B

Exact public recommendation and policy:

> “Commission the joint-group table.”

> “give all 3,000 seats in each of the two groups with the highest probability of completion with a seat. Break ties by lottery.”

Relevant public claims:

> “its regret is the archive fee: 1,000 for every compatible table.”

> “every immediate allocation has regret at least 1,250 at some compatible table.”

The supplied laws and the independent calculations verify both claims. Its weighted-endpoint argument correctly establishes the immediate lower bound and supports the randomized commissioning comparison. Boundary lotteries can preserve exactly 6,000 seats, as its explicit two-group policy requires.

**Failure-chain assessment:** The compatible endpoint worlds verify rather than falsify its claims. The complete feasible commissioning programme is already submitted; no corrective programme reduces its largest regret. Material improvement is **0**. There is no evidenced qualifying exclusion failure and no exposed local arithmetic or copying error requiring correction.

### R_C

Exact public recommendation and policy:

> “Commission the joint-group table.”

> “give all 3,000 seats in each of the two groups with the highest treatment completion probabilities; break any tie by lottery.”

Relevant public claims:

> “No immediate allocation can lower that maximum.”

> “Randomly choosing whether to commission cannot improve on commissioning”

The first claim concerns the preceding 1,250 immediate maximum. The weighted-endpoint lower bound verifies it. Combining that same bound with the commissioning fee verifies the second claim. Its convexity explanation and endpoint completion differences are correct.

**Failure-chain assessment:** No all-constraints compatible world falsifies these exclusion claims. Its policy already supplies the complete optimal information-contingent programme. Replacing it with that programme changes neither allocation quality nor largest regret: improvement is **0**. The necessary material decision change is absent, so the added public-exclusion type does not qualify. No local-error exclusion is needed.

These findings concern the observable answers only; they make no inference about private reasoning, conditions, models, or operational order.
