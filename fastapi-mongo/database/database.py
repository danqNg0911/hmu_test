from typing import List, Union, Optional
from beanie import PydanticObjectId

from models.user import User
from models.station import Station
from models.patient_info import PatientInfo
from models.exam_session import ExamSession
from models.exam_station import ExamStation
from models.message import Message

# ================= USER =================

async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def retrieve_user(id: PydanticObjectId) -> Union[User, None]:
    return await User.get(id)


# ================= STATION =================

async def add_station(new_station: Station) -> Station:
    station = await new_station.create()
    return station

async def retrieve_stations() -> List[Station]:
    return await Station.all().to_list()

async def retrieve_station(id: PydanticObjectId) -> Union[Station, None]:
    return await Station.get(id)

async def get_random_station(limit: int) -> List[dict]:
    return await Station.aggregate([
        {"$sample": {"size": limit}}
    ]).to_list()



# ================= PATIENT INFO =================

async def add_patient_info(new_patient: PatientInfo) -> PatientInfo:
    return await new_patient.create()

async def retrieve_patient_info(id: PydanticObjectId) -> Union[PatientInfo, None]:
    return await PatientInfo.get(id)

async def update_patient_info_data(id: PydanticObjectId, data: dict) -> Union[bool, PatientInfo]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": des_body}
    
    patient = await PatientInfo.get(id)
    if patient:
        await patient.update(update_query)
        return patient
    return False


# ================= EXAM SESSION =================

async def add_exam_session(new_session: ExamSession) -> ExamSession:
    return await new_session.create()

async def retrieve_exam_session(id: PydanticObjectId) -> Union[ExamSession, None]:
    return await ExamSession.get(id)

async def update_exam_session_data(id: PydanticObjectId, data: dict) -> Union[bool, ExamSession]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": des_body}
    
    session = await ExamSession.get(id)
    if session:
        await session.update(update_query)
        return session
    return False

# ================= EXAM STATION =================
async def create_exam_stations(stations: List[ExamStation]) -> int:
    await ExamStation.insert_many(stations)
    return len(stations)

async def retrieve_exam_station(session_id: PydanticObjectId, station_number: int) -> Optional[ExamStation]:
    return await ExamStation.find_one(
        ExamStation.session_id == session_id,
        ExamStation.station_number == station_number
    )

async def get_exam_station_by_id(station_id: PydanticObjectId) -> Optional[ExamStation]:
    return await ExamStation.get(station_id)

async def update_exam_station(session_id: PydanticObjectId, station_number: int, update_data: dict) -> Optional[ExamStation]:
    exam_station = await ExamStation.find_one(
        ExamStation.session_id == session_id,
        ExamStation.station_number == station_number
    )

    if not exam_station:
        return None
    
    data = {k: v for k, v in update_data.items() if v is not None}

    await exam_station.update({"$set": data})
    return exam_station


# ================= MESSAGE =================

async def add_message(new_message: Message) -> Message:
    return await new_message.create()

async def retrieve_chat_history(user_id: str, agent_id: str) -> List[Message]:
    messages = await Message.find(
        {
            "$or": [
                {"sender": user_id, "recipient": agent_id},
                {"sender": agent_id, "recipient": user_id}
            ]
        }
    ).sort("+timestamp").to_list()
    return messages

# ================= EXAM SESSION =================

async def add_exam_session(new_session: ExamSession) -> ExamSession:
    return await new_session.create()