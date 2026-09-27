"""Jinja2 템플릿 설정 및 공통 렌더 헬퍼."""

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.core.db import BASE_DIR

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# DB에는 영문 코드값을 저장하고, 화면에는 아래 한국어 라벨을 표시합니다.
EMPLOYMENT_TYPE_LABELS = {
    "Full-time": "정규직",
    "Part-time": "시간제",
    "Contract": "계약직",
    "Internship": "인턴십",
    "Remote": "재택근무",
}

ROLE_LABELS = {
    "admin": "관리자",
    "employer": "고용주",
    "seeker": "구직자",
}

APPLICATION_STATUS_LABELS = {
    "submitted": "지원 완료",
    "reviewing": "검토 중",
    "accepted": "합격",
    "rejected": "불합격",
}


def salary_label(value: int) -> str:
    """원 단위 연봉을 만원 / 억원 단위 한국어 표기로 변환합니다."""
    man = value // 10000
    if man >= 10000:
        eok, rest = divmod(man, 10000)
        return f"{eok}억 {rest:,}만원" if rest else f"{eok}억원"
    return f"{man:,}만원"


def employment_label(value: str) -> str:
    """고용 형태 코드값을 한국어 라벨로 변환합니다."""
    return EMPLOYMENT_TYPE_LABELS.get(value, value)


def status_label(value: str) -> str:
    """지원 상태 코드값을 한국어 라벨로 변환합니다."""
    return APPLICATION_STATUS_LABELS.get(value, value)


templates.env.filters["salary_label"] = salary_label
templates.env.filters["employment_label"] = employment_label
templates.env.filters["status_label"] = status_label
templates.env.globals["EMPLOYMENT_TYPE_LABELS"] = EMPLOYMENT_TYPE_LABELS
templates.env.globals["ROLE_LABELS"] = ROLE_LABELS


def render(request: Request, name: str, user=None, **context):
    """current_user를 모든 템플릿에 주입하는 공통 렌더 함수."""
    context.update({"user": user})
    return templates.TemplateResponse(request, name, context)
