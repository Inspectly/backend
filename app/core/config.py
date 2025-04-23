from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    API_STR: str
    V0_STR: str
    PROJECT_NAME: str

    STRIPE_SECRET_KEY: str
    STRIPE_PUBLIC_KEY: str

    INSPECTLYAI_API_KEY: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

if __name__ == "__main__":
    print(settings.DATABASE_URL)
