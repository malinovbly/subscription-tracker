#src/models/sub.py
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship

from src.models import Base
from src.constants import Category


class SubModel(Base):
    __tablename__ = "sub"

    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    cost = Column(Numeric(precision=10, scale=2), nullable=False)
    next_payment_date = Column(Date, nullable=False)
    category = Column(SqlEnum(Category, native_enum=False), default=Category.OTHER, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("UserModel", back_populates="subs")
