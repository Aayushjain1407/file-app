from pydantic import BaseModel, validator
from typing import Optional

class UserBase(BaseModel):
    username: str
    phone_number: str

class UserCreate(UserBase):
    # id:str
    password: str

    @validator('phone_number')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            raise ValueError('Phone number must start with + and country code')
        return v

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v


class UserVerify(BaseModel):
    phone_number: str
    code: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True