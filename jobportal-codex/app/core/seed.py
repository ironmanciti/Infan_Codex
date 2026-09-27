"""데모 데이터 시드 — Faker로 회사 50곳, 채용 공고 1,000건, 데모 계정 3종 생성."""

import hashlib
import random

from faker import Faker

from app.core.db import get_db

fake = Faker("ko_KR")
Faker.seed(42)
random.seed(42)

INDUSTRIES = ["IT 서비스", "핀테크", "이커머스", "헬스케어", "교육",
              "제조", "미디어", "물류", "에너지", "게임"]

# 직군 코드값과 화면에 사용할 직함
CATEGORY_TITLES = {
    "백엔드": "백엔드 엔지니어",
    "프론트엔드": "프론트엔드 엔지니어",
    "풀스택": "풀스택 엔지니어",
    "데이터": "데이터 엔지니어",
    "DevOps": "DevOps 엔지니어",
    "모바일": "모바일 앱 개발자",
    "QA": "QA 엔지니어",
    "프로덕트": "프로덕트 매니저",
    "디자인": "프로덕트 디자이너",
    "보안": "보안 엔지니어",
}

LEVELS = ["주니어", "미들", "시니어", "리드", "스태프"]
EMPLOYMENT_TYPES = ["Full-time", "Part-time", "Contract", "Internship", "Remote"]
LOGO_COLORS = ["#4f6ef7", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#0ea5e9", "#ec4899"]

DESCRIPTION_SENTENCES = [
    "서비스의 핵심 기능을 설계하고 개발하며 안정적으로 운영합니다.",
    "동료와 코드 리뷰를 주고받으며 함께 품질을 높여 갑니다.",
    "기획, 디자인 조직과 긴밀하게 협업하여 요구사항을 구체화합니다.",
    "대규모 트래픽 환경에서 성능 개선과 장애 대응 경험을 쌓을 수 있습니다.",
    "새로운 기술 도입을 자유롭게 제안하고 검증할 수 있는 문화를 지향합니다.",
    "테스트와 자동화를 통해 반복 작업을 줄이는 데 관심이 있는 분을 환영합니다.",
    "관련 실무 경험이 있으면 좋지만, 성장 의지를 더 중요하게 봅니다.",
    "유연 근무제와 교육비 지원 등 성장을 위한 제도를 운영하고 있습니다.",
]

DEMO_USERS = [
    ("admin@demo.com", "admin123", "김관리", "admin", None),
    ("employer@demo.com", "employer123", "이고용", "employer", 1),
    ("seeker@demo.com", "seeker123", "박구직", "seeker", None),
]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def make_description(title: str) -> str:
    """공고 소개 문구를 한국어 문장 풀에서 조합합니다."""
    body = random.sample(DESCRIPTION_SENTENCES, 4)
    return " ".join([f"{title} 직무를 함께할 동료를 찾습니다."] + body)


def seed_if_empty() -> None:
    conn = get_db()
    try:
        count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        if count > 0:
            return

        # 회사 50곳
        for _ in range(50):
            conn.execute(
                "INSERT INTO companies (name, industry, location, description, website, logo_color)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (fake.company(), random.choice(INDUSTRIES), fake.city(),
                 fake.catch_phrase(), fake.url(), random.choice(LOGO_COLORS)),
            )

        # 채용 공고 1,000건
        for _ in range(1000):
            level = random.choice(LEVELS)
            cat = random.choice(list(CATEGORY_TITLES))
            title = f"{level} {CATEGORY_TITLES[cat]}"
            base = random.randint(3000, 9000) * 10000
            conn.execute(
                "INSERT INTO jobs (company_id, title, category, location, employment_type,"
                " salary_min, salary_max, description, posted_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (random.randint(1, 50), title, cat, fake.city(),
                 random.choice(EMPLOYMENT_TYPES), base, base + random.randint(500, 4000) * 10000,
                 make_description(title),
                 fake.date_between(start_date="-90d", end_date="today").isoformat()),
            )

        # 데모 계정 3종 + 구직자 프로필(빈 상태)
        for email, pw, name, role, company_id in DEMO_USERS:
            cur = conn.execute(
                "INSERT INTO users (email, password_hash, name, role, company_id)"
                " VALUES (?, ?, ?, ?, ?)",
                (email, hash_password(pw), name, role, company_id),
            )
            if role == "seeker":
                conn.execute("INSERT INTO profiles (user_id) VALUES (?)", (cur.lastrowid,))

        conn.commit()
    finally:
        conn.close()
