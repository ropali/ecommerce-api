from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    PROJECT_NAME: str = "E-Commerce API"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432

    # Environment
    ENVIRONMENT: str = "dev"

    # Debugging
    DEBUG: bool = ENVIRONMENT == "dev"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "*"
    ]  # TODO: In production, replace with specific origins

    # Create DB_URL from database settings
    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = "./.env"
        case_sensitive = True
        frozen = True


# Create a global settings object
settings = _Settings()
