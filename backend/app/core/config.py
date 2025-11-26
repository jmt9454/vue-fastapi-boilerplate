from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vue FastAPI Boilerplate"
    
    # Environment Settings
    MODE: str = "dev"
    DEBUG: bool = False
    
    # CORS (Cross-Origin Resource Sharing)
    # This validator parses a comma-separated string from .env into a List
    # Example .env: ALLOW_ORIGINS=http://localhost:3000,http://localhost:8080
    ALLOW_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str

    # Configuration for loading the .env file
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore" # Ignore extra fields in .env that aren't defined here
    )

settings = Settings()