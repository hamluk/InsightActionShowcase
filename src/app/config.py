from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseModel
from qdrant_client.http.models import Distance

from src.app.schemas.prompt import PromptLoader


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
    openai_api_key: str
    prompts: PromptLoader = PromptLoader()


class MailSettings(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_from: str
    smtp_to: str
    smtp_username: str
    smtp_password: str


class Settings(BaseModel):
    """
    Settings class for backend app
    """
    data_dir: Path
    raw_dir: Path

    vectorstore: VectorstoreSettings
    llm_model: LLMModelSettings
    mail: MailSettings


@lru_cache()
def get_settings() -> Settings:
    return Settings()
