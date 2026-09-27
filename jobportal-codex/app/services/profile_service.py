"""구직자 프로필 서비스 — 완성도 계산 포함."""

from app.core.db import get_db

PROFILE_FIELDS = ["photo_url", "phone", "headline", "location", "skills", "resume"]


def get_profile(user_id: int):
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
        if row is None:
            conn.execute("INSERT INTO profiles (user_id) VALUES (?)", (user_id,))
            conn.commit()
            row = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
        return row
    finally:
        conn.close()


def update_profile(user_id: int, photo_url: str, phone: str, headline: str,
                   location: str, skills: str, resume_url: str):
    conn = get_db()
    try:
        conn.execute(
            "UPDATE profiles SET photo_url = ?, phone = ?, headline = ?,"
            " location = ?, skills = ?, resume_url = ? WHERE user_id = ?",
            (photo_url.strip(), phone.strip(), headline.strip(),
             location.strip(), skills.strip(), resume_url.strip(), user_id))
        conn.commit()
    finally:
        conn.close()


def calculate_completion(profile) -> int:
    """프로필 완성도(%) — 채워진 필드 수 / 전체 필드 수."""
    if profile is None:
        return 0
    data = dict(profile)
    filled = sum(1 for field in PROFILE_FIELDS if str(data.get(field, "")).strip())
    return round(filled / len(PROFILE_FIELDS) * 100)
