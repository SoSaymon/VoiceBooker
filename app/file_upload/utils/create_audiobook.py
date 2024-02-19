from typing import Optional

from app.database.database import Session
from app.database.model import Audiobook


def create_audiobook(
    filename: str,
    ebook_id: int,
    user_id: int,
    session: Session = None,
) -> Audiobook:
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
