from functools import cached_property
from pydantic import field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    mode: str = "DEV"
    # server
    title: str = "FastAPI Project"
    description: str = "FastAPI Project"
    version: str = "0.1.0"
    # database
    port: int
    host: str
    user: str
    password: str
    db_name: str

    debug: bool = False

    model_config = SettingsConfigDict(frozen=True, env_file="dev.env")

    @cached_property
    def log_level(self) -> str:
        return "DEBUG" if self.debug else "INFO"

    def postgres_dsn_asyncpg_scheme(cls) -> PostgresDsn:

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=cls.user,
            password=cls.password,
            host=cls.host,
            port=cls.port,
            path=cls.db_name,
        ).__str__()

    @cached_property
    def db_dsn(self) -> str:
        return self.postgres_dsn_asyncpg_scheme()


settings = Settings()
