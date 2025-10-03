from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class CreateUser(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(Post):
    pass


class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse


class PostOut(BaseModel):
    Post: PostResponse
    likes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    dir: bool
