"""채용 공고 조회·검색·등록 서비스."""

from app.core.db import get_db

PAGE_SIZE = 20


def list_jobs(page: int = 1, q: str = "", category: str = "", emp_type: str = ""):
    """공고 목록 (검색·필터·페이지네이션)."""
    conn = get_db()
    try:
        where, params = ["1=1"], []
        if q:
            where.append("(jobs.title LIKE ? OR companies.name LIKE ?)")
            params += [f"%{q}%", f"%{q}%"]
        if category:
            where.append("jobs.category = ?")
            params.append(category)
        if emp_type:
            where.append("jobs.employment_type = ?")
            params.append(emp_type)
        clause = " AND ".join(where)

        total = conn.execute(
            f"SELECT COUNT(*) FROM jobs JOIN companies ON companies.id = jobs.company_id"
            f" WHERE {clause}", params).fetchone()[0]
        rows = conn.execute(
            f"SELECT jobs.*, companies.name AS company_name, companies.logo_color"
            f" FROM jobs JOIN companies ON companies.id = jobs.company_id"
            f" WHERE {clause} ORDER BY jobs.posted_at DESC, jobs.id DESC LIMIT ? OFFSET ?",
            params + [PAGE_SIZE, (page - 1) * PAGE_SIZE]).fetchall()
        return rows, total, (total + PAGE_SIZE - 1) // PAGE_SIZE
    finally:
        conn.close()


def get_job(job_id: int):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT jobs.*, companies.name AS company_name, companies.logo_color,"
            " companies.location AS company_location"
            " FROM jobs JOIN companies ON companies.id = jobs.company_id"
            " WHERE jobs.id = ?", (job_id,)).fetchone()
    finally:
        conn.close()


def latest_jobs(limit: int = 6):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT jobs.*, companies.name AS company_name, companies.logo_color"
            " FROM jobs JOIN companies ON companies.id = jobs.company_id"
            " ORDER BY jobs.posted_at DESC, jobs.id DESC LIMIT ?", (limit,)).fetchall()
    finally:
        conn.close()


def jobs_by_company(company_id: int):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT jobs.*, companies.name AS company_name, companies.logo_color"
            " FROM jobs JOIN companies ON companies.id = jobs.company_id"
            " WHERE company_id = ? ORDER BY posted_at DESC", (company_id,)).fetchall()
    finally:
        conn.close()


def create_job(company_id: int, title: str, category: str, location: str,
               emp_type: str, salary_min: int, salary_max: int, description: str):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO jobs (company_id, title, category, location, employment_type,"
            " salary_min, salary_max, description, posted_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'))",
            (company_id, title, category, location, emp_type, salary_min, salary_max, description))
        conn.commit()
    finally:
        conn.close()


def delete_job(job_id: int, company_id: int):
    conn = get_db()
    try:
        conn.execute("DELETE FROM jobs WHERE id = ? AND company_id = ?", (job_id, company_id))
        conn.commit()
    finally:
        conn.close()


def categories():
    conn = get_db()
    try:
        return [r[0] for r in conn.execute(
            "SELECT DISTINCT category FROM jobs ORDER BY category").fetchall()]
    finally:
        conn.close()
