"""구직자(Seeker) 라우터 — 프로필, 지원 내역, 저장한 공고."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.auth import get_current_user, require_role
from app.core.templating import render
from app.services import profile_service
from app.services import misc_services as misc

router = APIRouter()


@router.get("/profile")
def profile_page(request: Request, user=Depends(get_current_user), saved: int = 0):
    require_role(user, "seeker")
    profile = profile_service.get_profile(user["id"])
    completion = profile_service.calculate_completion(profile)
    return render(request, "profile.html", user=user, profile=profile,
                  completion=completion, saved=bool(saved))


@router.post("/profile")
def profile_update(request: Request, user=Depends(get_current_user),
                   photo_url: str = Form(""), phone: str = Form(""),
                   headline: str = Form(""), location: str = Form(""),
                   skills: str = Form(""), resume_url: str = Form("")):
    require_role(user, "seeker")
    profile_service.update_profile(user["id"], photo_url, phone, headline,
                                   location, skills, resume_url)
    return RedirectResponse("/profile?saved=1", status_code=303)


@router.get("/applied")
def applied_page(request: Request, user=Depends(get_current_user)):
    require_role(user, "seeker")
    return render(request, "applied.html", user=user, jobs=misc.applied_jobs(user["id"]))


@router.get("/saved")
def saved_page(request: Request, user=Depends(get_current_user)):
    require_role(user, "seeker")
    return render(request, "saved.html", user=user, jobs=misc.saved_jobs(user["id"]))
