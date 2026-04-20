from config import OPENAI_API_KEY, MODEL
import json
import time
from services.observability import client


def call_llm(prompt: str, temperature=0.7, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                timeout=15,
            )
            output = response.choices[0].message.content
            return output
        

        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(1)

def call_llm_json(prompt: str, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{
                    "role": "system",
                    "content": "You must return valid json only. No explanation"
                },
                {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
                timeout=15,
            )
            content = response.choices[0].message.content
            return json.loads(content)
        
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(1)

def stream_llm(prompt: str):
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content