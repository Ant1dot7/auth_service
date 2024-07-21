from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_db: str = Field(alias='POSTGRES_DB')
    postgres_user: str = Field(alias='POSTGRES_USER')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD')
    postgres_host: str = Field(alias='POSTGRES_HOST')
    postgres_port: str = Field(alias='POSTGRES_PORT')
    db_engine: str = Field(alias='DB_ENGINE')

    @property
    def db_url(self) -> str:
        return (f"{self.db_engine}://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
