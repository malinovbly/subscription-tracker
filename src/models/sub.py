#src/models/sub.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, CheckConstraint, func, Enum as SqlEnum
from sqlalchemy.orm import relationship

from src.models import Base
from src.schemas import Category


class SubModel(Base):
    __tablename__ = "sub"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    next_payment_date = Column(Date, nullable=False)
    category = Column(SqlEnum(Category), default=Category.OTHER, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("UserModel", back_populates="subs")

    __table_args__ = (
        CheckConstraint(next_payment_date >= func.current_date(), name='check_future_date'),
    )
