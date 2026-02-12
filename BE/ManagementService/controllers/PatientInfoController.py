from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from schemas.PatientInfoSchema import PatientCreate, PatientResponse, PatientUpdate
from services.PatientInfoService import PatientInfoService

router = APIRouter()

def getPatientService():
    return PatientInfoService()

@router.post(
    "patient/create",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient"
)
async def createPatient(
    payload: PatientCreate,
    service: PatientInfoService = Depends(getPatientService)
):
    return await service.createPatient(payload)


@router.get(
    "patient/",
    response_model=List[PatientResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all patients"
)
async def getAllPatients(
    service: PatientInfoService = Depends(getPatientService)
):
    return await service.getAllPatients()

@router.delete(
    "patient/{patientId}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a patient"
)
async def deletePatient(
    patientId: str,
    service: PatientInfoService = Depends(getPatientService)
):
    return await service.deletePatient(patientId)