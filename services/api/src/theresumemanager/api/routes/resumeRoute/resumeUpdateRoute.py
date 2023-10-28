from fastapi import APIRouter
from fastapi.responses import FileResponse
from ....data.database.DB import DB
from ....models.Response import Response
from ....models.ErrorResponse import ErrorResponse
import os

router = APIRouter()
class ResumeGetErrorResponse(ErrorResponse):
    pass

@router.get("/{uuid}/update/status/{status}")
async def update_resume(uuid: str, status: str):
    class UpdateResumeResponse(Response):
        pass

    root = "./data/"
    folder_name = uuid
    file_name = "/Resume_Final.pdf"
    absolute_path = root + folder_name + file_name

    if not os.path.exists(absolute_path):
        return ResumeGetErrorResponse("error", 404, "Invalid Data Requested.", {"uuid": uuid})

    # import a json file
    # with open(root + folder_name + "/details.json") as json_file:
    #     job_data = json.load(json_file)

    database = DB()
    def callback(data):
        if data:
            return UpdateResumeResponse("success", 200, "Data Updated Successfully", data)
        else:
            return ErrorResponse("error", 404, "Invalid Data Requested.", {"uuid": uuid})

    database.update_status(uuid, status, callback)    
