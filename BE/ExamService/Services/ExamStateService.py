"""
ExamStateService - Quản lý trạng thái phiên thi
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from BE.ExamService.Repository.QuestionRepository import QuestionRepository
from BE.ExamService.Models.ExamSessionModel import ExamSession


class ExamStateService:
    
    def __init__(self):
        self.question_repo = QuestionRepository()
    
    async def get_current_state(self, session_id: str) -> Dict:
        try:
            return {
                'status': 'IN_PROGRESS',
                'remaining_seconds': 600,
                'current_station_index': 0
            }
            
        except Exception as e:
            return {
                'status': 'ERROR',
                'remaining_seconds': 0,
                'current_station_index': 0,
                'error': str(e)
            }
    
    async def is_session_timeout(self, session_id: str) -> bool:
        pass
    
    async def get_remaining_time(self, session_id: str) -> int:
        pass
    
    async def get_station_progress(self, session_id: str) -> Dict:
        pass
    
    async def update_station_index(self, session_id: str, new_index: int) -> bool:
        pass
    
    async def mark_session_completed(self, session_id: str) -> bool:
        pass
    
    async def check_and_update_status(self, session_id: str) -> str:
        state = await self.get_current_state(session_id)
        return state['status']
