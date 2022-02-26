from pydantic import BaseModel, Field, validator
from datetime import date


class UserSchemas(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str = Field(..., min_length=5, max_length=127)
    email: str = Field(..., min_length=9, max_length=127)
    password: str = Field(..., min_length=8, max_length=63)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "LeVaSiK",
                "email": "lev201611@gmail.com",
                "password": "LeVaSiK123#"
            }
        }


class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "LeVaSiK",
                "password": "LeVaSiK123#"
            }
        }



class Item(BaseModel):
    id: int
    name: str
    description: str
    created_at: date
    price: int
    on_offer: bool

    class Config:
        orm_mode=True
        allow_population_by_field_name = True


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
        allow_population_by_field_name = True


class ItemUpdate(BaseModel):
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode=True
        allow_population_by_field_name = True


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CategoryAdd(BaseModel):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CategoryCreateUpdate(BaseModel):
    name: str = Field(..., min_length=5, max_length=127)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ItemSchema(Item):
    categorys: list[Category] = []


class CategorySchema(Category):
    items: list[Item] = []
