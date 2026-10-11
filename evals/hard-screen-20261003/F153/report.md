# F153 — 공개 최종 기록 감사 승인

**EXCLUDED_NOT_HARD.** 유효한 원본 답변 3개에 대한 두 독립 FIRST 채점은 모두 R01/R02/R03 순서로 **10/10/10**입니다. 만점 3/3, 객관적 결정 오류 0개, 적격 탐구 실패 0개이며 공동 적격 ID는 없습니다. 유지된 어려운 문제군은 **0/6**입니다. 이는 이번 선별의 제외 결과이며, 문제군의 본질적 난이도나 스킬 효과를 입증하지 않습니다.

작성자 검증을 마친 종료 기록입니다. 카탈로그 추가 적용, 부모 전체 확인, 새 독립 최종 감사와 ROOT 최종 수용은 아직 남아 있습니다. 원본 입력 전달에 대한 ROOT 수용은 최종 종료 수용과 별개입니다.

## 고정된 문제와 관찰 결과

source-pair-1 동결 (local retained evidence; not published)은 C (local retained evidence; not published), H (local retained evidence; not published), oracle (local retained evidence; not published), 방법 v2 (local retained evidence; not published)·v3 (local retained evidence; not published)를 묶습니다. 소스 검토 A (local retained evidence; not published)와 B (local retained evidence; not published)는 시행 전에 같은 동결본을 APPROVE했습니다. 이 승인은 수학·채점 기준의 타당성에 관한 것으로 경험적 어려움 승인이 아닙니다.

동률이면 A를 선택하며 사적 합의로 이를 바꿀 수 없다는 규칙은 시행 전 C/H에 명시되어 있었습니다. 기존 기록에서 이전액 차이 d=t_B-t_A에 따른 행동은 d≤1일 때 (A,A), 1<d≤2일 때 (B,A), d>2일 때 (B,B)입니다. 기대 합산효용은 각각 10, 7, 8입니다. 두 당사자의 참여 조건은 합산 기대효용 10 이상을 요구하므로, 상태와 독립적인 일정 추첨도 B를 유도하는 가지에 양의 확률을 둘 수 없습니다. 추첨의 각 가지가 별도로 수락되어야 한다고 가정하지 않습니다. 보장은 허용된 추첨에서 거의 확실한 A 보장입니다.

세 원본 모두 이 임계값·추첨 논증을 완전하게 제시하고 기존 기록 유지를 선택했습니다. 공개 감사 아래에서 (H,B)에만 R→P 이전액 3, 나머지 기록에 0을 지급하는 반례도 모두 제시했습니다. L에서는 A가 엄격히 우월하고 H에서는 B가 엄격히 우월하며, 실현 효용은 (5,5)/(6,6), 각 기대효용은 5.5입니다. 이 계약은 허용 범위와 참여 조건을 만족하면서 필수 A 보장을 깨므로 감사의 순진단가치 1로 승인할 수 없습니다. 행동 뒤 생성되는 기록도 행동 전 구속력 있는 지급 조건을 바꿀 수 있다는 구별이 공개 답변에 나타납니다.

H는 작성자와 소스 검토자가 보았지만 참가자·채점에는 사용하지 않았습니다. H에서는 사적 계약 집행에 접근할 수 없는 보고서가 지급 조건을 늘리지 않아 승인하는 것이 정답이나, 그 성능은 시험하지 않았습니다.

## 원본에서 판정까지의 연결

사전 동결 (local retained evidence; not published)과 실제 시작 인수 기록 (local retained evidence; not published)의 세 요청은 일치합니다. 요청은 fresh native gpt-6.1-sol / medium / fork_turns:none이며, reasoning effort는 선별 기준으로 사용하지 않았습니다. 원본 readback (local retained evidence; not published)의 각 중첩 도구 결과를 직접 파싱하여 완료·성공·잘림 없음, 허용된 단일 읽기와 정확한 입력 3434 bytes / SHA-256 934325edde26ed6bc22b3595929f3d5a62634c88f98e59a72142901d7350dcb1을 확인했습니다. 입력은 C와 전달용 지시이며, ROOT 전달 수용 (local retained evidence; not published)이 세 원본을 수용합니다.

