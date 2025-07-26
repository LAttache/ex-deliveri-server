from app.domain.models.user import User
from app.infrastructure.database.models import UserDB


def map_user_db_to_user(user_db: UserDB) -> User:
    return User(
        user_id=user_db.id,
        username=user_db.username,
        surname=user_db.surname,
        email=user_db.email,
        is_email_verified=user_db.is_email_verified,
        is_blocked=user_db.is_blocked,
        hashed_password="",
    )
