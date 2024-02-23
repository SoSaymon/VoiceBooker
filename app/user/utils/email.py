import re
from graphql import GraphQLError


def is_valid_email(email: str) -> bool:
    """
    Checks if the provided email is valid.

    Args:
        email (str): The email to check.

    Returns:
        bool: True if the email is valid, else raises a GraphQLError.
    """
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.match(email_regex, email) is None:
        raise GraphQLError("Your email is not valid")

    return True
