"""채용 공고 목록 · 상세 · 지원 · 저장 라우터."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.core.auth import get_current_user, require_role
from app.core.templating import render
from app.services import job_service
from app.services import misc_services as misc

router = APIRouter()


@router.get("/jobs")
def jobs_list(request: Request, user=Depends(get_current_user),
              page: int = 1, q: str = "", category: str = "", emp_type: str = ""):
    jobs, total, pages = job_service.list_jobs(page, q, category, emp_type)
    return render(request, "jobs.html", user=user, jobs=jobs, total=total,
                  pages=pages, page=page, q=q, category=category, emp_type=emp_type,
                  categories=job_service.categories())


@router.get("/jobs/{job_id}")
def job_detail(request: Request, job_id: int, user=Depends(get_current_user)):
    job = job_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")
    applied = saved = False
    if user and user["role"] == "seeker":
        applied, saved = misc.user_job_state(user["id"], job_id)
    return render(request, "job_detail.html", user=user, job=job,
                  applied=applied, saved=saved)


@router.post("/jobs/{job_id}/apply")
def apply(job_id: int, user=Depends(get_current_user)):
    require_role(user, "seeker")
    misc.apply_to_job(user["id"], job_id)
    return RedirectResponse(f"/jobs/{job_id}", status_code=303)


@router.post("/jobs/{job_id}/save")
def save(job_id: int, user=Depends(get_current_user)):
    require_role(user, "seeker")
    misc.save_job(user["id"], job_id)
    return RedirectResponse(f"/jobs/{job_id}", status_code=303)


@router.get("/companies")
def companies_list(request: Request, user=Depends(get_current_user), q: str = ""):
    return render(request, "companies.html", user=user,
                  companies=misc.list_companies(q), q=q)


@router.get("/companies/{company_id}")
def company_detail(request: Request, company_id: int, user=Depends(get_current_user)):
    company = misc.get_company(company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="회사를 찾을 수 없습니다.")
    return render(request, "company_detail.html", user=user, company=company,
                  jobs=job_service.jobs_by_company(company_id))
