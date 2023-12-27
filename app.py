import os
from typing import List, Optional
from datetime import datetime
import pandas as pd
import pyarrow.parquet as pq

from fastapi import FastAPI, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session, Query
from sqlalchemy import create_engine
from sqlalchemy.engine.row import Row
from loguru import logger
from catboost import CatBoostClassifier
import logging
from pprint import pformat

from database.database import SessionLocal
from database.models import User, Post, Feed, ProcessedPost
from database.schemas import GetPost, GetUser, GetFeed, GetProcessedPost
from config.config import COLUMNS

app = FastAPI()

def _get_db():
    try:
        with SessionLocal() as db:
            yield db
    except Exception as e:
        logger.error(f"Error getting database session: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def _get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH

def _load_model():
    logger.info("Getting model path")
    model_path = _get_model_path(os.path.join(os.getcwd(),"catboost_model"))
    logger.info("Initializing and loading model")
    loaded_model = CatBoostClassifier().load_model(model_path)
    logger.info("Model loaded")

logger.info("\nLoading model")
model = _load_model()

def _get_results_in_chunks(query, limit=None, chunk_size=500000):
    logger.info("Starting result retrieval in chunks...")
    count = 0
    offset = 0
    results = []
    while True:
        if limit and (limit - offset) < chunk_size:
            logger.info(f"Adjusting chunk size to {limit - offset} due to limit")
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
        .group_by(Feed.post_id, Feed.user_id)
    )
    liked_posts = _get_results_in_chunks(query,limit=100)
    liked_posts = [
        Feed(**{key: value for key, value in post._asdict().items()}) 
        for post in liked_posts
    ]
    return liked_posts

def _get_processed_posts(db: Session) -> List[ProcessedPost]:
    query = db.query(ProcessedPost)
    return _get_results_in_chunks(query,limit=100)

def _get_users(db: Session) -> List[User]:
    query = db.query(User)
    return _get_results_in_chunks(query, limit=100)
    
def _load_features() -> (List[Feed], List[ProcessedPost], List[User]):
    try:
        db = SessionLocal()
        logger.info("\nLoading feed")
        feed = _get_distinct_liked_posts(db)
        logger.info("\nLoading posts")
        posts = _get_processed_posts(db)
        logger.info("\nLoading users")
        users = _get_users(db)
        logger.info("Features loaded successfully.")
        return (feed, posts, users)

    except Exception as e:
        logger.error(f"Error retrieving features: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

logger.info("\nLoading features")
feed, posts, users = _load_features()
logger.info("\nService is up and running")

def _get_recommended_feed(user_id: int, time: datetime, limit: int):
    logger.info("Reading user features")
    user_features = [
        User(**{key: value for key, value in user.__dict__.items() if key != "id"}) 
        for user in users if user.id == user_id
    ]
    
    logger.info("Reading post features")
    post_features = [
        ProcessedPost(**{key: value for key, value in post.__dict__.items() if key != "_sa_instance_state"}) 
        for post in posts
    ]

    logger.info("Reading feed features")

    feed_features = [
        {**item['processed_post'].__dict__, **item['user'].__dict__} 
        for item in feed if item.user_id == user_id
    ]
    
    logger.info(f"Length of feed_features: {len(feed_features)}")
    
    if feed_features:
        logger.info(f"feed_features dir {dir(feed_features[0])}")
    else:
        logger.warning("feed_features is empty")
    
    # df = pd.DataFrame(columns=COLUMNS, index=['user_id', 'post_id'])

    # for item in feed_features:
    #     for col in COLUMN:
    #         df.iloc[[item['user_id'], item['post_id']]][col] =
            
    
    logger.info("Zipping everything")
    add_user_features = dict(zip(user_features.columns, user_features.values[0]))
    logger.info("assigning everything")
    user_posts_features = posts_features.assign(**add_user_features)
    user_posts_features = user_posts_features.set_index('post_id')

    # Добафим информацию о дате рекомендаций
    logger.info("add time info")
    user_posts_features['hour'] = time.hour
    user_posts_features['month'] = time.month

    # Сформируем предсказания вероятности лайкнуть пост для всех постов
    logger.info("predicting")
    predicts = model.predict_proba(user_posts_features)[:, 1]
    user_posts_features["predicts"] = predicts

    # Уберем записи, где пользователь ранее уже ставил лайк
    logger.info("deleting liked posts")
    liked_posts = features[0]
    liked_posts = liked_posts[liked_posts.user_id == id].post_id.values
    filtered_ = user_posts_features[~user_posts_features.index.isin(liked_posts)]

    # Рекомендуем топ-5 по вероятности постов
    recommended_posts = filtered_.sort_values('predicts')[-limit:].index

    return [GetPost(**{"id": i, "text": "gay", "topic": "unpleasant"}) for i in recommended_posts]


@app.get("/")
def check_status():
    return {"Status": "Ok"}

app = FastAPI()

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




