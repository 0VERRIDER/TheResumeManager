from fastapi import APIRouter
from fastapi.responses import FileResponse
from ....data.database.DB import DB
from ....models.Response import Response
from ....models.ErrorResponse import ErrorResponse
import os

router = APIRouter()
class ResumeGetErrorResponse(ErrorResponse):
    pass

@router.get("/{uuid}/get")
async def get_resume(uuid: str, dl: bool = 0):
    root = "./data/"
    folder_name = uuid
    file_name = "/Resume_Final.pdf"
    absolute_path = root + folder_name + file_name
    job_data = {}

    if not os.path.exists(absolute_path):
        return ResumeGetErrorResponse("error", 404, "Invalid Data Requested.", {"uuid": uuid})

    # import a json file
    # with open(root + folder_name + "/details.json") as json_file:
    #     job_data = json.load(json_file)

    database = DB()
    job_data = database.read(uuid)

    employer_name = job_data["employer_name"]
    job_role = job_data["job_title"]
    job_number = job_data["job_number"]
    export_name = "Anshil_P_" + employer_name + "_" + job_role + "_" + job_number + "_" + str(job_data["generated_on"]) + "_Resume"
    
    #replace special characters except underscore or hyphen from export_name
    export_name = export_name.replace(" ", "_")
    export_name = export_name.replace(":", "_")
    export_name = export_name.replace("(", "_")
    export_name = export_name.replace(")", "_")
    export_name = export_name.replace("/", "_")
    export_name = export_name.replace("\\", "_")
    export_name = export_name.replace(",", "_")
    export_name = export_name.replace(".", "_")
    export_name = export_name.replace(";", "_")
    export_name = export_name.replace("'", "_")
    export_name = export_name.replace("\"", "_")
    export_name = export_name.replace("!", "_")
    export_name = export_name.replace("@", "_")
    export_name = export_name.replace("#", "_")
    export_name = export_name.replace("$", "_")
    export_name = export_name.replace("%", "_")
    export_name = export_name.replace("^", "_")

    headers = {
        "Content-Disposition": "attachment; filename=" + export_name + ".pdf" + ";"
    } 

    if dl:
        return FileResponse(absolute_path, filename=export_name, headers=headers, media_type="application/pdf")
    else:
        class GetResumeDetailsResponse(Response):
            pass
        
        return GetResumeDetailsResponse("success", 200, "Data Fetched Successfully", job_data)
