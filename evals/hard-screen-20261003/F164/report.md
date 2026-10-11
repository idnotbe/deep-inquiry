# F164 — INCOMPLETE_PROTOCOL

2026-10-11 · F164_SOURCE_V2 · closure-1 · issue #15.

r3는 동결한 최초 제출 요청에서 쉼표 뒤 공백 하나가 삭제되어 INVALID다. 부모가 실제로 보낸 요청은 1177자에서 1176자로 바뀌었고 최초 차이는 index 1058이다. 다른 인자는 일치한다. 알려진 실제 제출 변경이며 표시 형식 차이로 면제하지 않는다. 독립 계약 검토 f164-submission-contract-review.md와 부모 f164-validity-disposition.md가 이 판정을 뒷받침한다. r1/r2는 전체 의미 감사가 완료되지 않아 UNVERIFIED이며, 유효하거나 무효라고 추정하지 않는다.

세 원본이 모두 VALID여야 하는 채점 조건을 충족할 수 없어 INCOMPLETE_PROTOCOL로 기록한다. 전체 의미 감사는 확인된 r3 위반을 치유하지 못하므로 의도적으로 실행하지 않았다. 세 원본 답안은 채점하지 않은 상태로 보존한다. 익명 패킷 작성·채점·점수·난도 판정은 없다. 유지 증가 0, 누계 0/6으로 전체 목표는 미완료다. 답안에 보이는 내용으로 정답 여부나 EXCLUDED_NOT_HARD를 추정하지 않는다. 스킬 효과는 UNKNOWN_NO_COMPARISON이다.

| 원본 | 상태 | 전체 원본 기록 | 공개 사본 | 최종 본문 바이트 |
|---|---|---:|---:|---:|
| r1 | UNVERIFIED | 23 | 8 | 2615 |
| r2 | UNVERIFIED | 22 | 8 | 2604 |
| r3 | INVALID | 22 | 8 | 2690 |

67개 원본 기록 목록은 수집 manifest의 실제 수다. 공개 사본은 총 24개다. 각 슬롯의 8개 사본은 호출, 중첩 호출, 중첩 관측, 수신 관측, 최종 표시 사본, 최종 본문, 완료 사본, 부모 전달 본문이다. 중첩 호출과 관측은 같은 원본 기록에서 나오므로 각 슬롯의 서로 다른 자식 공개 기록 번호는 6개다. 부모 본문 하나를 더한 공개 기록 발생 수는 각 7개, 총 21개다. 이는 수집 자료에서 계산한 수이며 과거 후보의 수를 가정하지 않는다.

원본 실행·문제 턴·최종 답안은 각각 3개다. 재시도·대체·후속 요청·추가 문제 턴·채점자·H 참가자 사용·중립 비교·스킬 비교·처치는 모두 0이다. H는 원문 작성 및 검토 범위였고 참가자 실행에 쓰이지 않았다. 요청은 native implementation-worker, gpt-6.1-sol, medium, fork none이며 수집 보고의 관측 설정과 일치한다. 노력 설정은 난도 근거가 아니다.

수집 보고는 세 번의 유일한 실행 연결, 각각 한 번의 허용된 입력 읽기, 중첩 인자의 정확한 일치, C 7774바이트/SHA-256 7de1fba3c394798196296cbecdcd747d23135a9c015347ae62bf052b9573cbec의 정확한 수신을 기록한다. 모든 실제 wrapper는 동결된 448바이트에 LF 하나가 더해진 449바이트다. 이 LF의 나머지 유효성 영향은 UNADJUDICATED이며 의미상 허용됐다고 주장하지 않는다. 부모 전달 envelope는 메타데이터 때문에 최종 본문과 다르지만 그 Payload는 정확히 일치한다. 자식 고정 범위는 변화 0이고 부모 고정 범위도 일치한다. 부모 파일의 후속 82474바이트에는 cutoff까지 기록 및 대상 활동이 0이라는 수집 안정성 보고를 보존한다. 이 종료 작업은 원시 로그를 다시 감사하지 않았다.

## 보존한 통과와 일탈

Source V1 검토 A는 APPROVE와 P2 한 건, B는 APPROVE였다. V2는 Audit의 필요성을 과장한 문구를 좁히고 같은 시도 재사용 대안을 명시했으며 새 검토 A/B 모두 APPROVE, P0/P1/P2 없음이다. V1 10개 payload와 원래 freeze, V2 22개 payload, 원문 권한 15개를 보존한다. 원문 유효성 승인은 참가자 유효성이나 난도 증거가 아니다. 기존 문제와의 겹침 및 쉬운 합법적 대안도 그대로다.

