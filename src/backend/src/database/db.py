from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database
from pymongo.errors import PyMongoError
from uuid import uuid4
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Dict

from .models import Challenge, ChallengeQuota

DEFAULT_QUOTA = 50

def _serialize_id(doc: Dict | None) -> Dict | None:
    if not doc:
        return None

    doc['id'] = str(doc['_id'])
    del doc['id']
    return doc

def get_challenge_quota(db: Database, user_id: str) -> Dict | None:
    try:
        col = db.get_collection("challenge_quotas")
        challenge_quota = col.find_one({"user_id": user_id})
        
        if challenge_quota is None:
            challenge_quota = {
                "user_id": user_id,
                "quota_remaining": DEFAULT_QUOTA,
                "last_reset_date": datetime.now()
            }
            col.insert_one(challenge_quota)
            challenge_quota = col.find_one({"user_id": user_id})
        
        return _serialize_id(challenge_quota)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_challenge_quota(db: Database, user_id: str) -> Dict | None:
    try:
        col = db.get_collection("challenge_quotas")
        challenge_quota = {
            "user_id": user_id,
            "quota_remaining": DEFAULT_QUOTA,
            "last_reset_date": datetime.now()
        }
        col.insert_one(challenge_quota)
        return _serialize_id(col.find_one({"user_id": user_id}))
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

def reset_challenge_quota(db: Database, quota: ChallengeQuota) -> Dict | None:
    try:
        col = db.get_collection("challenge_quotas")
        quota_reset_date = datetime.now()
        last_reset = quota.last_reset_date
        if not last_reset:
            last_reset = quota_reset_date
        
        time_diff = quota_reset_date - last_reset
        should_reset = time_diff > timedelta(hours=2)
        if should_reset:
            result = col.update_one(
                {"_id": ObjectId(quota.id)},
                {"$set": {"quota_remaining": DEFAULT_QUOTA, "last_reset_date": quota_reset_date}},
            )
            if result.modified_count > 0:
                updated = col.find_one({"_id": ObjectId(quota.id)})
                return _serialize_id(updated)
        return _serialize_id(quota.__dict__) if hasattr(quota, '__dict__') else dict(quota)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_challenge(
    db: Database,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str
) -> Dict | None:
    try:
        col = db.get_collection("challenges")
        challenge = {
            "difficulty": difficulty,
            "date_created": datetime.now(),
            "created_by": created_by,
            "title": title,
            "options": options,
            "correct_answer_id": correct_answer_id,
            "explanation": explanation
        }
        col.insert_one(challenge)
        saved = col.find_one({"_id": ObjectId(challenge["id"])})
        challenge = _serialize_id(saved)
        return challenge
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_challenges(db: Database, user_id: int) -> list[Dict | None]:
    try:
        col = db.get_collection("challenges")
        challenges = col.find({"created_by": str(user_id)}).sort("date_created", -1)
        return [_serialize_id(challenge) for challenge in challenges]
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


