from sqlalchemy.orm import Session
from . import models, schemas
from core.security import get_password_hash, verify_password
from fastapi import HTTPException
from datetime import datetime,timedelta
import random
import string
from twilio.rest import Client
from fastapi import HTTPException
from core.config import settings

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
# def generate_verification_code(length: int = 6) -> str:
#     """Generate a random verification code."""
#     return ''.join(random.choices(string.digits, k=length))

def create_user(db: Session, user: schemas.UserCreate):
    # Check if username exists
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if phone number exists
    if db.query(models.User).filter(models.User.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    db_user = models.User(
    username=user.username,
    phone_number=user.phone_number,
    hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate and send OTP    
    otp = generate_otp(db, db_user.id)
    if not db_user.phone_number.startswith("+91"):
        db_user.phone_number = "+91"+db_user.phone_number
    send_otp_sms(db_user.phone_number, otp)
    

    try:
        # Add and commit to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
def generate_otp(db: Session, user_id: str):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    db_otp = models.OTP(user_id=user_id, code=otp, expires_at=expires_at)
    db.add(db_otp)
    db.commit()
    return otp

def send_otp_sms(phone_number: str, otp: str):
    try:
        message = twilio_client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

def verify_user(db: Session, phone_number: str, code: str):
    user = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_otp = db.query(models.OTP).filter(
        models.OTP.user_id == user.id,
        models.OTP.code == code,
        models.OTP.is_used == False,
        models.OTP.expires_at > datetime.utcnow()
    ).first()
    
    if not db_otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    db_otp.is_used = True
    user.is_verified = True
    
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