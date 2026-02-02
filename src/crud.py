#src/crud.py
from typing import Optional
from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy import select, func
from sqlalchemy.orm import Session

import src.exceptions as exceptions
from src.models import SubModel, UserModel
from src.schemas import NewSub


#region User

def create_new_user(db: Session, username: str) -> UserModel:
    """
    Create a new user (UserModel) in db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        username (str): New username

    Returns:
        UserModel (src.models.UserModel): User model

    Raises:
        exceptions.UsernameNotUniqueException: Username already exists
    """
    if not __username_is_unique(db, username):
        raise exceptions.UsernameNotUniqueException()
    db_user = UserModel(name=username)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    return db_user


def get_db_user(db: Session, user_id: int = None, username: str = None, update_next_payment_dates: bool = False) -> UserModel:
    """
    Get user (UserModel) and update all next_payment_dates for user subscriptions in db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id
        username (str): Username
        update_next_payment_dates (bool): Update next payment dates or not

    Returns:
        UserModel (src.models.UserModel): User model

    Raises:
        ValueError: If neither user_id nor name is provided
        exceptions.UserIsNoneException: User not found
    """
    if user_id is None and username is None:
        raise ValueError("Either user_id or name must be provided")
    user: Optional[UserModel] = None
    if user_id is not None:
        user = db.query(UserModel).filter_by(id=user_id).first()
    elif username is not None:
        user = db.query(UserModel).filter_by(name=username).first()
    if user is None:
        raise exceptions.UserIsNoneException()
    if update_next_payment_dates:
        __update_all_next_payment_dates(db, user)
    return user


def delete_db_user(db: Session, user_id: int = None, username: str = None) -> None:
    """
    Delete user (UserModel) and his subs (SubModel) from db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id
        username (str): Username

    Returns:
        None

    Raises:
        ValueError: If neither sub_id nor sub_name is provided
        exceptions.UserIsNoneException: User not found
    """
    db_user = get_db_user(db, user_id, username)
    try:
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return None

#endregion


#region User (private)

def __username_is_unique(db: Session, username: str) -> bool:
    """
    Check if username is unique

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        username (str): Username

    Returns:
        bool: True if the username is unique, False otherwise
    """
    db_user = db.query(UserModel).filter_by(name=username).first()
    if db_user is None:
        return True
    return False

#endregion


#region Sub

def create_new_sub(db: Session, user_id: int, new_sub: NewSub) -> SubModel:
    """
    Create a new subscription (SubModel) in db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id
        new_sub (src.schemas.NewSub): New subscription scheme

    Returns:
        SubModel (src.models.SubModel): Subscription model

    Raises:
        exceptions.UserIsNoneException: User not found
        exceptions.SubNameNotUniqueException: Subscription name already exists
    """
    if not __sub_name_is_unique(db, user_id, new_sub.name):
        raise exceptions.SubNameNotUniqueException()
    get_db_user(db, user_id)
    db_sub = SubModel(
        name=new_sub.name,
        cost=new_sub.cost,
        next_payment_date=new_sub.next_payment_date,
        category=new_sub.category,
        user_id=user_id
    )
    try:
        db.add(db_sub)
        db.commit()
        db.refresh(db_sub)
    except Exception as e:
        db.rollback()
        raise e
    return db_sub


def get_db_sub(db: Session, user_id: int, sub_id: int = None, sub_name: str = None) -> SubModel:
    """
    Get subscription (SubModel) in db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id
        sub_id (int): Unique sub id
        sub_name (str): Subscription name

    Returns:
        SubModel (src.models.SubModel): Subscription model

    Raises:
        ValueError: If neither sub_id nor sub_name is provided
        exceptions.UserIsNoneException: User not found
        exceptions.SubIsNoneException: If the subscription does not exist or belongs to another user (via get_db_sub)
    """
    get_db_user(db, user_id, update_next_payment_dates=True)
    if sub_id is None and sub_name is None:
        raise ValueError("Either sub_id or sub_name must be provided")
    query = db.query(SubModel).filter_by(user_id=user_id)
    if sub_id is not None:
        query = query.filter_by(id=sub_id)
    else:
        query = query.filter_by(name=sub_name)
    sub: Optional[SubModel] = query.first()
    if sub is None:
        raise exceptions.SubIsNoneException()
    try:
        if sub.next_payment_date < date.today():
            sub.next_payment_date += relativedelta(months=+1)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return sub


