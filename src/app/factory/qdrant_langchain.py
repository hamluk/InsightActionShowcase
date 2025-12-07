from functools import lru_cache

from src.app.config import get_settings
from src.app.database.langchain_qdrant_wrapper import QdrantLangchainWrapper


@lru_cache
def get_qdrant_langchain_wrapper() -> QdrantLangchainWrapper:
    settings = get_settings()
    wrapper = QdrantLangchainWrapper(settings.vectorstore)
    return wrapper
