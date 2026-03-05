from models.station_result import StationResult, UserAnswer
from database import database as db
from typing import List, Optional

from beanie import PydanticObjectId


class StationResultService:   
    async def handle_question_answer(self, session, station, payload):
        
    async def handle_patient_interview(self, session, station):
        