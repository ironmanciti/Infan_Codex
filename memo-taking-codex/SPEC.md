Memo Taking Web App — Technical Specification

> 목적: 강의용 Memo Taking 웹 애플리케이션의 구현 기준 정의  
> 실행 환경: localhost  
> 기술 스택: FastAPI + Jinja2 + SQLite + fastapi-users  
> 문서 상태: Initial Specification

\---

## 1\. Project Overview

이 프로젝트는 인증된 사용자가 마크다운 형식의 메모를 생성하고 관리할 수 있는 **Memo Taking 웹 애플리케이션**이다.

사용자는 이메일과 비밀번호로 회원가입 및 로그인할 수 있으며, 로그인 후 자신의 메모를 생성, 조회, 수정, 삭제할 수 있다.

사용자는 특정 메모를 공개 상태로 전환하여 URL로 공유할 수 있으며, 공개된 메모는 로그인하지 않은 사용자도 읽을 수 있다.

본 프로젝트는 **강의 및 실습 목적의 localhost 애플리케이션**이며, 프로덕션 배포 환경 구성은 범위에 포함하지 않는다.

\---

## 2\. Goals

애플리케이션은 다음 기능을 제공해야 한다.

1. 이메일/비밀번호 회원가입
2. 이메일/비밀번호 로그인
3. 로그아웃
4. 인증 상태 유지
5. 메모 생성
6. 메모 목록 조회
7. 메모 상세 조회
8. 메모 수정
9. 메모 삭제
10. 메모 공개 공유
11. 메모 공유 중지
12. 비로그인 사용자의 공개 메모 조회

\---

## 3\. Non-Goals

MVP에서는 다음 기능을 구현하지 않는다.

* Google/GitHub 등 OAuth 로그인
* 이메일 인증
* 비밀번호 재설정
* 실시간 공동 편집
* 자동 저장
* 메모 버전 관리
* 휴지통 및 삭제 복원
* 이미지 업로드 / 파일 첨부
* 댓글, 태그, 폴더, 즐겨찾기
* 모바일 네이티브 앱
* 프로덕션 배포

\---

## 4\. Technology Stack

|영역|기술|사용 목적|
|-|-|-|
|Language|Python 3.11+|애플리케이션 개발|
|Framework|FastAPI|웹 애플리케이션 및 API|
|Templates|Jinja2|서버 렌더링 페이지|
|Styling|HTML / CSS|UI 구성|
|Authentication|fastapi-users|회원가입, 로그인, 사용자 관리|
|Database|SQLite|로컬 데이터 저장|
|Server|uvicorn|개발 서버 실행|

\---

## 5\. High-Level Architecture

```text
Browser
   │
   ├── Page Request ──→ FastAPI Router ──→ Jinja2 Template
   │
   ├── Auth Request ──→ Authentication Routes
   │
   └── Memo Request ──→ Memo API ──→ SQLite
```

애플리케이션은 크게 다음 영역으로 구성한다.

* 페이지 라우트
* 인증 기능
* 메모 CRUD API
* 데이터베이스
* Jinja2 템플릿
* 정적 CSS/JavaScript 파일

\---

## 6\. Application Routes

### 6.1 Public Routes

|Route|설명|
|-|-|
|`/`|랜딩 페이지|
|`/login`|로그인 페이지|
|`/signup`|회원가입 페이지|
|`/share/{share\\\_id}`|공개 메모 조회|

### 6.2 Protected Routes

|Route|설명|
|-|-|
|`/memos`|현재 사용자의 메모 목록|
|`/memos/new`|새 메모 작성|
|`/memos/{id}`|메모 조회 및 편집|

인증되지 않은 사용자가 보호된 페이지에 접근하면 로그인 페이지로 이동시킨다.

\---

## 7\. Authentication Specification

인증은 **fastapi-users**를 사용하여 구현한다.

사용자는 이메일과 비밀번호를 이용하여 회원가입 및 로그인할 수 있어야 한다.

### 주요 기능

* 회원가입
* 로그인
* 로그아웃
* 현재 로그인 사용자 확인

### 인증 규칙

* `/memos/\\\*\\\*` 페이지는 로그인한 사용자만 접근할 수 있다.
* 개인 메모 API는 인증된 사용자만 사용할 수 있다.
* `/share/\\\*\\\*` 공개 페이지는 로그인하지 않아도 접근할 수 있다.
* 각 사용자는 자신의 메모만 조회·수정·삭제할 수 있다.

> fastapi-users의 세부 데이터베이스 구조와 인증 구현 방식은 구현 단계에서 공식 문서를 참고하여 구체화한다.

\---

## 8\. Database Design

SQLite 데이터베이스를 사용한다.

초기 설계에서는 사용자 정보와 메모 정보를 저장하기 위해 다음 두 개의 주요 데이터 영역을 둔다.

### 8.1 Users

사용자 정보에는 최소한 다음 데이터가 필요하다.

|필드|설명|
|-|-|
|`id`|사용자 식별자|
|`email`|사용자 이메일|
|`password`|인증에 필요한 비밀번호 정보|
|`is\\\_active`|사용자 활성 상태|
|`created\\\_at`|가입 시각|

> 실제 users 테이블 구조는 fastapi-users의 요구사항을 확인한 후 최종 결정한다.