준비 검사 108개 binding PASS, 부모 사전 검사 61/61 PASS, 독립 preflight의 61개 파일/84개 binding 및 최종 68개 파일 안정성 PASS를 보존한다. 작성자와 preflight의 C 읽기는 각각 한 번의 비참가자 전달 검사였다. 원래 preparation/pretrial/rootchecks의 대기·NOT_RUN 표시는 당시 기록이며 수정하지 않는다. 별도 dispatch acceptance는 실행만 허용했고 원본 유효성을 승인하지 않았다.

- r3_initial_request_space_deletion: 부모의 실제 제출 오타와 독립 INVALID 판정을 유지한다. 원본 수정·재시도·대체·면제는 없다.
- collector_unnecessary_filename_output: 수집자가 승인된 날짜 폴더의 불필요한 파일명 목록을 도구 출력에 내보낸 개인정보 최소화 일탈을 유지한다. 기록 파일에 경로나 원시 식별자를 다시 싣지 않으며 깨끗한 수집이라고 주장하지 않는다. 디렉터리 목록은 본문 읽기가 아니고 header 128개 및 일치한 세 자식/유일 부모의 제한된 본문 범위는 보존됐다.
- reviewer_embedded_oracle_paragraph_exposure: 계약 검토자가 pretrial의 관련 부분 출력 중 sourceV2Delta에 포함된 oracle-C 수정 문단을 실수로 표시했다. 실제 참가자 답안이나 별도 채점 자료는 읽지 않았으며 해당 문단은 바이트·계약 판정에 쓰지 않았다는 검토 범위를 보존한다. 깨끗한 no-oracle 검토로 바꾸지 않는다.
- all_wrappers_plus_LF_unadjudicated: 모든 wrapper의 추가 LF와 미판정 상태를 보존한다.
- failed_rehearsal_A_preserved / baseline_B_P2_preserved: 과거 rehearsal A FAIL과 B PASS의 P2 경로 출력 일탈을 지우지 않는다. 기존 공통 의미 검토는 조건부 재사용일 뿐 F164 전체 의미 감사 완료가 아니다.
- collector_setup_and_syntax_errors_preserved: 수집자의 실행 초기화 실패와 무변경 Node 구문 오류를 보존한다. 이를 새 깨끗한 감사로 덮지 않는다.

## 종료 검사와 한계

manifest.json은 75개 기존 입력의 바이트와 SHA-256을 묶는다. check.mjs는 동결 입력, 실제 제출 차이, 원본 기록 수, 공개 사본별 hash, 정확한 C 수신·사본·최종 본문, 안정성 보고, 미완료 상태와 보존 이력, 카탈로그 prefix/suffix를 검사한다. behavior-tests.mjs는 잘못된 VALID·채점·유지 주장과 누락 이력, 변형된 공개 사본·안정성 보고·카탈로그를 검사기에 주입한다. 실제 결과는 verification.json과 closure/behavior-verification.json, 후보 묶음은 closure/candidate.json에 둔다. 원시 로그나 새로운 의미 감사를 수행하지 않는 검사다.

카탈로그 기존 123674바이트 SHA-256 165814d569efa0a4af70762a6556725c581f9e5255f3e27164a33f2a059116b2를 확인한 뒤 fs.appendFile 한 번으로 동결 조각만 붙인다. 혼합 줄바꿈의 기존 prefix와 새 suffix를 바이트로 확인한다.

초기 보호 평문은 부모/native API 신뢰 가정이다. 실제 backend/fallback, 내부 bootstrap, 완전한 내부 격리는 미확인이고 공유 파일시스템은 격리되지 않는다. 해시·기록 목록·수집된 설정만으로 VALID, 무지침 모델, 인과적 스킬 효과를 주장하지 않는다. known r3 위반은 미확인 항목과 별개의 결정적인 계약 위반이다.

종료 작성 중 첫 광범위 임시 폴더 목록 조회는 다른 폴더의 접근 거절로 중단됐고 원시 본문을 열지 않았다. 이후 정확히 지정된 경로만 사용했다. 자동 편집기 진단은 biome이 없어 실행되지 않았으며 범위 밖 설치·전역 설정 변경은 하지 않았다. Node 검사로 이 후보를 확인한다. Git·이슈·네트워크·기억·새 참가자·채점자·다른 에이전트 작업은 수행하지 않았다.

PENDING_ROOT_FULLCHECK_AND_FRESH_REVIEW: 이 후보의 부모 최종 전체 검사와 새 독립 검토는 별도 수락에서 처리한다. 이 문서는 최종 수락을 대신하지 않는다.
