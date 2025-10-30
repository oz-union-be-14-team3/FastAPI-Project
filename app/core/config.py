from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    DB_SCHEME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    APP_TITLE: str = "FastAPI Mini Project"
    APP_VERSION: str = "0.119.1"

    QUOTES_SCRAPE_TARGET_URL: str = "https://quotes-site-xi.vercel.app" # 임시 사이트입니다.

    @property
    def DB_URL(self):
        return f"{self.DB_SCHEME}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=str(".env"),
        extra="ignore"
    )

settings = Settings()