from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    user: UserResponse
    #pass

    class Config:
        orm_mode = True



# class Vote(BaseModel):
    # post_id: int
    # dir: conint(le=1, ge=-1)

# class PostVote(BaseModel):
    # Post: PostResponse
    # votes: int

    # class Config:
        # orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=-1)

class PostVote(BaseModel):
    Post: PostResponse
    Vote: Optional[int]

    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
