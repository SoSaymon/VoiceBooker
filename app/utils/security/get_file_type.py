import magic
from typing import Union


def get_file_type(file: Union[bytes, bytearray]) -> str:
    """
    Determines the MIME type of a file.

    Args:
        file (Union[bytes, bytearray]): The file data.

    Returns:
        str: The MIME type of the file.
    """
    return magic.Magic(mime=True).from_buffer(file)
