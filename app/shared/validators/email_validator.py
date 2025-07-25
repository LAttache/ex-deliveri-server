import re
from fastapi import HTTPException, status

EMAIL_REGEX = re.compile(r"^[\w.-]+@[\w.-]+\.\w+$")

def validate_email(email: str):
    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )