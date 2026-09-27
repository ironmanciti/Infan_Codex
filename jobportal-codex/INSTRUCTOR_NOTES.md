# 강사용 노트 — 의도된 결함과 실습 시나리오 매핑

⚠️ **이 파일은 수강생 배포본에서 제외하세요** (스포일러). 강의 준비용입니다.

## 의도된 결함 4종

| # | 결함 | 위치 | 근본 원인 | 사용 강의 |
|---|---|---|---|---|
| D1 | Footer 법적 링크 툴팁 미표시 | `templates/partials/footer.html` | Privacy Policy·Terms·Cookie Policy 링크에 `class="tooltip"`만 있고 **`data-tip` 속성이 누락**. CSS(`.tooltip[data-tip]:hover::after`)는 속성이 있어야 렌더링됨. About Us는 정상 동작(비교 패턴) | 30강 Issue #2 — "다른 링크에도 동일 패턴" 보고까지 재현됨 |
| D2 | Contact Us가 내비게이션에 없음 | `templates/partials/navbar.html` (없음) / `footer.html` 법적 링크 사이에 묻혀 있음 | 내비게이션 메뉴에 미등록 | 31강 Issue #4 — "Contact Us를 네비게이션 바로 이동" |
| D3 | 저작권 연도 고정 | `templates/partials/footer.html` | `© 2024` 하드코딩 (동적 연도 미사용) | 31강 Issue #5 — "저작권 연도를 현재 연도로" |
| D4 | 프로필 100% 불가 → 경고 배너 지속 | `app/services/profile_service.py` | `PROFILE_FIELDS`가 `'resume'` 키를 검사하지만 실제 저장 필드는 `'resume_url'` → 6개 중 최대 5개 인정, **완성도 상한 83%**. 홈(`app/routers/pages.py`)의 `completion < 100` 조건으로 배너 상시 표시 | 코덱스 이슈 분석 실습 — "프로필을 100% 완성했는데 경고가 계속 뜹니다" |

## 검증 결과 (컨테이너에서 실측)

- 시드: 회사 50 · 공고 1,000 · 데모 계정 3종 정상 생성 (Faker seed=42 고정 → 재현 가능)
- 구직자 플로우: 로그인 → 배너(0%) → 프로필 6개 필드 전부 입력 → **83% 표시, 배너 지속** ✓ (D4)
- 지원/저장/지원 내역, 문의 등록 → 관리자 메시지함, 고용주 공고 등록/삭제 ✓
- Footer: `data-tip` 보유 링크 1개(About Us)뿐 ✓ (D1), navbar에 /contact 없음 ✓ (D2), © 2024 ✓ (D3)
- 다크 모드 토글(localStorage 유지), /docs 자동 문서 ✓

## 실습용 GitHub 이슈 템플릿

**Issue #2 (30강)** — 제목: `Footer legal link tooltips are not showing`
> 푸터의 'Cookie Policy' 링크에 마우스를 올려도 설명 툴팁이 표시되지 않습니다.
> 'About Us' 링크는 툴팁이 정상적으로 나타납니다. 사이트 디자인과 어울리는
> 툴팁으로 수정 부탁드립니다. (스크린샷 첨부)

**Issue #4 (31강)** — 제목: `Move Contact Us link to the navigation bar`
> Contact Us 페이지로 가는 링크가 푸터의 법적 고지 링크들 사이에 묻혀 있어
> 찾기 어렵습니다. 상단 네비게이션 바(Jobs, Companies 옆)로 옮겨 주세요.

**Issue #5 (31강)** — 제목: `Copyright year in footer is outdated`
> 푸터의 저작권 연도가 2024로 고정되어 있습니다. 현재 연도가 자동으로
> 표시되도록 수정해 주세요.

**코덱스 이슈 분석 실습** — 제목: `Profile completion warning never goes away`
> 구직자 계정으로 프로필의 모든 항목(사진, 전화번호, 소개, 지역, 스킬,
> 이력서)을 입력했는데도 홈 화면에 "프로필을 완성하세요 (83%)" 경고가
> 계속 표시됩니다. 완성도가 100%가 되지 않는 원인을 찾아 수정해 주세요.
> 실습 프롬프트: `GitHub 이슈의 증상을 읽고 원인을 조사해 줘. 먼저 근거를 보고하고, 내 요청이 있을 때 수정해 줘.`

## 코덱스 실습 자산

- **프로젝트 지침**: `AGENTS.md`에 FastAPI 구조·코딩·데이터·권한·Git 규칙을 통합
- **하위 에이전트 4종**: `.codex/agents/`의 security, performance, coding_standards, docs_researcher. 검토 목적의 읽기 전용 설정
- **훅 2종**: `.codex/hooks.json`에서 `apply_patch` 전 비밀값 검사와 패치 후 Python 파일 길이 경고. 프로젝트 신뢰 및 훅 검토가 필요하며 모든 편집 경로를 강제하지는 않음
- **스킬 2종**: `.agents/skills/`의 analyze-issue, feature-guide. 코덱스의 프로젝트 스킬 발견 경로를 사용
- **반복 점검 문구**: `.codex/loop.md`를 필요할 때 프롬프트로 사용. 자동 실행 설정은 아님

## 강의 진행 시 준비 순서

1. 이 폴더를 수강생 배포용으로 복사하고 **INSTRUCTOR_NOTES.md 삭제**
2. GitHub 실습을 진행할 경우 저장소를 만들고 위 이슈 4건을 등록. `gh issue view` 실습 전 `gh auth status` 확인
3. 이슈를 코덱스 채팅에서 직접 참조해 분석·수정. GitHub의 `@codex review`는 PR 리뷰 명령이므로 이슈 댓글 호출 예제로 사용하지 않음
4. 지침은 `AGENTS.md`, 스킬은 `.agents/skills/`, 하위 에이전트와 훅은 `.codex/`에서 시연. 훅은 코덱스의 신뢰 검토 후 실행 여부 확인
