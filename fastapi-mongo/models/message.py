from beanie import Document
from datetime import datetime
from pydantic import Field

class Message(Document):
    sender: str
    recipient: str
    messageType: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 

    class Settings:
        name = "Messages"