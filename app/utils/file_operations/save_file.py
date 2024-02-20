import uuid
from typing import Coroutine

from fastapi import UploadFile


def scramble_filename(filename: str) -> str:
    """
    Scrambles the filename by appending a UUID.

    Args:
        filename (str): The original filename.

    Returns:
        str: The scrambled filename.
    """
    return f"{uuid.uuid4()}.{filename.split('.')[-1]}"


async def save_file(file: UploadFile, filename: str) -> None:
    """
    Saves a file to the 'ebooks' directory.

    Args:
        file (UploadFile): The file to save.
        filename (str): The filename to save the file as.

    Returns:
        Coroutine: An awaitable representing the file saving operation.
    """
    with open(f"ebooks/{filename}", "wb") as buffer:
        buffer.write(await file.read())
