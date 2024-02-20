from typing import Optional

from graphene import ObjectType, Field, String
from app.database.database import Session
from app.database.model import User
from app.gql.types import UserObject


class UserQuery(ObjectType):
    """
    Query for fetching a user's details.

    Args:
        username (str): The username of the user.

    Returns:
        UserQuery: The user's details.
    """

    get_user = Field(UserObject, username=String(required=True))

    @staticmethod
    def resolve_get_user(root, info, username: str) -> Optional[User]:
        """
        Resolves the get_user query.

        Args:
            root: The root object that's passed to all resolution functions.
            info: Contains information about the execution state of the query.
            username (str): The username of the user.

        Returns:
            Optional[User]: The user's details if found, else None.
        """
        return Session.query(User).filter(User.username == username).first()
