import os
from typing import List, Optional

from fastapi import FastAPI, Depends, Path, Query
from sqlalchemy import select

# import pandas as pd
# from loguru import logger
# from sqlalchemy.orm import Session
# from catboost import CatBoostClassifier
# from psycopg2.extras import RealDictCursor
# import psycopg2

from database.database import SessionLocal
from database.models import User, Post, Feed
from database.schemas import GetPost, GetUser, GetFeed


def get_db():
    with SessionLocal() as db:
        return db
    # conn = psycopg2.connect(
    #     "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
    #     cursor_factory=RealDictCursor
    # )
    # return conn


app = FastAPI()


@app.get("/")
def check_status():
    return {"Status": "Ok"}


@app.get("/posts/{post_id}", response_model = GetPost) 
async def get_post(post_id: int = Path(..., title = "Post ID"), db = Depends(get_db)):
    return db.query(Post).filter(Post.id == post_id).all()[0]
    
    
    # with db.cursor() as cursor:
    #     query = """
    #         SELECT post_id as id, *
    #         FROM public.post_text_df
    #         WHERE post_id = %s
    #     """
    #     cursor.execute(query, (post_id,))
    #     post = cursor.fetchone() 
    # if not post:
    #     raise HTTPException(status_code=404, detail="Post not found")
    # logger.info(post)
    # return GetPost(**post)


@app.get("/posts", response_model = List[GetPost])
async def get_posts(db = Depends(get_db)):
    return db.query(Post).all()
    
    # with db.cursor() as cursor:
    #     query = """
    #         SELECT post_id as id, *
    #         FROM public.post_text_df
    #         LIMIT 3
    #     """
    #     cursor.execute(query)
    #     posts = cursor.fetchall() 
    # if not posts:
    #     raise HTTPException(status_code=404, detail="Posts not found")
    # return [GetPost(**post) for post in posts]


@app.get("/users/{user_id}", response_model = GetUser)
async def get_user(user_id: int = Path(..., title = "User_ID"), db = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).all()[0]

    # with db.cursor() as cursor:
    #     query = """
    #         SELECT user_id as id, *
    #         FROM public.user_data
    #         WHERE user_id = %s
    #     """
    #     cursor.execute(query, (user_id,))
    #     user = cursor.fetchone()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    # logger.info(user)
    # return GetUser(**user)
    
@app.get("/users", response_model = List[GetUser])
async def get_users(db = Depends(get_db)):
    return db.query(User).all()
    
    # with db.cursor() as cursor:
    #     query = """
    #         SELECT user_id as id, *
    #         FROM public.user_data
    #         LIMIT 2
    #     """
    #     cursor.execute(query)
    #     users = cursor.fetchall()
    # if not users:
    #     raise HTTPException(status_code=404, detail="Users not found")
    # logger.info(users)
    # return [GetUser(**user) for user in users]


@app.get("/feed", response_model = List[GetFeed])
def get_feed(
    user_id: Optional[int] = Query(None, description="ID of the user to filter the feed"),
    post_id: Optional[int] = Query(None, description="ID of the post to filter the feed"),
    limit: int = 10,
    db = Depends(get_db)
):
    # query = select(Feed)
    query = db.query(Feed)

    if user_id is not None:
        query = query.filter(Feed.user_id == user_id)
    elif post_id is not None:
        query = query.filter(Feed.post_id == post_id)

    if limit is not None:
        query = query.limit(limit)

    # return db.execute(query).all()
    return query.all()


    # query = """
    #     SELECT * FROM public.feed_data 
    # """
    
    # conditions = []
    
    # if user_id:
    #     conditions.append("user_id = %s")
    # if post_id:
    #     conditions.append("post_id = %s")
    # if conditions:
    #     query += " WHERE " + " AND ".join(conditions)
    # query += " LIMIT 10"   
    # logger.info(query)
    
    # with db.cursor() as cursor:
    #     cursor.execute(query, (user_id, post_id)) 
    #     feeds = cursor.fetchall()

    # if not feeds:
    #     raise HTTPException(status_code=404, detail="Feeds not found")
        
    # logger.info(feeds)
    # return [GetFeed(**feed) for feed in feeds]

    

# def get_model_path(path: str) -> str:
#     if os.environ.get("IS_LMS") == "1": 
#         MODEL_PATH = '/workdir/user_input/model'
#     else:
#         MODEL_PATH = path
#     return MODEL_PATH

# def load_models() -> CatBoostClassifier:
#     model_path = get_model_path("")
#     model = pickle.load(model_path) # пример как можно загружать модели
#     return model


# def batch_load_sql(query: str) -> pd.DataFrame:
#     global ENGINE
#     CHUNKSIZE = 200000
#     conn = engine.connect().execution_options(stream_results=True)
#     chunks = []
#     for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
#         chunks.append(chunk_dataframe)
#     conn.close()
#     return pd.concat(chunks, ignore_index=True)

# def load_features():
#     pass






























    