### 8.2 Memos

```sql
CREATE TABLE memos (
    id TEXT PRIMARY KEY,
    user\\\_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    is\\\_public INTEGER NOT NULL DEFAULT 0,
    share\\\_id TEXT,
    created\\\_at TEXT NOT NULL,
    updated\\\_at TEXT NOT NULL
);
```

|Column|설명|
|-|-|
|`id`|메모 식별자|
|`user\\\_id`|메모 소유 사용자|
|`title`|메모 제목|
|`content`|메모 본문|
|`is\\\_public`|공개 여부|
|`share\\\_id`|공유 URL에 사용할 식별자|
|`created\\\_at`|생성 시각|
|`updated\\\_at`|수정 시각|

\---

## 9\. Authorization Rules

Authentication은 사용자가 누구인지 확인하고, Authorization은 해당 사용자가 리소스를 사용할 권한이 있는지 확인한다.

모든 개인 메모는 현재 로그인한 사용자의 소유인지 확인해야 한다.

```text
memo.user\\\_id == current\\\_user.id
```

다른 사용자의 메모는 조회, 수정, 삭제 또는 공유할 수 없어야 한다.

공개 메모는 읽기 전용으로 제공한다.

\---

## 10\. Memo CRUD API

|Method|Endpoint|기능|인증|
|-|-|-|-|
|GET|`/api/memos`|내 메모 목록 조회|Required|
|POST|`/api/memos`|메모 생성|Required|
|GET|`/api/memos/{id}`|메모 상세 조회|Required|
|PUT|`/api/memos/{id}`|메모 수정|Required|
|DELETE|`/api/memos/{id}`|메모 삭제|Required|
|POST|`/api/memos/{id}/share`|메모 공유 시작|Required|
|DELETE|`/api/memos/{id}/share`|메모 공유 중지|Required|
|GET|`/api/share/{share\\\_id}`|공개 메모 조회|Not Required|

### API 기본 규칙

* 새 메모의 ID는 서버에서 생성한다.
* 메모 생성 시 생성 시각과 수정 시각을 서버에서 기록한다.
* 메모 수정 시 `updated\\\_at`을 갱신한다.
* 개인 메모 API는 현재 로그인 사용자가 메모 소유자인지 확인한다.
* 클라이언트가 전달한 사용자 ID를 그대로 신뢰하지 않는다.

\---

## 11\. Sharing Specification

사용자는 자신이 소유한 메모를 공개 상태로 전환할 수 있다.

공유를 시작하면 서버는 공개 URL에서 사용할 `share\\\_id`를 생성한다.

공개 URL 형식:

```text
http://localhost:8000/share/{share\\\_id}
```

공개 메모 페이지는 인증 없이 접근할 수 있으며 읽기 전용으로 제공한다.

공유를 중지하면 기존 공개 URL에서는 더 이상 메모를 조회할 수 없어야 한다.

\---

## 12\. UI Specification

|화면|핵심 요소|
|-|-|
|`/`|앱 소개, 로그인, 회원가입|
|`/login`|이메일/비밀번호 로그인 폼|
|`/signup`|이메일/비밀번호 회원가입 폼|
|`/memos`|메모 목록, 새 메모 버튼, 로그아웃|
|`/memos/{id}`|제목, 본문 편집, 저장, 공유, 삭제|
|`/share/{share\\\_id}`|공개 메모 읽기 화면|

전체 페이지는 공통 레이아웃을 사용하고 단순한 CSS로 구성한다.

\---

## 13\. Suggested Project Structure

```text
memo-taking/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── memos.py
│   ├── services/
│   │   └── memo\\\_service.py
│   ├── models/
│   └── schemas/
├── templates/
├── static/
├── data/
├── main.py
├── requirements.txt
└── SPEC.md
```

프로젝트 구조는 구현 과정에서 필요한 파일을 추가하거나 조정할 수 있다.

\---

## 14\. Validation Rules

### 사용자

* 이메일은 올바른 이메일 형식이어야 한다.
* 비밀번호는 최소 길이 기준을 적용한다.

### 메모

* 제목은 문자열이어야 한다.
* 제목의 최대 길이는 200자로 제한한다.
* 본문은 문자열이어야 한다.
* `share\\\_id`는 서버에서 생성하며 클라이언트가 직접 지정하지 않는다.

\---

## 15\. HTTP Status Codes

|Status|사용 사례|
|-|-|
|`200 OK`|정상 조회 또는 수정|
|`201 Created`|리소스 생성|
|`204 No Content`|삭제 성공|
|`400 Bad Request`|잘못된 요청|
|`401 Unauthorized`|로그인 필요|
|`403 Forbidden`|접근 권한 없음|
|`404 Not Found`|리소스를 찾을 수 없음|
|`500 Internal Server Error`|서버 오류|

\---

## 16\. Implementation Memos

이 문서는 프로젝트 시작 단계의 초기 명세이다.

구현을 진행하면서 사용하는 라이브러리의 공식 문서를 확인하고, 라이브러리가 요구하는 데이터베이스 스키마나 설정이 현재 명세와 다를 경우 해당 부분을 업데이트한다.

특히 인증 기능은 **fastapi-users 공식 문서를 기준으로 users 테이블과 인증 관련 구조를 구체화해야 한다.**

