from schemas.station_result import UserAnswerRequest, UserAnswer
from database import database as db
from typing import List, Optional
from service.ExamService import agent_service

from beanie import PydanticObjectId

class StationResultService:   
    async def handle_question_answer(self, session_id: PydanticObjectId, station_id: PydanticObjectId, type: str, user_answer_requests: List[UserAnswerRequest]) -> None:
        user_answers = [
            UserAnswer(**ans.model_dump(), evaluation=None)
            for ans in user_answer_requests
        ]
        await db.create_or_update_station_result(session_id, station_id, type, user_answers)
        
        evaluation = await agent_service.mock_evaluate_question_answer_station(station_id, type, user_answer_requests)

        print(evaluation)
        
    #async def handle_patient_interview(self, session, station):
        