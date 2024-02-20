import threading
from typing import Optional, Tuple

from graphene import Mutation, String, Boolean, Field, Int
from graphql import GraphQLError

from app.database.database import Session
from app.database.model import FileUpload
from app.ebook.utils.create_ebook import create_ebook
from app.file_convertion.epub_to_txt import epub_to_txt
from app.file_convertion.pdf_to_txt import pdf_to_txt
from app.gql.types import FileUploadObject
from app.user.utils.user import get_authenticated_user


class CreateFileUpload(Mutation):
    """
    Mutation for creating a file upload.

    Attributes:
        ok (Boolean): Indicates if the mutation was successful.
        file_upload (FileUploadObject): The created file upload.
    """

    class Arguments:
        filename = String(required=True)
        file_type = String(required=True)
        title = String(required=True)
        author = String(required=True)
        summary = String(required=True)

    ok: Optional[bool] = Boolean()
    file_upload: Optional[FileUploadObject] = Field(FileUploadObject)

    @staticmethod
    def mutate(
        root,
        info,
        filename: str,
        file_type: str,
        title: str,
        author: str,
        summary: str,
    ) -> "CreateFileUpload":
        """
        The mutation method for creating a file upload.

        Args:
            root: The root object that GraphQL was called on.
            info: Provides access to execution-specific state in GraphQL.
            filename (str): The name of the file.
            file_type (str): The type of the file.
            title (str): The title of the ebook.
            author (str): The author of the ebook.
            summary (str): The summary of the ebook.

        Returns:
            CreateFileUpload: The mutation response.
        """
        with Session() as session:
            token_user = get_authenticated_user(info.context)
            user = token_user[0]

            file_upload = FileUpload(
                filename=filename, file_type=file_type, user_id=user.id
            )

            session.add(file_upload)
            session.commit()
            session.refresh(file_upload)

            file_upload_id = file_upload.id

            create_ebook(
                title=title,
                author=author,
                summary=summary,
                file_upload_id=file_upload_id,
                user_id=user.id,
                session=session,
            )

            if file_type == "application/pdf":
                t1 = threading.Thread(target=pdf_to_txt)
                t1.start()
            elif file_type == "application/epub+zip":
                t1 = threading.Thread(target=epub_to_txt)
                t1.start()

            return CreateFileUpload(ok=True, file_upload=file_upload)


class DeleteFileUpload(Mutation):
    """
    Mutation for deleting a file upload.

    Attributes:
        ok (Boolean): Indicates if the mutation was successful.
    """

    class Arguments:
        id = Int(required=True)

    ok: Optional[bool] = Boolean()

    @staticmethod
    def mutate(root, info, id: int) -> "DeleteFileUpload":
        """
        The mutation method for deleting a file upload.

        Args:
            root: The root object that GraphQL was called on.
            info: Provides access to execution-specific state in GraphQL.
            id (int): The ID of the file upload to delete.

        Returns:
            DeleteFileUpload: The mutation response.
        """
        with Session() as session:
            token_user = get_authenticated_user(info.context)
            user = token_user[0]

            file_upload = session.query(FileUpload).filter(FileUpload.id == id).first()

            if not file_upload:
                raise GraphQLError("FileUpload not found")

            if not (file_upload.user_id == user.id or user.is_admin):
                raise GraphQLError("You are not authorized to delete this file")

            session.delete(file_upload)
            session.commit()

            return DeleteFileUpload(ok=True)
