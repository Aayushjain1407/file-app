from sqlalchemy import Column, Integer, String, Boolean, DateTime
from db.basemodel import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'
    
    username = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    
    #relationships
    raw_file = relationship("RawFile", back_populates="user")
    
class OTP(BaseModel):
    __tablename__ = 'otp'

    user_id = Column(String(length=12), index=True)
    code = Column(String)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
    