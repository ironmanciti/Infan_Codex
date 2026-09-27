"""Job Portal — FastAPI 실습용 애플리케이션.

실행:
    uvicorn main:app --reload
    (또는 python main.py)

데모 계정:
    admin@demo.com / admin123       (관리자)
    employer@demo.com / employer123 (고용주)
    seeker@demo.com / seeker123     (구직자)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.db import BASE_DIR, init_db
from app.core.seed import seed_if_empty
from app.routers import (admin_routes, auth_routes, employer_routes,
                         jobs_routes, pages, seeker_routes)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_if_empty()
    yield


app = FastAPI(title="Job Portal", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(pages.router)
app.include_router(auth_routes.router)
app.include_router(jobs_routes.router)
app.include_router(seeker_routes.router)
app.include_router(employer_routes.router)
app.include_router(admin_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
