from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import Dict, Any


class Challenge(BaseModel):
    id: Optional[str] = Field(alias='_id')
    difficulty: str = Field(default_factory=str, description='coding challenge level')
    date_created: datetime = Field(default_factory=datetime.now, description='current datetime')
    created_by: str = Field(default_factory=str, description='store the ID of clerk user who created this challenge')
    title: str = Field(default_factory=str, description='coding challenge question')
    options: str = Field(default_factory=str, description='coding challenge options')
    correct_answer_id: int = Field(default_factory=int, description='coding challenge correct answer')
    explanation: str = Field(default_factory=str, description='coding challenge explanation')

    @staticmethod
    def from_doc(doc: Dict[str, Any]) -> "Challenge":
        return Challenge(
            _id = str(doc['_id']),
            difficulty = doc['difficulty'],
            date_created = doc['date_created'],
            created_by = doc['created_by'],
            title = doc['title'],
            options = doc['options'],
            correct_answer_id = doc['correct_answer_id'],
            explanation = doc['explanation']
        )


class ChallengeQuota(BaseModel):
    user_id: Optional[str] = Field(alias='_id')
    quota_remaining: int = Field(default=50, description='remaining quota')
    last_reset_date: datetime = Field(default_factory=datetime.now, description='user reset his/her quota')

    @staticmethod
    def from_doc(doc: Dict[str, Any]) -> "ChallengeQuota":
        return ChallengeQuota(
            _id = str(doc['_id']),
            quota_remaining = doc['quota_remaining'],
            last_reset_date = doc['last_reset_date']
        )

