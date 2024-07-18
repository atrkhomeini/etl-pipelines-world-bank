import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


project_name = "etl_world_bank"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"artifacts/raw/__init__.py",
    f"artifacts/transform/__init__.py",
    f"utils/__init__.py",
    f"config/configuration.py",
    f"src/pipeline/",
    f"test/__init__.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
]



for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")
