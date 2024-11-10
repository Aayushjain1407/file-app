from sqlalchemy.orm import Session
from . import models, schemas
from core.security import get_password_hash, verify_password
from fastapi import HTTPException
from datetime import datetime
import random
import string

def generate_verification_code(length: int = 6) -> str:
    """Generate a random verification code."""
    return ''.join(random.choices(string.digits, k=length))

def create_user(db: Session, user: schemas.UserCreate):
    # Check if username exists
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if phone number exists
    if db.query(models.User).filter(models.User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Generate verification code
    verification_code = generate_verification_code()
    
    # Create user object
    db_user = models.User(
        username=user.username,
        phone_number=user.phone_number,
        hashed_password=get_password_hash(user.password),
        verification_code=verification_code,
        is_verified=False
    )
    
    try:
        # Add and commit to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Here you would normally send the verification code via Twilio
        # For now, we'll just print it
        print(f"Verification code for {user.phone_number}: {verification_code}")
        
        
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def verify_user(db: Session, phone_number: str, code: str):
    user = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    user.is_verified = True
    user.verification_code = None  # Clear the verification code after use
    
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Please verify your phone number first")
        
    return user

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user