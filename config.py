from functools import lru_cache
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseSettings, Field

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # SMTP configuration
    smtp_host: str = Field(default="")
    smtp_port: int = Field(default=587)
    smtp_username: str = Field(default="")
    smtp_password: str = Field(default="")
    email_from: str = Field(default="")
    smtp_timeout: int = Field(default=30)

    # Gemini API configuration
    email_api_key: str = Field(default="")
    email_api_url: str = Field(default="")
    email_model: str = Field(default="gemini-2.0-flash")
    email_api_configured: bool = Field(default=False)

    # SQLite database
    sqlite_path: Path = Field(default=Path(__file__).parent / "database.db")

    @property
    def smtp_configured(self):
        return all([self.smtp_host, self.smtp_username, self.smtp_password, self.email_from])

    @property
    def email_api_ready(self):
        return self.email_api_configured and self.email_api_key and self.email_api_url

@lru_cache
def get_settings():
    return Settings()
