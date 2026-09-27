"""회사·지원·저장·문의 서비스 모음."""

from app.core.db import get_db


# --- 회사 -------------------------------------------------------------------
def list_companies(q: str = ""):
    conn = get_db()
    try:
        if q:
            return conn.execute(
                "SELECT companies.*, COUNT(jobs.id) AS job_count FROM companies"
                " LEFT JOIN jobs ON jobs.company_id = companies.id"
                " WHERE companies.name LIKE ? GROUP BY companies.id ORDER BY companies.name",
                (f"%{q}%",)).fetchall()
        return conn.execute(
            "SELECT companies.*, COUNT(jobs.id) AS job_count FROM companies"
            " LEFT JOIN jobs ON jobs.company_id = companies.id"
            " GROUP BY companies.id ORDER BY companies.name").fetchall()
    finally:
        conn.close()


def get_company(company_id: int):
    conn = get_db()
    try:
        return conn.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()
    finally:
        conn.close()


def create_company(name: str, industry: str, location: str, description: str, website: str):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO companies (name, industry, location, description, website)"
            " VALUES (?, ?, ?, ?, ?)", (name, industry, location, description, website))
        conn.commit()
    finally:
        conn.close()


def update_company(company_id: int, name: str, industry: str, location: str,
                   description: str, website: str):
    conn = get_db()
    try:
        conn.execute(
            "UPDATE companies SET name = ?, industry = ?, location = ?, description = ?,"
            " website = ? WHERE id = ?",
            (name, industry, location, description, website, company_id))
        conn.commit()
    finally:
        conn.close()


def delete_company(company_id: int):
    conn = get_db()
    try:
        conn.execute("DELETE FROM jobs WHERE company_id = ?", (company_id,))
        conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
        conn.commit()
    finally:
        conn.close()


# --- 지원 / 저장 ------------------------------------------------------------
def apply_to_job(user_id: int, job_id: int):
    conn = get_db()
    try:
        conn.execute("INSERT OR IGNORE INTO applications (user_id, job_id) VALUES (?, ?)",
                     (user_id, job_id))
        conn.commit()
    finally:
        conn.close()


def save_job(user_id: int, job_id: int):
    conn = get_db()
    try:
        conn.execute("INSERT OR IGNORE INTO saved_jobs (user_id, job_id) VALUES (?, ?)",
                     (user_id, job_id))
        conn.commit()
    finally:
        conn.close()


def applied_jobs(user_id: int):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT jobs.*, companies.name AS company_name, companies.logo_color,"
            " applications.status, applications.applied_at"
            " FROM applications JOIN jobs ON jobs.id = applications.job_id"
            " JOIN companies ON companies.id = jobs.company_id"
            " WHERE applications.user_id = ? ORDER BY applications.applied_at DESC",
            (user_id,)).fetchall()
    finally:
        conn.close()


def saved_jobs(user_id: int):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT jobs.*, companies.name AS company_name, companies.logo_color,"
            " saved_jobs.saved_at"
            " FROM saved_jobs JOIN jobs ON jobs.id = saved_jobs.job_id"
            " JOIN companies ON companies.id = jobs.company_id"
            " WHERE saved_jobs.user_id = ? ORDER BY saved_jobs.saved_at DESC",
            (user_id,)).fetchall()
    finally:
        conn.close()


def user_job_state(user_id: int, job_id: int):
    """특정 공고에 대한 지원/저장 여부."""
    conn = get_db()
    try:
        applied = conn.execute("SELECT 1 FROM applications WHERE user_id = ? AND job_id = ?",
                               (user_id, job_id)).fetchone() is not None
        saved = conn.execute("SELECT 1 FROM saved_jobs WHERE user_id = ? AND job_id = ?",
                             (user_id, job_id)).fetchone() is not None
        return applied, saved
    finally:
        conn.close()


# --- 문의 -------------------------------------------------------------------
def create_message(name: str, email: str, subject: str, message: str):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip(), subject.strip(), message.strip()))
        conn.commit()
    finally:
        conn.close()


def list_messages():
    conn = get_db()
    try:
        return conn.execute(
            "SELECT * FROM contact_messages ORDER BY created_at DESC").fetchall()
    finally:
        conn.close()


# --- 관리자: 고용주 관리 -----------------------------------------------------
def list_users():
    conn = get_db()
    try:
        return conn.execute(
            "SELECT users.*, companies.name AS company_name FROM users"
            " LEFT JOIN companies ON companies.id = users.company_id"
            " ORDER BY users.id").fetchall()
    finally:
        conn.close()


def grant_employer(user_id: int, company_id: int):
    conn = get_db()
    try:
        conn.execute("UPDATE users SET role = 'employer', company_id = ? WHERE id = ?",
                     (company_id, user_id))
        conn.commit()
    finally:
        conn.close()
