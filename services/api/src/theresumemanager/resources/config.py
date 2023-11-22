import os
import json
from dotenv import load_dotenv
from ..core.tools.dictionary.dictTools import dict2obj
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
load_dotenv()


# Register The Font
pdfmetrics.registerFont(
TTFont('Poppins', "./src/theresumemanager/resources/fonts/Poppins-Medium.ttf")
)

required_env_vars = {
    "ENV": os.getenv("ENV"),
    "ALLOWED_ORIGINS": json.loads(os.getenv("ALLOWED_ORIGINS")),
    "ALLOWED_DEV_ORIGINS": json.loads(os.getenv("ALLOWED_DEV_ORIGINS")),
    "FIGMA_BASE_URL": os.getenv("FIGMA_BASE_URL"),
    "FIGMA_ACCESS_KEY": os.getenv("FIGMA_ACCESS_KEY"),
    "FIGMA_PROJECT_ID" : os.getenv("FIGMA_PROJECT_ID"),
    # "FIGMA_RESUME_DESIGN" : json.loads(os.getenv("FIGMA_RESUME_DESIGN")),
    "PORT" : os.getenv("PORT", 8000),
    "DATABASE_HOST" : os.getenv("DATABASE_HOST"),
    "DATABASE_PORT" : os.getenv("DATABASE_PORT", "3306"), # "3306
    "DATABASE_USER" : os.getenv("DATABASE_USER"),
    "DATABASE_PASSWORD" : os.getenv("DATABASE_PASSWORD"),
    "DATABASE_NAME" : os.getenv("DATABASE_NAME")
}

strings = dict2obj(json.load(open("src/theresumemanager/resources/strings.json", "r")))
paths = dict2obj(json.load(open("src/theresumemanager/resources/paths.json", "r")))
designs = json.load(open("src/theresumemanager/resources/designs.json", "r"))

env = dict2obj(required_env_vars)

figma_config = {
    "file_id": env.FIGMA_PROJECT_ID,
    "personal_access_token": env.FIGMA_ACCESS_KEY,
    "resume": designs,
    "export_format": "pdf"
}