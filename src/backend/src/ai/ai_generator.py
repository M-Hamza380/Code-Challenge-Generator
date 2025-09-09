from openai import OpenAI
from typing import Dict, Any
import json

from ..contants import OPENAI_API_KEY
from ..ai.prompts import SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content is not None:
            challenge_data = json.loads(content)
        else:
            raise ValueError("Invalid response from OpenAI API")
        
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        if all(field in challenge_data for field in required_fields):
            return challenge_data
        else:
            raise ValueError(f"Invalid challenge data: {challenge_data}")
        
    except Exception as e:
        print("Error in generate_challenge_with_ai :", e)
        return {
            "title": "Basic Python List Operation",
            "options": [
                "my_list.append(5)",
                "my_list.add(5)",
                "my_list.push(5)",
                "my_list.insert(5)",
            ],
            "correct_answer_id": 0,
            "explanation": "In Python, append is the correct method to add an element to the end of a list."
        }
        
    
        

