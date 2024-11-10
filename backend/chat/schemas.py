from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    session_id: str
    is_bot: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionCreate(BaseModel):
    title: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: str
    title: Optional[str]
    last_message_at: datetime
    user_id: str

    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    session: ChatSessionResponse
    messages: List[MessageResponse]
    