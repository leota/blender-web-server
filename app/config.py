from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Blender Engine API"
    ENVIRONMENT: str
    SENTRY_DSN: str
    DO_SPACES_REGION: str
    DO_SPACES_ENDPOINT: str
    DO_SPACES_BUCKET_NAME: str
    DO_SPACES_KEY: str
    DO_SPACES_SECRET: str
    PROJECTS_FOLDER: str
    OUTPUT_FOLDER: str

    class Config:
        env_file = ".env"