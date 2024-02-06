import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'username': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

engine  = create_engine(URL.create(**DATABASE))

# Base = declarative_base()

# with engine.connect() as conn:
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f'{res=}')
