# Desafio MBA Engenharia de Software com IA - Full Cycle

Este guia demonstra como configurar e executar o sistema de RAG implementado.

## Pré-requisitos

1.  **Docker & Docker Compose** instalados e rodando.
2.  **Chaves de API**: OpenAI API Key ou Google AI Studio Key.
3.  **Python 3.10+** e ambiente virtual configurado.

## Configuração

1.  Edite o arquivo `.env` na raiz do projeto e adicione suas chaves.
    *   Defina `LLM_PROVIDER` como `openai` ou `gemini`.
    *   Preencha `OPENAI_API_KEY` ou `GOOGLE_API_KEY`.

    ```bash
    # Exemplo .env
    LLM_PROVIDER=openai
    OPENAI_API_KEY=sk-proj-123...
    ```

2.  Instale as dependências:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Passo 1: Infraestrutura

Suba o banco de dados PostgreSQL com pgVector:

```bash
docker compose up -d
```

Verifique se os containers `postgres_rag` e `bootstrap_vector_ext` (se aplicável) estão rodando.

## Passo 2: Ingestão de Dados

Execute o script para processar o PDF `document.pdf`:

```bash
python src/ingest.py
```

**Esperado:** Logs indicando carregamento do PDF, divisão em chunks e armazenamento no PGVector.

## Passo 3: Chat Interativo

Inicie o chat CLI:

```bash
python src/chat.py
```

### Exemplo de Uso

```text
Faça sua pergunta:
Qual o faturamento da Empresa SuperTechIABrazil?

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.
```

### Exemplo Fora do Contexto

```text
Faça sua pergunta:
Quantos clientes temos em 2024?

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Para sair, digite `sair` ou `exit`.
