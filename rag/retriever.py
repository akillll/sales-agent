from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from rag.config import CHROMA_PATH, EMBEDDING_MODEL

def get_retriever(k: int = 3):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": k}
    )