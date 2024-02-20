from functools import wraps
from typing import Callable, Any
from graphql import GraphQLError

from app.database.model import User
from app.user.utils.user import get_authenticated_user


def logged_in(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to ensure the user is logged in.

    Args:
        func (Callable[..., Any]): The function to be decorated.

    Returns:
        Callable[..., Any]: The decorated function.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        info = args[1]
        user_token = get_authenticated_user(info.context)

        if user_token is None:
            raise GraphQLError("Authentication failed")

        user: User = user_token[0]

        if not user:
            raise GraphQLError("You have to be logged in to perform this action")

        return func(*args, **kwargs)

    return wrapper
