from fastapi import FastAPI


# Register Routes
from .api.routes.resumeRoute.resumeGenerateRoute import router as resumeGeneratorRouter


app = FastAPI(
    title="The Resume Manager",
    description="A Simple Resume Generator",
    version="0.1",
    docs_url="/",
)

app.include_router(resumeGeneratorRouter, tags=["Resume"], prefix="/api/v1/generate")



@app.get("/")
def read_root():
    return {"Hello": "World"}

