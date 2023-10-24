from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# Register Routes
from .api.routes.resumeRoute.resumeGenerateRoute import router as resumeGeneratorRouter
from .api.routes.resumeRoute.resumeGetRoute import router as resumeGetRouter


app = FastAPI(
    title="The Resume Manager",
    description="A Simple Resume Generator",
    version="0.1",
)

origins = [
    "http://localhost:5501",
    "http://127.0.0.1:5501"
    "https://resume.anshil.me",
    "http://10.42.0.127:5501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resumeGeneratorRouter, tags=["Resume"], prefix="/api/v1/resume")
app.include_router(resumeGetRouter, tags=["Resume"], prefix="/api/v1/get")

app.mount("/", StaticFiles(directory="src/theresumemanager/resources", html=True), name="ui")


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

