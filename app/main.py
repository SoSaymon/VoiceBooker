from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.database.utils.load_data import create_database
from app.gql.mutations import Mutation
from app.gql.queries import Query

app = FastAPI()

schema = Schema(query=Query, mutation=Mutation)


# @app.on_event("startup")
# def startup_event():
#     create_database()


app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
