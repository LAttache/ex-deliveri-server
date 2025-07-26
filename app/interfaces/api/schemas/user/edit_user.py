from pydantic import BaseModel, EmailStr
from typing import Optional


class EditUserRequest(BaseModel):
    username: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None