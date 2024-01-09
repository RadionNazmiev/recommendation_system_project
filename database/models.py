from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, PrimaryKeyConstraint, inspect
from sqlalchemy.orm import relationship, composite

from database.database import Base, engine, SessionLocal


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    os = Column(String)
    source = Column(String)


class Feed(Base):
    __tablename__ = "feeds"
    __table_args__ = (
        PrimaryKeyConstraint("timestamp", "user_id", "post_id"),
        {"schema": "public"},
    )

    user_id = Column(Integer, ForeignKey("public.users.id"))
    user = relationship("User")
    post_id = Column(Integer, ForeignKey("public.posts.id"))
    post = relationship("Post")
    timestamp = Column(TIMESTAMP)
    action = Column(String)
    target = Column(Integer, nullable=True) 


class ProcessedPost(Base):
    __tablename__ = "processed_posts"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)
    total_tfidf = Column(Float)
    max_tfidf = Column(Float)
    mean_tfidf = Column(Float)
    text_cluster = Column(Integer)
    dist_to_1st = Column(Float)
    dist_to_2st = Column(Float)
    dist_to_3st = Column(Float)
    dist_to_4st = Column(Float)
    dist_to_5st = Column(Float)
    dist_to_6st = Column(Float)
    dist_to_7st = Column(Float)
    dist_to_8st = Column(Float)
    dist_to_9st = Column(Float)
    dist_to_10st = Column(Float)
    dist_to_11st = Column(Float)
    dist_to_12st = Column(Float)
    dist_to_13st = Column(Float)
    dist_to_14st = Column(Float)
    dist_to_15st = Column(Float)
    dist_to_16st = Column(Float)
    dist_to_17st = Column(Float)
    dist_to_18st = Column(Float)
    dist_to_19st = Column(Float)
    dist_to_20st = Column(Float)

    
        




