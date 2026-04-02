"""Configuration management for AuditAI backend."""
import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator


_FALSE_BOOL_VALUES = {"false", "0", "no", "off", "release"}
_TRUE_BOOL_VALUES = {"true", "1", "yes", "on", "debug"}


def _normalize_bool_env(key: str) -> None:
    value = os.environ.get(key)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in _FALSE_BOOL_VALUES:
            os.environ[key] = "false"
        elif normalized in _TRUE_BOOL_VALUES:
            os.environ[key] = "true"


# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
_normalize_bool_env("DEBUG")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(extra='ignore', env_file='.env')

    # API
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    secret_key: str = Field(default="your-secret-key-change-in-production", alias="SECRET_KEY")

    # Database
    database_url: str = Field(default="postgresql://postgres:password@localhost:5432/auditai", alias="DATABASE_URL")
    database_async_url: str = Field(default="postgresql+asyncpg://postgres:password@localhost:5432/auditai", alias="DATABASE_ASYNC_URL")

    # JWT
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # OAuth
    google_client_id: str = Field(default="", alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="", alias="GOOGLE_CLIENT_SECRET")

    # External APIs
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_default_model: str = Field(default="nvidia/llama-3.1-nemotron-70b-instruct", alias="OPENROUTER_DEFAULT_MODEL")
    huggingface_api_key: str = Field(default="", alias="HUGGINGFACE_API_KEY")

    # Supabase
    next_public_supabase_url: str = Field(default="", alias="NEXT_PUBLIC_SUPABASE_URL")
    next_public_supabase_publishable_default_key: str = Field(default="", alias="NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
    supabase_service_key: str = Field(default="", alias="SUPABASE_SERVICE_KEY")

    # Storage
    storage_path: str = Field(default="./storage", alias="STORAGE_PATH")
    upload_dir: str = Field(default="./storage/uploads", alias="UPLOAD_DIR")
    report_dir: str = Field(default="./storage/reports", alias="REPORT_DIR")

    # ML Models
    fraud_model_path: str = Field(default="./app/ai/fraud_model/artifacts/fraud_classifier.joblib", alias="FRAUD_MODEL_PATH")
    risk_model_path: str = Field(default="./app/ai/risk_model/artifacts/risk_regressor.joblib", alias="RISK_MODEL_PATH")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", alias="LOG_FILE")

    @field_validator("debug", mode="before")
    def _coerce_debug_flag(cls, value):
        """Accept custom string values (e.g., 'release') as boolean flags."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"false", "0", "no", "off", "release"}:
                return False
            if normalized in {"true", "1", "yes", "on", "debug"}:
                return True
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()
