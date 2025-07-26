from pydantic import BaseModel


class EditUserRequest(BaseModel):
    username: str
    surname: str
    email: str