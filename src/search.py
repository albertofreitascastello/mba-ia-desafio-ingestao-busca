import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

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
    context_parts = []

    for item in results:
        if isinstance(item, tuple):
            doc, score = item
        else:
            doc = item

        context_parts.append(doc.page_content)

    return "\n\n".join(context_parts)
  
def open_vector_store():
    embedding_model = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    return  PGVector(
      collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
      connection=os.getenv("DATABASE_URL"),
      embeddings=embedding_model,
      use_jsonb=True  
      )
    
def search_context(question=None):
    #Abrir a conexão com o vetor armazenado no PGVector
    vector_store = open_vector_store()

    # Definimos um limite de pontuação para considerar os resultados relevantes. Se o melhor resultado tiver uma pontuação acima desse limite, 
    # consideramos que não temos informações suficientes para responder à pergunta.
    MAX_SCORE = 0.60
    results = vector_store.similarity_search_with_score(question, k=10)

    if not results:
        return "Não tenho informações necessárias para responder sua pergunta."

    best_score = results[0][1]
    print(f"Best score: {best_score}")

    if best_score > MAX_SCORE:
        return "Não tenho informações necessárias para responder sua pergunta."

    return results
  

def search_prompt(question=None):
  # Realiza a busca no vetor e obtém os resultados
  results = search_context(question)   
  
  # Se a resposta for uma string, significa que não há informações suficientes para responder à pergunta, então retornamos essa string diretamente
  if isinstance(results, str):
    return results
  
  # Construímos o contexto a partir dos resultados da busca
  context = build_context(results)
  #print(f"Contexto construído:\n{context}\n")
  
  prompt = prompt_template.format(
        contexto=context,
        pergunta=question
    )

  # Criamos uma instância do modelo de linguagem e geramos a resposta com base no prompt
  llm = ChatOpenAI(model="gpt-5-nano")
  response = llm.invoke(prompt)

  return response.content