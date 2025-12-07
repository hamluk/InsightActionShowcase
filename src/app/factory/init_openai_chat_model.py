from langchain_openai import ChatOpenAI

from src.app.core.config import LLMModelSettings


def init_openai_chat_model(llm_model_settings: LLMModelSettings):
    return ChatOpenAI(
            temperature=llm_model_settings.temperature,
            model=llm_model_settings.model_name,
        )