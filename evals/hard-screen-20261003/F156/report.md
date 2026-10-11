# F156 — INCOMPLETE_PROTOCOL

F156의 유일한 원본 실행은 캡처 형식 검증에서 중단되어 `INCOMPLETE_PROTOCOL`로 기록한다. 난도 `UNKNOWN`, 채점 `NOT_RUN`, 유지 0/6이다. 독립 전달 감사 (local retained evidence; not published)는 이 종료를 승인했고 P0/P1 결함이 없었다. ROOT 최종 승인 전의 로컬 마감 후보이며, 답변의 정오나 실제 입력 전달 실패를 판정한 결과가 아니다.

원래 계획은 독립 에피소드 3개, 각각 예비·최종 단계 2턴으로 총 6턴이다. 실제 관측은 첫 단계 3턴과 예비 답변 3개이며 최종 단계 답변은 0개다. 세 참가자는 fresh native subagent에 `gpt-6.1-sol` / `medium` / `fork_turns:none`으로 요청되었다. 이는 요청값이고 실제 숨은 백엔드, 호스트 추가 문맥, 완전한 격리를 입증하지 않는다. 공유 파일시스템도 격리되지 않았다.

체크포인트 (local retained evidence; not published)에서 세 원본 모두 `INVALID_OR_INCOMPLETE`였다. 형식 진단 (local retained evidence; not published)은 `inspect_stage1`이 어댑터 197행에서 `turn_context`보다 앞선 미지원 record type `world_state`를 만나 거부했음을 보여준다. 같은 공개 형식 목록에는 추가 미지원 `inter_agent_communication_metadata`, `token_usage_record`, `event_msg/item_completed`도 있다. 이 거부는 캡처 계약의 runtime 형식 미지원이며, 참가자의 오답·도구 위반·실제 입력 미전달을 입증하지 않는다. 집계 readback (local retained evidence; not published)의 포괄적 실패 사유도 개인정보 유출이나 특정 전달 위반이 확인되었다는 뜻으로 확대하지 않는다.

사전에 동결한 규칙은 유효한 첫 단계 체크포인트 뒤에만 동일 참가자에게 고정된 두 번째 입력을 보내도록 했다. 따라서 두 번째 단계는 세 건 모두 **호출하지 않았다**. launches의 `followupSucceeded:false`는 호출 실패 3회가 아니라 미실행을 뜻한다. 예비 답변 내용에 따른 분기나 정답 피드백은 없으며 원본 재시도·대체·추가 문제 턴은 0회다. 원본 한 개라도 유효성을 입증하지 못하면 가족 전체를 미완료로 남기는 v2/v3 규칙을 적용한다.

원본 예비 답변 보존본 (local retained evidence; not published)에 세 답변의 정확한 문자열, 순서, UTF-8 바이트 수와 SHA-256을 보존했다. 첫 단계는 무해하고 비채점이며 이 자료는 `UNACCEPTED_NOT_GRADEABLE`이다. 최종 답변, 익명 채점 패킷, 독립 채점, 점수, 객관적 의사결정 오류 및 적격 inquiry failure 판정은 없다. H는 작성자·검토자가 보았지만 참가자에게 사용하지 않았다. 중립 검사·스킬 비교·점수 비교 처치는 모두 0회이며 스킬 효과는 UNKNOWN이다.

소스 `source-pair-2`는 독립 검토 A/B가 승인했다. 캡처 초기 검토 A/B의 결함을 수정한 revision 3은 검토 C에서 승인되었으며 45개 기존 합성 검사와 10개 별도 메모리 검사가 통과했다고 기록되어 있다. 이 실행 전 승인은 실제 호스트 형식 수용이나 참가자 전달 성공의 증거가 아니다. 동결 pretrial의 `captureReviewStatus`와 preparation 상태에는 검토 대기라는 과거 문구가 남아 있다. 이를 사후 수정하지 않고, 현재 revision 3과 그 pretrial 해시를 명시한 검토 C를 별도 바인딩한다. 이 기록 자체는 전체 실행 전 승인 시점의 독립 증명이 아니다.

[검증](verification.json)과 [manifest](manifest.json)는 현재 소스·동결본·방법론·pretrial·parser revision 3·검토·호출 기록·체크포인트·진단·원본 보존본을 바이트 수와 SHA-256으로 연결한다. 원본 세션 경로·식별자·이벤트 본문·암호화 내용·비공개 추론은 포함하지 않는다. 카탈로그는 부모가 기존 바이트 접두부를 보존하여 별도 append할 예정이며 루트 README는 변경하지 않는다. 과거 사례나 원본 소스·캡처·출력은 수정하지 않았고, 이 미완료 실행으로 난도나 가족 간 독립성을 결론내리지 않는다.
