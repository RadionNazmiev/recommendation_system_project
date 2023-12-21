from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users_by_r_nazmiev"
    id = Column(Integer, primary_key=True)
    age: Column(Integer)
    city: Column(String)
    country: Column(String)
    exp_group: Column(Integer)
    gender: Column(Integer)
    os: Column(String)
    source: Column(String)

if __name__ == "__main__":
    Base.metadata.create_all(engine)