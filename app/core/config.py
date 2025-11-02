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

    QUOTES_SCRAPE_TARGET_URL: str = "https://htmlpreview.github.io/?http://github.com/JaMiLy-max/html_css_js/blob/main/scraping/index.html"
    QUESTION_SCRAPE_TARGET_URL: str = "https://ksmb.tistory.com/entry/%EC%98%A4%EB%8A%98-%EB%82%98%EC%97%90%EA%B2%8C-%ED%95%98%EB%8A%94-%EC%A7%88%EB%AC%B8-%EB%8C%80%EB%8B%B5?utm_source=chatgpt.com"

    @property
    def DB_URL(self):
        return f"{self.DB_SCHEME}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=str(".env"),
        extra="ignore"
    )

settings = Settings()
