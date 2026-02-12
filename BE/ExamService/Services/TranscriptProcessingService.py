"""
TranscriptProcessingService - Xử lý nội dung khi sinh viên nói
Tương ứng với proto message: TranscriptRequest, StandardResponse
"""
from datetime import datetime
from typing import Dict, Optional
from BE.ExamService.Repository.UserDialogRepository import UserDialogRepository
from BE.ExamService.Models.UserDialogModel import UserDialog
from BE.ExamService.Models.PyObjectId import PyObjectId


class TranscriptProcessingService:
    """Service xử lý transcript từ TranscriptRequest"""
    
    def __init__(self):
        self.dialog_repo = UserDialogRepository()
    
    async def receive_transcript(self, session_id: str, text_content: str, 
                                 is_final: bool) -> Dict:
        """
        Nhận kết quả Text từ Media Service (S2T) hoặc Coordinator gửi sang
        Tương ứng với rpc ReceiveTranscript
        
        Args:
            session_id: ID của phiên thi
            text_content: Nội dung sinh viên nói (đã convert từ speech to text)
            is_final: True nếu câu nói đã kết thúc, False nếu đang stream
        
        Returns:
            {
                'success': bool,
                'message': str
            }
        """
        try:
            # 1. Kiểm tra content không rỗng
            if not text_content or len(text_content.strip()) == 0:
                return {
                    'success': False,
                    'message': 'Content không được rỗng'
                }
            
            # 2. Lưu vào DB (ghi nhận người học nói gì)
            await self.dialog_repo.add_entry(
                session_id=session_id,
                role="STUDENT",
                content=text_content,
                is_final=is_final,
                timestamp=datetime.utcnow()
            )
            
            # 3. Nếu câu nói đã kết thúc (is_final=True), trigger xử lý ai
            if is_final:
                # TODO: Bắn event sang Message Queue (RabbitMQ, Kafka)
                # hoặc gọi Coordinator Service để AI xử lý
                # await self.trigger_ai_evaluation(session_id)
                pass
            
            return {
                'success': True,
                'message': 'Nhận transcript thành công'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi nhận transcript: {str(e)}'
            }
    
    async def get_session_dialog(self, session_id: str) -> Optional[UserDialog]:
        """
        Lấy lịch sử hội thoại của một phiên thi
        
        Args:
            session_id: ID của phiên thi
        
        Returns:
            UserDialog object hoặc None
        """
        # TODO: Cần thêm method trong UserDialogRepository 
        # để lấy dialog theo session_id
        pass
    
    async def save_transcript(self, session_id: str, text: str, 
                            is_final: bool, role: str = "STUDENT") -> bool:
        """
        Lưu transcript vào database
        
        Args:
            session_id: ID phiên thi
            text: Nội dung text
            is_final: Có phải câu nói cuối cùng không
            role: Vai trò (STUDENT, SYSTEM, AI)
        
        Returns:
            True nếu lưu thành công
        """
        try:
            await self.dialog_repo.add_entry(
                session_id=session_id,
                role=role,
                content=text,
                is_final=is_final,
                timestamp=datetime.utcnow()
            )
            return True
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False
    
    async def process_final_transcript(self, session_id: str) -> Dict:
        """
        Xử lý transcript sau khi câu nói kết thúc
        Có thể dùng để trigger AI evaluation hoặc gọi service khác
        
        Args:
            session_id: ID phiên thi
        
        Returns:
            {
                'success': bool,
                'message': str
            }
        """
        try:
            # Get dialog history
            dialog = await self.get_session_dialog(session_id)
            if not dialog:
                return {
                    'success': False,
                    'message': 'Không tìm thấy lịch sử hội thoại'
                }
            
            # TODO: Trigger AI evaluation
            # Send to message queue or call Coordinator service
            
            return {
                'success': True,
                'message': 'Bắt đầu xử lý transcript'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi xử lý transcript: {str(e)}'
            }
