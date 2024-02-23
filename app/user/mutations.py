from graphene import ObjectType

from app.user.user_mutations import (
    CreateUser,
    LoginUser,
    UpdateUser,
    DeleteUser,
    RegenerateJWT,
)


class UserMutation(ObjectType):
    """
    Mutation class for user-related operations.

    Attributes:
        create_user (CreateUser): Mutation for creating a new user.
        login_user (LoginUser): Mutation for logging in a user.
        update_user (UpdateUser): Mutation for updating a user's details.
        delete_user (DeleteUser): Mutation for deleting a user.
        refresh_token (RegenerateJWT): Mutation for regenerating a user's JWT.
    """

    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    refresh_token = RegenerateJWT.Field()
