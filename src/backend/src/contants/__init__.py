import os
from dotenv import load_dotenv
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from fastapi import HTTPException


load_dotenv()

COLLECTION_NAME = ""
MONGODB_URI = os.environ.get("MONGODB_URI")
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}

clerk_sdk = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))

def authenticate_and_get_user_details(request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                jwt_key=os.getenv('JWT_KEY'),
                authorized_parties=["http://localhost:5173", "http://localhost:5174"]
            )
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = request_state.payload.get("sub") if request_state.payload else None

        return {'user_id': user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
