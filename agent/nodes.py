from agent.tools import enrich_prospect
from services.llm import call_llm, call_llm_json
from agent.prompts import (
    email_prompt,
    reply_classification_prompt,
    objection_prompt
)
from rag.retriever import get_retriever
from services.observability import observe

@observe(name="enrich_node")
def enrich_node(state):
    enrichment = enrich_prospect(state["name"], state["company"])
    state["enrichment"] = enrichment
    print("➡️ enrich_node")
    return state

@observe(name="email_node")
def email_node(state):
    prompt = email_prompt(state)
    email = call_llm(prompt)
    state["email"] = email
    print("➡️ email_node")
    return state

@observe(name="classify_node")
def classify_reply_node(state):
    if not state.get("reply"):
        return state
    
    result = call_llm_json(reply_classification_prompt(state["reply"]))
    state["classification"] = result
    print("➡️ classify_node")
    return state

def route_reply(state):
    if not state.get("reply"):
        return "no_reply"
    return state["classification"]["type"]

@observe(name="objection_node")
def objection_node(state):
    context = f"""
    Name: {state['name']}
    Company: {state['company']}
    Email: {state.get('email')}
    History: {state.get('history')}
    """

    state["response"] = call_llm(objection_prompt(context, state["reply"], state.get("rag_context", "")))
    return state

@observe(name="positive_node")
def positive_node(state):
    state["response"] = call_llm(
        f"User is interested. Push for meeting \nReply: {state['reply']}"
    )
    return state

@observe(name="neutral_node")
def neutral_node(state):
    state["response"] = call_llm(
        f"Respond casually and continue conversation.\nReply: {state['reply']}"
    )
    return state 

@observe(name="rag_node")
def rag_node(state):
    print("➡️ rag_node")

    retriever = get_retriever(k=3)

    if state.get("reply"):
        query = state["reply"]
    else:
        query = f"""
        Generate sales context for:
        Company: {state['company']}
        Industry: {state['enrichment'].get('industry')}
        Pain Points: {state['enrichment'].get('pain_points')}
        """
    docs = retriever.invoke(query)

    context = "\n\n".join(doc.page_content for doc in docs)

    state["rag_context"] = context

    return state