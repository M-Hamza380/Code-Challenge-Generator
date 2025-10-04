from fastapi import (
    APIRouter,
    HTTPException,
    Request
)
from pydantic import BaseModel, Field
import json
from datetime import datetime

from ..contants import authenticate_and_get_user_details
from ..database.db import (
    get_challenge_quota,
    create_challenge_quota,
    get_user_challenges,
    reset_challenge_quota,
    create_challenge
)
from ..ai.ai_generator import generate_challenge_with_ai
from ..utilities.logger import logger

router = APIRouter()

def get_user_details(request: Request):
    try:
        user_details = authenticate_and_get_user_details(request)
        
        user_id = user_details.get("user_id")
        if not user_details or user_id is None:
            logger.error("Authentication failed: Invalid or missing token")
            raise HTTPException(
                status_code=401, 
                detail="Authentication failed: Please log in again"
            )
        return user_details, user_id
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=401, 
            detail="Authentication failed: Invalid token"
        )


class ChallengeRequest(BaseModel):
    difficulty: str = Field(default_factory=str, description="The difficulty level of the challenge user select")
    
    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "easy"
            }
        }
    

@router.post("/generate-challenge")
async def generate_challenge(request: Request, challenge_request: ChallengeRequest):
    try:
        user_details, user_id = get_user_details(request)
        db = request.app.state.db
        
        # Get or create quota
        quota = get_challenge_quota(db, user_id)
        if not quota:
            quota = create_challenge_quota(db, user_id)
        
        # Reset quota if needed
        quota = reset_challenge_quota(db, quota)
        
        if quota:
            if quota.get("quota_remaining", 0) <= 0:
                raise HTTPException(
                    status_code=429, 
                    detail="Quota has been exhausted for today"
                )
        else:
            raise HTTPException(
                status_code=500, 
                detail="Quota not found"
            )
            
        # Generate challenge
        challenge_data = generate_challenge_with_ai(challenge_request.difficulty)
        
        # Create challenge with correct date
        new_challenge = create_challenge(
            db=db,
            difficulty=challenge_request.difficulty,
            created_by=user_id,
            title=challenge_data["title"],
            options=json.dumps(challenge_data["options"]),
            correct_answer_id=challenge_data["correct_answer_id"],
            explanation=challenge_data["explanation"]
        )
        
        # Update quota
        quota.get("quota_remaining") -= 1
        db.commit()
        db.refresh(quota)
        
        return {
            "id": new_challenge.id,
            "difficulty": new_challenge.difficulty,
            "title": new_challenge.title,
            "options": json.loads(new_challenge.options),
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp": new_challenge.date_created.isoformat()
        }
    except Exception as e:
        logger.error(f"Error in generate_challenge: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-history")
async def my_history(request: Request):
    try:
        user_details, user_id = get_user_details(request)
        db = request.app.state.db
        
        challenges = get_user_challenges(db, user_id)
        response_data = {
            "challenges": challenges
        }
        return response_data
    except Exception as e:
        logger.error(f"Error in my_history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quota")
async def get_quota(request: Request):
    try:
        user_details, user_id = get_user_details(request)
        
        if not hasattr(request.app.state, 'db'):
            logger.error("Database connection not initialized")
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        db = request.app.state.db
        challenge_quota = get_challenge_quota(db, user_id)
        if not challenge_quota:
            challenge_quota = create_challenge_quota(db, user_id)
            return {
                "user_id": user_id,
                "quota_remaining": 0,
                "last_reset_date": datetime.now()
            }
        quota_reset = reset_challenge_quota(db, challenge_quota)
        return {
            "user_id": user_id,
            "quota_remaining": quota_reset.quota_remaining,
            "last_reset_date": quota_reset.last_reset_date.isoformat()
        }
    except Exception as e:
        logger.error(f"Error in get_quota: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



