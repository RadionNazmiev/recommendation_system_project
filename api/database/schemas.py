import datetime
from typing import Optional

from pydantic import BaseModel


class GetPost(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

class GetProcessedPost(BaseModel):
    id : int
    text: str
    topic : str
    total_tfidf : float
    max_tfidf : float
    mean_tfidf : float
    text_cluster : int
    dist_to_1st : float
    dist_to_2st : float
    dist_to_3st : float
    dist_to_4st : float
    dist_to_5st : float
    dist_to_6st : float
    dist_to_7st : float
    dist_to_8st : float
    dist_to_9st : float
    dist_to_10st : float
    dist_to_11st : float
    dist_to_12st : float
    dist_to_13st : float
    dist_to_14st : float
    dist_to_15st : float
    dist_to_16st : float
    dist_to_17st : float
    dist_to_18st : float
    dist_to_19st : float
    dist_to_20st : float

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