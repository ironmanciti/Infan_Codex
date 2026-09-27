"""로그인 · 로그아웃 라우터."""

from fastapi import APIRouter, Cookie, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.auth import (SESSION_COOKIE, create_session, destroy_session,
                           get_current_user, verify_credentials)
from app.core.templating import render

router = APIRouter()


@router.get("/login")
def login_page(request: Request, user=Depends(get_current_user)):
    if user:
        return RedirectResponse("/", status_code=303)
    return render(request, "login.html", user=None, error=None)


@router.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    account = verify_credentials(email, password)
    if account is None:
        return render(request, "login.html", user=None,
                      error="이메일 또는 비밀번호가 올바르지 않습니다.")
    token = create_session(account["id"])
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(SESSION_COOKIE, token, httponly=True)
    return response


@router.get("/logout")
def logout(jobportal_session: str | None = Cookie(default=None)):
    destroy_session(jobportal_session)
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response
