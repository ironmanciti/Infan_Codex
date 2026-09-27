# Job Portal — FastAPI 실습 프로젝트

코덱스 강의에서 사용하는 실습용 구인·구직 포털입니다.
백엔드는 FastAPI + SQLite, 화면은 Jinja2 템플릿으로 구성되어 있으며,
첫 실행 시 회사 50곳과 채용 공고 1,000건이 자동으로 시드됩니다.

## 로컬 환경 설정

1. **Python 확인**: `python --version` (3.11 이상 권장)
2. **패키지 설치**: `pip install -r requirements.txt`
3. **앱 실행**: `uvicorn main:app --reload`
4. **접속**: http://127.0.0.1:8000 (API 문서: /docs)
5. **종료**: 터미널에서 Ctrl + C

DB를 초기화하고 싶으면 `jobportal.db` 파일을 삭제 후 재실행하세요.

## 데모 계정 (Demo Credentials)

| 역할 | 이메일 | 비밀번호 |
| --- | --- | --- |
| 관리자 (Admin) | admin@demo.com | admin123 |
| 고용주 (Employer) | employer@demo.com | employer123 |
| 구직자 (Job Seeker) | seeker@demo.com | seeker123 |

- **관리자**: 회사 관리, 문의 메시지 확인, 고용주 권한 부여
- **고용주**: 회사 대표로 채용 공고 등록·관리
- **구직자**: 프로필 완성, 공고 지원(Apply)·저장(Save)

## 참고

구직자 계정으로 앱을 둘러보면 몇 가지 이상한 점을 발견할 수 있습니다.
이 결함들은 강의에서 코덱스로 직접 분석하고 해결해 보기 위해 의도적으로
남겨 둔 것입니다. 미리 고치지 말고 강의 순서를 따라 주세요!

## 코덱스 실습 자료

이 폴더를 작업 디렉터리로 열면 `AGENTS.md`의 프로젝트 지침을 사용할 수 있습니다.
기능 추적과 이슈 분석 스킬은 `.agents/skills/`에, 읽기 전용 검토 에이전트는 `.codex/agents/`에 있습니다.
`.codex/hooks.json`은 패치의 비밀값 검사와 Python 파일 길이 경고 예제입니다. 프로젝트와 훅을 신뢰한 환경에서 활성화되며, 패치 이외의 파일 변경 경로까지 검사하는 보안 장치는 아닙니다.
강사용 결함 설명은 `INSTRUCTOR_NOTES.md`에 있으므로 수강생 배포본에서는 제외하세요.
