from typing import List, Union
from beanie import PydanticObjectId

from models.user import User
from models.station import Station
from models.patient_info import PatientInfo
from models.exam_session import ExamSession
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