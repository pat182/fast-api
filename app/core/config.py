import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str
    DEBUG: bool
    SECRET_KEY: str
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # db
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None
    ###
    API_PREFIX: str  = "/api"
    JWT_HASHING_ALGORITHM: str
    JWT_MINUTES : int
    JWT_REFRESH_DAYS : int

    @property
    def use_sqlite(self) -> bool:
        """Return True if CI/test mode should use SQLite instead of MySQL."""
        return self.DB_HOST == "sqlite"


settings = Settings()



