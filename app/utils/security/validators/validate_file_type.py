from typing import List

from fastapi import HTTPException

from app.utils.security.get_file_type import get_file_type


def validate_file_type(file: bytes, allowed_file_types: List[str]) -> str:
    """
    Validates the MIME type of a file against a list of allowed types.

    Args:
        file (bytes): The file data.
        allowed_file_types (List[str]): The list of allowed MIME types.

    Returns:
        str: The MIME type of the file if it's in the list of allowed types.

    Raises:
        HTTPException: If the MIME type of the file is not in the list of allowed types.
    """
    file_type = get_file_type(file)

    if file_type not in allowed_file_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    return file_type
