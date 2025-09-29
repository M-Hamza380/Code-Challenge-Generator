import os
from dotenv import load_dotenv
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from fastapi import HTTPException, Request
from typing import Dict, Any


load_dotenv()


SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}
JWT_KEY = os.getenv('JWT_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_ID = "gemini-2.0-flash"
CLERK_WEBHOOK_SECRET = os.getenv('CLERK_WEBHOOK_SECRET')
clerk_sdk = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))

def authenticate_and_get_user_details(request: Request) -> Dict[str, Any | None]:
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                jwt_key=JWT_KEY,
                authorized_parties=["http://localhost:5173", "http://localhost:5174", "http://localhost:4173"]
            )
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = request_state.payload.get("sub") if request_state.payload else None

        return {'user_id': user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
