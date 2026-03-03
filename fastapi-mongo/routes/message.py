from fastapi import APIRouter, Body
from typing import List

from models.message import Message
from schemas.message import MessageCreate, MessageResponse

from database.database import add_message, retrieve_chat_history

router = APIRouter()

@router.post("/", response_model=MessageResponse)
async def send_message(msg_data: MessageCreate = Body(...)):
    new_message = Message(**msg_data.model_dump())
    created_message = await add_message(new_message)
    return created_message

@router.get("/history/{user_id}/{agent_id}", response_model=List[MessageResponse])
async def get_chat_history(user_id: str, agent_id: str):
    messages = await retrieve_chat_history(user_id, agent_id)
    return messages