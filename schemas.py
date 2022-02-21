
from pydantic import BaseModel, Field, validator
from datetime import date



class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    created_at: date
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserCreateUpdate(BaseModel):
    username: str = Field(..., min_length=6, max_length=127)
    email: str = Field(..., min_length=9, max_length=127)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    password: str = Field(..., min_length=8, max_length=127)

    class Config:
        orm_mode = True


class Item(BaseModel):
    id: int
    name: str
    description: str
    created_at: date
    price: int
    on_offer: bool
    category_id: int

    class Config:
        orm_mode=True


class ItemCreate(BaseModel):
    name: str
    description: str
    price: int
    on_offer: bool = Field(default=False)
    created_at: date = Field(default=date.today())

    @validator('price')
    def price_validator(cls, v):
        if v == 0:
            raise ValueError({"error": f'price must be more then {v}'})
        elif v > 100000:
            raise ValueError({"error": f"price must be less then {v}"})
        return v

    class Config:
        orm_mode=True


class ItemUpdate(BaseModel):
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode=True


class Category(BaseModel):
    id: int
    name: str
    items: list[Item] = []

    class Config:
        orm_mode = True


class CategoryCreateUpdate(BaseModel):
    name: str = Field(..., min_length=5, max_length=127)

    class Config:
        orm_mode = True
