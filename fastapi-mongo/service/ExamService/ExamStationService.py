from datetime import datetime, timedelta, timezone
from typing import List, Optional
from beanie import PydanticObjectId
import logging

from models.exam_session import ExamSession
from fastapi import HTTPException
from models.exam_station import ExamStation
from schemas.exam_station import ExamStationResponse, ExamStationUpdate
from database import database as db

logger = logging.getLogger(__name__)

class ExamStationService:
    async def create_initial_exam_stations(self, session_id: PydanticObjectId, user_id: PydanticObjectId, stations_id: List[PydanticObjectId], stations_time: List[int]) -> None:
        exam_stations = []

        for index, (station_id, time_limit) in enumerate(zip(stations_id, stations_time)):
            exam_stations.append(
                ExamStation(
                    session_id=session_id,
                    user_id=user_id,
                    station_id=station_id,
                    station_number=index + 1,
                    status="NOT_STARTED",
                    time_limit=time_limit
                )
            )
        await db.create_exam_stations(exam_stations)

    
    async def get_exam_station(self, session_id: PydanticObjectId, station_number: int) -> Optional[ExamStationResponse]:
        return await db.retrieve_exam_station(session_id, station_number)
    
    async def check_and_update_exam_station(self, session_id: PydanticObjectId, station_number: int):
        exam_station = await db.retrieve_exam_station(session_id, station_number)

        if not exam_station:
            raise HTTPException(404, "Exam station not found")
        
        if exam_station.status == "NOT_STARTED":
            await db.update_exam_station(
                session_id,
                station_number,
                {
                    "status": "IN_PROGRESS",
                    "started_at": datetime.now(timezone.utc)
                }
            )

            return ExamStationUpdate(
                status="IN_PROGRESS",
                remaining_time=exam_station.time_limit
            )
        
        elif exam_station.status == "IN_PROGRESS":
            remaining_time = self.calculate_remaining_time(exam_station)
            if remaining_time <= 0:
                await db.update_exam_station(
                    session_id,
                    station_number,
                    {
                        "status": "TIME_OUT",
                        "finished_at": exam_station.started_at + timedelta(seconds=exam_station.time_limit)
                    }
                )

                return ExamStationUpdate(
                    status="TIME_OUT",
                    remaining_time=0
                )
            return ExamStationUpdate(
                status="IN_PROGRESS",
                remaining_time=remaining_time
            )
        
        else:
            return ExamStationUpdate(
                status=exam_station.status,
                remaining_time=0
            )



    def calculate_remaining_time(self, station: ExamStation) -> int:
        if not station.started_at:
            return station.time_limit

        now = datetime.now(timezone.utc)
        elapse = (now - station.started_at).total_seconds()
        remaining = station.time_limit - int(elapse)

        return remaining