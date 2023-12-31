from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2, time
from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_URL =f"postgresql://{settings.database_username}:{settings.database_pass}@{settings.database_host}/{settings.database_name}"

engine= create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='meshmeshmesh'
#                             ,cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print('database connected succesfully')
#         break
#     except Exception as error:
#         print('connection failed: ',error)
#         time.sleep(3)
