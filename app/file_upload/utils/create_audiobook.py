from typing import Optional

from app.database.database import Session
from app.database.model import Audiobook


def create_audiobook(
    filename: str,
    ebook_id: int,
    user_id: int,
    session: Optional[Session] = None,
) -> Audiobook:
    """
    Function to create an audiobook.

    Args:
        filename (str): The name of the file.
        ebook_id (int): The ID of the ebook.
        user_id (int): The ID of the user.
        session (Optional[Session], optional): The database session. Defaults to None.

    Returns:
        Audiobook: The created audiobook.
    """
    if not session:
        with Session() as session:
            audiobook = create_audiobook(
                filename=filename,
                ebook_id=ebook_id,
                user_id=user_id,
                session=session,
            )
            return audiobook

    audiobook = Audiobook(
        filename=filename,
        ebook_id=ebook_id,
        user_id=user_id,
    )

    session.add(audiobook)
    session.commit()
    session.refresh(audiobook)

    return audiobook
