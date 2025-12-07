from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams

from src.app.config import VectorstoreSettings

load_dotenv()


class QdrantLangchainWrapper:
    def __init__(self, vectorstore_settings: VectorstoreSettings):
        self.vectorstore_settings = vectorstore_settings
        self.embeddings = OpenAIEmbeddings(model=self.vectorstore_settings.embedding_model)

        self.qdrant_client: QdrantClient = QdrantClient(
            location=self.vectorstore_settings.qdrant_endpoint,
            api_key=self.vectorstore_settings.qdrant_api_key
        )

        if not self.qdrant_client.collection_exists(collection_name=self.vectorstore_settings.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.vectorstore_settings.collection_name,
                vectors_config=VectorParams(
                    size=self.vectorstore_settings.dimension, distance=self.vectorstore_settings.distance
                ),
            )

        self.store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.vectorstore_settings.collection_name,
            embedding=self.embeddings,
        )

    def upsert_documents(self, docs: List[Document]):
        """
        Upsert pre-chunked langchain documents int Qdrant vectorstore
        - creates uuids for the given chunks
        - upsert documents with using langchain wrapper

        :param docs: chunked documents to be upserted
        :return:
        """
        # todo: make sure no document is uploaded twice
        uuids = [str(uuid4()) for _ in range(len(docs))]
        self.store.add_documents(documents=docs, ids=uuids)

    def get_retriever(self, k: int) -> VectorStoreRetriever:
        """
        Get the retriever for the connected Qdrant vectorstore

        :param k: number of results to retrieve
        :return: langchain vectorstore retriever for building RAG chains
        """
        return self.store.as_retriever(search_kwargs={"k": k})
