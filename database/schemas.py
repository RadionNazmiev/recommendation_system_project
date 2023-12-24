import datetime
from typing import Optional

from pydantic import BaseModel


class GetPost(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

class GetUser(BaseModel):
    id: int
    age: int
    city: str
    country: str
    exp_group: int
    gender: int
    os: str
    source: str

    class Config:
        orm_mode = True

class GetFeed(BaseModel):
    user_id: int
    post_id: int
    action: str
    timestamp: datetime.datetime
    target: Optional[int] = None
    
    user: GetUser
    post: GetPost

    class Config:
        orm_mode = True