from fastapi import APIRouter, HTTPException, Body
from beanie import PydanticObjectId
from typing import List

from database.database import add_patient_info, retrieve_patient_info

from models.patient_info import PatientInfo
from schemas.patient_info import PatientInfoCreate, PatientInfoResponse

router = APIRouter()

@router.post("/", response_model=PatientInfoResponse)
async def create_patient_info(patient_data: PatientInfoCreate = Body(...)):
    new_patient = PatientInfo(**patient_data.model_dump())
    created_patient = await add_patient_info(new_patient)
    return created_patient

@router.get("/{id}", response_model=PatientInfoResponse)
async def get_patient_info(id: PydanticObjectId):
    patient = await retrieve_patient_info(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    return patient