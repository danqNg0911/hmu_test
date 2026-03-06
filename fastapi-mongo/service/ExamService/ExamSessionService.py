from typing import List, Optional
from beanie import PydanticObjectId
import logging
from datetime import datetime

from models.exam_session import ExamSession
from fastapi import HTTPException
from models.station import Station
from models.exam_station import ExamStation
from schemas.exam_session import ExamSessionCreate, ExamSessionResponse, ExamSessionUpdate, ExamSessionStartResponse
from schemas.station_result import UserAnswerRequest, UserAnswer
from service.ExamService.ExamStationService import ExamStationService
from service.ExamService.StationResultService import StationResultService
from database import database as db

logger = logging.getLogger(__name__)

class ExamSessionService:
    def __init__(self):
        self.ExamStationService = ExamStationService()
        self.StationResultService = StationResultService()
    
    async def startExamSession(self, user_id: str, total_stations: int):
        try:
            stations = await db.get_random_station(limit=total_stations)

            stations_id = [s["_id"] for s in stations]
            stations_time = [s["time"] for s in stations]

            if len(stations) < total_stations:
                raise HTTPException(status_code=400, detail="Error retrieving stations for this session")
            
            new_session = ExamSession(
                user_id=PydanticObjectId(user_id),
                stations = stations_id,
                status="IN_PROGRESS",
                current_station=0
            )

            saved_session = await db.add_exam_session(new_session)
            await self.ExamStationService.create_initial_exam_stations(saved_session.id, PydanticObjectId(user_id), stations_id, stations_time)

            return ExamSessionStartResponse(
                id = saved_session.id,
                current_station = 1,
                status = "IN_PROGRESS"
            )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error starting exam session: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")

    async def getSession(self, session_id: PydanticObjectId):
        try:
            session = await db.retrieve_exam_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            return {
                "id": str(session.id),
                "status": session.status,
                "current_station": session.current_station + 1,
                "total_stations": len(session.stations)
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving session: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
            

    async def getCurrentStation(self, session_id: PydanticObjectId):
        try:
            session = await db.retrieve_exam_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            if session.status == "COMPLETED":
                raise HTTPException(status_code=400, detail="Exam session already completed")
            
            current_index = session.current_station
            current_station_id = session.stations[current_index]
            current_station = await db.retrieve_station(current_station_id)

            current_exam_station = await self.ExamStationService.check_and_update_exam_station(session_id, current_index + 1)

            if current_exam_station.status != "IN_PROGRESS":
                return {
                    "station_number": current_index + 1,
                    "station_status": current_exam_station.status,
                    "time_remaining": 0,
                    "station": None
                }
            
            return {
                    "station_number": current_index + 1,
                    "station_status": "IN_PROGRESS",
                    "time_remaining": current_exam_station.remaining_time,
                    "station": current_station.model_dump(by_alias=True)
                }
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving current station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")

    async def submitCurrentStation(self, session_id: PydanticObjectId, station_id: str, answers: List[UserAnswerRequest]):
        try:
            session = await db.retrieve_exam_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            if session.status == "COMPLETED":
                raise HTTPException(status_code=400, detail="Exam session already completed")
            
            if session.current_station >= len(session.stations):
                raise HTTPException(status_code=400, detail="Exam session already completed")
            
            #cập nhật trạng thái của station trong session đó sang submitted/time_out
            await self.ExamStationService.submit_exam_station(session_id, session.current_station + 1)

            station_id_obj = session.stations[session.current_station]
            station = await db.retrieve_station(station_id_obj)
            station_type = station.type

            #xử lý logic nộp kết quả 
            if station_type == "question_answer":
                await self.StationResultService.handle_question_answer(session_id, station_id_obj, station_type, answers)

            else:
                await self.StationResultService.handle_patient_interview(session_id, station_id_obj, station_type)

            
            next_index = session.current_station + 1
            total = len(session.stations)

            #xử lý nộp trạm cuối -> nộp cả bài thi
            if next_index >= total:
                # cập nhật session hoàn thành
                await db.update_exam_session_data(
                    session_id,
                    {"status": "COMPLETED"}
                )
                
                station_results = await db.get_all_station_results(session_id)
                total_score = sum(result.score or 0 for result in station_results)
                stations = await db.get_stations_by_session_ids([session_id])
                session_start_time = stations[0].started_at

                # lưu kết quả cả bài thi
                await db.create_exam_result(
                    user_id=session.user_id,
                    start_at=session_start_time,
                    end_at=datetime.utcnow(),
                    total_score=total_score,
                    overall_feedback=None
                )
                
                return {
                    "status": "COMPLETED",
                    "message": "Exam completed successfully"
                }
            
            next_station_id = session.stations[next_index]
            next_station = await db.retrieve_station(next_station_id)

            await db.update_exam_session_data(
                session_id,
                {
                    "current_station": next_index
                }
            )

            return {
                "status": "IN_PROGRESS",
                "station_number": next_index + 1,
                "station":  next_station.model_dump(by_alias=True)
            }
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error submitting station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")

    #tạm thời bỏ qua
    async def submitExamSession(self, session_id: PydanticObjectId):
        try:
            session = await db.retrieve_exam_session(session_id)

            if not session:
                raise HTTPException(404, "Session not found")

            await db.update_exam_session_data(
                session.id,
                {"status": "COMPLETED"}
            )

            return {
                "status": "COMPLETED",
                "message": "Exam submitted successfully"
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error submitting station: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")