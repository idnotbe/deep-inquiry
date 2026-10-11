# F154 — 평균 보정 검증과 조건부 서비스 대상 선정

**EXCLUDED_NOT_HARD.** 유효한 원본 답변 3개에 대한 두 독립 FIRST 채점은 R01/R02/R03 순서로 모두 **10/10/10**입니다. 만점 3/3, 객관적 결정 오류 0개, 적격 탐구 실패 0개이며 공동 적격 ID는 없습니다. 유지된 어려운 문제군은 **0/6**입니다. 이번 선별에서 제외되었으며, 문제군의 본질적 난이도나 스킬 효과를 입증하지 않습니다.

작성자 검증을 마친 종료 기록입니다. 카탈로그 적용, 부모 전체 확인, 새 독립 최종 감사와 ROOT 최종 수용은 아직 남아 있습니다. 원본 입력 전달에 대한 ROOT 수용은 최종 종료 수용과 별개입니다.

## 고정된 문제와 관찰 결과

source-pair-1 동결 (local retained evidence; not published)은 C (local retained evidence; not published), H (local retained evidence; not published), oracle (local retained evidence; not published), 방법 v2 (local retained evidence; not published)·v3 (local retained evidence; not published)를 묶습니다. 소스 검토 A (local retained evidence; not published)와 B (local retained evidence; not published)는 시행 전 같은 동결본을 APPROVE했습니다. 이 승인은 소스와 채점 기준의 타당성에 관한 것이며 경험적 어려움 승인이 아닙니다.

C에서 h는 두 고정 행동의 전체 인과평균 2/5를 재현하지만, 그 사실은 h(w,a)가 W별 인과평균이라는 보장이 아닙니다. 메모의 h 대입 산술은 맞지만 그 값을 대상 선정 정책의 인과적 가치로 옮기는 단계가 성립하지 않습니다. 별도로 명시된 잠재 상태 U의 조건부 독립성과 가중치 조건은 E[1{A=a}q(Z,a)Yg(W)]=E[Y(a)g(W)]를 보장합니다. 세 원본 모두 이 논증을 제시하고 W별 값을 계산했습니다. 관측된 보정식의 적합만으로 잠재 조건을 추론한 것이 아닙니다.

가중 합으로 얻은 E[Y(a)1{W=w}]는 무서비스에서 양쪽 W 모두 1/5, 서비스에서 W=0은 7/40, W=1은 9/40입니다. 각 W의 확률은 1/2이므로 서비스의 조건부 성공률은 7/20과 9/20, 비용 1/10을 뺀 증분은 −3/20과 −1/20입니다. 따라서 임의의 서비스 확률 r0,r1∈[0,1]에 대해 순가치는 **2/5−3r0/40−r1/40**입니다. 세 답변 모두 무작위 정책까지 포함하여 **무서비스, 순가치 2/5**를 선택했습니다. 메모의 W=1만 서비스하는 정책은 실제 순가치 **3/8**로 1/40만큼 낮습니다. 메모의 9/20은 C의 실제 정책 가치가 아닙니다.

H는 별도 무작위 검증 모집단이며 h(w,a)를 W별 인과평균으로 직접 검증합니다. H에서는 순가치 2/5−3r0/20+r1/20, W=1만 서비스하는 정책과 9/20이 정답입니다. H는 작성자·소스 검토자가 보았지만 참가자 시행과 채점에는 사용하지 않았으며, 그 성능은 시험하지 않았습니다.

## 원본에서 판정까지의 연결

사전 동결 (local retained evidence; not published)과 실제 시작 인수 기록 (local retained evidence; not published)의 세 요청은 일치합니다. 요청은 fresh native gpt-6.1-sol / medium / fork_turns:none이며 reasoning effort는 선별 기준으로 사용하지 않았습니다. 원본 readback (local retained evidence; not published)의 중첩 도구 결과를 직접 파싱하여 세 원본 각각 완료·성공, 허용된 단일 읽기와 정확한 입력 **3367 bytes / SHA-256 04fe081fc00802907571534f1c01a7a8be327979f15c5cc625d8c8c608464b6a**를 확인했습니다. 입력은 C 전체와 전달용 지시이며, ROOT 전달 수용 (local retained evidence; not published)이 세 원본을 수용합니다.

