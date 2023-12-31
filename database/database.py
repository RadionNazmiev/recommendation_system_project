import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

from config.config import PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_DATABASE


URL = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"


engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


if __name__ == "__main__":
    from config.utils import load_config
    d = load_config(os.path.join("config", "config.yaml"))
    print(d)
    print(PG_USER)


