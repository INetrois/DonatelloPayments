from os import getenv
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    load_dotenv(BASE_DIR / ".env")
    api_v1_prefix: str = "/api/v1"

    # ------ Application settings ------
    version: str = "0.1.0"
    name: str = "DonatelloPayments"
    description: str = "This API allows you to make payments using Donatello."
    debug: bool = bool(getenv("DEBUG", "false").lower() == "true")

    # ------ Host settings ------
    host: str = getenv("HOST", "0.0.0.0")
    port: int = int(getenv("PORT", 8000))

    # ------ Donatello settings ------
    donatello_user: str = "Degchan"
    donatello_token: str = getenv("DONATELLO_TOKEN")

    # ------ Database settings ------
    db_filename: str = "db.sqlite3"
    db_filepath: str = f"{BASE_DIR}/dbs/{db_filename}"
    db_url: str = getenv(
        "DATABASE_URL", f"sqlite+aiosqlite:///{db_filepath}"
    )
    db_echo: bool = debug # Echo SQL queries if in debug mode | You can set it


settings = Settings()