중립 패킷 (local retained evidence; not published)은 C 전체와 원본 answer 문자열을 그대로 담습니다. 비공개 매핑 (local retained evidence; not published)은 R01=참가자2, R02=참가자3, R03=참가자1입니다. 준비 영수증 (local retained evidence; not published)의 source_bindings/artifacts를 실제 파일의 바이트·해시와 대조했습니다. 패킷은 조건·모델·출처·H 전용 내용 없이 C의 기준을 제공합니다.

채점 사전 기록 (local retained evidence; not published)에는 부모가 처음 response.text를 잘못 접근한 뒤 실제 스키마인 response.answer로 수정해 정확한 일치를 확인한 이력이 있습니다. 패킷 내용은 바꾸지 않았습니다. 두 FIRST 원본 (local retained evidence; not published)의 canonicalFinal JSON을 새로 파싱해 저장된 parsed 값과 완전히 일치함을 확인했습니다. 패킷 SHA-256은 e933107cb3613ce3acdb2771f6d25eeb5fbd7b8f02aaa88721a4a58aeb06fd34입니다.

| 응답 | FIRST A | FIRST B | 객관적 오류 A/B | 적격 실패 A/B |
|---|---:|---:|---|---|
| R01 | 10 | 10 | false / false | false / false |
| R02 | 10 | 10 | false / false | false / false |
| R03 | 10 | 10 | false / false | false / false |

두 채점 모두 다섯 항목 각 2점이며 공개 근거가 충분한 정답으로 판정했습니다. 같은 ID 최소 2개가 공동 적격이어야 하는 v2/v3 유지 조건을 충족하지 못합니다. 전원 적격에 따른 추가 유효성 검토 조건도 발생하지 않았습니다.

## 한계와 남은 작업

원본 3회, FIRST 2회 외 참가자 재시도·대체·후속 요청, 재채점, H 시행, neutral/control·스킬 비교·scored treatment는 0회입니다. 스킬 효과는 UNKNOWN입니다. 역사적 사례 재분류, 실제 controller 설치·출시 또는 Git·원격 작업은 수행하지 않았습니다.

공개 기록은 요청한 모델·노력·fresh context와 노출된 읽기·답변을 입증합니다. 최초 시작 메시지 원문은 조정자가 보존한 인수이며 암호화된 호스트 기록에서 독립 복호화한 것이 아닙니다. 실제 숨은 백엔드, 호스트 추가 문맥, 노출되지 않은 작업은 미확인입니다. 공유 파일시스템은 격리되어 있지 않으며 sterile host나 별도 CLI 자격을 주장하지 않습니다. 공개 최종 추천과 근거만 평가했고 숨은 사고·동기는 추정하지 않았습니다.

변경되지 않은 F149 capture.py(11300 bytes, SHA-256 df85e5939415d47e0f5c807a8e53400c8710c0f848a231b56cb57c65b0036887)를 F149→F153, f149→f153, 0149→0153의 선언된 런타임 치환으로 재사용했습니다. 동결·readback의 pending/checkpoint 필드는 당시 기록으로 보존되며 후속 수용·채점 문서가 그 이후 단계를 설명합니다. 응답과 채점은 기존 canonical 문자열만 사용하고 복제 출력 파일이나 새 스크립트는 만들지 않았습니다.

[상태](state.json), 검증 기록 (local retained evidence; not published), 파일 해시 목록 (local retained evidence; not published), 카탈로그 추가 초안 (local retained evidence; not published)을 제공합니다. 부모가 카탈로그를 바이트 단위로 추가하고 원래 접두부 보존을 확인해야 합니다. 최종 수용은 아직 주장하지 않습니다.
