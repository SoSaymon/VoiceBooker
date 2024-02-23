from typing import List, Union, Dict
from fastapi import FastAPI, UploadFile, File, Header
from graphene import Schema
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.database.database import Session
from app.database.model import User, Audiobook, EBook
from app.gql.mutations import Mutation
from app.gql.queries import Query
from app.utils.file_operations.save_file import scramble_filename, save_file
from app.utils.security.get_email_from_jwt import get_email_from_jwt
from app.utils.security.validators.validate_authorization_header import (
    validate_authorization_header,
)
from app.utils.security.validators.validate_file_type import validate_file_type

app: FastAPI = FastAPI()

schema: Schema = Schema(query=Query, mutation=Mutation)

origins: List[str] = [
    "http://localhost:3000",
    "http://localhost:3000/upload-ebook",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST"],
    allow_headers=["*"],
)


@app.post("/upload-ebook")
async def upload_ebook(
    file: UploadFile = File(...),
    authorization: str = Header(None),
) -> Dict[str, str]:
    """
    Uploads an ebook to the server.

    Args:
        file (UploadFile): The file to be uploaded.
        authorization (str): The authorization token.

    Returns:
        dict: A dictionary containing the filename, file_type, and email.
    """
    validate_authorization_header(authorization)
    email: str = get_email_from_jwt(authorization)

    allowed_file_types: List[str] = [
        "application/pdf",
        "application/epub+zip",
    ]
    file_type: str = validate_file_type(file.file.read(), allowed_file_types)
    file.file.seek(0)

    filename: str = scramble_filename(file.filename)
    await save_file(file, filename)

    return {"filename": filename, "file_type": file_type, "email": email}


@app.get("/get-audiobook/{filename}")
async def get_audiobook(
    filename: str,
    authorization: str = Header(None),
):
    """
    Retrieves an audiobook from the server.

    Args:
        filename (str): The filename of the audiobook.
        authorization (str): The authorization token.

    Returns:
        dict: A dictionary containing the message or the FileResponse.
    """
    # Validate authorization header
    validate_authorization_header(authorization)

    with Session() as session:
        # Extract email from JWT token
        email: str = get_email_from_jwt(authorization)
        # Retrieve user based on email
        user: User = session.query(User).filter(User.email == email).first()
        # Retrieve audiobook based on filename
        audiobook: Audiobook = (
            session.query(Audiobook)
            .filter(Audiobook.filename == filename)
            .first()
        )

        if not audiobook:
            return {"message": "Audiobook not found"}

        # Check if the user is authorized to access the audiobook
        if user.is_admin or audiobook.user_id == user.id:
            # Construct the filename for the response
            filename = f"{audiobook.title}.mp3"
            # Return the audiobook file as FileResponse
            return FileResponse(
                f"audiobooks/{filename}",
                filename=filename,
                media_type="audio/mpeg"
            )
        else:
            return {"message": "Unauthorized"}




app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
