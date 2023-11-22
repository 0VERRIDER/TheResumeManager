from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .resources.config import env, strings, paths
from .data.database.connection import db_cursor

# Register Routes
from .api.routes.resumeRoute.resumeGenerateRoute import router as resumeGeneratorRouter
from .api.routes.resumeRoute.resumeGetRoute import router as resumeGetRouter
from .api.routes.resumeRoute.resumeUpdateRoute import router as resumeUpdateRouter
from .api.routes.figmaRoute.figmaGetRoute import router as figmaGetRouter

app = FastAPI(
    title = strings.APP_NAME,
    description = strings.APP_DESCRIPTION,
    version = strings.APP_VERSION,
)

origins = env.ALLOWED_DEV_ORIGINS if env.ENV == "dev" else env.ALLOWED_ORIGINS 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_resume_path = f"{paths.BASE_API_PATH}{paths.RESUME_CREATE_URL}"

app.include_router(
    resumeGeneratorRouter, 
    tags=["Resume"], 
    prefix=create_resume_path
)

app.include_router(
    resumeGetRouter, 
    tags=["Resume"], 
    prefix=f"{paths.BASE_API_PATH}{paths.RESUME_URL}",
)

app.include_router(
    resumeUpdateRouter, 
    tags=["Resume"], 
    prefix=f"{paths.BASE_API_PATH}{paths.RESUME_URL}",
)

app.include_router(
    figmaGetRouter, 
    tags=["Figma"], 
    prefix=f"{paths.BASE_API_PATH}{paths.FIGMA_URL}",
)


# GET path: /
app.mount(
    paths.HOME_URL, 
    StaticFiles(
        directory="src/theresumemanager/resources/static", 
        html=True
    ), 
    name = strings.STATIC_FILE_NAME
)