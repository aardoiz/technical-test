from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    AZURE_API_BASE: str
    AZURE_API_VERSION: str
    AZURE_API_KEY: str
    AZURE_API_DEPLOYMENT: str
    AZURE_API_EMBEDDINGS: str

    MONGO_URI: str
    MONGO_COLLECTION: str
    MONGO_DATABASE: str

    QDRANT_HOST: str
    QDRANT_PORT: int
