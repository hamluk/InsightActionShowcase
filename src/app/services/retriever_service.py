from typing import List

from langchain_core.documents import Document


def upsert_documents(chunks: List[Document]):
    """
    Accepts list of Document-like objects with .text and .meta
    or a custom DocumentChunk dataclass.
    """
    pass


def get_retriever(k=4):
    # if _vector_store is None:
    #     init_vectorstore()
    # return _vector_store.as_retriever(search_kwargs={"k": k})
    pass

