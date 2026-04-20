from agent.tools import enrich_prospect
from services.llm import call_llm, call_llm_json
from agent.prompts import (
    email_prompt,
    reply_classification_prompt,
    objection_prompt
)
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

    state["response"] = call_llm(objection_prompt(context, state["reply"]))
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