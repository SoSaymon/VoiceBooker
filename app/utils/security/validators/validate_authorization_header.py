from fastapi import Header, HTTPException
from typing import Optional

from app.user.utils.jwt import verify_jwt


def validate_authorization_header(authorization: Optional[str] = Header(None)) -> None:
    """
    Validates the authorization header.

    Args:
        authorization (Optional[str], optional): The authorization header. Defaults to None.

    Raises:
        HTTPException: If the token is invalid, the scheme is invalid, or the authorization header is missing.
    """
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer":
            is_valid, payload = verify_jwt(token)
            if not is_valid:
                raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="Invalid scheme")
    else:
        raise HTTPException(status_code=401, detail="No authorization header")
