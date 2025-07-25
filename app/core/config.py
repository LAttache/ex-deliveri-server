from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    @property
    def access_token_expiration(self) -> timedelta:
        return timedelta(minutes=self.access_token_expire_minutes)

    @property
    def refresh_token_expiration(self) -> timedelta:
        return timedelta(days=self.refresh_token_expire_days)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
