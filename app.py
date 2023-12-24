import os
from typing import List, Optional
from fastapi import FastAPI, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session
from loguru import logger

from database.database import SessionLocal
from database.models import User, Post, Feed
from database.schemas import GetPost, GetUser, GetFeed

app = FastAPI()

def get_db():
    try:
        with SessionLocal() as db:
            yield db
    except Exception as e:
        logger.error(f"Error getting database session: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
def check_status():
    return {"Status": "Ok"}

@app.get("/posts/{post_id}", response_model=GetPost) 
async def get_post(post_id: int = Path(..., title="Post ID"), db: Session = Depends(get_db)):
    try:
        return db.query(Post).filter(Post.id == post_id).first()
    except Exception as e:
        logger.error(f"Error retrieving post with id {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/posts", response_model=List[GetPost])
async def get_posts(db: Session = Depends(get_db)):
    try:
        return db.query(Post).all()
    except Exception as e:
        logger.error(f"Error retrieving posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users/{user_id}", response_model=GetUser)
async def get_user(user_id: int = Path(..., title="User_ID"), db: Session = Depends(get_db)):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error retrieving user with id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users", response_model=List[GetUser])
async def get_users(db: Session = Depends(get_db)):
    try:
        return db.query(User).all()
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/feed", response_model=List[GetFeed])
async def get_feed(
    user_id: Optional[int] = Query(None, description="ID of the user to filter the feed"),
    post_id: Optional[int] = Query(None, description="ID of the post to filter the feed"),
    limit: Optional[int] = Query(None, description="Limit of the posts to filter the feed"),
    db: Session = Depends(get_db)
):
    query = db.query(Feed)
    try:
        if user_id:
            query = query.filter(Feed.user_id == user_id)
        if post_id:
            query = query.filter(Feed.post_id == post_id)
        if limit:
            query = query.limit(limit)
        return query.all()
    except Exception as e:
        logger.error(f"Error retrieving feed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
