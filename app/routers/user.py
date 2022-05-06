from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import update
from .. import models, schemas, utilities
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payload: schemas.UserModel, db: Session = Depends(get_db)):
    hashed_pwd=utilities.hash(payload.password)
    payload.password=hashed_pwd
    add_user = models.User(**payload.dict())
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    return add_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    your_user=db.query(models.User).filter(models.User.id == id).first()
    if not your_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not found or doesn't exist")
    return your_user