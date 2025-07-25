from datetime import datetime
from uuid import UUID

class User:
    def __init__(self, user_id: UUID, email: str, hashed_password: str, created_at: datetime, username: str = ""):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = created_at

