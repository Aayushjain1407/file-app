from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from datetime import datetime
import shortuuid

def create_chat_session(db: Session, user_id: str, title: str = None):
    db_session = models.ChatSession(
        id=shortuuid.uuid()[:12],
        user_id=user_id,
        title=title,
        last_message_at=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_sessions(db: Session, user_id: str):
    return db.query(models.ChatSession)\
        .filter(models.ChatSession.user_id == user_id)\
        .order_by(models.ChatSession.last_message_at.desc())\
        .all()

def get_chat_history(db: Session, session_id: str, user_id: str):
    session = db.query(models.ChatSession)\
        .filter(
            models.ChatSession.id == session_id,
            models.ChatSession.user_id == user_id
        ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    messages = db.query(models.ChatMessage)\
        .filter(models.ChatMessage.session_id == session_id)\
        .order_by(models.ChatMessage.created_at)\
        .all()
    
    return {"session": session, "messages": messages}

def create_message(db: Session, session_id: str, content: str, is_bot: bool = False):
    db_message = models.ChatMessage(
        id=shortuuid.uuid()[:12],
        session_id=session_id,
        content=content,
        is_bot=is_bot
    )
    
    # Update session's last_message_at
    db.query(models.ChatSession)\
        .filter(models.ChatSession.id == session_id)\
        .update({"last_message_at": datetime.utcnow()})
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