중립 패킷 (local retained evidence; not published)은 C 전체와 원본 answer 문자열을 그대로 담습니다. 비공개 매핑 (local retained evidence; not published)은 R01=참가자2, R02=참가자3, R03=참가자1입니다. 준비 영수증 (local retained evidence; not published)의 source_bindings/artifacts를 실제 바이트·해시와 대조했습니다. 패킷의 C 근거·실패 기준·루브릭과 v2/v3 제외 규정을 읽었으며 후보·모델·조건·출처 표시와 H 전용 내용이 없는지 확인했습니다. 패킷 SHA-256은 **10aead057b7d79b9883ad8d008fb54f1bb56046a9bcb419f452ce6f5a04bc891**입니다.

채점 사전 기록 (local retained evidence; not published)은 원본과 패킷의 정확한 일치 및 기준 검토를 보존합니다. 두 FIRST 원본 (local retained evidence; not published)의 canonicalFinal JSON을 새로 파싱하여 저장된 parsed 값과 정확히 일치함을 확인했습니다. 원본 답변과 채점 전문은 해당 canonical 문자열에 연결하며 별도 복제 파일을 만들지 않았습니다.

| 응답 | FIRST A | FIRST B | 객관적 오류 A/B | 적격 실패 A/B |
|---|---:|---:|---|---|
| R01 | 10 | 10 | false / false | false / false |
| R02 | 10 | 10 | false / false | false / false |
| R03 | 10 | 10 | false / false | false / false |

두 채점은 다섯 항목 각 2점이며 정답·가치·식별 근거·검증 범위·무작위 정책 포괄을 모두 충족한다고 판정했습니다. 같은 ID 최소 2개가 공동 적격이어야 하는 유지 조건을 충족하지 못합니다. 전원 적격에 따른 추가 유효성 검토 조건도 발생하지 않았습니다.

준비 영수증에는 넓은 상위 경로 검색의 시간 초과, 실행 전 Python SyntaxError, 일반 규정의 actual action history를 출처 표시로 잘못 잡은 뒤 review history로 좁힌 검사 수정이 남아 있습니다. 이는 준비 단계 검사 이력이며 소스·패킷 변경, 참가자 재시도 또는 시행 무효를 뜻하지 않습니다. 최종 준비 검사는 통과했습니다.

## 한계와 남은 작업

원본 3회, FIRST 2회 외 참가자 재시도·대체·후속 요청, 재채점, H 시행, neutral/control·스킬 비교·scored treatment는 0회입니다. 스킬 효과는 UNKNOWN입니다. 역사적 사례 재분류, controller 설치·출시 또는 Git·원격 작업은 수행하지 않았습니다.

공개 기록은 요청 모델·노력·fresh context와 노출된 읽기·답변을 입증합니다. 최초 시작 메시지는 조정자가 보존한 인수이며 호스트 기록에서 독립 복호화한 평문이 아닙니다. 실제 숨은 백엔드, 호스트 추가 문맥과 노출되지 않은 작업은 미확인입니다. 공유 파일시스템은 격리되어 있지 않으며 sterile host나 별도 CLI 자격을 주장하지 않습니다. 공개 최종 추천과 근거만 평가했고 숨은 사고·동기는 추정하지 않았습니다.

변경되지 않은 F149 capture.py (local retained evidence; not published)(11300 bytes, SHA-256 df85e5939415d47e0f5c807a8e53400c8710c0f848a231b56cb57c65b0036887)를 F149→F154, f149→f154, 0149→0154의 선언된 런타임 치환으로 재사용했습니다. 동결·readback의 pending/checkpoint 필드는 당시 기록으로 보존하며 후속 수용·채점 문서가 이후 단계를 설명합니다.

부모가 지정한 유일한 다음 후보 F155는 **F154와 같은 문제군의 전향적 단서 제거 개정**입니다. 독립된 새 문제군으로 세지 않으며 F154의 원본·점수·제외 결과를 바꾸지 않습니다. 이 종료 작성에서는 F155 구성이나 시행을 수행하지 않았습니다. 안내 문구가 현재 성공의 원인이라는 인과적 결론도 내리지 않습니다.

[상태](state.json), 검증 기록 (local retained evidence; not published), 파일 해시 목록 (local retained evidence; not published), 카탈로그 추가 초안 (local retained evidence; not published)을 제공합니다. 카탈로그는 적용 전 **112314 bytes / SHA-256 b9b23c90c9df20f1050a215bad2be800bd0601512d4d9d850ed0cbbfa583c13b** 그대로입니다. 부모가 바이트 추가와 기존 접두부 보존을 확인해야 하며 최종 수용은 아직 주장하지 않습니다.
