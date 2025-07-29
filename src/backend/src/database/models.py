from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
    def from_doc(doc) -> "Challenge":
        return Challenge(
            _id = str(doc['_id']),
            difficulty = doc['difficulty'],
            date_created = doc.get('date_created'),
            created_by = doc.get('created_by'),
            title = doc.get('title'),
            options = doc.get('options'),
            correct_answer_id = doc.get('correct_answer_id'),
            explanation = doc.get('explanation')
        )


class ChallengeQuota(BaseModel):
    user_id: Optional[str] = Field(alias='_id')
    quota_remaining: int = Field(default=50, description='remaining quota')
    last_reset_date: datetime = Field(default_factory=datetime.now, description='user reset his/her quota')

    @staticmethod
    def from_doc(doc) -> "ChallengeQuota":
        return ChallengeQuota(
            _id = str(doc['_id']),
            quota_remaining = doc.get('quota_remaining'),
            last_reset_date = doc.get('last_reset_date')
        )

