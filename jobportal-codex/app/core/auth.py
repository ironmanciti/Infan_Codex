"""세션 기반 인증 — 서명된 쿠키 대신 서버 메모리 세션(데모용 단순화)."""

import secrets

from fastapi import Cookie, HTTPException, status

from app.core.db import get_db
from app.core.seed import hash_password

# 데모용 인메모리 세션 저장소 {token: user_id}
_sessions: dict[str, int] = {}

SESSION_COOKIE = "jobportal_session"


def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[token] = user_id
    return token


def destroy_session(token: str | None) -> None:
    if token:
        _sessions.pop(token, None)


def verify_credentials(email: str, password: str):
    """이메일·비밀번호 검증 후 사용자 row 반환 (실패 시 None)."""
    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and user["password_hash"] == hash_password(password):
            return user
        return None
    finally:
        conn.close()


def get_current_user(jobportal_session: str | None = Cookie(default=None)):
    """현재 로그인 사용자 (비로그인 시 None) — 템플릿 공통 컨텍스트용."""
    user_id = _sessions.get(jobportal_session or "")
    if not user_id:
        return None
    conn = get_db()
    try:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    finally:
        conn.close()


def require_role(user, *roles: str):
    """역할 검사 — 미로그인 401, 권한 없음 403."""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인이 필요합니다.")
    if user["role"] not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="접근 권한이 없습니다.")
