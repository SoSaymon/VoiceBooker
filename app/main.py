from fastapi import FastAPI
from graphene import Schema
from starlette.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.database.utils.load_data import create_database
from app.gql.mutations import Mutation
from app.gql.queries import Query

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


# @app.on_event("startup")
# def startup_event():
#     create_database()


app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
