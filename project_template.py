import os, logging
from pathlib import Path


logging.basicConfig(
    format="[ [%(asctime)s] : %(levelname)s : %(name)s : %(pathname)s : %(module)s : %(lineno)d : %(message)s ]",
    level=logging.INFO
)


list_of_files = [
    f"src/backend/src/__ini__.py",
    f"src/backend/src/contants/__init__.py",
    f"src/backend/src/utilities/__init__.py",
    f"src/backend/src/utilities/logger.py",
    f"src/backend/src/database/__ini__.py",
    f"src/backend/src/database/models.py",
    f"src/backend/src/database/db.py",
    f"src/backend/src/ai/__init__.py",
    f"src/backend/src/ai/ai_generator.py",
    f"src/backend/src/ai/prompts.py",
    f"src/backend/src/routers/__ini__.py",
    f"src/backend/src/routers/router.py",
    f"src/backend/src/routers/challenge.py",
    f"src/backend/src/routers/webhooks.py",
    f"src/backend/server.py",
    f"src/backend/__init__.py",
    f"src/backend/.env",
    f"src/backend/.env-example",
    f"src/backend/.dockerignore",
    f"src/backend/Dockerfile",
    "nginx/nginx.conf",
    "docker-compose.yaml",
]


for file in list_of_files:
    if file:
        filepath = Path(file)
        file_dir, file_name = os.path.split(filepath)

        if file_dir != "":
            os.makedirs(file_dir, exist_ok=True)
            logging.info(f"Creating directory: {file_dir} for file: {file_name}!")
        
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(file, 'w') as f:
                pass
                logging.info(f"Creating empty file: {file}!")
        else:
            logging.info(f"That {file} already exists!")
    else:
        logging.info(f"File: {file} is empty!")
