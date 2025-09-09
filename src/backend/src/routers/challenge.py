from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
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
from ..database.models import get_db
from ..ai.ai_generator import generate_challenge_with_ai

router = APIRouter()

def get_user_details(request: Request):
    try:
        user_details = authenticate_and_get_user_details(request)
        if user_details['user_id'] is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = user_details['user_id']
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_details, user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChallengeRequest(BaseModel):
    difficulty: str = Field(default_factory=str, description="The difficulty level of the challenge user select")
    
    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "easy"
            }
        }
    

@router.post("/generate-challenge")
async def generate_challenge(request: Request, challenge_request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        user_details, user_id = get_user_details(request)
        quota = get_challenge_quota(db, user_id)
        
        if not quota:
            quota = create_challenge_quota(db, user_id)
        
        quota = reset_challenge_quota(db, quota)
        if quota is None:
            raise HTTPException(status_code=500, detail="Failed to reset challenge quota")
        
        quota_remaining = quota.quota_remaining.first()
        if quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota has been exhausted for today")
        
        challenge_data = generate_challenge_with_ai(challenge_request.difficulty)
        
        new_challenge = create_challenge(
            db,
            challenge_request.difficulty,
            datetime.now(),
            **challenge_data
        )
        
        if new_challenge.options is not None:
            options = json.loads(new_challenge.options.values)
        else:
            options = []
        
        quota_remaining -= 1
        db.commit()
        db.refresh(quota_remaining)
        
        return {
            "id": new_challenge.id,
            "difficulty": new_challenge.difficulty,
            "title": new_challenge.title,
            "options": options,
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-challenge")
async def my_history(request: Request, db: Session = Depends(get_db)):
    try:
        user_details, user_id = get_user_details(request)
        challenges = get_user_challenges(db, user_id)
        return {"challenges": challenges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    try:
        user_details, user_id = get_user_details(request)
        challenge_quota = get_challenge_quota(db, user_id)
        if not challenge_quota:
            return {
                "user_id": user_id,
                "quota_remaining": 0,
                "last_reset_date": datetime.now()
            }
        quota_reset = reset_challenge_quota(db, challenge_quota)
        return quota_reset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



