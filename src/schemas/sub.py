#src/schemas/sub.py
from typing import Annotated
from datetime import date

from pydantic import BaseModel, Field, field_validator
from pydantic.types import StringConstraints

from src.constants import MIN_SUB_NAME_LENGTH, MAX_SUB_NAME_LENGTH, MIN_SUB_COST, MIN_MONTH_COUNT, Category


class Sub(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(min_length=MIN_SUB_NAME_LENGTH, max_length=MAX_SUB_NAME_LENGTH)]
    cost: Annotated[float, Field(ge=MIN_SUB_COST)]
    next_payment_date: date
    category: Category = Category.OTHER


class NewSub(BaseModel):
    name: Annotated[str, StringConstraints(min_length=MIN_SUB_NAME_LENGTH, max_length=MAX_SUB_NAME_LENGTH)]
    cost: Annotated[float, Field(ge=MIN_SUB_COST)]
    next_payment_date: date
    category: Category = Category.OTHER

    @field_validator("next_payment_date")
    @classmethod
    def date_must_be_in_future(cls, value: date):
        if value < date.today():
            raise ValueError("the next payment date cannot be in the past")
        return value


class AmountResponse(BaseModel):
    month_count: Annotated[int, Field(ge=MIN_MONTH_COUNT)]
    amount: Annotated[float, Field(ge=MIN_SUB_COST)]
