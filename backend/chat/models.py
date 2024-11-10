from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.basemodel import Base
from datetime import datetime

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    user_id = Column(String(12), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    session_id = Column(String(12), ForeignKey("chat_sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_bot = Column(Boolean, default=False)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")