from fastapi import APIRouter, Depends,status,HTTPException,responses
from sqlalchemy.orm import Session
from .. import database, schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router=APIRouter(tags=['authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_details: OAuth2PasswordRequestForm=Depends(),db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_details.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    
    if not utils.verify(user_details.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    
    access_token=oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}