#src/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, SubModel, UserModel


#region sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}  # it's for sqlite only
# )
#endregion

#region mysql
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:1234@db:3306/subs_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#endregion

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
