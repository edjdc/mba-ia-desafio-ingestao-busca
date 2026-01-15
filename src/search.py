import logging
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.llm import get_embeddings, get_llm
from src.config import settings

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

_vector_store = None

def get_vector_store():
    global _vector_store
    
    if _vector_store is not None:
        return _vector_store

    try:
        embeddings = get_embeddings()
        connection_string = settings.DATABASE_URL
        collection_name = "document_chunks"

        _vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=connection_string,
            use_jsonb=True,
        )
        return _vector_store
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise e

def search_prompt(question):
    try:
        vector_store = get_vector_store()

        docs_and_scores = vector_store.similarity_search_with_score(question, k=10)
        docs = [doc for doc, score in docs_and_scores]
        
        contexto = format_docs(docs)

        llm = get_llm()
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        
        formatted_prompt = prompt.format(contexto=contexto, pergunta=question)
        response = llm.invoke(formatted_prompt)
        
        return response.content

    except Exception as e:
        logger.error(f"Error during search: {e}")
        return "Ocorreu um erro ao processar sua pergunta."