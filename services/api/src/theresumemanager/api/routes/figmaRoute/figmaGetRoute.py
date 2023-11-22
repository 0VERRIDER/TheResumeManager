from fastapi import APIRouter
from ....data.database.DB import DB
from ....core.functions.figma.figmaFunction import get_resume_ids_from_figma
from ....models.Response import Response
from ....models.ErrorResponse import ErrorResponse
import os

router = APIRouter()
class figmaGetErrorResponse(ErrorResponse):
    pass

@router.get("/ids")
async def get_design_ids():
        ids = get_resume_ids_from_figma()
        class GetFigmaDesignResponse(Response):
            pass
        
        return GetFigmaDesignResponse("success", 200, "Data Fetched Successfully", ids)