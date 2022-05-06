from operator import and_
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.VoteInPost])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    # raw sql
    # cursor.execute("""SELECT * FROM posts""")
    # the_post=cursor.fetchall()
    
    the_post=db.query(models.Post, func.count(models.Vote.post_id).label('post_vote_count')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return the_post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostModel, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(" INSERT INTO posts (title, content) VALUES(%s, %s) ", (payload.title, payload.content))
    # conn.commit()
    add_post = models.Post(user_id=current_user.id ,**payload.dict())
    db.add(add_post)
    db.commit()
    db.refresh(add_post)
    return add_post

@router.get("/{id}", response_model=schemas.VoteInPost)
def get_post(id: int, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(" SELECT * FROM posts WHERE id = %s", (str(id),))
    # your_post=cursor.fetchone()
    your_post=db.query(models.Post, func.count(models.Vote.post_id).label('post_vote_count')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not your_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not found or doesn't exist")
    return your_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id),))
    # index_of_post=cursor.fetchone()
    # conn.commit()
    index_of_post=db.query(models.Post).filter(models.Post.id == id)
    if index_of_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not found or doesn't exist")
    index_of_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, payload: schemas.PostModel, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s returning *", (payload.title, payload.content, str(id)))
    # post_index=cursor.fetchone()
    # conn.commit()
    post_index=db.query(models.Post).filter(and_(models.Post.user_id==current_user.id, models.Post.id==id))
    grab_post=post_index.first()
    print(grab_post)
    if grab_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found or doesn't exist")
    post_index.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post_index.first()