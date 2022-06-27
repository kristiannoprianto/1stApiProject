from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/vote",
    tags= ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def send_vote(payload: schemas.Vote,db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    fetch_post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {payload.post_id} doesn't exist")
    else:
        vote_status = db.query(models.Vote).filter(models.Vote.post_id == payload.post_id,models.Vote.user_id == current_user.id)
        fetch_vote=vote_status.first()
    if payload.vote_dir == 1:
        if fetch_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already vote post {payload.post_id}")
        add_vote = models.Vote(user_id=current_user.id , post_id=payload.post_id)
        db.add(add_vote)
        db.commit()
        return {"message": "Voted", "value": 1}
    else:
        if not fetch_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not yet vote or doesn't exist")
        vote_status.delete(synchronize_session=False)
        db.commit()
        return {"message": "Unvoted", "value": 0}