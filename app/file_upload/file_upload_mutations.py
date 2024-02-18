from graphene import Mutation, String, Boolean, Field, Int
from graphql import GraphQLError

from app.database.database import Session
from app.database.model import FileUpload
from app.gql.types import FileUploadObject
from app.user.utils.user import get_authenticated_user


class CreateFileUpload(Mutation):
    class Arguments:
        filename = String(required=True)
        file_type = String(required=True)

    ok = Boolean()
    file_upload = Field(FileUploadObject)

    @staticmethod
    def mutate(root, info, filename: str, file_type: str):
        with Session() as session:
            token_user = get_authenticated_user(info.context)
            user = token_user[0]

            file_upload = FileUpload(
                filename=filename, file_type=file_type, user_id=user.id
            )

            session.add(file_upload)
            session.commit()
            session.refresh(file_upload)

            return CreateFileUpload(ok=True, file_upload=file_upload)


class DeleteFileUpload(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, id: int):
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
