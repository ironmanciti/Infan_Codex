---
name: feature-guide
description: JobPortal 기능의 실제 요청 경로와 데이터 흐름을 FastAPI 라우터부터 SQLite와 Jinja2 화면까지 추적해 설명합니다. 특정 기능의 동작 설명이나 탐색 요청에 사용합니다.
---

# 기능 흐름 설명

요청한 기능과 연결된 `app/routers/`, `app/services/`, `app/core/`, `templates/` 파일을 확인합니다. 시작 경로는 `main.py`의 라우터 등록과 해당 `@router` 데코레이터에서 찾습니다.

- 공개 기능: 채용공고·회사 탐색은 `jobs_routes.py`, 홈·문의는 `pages.py`, 로그인은 `auth_routes.py`에서 시작합니다.
- 구직자: 프로필·지원 내역·저장 목록은 `seeker_routes.py`, 지원·저장 POST는 `jobs_routes.py`에서 시작합니다.
- 고용주와 관리자: 각각 `employer_routes.py`, `admin_routes.py`에서 시작합니다.

라우터의 인증·역할 검사, 호출하는 서비스 함수, SQLite 테이블·쿼리, 렌더링 템플릿과 사용자에게 보이는 결과를 순서대로 설명합니다. 실제 파일 경로와 함수명을 적고, 확인하지 않은 동작은 추정이라고 밝힙니다. 이 프로젝트는 서버 렌더링 앱이므로 React Context나 프론트엔드 상태 계층을 가정하지 않습니다.
