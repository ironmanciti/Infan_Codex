"""홈 · 문의(Contact) 라우터."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.auth import get_current_user
from app.core.templating import render
from app.services import job_service, profile_service
from app.services import misc_services as misc

router = APIRouter()


@router.get("/")
def home(request: Request, user=Depends(get_current_user)):
    jobs = job_service.latest_jobs(6)
    companies = misc.list_companies()[:8]

    # 구직자에게 프로필 완성 경고 배너 표시 여부
    profile_warning = False
    completion = 0
    if user and user["role"] == "seeker":
        profile = profile_service.get_profile(user["id"])
        completion = profile_service.calculate_completion(profile)
        if completion < 100:
            profile_warning = True

    return render(request, "index.html", user=user, jobs=jobs, companies=companies,
                  profile_warning=profile_warning, completion=completion)


@router.get("/contact")
def contact_page(request: Request, user=Depends(get_current_user)):
    return render(request, "contact.html", user=user, sent=False)


@router.post("/contact")
def contact_submit(request: Request, user=Depends(get_current_user),
                   name: str = Form(...), email: str = Form(...),
                   subject: str = Form(...), message: str = Form(...)):
    misc.create_message(name, email, subject, message)
    return render(request, "contact.html", user=user, sent=True)
