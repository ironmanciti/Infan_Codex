# 채용 포털 실습 지침

이 파일은 코덱스가 채용 포털 실습에서 작업할 때 따라야 할 지침입니다.

## 명령어

- `uvicorn main:app --reload` — 개발 서버 실행 (http://127.0.0.1:8000)
- `pip install -r requirements.txt` — 의존성 설치
- `pytest` — 테스트 실행
- `ruff check .` — 린트 / `ruff format` — 포맷팅

## 저장소 구조

```text
jobportal-codex/
├── main.py               # 앱 조립: 라우터 등록, lifespan(스키마+시드)
├── app/
│   ├── core/             # 인프라: db, auth(세션·역할), seed, templating
│   ├── routers/          # HTTP 라우트 (권한 검사 + 렌더링만)
│   └── services/         # 비즈니스 로직 + 모든 DB 접근
├── templates/            # Jinja2 (base.html 상속, partials/, admin/)
├── static/               # css/style.css (CSS 변수·다크모드), js/main.js
└── jobportal.db          # SQLite (첫 실행 시 자동 생성·시드)
```

## 데모 계정

admin@demo.com/admin123 · employer@demo.com/employer123 · seeker@demo.com/seeker123

## 아키텍처

FastAPI 기반 서버 렌더링 웹 애플리케이션이며, Jinja2 템플릿과 SQLite를 사용합니다.
프론트엔드 프레임워크는 사용하지 않고 순수 CSS와 최소한의 JavaScript만 사용합니다.

### 기술 스택

| 계층 | 기술 |
| --- | --- |
| 웹 프레임워크 | FastAPI |
| 템플릿 | Jinja2 (서버 렌더링) |
| 데이터 | SQLite (WAL 모드, 표준 라이브러리 sqlite3) |
| 시드 데이터 | Faker (첫 실행 시 자동 생성) |
| 스타일 | 순수 CSS (static/css/style.css, CSS 변수 기반 다크 모드) |
| 실행 | uvicorn |

### 계층 구조

세 개의 계층으로 구분하며, 역할을 혼합하지 않습니다.

- **`app/routers/`** — HTTP 라우트. 요청 파싱, 권한 검사, 템플릿 렌더링만 담당
- **`app/services/`** — 비즈니스 로직과 모든 데이터베이스 접근
- **`app/core/`** — 인프라: DB 연결(db.py), 인증(auth.py), 시드(seed.py), 템플릿 설정(templating.py)

라우터에서 SQL을 직접 실행하지 마세요. 데이터 접근은 반드시 services 계층을 거칩니다.

### 작업별 파일 위치

| 작업 | 위치 |
| --- | --- |
| 새 페이지 추가 | `app/routers/`에 라우트 추가 + `templates/`에 템플릿 추가 + `main.py`에 라우터 등록 |
| 공통 레이아웃 수정 | `templates/base.html`, `templates/partials/` |
| 인증 로직 | `app/core/auth.py` |
| 채용공고 / 지원 로직 | `app/services/job_service.py`, `app/services/misc_services.py` |
| 프로필 로직 | `app/services/profile_service.py` |
| 스키마 변경 | `app/core/db.py` (SCHEMA) |
| 시드 데이터 수정 | `app/core/seed.py` |

## 코딩 표준

### 언어 및 구조

- Python 3.11+ 기준으로 작성하며 PEP 8을 따릅니다.
- 함수 시그니처에는 타입 힌트 사용을 권장합니다.
- 모든 모듈 첫 줄에 한 줄 docstring을 작성합니다.
- 새 Python 파일은 가능한 500줄 이하로 유지합니다. `.codex/hooks/line_limit.py`는 패치 후 초과 파일을 경고합니다.

### 네이밍 규칙

- 함수·변수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- 템플릿 파일: `snake_case.html`

### 템플릿과 스타일

- 모든 페이지 템플릿은 `base.html`을 extends 합니다.
- 스타일은 `static/css/style.css`의 CSS 변수(`var(--...)`)만 사용합니다. inline style 금지.
- 다크 모드는 `html[data-theme]` 속성 전환 방식입니다. 새 색상은 반드시 라이트/다크 두 팔레트에 추가하세요.

### 린트

- `ruff check .`로 검사하고 `ruff format`으로 포맷팅합니다.

## 데이터 계층 규칙

### 서비스 계층 원칙

- 모든 데이터베이스 접근은 `app/services/`의 서비스 함수를 통해서만 수행합니다.
- 라우터는 서비스 함수를 호출할 뿐, SQL을 직접 실행하지 않습니다.
- 서비스 함수는 sqlite3.Row(또는 그 리스트)를 반환하고, 표현(포맷팅)은 템플릿에 맡깁니다.

### SQLite 사용 규칙

- 연결은 항상 `app/core/db.py`의 `get_db()`로 얻습니다 (WAL 모드·row_factory 설정 포함).
- 연결은 `try/finally`로 반드시 `conn.close()` 합니다.
- SQL 값 삽입은 **반드시 파라미터 바인딩(`?`)**을 사용합니다. f-string으로 값을 조립하지 마세요 (SQL 인젝션 방지).
- 쓰기 작업 후에는 `conn.commit()`을 잊지 마세요.

### 스키마 변경

- 테이블 추가·변경은 `app/core/db.py`의 SCHEMA 문자열에서만 수행합니다.
- 시드 데이터가 필요한 변경이면 `app/core/seed.py`도 함께 갱신합니다.
- 개발 중 스키마가 바뀌면 `jobportal.db` 파일을 삭제하고 재실행하면 재생성됩니다.

## 라우팅 및 역할 규칙

### 역할 정의

총 3개의 역할이 있으며, 각 역할마다 접근할 수 있는 보호된 경로가 다릅니다.

| 역할 | 접근 가능한 경로 |
| --- | --- |
| `seeker` | `/profile`, `/applied`, `/saved`, 공고 지원·저장 POST |
| `employer` | `/employer/*` |
| `admin` | `/admin/*` |

### 라우트 보호

- 보호된 라우트는 핸들러 첫 줄에서 `require_role(user, "역할")`을 호출합니다 (`app/core/auth.py`).
- 현재 사용자는 `user=Depends(get_current_user)`로 주입받습니다. 비로그인 시 None입니다.
- 템플릿 렌더링은 `app/core/templating.py`의 `render()`를 사용해 user가 항상 주입되게 합니다.

### 라우팅 컨벤션

- 폼 제출(POST) 성공 후에는 항상 `RedirectResponse(..., status_code=303)`으로 리다이렉트합니다 (PRG 패턴).
- 새 라우터 파일은 `main.py`의 `include_router`에 등록해야 활성화됩니다.
- 역할별 내비게이션 링크는 `templates/partials/navbar.html`에서 조건 분기합니다.

## Git 규칙

### 브랜치 규칙

브랜치 이름은 작업 목적에 따라 다음과 같은 형식을 사용합니다.

```text
codex/add-job-filter-sidebar           # 새로운 기능 추가
codex/fix-employer-route-redirect      # 버그 수정
codex/update-readme                    # 문서 수정
codex/upgrade-dependencies             # 유지보수 작업
codex/simplify-auth-session            # 코드 리팩터링
codex/mobile-job-card-spacing          # UI 스타일 수정
```

- 모든 새로운 작업은 `main`에서 `codex/` 접두사 브랜치로 분기합니다.
- 브랜치는 가능한 한 짧은 기간 동안 유지하고, 작업이 완료되면 PR(Pull Request)을 생성합니다.
- PR이 병합된 후에는 작업 브랜치를 삭제합니다.

### 커밋 메시지 규칙

커밋 메시지는 **Conventional Commits** 형식을 따릅니다.

```text
feat: add saved jobs count to navbar
fix: correct role guard on employer routes
docs: update README with demo credentials
chore: upgrade fastapi to latest
refactor: extract job card into shared template partial
style: fix spacing on mobile job list
```

주요 커밋 유형은 다음과 같습니다.

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `chore`: 의존성 업데이트, 설정 변경 등 유지보수 작업
- `refactor`: 기능 변경 없이 코드 구조 개선
- `style`: UI 스타일, 레이아웃 등 시각적 요소 수정

커밋 메시지 작성 시 다음 규칙을 따릅니다.

- 현재형을 사용합니다.
- 영문 소문자로 작성합니다.
- 제목 끝에 마침표(`.`)를 사용하지 않습니다.
- 제목은 72자 이내로 작성합니다.
- 변경 내용이 명확하지 않거나 추가 설명이 필요한 경우 커밋 본문(body)을 작성합니다.
- main에 직접 push 금지. 항상 PR로
- 커밋 전 `pytest`와 `ruff check .` 실행

### Pull Request 규칙

- PR 제목은 **Conventional Commits** 형식을 따릅니다.

```text
feat: add saved jobs count to navbar
fix: correct role guard on employer routes
```

- PR 설명에는 다음 내용을 포함합니다.
  - 변경 사항 요약(Summary)
  - 테스트 방법 및 결과(Test Plan)

- PR의 대상(base) 브랜치는 `main`으로 설정합니다.
