from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever

from src.app.config import LLMModelSettings, VectorstoreSettings, Settings
from src.app.database.langchain_qdrant_wrapper import QdrantLangchainWrapper
from src.app.factory.openai_chat_model import init_openai_chat_model
from src.app.schemas.insight import Insight, Evidence


def _run_retrival_insight_chain(query: str, docs: List[Document], llm_model_settings: LLMModelSettings):
    #todo: check why retriever is returning the same chunk twice
    chat_prompt = ChatPromptTemplate([
        ("system", llm_model_settings.prompts.insight_prompt),
        ("human", "User question: {query}")
    ])

    llm_chat = init_openai_chat_model(llm_model_settings)
    llm_chat.with_structured_output(Insight)

    parser = PydanticOutputParser(pydantic_object=Insight)

    chain = chat_prompt | llm_chat | parser

    context_text = "\n\n---\n\n".join([d.page_content for d in docs])

    response = chain.invoke({
        "context": context_text,
        "query": query,
        "format_instruction": parser.get_format_instructions()
    })

    return response


def _build_evidence_from_docs(docs, top_k=3):
    """
    docs: List[Document] returned by retriever, in ranked order (most relevant first).
    Returns: list of Evidence (first top_k docs).
    """

    evidences: List[Evidence] = []
    for i, d in enumerate(docs[:top_k], start=1):
        md = getattr(d, "metadata", {}) or {}
        evidence = Evidence(
            source=md.get("source"),
            page=md.get("page"),
            file_chunk_id=md.get("file_chunk_index", -1),
            page_chunk_id=md.get("page_chunk_index", -1)
        )
        evidences.append(evidence)
    return evidences


def _generate_insight(
        query: str,
        llm_model_settings: LLMModelSettings,
        vector_store_settings: VectorstoreSettings,
        vector_store_wrapper: QdrantLangchainWrapper
):
    """

    :param query:
    :param llm_model_settings:
    :param vector_store_settings:
    :param vector_store_wrapper:
    :return:
    """

    retriever: VectorStoreRetriever = vector_store_wrapper.get_retriever(vector_store_settings.retrieve_documents_count)
    docs = retriever.invoke(query)
    response =  _run_retrival_insight_chain(query=query, docs=docs, llm_model_settings=llm_model_settings)
    response.evidence = _build_evidence_from_docs(docs, vector_store_settings.retrieve_documents_count)

    return response

def create_insight(
        query: str,
        settings: Settings,
        vector_store_wrapper: QdrantLangchainWrapper
):
    docs =  _generate_insight(
        query=query,
        llm_model_settings=settings.llm_model,
        vector_store_settings=settings.vectorstore,
        vector_store_wrapper=vector_store_wrapper)
    return docs
