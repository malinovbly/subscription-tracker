#src/api/__init__.py
from fastapi import APIRouter

from src.api.sub import router as sub_router
from src.api.user import router as user_router


main_router = APIRouter()

main_router.include_router(sub_router)
main_router.include_router(user_router)
