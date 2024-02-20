from datetime import timezone, datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

from app.database.database import Base


class User(Base):
    """
    User model for the application.

    Attributes:
        id (int): The ID of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        full_name (str): The full name of the user.
        is_active (bool): The active status of the user.
        is_admin (bool): The admin status of the user.
        created_at (datetime): The creation time of the user.
        last_login (datetime): The last login time of the user.
        file_uploads (relationship): The relationship between the user and file uploads.
        ebooks (relationship): The relationship between the user and ebooks.
        audiobooks (relationship): The relationship between the user and audiobooks.
    """

    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True, index=True, nullable=False)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    full_name: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, nullable=False)
    is_admin: bool = Column(Boolean, nullable=False)
    created_at: datetime = Column(
        DateTime, default=datetime.now(tz=timezone.utc), nullable=False
    )
    last_login: Optional[datetime] = Column(DateTime)

    # relationships
    file_uploads = relationship("FileUpload", back_populates="user", lazy="selectin")
    ebooks = relationship("EBook", back_populates="user", lazy="selectin")
    audiobooks = relationship("Audiobook", back_populates="user", lazy="selectin")


class FileUpload(Base):
    """
    FileUpload model for the application.

    Attributes:
        id (int): The ID of the file upload.
        filename (str): The filename of the file upload.
        file_type (str): The file type of the file upload.
        user_id (int): The ID of the user who uploaded the file.
        created_at (datetime): The creation time of the file upload.
        delete_time (datetime): The deletion time of the file upload.
        user (relationship): The relationship between the file upload and the user.
        ebooks (relationship): The relationship between the file upload and ebooks.
    """

    __tablename__ = "file_uploads"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    filename: str = Column(String, nullable=False)
    file_type: str = Column(String, nullable=False)
    user_id: int = Column(ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(
        DateTime, default=datetime.now(tz=timezone.utc), nullable=False
    )
    delete_time: datetime = Column(
        DateTime,
        default=datetime.now(tz=timezone.utc) + timedelta(days=30),
        nullable=False,
    )

    # relationships
    user = relationship("User", back_populates="file_uploads", lazy="selectin")
    ebooks = relationship("EBook", back_populates="file_upload", lazy="selectin")


class Audiobook(Base):
    """
    Audiobook model for the application.

    Attributes:
        id (int): The ID of the audiobook.
        filename (str): The filename of the audiobook.
        ebook_id (int): The ID of the ebook associated with the audiobook.
        user_id (int): The ID of the user who created the audiobook.
        created_at (datetime): The creation time of the audiobook.
        delete_time (datetime): The deletion time of the audiobook.
        ebook (relationship): The relationship between the audiobook and the ebook.
        user (relationship): The relationship between the audiobook and the user.
    """

    __tablename__ = "audiobooks"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    filename: str = Column(String, nullable=False)
    ebook_id: int = Column(ForeignKey("ebooks.id"), nullable=False, unique=True)
    user_id: int = Column(ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(
        DateTime, default=datetime.now(tz=timezone.utc), nullable=False
    )
    delete_time: datetime = Column(
        DateTime,
        default=datetime.now(tz=timezone.utc) + timedelta(days=30),
        nullable=False,
    )

    # relationships
    ebook = relationship("EBook", back_populates="audiobooks", lazy="selectin")
    user = relationship("User", back_populates="audiobooks", lazy="selectin")


class EBook(Base):
    """
    EBook model for the application.

    Attributes:
        id (int): The ID of the ebook.
        title (str): The title of the ebook.
        author (str): The author of the ebook.
        summary (str): The summary of the ebook.
        file_upload_id (int): The ID of the file upload associated with the ebook.
        user_id (int): The ID of the user who created the ebook.
        created_at (datetime): The creation time of the ebook.
        last_accessed (datetime): The last accessed time of the ebook.
        file_upload (relationship): The relationship between the ebook and the file upload.
        audiobooks (relationship): The relationship between the ebook and the audiobooks.
        user (relationship): The relationship between the ebook and the user.
    """

    __tablename__ = "ebooks"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    author: str = Column(String, nullable=False)
    summary: str = Column(String, nullable=False)
    file_upload_id: int = Column(ForeignKey("file_uploads.id"), nullable=False)
    user_id: int = Column(ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(
        DateTime, default=datetime.now(tz=timezone.utc), nullable=False
    )
    last_accessed: Optional[datetime] = Column(DateTime, nullable=True)

    # relationships
    file_upload = relationship("FileUpload", back_populates="ebooks", lazy="selectin")
    audiobooks = relationship("Audiobook", back_populates="ebook", lazy="selectin")
    user = relationship("User", back_populates="ebooks", lazy="selectin")
