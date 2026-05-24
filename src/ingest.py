import os
from dotenv import load_dotenv
from pathlib import Path


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

# Verificação de carregamento do PDF e do processo de divisão
root_dir = Path(__file__).parent.parent
pdf_path = root_dir / os.getenv("PDF_NAME")
print(f"Carregando PDF do caminho: {pdf_path}")
document = PyPDFLoader(str(pdf_path)).load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(document)
if not splitter:
    print("Nenhum documento foi gerado após a divisão. Verifique o processo de divisão.")
else:
    print(f"{len(splitter)} documentos foram gerados após a divisão.") 
    
# Verificação do processo de geração de embeddings
embedding_model = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
embeddings = embedding_model.embed_documents([doc.page_content for doc in splitter])
if not embeddings:
    print("Nenhuma embedding foi gerada. Verifique o processo de geração de embeddings.")
else:
    print(f"{len(embeddings)} embeddings foram geradas.")




