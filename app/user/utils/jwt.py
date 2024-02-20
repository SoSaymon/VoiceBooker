from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

import jwt
from graphql import GraphQLError

from app.utils.load_env import getenv

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(getenv("TOKEN_EXPIRE_MINUTES"))
TOKEN_EXPIRE_REFRESH_MINUTES = int(getenv("TOKEN_EXPIRE_REFRESH_MINUTES"))


def generate_jwt(email: str, token_type: str) -> str:
    """
    Generates a JWT for the given email and token type.

    Args:
        email (str): The email of the user.
        token_type (str): The type of the token ("access" or "refresh").

    Returns:
        str: The generated JWT.
    """
    if token_type == "access":
        expiration = get_expiration_date(TOKEN_EXPIRE_MINUTES)
    elif token_type == "refresh":
        expiration = get_expiration_date(TOKEN_EXPIRE_REFRESH_MINUTES)
    else:
        raise GraphQLError("Invalid token type")

    payload = {"sub": email, "type": token_type, "exp": expiration}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_expiration_date(expire_minutes: int) -> datetime:
    """
    Gets the expiration date for a token.

    Args:
        expire_minutes (int): The number of minutes until the token expires.

    Returns:
        datetime: The expiration date of the token.
    """
    return datetime.utcnow() + timedelta(minutes=expire_minutes)


def verify_jwt(token: str) -> Tuple[bool, Dict]:
    """
    Verifies a JWT.

    Args:
        token (str): The JWT to verify.

    Returns:
        Tuple[bool, Dict]: A tuple containing a boolean indicating whether the token is valid and the payload of the token.
    """
    try:
        payload: Dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        if datetime.now(timezone.utc) > datetime.fromtimestamp(
            payload.get("exp"), tz=timezone.utc
        ):
            raise GraphQLError("Token has expired")

        if payload.get("type") != "access":
            raise GraphQLError("Invalid token type")

        return True, payload
    except jwt.exceptions.PyJWTError:
        raise GraphQLError("Invalid token")


def verify_refresh_jwt(token: str) -> Tuple[bool, Dict]:
    """
    Verifies a refresh JWT.

    Args:
        token (str): The refresh JWT to verify.

    Returns:
        Tuple[bool, Dict]: A tuple containing a boolean indicating whether the token is valid and the payload of the token.
    """
    try:
        payload: Dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        if datetime.now(timezone.utc) > datetime.fromtimestamp(
            payload.get("exp"), tz=timezone.utc
        ):
            raise GraphQLError("Token has expired")

        if payload.get("type") != "refresh":
            raise GraphQLError("Invalid token type")

        return True, payload
    except jwt.exceptions.PyJWTError:
        raise GraphQLError("Invalid token")


def regenerate_jwt(token: str) -> Tuple[str, str]:
    """
    Regenerates a JWT and a refresh JWT.

    Args:
        token (str): The refresh JWT to use for regeneration.

    Returns:
        Tuple[str, str]: A tuple containing the regenerated JWT and refresh JWT.
    """
    valid, payload = verify_refresh_jwt(token)

    if valid:
        token = generate_jwt(payload.get("sub"), "access")
        refresh_token = generate_jwt(payload.get("sub"), "refresh")

        return token, refresh_token
    else:
        raise GraphQLError("Invalid token")
