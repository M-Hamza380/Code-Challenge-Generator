from fastapi import APIRouter

from .challenge import router as challenge_router
from .webhooks import router as webhooks_router

router = APIRouter()

router.include_router(challenge_router, prefix="/api")
router.include_router(webhooks_router, prefix="/webhooks")

