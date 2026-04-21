from typing import TypedDict, List

class AgentState(TypedDict):
    name: str
    company: str
    enrichment: dict
    rag_context: str
    email: str
    reply: str
    response: str
    history: List[str]
    classification: dict