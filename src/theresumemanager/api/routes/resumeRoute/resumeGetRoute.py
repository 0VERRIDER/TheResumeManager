from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
import json

router = APIRouter()

@router.get("/{uuid}")
async def get_resume(uuid: str):
    root = "./data/"
    folder_name = uuid
    file_name = "/Resume_Final.pdf"
    absolute_path = root + folder_name + file_name
    job_data = {}

    if not os.path.exists(absolute_path):
        return {"message": "File not found"}

    # import a json file
    with open(root + folder_name + "/details.json") as json_file:
        job_data = json.load(json_file)

    export_name = "Anshil_P_" + job_data["employer_name"] + "_" + job_data["job_role"] + "_" + job_data["job_Number"] + "_" + job_data["GeneratedOn"].split(" ")[0] + "_Resume.pdf"
    
    headers = {
        "Content-Disposition": "attachment; filename=" + export_name + ";"
    } 

    return FileResponse(absolute_path, filename=export_name, headers=headers, media_type="application/pdf")