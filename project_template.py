import os, logging
from pathlib import Path


logging.basicConfig(
    format="[ [%(asctime)s] : %(levelname)s : %(name)s : %(pathname)s : %(module)s : %(lineno)d : %(message)s ]",
    level=logging.INFO
)


list_of_files = [
    f"src/backend/__ini__.py",
    f"src/backend/main.py",
    f"src/backend/routers/__ini__.py",
    f"src/backend/routers/route.py",
    f"src/backend/database/__ini__.py",
    f"src/backend/database/model.py",
]


for file in list_of_files:
    filepath = Path(file)
    file_dir, file_name = os.path.split(filepath)

    if filepath != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for file: {file_name}!")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(file, 'w') as f:
            pass
            logging.info(f"Creating empty file: {file}!")
    else:
        logging.info(f"That {file} already exists!")
