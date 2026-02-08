#src/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False, unique=True)

    subs = relationship("SubModel", back_populates="user", cascade="all, delete-orphan")
