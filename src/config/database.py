import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_config = {"user": 'root', "password": 'root', "host": 'mariadb', "port": '3306', "database": 'goorm'}
# db_config = {"user": 'root', "password": 'root', "host": '127.0.0.1', "port": '3306', "database": 'goorm'}

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_config.get('user')}:{db_config.get('password')}@{db_config.get('host')}:{db_config.get('port')}/{db_config.get('database')}?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
