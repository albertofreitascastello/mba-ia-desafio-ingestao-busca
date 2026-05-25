import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_prompts import ChatPromptTemplate

load_dotenv()

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

prompt_template = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["contexto", "pergunta"]
)

def build_context(results):
    return "\n\n".join([doc.page_content for doc, score in results])
  
def open_vector_store():
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    return  PGVector(
      collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
      connection=os.getenv("DATABASE_URL"),
      embeddings=embedding_model,
      use_jsonb=True  
      )
    
def search_context(question=None):
    vector_store = open_vector_store()
    return vector_store.similarity_search_with_score(question, k=10)
  

def search_prompt(question=None):
  results = search_context(question)   
  context = build_context(results)
  prompt = prompt_template.format(
        contexto=context,
        pergunta=question
    )

  llm = ChatOpenAI(model="gpt-5-nano")
  response = llm.invoke([HumanMessage(content=prompt)])

  return response.content