import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker

from src.routers.router import router
from src.database.models import Base, engine
from src.contants import DEBUG
from src.utilities.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        app.state.db = SessionLocal()
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
