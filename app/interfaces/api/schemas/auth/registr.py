from pydantic import BaseModel


class RegistrationResponse(BaseModel):
    data: str

class RegistrationRequest(BaseModel):
    username: str
    email: str
    password: str