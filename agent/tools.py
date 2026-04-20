from services.llm import call_llm_json
from agent.prompts import enrichment_prompt

def enrich_prospect(name: str, company: str):
    prompt = enrichment_prompt(name, company)
    return call_llm_json(prompt)