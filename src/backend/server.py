import uvicorn
from src.main import app

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True, host="localhost", port=1243)
