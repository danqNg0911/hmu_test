from fastapi import APIRouter, HTTPException, Body
from beanie import PydanticObjectId
from typing import List

from database.database import add_patient_info, add_station, retrieve_patient_info

from models.patient_info import PatientInfo
from models.station import Station
from schemas.patient_info import PatientInfoCreate, PatientInfoResponse
from schemas.station import StationResponse, StationCreate

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

@router.post("/{id}/station/", response_model=StationResponse)
async def create_patient_station(patient_id: PydanticObjectId, station_data: StationCreate = Body(...)):
    patient = await PatientInfo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    new_station = Station(patient_id=patient.id, **station_data.model_dump())
    created_station = await add_station(new_station)
    return created_station