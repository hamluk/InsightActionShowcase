from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from qdrant_client.http.models import Distance

from src.app.core.prompt import PromptLoader


class VectorstoreSettings(BaseModel):
    """
    Settings class for the vectorstore
    """
    embedding_model: str
    collection_name: str
    dimension: int
    retrieve_documents_count: int
    distance: Distance
    qdrant_endpoint: str
    qdrant_api_key: str


class LLMModelSettings(BaseModel):
    model_name: str
    temperature: float
    prompts: PromptLoader = PromptLoader()


class MailSettings(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_from: str
    smtp_to: str
    smtp_username: str
    smtp_password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__")

    """
    Settings class for backend app
    """
    app_host: str
    app_port: int
    data_dir: Path
    raw_dir: Path
    ALLOWED_EXTENSIONS: List[str]
    openai_api_key: str
    namespace: str
    FILE_MAX_SIZE: int
    chunk_size: int
    chunk_overlap: int
    add_start_index: bool
    pseudonymize_on_ingest: bool

    vectorstore: VectorstoreSettings
    llm_model: LLMModelSettings
    mail: MailSettings


@lru_cache()
def get_settings() -> Settings:
    return Settings()
