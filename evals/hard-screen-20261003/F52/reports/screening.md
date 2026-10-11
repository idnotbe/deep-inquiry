# F52 — EXCLUDED

원래 F52C 세 응답은 모두 유효하게 완료됐고, 최초 독립 채점 양쪽10·10·10·객관적 결정 오류0개·적격 실패0개다. 동일 적격 응답 최소2개 조건을 충족하지 못해 EXCLUDED이며 확보는0/6개로 목표가 아직 미완료다. 이는 이번 문항이 선별 기준을 통과하지 못했다는 결과이지 스킬 효과 비교가 아니다.

세 응답은 추첨 전 North 필수 보고 PRIVATE 비용1·South 필수 보고 PUBLIC 비용0·추가 공개 없음·기존 동시 latch·기존 정산을 등록했다. South VALID에서 solo/series 각1/2라 수리 기대 순익이 최소1/2로 엄격히 양수이며, 실제 두 보고를 아는 North는 South의 해당 정보와 엄격한 합리적 응답을 알고 series에서 수리한다. North의 series 선택은 임의 상대 전략에 대한 무조건 우월성이 아니라 순차적인 최적응답 추론이다. 모두 모든 지원 상태·합리적 응답·실현 seed에서 출고를 보장하고 비용1로 잘못된 최소2 승인 거절을 바로잡았다. 상대가 알고 있다는 사실만으로 거절이 계속된다는 오류는 관찰되지 않았다.

원래 응답 (local retained evidence; not published)은 실제 terminal 문자열을 UTF8 해시와 바이트 동일하게 보존했다. 첫 채점 원문과 조회 (local retained evidence; not published)는 두 NEW fork-none 익명 packet-only 검토자의 완전한 첫 보고를 포함한다. 원문을 UTF8/LF로 전사한 로컬 해시와 원시 전달 인증은 구분한다. 재채점·평균·유리한 결과 선택·추가 채점자는 없으며 사후 타당성 audit도 all3 적격 조건이 아니어서 필요하지 않다.

처음 READY 중립 baseline의 `turn_completion / contract_rejected` 실패는 그대로 남아 있다. 당시 보고 (local retained evidence; not published), 상태 (local retained evidence; not published), 증거 (local retained evidence; not published)를 현재 갱신 전에 바이트 그대로 보존했다. 첫 실패의 실제 모델 실행·완료와 retry flag/실제 원인은 UNKNOWN이다. 별도 source 수준에서 확인한 explicit retryable error 처리 결함 수정은 원래 runner 담당자가 작성했고 두 독립 코드 검토를 거쳤다. 현재 성공을 과거 실패 원인의 증명으로 옮기지 않았다.

변경 runner를 고정한 별도 prospective READY health baseline/treatment는 각1턴·최종READY와 실제 input/LF0a0aCOMMON·문맥·baseline root 없음/refs0·treatment root+3refs·무도구·소스 보존·프로세스·복사 인증 정리를 통과했다. 이 별도 중립2턴은 문제 집계에서 제외하며 이전 실패의 복구·대체·재시도로 표시하지 않는다. 이후 새 원래 런타임 freeze와 actual common reference·계획을 문제 출력 전에 결합했다. FIRST C r2/r3/r1 attempt1은 각1턴·terminal1개이며 전체 입력·문맥·스킬 미노출·무도구·소스·정리가 참이다. 소유 Python28104/Node27812를 GO 전에 기록하고 같은 실행 cell262에서 종료0을 확인했다. PID/종료만으로 다른 안전 검증을 대신하지 않았다.

원자료 두 독립 복원 이후 같은 두 독립 검토자가 FULL 자료를 병렬 검토했으며 네 명의 새 검토자로 표시하지 않았다. 원래 both-private 비용2 자료는 현재 budget1에 불법인 역사적 witness로 보존했고 현재 refinement가 실제 비대칭 비용1을 다룬다. H는 실제 North 먼저 실행 후 South 관측·순차 합리성, K는 현재 singleton 상태만 있는 구조다. H/K는 작성자·검토자는 보았지만 모델 확인 실행에 쓰지 않은 미사용 문항이다. scored treatment·스킬 수정·푸시는 없다.

확인된 누적 하한은47개 시도 문제군·보존 최종136개·완료 문제 턴 캡처192개다. F46 실제 기여와 F51 실제 모델 실행·완료는 미확인으로 그대로다. 이전 F41/F46/F51 원본·설정은 변경하지 않았다. 요청 gpt-6-sol과 실제 backend 증명을 구분하며 추론 수준은 판단·중단의 고려 사항이 아니다. [현재 상태](original-status.json)와 [증거 연결](evidence.json)은 역사적 실패·현재 health·최초 문제 실행·최초 채점을 분리한다. F32 이후 최종 두 successive 독립 산출물 검토·Git 보관은 전체 자료 안정 뒤로 유보 상태다.
