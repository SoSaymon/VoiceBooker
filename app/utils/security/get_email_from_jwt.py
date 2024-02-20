from fastapi import Header, HTTPException
from app.user.utils.jwt import verify_jwt


def get_email_from_jwt(authorization: str = Header(None)) -> str:
    """
    Extracts the email from the JWT token in the authorization header.

    Args:
        authorization (str, optional): The authorization header. Defaults to None.

    Returns:
        str: The email extracted from the JWT token.

    Raises:
        HTTPException: If the token is invalid or the authorization header is missing.
    """
    if authorization:
        scheme, _, token = authorization.partition(" ")
        is_valid, payload = verify_jwt(token)
        if is_valid:
            return payload.get("sub")
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=401, detail="No authorization header")
