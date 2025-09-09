from openai import OpenAI
from typing import Dict, Any

from src.backend.src.contants import OPENAI_CLIENT

client = OpenAI(api_key=OPENAI_CLIENT)

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
        

