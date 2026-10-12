from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi.encoders import jsonable_encoder
from src.config import Config
from itsdangerous import URLSafeTimedSerializer
import jwt
import uuid
import logging

passwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password_hash(password: str, password_hash: str) -> bool:
    return passwd_context.verify(password, password_hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh


    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.error(f"Error decoding JWT token: {e}")
        return None

serializer = URLSafeTimedSerializer(Config.JWT_SECRET_KEY, salt="email-verification")

def create_safe_url_token(data: dict):
    
    token = serializer.dumps(data)
    return token

def decode_safe_url_token(token:str):
    try:
        token_data = serializer.loads(token)

        return token_data
    except Exception as e:
        logging.error(f"Error decoding safe URL token: {e}")
        return None
