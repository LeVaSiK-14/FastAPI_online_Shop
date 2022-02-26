from fastapi import FastAPI, status, HTTPException, Response, Depends
import services
import datetime
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal

import models

from schemas import (
                Item, 
                ItemUpdate, 
                ItemCreate, 
                Category, 
                CategoryCreateUpdate,
                ItemSchema,
                CategorySchema,
                CategoryAdd,
                User,
                UserLogin,
                UserSchemas
)

app = FastAPI()
db = SessionLocal()


@app.post('/api/users')
async def create_user(user: User, db: Session = Depends(services.get_db)):
    db_user = await services.get_user_by_email(user.email, db)
    if db_user is not None:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail='Email alredy exists'
        )
    return await services.create_user(user, db)
    

@app.post('/api/token')
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(services.get_db)
):
    user = await services.authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='this user is not registered'
        )
    return await services.create_token(user)
    


@app.get('/users', response_model=list[UserSchemas], status_code=status.HTTP_200_OK)
async def get_all_users():
    users = db.query(models.User).all()
    return users


@app.get('/api/users/me',  response_model=User)
async def get_user(user: User=Depends(services.get_current_user)):
    return user



@app.get(
        '/categorys', 
        response_model=list[CategorySchema], 
        status_code=status.HTTP_200_OK
)
async def get_categorys():
    categorys = db.query(models.Category).all()
    return categorys


@app.get(
        '/category/{category_id}', 
        response_model=CategorySchema, 
        status_code=status.HTTP_200_OK
)
async def get_an_category(category_id: int):
    db_item = db.query(models.Category).filter(models.Category.id==category_id).first()
    if db_item is None:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f'category with id {category_id} not found'
        )
    return db_item


@app.post(
        '/categorys', 
        response_model=CategorySchema, 
        status_code=status.HTTP_201_CREATED
)
async def create_category(category: CategoryCreateUpdate):
    new_category = models.Category(
        name = category.name
    )

    db_category = db.query(models.Category).filter(models.Category.name==new_category.name).first()

    if db_category is not None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Category with name {new_category.name} is alredy yet'
        )
    
    db.add(new_category)
    db.commit()

    return new_category


@app.put(
        '/category/{category_id}',
        response_model=CategorySchema, 
        status_code=status.HTTP_200_OK
)
async def update_category(category_id: int, category: CategoryCreateUpdate):
    db_category = db.query(models.Category).filter(models.Category.id==category_id).first()

    if db_category is None:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f'Category with id {category_id} not found'
        )
    db_category.name = category.name
    db.commit()
    return db_category


@app.delete(
        '/category/{category_id}', 
        status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id==category_id).first()
    if db_category is None:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Category with id {category_id} not found'
        )
    db.delete(db_category)
    db.commit()
    return Response("success")








@app.get(
        '/items', 
        response_model=list[ItemSchema], 
        status_code=status.HTTP_200_OK
)
async def get_all_items():
    items = db.query(models.Item).all()
    return items


@app.get(
        '/item/{item_id}', 
        response_model=ItemSchema, 
        status_code=status.HTTP_200_OK
)
async def get_an_item(item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id==item_id).first()
    if db_item is None:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f'Item with id {item_id} not found'
        )
    return db_item






@app.post(
        '/item/create', 
        response_model=ItemSchema, 
        status_code=status.HTTP_201_CREATED
)
async def create_an_item(item: ItemCreate, categorys: CategoryAdd):
    new_item = models.Item(
        name=item.name,
        description=item.description,
        created_at=datetime.date.today(),
        price=item.price,
        on_offer=item.on_offer
    )
    db_item = db.query(models.Item).filter(models.Item.name==new_item.name).first()


    if db_item is not None:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Item alredy exists"
        )
    db_categorys = []

    for category in categorys:
        c = db.query(models.Category).filter(models.Category.id==category[1]).first()
        if c is not None:
            db_categorys.append(c)
        else:
            continue
    
    new_item.categorys = db_categorys

    db.add(new_item)
    db.commit()

    return new_item


# @app.put(
#         '/item/{item_id}', 
#         response_model=ItemSchema, 
#         status_code=status.HTTP_200_OK
# )
# async def update_an_item(item_id: int, item: ItemUpdate, categorys: list[CategoryAdd]):

#     update_item = db.query(models.Item).filter(models.Item.id==item_id).first()
#     if update_item is None:
#         raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, 
#                     detail=f'Item with id {item_id} not found'
#         )

#     update_item.id = update_item.id
#     update_item.name = item.name
#     update_item.description=item.description,
#     update_item.created_at=update_item.created_at,
#     update_item.price=item.price,
#     update_item.on_offer=item.on_offer
#     for category in categorys:

#         update_item.categorys.append(category)

#     db.commit()

#     return update_item


@app.delete(
        '/item/{item_id}', 
        status_code=status.HTTP_204_NO_CONTENT
)
async def delete_an_item(item_id: int):
    delete_item = db.query(models.Item).filter(models.Item.id==item_id).first()
    if delete_item is None:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f'Item with id {item_id} not found'
        )
    
    db.delete(delete_item)
    db.commit()

    return Response('Success')
