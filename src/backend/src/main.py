import os
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from bson import ObjectId
from pymongo import AsyncMongoClient
from datetime import datetime

from contants import COLLECTION_NAME
from database.db import ChallengeDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        uri = ""
        client = AsyncMongoClient(uri)
        db = client.get_database("")

        pong = await db.command('ping')
        if int(pong['ok']) != 1:
            raise Exception('Cluster connection is not ok!')
        
        coding = db.get_collection(COLLECTION_NAME)
        app.state.coding_db = ChallengeDB(coding)

        yield

        await client.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app = FastAPI(
    title="Coding Challenge Generator",
    version="0.1.0",
    description="Coding Challenge Generator APP",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

