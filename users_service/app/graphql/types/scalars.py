import re
from typing import Any
import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info


@strawberry.scalar(
    description="Valid email address",
    serialize=lambda v: str(v),
    parse_value=lambda v: validate_email(v),
)
class Email:
    @staticmethod
    def parse_literal(ast: "strawberry.literal.ValueNode") -> str:
        if ast.kind == "string_value":
            return validate_email(ast.value)
        raise ValueError("Email must be a string")


def validate_email(value: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        raise ValueError("Invalid email format")
    return value.lower().strip()
