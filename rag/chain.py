from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langfuse.langchain import CallbackHandler
from rag.retriever import get_retriever
from rag.config import LLM_MODEL

langfuse_handler = CallbackHandler()

RAG_PROMPT = ChatPromptTemplate.from_template("""
You are a sales assistant.

Use ONLY the context below to answer.
If not found, say: "I don't have that information."

Context:
{context}

Question:
{question}

Answer:
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain():
    retriever = get_retriever(k=3)

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain

def ask(question: str):
    retriever = get_retriever(k=3)
    chain = build_rag_chain()

    docs = retriever.invoke(question)

    print(f"Retrieved {len(docs)} docs")

    answer = chain.invoke(
        question,
        config={"callbacks": [langfuse_handler]}
    )

    return {
        "answer": answer,
        "sources": [doc.page_content for doc in docs]
    }