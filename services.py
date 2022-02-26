from fastapi import security
import database
from sqlalchemy import orm
import models
import schemas
from passlib.hash import bcrypt 
import jwt
from fastapi import Depends, HTTPException


SECRET_KEY = "MyJWTSecretKey"
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email==email).first()
        


async def create_user(user: schemas.User, db: orm.Session):
    user_obj = models.User(email=user.email, username=user.username, password=bcrypt.hash(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return user_obj
    
    
async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.User):
    user_obj = schemas.UserLogin.from_orm(user)
    
    token = jwt.encode(user_obj.dict(), SECRET_KEY)
    
    return dict(access_token=token, token_type='baerer')
    
    
async def get_current_user(
    db: orm.Session = Depends(get_db),
    token: str = Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = db.query(models.User).filter(models.User.email == payload["email"]).first()
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return schemas.User.from_orm(user)