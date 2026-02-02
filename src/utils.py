#src/utils.py
from src.schemas import Sub, User
from src.models import SubModel, UserModel


def make_scheme_from_submodel(sub: SubModel) -> Sub:
    return Sub(
        id=sub.id,
        name=sub.name,
        cost=sub.cost,
        next_payment_date=sub.next_payment_date,
        category=sub.category
    )


def make_scheme_from_usermodel(user: UserModel) -> User:
    return User(
        id=user.id,
        name=user.name
    )
