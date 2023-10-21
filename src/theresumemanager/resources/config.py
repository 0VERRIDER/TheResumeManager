import os
from dotenv import load_dotenv
from ..core.tools.dictionary.dictTools import dict2obj
load_dotenv()


required_env_vars = {
    "FIGMA_ACCESS_KEY": os.getenv("FIGMA_ACCESS_KEY"),
    "FIGMA_PROJECT_ID" : os.getenv("FIGMA_PROJECT_ID"),
    "FIGMA_DESIGN_IDS" : os.getenv("FIGMA_DESIGN_IDS").split(","),
    "PORT" : os.getenv("PORT")
}

env = dict2obj(required_env_vars)

figma_config = {
    "file_id": env.FIGMA_PROJECT_ID,
    "personal_access_token": env.FIGMA_ACCESS_KEY,
    "design_ids": env.FIGMA_DESIGN_IDS,
    "export_format": "pdf"
}