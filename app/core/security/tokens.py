from fastapi.security import HTTPBearer
from jose import jwt

from app.core.config import settings

security = HTTPBearer()

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
