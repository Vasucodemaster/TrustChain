from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "TrustChain"
    VERSION: str = "1.0.0"

    DATABASE_URL: str

    NEO4J_URI: str = ""
    NEO4J_USERNAME: str = ""
    NEO4J_PASSWORD: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
