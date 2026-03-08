from http.client import HTTPException

from fastapi import APIRouter, Body
from typing import List
from beanie import PydanticObjectId

from models.exam_result import ExamResult
from models.station_result import StationResult
from models.patient_info import PatientInfo
from schemas.exam_result import ExamResultResponse
from schemas.station_result import StationResultResponse
from database.database import retrieve_exam_list_result, get_station_result, retrieve_exam_result

router = APIRouter()

#test post
@router.post("/exam/", response_model=ExamResultResponse)
async def create_exam_result(exam_result: ExamResultResponse = Body(...)):
    new_exam_result = ExamResult(**exam_result.model_dump())
    created_exam_result = await create_exam_result(new_exam_result)
    return created_exam_result

@router.post("/exam/{session_id}/station/{station_id}", response_model=StationResultResponse)
async def create_station_result(session_id: PydanticObjectId, station_id: PydanticObjectId, station_result: StationResultResponse = Body(...)):
    new_station_result = StationResult(session_id=session_id, station_id=station_id, **station_result.model_dump())
    created_station_result = await new_station_result.create()
    return created_station_result 
#======================
@router.get("/exam", response_model=List[ExamResultResponse])
async def get_all_exam_results():
    exam_results = await retrieve_exam_list_result()
    if not exam_results:
        raise HTTPException(status_code=404, detail="Không tìm thấy danh sách kết quả thi")
    return exam_results

@router.get("/exam/{session_id}", response_model=ExamResultResponse)
async def get_exam_result(session_id: PydanticObjectId):
    exam_results = await retrieve_exam_result(session_id)
    if not exam_results:
        raise HTTPException(status_code=404, detail="Không tìm thấy kết quả thi")
    return exam_results

@router.get("/exam/{session_id}/station/{station_id}", response_model=List[ExamResultResponse])
async def get_station_result(session_id: PydanticObjectId, station_id: PydanticObjectId):
    exam_results = await get_station_result(session_id, station_id)
    if not exam_results:
        raise HTTPException(status_code=404, detail="Không tìm thấy kết quả thi")
    return exam_results
