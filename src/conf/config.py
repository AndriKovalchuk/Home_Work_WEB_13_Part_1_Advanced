from typing import Any

from pydantic import ConfigDict, EmailStr, field_validator
from pydantic_settings import BaseSettings


# fake data
class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/Module_13_Home_Work_WEB"
    SECRET_KEY_JWT: str = "123456789"
    ALGORITHM: str = "123456789"
    MAIL_USERNAME: EmailStr = "123456789"
    MAIL_PASSWORD: str = "123456789"
    MAIL_FROM: str = "123456789"
    MAIL_PORT: int = 123456789
    MAIL_SERVER: str = "123456789"
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "abcdefghijklmnopqrstuvwxyz"
    CLD_API_KEY: int = 123456789
    CLD_API_SECRET: str = "secret"

    @field_validator("ALGORITHM")  # noqa
    @classmethod
    def validate_ALGORITHM(cls, value: Any) -> str:
        if value not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be either HS256 or HS512")
        return value

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
