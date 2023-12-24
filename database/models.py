from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, composite

from database.database import Base, engine, SessionLocal


class Post(Base):
    __tablename__ = "post_text_df"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True, name="post_id")
    text = Column(String)
    topic = Column(String)


class User(Base):
    __tablename__ = "user_data"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True, name="user_id")
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    os = Column(String)
    source = Column(String)


class Feed(Base):
    __tablename__ = "feed_data"
    __table_args__ = (
        PrimaryKeyConstraint("timestamp", "user_id", "post_id"),
        {"schema": "public"},
    )

    user_id = Column(Integer, ForeignKey("public.user_data.user_id"))
    user = relationship("User")
    post_id = Column(Integer, ForeignKey("public.post_text_df.post_id"))
    post = relationship("Post")
    timestamp = Column(TIMESTAMP)
    action = Column(String)
    target = Column(Integer, nullable=True) 

 
if __name__ == "__main__":
    pass

        




