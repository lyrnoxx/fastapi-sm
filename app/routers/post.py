from fastapi import FastAPI,status,Response,HTTPException,Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func 

app=APIRouter(
    prefix="/posts",
    tags=['posts']
)


@app.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),curr_user: int=Depends(oauth2.get_current_user)
              ,limit: int =10,skip: int=0,search:Optional[str]=""):
    
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all().all()
    
    return posts
 
@app.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session=Depends(get_db),curr_user: int=Depends(oauth2.get_current_user)):
    new_post=models.Post(user_id=curr_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/{id}',response_model=schemas.PostOut)
def get_post(id: int,db: Session=Depends(get_db),curr_user: int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='no posts with that id')
    return post

@app.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int,db: Session=Depends(get_db),curr_user: int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='no post with that id')
    
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized')

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'deleted'}

@app.put('/{id}',response_model=schemas.Post)
def update_post(id: int,post: schemas.PostCreate,db: Session=Depends(get_db),curr_user: int=Depends(oauth2.get_current_user)):
    update=db.query(models.Post).filter(models.Post.id==id)
    to_update=update.first()
    if not to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='no post with that id')
   
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized')

    update.update(post.dict(),synchronize_session=False)
    db.commit()
    return update.first()
