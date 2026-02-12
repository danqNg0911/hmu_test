"""
ExamStateService - Quản lý trạng thái phiên thi
Tương ứng với proto message: SessionIdRequest, ExamStateResponse
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from BE.ExamService.Repository.QuestionRepository import QuestionRepository
from BE.ExamService.Models.ExamSessionModel import ExamSession


class ExamStateService:
    
    def __init__(self):
        self.question_repo = QuestionRepository()
    
    async def get_current_state(self, session_id: str) -> Dict:
        """
        Lấy trạng thái hiện tại của phiên thi
        Tương ứng với rpc GetCurrentState
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            {
                'status': str,              # 'IN_PROGRESS', 'TIMEOUT', 'PAUSED', 'COMPLETED'
                'remaining_seconds': int,    # Thời gian còn lại (giây)
                'current_station_index': int # Index trạm hiện tại (0-based)
            }
        """
        try:
            # TODO: Cần fetch ExamSession từ database
            # session = await self.session_repo.find_by_id(session_id)
            
            # Giả sử có session object
            # remaining = (session.end_time - datetime.utcnow()).total_seconds()
            
            # if remaining <= 0:
            #     session.status = "TIMEOUT"
            #     remaining = 0
            #     await self.session_repo.save(session)
            
            return {
                'status': 'IN_PROGRESS',
                'remaining_seconds': 1800,  # 30 phút
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
        """
        Kiểm tra phiên thi có hết thời gian không
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            True nếu hết thời gian
        """
        # TODO: Implement logic check timeout
        pass
    
    async def get_remaining_time(self, session_id: str) -> int:
        """
        Lấy thời gian còn lại (giây)
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            Số giây còn lại
        """
        # TODO: Implement logic tính thời gian còn lại
        pass
    
    async def get_station_progress(self, session_id: str) -> Dict:
        """
        Lấy tiến độ hiện tại ở trạm (station)
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            {
                'current_station_index': int,
                'total_stations': int,
                'current_question_index': int,
                'total_questions_in_station': int
            }
        """
        # TODO: Implement logic lấy station progress
        pass
    
    async def update_station_index(self, session_id: str, new_index: int) -> bool:
        """
        Update index trạm hiện tại
        
        Args:
            session_id: ID của phiên thi
            new_index: Index trạm mới
        
        Returns:
            True nếu update thành công
        """
        # TODO: Implement logic update station index
        pass
    
    async def mark_session_completed(self, session_id: str) -> bool:
        """
        Đánh dấu phiên thi đã hoàn thành
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            True nếu thành công
        """
        # TODO: Implement logic mark as completed
        pass
    
    async def check_and_update_status(self, session_id: str) -> str:
        """
        Kiểm tra và update trạng thái phiên thi
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            Trạng thái hiện tại ('IN_PROGRESS', 'TIMEOUT', 'PAUSED', 'COMPLETED')
        """
        state = await self.get_current_state(session_id)
        return state['status']
