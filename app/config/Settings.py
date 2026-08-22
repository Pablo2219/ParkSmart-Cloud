from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    LOG_LEVEL: str = "INFO"
    ROOT_PATH: str = ""

    DATABASE_URL: str
    MIGRATION_DATABASE_URL: str | None = None
    DATABASE_CA_CERT: str = ""

    SECRET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    RESET_TOKEN_MINUTES: int = 15
    AUTH_DEBUG_RESET_TOKEN: bool = False

    PRIVACY_POLICY_VERSION: str = "1.0"
    DATA_CONTROLLER_NAME: str = "ParkSmart"
    DATA_CONTROLLER_CONTACT: str = "privacidad@parksmart.local"

    CORS_ORIGINS: str = (
        "http://127.0.0.1:5500,http://localhost:5500,"
        "http://127.0.0.1:8000,http://localhost:8000"
    )
    FRONTEND_URL: str = "http://127.0.0.1:5500"

    NOTIFICATION_MODE: str = "SIMULATION"
    DEFAULT_PHONE_COUNTRY_CODE: str = "+506"

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    SMTP_USE_TLS: bool = True

    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_SMS_FROM: str = ""
    TWILIO_WHATSAPP_FROM: str = ""

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
