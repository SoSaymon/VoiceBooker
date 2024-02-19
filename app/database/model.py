from datetime import timezone, datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database.database import Base


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    last_login = Column(DateTime)

    # relationships
