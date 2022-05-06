from datetime import datetime
import email
from turtle import title
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True

class UserModel(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created: datetime
    
    class Config:
        orm_mode=True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostResponse(PostModel):
    id: int
    created: datetime
    user_id: int
    user: UserResponse
    
    class Config:
        orm_mode=True

class VoteInPost(BaseModel):
    Post: PostResponse
    post_vote_count: int
    
    class Config:
        orm_mode=True

class Token(BaseModel):
    token_type: str
    access_token: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    vote_dir: conint(ge=0,le=1)