from sqlalchemy import String, Integer, Boolean, ForeignKey, Column, Date, Text
from sqlalchemy.orm import relationship

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from database import Base

import datetime


class User(Base, SQLAlchemyBaseUserTable):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(Date, default=datetime.date.today())
    is_superuser = Column(Boolean, default=False)
    password = Column(String, nullable=False)


class Category(Base):
    __tablename__ = 'categorys'

    id=Column(Integer, primary_key=True, unique=True, index=True)
    name=Column(String(255), unique=True, nullable=False)
    items = relationship("Item", back_populates="category")


class Item(Base):

    __tablename__ = 'items'

    id=Column(Integer, primary_key=True, unique=True, index=True)
    name=Column(String(255), nullable=False, unique=True)
    description=Column(Text, nullable=False)
    created_at=Column(Date)
    price=Column(Integer, default=0, nullable=False)
    on_offer=Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categorys.id'))
    category = relationship("Category", back_populates="items")

    def __repr__(self):
        return f"<Item name={self.name} price={self.price} created_at={self.created_at}/>"





