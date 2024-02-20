from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError

from app.utils.load_env import getenv


def is_password_secure(password: str) -> bool:
    """
    Checks if the provided password is secure.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is secure, else raises a GraphQLError.
    """
    MIN_PASSWORD_LENGTH = int(getenv("MIN_PASSWORD_LENGTH", 8))

    if len(password) < MIN_PASSWORD_LENGTH:
        raise GraphQLError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )

    # password requirements
    # - at least 8 characters
    # - at least 1 uppercase letter
    # - at least 1 lowercase letter
    # - at least 1 number
    # - at least 1 special character
    # - no spaces
    # - no unicode characters

    if not any(char.isupper() for char in password):
        raise GraphQLError("Password must contain at least 1 uppercase letter")
    if not any(char.islower() for char in password):
        raise GraphQLError("Password must contain at least 1 lowercase letter")
    if not any(char.isdigit() for char in password):
        raise GraphQLError("Password must contain at least 1 number")
    if not any(not char.isalnum() for char in password):
        raise GraphQLError("Password must contain at least 1 special character")
    if " " in password:
        raise GraphQLError("Password must not contain spaces")
    if not all(ord(char) < 128 for char in password):
        raise GraphQLError("Password must not contain unicode characters")

    return True


def hash_password(password: str) -> str:
    """
    Hashes the provided password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> None:
    """
    Verifies the provided password against the hashed password.

    Args:
        hashed_password (str): The hashed password.
        password (str): The password to verify.

    Returns:
        None: If the password is verified, else raises a GraphQLError.
    """
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")
