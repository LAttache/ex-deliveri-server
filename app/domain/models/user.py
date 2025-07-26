from datetime import datetime, timezone
from uuid import UUID

class User:
    def __init__(
            self,
            user_id: UUID,
            email: str,
            hashed_password: str,
            username: str = "",
            surname: str = "",
            is_email_verified: bool = False,
            is_blocked: bool = False,
    ):
        self.user_id = user_id
        self.username = username
        self.surname = surname
        self.email = email
        self.hashed_password = hashed_password
        self.is_email_verified = is_email_verified
        self.is_blocked = is_blocked
