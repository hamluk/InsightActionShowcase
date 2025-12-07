from pathlib import Path
from typing import Dict, List
from uuid import uuid4

import fitz
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.app.config import Settings
from src.app.database.langchain_qdrant_wrapper import QdrantLangchainWrapper
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def pdf_extract_text(path: Path, original_filename: str) -> List[Document]:
    logger.info(f"Extracting text from pdf: {original_filename}")
    doc = fitz.open(path)
    docs: List[Document] = []

    for i, p in enumerate(doc):
        text = p.get_text("text")
        metadata = {
            "source": original_filename,
            "page": i+1,
            "type": "pdf"
        }
        docs.append(Document(page_content=text, metadata=metadata))

    return docs


def chunk_documents(page_docs: List[Document], settings: Settings) -> List[Document]:
    logger.info(f"Chunking documents: {len(page_docs)}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=settings.add_start_index,
    )

    doc_chunks: List[Document] = []
    global_chunk_index = 0
    for page in page_docs:

        chunks = text_splitter.split_text(page.page_content)
        for idx, chunk in enumerate(chunks):
            md = dict(page.metadata)
            md.update({
                "page_chunk_index": idx,
                "file_chunk_index": global_chunk_index,
            })
            doc_chunks.append(Document(page_content=chunk, metadata=md))
            global_chunk_index += 1
    return doc_chunks


async def ingest_file_path(
        path: Path,
        original_filename: str,
        settings: Settings,
        vector_store_wrapper: QdrantLangchainWrapper
) -> Dict:
    """
    Top-level ingest function. Extracts data from different datatypes, takes care of pseudonymizing,
    upserts files into vector database.
    :param path: disk path
    :param original_filename: file name
    :param settings:
    :param vector_store_wrapper:
    :return: job metadata dictionary
    """
    if not path.exists():
        raise FileNotFoundError(str(path))

    ext = path.suffix.lower().lstrip(".")

    if ext == "pdf":
        logger.info(f"Processing pdf file: {original_filename}")
        page_docs = pdf_extract_text(path, original_filename)
        doc_chunks = chunk_documents(page_docs, settings)
        logger.info(f"{len(doc_chunks)} chunks from document extracted and upserting them to vector database")
        vector_store_wrapper.upsert_documents(doc_chunks)
        logger.info("finished processing pdf file")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if settings.pseudonymize_on_ingest:
        pass  # Todo: add pseudonymizing process

    # for doc_chunk in doc_chunks:
    #     md = dict(doc_chunk.metadata or {})
    #     md.setdefault("namespace", settings.namespace)
    #     md.setdefault("source", original_filename)
    #     doc_chunk.metadata = md

    # await run_in_threadpool(upsert_documents, doc_chunks)

    job = {"job_id": str(uuid4()), "status": "ingested", "file": original_filename, "chunks": len(doc_chunks)}
    logger.info(f"Job id: {job['job_id']}")
    return job
