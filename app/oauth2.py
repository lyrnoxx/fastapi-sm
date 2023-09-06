from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

secret=settings.secret_key
algorithm=settings.algorithm
accesstokenexpire=settings.access_expire


def create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=accesstokenexpire)
    to_encode.update({"exp":expire})

    encoded= jwt.encode(to_encode,secret,algorithm=algorithm)
    return encoded

def verify_access_token(token: str, credentials_exception):
    try:    
        payload=jwt.decode(token,secret,algorithms=[algorithm])
        id : str =payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token:str=Depends(oauth2_scheme),db: Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate',headers={"WWW-Authenticate":"Bearer"})
    token= verify_access_token(token,credentials_exception) 

    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user