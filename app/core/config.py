from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "GymAPI"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-insecure-key-cambiar-en-produccion-minimo-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DB_NAME: str = "gym_db"
    DB_USER: str = "gymuser"
    DB_PASSWORD: str = "gympassword"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    DATABASE_URL: Optional[str] = None

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"    
    
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=disable"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
