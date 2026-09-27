"""관리자(Admin) 라우터 — 회사 관리, 문의 내역, 고용주 권한 부여."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.auth import get_current_user, require_role
from app.core.templating import render
from app.services import misc_services as misc

router = APIRouter(prefix="/admin")


@router.get("")
def dashboard(request: Request, user=Depends(get_current_user)):
    require_role(user, "admin")
    return render(request, "admin/dashboard.html", user=user,
                  companies=misc.list_companies(), messages=misc.list_messages(),
                  users=misc.list_users())


@router.get("/companies")
def companies_admin(request: Request, user=Depends(get_current_user)):
    require_role(user, "admin")
    return render(request, "admin/companies.html", user=user,
                  companies=misc.list_companies())


@router.post("/companies")
def company_create(user=Depends(get_current_user), name: str = Form(...),
                   industry: str = Form(...), location: str = Form(...),
                   description: str = Form(""), website: str = Form("")):
    require_role(user, "admin")
    misc.create_company(name, industry, location, description, website)
    return RedirectResponse("/admin/companies", status_code=303)


@router.post("/companies/{company_id}/update")
def company_update(company_id: int, user=Depends(get_current_user),
                   name: str = Form(...), industry: str = Form(...),
                   location: str = Form(...), description: str = Form(""),
                   website: str = Form("")):
    require_role(user, "admin")
    misc.update_company(company_id, name, industry, location, description, website)
    return RedirectResponse("/admin/companies", status_code=303)


@router.post("/companies/{company_id}/delete")
def company_delete(company_id: int, user=Depends(get_current_user)):
    require_role(user, "admin")
    misc.delete_company(company_id)
    return RedirectResponse("/admin/companies", status_code=303)


@router.get("/messages")
def messages_admin(request: Request, user=Depends(get_current_user)):
    require_role(user, "admin")
    return render(request, "admin/messages.html", user=user, messages=misc.list_messages())


@router.get("/employers")
def employers_admin(request: Request, user=Depends(get_current_user)):
    require_role(user, "admin")
    return render(request, "admin/employers.html", user=user,
                  users=misc.list_users(), companies=misc.list_companies())


@router.post("/employers/grant")
def grant_employer(user=Depends(get_current_user), user_id: int = Form(...),
                   company_id: int = Form(...)):
    require_role(user, "admin")
    misc.grant_employer(user_id, company_id)
    return RedirectResponse("/admin/employers", status_code=303)
