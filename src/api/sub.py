#src/api/sub.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import src.exceptions as exceptions
from src.schemas import NewSub, Sub, Category, Ok, AmountResponse
from src.db import get_db
from src.crud import (get_db_user, create_new_sub, get_db_sub, delete_db_sub, delete_all_user_db_subs,
                      get_next_payment_db_sub, count_monthly_amount)
from src.utils import make_scheme_from_submodel


router = APIRouter()


#region POST

@router.post(path="/subs", tags=["subs"], response_model=Sub)
def post_sub(
    user_id: int,
    new_sub: NewSub,
    db: Session = Depends(get_db)
):
    try:
        db_sub = create_new_sub(db, user_id, new_sub)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.SubNameNotUniqueException:
        raise HTTPException(status_code=409, detail=exceptions.DetailsForHTTPExceptions.SubNameNotUniqueException)
    return make_scheme_from_submodel(db_sub)

#endregion


#region GET

@router.get(path="/subs", tags=["subs"], response_model=List[Sub])
def get_subs(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user = get_db_user(db, user_id, update_next_payment_dates=True)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    return user.subs


@router.get(path="/subs/by-category/{category}", tags=["subs"], response_model=List[Sub])
def get_subs_by_category(
    user_id: int,
    category: Category,
    db: Session = Depends(get_db)
):
    try:
        user = get_db_user(db, user_id, update_next_payment_dates=True)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    response = [make_scheme_from_submodel(sub) for sub in user.subs if sub.category == category]
    return response


@router.get(path="/subs/by-id/{sub_id}", tags=["subs"], response_model=Sub)
def get_sub_by_id(
    user_id: int,
    sub_id: int,
    db: Session = Depends(get_db)
):
    try:
        sub = get_db_sub(db, user_id, sub_id)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.SubIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.SubIsNoneException)
    return make_scheme_from_submodel(sub)


@router.get(path="/subs/by-name/{sub_name}", tags=["subs"], response_model=Sub)
def get_sub_by_name(
    user_id: int,
    sub_name: str,
    db: Session = Depends(get_db)
):
    try:
        sub = get_db_sub(db, user_id, None, sub_name)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.SubIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.SubIsNoneException)
    return make_scheme_from_submodel(sub)


@router.get(path="/subs/next-payment", tags=["subs"], response_model=Sub)
def get_next_payment_sub(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        next_payment_sub = get_next_payment_db_sub(db, user_id)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.UserHasNoSubsException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserHasNoSubsException)
    return next_payment_sub


@router.get(path="/subs/monthly-amount", tags=["subs"], response_model=AmountResponse)
def get_monthly_amount(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        monthly_amount = count_monthly_amount(db, user_id)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.UserHasNoSubsException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserHasNoSubsException)
    return monthly_amount


@router.get(path="/subs/annual-amount", tags=["subs"], response_model=AmountResponse)
def get_annual_amount(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        monthly_amount = count_monthly_amount(db, user_id)
        annual_amount = monthly_amount * 12
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.UserHasNoSubsException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserHasNoSubsException)
    return annual_amount

#endregion


#region DELETE

@router.delete(path="/subs", tags=["subs"], response_model=Ok)
def delete_all_subs(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        delete_all_user_db_subs(db, user_id)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    return Ok()


@router.delete(path="/subs/by-id/{sub_id}", tags=["subs"], response_model=Ok)
def delete_sub_by_id(
    user_id: int,
    sub_id: int,
    db: Session = Depends(get_db)
):
    try:
        delete_db_sub(db, user_id, sub_id=sub_id)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.SubIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.SubIsNoneException)
    return Ok()


@router.delete(path="/subs/by-name/{sub_name}", tags=["subs"], response_model=Ok)
def delete_sub_by_name(
    user_id: int,
    sub_name: str,
    db: Session = Depends(get_db)
):
    try:
        delete_db_sub(db, user_id, sub_name=sub_name)
    except exceptions.UserIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.UserIsNoneException)
    except exceptions.SubIsNoneException:
        raise HTTPException(status_code=404, detail=exceptions.DetailsForHTTPExceptions.SubIsNoneException)
    return Ok()

#endregion
