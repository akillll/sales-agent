from langfuse import observe
from langfuse.openai import OpenAI
from openai import OpenAI
from config import OPENAI_API_KEY
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

__all__ = ["client", "observe"]