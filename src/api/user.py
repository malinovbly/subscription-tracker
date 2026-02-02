#src/api/user.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import src.exceptions as exceptions
from src.db import get_db
from src.schemas import User, NewUser, Ok
from src.crud import create_new_user, delete_db_user
from src.utils import make_scheme_from_usermodel


router = APIRouter()


#region POST

@router.post(path="/register", tags=["user"], response_model=User)
def create_user(
    new_user: NewUser,
    db: Session = Depends(get_db)
):
    try:
        user = create_new_user(db, new_user.name)
        return make_scheme_from_usermodel(user)
    except exceptions.UsernameNotUniqueException:
        raise HTTPException(status_code=409, detail=exceptions.DetailsForHTTPExceptions.UserNameNotUniqueException)

#endregion


#region DELETE

@router.delete(path="/delete-user/by-id", tags=["user"], response_model=Ok)
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        delete_db_user(db, user_id=user_id)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    return Ok()


@router.delete(path="/delete-user/by-name", tags=["user"], response_model=Ok)
def delete_user_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    try:
        delete_db_user(db, username=name)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    return Ok()

#endregion
