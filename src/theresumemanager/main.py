from fastapi import FastAPI


# Register Routes
from .api.routes.resumeRoute.resumeRoute import router as resumeRouter


app = FastAPI()

app.include_router(resumeRouter, tags=["Resume"], prefix="/api/v1/generate")



@app.get("/")
def read_root():
    return {"Hello": "World"}

