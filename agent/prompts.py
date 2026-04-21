def enrichment_prompt(name, company):
    return f"""
Given the following prospect:

Name: {name}
Company: {company}

Return:
- role
- company_size
- industry
- pain_points

"""


def email_prompt(data):
    return f"""
Write a personalized cold email.

Prospect:
Name: {data['name']}
Company: {data['company']}
Role: {data['enrichment']['role']}
Industry: {data['enrichment']['industry']}
Pain Points: {data['enrichment']['pain_points']}

Product Knowledge:
{data.get('rag_context', '')}

Keep it short, human, and engaging. Use product knowledge if relevant
"""


def reply_classification_prompt(reply):
    return f"""
Classify this reply:

"{reply}"

Return JSON:
{{
  "type": "positive | objection | neutral",
  "reason": "..."
}}
"""


def objection_prompt(context, reply, rag_context):
    return f"""
Handle this objection:

Reply: {reply}

Context:
{context}

Product Knowledge:
{rag_context}

Be polite, acknowledge concern, and re-engage. Use knowledge base to respond and Address objection clearly.
"""