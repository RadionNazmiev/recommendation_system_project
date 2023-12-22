from pydantic import BaseModel
import datetime
from typing import Optional

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
    user: GetUser
    post_id: int
    post: GetPost
    timestamp: datetime.datetime
    action: str
    target: Optional[int] = None

    class Config:
        orm_mode = True