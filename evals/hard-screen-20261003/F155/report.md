# F155 — 풀이 단서 제거 후 조건부 서비스 정책 선별

**EXCLUDED_NOT_HARD.** 유효한 원본 3개에 대한 두 독립 FIRST 채점은 R01/R02/R03 순서로 각각 **10/10/10**입니다. 만점 3/3, 객관적 결정 오류·적격 탐구 실패 각 0개, 공동 적격 ID 없음으로 유지 **0/6**입니다. 작성자 검증을 마친 종료 기록이며 카탈로그 적용, 부모 전체 확인, 새 독립 최종 감사와 ROOT 최종 수용은 대기 중입니다.

## 전향적 수정과 관찰

F155는 F154와 **같은 문제군의 전향적 개정**입니다. 설계 기록 (local retained evidence; not published)의 가설에 따라 C의 가중치 증명 안내, W별 검증이 없다는 명시적 단서와 특정 감사 요청을 제거하고 일반적인 서비스 계획 승인 요청으로 바꿨습니다. C는 3156→2719바이트로 **437바이트 감소**했습니다. 수치·비용·정책 선택지·식별 전제는 유지됩니다. 독립된 새 메커니즘으로 세지 않으며 F154의 원본·점수·판정도 바꾸지 않습니다. 단서 제거가 성공 또는 난이도에 미친 인과 효과는 이번 결과로 입증되지 않습니다.

source-pair-1 동결 (local retained evidence; not published)은 C (local retained evidence; not published), H (local retained evidence; not published), oracle (local retained evidence; not published), 방법 v2 (local retained evidence; not published)·v3 (local retained evidence; not published)를 묶습니다. 소스 검토 A (local retained evidence; not published)와 B (local retained evidence; not published)는 시행 전에 같은 소스를 APPROVE했습니다. 소스 타당성 승인이 경험적 어려움 승인은 아닙니다.

C에서 고정 행동의 전체 평균을 h로 검증한 사실은 W별 인과평균을 보장하지 않습니다. 별도로 주어진 일관성, U 조건부 독립성과 가중치 정규화로 E[1{A=a}q(Z,a)Yg(W)]=E[Y(a)g(W)]를 도출할 수 있습니다. 세 원본 모두 제거된 증명 안내 없이 이 식별 근거를 스스로 제시했습니다. 이는 관측된 보정식 적합만으로 잠재 전제를 추론한 것이 아닙니다.

가중 성공 질량은 무서비스에서 W 양쪽 모두 1/5, 서비스에서는 7/40과 9/40입니다. P(W=w)=1/2이므로 서비스 성공률은 7/20과 9/20이며 비용 차감 증분은 −3/20과 −1/20입니다. 세 원본 모두 임의 서비스 확률 r0,r1∈[0,1]에 대해 **2/5−3r0/40−r1/40**을 도출했습니다. 따라서 최적은 **무서비스, 2/5**입니다. 메모의 W=1만 서비스하는 제안은 실제 **3/8**로 1/40 열등하며, 메모의 9/20은 C에서 정당화되지 않은 h 대입값입니다.

H는 별도 무작위 검증 모집단으로 W별 인과평균을 직접 식별합니다. H의 값은 2/5−3r0/20+r1/20이며 최적은 W=1만 서비스, **9/20**입니다. H는 작성자·소스 검토자가 보았지만 참가자 시행과 채점에 사용되지 않았습니다.

## 원본·패킷·채점 연결

사전 동결 (local retained evidence; not published)과 실제 시작 인수 (local retained evidence; not published)의 세 요청은 일치합니다. 요청은 fresh native gpt-6.1-sol / medium / fork_turns:none입니다. 원본 readback (local retained evidence; not published)의 중첩 도구 결과를 직접 파싱해 각 원본의 단일 허용 읽기, 완료·성공, 정확한 입력 **2930 bytes / SHA-256 cbac4e8017786dfe9a6377d7c3681a244637011e368baece24efe87ae8989617**를 확인했습니다. 입력은 C 전체와 전달 지시입니다. ROOT 전달 수용 (local retained evidence; not published)은 세 원본을 FIRST 채점에 수용한 기록이며 최종 종료 수용과는 별개입니다.

