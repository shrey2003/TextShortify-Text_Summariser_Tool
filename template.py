import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(levelname)s %(message)s:')

project_name = "Docqna"

list_of_files = [
    ".github/workflows/.gitkeep", 
    f"src/{project_name}/__init__.py", 
    f"src/{project_name}/components/__init__.py", 
    f"src/{project_name}/utils/__init__.py",  
    f"src/{project_name}/utils/common.py",  
    f"src/{project_name}/logging/__init__.py",  
    # f"src/{project_name}/config/__init__.py", 
    # f"src/{project_name}/config/configuration.py",  
    f"src/{project_name}/pipeline/__init__.py",  
    f"src/{project_name}/entity/__init__.py",  
    # f"src/{project_name}/constants/__init__.py",  
    "config/config.yaml", 
    "main.py",
    "params.yaml",  
    "Dockerfile",  
    "requirements.txt",  
    "setup.py",  
    "research/trials.ipynb",  
]


for filepath in list_of_files:
    path = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    # Create directory if it doesn't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    # Create file if it doesn't exist or is empty
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
       
        logging.info(f"Creating file: {filepath} if it doesn't exist or is empty")
        with open(filepath, 'w') as f:
            pass  # Empty file created
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"File already exists: {filename}")

