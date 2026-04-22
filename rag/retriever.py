from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from sentence_transformers import CrossEncoder
from langchain_core.runnables import RunnableLambda
from rag.config import CHROMA_PATH, EMBEDDING_MODEL

reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, docs, top_k=3):
    pairs = [(query, doc.page_content) for doc in docs]

    scores = reranker_model.predict(pairs)

    scored_docs = list(zip(docs, scores))
    scored_docs.sort(key= lambda x: x[1], reverse=True)

    return [doc for doc, _ in scored_docs[:top_k]]

def get_retriever(k: int = 3):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    vector_retriever = vectorstore.as_retriever(
        search_kwargs={"k": 8}
    )

    docs = vectorstore.similarity_search("", k=50)

    bm25 = BM25Retriever.from_documents(docs)
    bm25.k = 8

    hybrid = EnsembleRetriever(
        retrievers=[bm25, vector_retriever],
        weights=[0.4, 0.6]
    )

    def retrieve_and_rerank(query):
        docs = hybrid.invoke(query)
        return rerank(query, docs, top_k=k)

    return RunnableLambda(retrieve_and_rerank)