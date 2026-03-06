from beanie import Document, PydanticObjectId
from datetime import datetime
from pydantic import Field

class Message(Document):
    session_id: PydanticObjectId
    station_id: PydanticObjectId
    sender: str
    recipient: str
    messageType: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 

    class Settings:
        name = "Messages"