중립 패킷 (local retained evidence; not published)은 C 전체와 세 canonical answer 문자열을 그대로 담습니다. 비공개 매핑 (local retained evidence; not published)은 R01=참가자2, R02=참가자3, R03=참가자1입니다. 준비 영수증 (local retained evidence; not published)의 패킷·매핑 바인딩과 후보·모델·조건·계보·H 전용 표시 제외를 확인했습니다. 패킷은 **19148 bytes / SHA-256 4267434ec4bf16890c7fbb9881d61462038954296aa186c0886b64002dad6553**입니다.

채점 사전 기록 (local retained evidence; not published)과 두 FIRST 원본 (local retained evidence; not published)을 대조하고 canonicalFinal JSON을 새로 파싱해 저장된 parsed 값과 일치함을 확인했습니다. 원본 답변·채점 전문을 새 파일에 복제하지 않고 기존 canonical 문자열의 바이트·해시에 연결합니다.

| 응답 | FIRST A | FIRST B | 객관적 오류 A/B | 적격 실패 A/B |
|---|---:|---:|---|---|
| R01 | 10 | 10 | false / false | false / false |
| R02 | 10 | 10 | false / false | false / false |
| R03 | 10 | 10 | false / false | false / false |

각 채점의 다섯 항목이 모두 2점입니다. 최소 두 동일 ID의 공동 적격 실패라는 유지 조건을 충족하지 못했고, 전원 적격에 따른 추가 유효성 검토 조건도 발생하지 않았습니다. 공개 최종 추천과 근거만 평가하며 숨은 사고·동기를 추정하지 않습니다.

준비 영수증은 루트 AGENTS.md 부재 확인, 결합 출력 잘림, 첫 집계 JSON의 Unexpected end of JSON input 실패와 작은 범위 재읽기를 통한 복구를 보존합니다. 패킷 작성 전에 복구했고 최종 준비 검사는 통과했습니다. 이는 참가자 재시도나 시행 무효가 아닙니다. 준비자의 Biome LSP 부재는 Node JSON 검증으로 보완됐고 설치는 하지 않았습니다. 이번 작성자의 최초 exec_command도 helper setup 오류로 시작하지 못했으며 이후 읽기·검사는 Git Bash로 수행했습니다. 큰 표시 출력은 잘려서 완전한 근거로 사용하지 않았고 작은 구조화 읽기와 정확한 문자열·해시 검사로 확인했습니다.

## 범위와 한계

원본 **3회**, FIRST **2회**이며 재시도·대체·참가자 후속 요청·재채점·H 시행·neutral/control·스킬 비교·scored treatment는 **0회**입니다. 스킬 효과는 UNKNOWN입니다. Git·원격 작업이나 역사적 재분류, controller 설치·출시는 수행하지 않았습니다.

요청 모델·노력·fresh context와 노출된 읽기·답변은 기록에 연결됩니다. 시작 인수는 조정자가 보존한 값이며 호스트 암호화 기록에서 독립 복호화한 평문은 아닙니다. 실제 숨은 백엔드, 호스트 추가 문맥, 노출되지 않은 작업은 미확인입니다. 공유 파일시스템은 격리되지 않으며 sterile host나 별도 CLI 자격을 주장하지 않습니다. 노력 수준은 선별 기준으로 사용하지 않았습니다.

변경되지 않은 F149 capture.py (local retained evidence; not published)(11300 bytes, SHA-256 df85e5939415d47e0f5c807a8e53400c8710c0f848a231b56cb57c65b0036887)를 F149→F155, f149→f155, 0149→0155의 선언된 런타임 치환으로 재사용했습니다. 동결·readback의 pending 필드는 당시 단계 기록이며 후속 수용·채점 문서와 함께 읽어야 합니다.

부모가 지정한 유일한 다음 후보 **F156**은 **두 단계 전향적 증거 갱신 설계**로 아직 참가자에게 전달하지 않았습니다. 그 구성과 시행은 이번 종료 작성 범위 밖입니다.

[상태](state.json), 검증 기록 (local retained evidence; not published), 해시 목록 (local retained evidence; not published), 카탈로그 추가 초안 (local retained evidence; not published)을 제공합니다. 카탈로그 적용 전 기준은 **113560 bytes / SHA-256 543f8e9c8625f1cb2b1d61a5ebc195412666fc773c97328dd38ba4d2f41a3b7f**이며 작성자는 카탈로그를 수정하지 않았습니다. 부모의 추가 적용·기존 접두부 보존 확인·독립 최종 감사·ROOT 수용은 남아 있습니다.
