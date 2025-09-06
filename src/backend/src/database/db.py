from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from .models import Challenge, ChallengeQuota

def get_challenge_quota(db: Session, user_id: int) -> ChallengeQuota:
    try:
        challenge_quota = db.query(ChallengeQuota).filter(ChallengeQuota.user_id == user_id).first()
        if challenge_quota is None:
            challenge_quota = ChallengeQuota(user_id=user_id)
            db.add(challenge_quota)
        return challenge_quota
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_challenge_quota(db: Session, user_id: int) -> ChallengeQuota:
    try:
        challenge_quota = ChallengeQuota(user_id=user_id)
        db.add(challenge_quota)
        db.commit()
        db.refresh(challenge_quota)
        return challenge_quota
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def reset_challenge_quota(db: Session, quota: ChallengeQuota) -> ChallengeQuota | None:
    try:
        quota_reset_date = datetime.now()
        quota_sub = (quota_reset_date - quota.last_reset_date).total_seconds() / 60
        if quota_sub > 30:
            db.query(ChallengeQuota).filter(ChallengeQuota.id == quota.id).update(
                {
                    "quota_remaining": 50, 
                    "last_reset_date": quota_reset_date
                }
            )
            db.commit()
            db.refresh(quota)
            return quota
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_challenge(
    db: Session,
    difficulty: str,
    date_created: datetime,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str
) -> Challenge:
    try:
        challenge = Challenge(
            difficulty=difficulty,
            date_created=date_created,
            title=title,
            options=options,
            correct_answer_id=correct_answer_id,
            explanation=explanation
        )
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
        return challenge
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_challenges(db: Session, user_id: int) -> list[Challenge]:
    try:
        return db.query(Challenge).filter(Challenge.correct_answer_id == user_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


