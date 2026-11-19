import os
from functools import cache

from sqlalchemy import URL


def database_url() -> str | URL:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    password = os.getenv("POSTGRES_PASSWORD")
    if not password:
        raise RuntimeError("Configura DATABASE_URL o POSTGRES_PASSWORD.")
    return URL.create(
        "postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER", "postgres"),
        password=password,
        host=os.getenv("POSTGRES_HOST", "db"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "cafeteria_db"),
    )


@cache
def jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET", "")
    if len(secret.encode()) < 32:
        raise RuntimeError("JWT_SECRET debe contener al menos 32 bytes.")
    return secret


def cookie_secure() -> bool:
    return os.getenv("COOKIE_SECURE", "true").lower() != "false"


@cache
def allowed_origins() -> list[str]:
    origins = [origin.strip() for origin in os.getenv("APP_ORIGINS", "").split(",") if origin.strip()]
    if any("*" in origin for origin in origins):
        raise RuntimeError("APP_ORIGINS debe contener orígenes explícitos.")
    return origins
