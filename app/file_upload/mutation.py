from graphene import ObjectType
from typing import Type

from app.file_upload.file_upload_mutations import CreateFileUpload, DeleteFileUpload


class FileUploadMutation(ObjectType):
    """
    A class that serves as the entry point for all file upload mutations in the application.

    This class includes fields for `CreateFileUpload` and `DeleteFileUpload` mutations, allowing for the creation and
    deletion of file uploads.

    Attributes:
        create_file_upload (CreateFileUpload): Field for the `CreateFileUpload` mutation.
        delete_file_upload (DeleteFileUpload): Field for the `DeleteFileUpload` mutation.
    """

    create_file_upload: Type[CreateFileUpload] = CreateFileUpload.Field()
    delete_file_upload: Type[DeleteFileUpload] = DeleteFileUpload.Field()
