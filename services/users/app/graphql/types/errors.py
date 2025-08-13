import re
from graphql import GraphQLError


class Validation:

    USERNAME_ALLOWED = re.compile(r"^[a-zA-Z0-9._-]+$")
    USERNAME_NO_DOUBLE_SYMBOLS = re.compile(
        r"(--|\.\.|__|_-|-_|-\.|\.-|\.{2,}|_{2,}|-{2,})"
    )
    USERNAME_NO_BOUNDARY_SYMBOLS = re.compile(r"^[-_.]|[-_.]$")

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise Errors.validation(
                message="Invalid password",
                obj="password",
                rule="must be at least 8 characters long",
            )

    @staticmethod
    def validate_username(username: str):
        if len(username) < 3:
            raise Errors.validation(
                message="Username is too short",
                obj="username",
                rule="username is too short",
            )

        if len(username) > 30:
            raise Errors.validation(
                message="Username is too long",
                obj="username",
                rule="username is too long",
            )

        if not Validation.USERNAME_ALLOWED.match(username):
            raise Errors.validation(
                message="Username contains disallowed characters",
                obj="username",
                rule="username has invalid characters",
            )

        if Validation.USERNAME_NO_BOUNDARY_SYMBOLS.search(username):
            raise Errors.validation(
                message="Username cannot start or end with '.', '-', or '_'",
                obj="username",
                rule="username can't start or end with boundary character",
            )

        if Validation.USERNAME_NO_DOUBLE_SYMBOLS.search(username):
            raise Errors.validation(
                message="Username contains repeated special characters",
                obj="username",
                rule="username can't contain consecutive specials",
            )

    @staticmethod
    def validate_email(email):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise Errors.validation(
                message="Invalid email address",
                obj="email",
                rule="must be a valid email address",
            )

    @staticmethod
    def validate_user(user):
        if user.password is not None:
            Validation.validate_password(user.password)
        if user.username is not None:
            Validation.validate_username(user.username)
        if user.email is not None:
            Validation.validate_email(user.email)


class Errors:
    @staticmethod
    def not_found(obj: str, location: str) -> GraphQLError:
        return GraphQLError(
            message=f"{obj} not found",
            extensions={
                "code": "NOT_FOUND_ERROR",
                "details": {"obj": obj, "location": location},
            },
        )

    @staticmethod
    def validation(message: str, obj: str, rule: str):
        raise GraphQLError(
            message=message,
            extensions={
                "code": "VALIDATION_ERROR",
                "details": {
                    "obj": obj,
                    "rule": rule,
                },
            },
        )
