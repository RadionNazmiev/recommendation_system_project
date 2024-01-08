from datetime import datetime
import os
from typing import List, Optional

from catboost import CatBoostClassifier
from fastapi import FastAPI, Depends, Path, Query, HTTPException
from loguru import logger
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy.orm import Session

from config.utils import load_config
from database.database import SessionLocal
from database.models import User, Post, Feed, ProcessedPost
from database.schemas import GetPost, GetUser, GetFeed, GetProcessedPost

CONFIG_PATH = os.path.join("config", "config.yaml")

app = FastAPI()

def _get_db():
    try:
        with SessionLocal() as db:
            yield db
    except Exception as e:
        logger.error(f"Error getting database session: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def _get_model_path(path: str) -> str:
    model_path = '/workdir/user_input/model' if os.environ.get("IS_LMS") == "1" else path
    return model_path

def _load_model():
    logger.info("Getting model path")
    model_path = _get_model_path("catboost_model")
    logger.info("Initializing and loading model")
    loaded_model = CatBoostClassifier().load_model(model_path)
    logger.info("Model loaded")
    return loaded_model

logger.info("Loading model")
model = _load_model()

def _get_results_in_chunks(query, limit=None, chunk_size=500000):
    logger.info("Starting result retrieval in chunks...")
    count = 0
    offset = 0
    results = []
    while True:
        if limit and (limit - offset) < chunk_size:
            chunk_size = limit - offset
        chunk = query.offset(offset).limit(chunk_size).all()
        if not chunk:
            logger.info("No more chunks to fetch.")
            break
        count += 1
        results.extend(chunk)
        if count == 1:
            logger.info(f"Data type is {type(results[0])}")
        offset += chunk_size
        logger.info(f"Fetched {count} chunk. Current length of results is {len(results)}")

        if limit and len(results) >= limit:
            logger.info(f"Reached limit of {limit} results.")
            break

    logger.info(f"Retrieved {len(results)} results in total.")
    return results
    
def _get_distinct_liked_posts(db: Session) -> List[Feed]:
    query = (
        db.query(Feed.post_id, Feed.user_id)
        .filter(Feed.action == "like")
        .group_by(Feed.post_id, Feed.user_id).limit(1)
    )
    # liked_posts = _get_results_in_chunks(query,)
    liked_posts = query.all()
    print(liked_posts, file=open("liked_posts.txt", "w"))
    liked_posts = [
        Feed(**{key: value for key, value in post._asdict().items()})
        for post in liked_posts
    ]
    return liked_posts

def _get_processed_posts(db: Session) -> List[ProcessedPost]:
    query = db.query(ProcessedPost)
    return _get_results_in_chunks(query)

def _get_users(db: Session) -> List[User]:
    query = db.query(User)
    return _get_results_in_chunks(query)
    
def _load_features() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    try:
        db = SessionLocal()
        logger.info("Loading posts")
        posts = _get_processed_posts(db)     
        POSTS_COLUMNS = load_config(CONFIG_PATH).get("POSTS_COLUMNS")
        posts = pd.DataFrame([vars(post) for post in posts], columns=POSTS_COLUMNS)
        posts.to_parquet(posts_path)
        logger.info("Loading users")
        users = _get_users(db)
        USERS_COLUMNS = load_config(CONFIG_PATH).get("USERS_COLUMNS")
        users = pd.DataFrame([vars(user) for user in users], columns=USERS_COLUMNS)
        users.to_parquet(users_path)
        logger.info("Loading feed")
        feeds = _get_distinct_liked_posts(db)
        DISTINCT_USER_POST = load_config(CONFIG_PATH).get("DISTINCT_USER_POST")
        feeds = pd.DataFrame([vars(feed) for feed in feeds], columns=DISTINCT_USER_POST) 
        feeds.to_parquet(feeds_path)
        logger.info("Features loaded successfully.")
        return (feeds, posts, users)

    except Exception as e:
        logger.error(f"Error retrieving features: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

logger.info("Loading features")
feeds_path = os.path.join("data", "feeds.parquet")
posts_path = os.path.join("data", "posts.parquet")
users_path = os.path.join("data", "users.parquet")

try:
    feeds = pd.read_parquet(feeds_path)
    posts = pd.read_parquet(posts_path)
    users = pd.read_parquet(users_path)
except FileNotFoundError:
    logger.warning("Parquet file not found. Loading features from the database.")
    feeds, posts, users = _load_features()
        
logger.info("Service is up and running")

def _get_recommended_feed(user_id: int, time: datetime, limit: int) -> List[GetPost]:
    logger.info("Extracting month and hour")
    users['hour'] = time.hour
    users['month'] = time.month
    user = users[users['id'] == user_id].iloc[0:len(posts)].drop('id', axis=1)
    
    user = pd.concat([user] * len(posts), ignore_index=True)
    
    logger.info("Concatenating user with posts")
    df = pd.concat((user, posts), axis=1).set_index('id')

    COLUMN_MAPPING = load_config(CONFIG_PATH).get("COLUMN_MAPPING")
    df = df.rename(columns=COLUMN_MAPPING)
    logger.info("Rearranging columns order")
    TRAIN_SET_FEATURES = load_config(CONFIG_PATH).get("TRAIN_SET_FEATURES")
    TRAIN_SET_TYPES = load_config(CONFIG_PATH).get("TRAIN_SET_TYPES")
    valid_set = df[TRAIN_SET_FEATURES].astype(TRAIN_SET_TYPES)
    
    logger.info("Predicting")
    predicts = model.predict_proba(valid_set.drop('text', axis=1))[:, 1]
    valid_set["like_proba"] = predicts

  
    logger.info("Deleting liked posts")
    liked_posts = feeds[feeds.user_id == user_id]['post_id']
    filtered_ = valid_set[~valid_set.index.isin(liked_posts)]
    filtered_ = filtered_.reset_index()

    logger.info("Filtering liked posts")
    recommended_posts = filtered_.sort_values('like_proba')[-limit:].index

    return [
        GetPost(
            id=i,
            text=str(filtered_[filtered_['id'] == i]["text"]),  
            topic=str(filtered_[filtered_['id'] == i]["topic"]) 
        ) for i in recommended_posts
    ]


@app.get("/")
def check_status():
    return {"Status": "Ok"}

@app.get("/post/recommendations", response_model=List[GetPost])
def get_recommended_posts(
    user_id: int, 
    time: datetime, 
    limit: int = 10,
) -> List[GetPost]:
    return _get_recommended_feed(user_id, time, limit)

@app.get("/posts/{post_id}", response_model=GetPost)
async def get_post(
    post_id: int = Path(..., title="Post ID"), 
    db: Session = Depends(_get_db)
):
    logger.info(f"Retrieving post with ID: {post_id}")
    try:
        return db.query(Post).filter(Post.id == post_id).first()
    except Exception as e:
        logger.error(f"Error retrieving post with id {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/posts", response_model=List[GetPost])
async def get_posts(
    limit: Optional[int] = None,
    db: Session = Depends(_get_db)
):
    logger.info("Retrieving posts...")
    try:
        query = db.query(Post)
        return _get_results_in_chunks(query, limit)
    except Exception as e:
        logger.error(f"Error retrieving posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users/{user_id}", response_model=GetUser)
async def get_user(
    user_id: int = Path(..., title="User_ID"), 
    db: Session = Depends(_get_db)
):
    logger.info(f"Retrieving user with ID: {user_id}")
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error retrieving user with id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users", response_model=List[GetUser])
async def get_users(
    limit: Optional[int] = None,
    db: Session = Depends(_get_db)
):
    logger.info("Retrieving users...")
    try:
        query = db.query(User)
        return _get_results_in_chunks(query, limit)
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/feed", response_model=List[GetFeed])
async def get_feed(
    user_id: Optional[int] = None,
    post_id: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(_get_db),
):
    logger.info("Retrieving feed...")
    try:
        query = db.query(Feed)

        if user_id:
            logger.debug(f"Filtering feed by user_id: {user_id}")
            query = query.filter(Feed.user_id == user_id)
        if post_id:
            logger.debug(f"Filtering feed by post_id: {post_id}")
            query = query.filter(Feed.post_id == post_id)

        return _get_results_in_chunks(query, limit)

    except Exception as e:
        logger.error(f"Error retrieving feed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




