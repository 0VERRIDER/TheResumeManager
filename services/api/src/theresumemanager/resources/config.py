import os
import json
from dotenv import load_dotenv
from ..core.tools.dictionary.dictTools import dict2obj
load_dotenv()


required_env_vars = {
    "ENV": os.getenv("ENV"),
    "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS").split(","),
    "ALLOWED_DEV_ORIGINS": os.getenv("ALLOWED_DEV_ORIGINS").split(","),
    "FIGMA_ACCESS_KEY": os.getenv("FIGMA_ACCESS_KEY"),
    "FIGMA_PROJECT_ID" : os.getenv("FIGMA_PROJECT_ID"),
    "FIGMA_DESIGN_IDS" : os.getenv("FIGMA_DESIGN_IDS").split(","),
    "PORT" : os.getenv("PORT"),
    "DATABASE_HOST" : os.getenv("DATABASE_HOST"),
    "DATABASE_PORT" : os.getenv("DATABASE_PORT", "3306"), # "3306
    "DATABASE_USER" : os.getenv("DATABASE_USER"),
    "DATABASE_PASSWORD" : os.getenv("DATABASE_PASSWORD"),
    "DATABASE_NAME" : os.getenv("DATABASE_NAME")
}

env = dict2obj(required_env_vars)

figma_config = {
    "file_id": env.FIGMA_PROJECT_ID,
    "personal_access_token": env.FIGMA_ACCESS_KEY,
    "design_ids": env.FIGMA_DESIGN_IDS,
    "export_format": "pdf"
}

strings = dict2obj(json.load(open("src/theresumemanager/resources/strings.json", "r")))
paths = dict2obj(json.load(open("src/theresumemanager/resources/paths.json", "r")))