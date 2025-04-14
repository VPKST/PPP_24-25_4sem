from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app/db/database.db"
    JWT_SECRET_KEY: str = "secretkey"
    ALGORITHM: str = "HS256"

settings = Settings()
