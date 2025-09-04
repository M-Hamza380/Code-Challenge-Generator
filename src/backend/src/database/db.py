from bson import ObjectId
from pymongo.client_session import ClientSession
from typing import Any, Dict

from .models import Challenge, ChallengeQuota


class ChallengeDB:

    def __init__(self, challenges: Any):
        self._challenges = challenges
        
    
    async def check_user_quota(self, user_id: str, session: ClientSession | None = None):
        quota = await self.get_challenge_quota(user_id, session=session)
        return quota
    
    async def get_challenge_quota(self, user_id: str, session: ClientSession | None = None):
        return ChallengeQuota.from_doc(await self._challenges.find_one({'_id': ObjectId(user_id)}, session=session))
    
    async def create_challenge(self, challenge_data: Dict[str, Any], session: ClientSession | None = None):
        response = await self._challenges.insert_one(
            {'challenge_data': challenge_data},
            session = session
            )
        return str(response.inserted_id)
    
    async def get_challenge(self, challenge_id: str, session: ClientSession | None = None):
        return Challenge.from_doc(await self._challenges.find_one({'_id': ObjectId(challenge_id)}))
    

