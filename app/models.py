import email
from enum import unique
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__= "posts"
    id= Column(Integer, primary_key=True, nullable=False)
    title= Column(String , nullable=False)
    content= Column(String , nullable=False)
    published= Column(Boolean , server_default='TRUE', nullable=False)
    created= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user= relationship("User")
    
class User(Base):
    __tablename__="users"
    id= Column(Integer, primary_key=True, nullable=False)
    email= Column(String, unique=True, nullable=False)
    password= Column(String, nullable=False)
    created= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)