import ssl
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utilities, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user_login=db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user_login:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User does not exist")
    is_login=utilities.verify(credentials.password, user_login.password)
    if not is_login:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username and password does not match")
    
    auth_token=oauth2.create_access_token(data={"user_id": user_login.id})
    
    
    return {"access_token": auth_token, "token_type": "Bearer"}
