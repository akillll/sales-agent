from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from rag.config import CHROMA_PATH, EMBEDDING_MODEL
from dotenv import load_dotenv

load_dotenv()

def ingest_documents():
    loader = TextLoader("rag/knowledge/playbook.txt")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata = {"chunk_id": i}

    print(f"Created {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )

    print("Ingestion Complete")


if __name__ == "__main__":
    ingest_documents()

