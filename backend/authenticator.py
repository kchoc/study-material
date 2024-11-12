from datetime import datetime, timedelta
from http import HTTPStatus
from os import getenv
from typing import Optional
from bcrypt import checkpw, gensalt, hashpw
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt

class Authenticator:
    key: str
    algorithm = "HS256"

    def __init__(self):
        load_dotenv()
        self.key = getenv('SECRET_KEY')

    def create_jwt_token(self, payload: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token with default expiry time of 60 minutes"""
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=60)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.key, self.algorithm)
    
    def decode_jwt_token(self, jwt_token: str) -> dict:
        """Decode/Authenticate JWT token and Raise Errors"""
        try:
            payload = jwt.decode(jwt_token, self.key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid token",
            )

    def hash_password(self, password: str) -> str:
        """Hash Password"""
        return hashpw(password.encode(), gensalt()).decode()
    
    def check_password(self, password: str, hashed_password: bytes) -> bool:
        """Check Password by hashing input and comparing with database password"""
        return checkpw(password.encode(), hashed_password)