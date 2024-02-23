import typing
from datetime import datetime

from graphene import ObjectType, Int, String, Boolean, DateTime, List, Field


class UserObject(ObjectType):
    """
    GraphQL object type for a user.

    Attributes:
        id (Int): The user's ID.
        username (String): The user's username.
        email (String): The user's email.
        full_name (String): The user's full name.
        is_active (Boolean): Whether the user is active.
        is_admin (Boolean): Whether the user is an admin.
        created_at (DateTime): When the user was created.
        last_login (DateTime): The user's last login time.
        file_uploads (List[FileUploadObject]): The user's file uploads.
        ebooks (List[EBookObject]): The user's ebooks.
        audiobooks (List[AudiobookObject]): The user's audiobooks.
    """

    id: int = Int()
    username: str = String()
    email: str = String()
    full_name: str = String()
    is_active: bool = Boolean()
    is_admin: bool = Boolean()
    created_at: datetime = DateTime()
    last_login: datetime = DateTime()
    file_uploads: typing.List["FileUploadObject"] = List(lambda: FileUploadObject)
    ebooks: typing.List["EBookObject"] = List(lambda: EBookObject)
    audiobooks: typing.List["AudiobookObject"] = List(lambda: AudiobookObject)

    @staticmethod
    def resolve_file_uploads(root, info) -> typing.List["FileUploadObject"]:
        """Resolves the file_uploads attribute."""
        return root.file_uploads

    @staticmethod
    def resolve_ebooks(root, info) -> typing.List["EBookObject"]:
        """Resolves the ebooks attribute."""
        return root.ebooks

    @staticmethod
    def resolve_audiobooks(root, info) -> typing.List["AudiobookObject"]:
        """Resolves the audiobooks attribute."""
        return root.audiobooks


class FileUploadObject(ObjectType):
    """
    GraphQL object type for a file upload.

    Attributes:
        id (Int): The file upload's ID.
        filename (String): The name of the file.
        file_type (String): The type of the file.
        user_id (Int): The ID of the user who uploaded the file.
        created_at (DateTime): When the file was uploaded.
        delete_time (DateTime): When the file was deleted.
        user (Field): The user who uploaded the file.
        ebooks (List): The ebooks associated with the file upload.
    """

    id: int = Int()
    filename: str = String()
    file_type: str = String()
    user_id: int = Int()
    created_at: datetime = DateTime()
    delete_time: datetime = DateTime()
    user: "UserObject" = Field(lambda: UserObject)
    ebooks: typing.List["EBookObject"] = List(lambda: EBookObject)

    @staticmethod
    def resolve_user(root, info) -> "UserObject":
        """Resolves the user attribute."""
        return root.user

    @staticmethod
    def resolve_ebooks(root, info) -> typing.List["EBookObject"]:
        """Resolves the ebooks attribute."""
        return root.ebooks


class EBookObject(ObjectType):
    """
    GraphQL object type for an ebook.

    Attributes:
        id (Int): The ebook's ID.
        title (String): The title of the ebook.
        author (String): The author of the ebook.
        summary (String): The summary of the ebook.
        file_upload_id (Int): The ID of the file upload associated with the ebook.
        user_id (Int): The ID of the user who uploaded the ebook.
        created_at (DateTime): When the ebook was uploaded.
        delete_time (DateTime): When the ebook was deleted.
        file_upload (Field): The file upload associated with the ebook.
        user (Field): The user who uploaded the ebook.
        audiobooks (List): The audiobooks associated with the ebook.
    """

    id: int = Int()
    title: str = String()
    author: str = String()
    summary: str = String()
    file_upload_id: int = Int()
    user_id: int = Int()
    created_at: datetime = DateTime()
    delete_time: datetime = DateTime()
    file_upload: "FileUploadObject" = Field(lambda: FileUploadObject)
    user: "UserObject" = Field(lambda: UserObject)
    audiobooks: typing.List["AudiobookObject"] = List(lambda: AudiobookObject)

    @staticmethod
    def resolve_file_upload(root, info) -> "FileUploadObject":
        """Resolves the file_upload attribute.

        Args:
            root: The root object that's being resolved.
            info: The info object.

        Returns:
            FileUploadObject: The file upload associated with the ebook.
        """
        return root.file_upload

    @staticmethod
    def resolve_user(root, info) -> "UserObject":
        """Resolves the user attribute.

        Args:
            root: The root object that's being resolved.
            info: The info object.

        Returns:
            UserObject: The user who uploaded the ebook.
        """
        return root.user

    @staticmethod
    def resolve_audiobooks(root, info) -> typing.List["AudiobookObject"]:
        """Resolves the audiobooks attribute.

        Args:
            root: The root object that's being resolved.
            info: The info object.

        Returns:
            List[AudiobookObject]: The audiobooks associated with the ebook.
        """
        return root.audiobooks


class AudiobookObject(ObjectType):
    """
    GraphQL object type for an audiobook.

    Attributes:
        id (Int): The audiobook's ID.
        filename (String): The name of the audiobook file.
        ebook_id (Int): The ID of the ebook associated with the audiobook.
        user_id (Int): The ID of the user who uploaded the audiobook.
        created_at (DateTime): When the audiobook was uploaded.
        delete_time (DateTime): When the audiobook was deleted.
        ebook (Field): The ebook associated with the audiobook.
        user (Field): The user who uploaded the audiobook.
    """

    id: int = Int()
    filename: str = String()
    ebook_id: int = Int()
    user_id: int = Int()
    created_at: datetime = DateTime()
    delete_time: datetime = DateTime()
    ebook: "EBookObject" = Field(lambda: EBookObject)
    user: "UserObject" = Field(lambda: UserObject)

    @staticmethod
    def resolve_ebook(root, info) -> "EBookObject":
        """Resolves the ebook attribute.

        Args:
            root: The root object that's being resolved.
            info: The info object.

        Returns:
            EBookObject: The ebook associated with the audiobook.
        """
        return root.ebook

    @staticmethod
    def resolve_user(root, info) -> "UserObject":
        """Resolves the user attribute.

        Args:
            root: The root object that's being resolved.
            info: The info object.

        Returns:
            UserObject: The user who uploaded the audiobook.
        """
        return root.user
