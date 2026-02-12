from typing import List, Optional
from fastapi import HTTPException
from bson import ObjectId
import logging

from models.RubricModel import Rubric
from repository.RubricRepository import RubricRepository
from schemas.RubricSchema import RubricCreate, RubricResponse, RubricUpdate

logger = logging.getLogger(__name__)

class RubricService:
    def __init__(self):
        self.repository = RubricRepository()

    async def createRubric(self, data: RubricCreate) -> RubricResponse:
        if data.maxScore is not None and data.maxScore < 0:
            raise HTTPException(status_code=400, detail="maxScore must be positive")
        try: 
            rubricModel = Rubric(**data.model_dump())
            createdRubric = await self.repository.create(rubricModel)
            return RubricResponse(**createdRubric.model_dump(by_alias=True))
        except Exception as e:
            logger.error(f"Error creating rubric: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")     
        
    async def getAllRubrics(self) -> List[RubricResponse]:
        rubrics = await self.repository.getAll()
        return [RubricResponse(**rubric.model_dump(by_alias=True)) for rubric in rubrics]
    
    async def getRubricById(self, rubricId: str) -> Optional[RubricResponse]:
        if ObjectId.is_valid(rubricId):
            raise HTTPException(status_code=400, detail="Invalid rubric ID")
        
        rubric = await self.repository.getById(rubricId)
        if rubric:
            return RubricResponse(**rubric.model_dump(by_alias=True))
        return None
    
    async def updateRubric(self, rubricId: str, data: RubricUpdate) -> bool:
        if data.maxScore is not None and data.maxScore < 0:
            raise HTTPException(status_code=400, detail="maxScore must be positive")
        
        try:
            updateData = data.model_dump(exclude_unset=True)
            if not updateData:
                raise HTTPException(status_code=400, detail="No data provided for update")
            isUpdated = await self.repository.update(rubricId, updateData)
            if not isUpdated:
                existedRubric = await self.repository.getById(rubricId)
                if not existedRubric:
                    raise HTTPException(status_code=404, detail="Rubric not found")
                return False
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating rubric: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
        
    async def deleteRubric(self, rubricId: str) -> bool:
        if ObjectId.is_valid(rubricId):
            raise HTTPException(status_code=400, detail="Invalid rubric ID")
        
        try:
            isDeleted = await self.repository.delete(rubricId)
            if not isDeleted:
                raise HTTPException(status_code=404, detail="Rubric not found")
        except HTTPException:
            raise
        except HTTPException as e:
            logger.error(f"Error deleting rubric: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")