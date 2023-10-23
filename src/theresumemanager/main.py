from fastapi import FastAPI


# Register Routes
from .api.routes.resumeRoute.resumeGenerateRoute import router as resumeGeneratorRouter
from .api.routes.resumeRoute.resumeGetRoute import router as resumeGetRouter


app = FastAPI(
    title="The Resume Manager",
    description="A Simple Resume Generator",
    version="0.1",
    docs_url="/",
)

app.include_router(resumeGeneratorRouter, tags=["Resume"], prefix="/api/v1/generate")
app.include_router(resumeGetRouter, tags=["Resume"], prefix="/api/v1/get")



# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

