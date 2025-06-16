from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

db_url = os.getenv("DATABASE_URL")

#give deals give db entirely from creating table to commit to etc.
engine = create_engine(db_url,connect_args={"check_same_thread":False})
#this provides the db instance at the particular time through engine
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)
#isse auto commit toh chalme on off kar sakta hu
#base specifies the schema of DB to the python class of data base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()