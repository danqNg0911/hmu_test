from fastapi import APIRouter, HTTPException, Body
from beanie import PydanticObjectId
from typing import List

from database.database import add_patient_info, add_station, retrieve_patient_info, update_patient_info_data, update_station

from models.patient_info import PatientInfo
from models.station import Station
from schemas.patient_info import PatientInfoCreate, PatientInfoResponse, PatientInfoUpdate, PatientInfoDetailResponse
from schemas.station import StationResponse, StationCreate, StationUpdate

router = APIRouter()

@router.post("/", response_model=PatientInfoResponse)
async def create_patient_info(patient_data: PatientInfoCreate = Body(...)):
    new_patient = PatientInfo(**patient_data.model_dump())
    created_patient = await add_patient_info(new_patient)
    return created_patient

@router.get("/", response_model=List[PatientInfoResponse])
async def get_all_patient_info():
    patients = await PatientInfo.find_all().to_list()
    return patients

@router.get("/{id}", response_model=PatientInfoDetailResponse)
async def get_patient_info(id: PydanticObjectId):
    patient = await retrieve_patient_info(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    return patient

@router.put("/{id}", response_model=PatientInfo)
async def update_patient_info(id: PydanticObjectId, patient_data: PatientInfoUpdate = Body(...)):
    patient = await retrieve_patient_info(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    patient = await update_patient_info_data(id, patient_data)
    await patient.save()
    return patient

@router.delete("/{id}")
async def delete_patient_info(id: PydanticObjectId):
    patient = await retrieve_patient_info(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    await patient.delete()
    return {"detail": "Thông tin bệnh nhân đã được xóa"}

#======= Station by patient info =======
@router.post("/{id}/station/", response_model=StationResponse)
async def create_patient_station(patient_id: PydanticObjectId, station_data: StationCreate = Body(...)):
    patient = await PatientInfo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    new_station = Station(patient_id=patient.id, **station_data.model_dump())
    created_station = await add_station(new_station)
    return created_station

@router.get("/{id}/station/{station_id}", response_model=StationResponse)
async def get_station(patient_id: PydanticObjectId, station_id:PydanticObjectId):
    patient = await PatientInfo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    station = await Station.get(station_id)
    if not station:
        raise HTTPException(status_code=404,detail="Không tìm thấy trạm")
    return station

@router.put("/{id}/station/{station_id}", response_model=Station)
async def update_patient_station(patient_id: PydanticObjectId, station_id: PydanticObjectId, station_data: StationUpdate = Body(...)):
    patient = await PatientInfo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    station = await Station.get(station_id)
    if not station or station.patient_info_id != patient_id:
        raise HTTPException(status_code=404, detail="Không tìm thấy trạm cho bệnh nhân này")
    
    station = await update_station(patient_id, station_id, station_data)
    return station

@router.delete("/{id}/station/{station_id}")
async def delete_patient_station(patient_id: PydanticObjectId, station_id: PydanticObjectId):
    patient = await PatientInfo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin bệnh nhân")
    
    station = await Station.get(station_id)
    if not station or station.patient_info_id != patient_id:
        raise HTTPException(status_code=404, detail="Không tìm thấy trạm cho bệnh nhân này")
    
    await station.delete()
    return {"detail": "Trạm đã được xóa"}