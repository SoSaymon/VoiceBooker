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

app = FastAPI()

schema = Schema(query=Query, mutation=Mutation)

origins = [
    "http://localhost:3000",
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
):
    validate_authorization_header(authorization)
    email = get_email_from_jwt(authorization)

    allowed_file_types = [
        "application/pdf",
        "application/epub+zip",
    ]
    file_type = validate_file_type(file.file.read(), allowed_file_types)
    file.file.seek(0)

    filename = scramble_filename(file.filename)
    await save_file(file, filename)

    return {"filename": filename, "file_type": file_type, "email": email}


@app.get("/get-audiobook/{filename}")
async def get_audiobook(
    filename: str,
    authorization: str = Header(None),
):
    validate_authorization_header(authorization)
    old_filename = filename
    with Session() as session:
        email = get_email_from_jwt(authorization)
        user = session.query(User).filter(User.email == email).first()
        audiobook = (
            session.query(Audiobook).filter(Audiobook.filename == old_filename).first()
        )
        if not audiobook:
            return {"message": "Audiobook not found"}
        ebook = session.query(EBook).filter(EBook.id == audiobook.ebook_id).first()
        if not ebook:
            return {"message": "Ebook not found"}
        if (
            ebook.user_id != user.id or audiobook.user_id != user.id
        ) and not user.is_admin:
            return {"message": "Unauthorized"}
        filename = f"{ebook.title} - {ebook.author}.mp3"

    return FileResponse(
        f"audiobooks/{old_filename}", filename=filename, media_type="audio/mpeg"
    )


# @app.on_event("startup")
# def startup_event():
#     create_database()


app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
