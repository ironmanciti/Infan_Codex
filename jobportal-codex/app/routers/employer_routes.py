"""고용주(Employer) 라우터 — 내 공고 관리, 공고 등록."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.auth import get_current_user, require_role
from app.core.templating import render
from app.services import job_service
from app.services import misc_services as misc

router = APIRouter(prefix="/employer")


@router.get("/jobs")
def my_jobs(request: Request, user=Depends(get_current_user)):
    require_role(user, "employer")
    company = misc.get_company(user["company_id"])
    return render(request, "employer_jobs.html", user=user, company=company,
                  jobs=job_service.jobs_by_company(user["company_id"]))


@router.post("/jobs")
def post_job(request: Request, user=Depends(get_current_user),
             title: str = Form(...), category: str = Form(...),
             location: str = Form(...), emp_type: str = Form(...),
             salary_min: int = Form(...), salary_max: int = Form(...),
             description: str = Form("")):
    require_role(user, "employer")
    job_service.create_job(user["company_id"], title, category, location,
                           emp_type, salary_min, salary_max, description)
    return RedirectResponse("/employer/jobs", status_code=303)


@router.post("/jobs/{job_id}/delete")
def remove_job(job_id: int, user=Depends(get_current_user)):
    require_role(user, "employer")
    job_service.delete_job(job_id, user["company_id"])
    return RedirectResponse("/employer/jobs", status_code=303)
