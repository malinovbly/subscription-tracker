#src/main.py
from fastapi import FastAPI

from src.api import main_router
from src.db import create_db


GLOBAL_TAGS = [
    {"name": "subs"},
    {"name": "user"}
]

app = FastAPI(global_tags=GLOBAL_TAGS)
app.include_router(main_router)

create_db()

#TODO: postgres, docker, docker-compose
