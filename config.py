from pydantic import BaseSettings
import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", 5432)
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "bdd")
    POSTGRES_HOSTNAME: str = os.getenv("POSTGRES_HOSTNAME", "localhost")


settings = Settings()
