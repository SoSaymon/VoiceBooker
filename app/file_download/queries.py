from graphene import ObjectType, Field, String, Int
from typing import Optional

from app.database.database import Session
from app.database.model import Audiobook
from app.utils.decorators import logged_in


class FileDownloadQuery(ObjectType):
    """
    A class that serves as the entry point for all file download queries in the application.

    This class includes a field for `get_audiobook_filename` query, allowing for the retrieval of an audiobook's filename.

    Attributes:
        get_audiobook_filename (str): Field for the `get_audiobook_filename` query.
    """

    get_audiobook_filename: Optional[str] = Field(String, ebook_id=Int(required=True))

    @staticmethod
    @logged_in
    def resolve_get_audiobook_filename(root, info, ebook_id: int) -> Optional[str]:
        """
        The resolver method for getting an audiobook's filename.

        Args:
            root: The root object that GraphQL was called on.
            info: Provides access to execution-specific state in GraphQL.
            ebook_id (int): The ID of the ebook.

        Returns:
            str: The filename of the audiobook.
        """
        with Session() as session:
            audiobook = session.query(Audiobook).filter_by(ebook_id=ebook_id).first()
            filename = audiobook.filename
            return filename
