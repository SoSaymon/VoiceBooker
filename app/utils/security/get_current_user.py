from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.model import User
from typing import Optional


def get_user(email: str, session: Session) -> Optional[User]:
    """
    Retrieves a user from the database by their email.

    Args:
        email (str): The email of the user.
        session (Session): The database session to use.

    Returns:
        Optional[User]: The user if found, otherwise None.

    Raises:
        HTTPException: If the user is not found.
    """
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
