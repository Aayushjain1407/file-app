from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from datetime import timedelta, datetime
from jose import jwt, JWTError
from core.config import settings
from fastapi import Depends
from db.session import get_db
from users.models import User
from core import security
import logging
from jose import JWTError
logging.basicConfig(level=logging.DEBUG)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data,  expiry: timedelta = timedelta(minutes=15)):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data):
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
    except JWTError as e:  # Handle general JWT-related errors
        logging.error(f"Error decoding token: {e}")
    return None

def get_current_user(token: str= Depends(oauth2_scheme)):
    logging.debug(f"Received Token: {token}")
    try:
        payload = get_token_payload(token)
        logging.debug(f"Decoded Payload: {payload}")
    except Exception as e:
        logging.error(f"Error decoding token: {e}")
        return None

    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get('id', None)
    role = payload.get('role', None)
    if not user_id or not role:
        return None

    db = next(get_db())

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return user

class JWTAuth:
    async def authenticate(self, conn):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        
        if 'authorization' not in conn.headers:
            return guest
        
        token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
        if not token:
            return guest
        
        user = get_current_user(token=token)
        
        if not user:
            return guest
        
        return AuthCredentials('authenticated'), user
    