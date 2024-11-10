from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, services
from .connection_manager import manager
from .langchain_service import ChatService
from db.session import get_db
from core.security import get_current_user
from users.models import User
import json

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/sessions", response_model=schemas.ChatSessionResponse)
async def create_chat_session(
    session: schemas.ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.create_chat_session(db=db, user_id=current_user.id, title=session.title)

@router.get("/sessions", response_model=List[schemas.ChatSessionResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.get_user_sessions(db=db, user_id=current_user.id)

@router.get("/sessions/{session_id}", response_model=schemas.ChatHistory)
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return services.get_chat_history(db=db, session_id=session_id, user_id=current_user.id)

@router.websocket("/ws/{session_id}")
async def chat_websocket(
    websocket: WebSocket,
    session_id: str,
    db: Session = Depends(get_db)
):
    chat_service = ChatService()
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            message = await websocket.receive_text()
            
            # Process message with LangChain
            ai_response = await chat_service.get_response(message)
            
            # Save user message and AI response
            user_message = services.create_message(
                db=db,
                session_id=session_id,
                content=message,
                is_bot=False
            )
            
            bot_message = services.create_message(
                db=db,
                session_id=session_id,
                content=ai_response,
                is_bot=True
            )
            
            # Broadcast messages to all clients in the session
            await manager.broadcast_to_session(
                {
                    "type": "user_message",
                    "data": schemas.MessageResponse.from_orm(user_message).dict()
                },
                session_id
            )
            
            await manager.broadcast_to_session(
                {
                    "type": "bot_message",
                    "data": schemas.MessageResponse.from_orm(bot_message).dict()
                },
                session_id
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        chat_service.clear_memory()