import os

from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd


app = FastAPI()

print("Connecting to database...")
# con = create_engine('postgresql://postgres:postgres@postgres_db:5432/postgres')
pg_host = os.getenv("PG_TEST_HOST")
pg_port = os.getenv("PG_TEST_PORT")
pg_user = os.getenv("PG_TEST_USER")
pg_pass = os.getenv("PG_TEST_PASS")

con = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/postgres')
df = pd.DataFrame({'id': [1, ], 'text': ["test", ], "topic": ["test",]})
df.to_sql("test", con, if_exists='append', index=False)
print("upload complete")

@app.get("/")
def check_status():
    return {"Status": "Ok"}


