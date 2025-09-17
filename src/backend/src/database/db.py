from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta

from .models import Challenge, ChallengeQuota

def get_challenge_quota(db: Session, user_id: int) -> ChallengeQuota:
    try:
        challenge_quota = db.query(ChallengeQuota).filter(ChallengeQuota.user_id == user_id).first()
        if challenge_quota is None:
            challenge_quota = ChallengeQuota(
                user_id=user_id,
                quota_remaining=50,
                last_reset_date=datetime.now()
            )
            db.add(challenge_quota)
            db.commit()
            db.refresh(challenge_quota)
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
        time_diff = quota_reset_date - quota.last_reset_date
        should_reset = time_diff > timedelta(hours=2)
        if should_reset:
            result = db.query(ChallengeQuota).filter(ChallengeQuota.user_id == quota.user_id).update(
                {
                    "quota_remaining": 50, 
                    "last_reset_date": quota_reset_date
                }
            )
            db.commit()
            if result > 0:
                db.refresh(quota)
        return quota
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str
) -> Challenge:
    try:
        challenge = Challenge(
            difficulty=difficulty,
            created_by=created_by,
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
        challenges = db.query(Challenge).filter(Challenge.created_by == str(user_id)).order_by(
            Challenge.date_created.desc()
        ).all()
        return challenges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