def get_next_payment_db_sub(db: Session, user_id: int) -> SubModel:
    """
    Get subscription (SubModel) in db with nearest payment date

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id

    Returns:
        SubModel (src.models.SubModel): Subscription model

    Raises:
        exceptions.UserIsNoneException: User not found
        exceptions.UserHasNoSubsException: If user has no subscriptions
    """
    get_db_user(db, user_id, update_next_payment_dates=True)
    today = date.today()
    next_payment_db_sub: Optional[SubModel] = (
        db.query(SubModel)
        .filter_by(user_id=user_id)
        .filter(SubModel.next_payment_date >= today)
        .order_by(SubModel.next_payment_date.asc())
        .first()
    )
    if next_payment_db_sub is None:
        raise exceptions.UserHasNoSubsException()
    return next_payment_db_sub


def count_monthly_amount(db: Session, user_id: int) -> float:
    """
    Gets the amount of the user's monthly payments

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id

    Returns:
        float: Amount of monthly payments

    Raises:
        ValueError: If neither user_id nor name is provided to func get_db_user()
        exceptions.UserIsNoneException: User not found
        exceptions.UserHasNoSubsException: If user has no subscriptions
    """
    user = get_db_user(db, user_id)
    if len(user.subs) == 0:
        raise exceptions.UserHasNoSubsException()
    result = sum(sub.cost for sub in user.subs)
    return result


def delete_db_sub(db: Session, user_id: int, sub_id: int = None, sub_name: str = None) -> None:
    """
    Delete subscription (SubModel) from db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id
        sub_id (int): Unique sub id
        sub_name (str): Subscription name

    Returns:
        None

    Raises:
        ValueError: If neither sub_id nor sub_name is provided
        exceptions.UserIsNoneException: User not found
        exceptions.SubIsNoneException: If the subscription does not exist or belongs to another user (via get_db_sub)
    """
    db_sub = get_db_sub(db, user_id, sub_id, sub_name)
    try:
        db.delete(db_sub)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return None


def delete_all_user_db_subs(db: Session, user_id: int) -> None:
    """
    Delete all subscriptions (SubModel) of a user (UserModel) from db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id

    Returns:
        None

    Raises:
        ValueError: If neither sub_id nor sub_name is provided
        exceptions.UserIsNoneException: User not found
    """
    get_db_user(db, user_id)
    try:
        db.query(SubModel).filter_by(user_id=user_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return None

#endregion


#region Sub (private)

def __sub_name_is_unique(db: Session, user_id: int, sub_name: str) -> bool:
    """
    Check if sub_name is unique

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user_id (int): Unique user id
        sub_name (str): Subscription name

    Returns:
        bool: True if the subscription name is unique, False otherwise
    """
    unique = db.query(SubModel).filter_by(user_id=user_id, name=sub_name).first() is None
    return unique


def __update_all_next_payment_dates(db: Session, user: UserModel) -> None:
    """
    Update all next_payment_dates for user subscriptions in db

    Args:
        db (sqlalchemy.orm.Session): Database connection session
        user (src.models.UserModel): User model

    Returns:
        None
    """
    if not user.subs:
        return None
    try:
        today = date.today()
        changed = False
        for sub in user.subs:
            while sub.next_payment_date < today:
                sub.next_payment_date += relativedelta(months=+1)
                changed = True
        if changed:
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return None

#endregion
