from pydantic import BaseModel
from datetime import datetime
from beanie import PydanticObjectId

class MessageCreate(BaseModel):
    sender: str
    recipient: str
    messageType: str
    content: str

class MessageResponse(MessageCreate):
    id: PydanticObjectId
    timestamp: datetime