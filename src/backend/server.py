import uvicorn
from src.main import app

if __name__ == "__main__":
    uvicorn.run(app, reload=True, host="0.0.0.0", port=1243)
