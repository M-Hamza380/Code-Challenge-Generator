import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient, ASCENDING, DESCENDING

from src.routers.router import router
from src.contants import DEBUG, MONGODB_URI, DB_NAME
from src.utilities.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.warning("FastAPI server is starting up!")
        client = AsyncMongoClient(MONGODB_URI, tz_aware=True)
        
        result = await client.admin.command("ping")
        if result.get("ok") != 1:
            raise HTTPException(status_code=500, detail="Could not connect to MongoDB")
        
        db = client.get_database(DB_NAME)
        
        await db.challenge_quotas.create_index("user_id", unique=True)
        await db.challenges.create_index([("created_by", ASCENDING), ("date_created", DESCENDING)], unique=False)
        
        app.state.mongo_client = client
        app.state.db = db
        yield 
        
        if hasattr(app.state.db, 'db'):
            app.state.db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

app = FastAPI(
    title="Code challenge generator backend",
    description= "A challenge generator app backend with SQLite and Front-End in React",
    version="0.0.1",
    lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def index():
    return {'message': 'Hello World!'}


if __name__ == "__main__":
    if DEBUG:
        logger.info("Running in DEBUG mode")
        uvicorn.run("server:app", reload=True, host="localhost", port=1243)
    else:
        logger.info("Running in PRODUCTION mode")
        uvicorn.run("server:app", host="localhost", port=1243)
