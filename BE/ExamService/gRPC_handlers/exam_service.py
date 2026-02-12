import grpc
from protos import exam_service_pb2, exam_service_pb2_grpc
from Services.ExamSessionService import ExamSessionService
from Services.AnswerProcessingService import AnswerProcessingService
from Services.ExamStateService import ExamStateService

class ExamServiceHandler(exam_service_pb2_grpc.ExamServiceServicer):
    def __init__(self):
        self.exam_session_service = ExamSessionService()
        self.answer_processing_service = AnswerProcessingService()
        self.exam_state_service = ExamStateService()
    
    async def StartExamSession(self, request, context):
        response_data = await self.exam_session_service.start_exam_session(
            student_id=request.student_id,
            exam_script_id=request.exam_script_id
        )
        return exam_service_pb2.StartExamSessionResponse(**response_data)
    
    async def SubmitAnswer(self, request, context):
        response_data = await self.answer_processing_service.submit_answer(
            session_id=request.session_id,
            station_id=request.station_id,
            question_id=request.question_id,
            answer_data=request.answer_data
        )
        return exam_service_pb2.SubmitAnswerResponse(**response_data)
    
    async def GetCurrentState(self, request, context):
        response_data = await self.exam_state_service.get_current_state(
            session_id=request.session_id
        )
        return exam_service_pb2.GetCurrentStateResponse(**response_data)