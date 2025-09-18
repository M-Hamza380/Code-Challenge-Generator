from fastapi import APIRouter, Request, HTTPException
from svix.webhooks import Webhook
import json

from ..database.db import create_challenge_quota
from ..contants import CLERK_WEBHOOK_SECRET
from ..utilities.logger import logger

router = APIRouter()

@router.post("/clerk")
async def handle_user_created(request: Request):
    if not CLERK_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET is not set")
    
    db = request.app.state.db
    body = await request.body()
    playload = body.decode('utf-8')
    headers = dict(request.headers)
    
    try:
        wh = Webhook(CLERK_WEBHOOK_SECRET)
        wh.verify(playload, headers)
        
        data = json.loads(playload)
        
        if data.get('type') != 'user.created':
            return {'status': 'ignored'}
        
        user_data = data.get('data', {})
        user_id = user_data.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in payload")
        
        create_challenge_quota(db, user_id)
        
        return {'status': 'success'}
        
    except Exception as e:
        logger.error(f"Error in handle_user_created: {str(e)}", exc_info=True)
        raise HTTPException(status_code=401, detail=str(e))
            

