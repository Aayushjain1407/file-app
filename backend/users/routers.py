from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, services
from db.session import get_db
from auth.services import create_access_token, create_refresh_token
from datetime import timedelta
from core.config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db=db, user=user)

@router.post("/verify", response_model=schemas.UserResponse)
def verify_user(verify_data: schemas.UserVerify, db: Session = Depends(get_db)):
    return services.verify_user(
        db=db,
        phone_number=verify_data.phone_number,
        code=verify_data.code
    )


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = services.authenticate_user(
        db=db,
        username=user_credentials.username,
        password=user_credentials.password
    )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds()
    }