from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, PrimaryKeyConstraint, inspect
from sqlalchemy.orm import relationship, composite

from database.database import Base, engine, SessionLocal


def get_original_column(class_, column_name):
    mapper = inspect(class_)
    for column in mapper.columns:
        if column.key == column_name:
            return column
    return None

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


class ProcessedPost(Base):
    __tablename__ = "posts_info_by_radion_nazmiev"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True, name="post_id")
    topic = Column(String)
    total_tfidf = Column(Float, name="TotalTfIdf")
    max_tfidf = Column(Float, name="MaxTfIdf")
    mean_tfidf = Column(Float, name="MeanTfIdf")
    text_cluster = Column(Integer, name="TextCluster")
    dist_to_1st = Column(Float, name="DistanceTo1thCluster")
    dist_to_2st = Column(Float, name="DistanceTo2thCluster")
    dist_to_3st = Column(Float, name="DistanceTo3thCluster")
    dist_to_4st = Column(Float, name="DistanceTo4thCluster")
    dist_to_5st = Column(Float, name="DistanceTo5thCluster")
    dist_to_6st = Column(Float, name="DistanceTo6thCluster")
    dist_to_7st = Column(Float, name="DistanceTo7thCluster")
    dist_to_8st = Column(Float, name="DistanceTo8thCluster")
    dist_to_9st = Column(Float, name="DistanceTo9thCluster")
    dist_to_10st = Column(Float, name="DistanceTo10thCluster")
    dist_to_11st = Column(Float, name="DistanceTo11thCluster")
    dist_to_12st = Column(Float, name="DistanceTo12thCluster")
    dist_to_13st = Column(Float, name="DistanceTo13thCluster")
    dist_to_14st = Column(Float, name="DistanceTo14thCluster")
    dist_to_15st = Column(Float, name="DistanceTo15thCluster")
    dist_to_16st = Column(Float, name="DistanceTo16thCluster")
    dist_to_17st = Column(Float, name="DistanceTo17thCluster")
    dist_to_18st = Column(Float, name="DistanceTo18thCluster")
    dist_to_19st = Column(Float, name="DistanceTo19thCluster")
    dist_to_20st = Column(Float, name="DistanceTo20thCluster")

    
if __name__ == "__main__":
    post_text_column = get_original_column(Post, 'text')
    
    if post_text_column:
        print(f"Column '{post_text_column.key}' found in class '{Post.__name__}'.")
        print(f"Column type: {post_text_column.type}")
    else:
        print(f"Column not found in class '{Post.__name__}'.")

        




