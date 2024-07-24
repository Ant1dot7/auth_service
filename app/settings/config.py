from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent
    verify_template_path: Path = base_dir / "infra/smtp_service/email_template.html"

    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: str = Field(alias="POSTGRES_PORT")
    db_engine: str = Field(alias="DB_ENGINE")

    jwt_key: str = Field(alias="JWT_KEY")
    jwt_alg: str = Field(alias="JWT_ALG")

    aws_access_key_id: str = Field(alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(alias="AWS_SECRET_ACCESS_KEY")
    s3_url: str = Field(alias="S3_URL")
    user_bucket: str = Field(default="users")

    time_access_token: int = Field(default=60, alias="TIME_ACCESS_TOKEN")  # minutes
    time_refresh_token: int = Field(default=3660, alias="TIME_REFRESH_TOKEN")  # minutes
    domain_url: str = "http://127.0.0.1:8000"  # todo вынести

    smtp_user: str = Field(alias="SMTP_USER")
    smtp_password: str = Field(alias="SMTP_PASSWORD")
    smtp_host: str = Field(alias="SMTP_HOST")
    smtp_port: int = Field(alias="SMTP_PORT")

    @property
    def db_url(self) -> str:
        return (f"{self.db_engine}://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    class Config:
        env_file = ".env"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()
