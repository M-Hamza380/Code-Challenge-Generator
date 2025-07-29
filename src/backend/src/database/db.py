from bson import ObjectId
# from pymongo.collection import Collection
from typing import Any
from uuid import uuid4

from models import Challenge, ChallengeQuota


class ChallengeDB:

    def __init__(self, challenges: Any):
        self._challenges = challenges
    
    async def create_challenge(self, challenge_data: dict, session = None):
        response = await self._challenges.insert_one(
            {'challenge_data': challenge_data},
            session = session
            )
        return str(response.inserted_id)
    
    async def get_challenge(self, challenge_id: str, session = None):
        return Challenge.from_doc(await self._challenges.find_one({'_id': ObjectId(challenge_id)}))
    

