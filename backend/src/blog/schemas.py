from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    user_id: int

    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog]

    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    id: int
    author: ShowUser
    title: str
    body: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
