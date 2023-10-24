from fastapi import APIRouter
from fastapi.responses import FileResponse
from ....models.ErrorResponse import ErrorResponse
import os
import json

router = APIRouter()

class ResumeGetErrorResponse(ErrorResponse):
    pass

@router.get("/resume/{uuid}")
async def get_resume(uuid: str):
    root = "./data/"
    folder_name = uuid
    file_name = "/Resume_Final.pdf"
    absolute_path = root + folder_name + file_name
    job_data = {}

    if not os.path.exists(absolute_path):
        return ResumeGetErrorResponse("error", 404, "Invalid Resume Requested.", {"uuid": uuid})

    # import a json file
    with open(root + folder_name + "/details.json") as json_file:
        job_data = json.load(json_file)

    employer_name = "_".join(job_data["employer_name"].split(" "))
    job_role = "_".join(job_data["job_role"].split(" "))
    job_number = job_data["job_Number"]
    export_name = "Anshil_P_" + employer_name + "_" + job_role + "_" + job_number + "_" + job_data["GeneratedOn"].split(" ")[0] + "_Resume.pdf"
    
    headers = {
        "Content-Disposition": "attachment; filename=" + export_name + ";"
    } 

    return FileResponse(absolute_path, filename=export_name, headers=headers, media_type="application/pdf")