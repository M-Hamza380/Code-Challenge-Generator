from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers.router import router
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker

from .database.models import Base, engine

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
    return {'Hello': 'world'}
