import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from src.llm import get_embeddings
from src.config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_pdf():
    pdf_path = os.getenv("PDF_PATH", "document.pdf")
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found at: {pdf_path}")
        return

    logger.info(f"Loading PDF from: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    logger.info(f"Loaded {len(docs)} pages.")

    logger.info("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(docs)
    logger.info(f"Created {len(chunks)} chunks.")

    logger.info("Initializing embeddings...")
    try:
        embeddings = get_embeddings()
    except Exception as e:
        logger.error(f"Failed to initialize embeddings: {e}")
        return

    logger.info("Storing in PGVector...")
    connection_string = settings.DATABASE_URL
    collection_name = "document_chunks"

    try:
        PGVector.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=collection_name,
            connection=connection_string,
            use_jsonb=True,
        )
        logger.info("Ingestion complete!")
    except Exception as e:
        logger.error(f"Failed to ingest documents: {e}")

if __name__ == "__main__":
    ingest_pdf()