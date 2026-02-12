from typing import List, Optional
from fastapi import HTTPException
from bson import ObjectId
import logging

from schemas.PatientInfoSchema import PatientCreate, PatientResponse, PatientUpdate
from models.PatientInfoModel import PatientInfo
from repository.PatientInfoRepository import PatientRepository

logger = logging.getLogger(__name__)

class PatientInfoService:
    def __init__(self):
        self.repository = PatientRepository()
    
    async def createPatient(self, data: PatientCreate) -> PatientResponse:
        try: 
            patientModel = PatientInfo(**data.model_dump())
            createdPatient = await self.repository.create(patientModel)
            return PatientResponse(**createdPatient.model_dump(by_alias=True))
        
        except Exception as e:
            logger.error(f"Error creating patient: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
    
    async def getAllPatients(self) -> List[PatientResponse]:
        try:
            patientModels = await self.repository.getAll()

            return [PatientResponse(**patient.model_dump(by_alias=True)) for patient in patientModels]
        except Exception as e:
            logger.error(f"Error fetching patients: {e}")
            raise HTTPException(status_code=500, detail="Cannot fetch patients at the moment")
    
    async def getPatientById(self, patientId: str):
        if not ObjectId.is_valid(patientId):
            raise HTTPException(status_code=400, detail="Invalid patient ID")
        
        try:
            patient = await self.repository.getById(patientId)
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching required patient: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
        
    async def updatePatient(self, patientId: str, data: PatientUpdate):
        if not ObjectId.is_valid(patientId):
            raise HTTPException(status_code=400, detail="Invalid patient ID")
        
        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return False
        try:
            isUpdated = await self.repository.update(patientId, updateData)
            if not isUpdated:
                isExisted = await self.repository.getById(patientId)
                if not isExisted:
                    raise HTTPException(status_code=404, detail="Update patient not found")
                return False
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating patient: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
        
    async def deletePatient(self, patientId: str) -> bool:
        if not ObjectId.is_valid(patientId):
            raise HTTPException(status_code=400, detail="Invalid patient ID")
        try:
            isDeleted = await self.repository.delete(patientId)
            if not isDeleted:
                raise HTTPException(status_code=404, detail="Patient not found")
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting patient: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")