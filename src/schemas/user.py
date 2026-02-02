#src/schemas/user.py
from typing import Annotated

from pydantic import BaseModel
from pydantic.types import StringConstraints

from src.constants import MIN_USER_NAME_LENGTH, MAX_USER_NAME_LENGTH


class User(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(min_length=MIN_USER_NAME_LENGTH, max_length=MAX_USER_NAME_LENGTH)]


class NewUser(BaseModel):
    name: Annotated[str, StringConstraints(min_length=MIN_USER_NAME_LENGTH, max_length=MAX_USER_NAME_LENGTH)]
