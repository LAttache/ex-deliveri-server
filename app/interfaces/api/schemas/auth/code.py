from pydantic import BaseModel


class CodeRequest(BaseModel):
    email: str
    code: str

class NewCodeRequest(BaseModel):
    email: str