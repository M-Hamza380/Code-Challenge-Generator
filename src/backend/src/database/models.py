from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Challenge(BaseModel):    
    id: str = Field(..., description="MongoDB _id as primary key")
    difficulty: str 
    date_created: datetime 
    created_by: str 
    title: str 
    options: List[str] 
    correct_answer_id: int 
    explanation: str 
    

class ChallengeQuota(BaseModel):
    id: str
    user_id: str 
    quota_remaining: int 
    last_reset_date: datetime
    

