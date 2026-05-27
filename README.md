````md
A solução utiliza um score mínimo de relevância na busca vetorial. 
Como o PGVector retorna uma distância, quanto menor o score, maior a similaridade. 
Foi definido o limite `MAX_SCORE = 0.6`; quando o melhor resultado possui score acima desse valor, a aplicação retorna diretamente:

"Não tenho informações necessárias para responder sua pergunta."

## Como executar a solução

### 1. Subir o PostgreSQL com pgVector

```bash
docker compose up -d
````

### 2. Criar o arquivo `.env`

```env
OPENAI_API_KEY=sua_chave_openai

PG_VECTOR_CONNECTION=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
PG_VECTOR_COLLECTION_NAME=pdf_documents
PDF_PATH=document.pdf
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a ingestão do PDF

```bash
python src/ingest.py
```

Esse comando lê o PDF, divide o conteúdo em chunks, gera embeddings e grava os vetores no PostgreSQL com pgVector.

### 5. Executar o chat via terminal

```bash
python src/chat.py
```

Exemplo:

```bash
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.
```

Para sair:

```bash
sair
```

```
```
