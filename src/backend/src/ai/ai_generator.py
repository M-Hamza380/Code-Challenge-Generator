from google import genai
from google.genai import types
from typing import Dict, Any
import json

from ..contants import GEMINI_API_KEY, MODEL_ID
from ..ai.prompts import SYSTEM_PROMPT
from ..utilities.logger import logger

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    try:
        # prepare the system and user prompts
        combined_prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            "Return a coding challenge in this exact JSON format:\n"
            "{\n"
            '    "title": "Your challenge title",\n'
            '    "options": ["option1", "option2", "option3", "option4"],\n'
            '    "correct_answer_id": 0,\n'
            '    "explanation": "Your explanation"\n'
            "}\n\n"
            f"Make it a {difficulty} difficulty challenge. Respond ONLY with the JSON."
        )
        contents = types.Content(
            parts=[types.Part(text=combined_prompt)],
            role='user'
        )
        
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[contents],
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )
        
        if not response or not response.text:
            logger.error("Empty response from Gemini API")
            return get_fallback_challenge(difficulty)
        
        # Clean the response text
        content = response.text.strip()
        
        # Try to find JSON content within the response
        try:
            # Remove any markdown code block indicators if present
            if content.startswith("```json"):
                content = content.replace("```json", "", 1)
            if content.startswith("```"):
                content = content.replace("```", "", 1)
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]
                
            content = content.strip()
            challenge_data = json.loads(content)
            
        except json.JSONDecodeError as je:
            logger.error(f"JSON decode error: {je}, Response: {content}")
            return get_fallback_challenge(difficulty)
        
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        if all(field in challenge_data for field in required_fields):
            return challenge_data
        else:
            logger.error(f"Invalid challenge data: {challenge_data}", exc_info=True)
            raise ValueError(f"Invalid challenge data: {challenge_data}")
        
    except Exception as e:
        logger.error(f"Error in generate_challenge_with_ai: {str(e)}", exc_info=True)
        return get_fallback_challenge(difficulty)
        
def get_fallback_challenge(difficulty: str) -> Dict[str, Any]:
    fallback_challenges = {
        "easy": {
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
        # Add more fallback challenges for different difficulties
    }
    return fallback_challenges.get(difficulty.lower(), fallback_challenges["easy"])
        

