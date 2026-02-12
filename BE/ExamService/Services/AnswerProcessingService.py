"""
AnswerProcessingService - Xử lý nộp câu trả lời
Tương ứng với proto message: AnswerRequest, StandardResponse
"""
from datetime import datetime
from typing import Dict, List, Optional
from BE.ExamService.Repository.UserAnswerRepository import UserAnswerRepository
from BE.ExamService.Repository.QuestionRepository import QuestionRepository
from BE.ExamService.Models.UserAnswerModel import UserAnswer
from BE.ExamService.Models.PyObjectId import PyObjectId


class AnswerProcessingService:
    """Service xử lý nộp đáp án từ AnswerRequest"""
    
    def __init__(self):
        self.answer_repo = UserAnswerRepository()
        self.question_repo = QuestionRepository()
    
    async def submit_answer(self, session_id: str, station_id: str, 
                           question_id: str, answer_data: str) -> Dict:
        try:
            question = await self.question_repo.find_by_id(question_id)
            if not question:
                return {
                    'success': False,
                    'message': f'Câu hỏi {question_id} không tồn tại'
                }
            
            user_answer = UserAnswer(
                question_id=PyObjectId(question_id),
                answer_content=answer_data,
                evaluation=[]
            )
            
            answer_id = await self.answer_repo.create(user_answer)
            
            return {
                'success': True,
                'message': f'Nộp đáp án thành công (ID: {answer_id})'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi nộp đáp án: {str(e)}'
            }
    
    #async def get_session_answers(self, session_id: str) -> List[UserAnswer]:
        
    #async def validate_answer(self, answer_data: str, question_type: str) -> bool:
        
