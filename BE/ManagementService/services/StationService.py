from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException
import logging
import asyncio

from repository.StationRepository import StationRepository
from schemas.StationSchema import StationCreate, StationResponse, StationUpdate
from services.QuestionService import QuestionService
from services.PatientInfoService import PatientInfoService
from models.StationModel import Station
logger = logging.getLogger(__name__)

class StationService:
    def __init__(self):
        self.stationRepository = StationRepository()
        self.questionService = QuestionService()
        self.patientInfoService = PatientInfoService()

    async def getDetailStation(self, station: Station) -> StationResponse:
        try:
            questionIds = [str(qid) for qid in station.questions]
            fullQuestions = await self.questionService.getQuestionsOrderedByIds(questionIds)
            fullPatientInfo = None

            if station.patientId:
                patientId = str(station.patientId)
                fullPatientInfo = await self.patientInfoService.getPatientById(patientId)

            stationData = station.model_dump(by_alias=True)

            if 'patientId' in stationData:
                del stationData['patientId']

            stationData['questions'] = fullQuestions
            stationData['patient'] = fullPatientInfo
            
            return StationResponse(**stationData)

        except Exception as e:
            logger.error(f"Error getting detail station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server eror")

    async def createStation(self, data: StationCreate) -> StationResponse:
        try:
            stationModel = Station(**data.model_dump())
            createdStation = await self.stationRepository.create(stationModel)

            return await self.getDetailStation(createdStation)
        
        except Exception as e:
            logger.error(f"Error creating station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")


    async def getStationById(self, stationId: str) -> StationResponse:
        if not ObjectId.is_valid(stationId):
            raise HTTPException(status_code=400, detail="Invalid station ID")
        
        try:
            station = await self.stationRepository.getById(stationId)
            if not station:
                raise HTTPException(status_code=404, detail="Station not found")
            
            return await self.getDetailStation(station)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching station with id {stationId}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
    
    async def getStationByType(self, stationType: str) -> StationResponse:
        try: 
            stations = await self.stationRepository.getByType(stationType)
            results = []
            for s in stations:
                results.append(await self.getDetailStation(s))
            return results
        except Exception as e:
            logger.error(f"Error fetching station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
    
    async def updateStation(self, stationId: str, data: StationUpdate) -> bool:
        if not ObjectId.is_valid(stationId):
            raise HTTPException(status_code=400, detail="Invalid station ID")
        
        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return False
        try:
            isUpdated = await self.stationRepository.update(stationId, updateData)
            if not isUpdated:
                isExisted = await self.stationRepository.getById(stationId)
                if not isExisted:
                    raise HTTPException(status_code=404, detail="Update station not found")
                return False
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")

    async def deleteStation(self, stationId: str) -> bool:
        if not ObjectId.is_valid(stationId):
            raise HTTPException(status_code=400, detail="Invalid station ID")

        try:
            isDeleted = await self.stationRepository.delete(stationId)
            if not isDeleted:
                raise HTTPException(status_code=404, detail="Station not found")
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")