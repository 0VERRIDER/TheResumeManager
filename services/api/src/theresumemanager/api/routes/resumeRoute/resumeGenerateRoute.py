from fastapi import APIRouter
from fastapi.responses import FileResponse
from ....models.Response import Response
from datetime import datetime
from ....core.tools.hashing.hashingTools import generate_hash_function
from ....core.functions.resume.resumeFunction import generate_resume_pdf
from ....resources.config import figma_config

router = APIRouter()

class ResumeGenerateResponse(Response):
    pass

@router.get("")
async def generate_resume(job_number: str, employer_name: str, job_role: str, application_link: str = ""):
    dateTime = datetime.now()
    hash_func = generate_hash_function("sha256")
    uuid = hash_func(employer_name + str(job_number) + job_role)

    job_config = {
    "uuid": uuid,
    "job_id" : employer_name + "_" + job_role + "_" + str(job_number) + "_" + "_".join(str(dateTime).split(" ")),
    "job_role": job_role,
    "GeneratedOn": str(dateTime),
    "employer_name": employer_name,
    "job_number": job_number,
    "application_link": application_link
    }

    file = generate_resume_pdf(figma_config, job_config, export_location="./data/")
    # file_name = "Resume_" + job_config["job_id"] + ".pdf"
    # headers = {
    #     "Content-Disposition": "inline; filename=" + file_name + ";"
    # } 
    # return FileResponse(file, filename=file_name, headers=headers, media_type="application/pdf")

    return ResumeGenerateResponse("success", 200, "Resume Generated Successfully", {"uuid": job_config["uuid"]})