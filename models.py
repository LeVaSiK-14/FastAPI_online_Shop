from sqlalchemy import String, Integer, Boolean, ForeignKey, Column, Date, Text, Table
from sqlalchemy.orm import relationship
from database import Base
from passlib.hash import bcrypt 


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password)



categoryitem = Table(
    "categoryitem",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("category_id", ForeignKey("categorys.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = 'categorys'

    id=Column(Integer, primary_key=True, unique=True, index=True)
    name=Column(String(255), unique=True, nullable=False)
    items = relationship(
                    "Item", 
                    secondary=categoryitem,
                    back_populates="categorys"
    )


class Item(Base):

    __tablename__ = 'items'

    id=Column(Integer, primary_key=True, unique=True, index=True)
    name=Column(String(255), nullable=False, unique=True)
    description=Column(Text, nullable=False)
    created_at=Column(Date)
    price=Column(Integer, default=0, nullable=False)
    on_offer=Column(Boolean, default=False)
    categorys = relationship(
                    "Category",
                    secondary=categoryitem,
                    back_populates="items")

    def __repr__(self):
        return f"<Item name={self.name} price={self.price} created_at={self.created_at}/>"
