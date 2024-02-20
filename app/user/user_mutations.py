from datetime import datetime, timezone
from typing import Optional, Type

from graphene import Mutation, String, Boolean, Field, Int
from graphql import GraphQLError

from app.database.database import Session
from app.database.model import User
from app.gql.types import UserObject
from app.user.utils.email import is_valid_email
from app.user.utils.jwt import generate_jwt, regenerate_jwt
from app.user.utils.password import is_password_secure, hash_password, verify_password
from app.user.utils.user import get_authenticated_user
from app.utils.decorators import logged_in


class CreateUser(Mutation):
    """
    Mutation for creating a new user.

    Args:
        username (str): The username of the new user.
        email (str): The email of the new user.
        password (str): The password of the new user.
        full_name (str): The full name of the new user.

    Returns:
        CreateUser: The created user.
    """

    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        full_name = String(required=True)

    ok = Boolean()
    user = Field(UserObject)

    @staticmethod
    def mutate(
        root, info, username: str, email: str, password: str, full_name: str
    ) -> Type["CreateUser"]:
        with Session() as session:
            is_valid_email(email)

            user = session.query(User).filter(User.email == email).first()

            if user:
                raise GraphQLError("Email already exists")

            user = session.query(User).filter(User.username == username).first()

            if user:
                raise GraphQLError("Username already taken")

            is_password_secure(password)

            user = User(
                username=username,
                email=email,
                password=hash_password(password),
                full_name=full_name,
                is_active=True,
                is_admin=False,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return CreateUser(ok=True, user=user)


class LoginUser(Mutation):
    """
    Mutation for logging in a user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        LoginUser: The logged in user with their token, refresh token, and user object.
    """

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()
    refresh_token = String()
    user = Field(UserObject)

    @staticmethod
    def mutate(root, info, email: str, password: str) -> Type["LoginUser"]:
        with Session() as session:
            user = session.query(User).filter(User.email == email).first()

            if not user:
                raise GraphQLError("Invalid credentials")

            verify_password(user.password, password)

            if not user.is_active:
                raise GraphQLError("User is not active")

            token = generate_jwt(email, "access")
            refresh_token = generate_jwt(email, "refresh")

            user.last_login = datetime.now(timezone.utc)

            session.commit()
            session.refresh(user)

            return LoginUser(token=token, refresh_token=refresh_token, user=user)


class UpdateUser(Mutation):
    """
    Mutation for updating a user's details.

    Args:
        user_id (int): The ID of the user to update.
        old_password (str): The old password of the user.
        username (Optional[str], optional): The new username of the user. Defaults to None.
        email (Optional[str], optional): The new email of the user. Defaults to None.
        password (Optional[str], optional): The new password of the user. Defaults to None.
        active (Optional[bool], optional): The new active status of the user. Defaults to None.
        full_name (Optional[str], optional): The new full name of the user. Defaults to None.

    Returns:
        UpdateUser: The updated user.
    """

    class Arguments:
        user_id = Int(required=True)
        old_password = String(required=True)
        username = String()
        email = String()
        password = String()
        active = Boolean()
        full_name = String()

    ok = Boolean()
    user = Field(UserObject)

    @staticmethod
    @logged_in
    def mutate(
        root,
        info,
        user_id: int,
        old_password: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        active: Optional[bool] = None,
        full_name: Optional[str] = None,
    ) -> Type["UpdateUser"]:
        user_token = get_authenticated_user(info.context)

        if user_token:
            user: User = user_token[0]
            verify_password(user.password, old_password)
        else:
            raise GraphQLError("Could not verify user")

        with Session() as session:
            if user_id:
                changed_user = session.query(User).filter(User.id == user_id).first()
                is_user_active = changed_user.is_active

                if not changed_user:
                    raise GraphQLError("User not found")

                if (user_id != user.id) or user.is_admin:
                    if username:
                        is_taken = (
                            session.query(User)
                            .filter(User.username == username)
                            .first()
                        )

                        if is_taken:
                            raise GraphQLError("Username already taken")

                        changed_user.username = username

                    if email:
                        is_valid_email(email)
                        is_taken = (
                            session.query(User).filter(User.email == email).first()
                        )

                        if is_taken:
                            raise GraphQLError("Email already taken")

                        changed_user.email = email

                    if password:
                        is_password_secure(password)
                        changed_user.password = hash_password(password)

                    if active:
                        changed_user.is_active = active

                    if full_name:
                        changed_user.full_name = full_name

                    session.commit()
                    session.refresh(changed_user)

                    return UpdateUser(ok=True, user=changed_user)
                else:
                    raise GraphQLError("You are not allowed to perform this action")


class DeleteUser(Mutation):
    """
    Mutation for deleting a user.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        DeleteUser: A boolean indicating whether the deletion was successful.
    """

    class Arguments:
        user_id = Int(required=True)

    ok = Boolean()

    @staticmethod
    @logged_in
    def mutate(root, info, user_id: int) -> Type["DeleteUser"]:
        user_token = get_authenticated_user(info.context)

        if user_token:
            user: User = user_token[0]
        else:
            raise GraphQLError("Could not verify user")

        with Session() as session:
            if user_id:
                changed_user = session.query(User).filter(User.id == user_id).first()

                if not changed_user:
                    raise GraphQLError("User not found")

                if (user_id != user.id) or user.is_admin:
                    session.delete(changed_user)
                    session.commit()
                    return DeleteUser(ok=True)
                else:
                    raise GraphQLError("You are not allowed to perform this action")
            else:
                raise GraphQLError("User not found")


class RegenerateJWT(Mutation):
    """
    Mutation for regenerating a user's JWT.

    Returns:
        RegenerateJWT: The regenerated JWT, refresh token, and user object.
    """

    token = String()
    refresh_token = String()
    user = Field(UserObject)

    @staticmethod
    def mutate(root, info) -> Type["RegenerateJWT"]:
        user, token = get_authenticated_user(info.context, regeneration=True)
        tokens = regenerate_jwt(token)
        token = tokens[0]
        refresh_token = tokens[1]

        return RegenerateJWT(token=token, refresh_token=refresh_token, user=user)
